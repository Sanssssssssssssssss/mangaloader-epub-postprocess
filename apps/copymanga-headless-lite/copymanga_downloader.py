#!/usr/bin/env python3
"""Small Linux-friendly CopyManga downloader for chapter image folders."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_API_DOMAIN = "api.2025copy.com"
RETRYABLE_HTTP_CODES = {408, 425, 429, 500, 502, 503, 504}
DEFAULT_HEADERS = {
    "User-Agent": "COPY/3.0.0",
    "Accept": "application/json",
    "version": "2025.08.15",
    "platform": "1",
    "webp": "1",
    "region": "1",
}
IMAGE_HEADERS = {"User-Agent": "COPY/3.0.0"}


class DownloaderError(RuntimeError):
    """Base error for the lightweight downloader."""


class ApiRequestError(DownloaderError):
    """Raised when the API or image host returns an unrecoverable error."""


class AuthError(ApiRequestError):
    """Raised when token-authenticated content rejects the provided token."""


class RiskControlError(ApiRequestError):
    """Raised when the upstream indicates rate limiting or anti-bot control."""


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name).strip()
    return cleaned.rstrip(". ") or "untitled"


def build_headers(token: str | None = None) -> dict[str, str]:
    headers = dict(DEFAULT_HEADERS)
    if token:
        headers["authorization"] = f"Token {token}"
    return headers


def backoff_sleep(base_sec: float, jitter_sec: float, attempt: int) -> None:
    delay = max(base_sec, 0.0)
    if attempt > 0:
        delay *= attempt + 1
    if jitter_sec > 0:
        delay += random.uniform(0.0, jitter_sec)
    if delay > 0:
        time.sleep(delay)


def api_get_json(
    path: str,
    *,
    params: dict[str, object] | None = None,
    token: str | None = None,
    api_domain: str = DEFAULT_API_DOMAIN,
    timeout: int = 15,
    retries: int = 3,
    retry_base_sec: float = 1.0,
    retry_jitter_sec: float = 0.5,
    risk_wait_sec: float = 60.0,
) -> dict[str, object]:
    query = urllib.parse.urlencode(params or {})
    url = f"https://{api_domain}{path}"
    if query:
        url = f"{url}?{query}"
    last_error: Exception | None = None

    for attempt in range(max(retries, 0) + 1):
        request = urllib.request.Request(url, headers=build_headers(token))
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 401:
                raise AuthError(f"API request failed: {path} -> HTTP 401: token invalid or expired") from exc
            if exc.code == 210:
                last_error = RiskControlError(f"API request hit risk control: {path} -> HTTP 210: {detail[:300]}")
                if attempt < max(retries, 0):
                    time.sleep(max(risk_wait_sec, 0.0))
                    continue
                raise last_error from exc
            if exc.code in RETRYABLE_HTTP_CODES and attempt < max(retries, 0):
                last_error = ApiRequestError(f"API request failed: {path} -> HTTP {exc.code}: {detail[:300]}")
                backoff_sleep(retry_base_sec, retry_jitter_sec, attempt)
                continue
            raise ApiRequestError(f"API request failed: {path} -> HTTP {exc.code}: {detail[:300]}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = ApiRequestError(f"API request failed: {path} -> {exc}")
            if attempt < max(retries, 0):
                backoff_sleep(retry_base_sec, retry_jitter_sec, attempt)
                continue
            raise last_error from exc

        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ApiRequestError(f"API response was not valid JSON for {path}") from exc

        code = payload.get("code")
        if code == 200:
            results = payload.get("results")
            if not isinstance(results, dict):
                raise ApiRequestError(f"API results for {path} were not an object")
            return results

        message = str(payload.get("message", ""))
        if code == 210:
            last_error = RiskControlError(f"API returned risk control for {path}: {message}")
            if attempt < max(retries, 0):
                time.sleep(max(risk_wait_sec, 0.0))
                continue
            raise last_error
        raise ApiRequestError(f"API returned unexpected code for {path}: {code} {message}")

    raise ApiRequestError(f"API request failed after retries: {path}") from last_error


def search(keyword: str, page: int, limit: int, api_domain: str, request_options: dict[str, object]) -> dict[str, object]:
    offset = max(page - 1, 0) * limit
    return api_get_json(
        "/api/v3/search/comic",
        params={"limit": limit, "offset": offset, "q": keyword, "q_type": "", "platform": 1},
        api_domain=api_domain,
        **request_options,
    )


def get_comic(comic_path_word: str, api_domain: str, request_options: dict[str, object]) -> dict[str, object]:
    return api_get_json(
        f"/api/v3/comic2/{comic_path_word}",
        params={"platform": 1},
        api_domain=api_domain,
        **request_options,
    )


def get_group_chapters(
    comic_path_word: str,
    group_path_word: str,
    api_domain: str,
    request_options: dict[str, object],
) -> list[dict[str, object]]:
    limit = 100
    offset = 0
    items: list[dict[str, object]] = []
    while True:
        page = api_get_json(
            f"/api/v3/comic/{comic_path_word}/group/{group_path_word}/chapters",
            params={"limit": limit, "offset": offset},
            api_domain=api_domain,
            **request_options,
        )
        page_items = page.get("list") or []
        if not isinstance(page_items, list):
            raise ApiRequestError("Chapter list response was malformed")
        items.extend(page_items)
        total = int(page.get("total") or 0)
        offset += limit
        if offset >= total or not page_items:
            break
    return items


def get_chapter(
    comic_path_word: str,
    chapter_uuid: str,
    *,
    token: str | None,
    api_domain: str,
    request_options: dict[str, object],
) -> dict[str, object]:
    return api_get_json(
        f"/api/v3/comic/{comic_path_word}/chapter2/{chapter_uuid}",
        params={"platform": 1},
        token=token,
        api_domain=api_domain,
        **request_options,
    )


def format_output(data: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if isinstance(data, list):
        for item in data:
            print(item)
        return
    print(data)


def comic_group_map(comic_results: dict[str, object]) -> dict[str, dict[str, object]]:
    groups = comic_results.get("groups") or {}
    if not isinstance(groups, dict):
        raise ApiRequestError("Comic groups were malformed")
    return groups


def choose_group_title(comic_results: dict[str, object], group_path_word: str) -> str:
    groups = comic_group_map(comic_results)
    group = groups.get(group_path_word) or {}
    name = group.get("name")
    if isinstance(name, str) and name.strip():
        return name
    return group_path_word


def upgrade_image_url(url: str) -> str:
    return url.replace(".c800x.", ".c1500x.")


def fetch_image_bytes(
    url: str,
    *,
    timeout: int = 30,
    retries: int = 3,
    retry_base_sec: float = 1.0,
    retry_jitter_sec: float = 0.5,
) -> tuple[bytes, str]:
    last_error: Exception | None = None

    for attempt in range(max(retries, 0) + 1):
        request = urllib.request.Request(url, headers=IMAGE_HEADERS)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
                data = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = ApiRequestError(f"Image request failed: {url} -> HTTP {exc.code}: {detail[:300]}")
            if exc.code in RETRYABLE_HTTP_CODES and attempt < max(retries, 0):
                backoff_sleep(retry_base_sec, retry_jitter_sec, attempt)
                continue
            raise last_error from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = ApiRequestError(f"Image request failed: {url} -> {exc}")
            if attempt < max(retries, 0):
                backoff_sleep(retry_base_sec, retry_jitter_sec, attempt)
                continue
            raise last_error from exc

        ext = {
            "image/webp": "webp",
            "image/jpeg": "jpg",
        }.get(content_type)
        if not ext:
            raise ApiRequestError(f"Unsupported image content type: {content_type or 'missing'}")
        return data, ext

    raise ApiRequestError(f"Image request failed after retries: {url}") from last_error


def download_one_image(
    url: str,
    output_path: Path,
    skip_existing: bool,
    *,
    image_timeout_sec: int,
    api_retries: int,
    retry_base_sec: float,
    retry_jitter_sec: float,
    image_interval_sec: float,
) -> str:
    if skip_existing and output_path.exists():
        return f"SKIP {output_path.name}"
    data, ext = fetch_image_bytes(
        url,
        timeout=image_timeout_sec,
        retries=api_retries,
        retry_base_sec=retry_base_sec,
        retry_jitter_sec=retry_jitter_sec,
    )
    if output_path.suffix.lower() != f".{ext}":
        output_path = output_path.with_suffix(f".{ext}")
    output_path.write_bytes(data)
    if image_interval_sec > 0:
        time.sleep(image_interval_sec)
    return f"OK {output_path.name}"


def chapter_folder_name(chapter: dict[str, object]) -> str:
    index = int(chapter.get("index") or 0) + 1
    name = str(chapter.get("name") or "chapter")
    return f"{index:04d} {sanitize_filename(name)}"


def collect_page_jobs(chapter_results: dict[str, object], max_images: int | None) -> list[tuple[str, int]]:
    chapter = chapter_results.get("chapter") or {}
    contents = chapter.get("contents") or []
    if not isinstance(contents, list):
        raise SystemExit("Chapter contents were malformed")
    jobs: list[tuple[str, int]] = []
    for idx, content in enumerate(contents, start=1):
        if not isinstance(content, dict):
            continue
        url = str(content.get("url") or "")
        if not url:
            continue
        jobs.append((upgrade_image_url(url), idx))
    if max_images is not None:
        jobs = jobs[: max(max_images, 0)]
    return jobs


def chapter_output_dir(output_root: Path, comic_title: str, group_title: str, chapter: dict[str, object]) -> Path:
    return output_root / sanitize_filename(comic_title) / sanitize_filename(group_title) / chapter_folder_name(chapter)


def download_chapter_to_dir(
    *,
    output_root: Path,
    comic_title: str,
    group_title: str,
    chapter: dict[str, object],
    chapter_results: dict[str, object],
    image_workers: int,
    skip_existing: bool,
    max_images: int | None,
    image_timeout_sec: int,
    api_retries: int,
    retry_base_sec: float,
    retry_jitter_sec: float,
    image_interval_sec: float,
) -> Path:
    destination = chapter_output_dir(output_root, comic_title, group_title, chapter)
    destination.mkdir(parents=True, exist_ok=True)
    jobs = collect_page_jobs(chapter_results, max_images)
    if not jobs:
        raise SystemExit("No image URLs were found for the requested chapter")

    def worker(job: tuple[str, int]) -> str:
        url, index = job
        return download_one_image(
            url,
            destination / f"{index:04d}.webp",
            skip_existing,
            image_timeout_sec=image_timeout_sec,
            api_retries=api_retries,
            retry_base_sec=retry_base_sec,
            retry_jitter_sec=retry_jitter_sec,
            image_interval_sec=image_interval_sec,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(image_workers, 1)) as executor:
        results = list(executor.map(worker, jobs))

    print(f"Downloaded {len(results)} pages -> {destination}")
    return destination


def cmd_search(args: argparse.Namespace) -> int:
    results = search(args.keyword, args.page, args.limit, args.api_domain, request_options(args))
    rows = []
    for item in results.get("list") or []:
        rows.append(
            {
                "name": item.get("name"),
                "path_word": item.get("path_word"),
                "popular": item.get("popular"),
            }
        )
    format_output(rows, args.json)
    return 0


def cmd_comic(args: argparse.Namespace) -> int:
    results = get_comic(args.comic_path_word, args.api_domain, request_options(args))
    comic = results.get("comic") or {}
    groups = comic_group_map(results)
    payload = {
        "name": comic.get("name"),
        "path_word": comic.get("path_word"),
        "author": [author.get("name") for author in comic.get("author") or [] if isinstance(author, dict)],
        "groups": [
            {
                "path_word": key,
                "name": value.get("name"),
                "count": value.get("count"),
            }
            for key, value in groups.items()
        ],
    }
    format_output(payload, args.json)
    return 0


def cmd_chapters(args: argparse.Namespace) -> int:
    chapters = get_group_chapters(args.comic_path_word, args.group, args.api_domain, request_options(args))
    rows = [
        {
            "index": chapter.get("index"),
            "ordered": chapter.get("ordered"),
            "name": chapter.get("name"),
            "uuid": chapter.get("uuid"),
        }
        for chapter in chapters
    ]
    format_output(rows, args.json)
    return 0


def cmd_download_chapter(args: argparse.Namespace) -> int:
    comic_results = get_comic(args.comic_path_word, args.api_domain, request_options(args))
    chapter_results = get_chapter(
        args.comic_path_word,
        args.chapter_uuid,
        token=args.token or os.getenv("COPYMANGA_TOKEN"),
        api_domain=args.api_domain,
        request_options=request_options(args),
    )
    comic = chapter_results.get("comic") or {}
    chapter = chapter_results.get("chapter") or {}
    group_title = choose_group_title(comic_results, str(chapter.get("group_path_word") or "default"))
    download_chapter_to_dir(
        output_root=Path(args.output_root).resolve(),
        comic_title=str(comic.get("name") or args.comic_path_word),
        group_title=group_title,
        chapter=chapter,
        chapter_results=chapter_results,
        image_workers=args.image_workers,
        skip_existing=args.skip_existing,
        max_images=args.max_images,
        image_timeout_sec=args.image_timeout_sec,
        api_retries=args.api_retries,
        retry_base_sec=args.retry_base_sec,
        retry_jitter_sec=args.retry_jitter_sec,
        image_interval_sec=args.image_interval_sec,
    )
    return 0


def cmd_download_group(args: argparse.Namespace) -> int:
    comic_results = get_comic(args.comic_path_word, args.api_domain, request_options(args))
    comic = comic_results.get("comic") or {}
    comic_title = str(comic.get("name") or args.comic_path_word)
    group_title = choose_group_title(comic_results, args.group)

    chapters = get_group_chapters(args.comic_path_word, args.group, args.api_domain, request_options(args))
    if args.reverse:
        chapters = list(reversed(chapters))
    if args.limit is not None:
        chapters = chapters[: max(args.limit, 0)]
    if not chapters:
        raise SystemExit("No chapters matched the requested group selection")

    token = args.token or os.getenv("COPYMANGA_TOKEN")
    output_root = Path(args.output_root).resolve()
    total = len(chapters)
    for index, chapter in enumerate(chapters, start=1):
        chapter_uuid = str(chapter.get("uuid") or "")
        if not chapter_uuid:
            continue
        print(f"[{index}/{total}] {chapter.get('name')} ({chapter_uuid})")
        chapter_results = get_chapter(
            args.comic_path_word,
            chapter_uuid,
            token=token,
            api_domain=args.api_domain,
            request_options=request_options(args),
        )
        download_chapter_to_dir(
            output_root=output_root,
            comic_title=comic_title,
            group_title=group_title,
            chapter=chapter,
            chapter_results=chapter_results,
            image_workers=args.image_workers,
            skip_existing=args.skip_existing,
            max_images=args.max_images,
            image_timeout_sec=args.image_timeout_sec,
            api_retries=args.api_retries,
            retry_base_sec=args.retry_base_sec,
            retry_jitter_sec=args.retry_jitter_sec,
            image_interval_sec=args.image_interval_sec,
        )
        if index < total and args.chapter_interval_sec > 0:
            time.sleep(args.chapter_interval_sec)
    return 0


def request_options(args: argparse.Namespace) -> dict[str, object]:
    return {
        "timeout": args.api_timeout_sec,
        "retries": args.api_retries,
        "retry_base_sec": args.retry_base_sec,
        "retry_jitter_sec": args.retry_jitter_sec,
        "risk_wait_sec": args.risk_wait_sec,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small headless downloader for CopyManga chapter image folders")
    parser.add_argument("--api-domain", default=DEFAULT_API_DOMAIN, help=f"API domain, default: {DEFAULT_API_DOMAIN}")
    parser.add_argument("--api-timeout-sec", type=int, default=15, help="Per-request API timeout in seconds")
    parser.add_argument("--image-timeout-sec", type=int, default=30, help="Per-request image timeout in seconds")
    parser.add_argument("--api-retries", type=int, default=5, help="Retry count for API and image requests")
    parser.add_argument("--retry-base-sec", type=float, default=1.0, help="Base retry delay in seconds")
    parser.add_argument("--retry-jitter-sec", type=float, default=0.5, help="Random retry jitter in seconds")
    parser.add_argument("--risk-wait-sec", type=float, default=60.0, help="Wait time after HTTP/code 210 risk control")
    parser.add_argument("--chapter-interval-sec", type=float, default=0.0, help="Sleep between chapters")
    parser.add_argument("--image-interval-sec", type=float, default=0.0, help="Sleep after each image download")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search comics")
    search_parser.add_argument("keyword")
    search_parser.add_argument("--page", type=int, default=1)
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--json", action="store_true")
    search_parser.set_defaults(func=cmd_search)

    comic_parser = subparsers.add_parser("comic", help="Show comic metadata and groups")
    comic_parser.add_argument("comic_path_word")
    comic_parser.add_argument("--json", action="store_true")
    comic_parser.set_defaults(func=cmd_comic)

    chapters_parser = subparsers.add_parser("chapters", help="List chapters for one group")
    chapters_parser.add_argument("comic_path_word")
    chapters_parser.add_argument("--group", required=True, help="Group path word, for example: default")
    chapters_parser.add_argument("--json", action="store_true")
    chapters_parser.set_defaults(func=cmd_chapters)

    chapter_dl = subparsers.add_parser("download-chapter", help="Download one chapter to an image folder")
    chapter_dl.add_argument("comic_path_word")
    chapter_dl.add_argument("--chapter-uuid", required=True)
    chapter_dl.add_argument("--output-root", required=True)
    chapter_dl.add_argument("--token", help="Optional CopyManga token, or set COPYMANGA_TOKEN")
    chapter_dl.add_argument("--image-workers", type=int, default=8)
    chapter_dl.add_argument("--max-images", type=int, help="Optional smoke-test limit for pages to download")
    chapter_dl.add_argument("--skip-existing", action="store_true")
    chapter_dl.set_defaults(func=cmd_download_chapter)

    group_dl = subparsers.add_parser("download-group", help="Download multiple chapters from one group")
    group_dl.add_argument("comic_path_word")
    group_dl.add_argument("--group", required=True, help="Group path word, for example: default")
    group_dl.add_argument("--output-root", required=True)
    group_dl.add_argument("--limit", type=int, help="Optional number of chapters to download from the current ordering")
    group_dl.add_argument("--reverse", action="store_true", help="Reverse the chapter order before applying --limit")
    group_dl.add_argument("--token", help="Optional CopyManga token, or set COPYMANGA_TOKEN")
    group_dl.add_argument("--image-workers", type=int, default=8)
    group_dl.add_argument("--max-images", type=int, help="Optional smoke-test limit for pages per chapter")
    group_dl.add_argument("--skip-existing", action="store_true")
    group_dl.set_defaults(func=cmd_download_group)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except DownloaderError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
