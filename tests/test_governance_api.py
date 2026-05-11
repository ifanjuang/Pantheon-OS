"""Read-only tests for the governance document Domain API.

These tests verify the four endpoints added by Bloc 5 of the Pantheon Next
stabilization plan:

* `GET /domain/role-signals`
* `GET /domain/role-signal-profiles`
* `GET /domain/routing-foundation`
* `GET /domain/governance-index`

They use FastAPI's `TestClient` (in-process; no real network, no Postgres,
no Redis). They confirm that:

* every endpoint returns HTTP 200;
* the returned payload exposes the canonical schema
  (path / title / status / content / last_known_static_source);
* the documents carry the doctrine they claim to govern;
* the API itself never mutates the source files on disk.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


REPO_ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_DIR = REPO_ROOT / "docs" / "governance"

client = TestClient(app)


# ── Helpers ────────────────────────────────────────────────────────────────


def _doc_payload_fields() -> set[str]:
    return {"path", "title", "status", "content", "last_known_static_source"}


def _doc_dir_hash(directory: Path) -> str:
    """Hash the content of every Markdown file under `directory`.

    The hash lets a test confirm the API call did not mutate any source file
    on disk. Sort by path so the hash is deterministic.
    """
    hasher = hashlib.sha256()
    for path in sorted(p for p in directory.iterdir() if p.is_file()):
        hasher.update(path.name.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


# ── Per-document endpoints ─────────────────────────────────────────────────


def test_role_signals_endpoint_returns_doctrine() -> None:
    response = client.get("/domain/role-signals")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) >= _doc_payload_fields()
    assert payload["path"] == "docs/governance/ROLE_SIGNALS.md"
    assert payload["last_known_static_source"] == "docs/governance/ROLE_SIGNALS.md"
    assert payload["status"] == "active"
    assert "ROLE SIGNALS" in payload["content"]
    assert "Pantheon Next governs" in payload["content"]
    assert "Hermes Agent executes" in payload["content"]


def test_role_signal_profiles_endpoint_returns_iris_doctrine() -> None:
    response = client.get("/domain/role-signal-profiles")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) >= _doc_payload_fields()
    assert payload["path"] == "docs/governance/ROLE_SIGNAL_PROFILES.md"
    assert payload["status"] == "active"
    assert "IRIS" in payload["content"]
    assert "format_reminder_request" in payload["content"]
    assert "no_decision" in payload["content"]


def test_routing_foundation_endpoint_returns_routing_doctrine() -> None:
    response = client.get("/domain/routing-foundation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["path"] == "docs/governance/ROUTING_FOUNDATION.md"
    assert payload["status"] == "active"
    assert "ROUTING FOUNDATION" in payload["content"]
    assert "Pantheon Role" in payload["content"]


def test_per_document_endpoints_use_get_only() -> None:
    """The new endpoints must reject POST, PUT, PATCH and DELETE."""
    for path in (
        "/domain/role-signals",
        "/domain/role-signal-profiles",
        "/domain/routing-foundation",
    ):
        for method in (client.post, client.put, client.patch, client.delete):
            response = method(path)
            assert response.status_code in (404, 405), (
                f"{method.__name__.upper()} {path} should be rejected, got {response.status_code}"
            )


# ── Governance index endpoint ─────────────────────────────────────────────


def test_governance_index_lists_canonical_docs() -> None:
    response = client.get("/domain/governance-index")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) >= 30, f"expected the index to cover at least 30 docs, got {len(payload)}"

    paths = {entry["path"] for entry in payload}
    required = {
        "docs/governance/STATUS.md",
        "docs/governance/ROADMAP.md",
        "docs/governance/ARCHITECTURE.md",
        "docs/governance/AGENTS.md",
        "docs/governance/APPROVALS.md",
        "docs/governance/TASK_CONTRACTS.md",
        "docs/governance/EVIDENCE_PACK.md",
        "docs/governance/ROLE_SIGNALS.md",
        "docs/governance/ROLE_SIGNAL_PROFILES.md",
        "docs/governance/ROUTING_FOUNDATION.md",
        "docs/governance/HERMES_INTEGRATION.md",
        "docs/governance/OPENWEBUI_INTEGRATION.md",
    }
    missing = required - paths
    assert not missing, f"governance index missing canonical docs: {sorted(missing)}"


def test_governance_index_default_omits_content() -> None:
    """By default the index is metadata-only so the listing stays bounded."""
    response = client.get("/domain/governance-index")
    payload = response.json()

    for entry in payload:
        assert set(entry) >= _doc_payload_fields()
        assert entry["content"] == "", f"index entry for {entry['path']} should be metadata-only by default"
        assert entry["last_known_static_source"] == entry["path"]


def test_governance_index_include_content_returns_full_text() -> None:
    response = client.get("/domain/governance-index", params={"include_content": "true"})

    assert response.status_code == 200
    payload = response.json()
    role_signals = next(entry for entry in payload if entry["path"] == "docs/governance/ROLE_SIGNALS.md")
    assert role_signals["content"], "include_content=true should return content"
    assert "Pantheon Next governs" in role_signals["content"]


def test_governance_index_rejects_non_get() -> None:
    for method in (client.post, client.put, client.patch, client.delete):
        response = method("/domain/governance-index")
        assert response.status_code in (404, 405)


# ── Doctrine and safety invariants ─────────────────────────────────────────


def test_governance_endpoints_do_not_mutate_source_files() -> None:
    """Calling every new endpoint must leave docs/governance/ byte-identical."""
    baseline = _doc_dir_hash(GOVERNANCE_DIR)
    for path in (
        "/domain/role-signals",
        "/domain/role-signal-profiles",
        "/domain/routing-foundation",
        "/domain/governance-index",
        "/domain/governance-index?include_content=true",
    ):
        response = client.get(path)
        assert response.status_code == 200
    assert _doc_dir_hash(GOVERNANCE_DIR) == baseline, "governance API leaked a write to docs/governance/"


def test_hermes_is_not_indexed_as_pantheon_role() -> None:
    """The governance index must not promote Hermes to a Pantheon-role doc."""
    response = client.get("/domain/governance-index")
    payload = response.json()
    titles = {entry["title"] for entry in payload}
    # `Hermes Integration`, `Hermes Execution Model`, `Hermes Capability Map`
    # are governance boundary docs; none of them frames Hermes as a Pantheon
    # role. Reject any future entry that calls Hermes an agent / role.
    forbidden = {"Hermes Agent", "Hermes Role"}
    assert not forbidden & titles, f"forbidden Hermes-as-role title: {forbidden & titles}"


def test_unknown_governance_endpoint_returns_404() -> None:
    """A typo or unknown governance lookup must not crash; expect 404."""
    response = client.get("/domain/role-signal-profile")  # missing trailing s
    assert response.status_code == 404
