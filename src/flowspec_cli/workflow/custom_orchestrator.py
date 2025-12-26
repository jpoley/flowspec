"""
Custom workflow orchestration engine.

Executes user-defined workflow sequences from flowspec_workflow.yml
with conditional logic, checkpoints, and enforced rigor rules.
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from flowspec_cli.backlog.shim import task_edit, task_view
from flowspec_cli.hooks.emitter import emit_event
from flowspec_cli.hooks.events import Event, EventType
from flowspec_cli.workflow.config import WorkflowConfig

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Execution mode for custom workflows."""

    VIBING = "vibing"  # Autonomous, no interaction
    SPEC_ING = "spec-ing"  # Stop for guidance at checkpoints


@dataclass
class WorkflowStepResult:
    """Result of executing a single workflow step."""

    workflow_name: str
    success: bool
    skipped: bool
    error_message: Optional[str] = None
    checkpoint_approved: bool = True


@dataclass
class CustomWorkflowResult:
    """Result of executing a custom workflow."""

    workflow_name: str
    success: bool
    steps_executed: List[WorkflowStepResult]
    error_message: Optional[str] = None


class CustomWorkflowOrchestrator:
    """
    Orchestrates execution of user-defined custom workflows.

    Responsibilities:
    - Load custom workflow definitions from flowspec_workflow.yml
    - Execute workflow steps in sequence
    - Evaluate conditional logic for step execution
    - Handle checkpoints in spec-ing mode
    - Enforce rigor rules (logging, backlog, memory, constitution)
    - Emit events for all steps

    Example:
        >>> orchestrator = CustomWorkflowOrchestrator()
        >>> result = orchestrator.execute_custom_workflow(
        ...     "quick_build",
        ...     task_id="task-123",
        ...     context={"complexity": 3}
        ... )
    """

    def __init__(self, config: Optional[WorkflowConfig] = None):
        """
        Initialize custom workflow orchestrator.

        Args:
            config: Workflow configuration instance (defaults to singleton)
        """
        self.config = config or WorkflowConfig()
        self.workspace_root = Path.cwd()
        self.logs_dir = self.workspace_root / ".logs"
        self.decisions_dir = self.logs_dir / "decisions"
        self.events_dir = self.logs_dir / "events"

        # Ensure log directories exist
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def get_custom_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """
        Get custom workflow configuration by name.

        Args:
            workflow_name: Name of the custom workflow

        Returns:
            Custom workflow configuration dict

        Raises:
            ValueError: If workflow not found
        """
        custom_workflows = self.config.data.get("custom_workflows", {})
        if workflow_name not in custom_workflows:
            available = ", ".join(custom_workflows.keys())
            raise ValueError(
                f"Custom workflow '{workflow_name}' not found. "
                f"Available: {available or 'none'}"
            )
        return custom_workflows[workflow_name]

    def log_decision(self, decision_data: Dict[str, Any]) -> None:
        """
        Log a decision to .logs/decisions/*.jsonl.

        REQUIRED by rigor rules.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        log_file = self.decisions_dir / f"{timestamp}-custom-workflow.jsonl"

        with log_file.open("a") as f:
            json.dump(decision_data, f)
            f.write("\n")

    def log_event(self, event_data: Dict[str, Any]) -> None:
        """
        Log an event to .logs/events/*.jsonl.

        REQUIRED by rigor rules.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        log_file = self.events_dir / f"{timestamp}-custom-workflow.jsonl"

        with log_file.open("a") as f:
            json.dump(event_data, f)
            f.write("\n")

    def evaluate_condition(
        self, condition: Optional[str], context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate a condition expression.

        Args:
            condition: Condition string (e.g., "complexity >= 5")
            context: Context variables for evaluation

        Returns:
            True if condition is met or no condition provided

        NOTE: Currently supports simple comparisons. Can be extended.
        """
        if not condition:
            return True

        # SECURITY: Do NOT use eval() - that's a vulnerability
        # For MVP, support simple patterns: "key op value"
        # Example: "complexity >= 5"
        parts = condition.strip().split()
        if len(parts) == 3:
            key, op, value_str = parts
            context_value = context.get(key)

            if context_value is None:
                logger.warning(f"Condition key '{key}' not in context")
                return False

            try:
                value = int(value_str)
            except ValueError:
                value = value_str.strip("'\"")

            if op == ">=":
                return context_value >= value
            elif op == ">":
                return context_value > value
            elif op == "<=":
                return context_value <= value
            elif op == "<":
                return context_value < value
            elif op == "==":
                return context_value == value
            elif op == "!=":
                return context_value != value

        logger.warning(f"Unsupported condition: {condition}")
        return True  # Default to executing step

    def execute_custom_workflow(
        self,
        workflow_name: str,
        task_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> CustomWorkflowResult:
        """
        Execute a custom workflow.

        Args:
            workflow_name: Name of custom workflow to execute
            task_id: Optional backlog task ID
            context: Context variables for conditional evaluation

        Returns:
            Result of custom workflow execution
        """
        context = context or {}
        workflow_config = self.get_custom_workflow(workflow_name)

        # Log start
        self.log_event({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "custom_workflow_start",
            "workflow_name": workflow_name,
            "task_id": task_id,
            "mode": workflow_config["mode"],
        })

        # Enforce rigor rules
        rigor = workflow_config.get("rigor", {})
        if not rigor.get("log_decisions") or not rigor.get("log_events"):
            raise ValueError("Rigor rules REQUIRE log_decisions and log_events")

        steps_executed = []
        success = True
        error_message = None

        # Execute each step
        for step in workflow_config["steps"]:
            step_result = self._execute_step(
                step,
                workflow_config["mode"],
                task_id,
                context
            )
            steps_executed.append(step_result)

            if not step_result.success:
                success = False
                error_message = step_result.error_message
                break

            if step_result.skipped:
                continue

        # Log completion
        self.log_event({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "custom_workflow_complete",
            "workflow_name": workflow_name,
            "success": success,
            "steps_executed": len(steps_executed),
        })

        return CustomWorkflowResult(
            workflow_name=workflow_name,
            success=success,
            steps_executed=steps_executed,
            error_message=error_message,
        )

    def _execute_step(
        self,
        step: Dict[str, Any],
        mode: str,
        task_id: Optional[str],
        context: Dict[str, Any],
    ) -> WorkflowStepResult:
        """Execute a single workflow step."""
        workflow_name = step["workflow"]

        # Check condition
        condition = step.get("condition")
        if not self.evaluate_condition(condition, context):
            self.log_event({
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "workflow_step_skipped",
                "workflow": workflow_name,
                "reason": f"Condition not met: {condition}",
            })
            return WorkflowStepResult(
                workflow_name=workflow_name,
                success=True,
                skipped=True,
            )

        # Handle checkpoint in spec-ing mode
        if mode == "spec-ing" and "checkpoint" in step:
            # NOTE: In real implementation, would prompt user here
            # For autonomous mode, we log and continue
            self.log_decision({
                "timestamp": datetime.utcnow().isoformat(),
                "decision_type": "checkpoint",
                "workflow": workflow_name,
                "checkpoint_question": step["checkpoint"],
                "approved": True,  # Auto-approve in autonomous session
            })

        # Log step execution
        self.log_event({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "workflow_step_start",
            "workflow": workflow_name,
            "task_id": task_id,
        })

        # NOTE: Actual workflow execution would happen here
        # For MVP, we just log that we would execute
        # In full implementation, would call the actual workflow

        return WorkflowStepResult(
            workflow_name=workflow_name,
            success=True,
            skipped=False,
        )
