"""
Tests module affaires — CRUD projets MOE
"""
import pytest
from tests.conftest import auth_headers


class TestListAffaires:
    async def test_list_requires_auth(self, client):
        r = await client.get("/affaires/")
        assert r.status_code == 403

    async def test_list_empty(self, client, lecteur_token):
        r = await client.get("/affaires/", headers=auth_headers(lecteur_token))
        assert r.status_code == 200
        assert r.json() == []

    async def test_list_returns_affaires(self, client, lecteur_token, affaire):
        r = await client.get("/affaires/", headers=auth_headers(lecteur_token))
        assert r.status_code == 200
        codes = [a["code"] for a in r.json()]
        assert "TEST-001" in codes

    async def test_list_filter_by_statut(self, client, admin_token, affaire):
        r = await client.get("/affaires/?statut=actif", headers=auth_headers(admin_token))
        assert r.status_code == 200
        assert all(a["statut"] == "actif" for a in r.json())

        r = await client.get("/affaires/?statut=archive", headers=auth_headers(admin_token))
        assert r.status_code == 200
        assert r.json() == []


class TestCreateAffaire:
    async def test_create_by_moe(self, client, moe_token):
        r = await client.post(
            "/affaires/",
            json={"code": "PRJ-2024-001", "nom": "Immeuble Lumière", "statut": "actif"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["code"] == "PRJ-2024-001"
        assert data["nom"] == "Immeuble Lumière"
        assert "id" in data

    async def test_create_code_uppercased(self, client, moe_token):
        r = await client.post(
            "/affaires/",
            json={"code": "prj-lowercase", "nom": "Test"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        assert r.json()["code"] == "PRJ-LOWERCASE"

    async def test_create_duplicate_code(self, client, moe_token, affaire):
        r = await client.post(
            "/affaires/",
            json={"code": "TEST-001", "nom": "Doublon"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 409

    async def test_create_invalid_statut(self, client, moe_token):
        r = await client.post(
            "/affaires/",
            json={"code": "X-001", "nom": "Test", "statut": "invalide"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 422

    async def test_create_forbidden_for_lecteur(self, client, lecteur_token):
        r = await client.post(
            "/affaires/",
            json={"code": "X-002", "nom": "Test"},
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 403


class TestGetAffaire:
    async def test_get_existing(self, client, lecteur_token, affaire):
        r = await client.get(f"/affaires/{affaire.id}", headers=auth_headers(lecteur_token))
        assert r.status_code == 200
        assert r.json()["code"] == "TEST-001"

    async def test_get_not_found(self, client, lecteur_token):
        import uuid
        r = await client.get(
            f"/affaires/{uuid.uuid4()}", headers=auth_headers(lecteur_token)
        )
        assert r.status_code == 404


class TestUpdateAffaire:
    async def test_update_nom(self, client, moe_token, affaire):
        r = await client.patch(
            f"/affaires/{affaire.id}",
            json={"nom": "Nouveau nom"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json()["nom"] == "Nouveau nom"

    async def test_update_statut_archive(self, client, admin_token, affaire):
        r = await client.patch(
            f"/affaires/{affaire.id}",
            json={"statut": "archive"},
            headers=auth_headers(admin_token),
        )
        assert r.status_code == 200
        assert r.json()["statut"] == "archive"

    async def test_update_forbidden_for_lecteur(self, client, lecteur_token, affaire):
        r = await client.patch(
            f"/affaires/{affaire.id}",
            json={"nom": "Tentative"},
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 403


class TestDeleteAffaire:
    async def test_delete_by_admin(self, client, admin_token, db):
        from modules.affaires.service import create_affaire
        a = await create_affaire(db, "DEL-001", "À supprimer", None, "actif", None)
        await db.commit()

        r = await client.delete(f"/affaires/{a.id}", headers=auth_headers(admin_token))
        assert r.status_code == 204

        r = await client.get(f"/affaires/{a.id}", headers=auth_headers(admin_token))
        assert r.status_code == 404

    async def test_delete_forbidden_for_moe(self, client, moe_token, affaire):
        r = await client.delete(f"/affaires/{affaire.id}", headers=auth_headers(moe_token))
        assert r.status_code == 403
