"""
Basic smoke tests for dirclean project.
"""

import os
from ops import common

def test_file_hash(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hello")
    h = common.file_hash(str(f))
    assert isinstance(h, str) and len(h) > 0
