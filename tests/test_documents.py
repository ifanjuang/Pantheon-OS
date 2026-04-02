"""
Tests module documents — upload, search, liste, suppression.
StorageService et RagService sont mockés (pas besoin de MinIO/Ollama).
"""
import pytest
from unittest.mock import AsyncMock, patch
from tests.conftest import auth_headers


@pytest.fixture
def pdf_bytes() -> bytes:
    """Faux contenu PDF pour les tests d'upload."""
    return b"%PDF-1.4 fake pdf content for testing"


class TestUpload:
    async def test_upload_requires_auth(self, client, affaire, pdf_bytes):
        r = await client.post(
            "/documents/upload",
            data={"affaire_id": str(affaire.id)},
            files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
        )
        assert r.status_code == 403

    async def test_upload_success(self, client, moe_token, affaire, pdf_bytes, mocker):
        mocker.patch(
            "core.services.storage_service.StorageService.upload",
            new_callable=AsyncMock,
            return_value=f"{affaire.id}/documents/test.pdf",
        )
        mocker.patch(
            "core.services.rag_service.RagService.ingest",
            new_callable=AsyncMock,
            return_value=5,
        )

        r = await client.post(
            "/documents/upload",
            data={"affaire_id": str(affaire.id), "source_type": "note"},
            files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["nom"] == "test.pdf"
        assert data["chunks_created"] == 5
        assert "document_id" in data

    async def test_upload_forbidden_mime(self, client, moe_token, affaire):
        r = await client.post(
            "/documents/upload",
            data={"affaire_id": str(affaire.id)},
            files={"file": ("script.exe", b"MZ...", "application/x-msdownload")},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 415

    async def test_upload_forbidden_for_lecteur(self, client, lecteur_token, affaire, pdf_bytes):
        r = await client.post(
            "/documents/upload",
            data={"affaire_id": str(affaire.id)},
            files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 403


class TestSearch:
    async def test_search_returns_results(self, client, moe_token, affaire, mocker):
        mocker.patch(
            "core.services.rag_service.RagService.search",
            new_callable=AsyncMock,
            return_value=[
                {
                    "chunk_id": "abc-123",
                    "document_id": "doc-456",
                    "contenu": "Article 3.2 — Isolation acoustique minimale : 42 dB",
                    "meta": {"filename": "cctp.pdf", "source_type": "cctp"},
                    "score": 0.92,
                }
            ],
        )

        r = await client.post(
            "/documents/search",
            json={
                "query": "exigences acoustiques",
                "affaire_id": str(affaire.id),
                "top_k": 3,
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        results = r.json()
        assert len(results) == 1
        assert results[0]["score"] == pytest.approx(0.92)
        assert "acoustique" in results[0]["contenu"]

    async def test_search_requires_auth(self, client, affaire):
        r = await client.post(
            "/documents/search",
            json={"query": "test", "affaire_id": str(affaire.id)},
        )
        assert r.status_code == 403


class TestListDocuments:
    async def test_list_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/documents/?affaire_id={affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json() == []

    async def test_list_after_upload(self, client, moe_token, affaire, pdf_bytes, mocker, db):
        # Créer un document directement en DB
        from modules.documents.models import Document
        doc = Document(
            affaire_id=affaire.id,
            nom="cctp.pdf",
            couche="projet",
            type_doc="pdf",
            mime_type="application/pdf",
            taille_octets=len(pdf_bytes),
            storage_key=f"{affaire.id}/documents/cctp.pdf",
            uploaded_by=None,
        )
        db.add(doc)
        await db.commit()

        r = await client.get(
            f"/documents/?affaire_id={affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert len(r.json()) == 1
        assert r.json()[0]["nom"] == "cctp.pdf"


class TestDeleteDocument:
    async def test_delete_by_moe(self, client, moe_token, affaire, db, mocker):
        mocker.patch(
            "core.services.rag_service.RagService.delete_document",
            new_callable=AsyncMock,
            return_value=3,
        )
        mocker.patch(
            "core.services.storage_service.StorageService.delete",
            new_callable=AsyncMock,
        )

        from modules.documents.models import Document
        doc = Document(
            affaire_id=affaire.id,
            nom="a_supprimer.pdf",
            couche="projet",
            type_doc="pdf",
            mime_type="application/pdf",
            taille_octets=100,
            storage_key="test/key.pdf",
        )
        db.add(doc)
        await db.commit()

        r = await client.delete(
            f"/documents/{doc.id}", headers=auth_headers(moe_token)
        )
        assert r.status_code == 204

    async def test_delete_not_found(self, client, moe_token):
        import uuid
        r = await client.delete(
            f"/documents/{uuid.uuid4()}", headers=auth_headers(moe_token)
        )
        assert r.status_code == 404
