"""
Implements 'dedupe' command: resolves duplicates by linking or deleting.
"""

import os
from .common import iter_files, file_hash

def cmd_dedupe(args):
    files = list(iter_files(args.path, args.include, args.exclude))
    hashes = {}
    for f in files:
        h = file_hash(f, algo=args.hash)
        hashes.setdefault(h, []).append(f)
    for h, fs in hashes.items():
        if len(fs) < 2: continue
        master, *dupes = fs
        for d in dupes:
            if args.dry_run:
                print(f"Would {args.action} duplicate {d} -> {master}")
            else:
                if args.action == "delete":
                    os.remove(d)
                else:  # link
                    os.replace(d, d+".bak") # preserve original temporarily
                    os.link(master, d)
