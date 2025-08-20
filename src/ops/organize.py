"""
Implements 'organize' command: group files by type or date.
"""

import os, shutil
from datetime import datetime
from .common import iter_files

def cmd_organize(args):
    files = list(iter_files(args.path, args.include, args.exclude))
    dest_root = args.dest or args.path

    for f in files:
        if args.by == "type":
            ext = os.path.splitext(f)[1].lstrip(".").lower() or "noext"
            dest_dir = os.path.join(dest_root, ext)
        else:
            ts = os.path.getmtime(f)
            d = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            dest_dir = os.path.join(dest_root, d)
        os.makedirs(dest_dir, exist_ok=True)
        new_path = os.path.join(dest_dir, os.path.basename(f))
        if args.dry_run:
            print(f"Would move {f} -> {new_path}")
        else:
            shutil.move(f, new_path)
