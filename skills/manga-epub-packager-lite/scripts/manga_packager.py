#!/usr/bin/env python3
"""Linux-friendly manga packaging helper for chapter EPUB creation and optional merge."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def natural_key(text: str) -> list[object]:
    import re

    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", text)]


def find_kcc(explicit: str | None, dry_run: bool) -> str:
    if explicit:
        return explicit

    for candidate in ("kcc-c2e", "comic2ebook"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved

    if dry_run:
        return "kcc-c2e"

    raise SystemExit("KCC not found. Install `kcc-c2e` or `comic2ebook`, or pass --kcc-cmd.")


def run_command(command: list[str], dry_run: bool) -> None:
    print("RUN:", " ".join(command))
    if dry_run:
        return
    subprocess.run(command, check=True)


def chapter_dirs(input_root: Path) -> list[Path]:
    if not input_root.is_dir():
        raise SystemExit(f"Input root not found: {input_root}")
    chapters = [path for path in input_root.iterdir() if path.is_dir()]
    if not chapters:
        raise SystemExit(f"No chapter directories found in: {input_root}")
    return sorted(chapters, key=lambda p: natural_key(p.name))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Package manga chapter folders into EPUB and optionally merge them into one anthology"
    )
    parser.add_argument("--input-root", required=True, help="Directory containing chapter folders")
    parser.add_argument("--output-root", required=True, help="Directory where chapter EPUBs will be written")
    parser.add_argument("--kcc-cmd", help="Explicit KCC command path or name")
    parser.add_argument("--profile", default="KS", help="KCC device profile, default: KS")
    parser.add_argument("--title", help="Merged anthology title when --merge-output is used")
    parser.add_argument("--author", default="Unknown", help="Merged anthology author")
    parser.add_argument("--language", default="zh", help="Merged anthology language metadata")
    parser.add_argument("--description", default="", help="Merged anthology description metadata")
    parser.add_argument("--contributor", default="manga-epub-packager-lite", help="Merged anthology contributor")
    parser.add_argument("--merge-output", help="Optional final merged EPUB path")
    parser.add_argument("--order-file", help="Optional plain-text or JSON order file for merge")
    parser.add_argument("--plan-path", help="Optional path for generated merge-plan JSON")
    parser.add_argument("--skip-existing", action="store_true", help="Skip chapter packaging if <chapter>.epub exists")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them")
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="Extra argument to append to the KCC command. Repeat as needed.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    input_root = Path(args.input_root).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    kcc_cmd = find_kcc(args.kcc_cmd, args.dry_run)
    chapters = chapter_dirs(input_root)

    for chapter in chapters:
        expected_output = output_root / f"{chapter.name}.epub"
        if args.skip_existing and expected_output.exists():
            print(f"SKIP: {expected_output}")
            continue

        command = [
            kcc_cmd,
            "-p",
            args.profile,
            "-f",
            "EPUB",
            "--nokepub",
            "-n",
            "--forcecolor",
            "-o",
            str(output_root),
            str(chapter),
        ]
        command.extend(args.extra_arg)
        run_command(command, args.dry_run)

    if not args.merge_output:
        return 0

    if not args.title:
        raise SystemExit("--title is required when --merge-output is used")

    script_dir = Path(__file__).resolve().parent
    plan_path = Path(args.plan_path).resolve() if args.plan_path else output_root / "merge-plan.json"

    plan_command = [
        sys.executable,
        str(script_dir / "make_merge_plan.py"),
        "--epub-dir",
        str(output_root),
        "--output",
        str(Path(args.merge_output).resolve()),
        "--title",
        args.title,
        "--author",
        args.author,
        "--language",
        args.language,
        "--description",
        args.description,
        "--contributor",
        args.contributor,
        "--plan",
        str(plan_path),
    ]
    if args.order_file:
        plan_command.extend(["--order-file", str(Path(args.order_file).resolve())])
    run_command(plan_command, args.dry_run)

    merge_command = [
        sys.executable,
        str(script_dir / "merge_epub_by_order.py"),
        "--plan",
        str(plan_path),
    ]
    run_command(merge_command, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
