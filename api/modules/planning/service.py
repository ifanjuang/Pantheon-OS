"""
PlanningService — logique métier du module planning.

CRUD : lots, tâches, jalons, liens de dépendance.

Moteur d'analyse :
  - compute_critical_path  : algorithme CPM (forward/backward pass)
                             sur le DAG de dépendances des tâches.
  - propagate_delays       : propagation en cascade d'un décalage
                             via un BFS sur les liens FS sortants.
  - get_health             : KPIs de santé du planning.
"""
from collections import defaultdict, deque
from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.planning.models import Jalon, LienDependance, Lot, Tache


# ══════════════════════════════════════════════════════════════════════
# LOTS
# ══════════════════════════════════════════════════════════════════════

async def create_lot(db: AsyncSession, affaire_id: UUID, **fields) -> Lot:
    lot = Lot(affaire_id=affaire_id, **fields)
    db.add(lot)
    await db.flush()
    return lot


async def get_lot(db: AsyncSession, lot_id: UUID) -> Lot | None:
    return await db.get(Lot, lot_id)


async def list_lots(db: AsyncSession, affaire_id: UUID) -> list[Lot]:
    result = await db.execute(
        select(Lot).where(Lot.affaire_id == affaire_id).order_by(Lot.code)
    )
    return result.scalars().all()


async def update_lot(db: AsyncSession, lot: Lot, data: dict) -> Lot:
    for k, v in data.items():
        if v is not None:
            setattr(lot, k, v)
    await db.flush()
    return lot


async def delete_lot(db: AsyncSession, lot: Lot) -> None:
    await db.delete(lot)


# ══════════════════════════════════════════════════════════════════════
# TÂCHES
# ══════════════════════════════════════════════════════════════════════

async def create_tache(db: AsyncSession, affaire_id: UUID, **fields) -> Tache:
    tache = Tache(affaire_id=affaire_id, **fields)
    db.add(tache)
    await db.flush()
    return tache


async def get_tache(db: AsyncSession, tache_id: UUID) -> Tache | None:
    return await db.get(Tache, tache_id)


async def list_taches(
    db: AsyncSession,
    affaire_id: UUID,
    lot_id: UUID | None = None,
    statut: str | None = None,
    critique_only: bool = False,
) -> list[Tache]:
    q = select(Tache).where(Tache.affaire_id == affaire_id)
    if lot_id:
        q = q.where(Tache.lot_id == lot_id)
    if statut:
        q = q.where(Tache.statut == statut)
    if critique_only:
        q = q.where(Tache.critique.is_(True))
    result = await db.execute(q.order_by(Tache.date_debut_prevue.asc().nulls_last()))
    return result.scalars().all()


async def update_tache(db: AsyncSession, tache: Tache, data: dict) -> Tache:
    for k, v in data.items():
        if v is not None:
            setattr(tache, k, v)
    await db.flush()
    return tache


async def delete_tache(db: AsyncSession, tache: Tache) -> None:
    await db.delete(tache)


# ══════════════════════════════════════════════════════════════════════
# JALONS
# ══════════════════════════════════════════════════════════════════════

async def create_jalon(db: AsyncSession, affaire_id: UUID, **fields) -> Jalon:
    jalon = Jalon(affaire_id=affaire_id, **fields)
    db.add(jalon)
    await db.flush()
    return jalon


async def get_jalon(db: AsyncSession, jalon_id: UUID) -> Jalon | None:
    return await db.get(Jalon, jalon_id)


async def list_jalons(db: AsyncSession, affaire_id: UUID) -> list[Jalon]:
    result = await db.execute(
        select(Jalon)
        .where(Jalon.affaire_id == affaire_id)
        .order_by(Jalon.date_cible)
    )
    return result.scalars().all()


async def update_jalon(db: AsyncSession, jalon: Jalon, data: dict) -> Jalon:
    for k, v in data.items():
        if v is not None:
            setattr(jalon, k, v)
    await db.flush()
    return jalon


async def delete_jalon(db: AsyncSession, jalon: Jalon) -> None:
    await db.delete(jalon)


# ══════════════════════════════════════════════════════════════════════
# LIENS DE DÉPENDANCE
# ══════════════════════════════════════════════════════════════════════

async def create_lien(
    db: AsyncSession,
    predecesseur_id: UUID,
    successeur_id: UUID,
    type: str = "FS",
    delai_jours: int = 0,
) -> LienDependance:
    lien = LienDependance(
        predecesseur_id=predecesseur_id,
        successeur_id=successeur_id,
        type=type,
        delai_jours=delai_jours,
    )
    db.add(lien)
    await db.flush()
    return lien


async def get_lien(db: AsyncSession, lien_id: UUID) -> LienDependance | None:
    return await db.get(LienDependance, lien_id)


async def list_liens(db: AsyncSession, affaire_id: UUID) -> list[LienDependance]:
    """Retourne tous les liens dont le prédécesseur appartient à l'affaire."""
    result = await db.execute(
        select(LienDependance)
        .join(Tache, Tache.id == LienDependance.predecesseur_id)
        .where(Tache.affaire_id == affaire_id)
    )
    return result.scalars().all()


async def delete_lien(db: AsyncSession, lien: LienDependance) -> None:
    await db.delete(lien)


# ══════════════════════════════════════════════════════════════════════
# CHEMIN CRITIQUE (CPM)
# ══════════════════════════════════════════════════════════════════════

async def compute_critical_path(db: AsyncSession, affaire_id: UUID) -> dict:
    """
    Algorithme CPM complet sur le DAG des tâches d'une affaire.

    Durée utilisée (par priorité) :
      1. (date_fin_prevue - date_debut_prevue).days   si les deux sont renseignées
      2. duree_jours
      3. 1 jour par défaut

    Retourne un dict compatible avec CriticalPathResult.
    Met à jour le flag `tache.critique` en base.
    """
    taches = await list_taches(db, affaire_id)
    if not taches:
        return {
            "affaire_id": str(affaire_id),
            "duree_projet_jours": 0,
            "nb_taches_critiques": 0,
            "cycle_detecte": False,
            "taches": [],
        }

    liens = await list_liens(db, affaire_id)

    # Durée effective de chaque tâche
    def _dur(t: Tache) -> int:
        if t.date_debut_prevue and t.date_fin_prevue:
            d = (t.date_fin_prevue - t.date_debut_prevue).days
            return max(d, 1)
        return max(t.duree_jours or 1, 1)

    durations: dict[UUID, int] = {t.id: _dur(t) for t in taches}
    task_ids: list[UUID] = [t.id for t in taches]

    # Graphe
    successors: dict[UUID, list[tuple[UUID, int]]] = defaultdict(list)
    predecessors: dict[UUID, list[tuple[UUID, int]]] = defaultdict(list)
    for lien in liens:
        # On ne gère que FS pour le CPM en v1
        if lien.type == "FS":
            successors[lien.predecesseur_id].append((lien.successeur_id, lien.delai_jours))
            predecessors[lien.successeur_id].append((lien.predecesseur_id, lien.delai_jours))

    # ── Tri topologique (Kahn) ────────────────────────────────────────
    in_degree: dict[UUID, int] = defaultdict(int)
    for _, succs in successors.items():
        for succ_id, _ in succs:
            in_degree[succ_id] += 1

    queue: deque[UUID] = deque(
        [t_id for t_id in task_ids if in_degree[t_id] == 0]
    )
    topo_order: list[UUID] = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for succ_id, _ in successors[node]:
            in_degree[succ_id] -= 1
            if in_degree[succ_id] == 0:
                queue.append(succ_id)

    cycle_detected = len(topo_order) != len(task_ids)

    # Pour les nœuds dans un cycle (non atteints par Kahn), on les ajoute tels quels
    if cycle_detected:
        visited = set(topo_order)
        for t_id in task_ids:
            if t_id not in visited:
                topo_order.append(t_id)

    # ── Forward pass : EST / EFT ─────────────────────────────────────
    EST: dict[UUID, int] = {t_id: 0 for t_id in task_ids}
    EFT: dict[UUID, int] = {}
    for t_id in topo_order:
        for pred_id, lag in predecessors[t_id]:
            EST[t_id] = max(EST[t_id], EFT.get(pred_id, durations[pred_id]) + lag)
        EFT[t_id] = EST[t_id] + durations[t_id]

    project_end = max(EFT.values(), default=0)

    # ── Backward pass : LFT / LST ────────────────────────────────────
    LFT: dict[UUID, int] = {t_id: project_end for t_id in task_ids}
    LST: dict[UUID, int] = {}
    for t_id in reversed(topo_order):
        LST[t_id] = LFT[t_id] - durations[t_id]
        for pred_id, lag in predecessors[t_id]:
            LFT[pred_id] = min(LFT[pred_id], LST[t_id] - lag)

    # ── Float & chemin critique ──────────────────────────────────────
    floats: dict[UUID, int] = {t_id: LST[t_id] - EST[t_id] for t_id in task_ids}
    critical_ids: set[UUID] = {t_id for t_id, f in floats.items() if f == 0}

    # Mise à jour en base
    task_map = {t.id: t for t in taches}
    for t_id in task_ids:
        task_map[t_id].critique = t_id in critical_ids
    await db.flush()

    return {
        "affaire_id": str(affaire_id),
        "duree_projet_jours": project_end,
        "nb_taches_critiques": len(critical_ids),
        "cycle_detecte": cycle_detected,
        "taches": [
            {
                "id": t.id,
                "titre": t.titre,
                "est": EST[t.id],
                "eft": EFT[t.id],
                "lst": LST[t.id],
                "lft": LFT[t.id],
                "float_jours": floats[t.id],
                "critique": t.id in critical_ids,
            }
            for t in taches
        ],
    }


# ══════════════════════════════════════════════════════════════════════
# PROPAGATION DE DÉCALAGES
# ══════════════════════════════════════════════════════════════════════

async def propagate_delays(
    db: AsyncSession, tache_id: UUID, delta_jours: int
) -> list[dict]:
    """
    Propage un décalage de `delta_jours` (positif = retard) à tous les
    successeurs transitifs via les liens FS.

    La tâche source elle-même n'est pas modifiée ici — c'est la
    responsabilité du caller (PATCH /taches/{id}).

    Retourne la liste des tâches impactées avec leurs anciennes et nouvelles dates.
    """
    if delta_jours == 0:
        return []

    delta = timedelta(days=delta_jours)

    # BFS sur les liens FS sortants
    visited: set[UUID] = set()
    queue: deque[UUID] = deque([tache_id])

    while queue:
        current_id = queue.popleft()
        result = await db.execute(
            select(LienDependance).where(
                LienDependance.predecesseur_id == current_id,
                LienDependance.type == "FS",
            )
        )
        for lien in result.scalars().all():
            if lien.successeur_id not in visited:
                visited.add(lien.successeur_id)
                queue.append(lien.successeur_id)

    if not visited:
        return []

    result = await db.execute(
        select(Tache).where(Tache.id.in_(visited))
    )
    affected_tasks = result.scalars().all()

    output: list[dict] = []
    for t in affected_tasks:
        old_debut = t.date_debut_prevue
        old_fin = t.date_fin_prevue
        if t.date_debut_prevue:
            t.date_debut_prevue = t.date_debut_prevue + delta
        if t.date_fin_prevue:
            t.date_fin_prevue = t.date_fin_prevue + delta
        output.append({
            "id": str(t.id),
            "titre": t.titre,
            "decalage_jours": delta_jours,
            "old_debut": old_debut.isoformat() if old_debut else None,
            "new_debut": t.date_debut_prevue.isoformat() if t.date_debut_prevue else None,
            "old_fin": old_fin.isoformat() if old_fin else None,
            "new_fin": t.date_fin_prevue.isoformat() if t.date_fin_prevue else None,
        })

    await db.flush()
    return output


# ══════════════════════════════════════════════════════════════════════
# SANTÉ DU PLANNING
# ══════════════════════════════════════════════════════════════════════

async def get_health(db: AsyncSession, affaire_id: UUID) -> dict:
    """KPIs de santé du planning pour une affaire."""
    today = date.today()

    taches = await list_taches(db, affaire_id)
    jalons = await list_jalons(db, affaire_id)
    lots = await list_lots(db, affaire_id)

    # ── Tâches ────────────────────────────────────────────────────────
    non_annulees = [t for t in taches if t.statut != "annulee"]
    t_planifiees = sum(1 for t in taches if t.statut == "planifiee")
    t_en_cours = sum(1 for t in taches if t.statut == "en_cours")
    t_terminees = sum(1 for t in taches if t.statut == "terminee")
    t_bloquees = sum(1 for t in taches if t.statut == "bloquee")
    t_en_retard = sum(
        1 for t in non_annulees
        if t.date_fin_prevue and t.date_fin_prevue < today
        and t.statut not in ("terminee", "annulee")
    )
    avancement_moyen = (
        sum(t.avancement for t in non_annulees) / len(non_annulees)
        if non_annulees else 0.0
    )

    # ── Jalons ────────────────────────────────────────────────────────
    j_atteints = sum(1 for j in jalons if j.statut == "atteint")
    j_manques = sum(
        1 for j in jalons
        if j.date_cible < today and j.statut != "atteint"
    )
    j_a_venir = sum(1 for j in jalons if j.statut == "a_venir")

    # ── Lots ──────────────────────────────────────────────────────────
    l_en_cours = sum(1 for lot in lots if lot.statut == "en_cours")
    l_termines = sum(1 for lot in lots if lot.statut == "termine")

    # ── Score 0-100 ───────────────────────────────────────────────────
    # Pénalités : tâches en retard, jalons manqués, bloquées
    total = len(non_annulees) or 1
    retard_ratio = t_en_retard / total
    bloque_ratio = t_bloquees / total
    jalon_ratio = j_manques / max(len(jalons), 1)

    score = max(
        0,
        round(
            100
            - (retard_ratio * 40)
            - (bloque_ratio * 20)
            - (jalon_ratio * 30)
            - ((100 - avancement_moyen) * 0.1)
        ),
    )

    return {
        "affaire_id": str(affaire_id),
        "total_taches": len(taches),
        "taches_planifiees": t_planifiees,
        "taches_en_cours": t_en_cours,
        "taches_terminees": t_terminees,
        "taches_bloquees": t_bloquees,
        "taches_en_retard": t_en_retard,
        "avancement_moyen": round(avancement_moyen, 1),
        "total_jalons": len(jalons),
        "jalons_atteints": j_atteints,
        "jalons_manques": j_manques,
        "jalons_a_venir": j_a_venir,
        "total_lots": len(lots),
        "lots_en_cours": l_en_cours,
        "lots_termines": l_termines,
        "score_sante": score,
    }
