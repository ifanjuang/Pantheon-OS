"""
Conftest for the agents/ tree.

The root conftest.py puts platform/api/ first on sys.path so API tests resolve
`core.X` against the API's local core (settings, auth…). Agent tests need the
opposite: `core.contracts.agent.AgentBase` lives in the root-level core/ package.

This conftest only loads when pytest collects under agents/ — it removes
platform/api from sys.path and re-evicts cached `core.*` modules so the next
import resolves against the real root core/.
"""

import sys as _sys
from pathlib import Path as _Path

_repo_root = str(_Path(__file__).parent.parent)
_api = str(_Path(__file__).parent.parent / "platform" / "api")

while _api in _sys.path:
    _sys.path.remove(_api)

if _repo_root not in _sys.path:
    _sys.path.insert(0, _repo_root)

for _key in [k for k in list(_sys.modules) if k == "core" or k.startswith("core.")]:
    del _sys.modules[_key]
