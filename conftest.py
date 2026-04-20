import sys
from pathlib import Path

# platform/api/ must be first so api/core/ (settings, auth, etc.) takes
# precedence over the root-level core/ framework package.
_api = str(Path(__file__).parent / "platform" / "api")
while _api in sys.path:
    sys.path.remove(_api)
sys.path.insert(0, _api)
for _k in [k for k in list(sys.modules) if k == "core" or k.startswith("core.")]:
    del sys.modules[_k]
