"""Static repository for Pantheon OS Domain Layer definitions.

The repository intentionally starts as an in-code registry. This is simpler and
safer than binding the new Domain Layer to the previous autonomous runtime before
the post-pivot audit is complete.
"""

from __future__ import annotations

from .contracts import (
    ActionKind,
    AgentDefinition,
    ApprovalClassification,
    ApprovalClassificationRequest,
    ApprovalDecision,
    ComponentStatus,
    DomainLayerSnapshot,
    KnowledgeCollectionDefinition,
    Layer,
    LegacyComponentDefinition,
    MemoryStoreDefinition,
    SkillDefinition,
    WorkflowDefinition,
)


class DomainLayerRepository:
    """Read-only source of Pantheon definitions for API exposure."""

    def snapshot(self) -> DomainLayerSnapshot:
        return DomainLayerSnapshot(
            layers={
                "openwebui": "Interface chat, knowledge collections, RAG documentaire simple.",
                "hermes": "Runtime agentique, skills exécutables, tools, scheduler, doctor, gateways, mémoire opérationnelle.",
                "pantheon": "Domain Operating Layer, agents abstraits, workflows, skills contracts, mémoire validée, gouvernance.",
                "legacy_runtime": "Ancienne trajectoire FastAPI/runtime autonome à auditer avant conservation ou archivage.",
            },
            agents=self.agents(),
            skills=self.skills(),
            workflows=self.workflows(),
            memory_stores=self.memory_stores(),
            knowledge_collections=self.knowledge_collections(),
            legacy_components=self.legacy_components(),
        )

    def agents(self) -> list[AgentDefinition]:
        return [
            AgentDefinition(
                id="zeus",
                name="ZEUS",
                role="Orchestration, arbitrage, routing et terminaison sûre.",
                responsibilities=[
                    "Décider quels agents sont utiles.",
                    "Arbitrer les contradictions.",
                    "Déterminer si une validation humaine est nécessaire.",
                    "Maintenir le workflow dans son périmètre.",
                ],
                limits=[
                    "Ne devient pas un god-object.",
                    "Ne contourne pas THEMIS.",
                    "Ne modifie pas de fichier sans validation.",
                ],
                activation_triggers=["run structuré", "contradiction", "décision sensible", "workflow multi-étapes"],
                output_contract=["decision", "selected_agents", "approval_required", "next_step"],
            ),
            AgentDefinition(
                id="athena",
                name="ATHENA",
                role="Planification, classification et décomposition.",
                responsibilities=["Comprendre la demande.", "Découper les étapes.", "Sélectionner workflow ou skill."],
                limits=["Ne valide pas la vérité.", "N’exécute pas d’action sensible."],
                activation_triggers=["demande complexe", "besoin de plan", "ambiguïté de workflow"],
                output_contract=["plan", "inputs", "workflow_candidate", "risks"],
            ),
            AgentDefinition(
                id="argos",
                name="ARGOS",
                role="Observation, extraction factuelle et preuves.",
                responsibilities=["Extraire faits, entités, dates, montants et sources.", "Distinguer source, inférence et hypothèse."],
                limits=["Ne transforme pas un fait candidat en vérité.", "Ne conclut pas seul."],
                activation_triggers=["documents", "audit", "comparaison", "citations nécessaires"],
                output_contract=["facts", "sources", "uncertainties", "contradictions"],
            ),
            AgentDefinition(
                id="themis",
                name="THEMIS",
                role="Règle, procédure, légitimité, approval et veto.",
                responsibilities=["Identifier les actions soumises à validation.", "Bloquer les effets de bord non autorisés."],
                limits=["N’invente pas de règles métier hors overlay.", "Ne remplace pas la validation humaine."],
                activation_triggers=["C4", "C5", "effet de bord", "responsabilité", "contrat", "sécurité"],
                output_contract=["approval_status", "veto", "risk", "lift_condition"],
            ),
            AgentDefinition(
                id="apollo",
                name="APOLLO",
                role="Validation finale, confiance et qualité.",
                responsibilities=["Vérifier le support des claims.", "Évaluer cohérence et certitude."],
                limits=["Ne transforme pas une hypothèse en fait.", "Ne remplace pas les sources."],
                activation_triggers=["sortie finale", "réponse sensible", "forte incertitude"],
                output_contract=["confidence", "unsupported_claims", "final_quality_gate"],
            ),
            AgentDefinition(
                id="prometheus",
                name="PROMETHEUS",
                role="Contradiction, stress-test et anti-consensus.",
                responsibilities=["Attaquer les hypothèses faibles.", "Repérer les conclusions prématurées."],
                limits=["Ne gouverne pas seul.", "Ne bloque pas sans règle explicite."],
                activation_triggers=["enjeu élevé", "décision fragile", "solution trop consensuelle"],
                output_contract=["objections", "alternative_paths", "residual_risks"],
            ),
            AgentDefinition(
                id="hestia",
                name="HESTIA",
                role="Mémoire projet.",
                responsibilities=["Maintenir faits, décisions, risques et contraintes d’un projet."],
                limits=["Ne stocke pas tout.", "Ne promeut pas sans source."],
                activation_triggers=["mémoire projet", "continuité", "contradiction projet"],
                output_contract=["project_memory_candidates", "existing_memory_conflicts"],
            ),
            AgentDefinition(
                id="mnemosyne",
                name="MNEMOSYNE",
                role="Mémoire agence, patterns et capitalisation.",
                responsibilities=["Identifier les méthodes réutilisables.", "Proposer patterns, clauses et templates."],
                limits=["Ne généralise pas sans validation.", "Ne reçoit pas le bruit projet."],
                activation_triggers=["pattern réutilisable", "clause", "template", "préférence agence"],
                output_contract=["agency_memory_candidates", "generalization_rationale"],
            ),
            AgentDefinition(
                id="iris",
                name="IRIS",
                role="Communication.",
                responsibilities=["Adapter le ton.", "Produire emails, messages et synthèses."],
                limits=["Ne change pas le fond validé.", "N’envoie rien sans approval."],
                activation_triggers=["email", "message", "note client", "synthèse externe"],
                output_contract=["draft", "tone", "recipient_risk"],
            ),
            AgentDefinition(
                id="hephaestus",
                name="HEPHAESTUS",
                role="Analyse technique, robustesse et faisabilité.",
                responsibilities=["Examiner contraintes techniques et dépendances.", "Identifier risques d’implémentation."],
                limits=["Ne devient pas agent métier unique.", "Reçoit le contexte métier via overlay."],
                activation_triggers=["technique", "architecture système", "faisabilité", "dépendances"],
                output_contract=["technical_findings", "implementation_risks", "constraints"],
            ),
        ]

    def skills(self) -> list[SkillDefinition]:
        return [
            SkillDefinition(
                id="cctp_audit",
                name="Audit CCTP",
                domain="architecture",
                purpose="Auditer un CCTP contre structure, lots, pièces attendues, DOE, DPGF, risques et contradictions.",
                agents=["athena", "argos", "themis", "apollo"],
                inputs=["cctp", "programme", "lot_structure", "constraints"],
                outputs=["diagnostic", "inconsistency_table", "risks", "corrections"],
                knowledge_sources=["architecture_cctp_models", "architecture_contract_clauses"],
                approval_required_if=[ActionKind.FILE_MUTATION, ActionKind.EXTERNAL_COMMUNICATION, ActionKind.MEMORY_PROMOTION],
                risks=["Surinterprétation réglementaire", "modification contractuelle non validée"],
            ),
            SkillDefinition(
                id="dpgf_check",
                name="Contrôle DPGF",
                domain="architecture",
                purpose="Comparer quantités, unités, lots, oublis, doublons et cohérence CCTP/DPGF.",
                agents=["athena", "argos", "hephaestus", "apollo"],
                inputs=["dpgf", "cctp", "plans_optional"],
                outputs=["quantity_findings", "missing_items", "duplicate_items", "risk_level"],
                knowledge_sources=["architecture_dpgf_models", "architecture_cctp_models"],
                approval_required_if=[ActionKind.FILE_MUTATION, ActionKind.EXTERNAL_COMMUNICATION],
                risks=["Quantités non vérifiables sans plans", "confusion forfait / quantitatif"],
            ),
            SkillDefinition(
                id="notice_architecturale",
                name="Notice architecturale",
                domain="architecture",
                purpose="Produire une notice claire, structurée et cohérente avec programme, site, autorisations et stratégie projet.",
                agents=["athena", "argos", "iris", "apollo"],
                inputs=["programme", "site", "constraints", "tone"],
                outputs=["notice_draft", "missing_information", "validation_points"],
                knowledge_sources=["architecture_notices"],
                approval_required_if=[ActionKind.EXTERNAL_COMMUNICATION, ActionKind.FILE_MUTATION],
                risks=["Promesse non documentée", "contradiction avec autorisation"],
            ),
            SkillDefinition(
                id="repo_md_audit",
                name="Audit code / Markdown",
                domain="software",
                purpose="Comparer l’état réel du code avec les Markdown de référence et classer les écarts.",
                agents=["athena", "argos", "themis", "apollo"],
                inputs=["repository", "reference_markdowns"],
                outputs=["diagnostic", "inconsistency_table", "code_decisions", "documentation_decisions"],
                knowledge_sources=["software_repo_docs", "pantheon_governance"],
                approval_required_if=[ActionKind.FILE_MUTATION, ActionKind.DESTRUCTIVE],
                risks=["Suppression prématurée de code utile", "documentation non alignée"],
            ),
            SkillDefinition(
                id="source_check",
                name="Vérification des sources",
                domain="generic",
                purpose="Distinguer source fiable, source obsolète, hypothèse, inférence et information non supportée.",
                agents=["argos", "apollo", "themis"],
                inputs=["claims", "sources"],
                outputs=["supported_claims", "unsupported_claims", "source_quality"],
                knowledge_sources=["pantheon_governance"],
                approval_required_if=[ActionKind.MEMORY_PROMOTION],
                risks=["Fausse certitude", "source obsolète"],
            ),
            SkillDefinition(
                id="client_message",
                name="Message client",
                domain="generic",
                purpose="Rédiger un message clair, humain, proportionné et juridiquement prudent sans changer le fond validé.",
                agents=["iris", "themis", "apollo"],
                inputs=["facts", "recipient", "tone", "risk_level"],
                outputs=["draft", "approval_required", "risk_notes"],
                knowledge_sources=["pantheon_governance"],
                approval_required_if=[ActionKind.EXTERNAL_COMMUNICATION],
                risks=["Engagement involontaire", "ton inadapté"],
            ),
        ]

    def workflows(self) -> list[WorkflowDefinition]:
        return [
            WorkflowDefinition(
                id="repo_consistency_audit",
                name="Audit cohérence repo / Markdown",
                domain="software",
                purpose="Auditer le dépôt après pivot documentaire avant toute suppression ou réorientation de code.",
                steps=[
                    "Lire les six Markdown de référence.",
                    "Inventorier le code existant.",
                    "Classer chaque composant legacy.",
                    "Identifier contradictions et doublons.",
                    "Produire décisions documentation/code.",
                ],
                agents=["athena", "argos", "themis", "apollo"],
                skills=["repo_md_audit", "source_check"],
                approval_points=[ActionKind.FILE_MUTATION, ActionKind.DESTRUCTIVE],
                memory_targets=["memory/project/decisions", "memory/candidates/pending_rules"],
                fallback="Ne rien supprimer ; marquer à auditer.",
            ),
            WorkflowDefinition(
                id="memory_promotion",
                name="Promotion mémoire",
                domain="generic",
                purpose="Transformer une information candidate en mémoire Pantheon validée, ou la rejeter.",
                steps=["Identifier source", "Qualifier scope", "Vérifier conflit", "Demander validation", "Promouvoir ou rejeter"],
                agents=["hestia", "mnemosyne", "argos", "themis", "zeus"],
                skills=["source_check"],
                approval_points=[ActionKind.MEMORY_PROMOTION],
                memory_targets=["memory/project", "memory/agency", "memory/candidates"],
                fallback="Conserver comme candidate non active.",
            ),
            WorkflowDefinition(
                id="skill_promotion",
                name="Promotion skill",
                domain="generic",
                purpose="Évaluer une skill candidate avant activation officielle.",
                steps=["Lire SKILL.md", "Vérifier manifest", "Vérifier exemples", "Vérifier risques", "Valider ou archiver"],
                agents=["athena", "themis", "apollo", "hephaestus"],
                skills=["source_check"],
                approval_points=[ActionKind.FILE_MUTATION, ActionKind.MEMORY_PROMOTION],
                memory_targets=["memory/candidates/pending_skills"],
                fallback="Rester candidate.",
            ),
        ]

    def memory_stores(self) -> list[MemoryStoreDefinition]:
        return [
            MemoryStoreDefinition(
                id="project_memory",
                name="Mémoire projet",
                owner="hestia",
                purpose="Faits, décisions, risques et contraintes propres à un projet.",
                accepted_entries=["facts", "decisions", "risks", "constraints"],
                promotion_rule="Source identifiable + utilité durable + validation humaine si impact projet.",
                rejection_rule="Bruit, hypothèse non supportée, doublon ou information périmée.",
            ),
            MemoryStoreDefinition(
                id="agency_memory",
                name="Mémoire agence",
                owner="mnemosyne",
                purpose="Patterns, clauses, préférences, méthodes et templates réutilisables.",
                accepted_entries=["patterns", "clauses", "preferences", "templates"],
                promotion_rule="Généralisable au-delà d’un projet + validé + non contradictoire.",
                rejection_rule="Cas trop local, règle fragile, conflit avec doctrine ou absence de source.",
            ),
            MemoryStoreDefinition(
                id="candidate_memory",
                name="Mémoire candidate",
                owner="argos",
                purpose="Zone tampon pour faits, skills et règles proposés mais non actifs.",
                accepted_entries=["candidate_facts", "candidate_skills", "candidate_rules"],
                promotion_rule="Revue par agent responsable + validation selon criticité.",
                rejection_rule="Non vérifiable, redondant, obsolète ou risqué.",
            ),
        ]

    def knowledge_collections(self) -> list[KnowledgeCollectionDefinition]:
        return [
            KnowledgeCollectionDefinition(
                id="pantheon_governance",
                name="Pantheon Governance",
                purpose="Markdown de référence, règles de gouvernance, doctrine agents, modules et mémoire.",
                accepted_documents=["README", "ARCHITECTURE", "AGENTS", "MODULES", "ROADMAP", "STATUS", "AI_LOG"],
                excluded_documents=["drafts non validés", "logs bruts non synthétisés"],
                reliability_rule="Les six Markdown de référence prévalent sur tout autre document.",
            ),
            KnowledgeCollectionDefinition(
                id="architecture_cctp_models",
                name="Architecture CCTP Models",
                purpose="Modèles CCTP, clauses techniques et exemples agence.",
                accepted_documents=["CCTP", "lots", "DOE", "clauses techniques"],
                excluded_documents=["anciens modèles non marqués", "documents projet sans statut"],
                reliability_rule="Un modèle obsolète doit être marqué avant usage.",
            ),
            KnowledgeCollectionDefinition(
                id="architecture_dpgf_models",
                name="Architecture DPGF Models",
                purpose="Trames DPGF, unités, postes récurrents, contrôles quantitatifs.",
                accepted_documents=["DPGF", "tableaux de lots", "postes types"],
                excluded_documents=["devis entreprises non validés comme modèle"],
                reliability_rule="Toujours distinguer modèle, projet réel et estimation.",
            ),
            KnowledgeCollectionDefinition(
                id="architecture_contract_clauses",
                name="Architecture Contract Clauses",
                purpose="Clauses contractuelles, pénalités, DET, AOR, réception, DGD, DOE.",
                accepted_documents=["clauses", "CCAP", "modèles courriers", "règles mission"],
                excluded_documents=["avis juridique non vérifié"],
                reliability_rule="Ne pas transformer une clause type en avis juridique universel.",
            ),
            KnowledgeCollectionDefinition(
                id="software_repo_docs",
                name="Software Repo Docs",
                purpose="Documentation de dépôt, architecture logicielle, audits et décisions code.",
                accepted_documents=["README", "ARCHITECTURE", "STATUS", "CODE_AUDIT", "AI_LOG"],
                excluded_documents=["logs CI non interprétés"],
                reliability_rule="Comparer au code avant de conclure qu’une fonction existe.",
            ),
        ]

    def legacy_components(self) -> list[LegacyComponentDefinition]:
        return [
            LegacyComponentDefinition(
                id="fastapi_runtime",
                name="FastAPI autonomous runtime",
                path="platform/api/",
                previous_role="Runtime principal autonome avec modules dynamiques.",
                proposed_decision="Réorienter en façade Domain Layer et éventuel outil d’intégration Hermes.",
                risk="Conserver deux runtimes concurrents si non cadré.",
            ),
            LegacyComponentDefinition(
                id="module_registry",
                name="ModuleRegistry + modules.yaml",
                path="platform/api/core/registry.py, modules.yaml",
                previous_role="Chargement dynamique des apps API.",
                proposed_decision="Auditer ; conserver seulement si utile pour façade API ou legacy admin.",
                risk="Réactiver une architecture autonome non alignée.",
            ),
            LegacyComponentDefinition(
                id="workflow_loader",
                name="WorkflowDefinitionLoader",
                path="platform/api/core/registries/workflows.py",
                previous_role="Chargement workflow.yaml/tasks.yaml.",
                proposed_decision="Réorienter vers lecture des workflows contractuels Pantheon ou archiver.",
                risk="Double définition des workflows.",
            ),
            LegacyComponentDefinition(
                id="approval_api",
                name="Approval Gate API",
                path="platform/api/apps/approvals/",
                previous_role="Module HITL logiciel minimal.",
                proposed_decision="Conserver comme option future, désactivée tant que PolicyGate n’est pas stabilisé.",
                risk="Migration Alembic et DB inutiles si le pivot reste documentaire au départ.",
            ),
            LegacyComponentDefinition(
                id="installer_ui",
                name="Installer UI NAS",
                path="scripts/install/ui/",
                previous_role="Installation Pantheon autonome + Ollama LAN.",
                proposed_decision="Réorienter vers Hermes Lab isolé + diagnostic OpenWebUI/Ollama.",
                risk="Installer trop intrusif sur NAS existant.",
            ),
        ]

    def classify_approval(self, request: ApprovalClassificationRequest) -> ApprovalClassification:
        if request.action_kind in {ActionKind.DIAGNOSTIC, ActionKind.READ, ActionKind.DRAFT}:
            return ApprovalClassification(
                action_kind=request.action_kind,
                decision=ApprovalDecision.NOT_REQUIRED,
                reason="Diagnostic, lecture et brouillon sont autorisés sans effet de bord.",
                required_human_validation=False,
            )

        if request.action_kind is ActionKind.SECRET_OR_VOLUME_ACCESS:
            return ApprovalClassification(
                action_kind=request.action_kind,
                decision=ApprovalDecision.FORBIDDEN_UNTIL_POLICY_EXISTS,
                reason="Accès secrets, volumes sensibles ou Docker socket interdit tant qu’une policy explicite n’existe pas.",
                required_human_validation=True,
                blocked_until_policy_exists=True,
            )

        return ApprovalClassification(
            action_kind=request.action_kind,
            decision=ApprovalDecision.REQUIRED,
            reason="Action à effet de bord ou mémoire durable : validation humaine requise.",
            required_human_validation=True,
        )
