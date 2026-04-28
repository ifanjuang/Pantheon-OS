from pathlib import Path

from core.registries.workflows import WorkflowDefinitionLoader


def test_document_analysis_workflow_definition_is_valid():
    workflow_dir = Path("workflows/document_analysis")

    workflow = WorkflowDefinitionLoader(Path(".")).load_one(workflow_dir)

    assert workflow is not None
    assert workflow.id == "document_analysis"
    assert workflow.pattern == "cascade"
    assert list(workflow.task_map()) == [
        "extract_facts",
        "validate_facts",
        "synthesize_document",
    ]
    assert workflow.task_map()["validate_facts"].dependencies == ["extract_facts"]
    assert workflow.task_map()["synthesize_document"].dependencies == ["validate_facts"]
