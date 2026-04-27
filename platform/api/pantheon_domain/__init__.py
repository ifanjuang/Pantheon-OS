"""Pantheon OS domain layer package.

This package is the code-facing representation of the Hermes-backed pivot:
Pantheon defines, Hermes executes, OpenWebUI exposes and retrieves.
"""

from .repository import DomainLayerRepository

__all__ = ["DomainLayerRepository"]
