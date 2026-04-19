import sys
from pathlib import Path

# api/ must come before project root so api/core/ takes precedence over
# the root-level core/ package (meta-agent classes).
# Also evict any cached root-level core that pytest may have imported
# during its startup scan of the project directory.
_api = str(Path(__file__).parent / "api")
while _api in sys.path:
    sys.path.remove(_api)
sys.path.insert(0, _api)
for _k in [k for k in list(sys.modules) if k == "core" or k.startswith("core.")]:
    del sys.modules[_k]
