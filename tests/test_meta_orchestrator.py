"""Tests for meta-workflow orchestrator."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from flowspec_cli.workflow.meta_orchestrator import (
    MetaWorkflowOrchestrator,
)
from flowspec_cli.workflow.config import WorkflowConfig


@pytest.fixture
def mock_config():
    """Create a mock workflow configuration with meta-workflows."""
    config_data = {
        "version": "2.0",
        "states": ["To Do", "Planned", "Validated", "Deployed"],
        "workflows": {
            "assess": {
                "command": "/flow:assess",
                "agents": ["workflow-assessor"],
                "input_states": ["To Do"],
                "output_state": "Assessed",
            },
            "specify": {
                "command": "/flow:specify",
                "agents": ["product-requirements-manager"],
                "input_states": ["Assessed"],
                "output_state": "Specified",
            },
            "plan": {
                "command": "/flow:plan",
                "agents": ["software-architect"],
                "input_states": ["Specified"],
                "output_state": "Planned",
            },
            "implement": {
                "command": "/flow:implement",
                "agents": ["backend-engineer", "frontend-engineer"],
                "input_states": ["Planned"],
                "output_state": "In Implementation",
            },
            "validate": {
                "command": "/flow:validate",
                "agents": ["quality-guardian"],
                "input_states": ["In Implementation"],
                "output_state": "Validated",
            },
        },
        "meta_workflows": {
            "research": {
                "command": "/flow:research",
                "description": "Plan It - All analysis and design before implementation",
                "summary": "Assess + Specify + Plan",
                "sub_workflows": [
                    {"workflow": "assess", "required": True},
                    {"workflow": "specify", "required": True},
                    {"workflow": "plan", "required": True},
                ],
                "input_state": "To Do",
                "output_state": "Planned",
                "orchestration": {
                    "mode": "sequential",
                    "stop_on_error": True,
                },
            },
            "build": {
                "command": "/flow:build",
                "description": "Create It - Code, tests, and quality gates",
                "summary": "Implement + Validate",
                "sub_workflows": [
                    {"workflow": "implement", "required": True},
                    {"workflow": "validate", "required": True},
                ],
                "input_state": "Planned",
                "output_state": "Validated",
                "quality_gates": [
                    {"type": "test_coverage", "threshold": 80, "required": True},
                    {"type": "security_scan", "severity": "HIGH", "required": True},
                ],
                "orchestration": {
                    "mode": "sequential",
                    "stop_on_error": True,
                },
            },
        },
    }
    return WorkflowConfig(config_data)


def test_meta_orchestrator_init(mock_config):
    """Test meta-workflow orchestrator initialization."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)
    assert orchestrator.config == mock_config
    assert orchestrator.workspace_root == Path.cwd()


def test_get_meta_workflow(mock_config):
    """Test retrieving meta-workflow configuration."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Valid meta-workflow
    research = orchestrator.get_meta_workflow("research")
    assert research["command"] == "/flow:research"
    assert len(research["sub_workflows"]) == 3

    # Invalid meta-workflow
    with pytest.raises(ValueError, match="Meta-workflow 'invalid' not found"):
        orchestrator.get_meta_workflow("invalid")


def test_list_meta_workflows(mock_config):
    """Test listing all meta-workflows."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)
    meta_list = orchestrator.list_meta_workflows()

    assert len(meta_list) == 2
    names = [m["name"] for m in meta_list]
    assert "research" in names
    assert "build" in names

    # Check structure
    research = next(m for m in meta_list if m["name"] == "research")
    assert research["input_state"] == "To Do"
    assert research["output_state"] == "Planned"
    assert research["sub_workflows"] == ["assess", "specify", "plan"]


def test_should_skip_sub_workflow(mock_config):
    """Test conditional workflow skipping logic."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Required workflow - never skip
    required_config = {"required": True}
    assert not orchestrator.should_skip_sub_workflow(required_config, {})

    # Optional without condition - skip by default
    optional_config = {"required": False}
    assert orchestrator.should_skip_sub_workflow(optional_config, {})

    # Optional with condition - evaluate condition
    conditional_config = {"required": False, "condition": "complexity_score >= 7"}

    # Condition is True (complexity >= 7) -> don't skip
    context_high = {"complexity_score": 8}
    assert not orchestrator.should_skip_sub_workflow(conditional_config, context_high)

    # Condition is False (complexity < 7) -> skip
    context_low = {"complexity_score": 5}
    assert orchestrator.should_skip_sub_workflow(conditional_config, context_low)


def test_validate_quality_gates(mock_config):
    """Test quality gate validation."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Test coverage gate - passing
    gates = [{"type": "test_coverage", "threshold": 80, "required": True}]
    context = {"test_coverage": 85}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert passed
    assert error is None

    # Test coverage gate - failing
    context = {"test_coverage": 70}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert not passed
    assert "Test coverage gate failed" in error

    # Security scan gate - passing (no high findings)
    gates = [{"type": "security_scan", "severity": "HIGH", "required": True}]
    context = {"security_findings": [{"severity": "LOW"}]}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert passed

    # Security scan gate - failing (has high findings)
    context = {"security_findings": [{"severity": "HIGH"}]}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert not passed
    assert "Security scan gate failed" in error

    # Acceptance criteria gate
    gates = [{"type": "acceptance_criteria", "coverage": 100, "required": True}]
    context = {"ac_coverage": 100}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert passed

    context = {"ac_coverage": 80}
    passed, error = orchestrator.validate_quality_gates(gates, context)
    assert not passed
    assert "Acceptance criteria gate failed" in error


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
@patch("flowspec_cli.workflow.meta_orchestrator.task_edit")
@patch("flowspec_cli.workflow.meta_orchestrator._emit_event")
def test_execute_sub_workflow(mock_emit, mock_task_edit, mock_task_view, mock_config):
    """Test sub-workflow execution."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock task view response
    mock_task_view.return_value = MagicMock(
        success=True, output="Task: task-123\nStatus: Planned\nTitle: Test task"
    )
    mock_task_edit.return_value = MagicMock(success=True)

    # Execute sub-workflow
    context = {"task_id": "task-123"}
    result = orchestrator.execute_sub_workflow("implement", context)

    assert result.success
    assert result.workflow_name == "implement"
    assert result.output_state == "In Implementation"
    assert not result.skipped

    # Verify task was updated
    mock_task_edit.assert_called_once()
    call_args = mock_task_edit.call_args
    assert call_args[1]["task_id"] == "task-123"
    assert call_args[1]["status"] == "In Implementation"


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
def test_execute_sub_workflow_invalid_state(mock_task_view, mock_config):
    """Test sub-workflow execution with invalid input state."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock task in wrong state (To Do instead of Planned)
    mock_task_view.return_value = MagicMock(
        success=True, output="Task: task-123\nStatus: To Do\nTitle: Test task"
    )

    context = {"task_id": "task-123"}
    result = orchestrator.execute_sub_workflow("implement", context)

    assert not result.success
    assert "Cannot execute 'implement' from state 'To Do'" in result.error_message


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
@patch("flowspec_cli.workflow.meta_orchestrator.task_edit")
@patch("flowspec_cli.workflow.meta_orchestrator._emit_event")
def test_execute_meta_workflow_success(
    mock_emit, mock_task_edit, mock_task_view, mock_config
):
    """Test successful meta-workflow execution."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock state progression: To Do -> Assessed -> Specified -> Planned
    states = ["To Do", "Assessed", "Specified", "Planned"]
    state_index = [0]  # Use list for mutable closure

    def mock_view_side_effect(task_id, plain=True):
        state = states[min(state_index[0], len(states) - 1)]
        return MagicMock(
            success=True, output=f"Task: {task_id}\nStatus: {state}\nTitle: Test task"
        )

    def mock_edit_side_effect(task_id, status=None, **kwargs):
        if status:
            # Move to next state when status is updated
            state_index[0] = min(state_index[0] + 1, len(states) - 1)
        return MagicMock(success=True)

    mock_task_view.side_effect = mock_view_side_effect
    mock_task_edit.side_effect = mock_edit_side_effect

    # Execute meta-workflow
    result = orchestrator.execute_meta_workflow(
        "research", task_id="task-123", context={}
    )

    assert result.success
    assert result.meta_workflow_name == "research"
    assert result.final_state == "Planned"
    assert len(result.sub_results) == 3

    # All sub-workflows should have succeeded
    for sub_result in result.sub_results:
        assert sub_result.success or sub_result.skipped


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
def test_execute_meta_workflow_invalid_input_state(mock_task_view, mock_config):
    """Test meta-workflow execution with invalid input state."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock task in wrong state
    mock_task_view.return_value = MagicMock(
        success=True, output="Task: task-123\nStatus: Validated\nTitle: Test task"
    )

    # Try to execute research meta-workflow (requires To Do state)
    result = orchestrator.execute_meta_workflow("research", task_id="task-123")

    assert not result.success
    assert (
        "Cannot execute meta-workflow 'research' from state 'Validated'"
        in result.error_message
    )


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
@patch("flowspec_cli.workflow.meta_orchestrator.task_edit")
@patch("flowspec_cli.workflow.meta_orchestrator._emit_event")
def test_execute_meta_workflow_with_quality_gates(
    mock_emit, mock_task_edit, mock_task_view, mock_config
):
    """Test meta-workflow execution with quality gates."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock state progression: Planned -> In Implementation -> Validated
    states = ["Planned", "In Implementation", "Validated"]
    state_index = [0]

    def mock_view_side_effect(task_id, plain=True):
        state = states[min(state_index[0], len(states) - 1)]
        return MagicMock(
            success=True, output=f"Task: {task_id}\nStatus: {state}\nTitle: Test task"
        )

    def mock_edit_side_effect(task_id, status=None, **kwargs):
        if status:
            state_index[0] = min(state_index[0] + 1, len(states) - 1)
        return MagicMock(success=True)

    mock_task_view.side_effect = mock_view_side_effect
    mock_task_edit.side_effect = mock_edit_side_effect

    # Execute build meta-workflow with quality gates
    # Gates should pass
    result = orchestrator.execute_meta_workflow(
        "build",
        task_id="task-123",
        context={"test_coverage": 85, "security_findings": []},
    )

    assert result.success
    assert result.final_state == "Validated"


@patch("flowspec_cli.workflow.meta_orchestrator.task_view")
@patch("flowspec_cli.workflow.meta_orchestrator.task_edit")
@patch("flowspec_cli.workflow.meta_orchestrator._emit_event")
def test_execute_meta_workflow_quality_gate_failure(
    mock_emit, mock_task_edit, mock_task_view, mock_config
):
    """Test meta-workflow execution with failing quality gates."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Mock state progression: Planned -> In Implementation -> would go to Validated
    states = [
        "Planned",
        "In Implementation",
        "In Implementation",
    ]  # Stay in Implementation
    state_index = [0]

    def mock_view_side_effect(task_id, plain=True):
        state = states[min(state_index[0], len(states) - 1)]
        return MagicMock(
            success=True, output=f"Task: {task_id}\nStatus: {state}\nTitle: Test task"
        )

    def mock_edit_side_effect(task_id, status=None, **kwargs):
        if status:
            state_index[0] = min(state_index[0] + 1, len(states) - 1)
        return MagicMock(success=True)

    mock_task_view.side_effect = mock_view_side_effect
    mock_task_edit.side_effect = mock_edit_side_effect

    # Execute build meta-workflow with failing quality gates
    result = orchestrator.execute_meta_workflow(
        "build",
        task_id="task-123",
        context={"test_coverage": 60, "security_findings": []},  # Coverage too low
    )

    assert not result.success
    assert "Test coverage gate failed" in result.error_message


def test_execute_meta_workflow_without_task_id(mock_config):
    """Test meta-workflow execution without task_id."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Execute without task_id (should work but skip state management)
    result = orchestrator.execute_meta_workflow("research")

    # Should execute all sub-workflows
    assert len(result.sub_results) == 3
    assert all(
        r.workflow_name in ["assess", "specify", "plan"] for r in result.sub_results
    )


def test_emit_workflow_event_fail_safe(mock_config):
    """Test that event emission failures don't break workflow execution."""
    orchestrator = MetaWorkflowOrchestrator(config=mock_config)

    # Event emission should fail silently
    with patch(
        "flowspec_cli.workflow.meta_orchestrator._emit_event",
        side_effect=Exception("Event error"),
    ):
        # This should not raise an exception
        orchestrator._emit_workflow_event("test.event", task_id="task-123")
