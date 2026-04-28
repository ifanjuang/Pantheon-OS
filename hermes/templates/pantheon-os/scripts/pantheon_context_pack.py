#!/usr/bin/env python3
"""Fetch Pantheon OS Context Pack.

Local Hermes helper template. This script is intentionally small and read-only.
It should be copied into `~/.hermes/skills/pantheon-os/scripts/` with the skill.
"""

from __future__ import annotations

import json
import os
import sys
from urllib.error import URLError
from urllib.request import urlopen


def main() -> int:
    base_url = os.environ.get("PANTHEON_API_URL", "http://localhost:8000").rstrip("/")
    url = f"{base_url}/runtime/context-pack"

    try:
        with urlopen(url, timeout=10) as response:  # nosec B310 - local/operator helper
            payload = json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        print(json.dumps({"status": "error", "url": url, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
