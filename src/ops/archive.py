"""
Implements 'archive' command for dirclean.
"""

import os, tarfile, time
from datetime import datetime, timedelta
from .common import iter_files

def parse_age(expr):
    """Parse string like '90d' or '12m' into seconds."""
    unit = expr[-1]
    num = int(expr[:-1])
    if unit == 'd':
        return num*86400
    if unit == 'm':
        return num*2592000
    raise ValueError("bad expr")


def cmd_archive(args):
    files = list(iter_files(args.path, args.include, args.exclude))
    cutoff = time.time() - parse_age(args.older_than)
    old_files = [f for f in files if os.path.getmtime(f) < cutoff]
    if not old_files:
        print("No old files to archive.")
        return

    dest = os.path.expanduser(args.dest)
    os.makedirs(dest, exist_ok=True)
    archive_path = os.path.join(dest, f"archive_{int(time.time())}.tar.gz")

    if args.dry_run:
        print(f"Would archive {len(old_files)} files into {archive_path}")
        return

    with tarfile.open(archive_path, "w:gz") as tar:
        for f in old_files:
            tar.add(f)
            print(f"Archived {f}")
