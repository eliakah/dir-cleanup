"""
Implements the 'scan' command for dirclean.
"""

import os
from .common import iter_files, file_hash

def cmd_scan(args):
    """Scan directory and print report of file counts and optionally duplicates.
    This works by loading files through a hashmap, making it easy to identify duplicates"""
    files = list(iter_files(args.path, args.include, args.exclude))
    print(f"Scanned {len(files)} files in {args.path}")

    if args.hash:
        hashes = {}
        for f in files:
            h = file_hash(f)
            hashes.setdefault(h, []).append(f)
        dups = {h: fs for h, fs in hashes.items() if len(fs) > 1}
        if dups:
            print("Duplicate sets:")
            for h, fs in dups.items():
                print(f"{h[:8]}: {fs}")
