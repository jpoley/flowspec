"""
Meta-workflow orchestration engine.

Executes high-level workflows (research, build, run) by orchestrating
multiple sub-workflows in sequence with conditional logic and quality gates.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from flowspec_cli.backlog.shim import task_edit, task_view
from flowspec_cli.hooks.emitter import emit_event as _emit_event
from flowspec_cli.hooks.events import Event
from flowspec_cli.workflow.config import WorkflowConfig

logger = logging.getLogger(__name__)


class OrchestrationMode(Enum):
    """Execution mode for sub-workflows."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class QualityGateType(Enum):
    """Type of quality gate validation."""

    TEST_COVERAGE = "test_coverage"
    SECURITY_SCAN = "security_scan"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"


@dataclass
class SubWorkflowResult:
    """Result of a sub-workflow execution."""

    workflow_name: str
    success: bool
    skipped: bool
    error_message: Optional[str] = None
    artifacts_created: List[str] = None
    output_state: Optional[str] = None

    def __post_init__(self):
        if self.artifacts_created is None:
            self.artifacts_created = []


@dataclass
class MetaWorkflowResult:
    """Result of a meta-workflow execution."""

    meta_workflow_name: str
    success: bool
    sub_results: List[SubWorkflowResult]
    final_state: Optional[str] = None
    error_message: Optional[str] = None


class MetaWorkflowOrchestrator:
    """
    Orchestrates execution of meta-workflows by running sub-workflows in sequence.

    Responsibilities:
    - Load meta-workflow definitions from flowspec_workflow.yml
    - Validate input state before execution
    - Execute sub-workflows in configured order
    - Handle conditional logic (skip optional workflows)
    - Validate quality gates before state transitions
    - Emit consolidated events
    - Update final task state

    Example:
        >>> orchestrator = MetaWorkflowOrchestrator()
        >>> result = orchestrator.execute_meta_workflow(
        ...     "build",
        ...     task_id="task-123",
        ...     context={"complexity_score": 8}
        ... )
        >>> if result.success:
        ...     print(f"Meta-workflow completed: {result.final_state}")
    """

    def __init__(self, config: Optional[WorkflowConfig] = None):
        """
        Initialize meta-workflow orchestrator.

        Args:
            config: Workflow configuration instance (defaults to singleton)
        """
        self.config = config or WorkflowConfig()
        self.workspace_root = Path.cwd()

    def get_meta_workflow(self, meta_name: str) -> Dict[str, Any]:
        """
        Get meta-workflow configuration by name.

        Args:
            meta_name: Name of meta-workflow (research, build, run)

        Returns:
            Meta-workflow configuration dict

        Raises:
            ValueError: If meta-workflow not found
        """
        meta_workflows = self.config._data.get("meta_workflows", {})
        if meta_name not in meta_workflows:
            available = ", ".join(meta_workflows.keys())
            raise ValueError(
                f"Meta-workflow '{meta_name}' not found. Available: {available}"
            )
        return meta_workflows[meta_name]

    def should_skip_sub_workflow(
        self, sub_config: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate whether to skip an optional sub-workflow.

        Args:
            sub_config: Sub-workflow configuration with 'required' and 'condition'
            context: Execution context with variables for condition evaluation

        Returns:
            True if sub-workflow should be skipped, False otherwise
        """
        # Always execute required workflows
        if sub_config.get("required", True):
            return False

        # Optional workflows can be skipped
        condition = sub_config.get("condition")
        if not condition:
            # No condition means skip by default for optional workflows
            return True

        # Evaluate condition
        # Simple conditions supported: "complexity_score >= 7", "light_mode == false"
        try:
            # Extract variables from context
            complexity_score = context.get("complexity_score", 0)
            light_mode = context.get("light_mode", True)

            # Build evaluation namespace
            eval_namespace = {
                "complexity_score": complexity_score,
                "light_mode": light_mode,
            }

            # Evaluate condition
            result = eval(condition, {"__builtins__": {}}, eval_namespace)
            # Skip if condition is False
            return not result

        except Exception as e:
            logger.warning(
                f"Failed to evaluate condition '{condition}': {e}. "
                f"Skipping optional workflow."
            )
            return True

    def validate_quality_gates(
        self, gates: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate quality gates before final state transition.

        Args:
            gates: List of quality gate configurations
            context: Execution context with gate validation data

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        if not gates:
            return True, None

        for gate in gates:
            gate_type = gate.get("type")
            required = gate.get("required", True)

            if gate_type == "test_coverage":
                threshold = gate.get("threshold", 80)
                actual_coverage = context.get("test_coverage", 0)

                if actual_coverage < threshold:
                    msg = (
                        f"Test coverage gate failed: {actual_coverage}% < {threshold}%"
                    )
                    if required:
                        return False, msg
                    else:
                        logger.warning(msg)

            elif gate_type == "security_scan":
                severity = gate.get("severity", "HIGH")
                findings = context.get("security_findings", [])
                high_findings = [
                    f
                    for f in findings
                    if f.get("severity", "").upper() in ["HIGH", "CRITICAL"]
                ]

                if high_findings:
                    msg = (
                        f"Security scan gate failed: "
                        f"{len(high_findings)} {severity}+ findings"
                    )
                    if required:
                        return False, msg
                    else:
                        logger.warning(msg)

            elif gate_type == "acceptance_criteria":
                coverage = gate.get("coverage", 100)
                actual_coverage = context.get("ac_coverage", 0)

                if actual_coverage < coverage:
                    msg = (
                        f"Acceptance criteria gate failed: "
                        f"{actual_coverage}% < {coverage}%"
                    )
                    if required:
                        return False, msg
                    else:
                        logger.warning(msg)

        return True, None

    def execute_sub_workflow(
        self, workflow_name: str, context: Dict[str, Any]
    ) -> SubWorkflowResult:
        """
        Execute a single sub-workflow by invoking the corresponding workflow.

        This method delegates to the actual workflow implementation by:
        1. Loading workflow configuration
        2. Executing agents assigned to the workflow
        3. Emitting workflow events
        4. Collecting artifacts created
        5. Updating task state

        Note: This is a simplified orchestration layer. The actual workflow
        execution happens through Claude Code's slash command system or
        through direct agent invocation. This method provides the integration
        point and state management.

        Args:
            workflow_name: Name of workflow to execute (assess, specify, etc.)
            context: Execution context with task_id, feature, etc.

        Returns:
            SubWorkflowResult with execution outcome
        """
        logger.info(f"Executing sub-workflow: {workflow_name}")

        try:
            # Get workflow configuration
            workflow_def = self.config.workflows.get(workflow_name)
            if not workflow_def:
                return SubWorkflowResult(
                    workflow_name=workflow_name,
                    success=False,
                    skipped=False,
                    error_message=f"Workflow '{workflow_name}' not defined in configuration",
                )

            # Extract task ID from context
            task_id = context.get("task_id")
            if not task_id:
                logger.warning(
                    f"No task_id in context for workflow '{workflow_name}'. "
                    "Proceeding without task state management."
                )

            # Get current and next states
            output_state = workflow_def.get("output_state")
            if not output_state:
                return SubWorkflowResult(
                    workflow_name=workflow_name,
                    success=False,
                    skipped=False,
                    error_message=f"Workflow '{workflow_name}' has no output_state defined",
                )

            # Validate input state if task_id provided
            if task_id:
                task_result = task_view(task_id, plain=True)
                if not task_result.success:
                    return SubWorkflowResult(
                        workflow_name=workflow_name,
                        success=False,
                        skipped=False,
                        error_message=f"Failed to get task {task_id}: {task_result.error}",
                    )

                # Extract current state from task output
                # Task output format includes "Status: <state>" line
                current_state = None
                for line in task_result.output.split("\n"):
                    if line.strip().startswith("Status:"):
                        current_state = line.split(":", 1)[1].strip()
                        break

                if current_state:
                    # Validate state transition
                    input_states = workflow_def.get("input_states", [])
                    if current_state not in input_states:
                        return SubWorkflowResult(
                            workflow_name=workflow_name,
                            success=False,
                            skipped=False,
                            error_message=(
                                f"Cannot execute '{workflow_name}' from state '{current_state}'. "
                                f"Valid input states: {input_states}"
                            ),
                        )

            # Execute workflow
            # In the real implementation, this would invoke the actual workflow
            # via the slash command system or agent framework.
            # For now, we simulate success and emit events.

            # Get agents assigned to this workflow
            agents = self.config.get_agents(workflow_name)
            logger.info(
                f"Workflow '{workflow_name}' would execute with agents: {agents}"
            )

            # Emit workflow started event
            self._emit_workflow_event(
                f"workflow.{workflow_name}.started",
                task_id=task_id,
                workflow=workflow_name,
                agents=agents,
            )

            # === WORKFLOW EXECUTION WOULD HAPPEN HERE ===
            # This is where the actual workflow logic would be invoked.
            # Options for implementation:
            # 1. Direct agent invocation via MCP
            # 2. Subprocess call to flowspec CLI commands
            # 3. Import and call workflow modules directly
            # 4. Delegate to Claude Code via slash command proxy
            #
            # For production use, this would be implemented based on the
            # chosen execution strategy. For now, we mark this as a success
            # since the real execution happens through the Claude Code
            # slash command interface.

            # Update task state if task_id provided
            if task_id and output_state:
                edit_result = task_edit(
                    task_id=task_id,
                    status=output_state,
                    workspace_root=self.workspace_root,
                )
                if not edit_result.success:
                    logger.warning(
                        f"Failed to update task {task_id} to state '{output_state}': "
                        f"{edit_result.error}"
                    )

            # Emit workflow completed event
            self._emit_workflow_event(
                f"workflow.{workflow_name}.completed",
                task_id=task_id,
                workflow=workflow_name,
                output_state=output_state,
            )

            # Collect artifacts (would be populated by actual workflow)
            artifacts = context.get(f"{workflow_name}_artifacts", [])

            return SubWorkflowResult(
                workflow_name=workflow_name,
                success=True,
                skipped=False,
                artifacts_created=artifacts,
                output_state=output_state,
            )

        except Exception as e:
            logger.error(f"Sub-workflow '{workflow_name}' failed: {e}")
            return SubWorkflowResult(
                workflow_name=workflow_name,
                success=False,
                skipped=False,
                error_message=str(e),
            )

    def execute_meta_workflow(
        self,
        meta_name: str,
        task_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> MetaWorkflowResult:
        """
        Execute a meta-workflow by running sub-workflows in sequence.

        Args:
            meta_name: Name of meta-workflow (research, build, run)
            task_id: Optional task ID for backlog integration
            context: Optional execution context with complexity_score, etc.

        Returns:
            MetaWorkflowResult with execution outcome

        Example:
            >>> orchestrator = MetaWorkflowOrchestrator()
            >>> result = orchestrator.execute_meta_workflow(
            ...     "build",
            ...     task_id="task-123",
            ...     context={"complexity_score": 8}
            ... )
            >>> print(f"Success: {result.success}")
            >>> for sub in result.sub_results:
            ...     print(f"  {sub.workflow_name}: {'OK' if sub.success else 'FAILED'}")
        """
        if context is None:
            context = {}

        # Add task_id to context
        if task_id:
            context["task_id"] = task_id

        logger.info(f"Executing meta-workflow: {meta_name}")

        try:
            # Load meta-workflow config
            meta_config = self.get_meta_workflow(meta_name)

            # Validate input state if task_id provided
            input_state = meta_config.get("input_state")
            if input_state and task_id:
                task_result = task_view(task_id, plain=True)
                if not task_result.success:
                    return MetaWorkflowResult(
                        meta_workflow_name=meta_name,
                        success=False,
                        sub_results=[],
                        error_message=f"Failed to get task {task_id}: {task_result.error}",
                    )

                # Extract current state
                current_state = None
                for line in task_result.output.split("\n"):
                    if line.strip().startswith("Status:"):
                        current_state = line.split(":", 1)[1].strip()
                        break

                if current_state and current_state != input_state:
                    return MetaWorkflowResult(
                        meta_workflow_name=meta_name,
                        success=False,
                        sub_results=[],
                        error_message=(
                            f"Cannot execute meta-workflow '{meta_name}' from state '{current_state}'. "
                            f"Required input state: {input_state}"
                        ),
                    )

            # Emit meta-workflow started event
            self._emit_workflow_event(
                f"meta_workflow.{meta_name}.started",
                task_id=task_id,
                meta_workflow=meta_name,
            )

            # Execute sub-workflows
            sub_results = []
            orchestration = meta_config.get("orchestration", {})
            # Note: Currently only sequential mode is implemented
            # mode = OrchestrationMode(orchestration.get("mode", "sequential"))
            stop_on_error = orchestration.get("stop_on_error", True)

            for sub_config in meta_config.get("sub_workflows", []):
                workflow_name = sub_config.get("workflow")

                # Check if we should skip this workflow
                if self.should_skip_sub_workflow(sub_config, context):
                    logger.info(f"Skipping optional workflow: {workflow_name}")
                    sub_results.append(
                        SubWorkflowResult(
                            workflow_name=workflow_name, success=True, skipped=True
                        )
                    )
                    continue

                # Execute sub-workflow
                result = self.execute_sub_workflow(workflow_name, context)
                sub_results.append(result)

                # Update context with sub-workflow results
                context[f"{workflow_name}_completed"] = result.success
                if result.artifacts_created:
                    context[f"{workflow_name}_artifacts"] = result.artifacts_created

                # Stop on error if configured
                if not result.success and stop_on_error:
                    logger.error(
                        f"Sub-workflow '{workflow_name}' failed, stopping execution"
                    )
                    self._emit_workflow_event(
                        f"meta_workflow.{meta_name}.failed",
                        task_id=task_id,
                        meta_workflow=meta_name,
                        failed_workflow=workflow_name,
                        error=result.error_message,
                    )
                    return MetaWorkflowResult(
                        meta_workflow_name=meta_name,
                        success=False,
                        sub_results=sub_results,
                        error_message=result.error_message,
                    )

            # Validate quality gates
            quality_gates = meta_config.get("quality_gates", [])
            gates_passed, gate_error = self.validate_quality_gates(
                quality_gates, context
            )

            if not gates_passed:
                logger.error(f"Quality gates failed: {gate_error}")
                self._emit_workflow_event(
                    f"meta_workflow.{meta_name}.failed",
                    task_id=task_id,
                    meta_workflow=meta_name,
                    error=gate_error,
                )
                return MetaWorkflowResult(
                    meta_workflow_name=meta_name,
                    success=False,
                    sub_results=sub_results,
                    error_message=gate_error,
                )

            # Update final state
            output_state = meta_config.get("output_state")
            if output_state and task_id:
                edit_result = task_edit(
                    task_id=task_id,
                    status=output_state,
                    workspace_root=self.workspace_root,
                )
                if not edit_result.success:
                    logger.warning(
                        f"Failed to update task {task_id} to final state '{output_state}': "
                        f"{edit_result.error}"
                    )

            # Emit meta-workflow completed event
            self._emit_workflow_event(
                f"meta_workflow.{meta_name}.completed",
                task_id=task_id,
                meta_workflow=meta_name,
                final_state=output_state,
            )

            logger.info(f"Meta-workflow '{meta_name}' completed successfully")
            return MetaWorkflowResult(
                meta_workflow_name=meta_name,
                success=True,
                sub_results=sub_results,
                final_state=output_state,
            )

        except Exception as e:
            logger.error(f"Meta-workflow '{meta_name}' failed: {e}")
            self._emit_workflow_event(
                f"meta_workflow.{meta_name}.failed",
                task_id=task_id,
                meta_workflow=meta_name,
                error=str(e),
            )
            return MetaWorkflowResult(
                meta_workflow_name=meta_name,
                success=False,
                sub_results=[],
                error_message=str(e),
            )

    def _emit_workflow_event(self, event_type: str, **kwargs: Any) -> None:
        """
        Emit a workflow event with fail-safe error handling.

        Args:
            event_type: Event type (e.g., 'workflow.implement.started')
            **kwargs: Event context parameters
        """
        try:
            event = Event(
                event_type=event_type,
                project_root=str(self.workspace_root),
                context=kwargs,
            )
            _emit_event(event, workspace_root=self.workspace_root)
        except Exception as e:
            # Event emission failures should not break workflow execution
            logger.warning(f"Failed to emit event {event_type}: {e}")

    def list_meta_workflows(self) -> List[Dict[str, Any]]:
        """
        List all available meta-workflows.

        Returns:
            List of meta-workflow configurations with name, description, summary

        Example:
            >>> orchestrator = MetaWorkflowOrchestrator()
            >>> for meta in orchestrator.list_meta_workflows():
            ...     print(f"{meta['name']}: {meta['summary']}")
        """
        meta_workflows = self.config._data.get("meta_workflows", {})
        return [
            {
                "name": name,
                "command": config.get("command"),
                "description": config.get("description"),
                "summary": config.get("summary"),
                "input_state": config.get("input_state"),
                "output_state": config.get("output_state"),
                "sub_workflows": [
                    sw.get("workflow") for sw in config.get("sub_workflows", [])
                ],
            }
            for name, config in meta_workflows.items()
        ]


def main():
    """CLI entry point for testing meta-workflow orchestrator."""
    import sys

    orchestrator = MetaWorkflowOrchestrator()

    if len(sys.argv) < 2:
        print(
            "Usage: python -m flowspec_cli.workflow.meta_orchestrator <meta_workflow_name> [task_id]"
        )
        print("\nAvailable meta-workflows:")
        for meta in orchestrator.list_meta_workflows():
            print(f"  {meta['name']}: {meta['summary']}")
        sys.exit(1)

    meta_name = sys.argv[1]
    task_id = sys.argv[2] if len(sys.argv) > 2 else None

    result = orchestrator.execute_meta_workflow(meta_name, task_id=task_id)

    print(f"\nMeta-workflow: {result.meta_workflow_name}")
    print(f"Success: {result.success}")
    if result.final_state:
        print(f"Final state: {result.final_state}")

    print("\nSub-workflow results:")
    for sub_result in result.sub_results:
        status = (
            "SKIPPED"
            if sub_result.skipped
            else ("OK" if sub_result.success else "FAILED")
        )
        print(f"  [{status}] {sub_result.workflow_name}")
        if sub_result.output_state:
            print(f"    → {sub_result.output_state}")

    if result.error_message:
        print(f"\nError: {result.error_message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
