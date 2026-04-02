"""
Tests module auth — login, register, me, users
"""
import pytest
from tests.conftest import auth_headers


class TestLogin:
    async def test_login_success(self, client, admin_user):
        r = await client.post("/auth/login", json={
            "email": "admin@test.fr", "password": "password123"
        })
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client, admin_user):
        r = await client.post("/auth/login", json={
            "email": "admin@test.fr", "password": "mauvais"
        })
        assert r.status_code == 401

    async def test_login_unknown_email(self, client):
        r = await client.post("/auth/login", json={
            "email": "inconnu@test.fr", "password": "password123"
        })
        assert r.status_code == 401


class TestRegister:
    async def test_register_by_admin(self, client, admin_token):
        r = await client.post(
            "/auth/register",
            json={"email": "nouveau@test.fr", "password": "pass123", "role": "moe"},
            headers=auth_headers(admin_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == "nouveau@test.fr"
        assert data["role"] == "moe"

    async def test_register_duplicate_email(self, client, admin_token, admin_user):
        r = await client.post(
            "/auth/register",
            json={"email": "admin@test.fr", "password": "pass123"},
            headers=auth_headers(admin_token),
        )
        assert r.status_code == 409

    async def test_register_invalid_role(self, client, admin_token):
        r = await client.post(
            "/auth/register",
            json={"email": "x@test.fr", "password": "pass123", "role": "superadmin"},
            headers=auth_headers(admin_token),
        )
        assert r.status_code == 422

    async def test_register_forbidden_for_moe(self, client, moe_token):
        r = await client.post(
            "/auth/register",
            json={"email": "x@test.fr", "password": "pass123"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 403

    async def test_register_requires_auth(self, client):
        r = await client.post(
            "/auth/register",
            json={"email": "x@test.fr", "password": "pass123"},
        )
        assert r.status_code == 403


class TestMe:
    async def test_me_returns_profile(self, client, admin_token, admin_user):
        r = await client.get("/auth/me", headers=auth_headers(admin_token))
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == "admin@test.fr"
        assert data["role"] == "admin"

    async def test_me_without_token(self, client):
        r = await client.get("/auth/me")
        assert r.status_code == 403


class TestListUsers:
    async def test_list_users_admin(self, client, admin_token, admin_user, moe_user):
        r = await client.get("/auth/users", headers=auth_headers(admin_token))
        assert r.status_code == 200
        emails = [u["email"] for u in r.json()]
        assert "admin@test.fr" in emails
        assert "moe@test.fr" in emails

    async def test_list_users_forbidden_for_moe(self, client, moe_token):
        r = await client.get("/auth/users", headers=auth_headers(moe_token))
        assert r.status_code == 403
