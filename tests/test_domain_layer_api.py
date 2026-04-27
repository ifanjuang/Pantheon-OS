from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

API_ROOT = Path(__file__).resolve().parents[1] / "platform" / "api"
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from main import app  # noqa: E402

client = TestClient(app)


def test_domain_snapshot_exposes_pantheon_doctrine() -> None:
    response = client.get("/domain/snapshot")

    assert response.status_code == 200
    data = response.json()

    assert data["mode"] == "hermes_backed_domain_layer"
    assert data["doctrine"] == "Pantheon defines. Hermes executes. OpenWebUI exposes and retrieves."
    assert data["agents"]
    assert data["skills"]
    assert data["workflows"]
    assert any(component["id"] == "fastapi_runtime" for component in data["legacy_components"])


def test_read_action_does_not_require_approval() -> None:
    response = client.post(
        "/domain/approval/classify",
        json={"action_kind": "read", "description": "Read a reference Markdown file."},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "not_required"
    assert data["required_human_validation"] is False
    assert data["blocked_until_policy_exists"] is False


def test_secret_or_volume_access_is_blocked_until_policy_exists() -> None:
    response = client.post(
        "/domain/approval/classify",
        json={"action_kind": "secret_or_volume_access", "description": "Mount Docker socket."},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "forbidden_until_policy_exists"
    assert data["required_human_validation"] is True
    assert data["blocked_until_policy_exists"] is True


def test_file_mutation_requires_human_validation() -> None:
    response = client.post(
        "/domain/approval/classify",
        json={"action_kind": "file_mutation", "description": "Modify README.md."},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "required"
    assert data["required_human_validation"] is True
