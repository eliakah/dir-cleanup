"""
Common helper functions shared across dirclean ops modules.
"""

import os, hashlib

def iter_files(path, include=None, exclude=None):
    """Yield all file paths under path, filtering by include/exclude extensions."""
    include = set(include or [])
    exclude = set(exclude or [])
    for root, _, files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if include and ext not in include:
                continue
            if exclude and ext in exclude:
                continue
            yield os.path.join(root, f)

def file_hash(path, algo="sha256", block_size=65536):
    """Return hex digest for a file using chosen hashing algorithm."""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""): 
            h.update(chunk)
    return h.hexdigest()
