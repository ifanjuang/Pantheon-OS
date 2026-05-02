from pathlib import Path

from core.registries.loader import ManifestLoader


def test_manifest_loader_returns_empty_lists_when_modules_folder_is_missing(tmp_path: Path):
    loader = ManifestLoader(tmp_path / "missing")

    assert loader.load_agents() == []
    assert loader.load_skills() == []
    assert loader.load_workflows() == []


def test_manifest_loader_loads_enabled_manifests_and_skips_disabled(tmp_path: Path):
    agents_dir = tmp_path / "agents" / "meta" / "zeus_orchestrator"
    agents_dir.mkdir(parents=True)
    (agents_dir / "manifest.yaml").write_text(
        "id: zeus\n" "name: '@ZEUS'\n" "type: agent\n" "enabled: true\n",
        encoding="utf-8",
    )

    disabled_dir = tmp_path / "agents" / "meta" / "disabled_agent"
    disabled_dir.mkdir(parents=True)
    (disabled_dir / "manifest.yaml").write_text(
        "id: disabled\n" "type: agent\n" "enabled: false\n",
        encoding="utf-8",
    )

    loader = ManifestLoader(tmp_path)
    agents = loader.load_agents()

    assert len(agents) == 1
    assert agents[0].id == "zeus"
    assert agents[0].type == "agent"
    assert agents[0].manifest["name"] == "@ZEUS"


def test_manifest_loader_uses_folder_name_as_fallback_id(tmp_path: Path):
    skill_dir = tmp_path / "skills" / "extract_facts"
    skill_dir.mkdir(parents=True)
    (skill_dir / "manifest.yaml").write_text(
        "description: Extract facts\n",
        encoding="utf-8",
    )

    loader = ManifestLoader(tmp_path)
    skills = loader.load_skills()

    assert len(skills) == 1
    assert skills[0].id == "extract_facts"
    assert skills[0].type == "skill"
