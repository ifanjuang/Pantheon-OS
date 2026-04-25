import pytest
from pydantic import ValidationError

from core.contracts.tasks import TaskDefinition, WorkflowDefinition, load_workflow_definition


def test_task_requires_expected_output():
    with pytest.raises(ValidationError):
        TaskDefinition(
            id="extract_constraints",
            description="Extract constraints from document",
            expected_output="",
            assigned_agent="argos",
        )


def test_agent_task_accepts_assigned_role_instead_of_specific_agent():
    task = TaskDefinition(
        id="plan_workflow",
        description="Plan the execution",
        expected_output="A structured plan",
        assigned_role="planner",
    )

    assert task.execution_mode == "agent"
    assert task.assigned_role == "planner"


def test_skill_task_requires_assigned_skill():
    with pytest.raises(ValidationError):
        TaskDefinition(
            id="extract_facts",
            description="Extract facts",
            expected_output="Candidate facts",
            execution_mode="skill",
            assigned_agent="argos",
        )


def test_critical_task_requires_approval_by_default():
    task = TaskDefinition(
        id="send_notice",
        description="Prepare external notice",
        expected_output="Draft notice ready for approval",
        assigned_agent="themis",
        criticity="C4",
    )

    assert task.is_critical() is True
    assert task.requires_approval_by_default() is True


def test_workflow_rejects_duplicate_task_ids():
    with pytest.raises(ValidationError):
        WorkflowDefinition(
            id="duplicate_test",
            description="Invalid duplicate workflow",
            tasks=[
                {
                    "id": "same",
                    "description": "First",
                    "expected_output": "First output",
                    "assigned_agent": "argos",
                },
                {
                    "id": "same",
                    "description": "Second",
                    "expected_output": "Second output",
                    "assigned_agent": "apollo",
                },
            ],
        )


def test_workflow_rejects_unknown_dependencies():
    with pytest.raises(ValidationError):
        WorkflowDefinition(
            id="bad_deps",
            description="Invalid dependency workflow",
            tasks=[
                {
                    "id": "validate",
                    "description": "Validate facts",
                    "expected_output": "Validation report",
                    "assigned_agent": "apollo",
                    "dependencies": ["extract"],
                }
            ],
        )


def test_workflow_loads_valid_yaml_like_definition():
    workflow = load_workflow_definition(
        {
            "id": "document_analysis",
            "description": "Analyze a document with extraction and validation",
            "pattern": "cascade",
            "tasks": [
                {
                    "id": "extract",
                    "description": "Extract factual constraints",
                    "expected_output": "Candidate facts with source references",
                    "assigned_agent": "argos",
                    "success_criteria": ["facts have sources"],
                },
                {
                    "id": "validate",
                    "description": "Validate extracted facts",
                    "expected_output": "Validated facts or objections",
                    "assigned_agent": "apollo",
                    "dependencies": ["extract"],
                },
            ],
        }
    )

    assert workflow.id == "document_analysis"
    assert workflow.pattern == "cascade"
    assert list(workflow.task_map()) == ["extract", "validate"]
    assert workflow.critical_tasks() == []
