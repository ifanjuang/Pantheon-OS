"""Common helpers used across the runtime."""
from __future__ import annotations
import time


def truncate(text: str, max_chars: int = 500) -> str:
    return text[:max_chars] + "…" if len(text) > max_chars else text


class Timer:
    def __enter__(self):
        self._start = time.monotonic()
        return self

    def __exit__(self, *_):
        self.elapsed_ms = int((time.monotonic() - self._start) * 1000)
