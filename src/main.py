#!/usr/bin/env python3
"""
Main entry point for dirclean CLI.
Handles command parsing and dispatching to the appropriate "ops module"= corresponding function.
"""

import argparse
from ops.scan import cmd_scan
from ops.dedupe import cmd_dedupe
from ops.archive import cmd_archive
from ops.organize import cmd_organize

def build_parser():
    """Builds the CLI parser with all subcommands and options."""
    p = argparse.ArgumentParser(
        prog="dirclean",
        description="Unix directory cleanup CLI (safe by default).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # scan command / flags
    s = sub.add_parser("scan", help="Report sizes, largest files, duplicate candidates.")
    s.add_argument("path")
    s.add_argument("--top", type=int, default=20)
    s.add_argument("--hash", action="store_true")
    s.add_argument("--include", action="append", default=[])
    s.add_argument("--exclude", action="append", default=[])
    s.add_argument("--dry-run", action="store_true")

    # dedupe (de-duplication) command / flags
    d = sub.add_parser("dedupe", help="Hard-link or delete exact duplicates.")
    d.add_argument("path")
    d.add_argument("--action", choices=["link", "delete"], default="link")
    d.add_argument("--hash", choices=["sha256"], default="sha256")
    d.add_argument("--include", action="append", default=[])
    d.add_argument("--exclude", action="append", default=[])
    d.add_argument("--dry-run", action="store_true")

    # archive command / flags
    a = sub.add_parser("archive", help="Tar+gzip files older than a threshold.")
    a.add_argument("path")
    a.add_argument("--older-than", required=True, help="e.g., 90d or 12m")
    a.add_argument("--dest", default="~/Archives")
    a.add_argument("--include", action="append", default=[])
    a.add_argument("--exclude", action="append", default=[])
    a.add_argument("--dry-run", action="store_true")

    # organize command / flags
    o = sub.add_parser("organize", help="Group files by type or date.")
    o.add_argument("path")
    o.add_argument("--by", choices=["type", "date"], default="type")
    o.add_argument("--dest", default=None)
    o.add_argument("--include", action="append", default=[])
    o.add_argument("--exclude", action="append", default=[])
    o.add_argument("--dry-run", action="store_true")

    return p

def main():
    """Parses CLI arguments and dispatches to command handlers."""
    args = build_parser().parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "dedupe":
        cmd_dedupe(args)
    elif args.command == "archive":
        cmd_archive(args)
    elif args.command == "organize":
        cmd_organize(args)

if __name__ == "__main__":
    main()
