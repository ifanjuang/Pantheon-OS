from pathlib import Path

from core.registries.workflows import WorkflowDefinitionLoader


def test_workflow_loader_returns_empty_when_folder_missing(tmp_path: Path):
    loader = WorkflowDefinitionLoader(tmp_path)

    assert loader.load_all() == []


def test_workflow_loader_loads_workflow_with_tasks_yaml(tmp_path: Path):
    workflow_dir = tmp_path / "workflows" / "document_analysis"
    workflow_dir.mkdir(parents=True)

    (workflow_dir / "workflow.yaml").write_text(
        "id: document_analysis\ndescription: Analyze a document\npattern: cascade\noutputs:\n  - validated_facts\n",
        encoding="utf-8",
    )
    (workflow_dir / "tasks.yaml").write_text(
        "tasks:\n"
        "  - id: extract\n"
        "    description: Extract factual constraints\n"
        "    expected_output: Candidate facts with sources\n"
        "    assigned_agent: argos\n"
        "  - id: validate\n"
        "    description: Validate extracted facts\n"
        "    expected_output: Validated facts or objections\n"
        "    assigned_agent: apollo\n"
        "    dependencies: [extract]\n",
        encoding="utf-8",
    )

    loader = WorkflowDefinitionLoader(tmp_path)
    workflows = loader.load_all()

    assert len(workflows) == 1
    workflow = workflows[0]
    assert workflow.id == "document_analysis"
    assert list(workflow.task_map()) == ["extract", "validate"]


def test_workflow_loader_loads_inline_tasks_when_tasks_yaml_absent(tmp_path: Path):
    workflow_dir = tmp_path / "workflows" / "inline"
    workflow_dir.mkdir(parents=True)

    (workflow_dir / "workflow.yaml").write_text(
        "id: inline\n"
        "description: Inline task workflow\n"
        "tasks:\n"
        "  - id: plan\n"
        "    description: Plan execution\n"
        "    expected_output: Execution plan\n"
        "    assigned_role: planner\n",
        encoding="utf-8",
    )

    workflow = WorkflowDefinitionLoader(tmp_path).load_one(workflow_dir)

    assert workflow is not None
    assert workflow.id == "inline"
    assert workflow.tasks[0].id == "plan"


def test_workflow_loader_rejects_duplicate_task_sources(tmp_path: Path):
    workflow_dir = tmp_path / "workflows" / "duplicate_sources"
    workflow_dir.mkdir(parents=True)

    (workflow_dir / "workflow.yaml").write_text(
        "id: duplicate_sources\n"
        "description: Invalid workflow\n"
        "tasks:\n"
        "  - id: plan\n"
        "    description: Plan execution\n"
        "    expected_output: Execution plan\n"
        "    assigned_role: planner\n",
        encoding="utf-8",
    )
    (workflow_dir / "tasks.yaml").write_text(
        "tasks:\n"
        "  - id: execute\n"
        "    description: Execute plan\n"
        "    expected_output: Execution result\n"
        "    assigned_agent: zeus\n",
        encoding="utf-8",
    )

    workflow = WorkflowDefinitionLoader(tmp_path).load_one(workflow_dir)

    assert workflow is None


def test_workflow_loader_skips_invalid_workflow_and_loads_valid_one(tmp_path: Path):
    valid_dir = tmp_path / "workflows" / "valid"
    invalid_dir = tmp_path / "workflows" / "invalid"
    valid_dir.mkdir(parents=True)
    invalid_dir.mkdir(parents=True)

    (valid_dir / "workflow.yaml").write_text(
        "id: valid\n"
        "description: Valid workflow\n"
        "tasks:\n"
        "  - id: plan\n"
        "    description: Plan execution\n"
        "    expected_output: Execution plan\n"
        "    assigned_role: planner\n",
        encoding="utf-8",
    )
    (invalid_dir / "workflow.yaml").write_text(
        "id: invalid\n"
        "description: Invalid workflow\n"
        "tasks:\n"
        "  - id: validate\n"
        "    description: Validate missing dependency\n"
        "    expected_output: Validation report\n"
        "    assigned_agent: apollo\n"
        "    dependencies: [missing]\n",
        encoding="utf-8",
    )

    workflows = WorkflowDefinitionLoader(tmp_path).load_all()

    assert [workflow.id for workflow in workflows] == ["valid"]
