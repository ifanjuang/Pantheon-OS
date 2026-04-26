"""
Conftest for the modules/ tree.

The root tests/conftest.py is API-centric: it forces platform/api/core onto
sys.path[0] so that imports like `from core.auth import …` resolve against
the API's core package. That is incompatible with module-internal tests
(modules/agents/*/tests/test_agent.py) which need root-level core/contracts/.

This conftest reverses that for tests under modules/:
- Removes platform/api from sys.path so it can't shadow root core/.
- Evicts any cached `core.*` modules so the next import re-resolves
  against the real root package.

It only loads when pytest collects tests under modules/, so the API tests
under tests/ are unaffected.
"""

import sys as _sys
from pathlib import Path as _Path

_repo_root = str(_Path(__file__).parent.parent)
_api = str(_Path(__file__).parent.parent / "platform" / "api")

# Drop platform/api from sys.path entirely — modules/ tests don't need it.
while _api in _sys.path:
    _sys.path.remove(_api)

# Ensure repo root is on sys.path so `core.contracts`, `modules.agents.*`
# resolve against the runtime framework, not platform/api/core.
if _repo_root not in _sys.path:
    _sys.path.insert(0, _repo_root)

# Evict any `core.*` already imported via platform/api so the next import
# re-resolves against root core/.
for _key in [k for k in list(_sys.modules) if k == "core" or k.startswith("core.")]:
    del _sys.modules[_key]
