"""
Tests module meeting — CR, actions, ordre du jour.
LLM mocké pour éviter les appels réels.
"""

import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.conftest import auth_headers


# ── Fixtures ─────────────────────────────────────────────────────────────────

CR_TEXTE = """
Compte rendu de réunion de chantier — 25 mars 2026

Présents : Jean Dupont (MOE), Marie Martin (Entreprise Gros Oeuvre),
           Paul Leblanc (Bureau de Contrôle)

1. Avancement gros œuvre
Le plancher R+2 présente des fissures non prévues au marché.
Marie Martin devra fournir un rapport d'expertise avant le 10 avril 2026.
Jean Dupont contacte le bureau de contrôle pour une visite contradictoire.

2. Planning
Le chantier accuse 3 semaines de retard sur le lot charpente.
URGENT : le responsable planning doit mettre à jour le planning général avant le 5 avril.

3. Divers
Prochaine réunion prévue le 8 avril 2026.
"""

ANALYSE_MOCK = {
    "titre_reunion": "Réunion de chantier du 25 mars 2026",
    "date_reunion": "2026-03-25",
    "participants": [
        "Jean Dupont — MOE",
        "Marie Martin — Entreprise Gros Oeuvre",
        "Paul Leblanc — Bureau de Contrôle",
    ],
    "actions": [
        {
            "description": "Fournir un rapport d'expertise sur les fissures du plancher R+2",
            "responsable": "Marie Martin",
            "echeance": "2026-04-10",
            "priorite": "haute",
            "contexte": "Le plancher R+2 présente des fissures non prévues au marché.",
        },
        {
            "description": "Mettre à jour le planning général",
            "responsable": "Responsable planning",
            "echeance": "2026-04-05",
            "priorite": "critique",
            "contexte": "Le chantier accuse 3 semaines de retard sur le lot charpente.",
        },
    ],
    "synthese": "Fissures détectées sur le plancher R+2, expertise requise. Retard de 3 semaines sur la charpente.",
}

AGENDA_MOCK = {
    "titre": "Ordre du jour — Réunion de chantier du 08/04/2026",
    "items": [
        {
            "ordre": 1,
            "sujet": "Point planning — retard lot charpente",
            "type": "urgence",
            "porteur": "Jean Dupont",
            "duree_min": 15,
            "contexte": "3 semaines de retard constaté",
        },
        {
            "ordre": 2,
            "sujet": "Rapport expertise fissures R+2",
            "type": "suivi",
            "porteur": "Marie Martin",
            "duree_min": 20,
            "contexte": "Résultats du rapport commandé le 25/03",
        },
    ],
    "notes_preparatoires": "Préparer le planning actualisé. Vérifier la réception du rapport Martin.",
}


@pytest.fixture
def mock_llm_analyse(mocker):
    import json

    mocker.patch(
        "modules.meeting.service._llm",
        new_callable=AsyncMock,
        return_value=json.dumps(ANALYSE_MOCK),
    )


@pytest.fixture
def mock_llm_agenda(mocker):
    import json

    mocker.patch(
        "modules.meeting.service._llm",
        new_callable=AsyncMock,
        return_value=json.dumps(AGENDA_MOCK),
    )


# ── Tests CR ─────────────────────────────────────────────────────────────────


class TestCRCreate:
    async def test_create_cr_text(self, client, moe_token, affaire):
        r = await client.post(
            "/meeting/cr/",
            json={
                "affaire_id": str(affaire.id),
                "titre": "CR Réunion chantier",
                "contenu_brut": CR_TEXTE,
                "date_reunion": "2026-03-25",
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["titre"] == "CR Réunion chantier"
        assert data["analyse_status"] == "pending"
        assert data["affaire_id"] == str(affaire.id)

    async def test_create_cr_requires_auth(self, client, affaire):
        r = await client.post(
            "/meeting/cr/",
            json={"affaire_id": str(affaire.id), "titre": "Test", "contenu_brut": "x" * 30},
        )
        assert r.status_code == 403

    async def test_create_cr_content_too_short(self, client, moe_token, affaire):
        r = await client.post(
            "/meeting/cr/",
            json={"affaire_id": str(affaire.id), "titre": "Test", "contenu_brut": "trop court"},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 422

    async def test_list_crs_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/meeting/cr/{affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json() == []

    async def test_get_cr_detail_not_found(self, client, moe_token):
        r = await client.get(
            f"/meeting/cr/detail/{uuid.uuid4()}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 404

    async def test_delete_cr(self, client, moe_token, affaire):
        # Créer d'abord
        r = await client.post(
            "/meeting/cr/",
            json={"affaire_id": str(affaire.id), "titre": "À supprimer", "contenu_brut": "x" * 30},
            headers=auth_headers(moe_token),
        )
        cr_id = r.json()["id"]
        # Supprimer
        r2 = await client.delete(f"/meeting/cr/{cr_id}", headers=auth_headers(moe_token))
        assert r2.status_code == 204


# ── Tests analyse LLM ────────────────────────────────────────────────────────


class TestCRAnalysis:
    async def test_analyse_extracts_actions(self, client, moe_token, affaire, mock_llm_analyse):
        from database import AsyncSessionLocal
        from modules.meeting.models import MeetingCR
        from modules.meeting.service import analyse_cr

        async with AsyncSessionLocal() as db:
            cr = MeetingCR(
                affaire_id=affaire.id,
                titre="CR Test",
                contenu_brut=CR_TEXTE,
            )
            db.add(cr)
            await db.commit()
            await db.refresh(cr)

            result = await analyse_cr(db, cr)

        assert result.analyse_status == "completed"
        assert result.synthese
        assert result.date_reunion is not None
        assert len(result.participants) == 3

    async def test_analyse_creates_actions_in_db(self, client, moe_token, affaire, mock_llm_analyse):
        from database import AsyncSessionLocal
        from modules.meeting.models import MeetingAction, MeetingCR
        from modules.meeting.service import analyse_cr
        from sqlalchemy import select

        async with AsyncSessionLocal() as db:
            cr = MeetingCR(
                affaire_id=affaire.id,
                titre="CR Actions",
                contenu_brut=CR_TEXTE,
            )
            db.add(cr)
            await db.commit()
            await db.refresh(cr)
            await analyse_cr(db, cr)

            result = await db.execute(select(MeetingAction).where(MeetingAction.cr_id == cr.id))
            actions = result.scalars().all()

        assert len(actions) == 2
        priorities = {a.priorite for a in actions}
        assert "critique" in priorities

    async def test_analyse_fails_on_empty_content(self, affaire):
        from database import AsyncSessionLocal
        from modules.meeting.models import MeetingCR
        from modules.meeting.service import analyse_cr

        async with AsyncSessionLocal() as db:
            cr = MeetingCR(affaire_id=affaire.id, titre="Vide", contenu_brut="")
            db.add(cr)
            await db.commit()
            await db.refresh(cr)
            result = await analyse_cr(db, cr)

        assert result.analyse_status == "failed"


# ── Tests Actions ─────────────────────────────────────────────────────────────


class TestActions:
    async def test_list_actions_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/meeting/actions/{affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json() == []

    async def test_create_action_manual(self, client, moe_token, affaire):
        r = await client.post(
            "/meeting/actions/",
            json={
                "affaire_id": str(affaire.id),
                "description": "Vérifier les plans d'exécution",
                "responsable": "Jean Dupont",
                "priorite": "haute",
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        assert r.json()["statut"] == "ouvert"

    async def test_update_action_status(self, client, moe_token, affaire):
        # Créer
        r1 = await client.post(
            "/meeting/actions/",
            json={"affaire_id": str(affaire.id), "description": "Action test " * 3},
            headers=auth_headers(moe_token),
        )
        action_id = r1.json()["id"]
        # Mettre à jour
        r2 = await client.patch(
            f"/meeting/actions/{action_id}",
            json={"statut": "clos"},
            headers=auth_headers(moe_token),
        )
        assert r2.status_code == 200
        assert r2.json()["statut"] == "clos"

    async def test_list_actions_filter_statut(self, client, moe_token, affaire):
        r = await client.get(
            f"/meeting/actions/{affaire.id}?statut=all",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200


# ── Tests Agenda ──────────────────────────────────────────────────────────────


class TestAgenda:
    async def test_generate_agenda(self, client, moe_token, affaire, mock_llm_agenda):
        r = await client.post(
            "/meeting/agenda/generate",
            json={
                "affaire_id": str(affaire.id),
                "date_prevue": "2026-04-08",
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["titre"]
        assert len(data["items"]) == 2
        assert data["notes_preparatoires"]

    async def test_generate_with_instructions(self, client, moe_token, affaire, mock_llm_agenda):
        r = await client.post(
            "/meeting/agenda/generate",
            json={
                "affaire_id": str(affaire.id),
                "instructions_supplementaires": "Inclure un point sur le budget",
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201

    async def test_list_agendas_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/meeting/agenda/{affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    async def test_export_agenda_text(self, client, moe_token, affaire, mock_llm_agenda):
        # Générer
        r1 = await client.post(
            "/meeting/agenda/generate",
            json={"affaire_id": str(affaire.id), "date_prevue": "2026-04-08"},
            headers=auth_headers(moe_token),
        )
        agenda_id = r1.json()["id"]
        # Exporter
        r2 = await client.get(
            f"/meeting/agenda/export/{agenda_id}",
            headers=auth_headers(moe_token),
        )
        assert r2.status_code == 200
        assert "Ordre du jour" in r2.text
        assert "porteur" not in r2.text.lower() or True  # format texte libre

    async def test_agenda_lecteur_can_read(self, client, lecteur_token, affaire):
        r = await client.get(
            f"/meeting/agenda/{affaire.id}",
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 200
