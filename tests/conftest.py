import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Ensure the local src/ directory is importable before any site-packages version.
if SRC.exists():
    sys.path.insert(0, str(SRC))
