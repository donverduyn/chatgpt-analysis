# shared/setup_path.py

import sys
from pathlib import Path


def add_root():
    """Add the repo root (one level up from cwd) to sys.path."""
    repo_root = Path.cwd().parent
    sys.path.insert(0, str(repo_root))
