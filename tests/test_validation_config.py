"""Tests for workflow validation configuration module."""

from unittest.mock import patch

import yaml

from specify_cli.workflow.transition import ValidationMode
from specify_cli.workflow.validation_config import (
    configure_validation_modes,
    display_validation_summary,
    generate_workflow_yaml,
    prompt_all_transitions,
    prompt_validation_mode,
)


class TestPromptValidationMode:
    """Test interactive validation mode prompts."""

    @patch("specify_cli.workflow.validation_config.Prompt.ask")
    def test_prompt_none_default(self, mock_ask):
        """Test selecting NONE (default) validation mode."""
        # Simulate pressing Enter (empty input, uses default)
        mock_ask.return_value = ""

        mode, keyword = prompt_validation_mode("specify", "Create PRD")

        assert mode == ValidationMode.NONE
        assert keyword is None

    @patch("specify_cli.workflow.validation_config.Prompt.ask")
    def test_prompt_none_explicit(self, mock_ask):
        """Test explicitly selecting NONE validation mode."""
        mock_ask.return_value = "1"

        mode, keyword = prompt_validation_mode("specify", "Create PRD")

        assert mode == ValidationMode.NONE
        assert keyword is None

    @patch("specify_cli.workflow.validation_config.Prompt.ask")
    def test_prompt_keyword_with_custom_keyword(self, mock_ask):
        """Test selecting KEYWORD mode with custom keyword."""
        # First call returns "2" for KEYWORD, second returns the keyword
        mock_ask.side_effect = ["2", "PRD_REVIEWED"]

        mode, keyword = prompt_validation_mode("specify", "Create PRD")

        assert mode == ValidationMode.KEYWORD
        assert keyword == "PRD_REVIEWED"

    @patch("specify_cli.workflow.validation_config.Prompt.ask")
    def test_prompt_keyword_with_default_keyword(self, mock_ask):
        """Test selecting KEYWORD mode with default keyword."""
        # First call returns "2" for KEYWORD, second uses default
        mock_ask.side_effect = ["2", "SPECIFY_APPROVED"]

        mode, keyword = prompt_validation_mode("specify", "Create PRD")

        assert mode == ValidationMode.KEYWORD
        assert keyword == "SPECIFY_APPROVED"

    @patch("specify_cli.workflow.validation_config.Prompt.ask")
    def test_prompt_pull_request(self, mock_ask):
        """Test selecting PULL_REQUEST validation mode."""
        mock_ask.return_value = "3"

        mode, keyword = prompt_validation_mode("plan", "Create architecture")

        assert mode == ValidationMode.PULL_REQUEST
        assert keyword is None


class TestPromptAllTransitions:
    """Test prompting for all workflow transitions."""

    def test_batch_mode_none(self):
        """Test batch mode with NONE for all transitions."""
        configs = prompt_all_transitions(batch_mode="none")

        assert len(configs) > 0
        for transition_name, (mode, keyword) in configs.items():
            assert mode == ValidationMode.NONE
            assert keyword is None

    def test_batch_mode_keyword_default(self):
        """Test batch mode with KEYWORD using default keyword."""
        configs = prompt_all_transitions(batch_mode="keyword")

        assert len(configs) > 0
        for transition_name, (mode, keyword) in configs.items():
            assert mode == ValidationMode.KEYWORD
            assert keyword == "APPROVED"

    def test_batch_mode_keyword_custom(self):
        """Test batch mode with KEYWORD using custom keyword."""
        configs = prompt_all_transitions(
            batch_mode="keyword", batch_keyword="TEAM_APPROVED"
        )

        assert len(configs) > 0
        for transition_name, (mode, keyword) in configs.items():
            assert mode == ValidationMode.KEYWORD
            assert keyword == "TEAM_APPROVED"

    def test_batch_mode_pull_request(self):
        """Test batch mode with PULL_REQUEST for all transitions."""
        configs = prompt_all_transitions(batch_mode="pull-request")

        assert len(configs) > 0
        for transition_name, (mode, keyword) in configs.items():
            assert mode == ValidationMode.PULL_REQUEST
            assert keyword is None


class TestGenerateWorkflowYaml:
    """Test YAML workflow file generation."""

    def test_generate_yaml_with_mixed_modes(self, tmp_path):
        """Test generating YAML with mixed validation modes."""
        configs = {
            "assess": (ValidationMode.NONE, None),
            "specify": (ValidationMode.KEYWORD, "PRD_APPROVED"),
            "plan": (ValidationMode.PULL_REQUEST, None),
        }

        output_path = tmp_path / "jpspec_workflow.yml"
        generate_workflow_yaml(configs, output_path)

        # Verify file was created
        assert output_path.exists()

        # Load and verify YAML structure
        with open(output_path) as f:
            data = yaml.safe_load(f)

        assert data["version"] == "1.0"
        assert "workflow" in data
        assert data["workflow"]["name"] == "jpspec"
        assert "transitions" in data
        assert len(data["transitions"]) > 0

        # Verify specific transitions
        transitions_by_name = {t["name"]: t for t in data["transitions"]}

        # Check assess (NONE)
        if "assess" in transitions_by_name:
            assert transitions_by_name["assess"]["validation"] == "NONE"

        # Check specify (KEYWORD)
        if "specify" in transitions_by_name:
            assert (
                transitions_by_name["specify"]["validation"]
                == 'KEYWORD["PRD_APPROVED"]'
            )

        # Check plan (PULL_REQUEST)
        if "plan" in transitions_by_name:
            assert transitions_by_name["plan"]["validation"] == "PULL_REQUEST"

    def test_generate_yaml_all_none(self, tmp_path):
        """Test generating YAML with all NONE validation."""
        configs = {
            "assess": (ValidationMode.NONE, None),
            "specify": (ValidationMode.NONE, None),
            "plan": (ValidationMode.NONE, None),
        }

        output_path = tmp_path / "jpspec_workflow.yml"
        generate_workflow_yaml(configs, output_path)

        assert output_path.exists()

        with open(output_path) as f:
            data = yaml.safe_load(f)

        for transition in data["transitions"]:
            assert transition["validation"] == "NONE"


class TestDisplayValidationSummary:
    """Test validation summary display."""

    @patch("specify_cli.workflow.validation_config.console")
    def test_display_summary_mixed_modes(self, mock_console):
        """Test displaying summary with mixed validation modes."""
        configs = {
            "assess": (ValidationMode.NONE, None),
            "specify": (ValidationMode.KEYWORD, "PRD_APPROVED"),
            "plan": (ValidationMode.PULL_REQUEST, None),
        }

        display_validation_summary(configs)

        # Verify console.print was called
        assert mock_console.print.called


class TestConfigureValidationModes:
    """Test main configuration function."""

    def test_configure_with_no_prompts(self, tmp_path):
        """Test configuration with --no-validation-prompts flag."""
        configure_validation_modes(tmp_path, no_prompts=True)

        workflow_path = tmp_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # All transitions should be NONE
        for transition in data["transitions"]:
            assert transition["validation"] == "NONE"

    def test_configure_batch_mode_keyword(self, tmp_path):
        """Test configuration with batch mode keyword."""
        configure_validation_modes(tmp_path, batch_mode="keyword")

        workflow_path = tmp_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # All transitions should be KEYWORD
        for transition in data["transitions"]:
            assert transition["validation"].startswith("KEYWORD")

    def test_configure_batch_mode_pull_request(self, tmp_path):
        """Test configuration with batch mode pull-request."""
        configure_validation_modes(tmp_path, batch_mode="pull-request")

        workflow_path = tmp_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # All transitions should be PULL_REQUEST
        for transition in data["transitions"]:
            assert transition["validation"] == "PULL_REQUEST"

    def test_configure_batch_mode_none(self, tmp_path):
        """Test configuration with batch mode none."""
        configure_validation_modes(tmp_path, batch_mode="none")

        workflow_path = tmp_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # All transitions should be NONE
        for transition in data["transitions"]:
            assert transition["validation"] == "NONE"

    def test_workflow_yaml_structure(self, tmp_path):
        """Test that generated YAML has correct structure."""
        configure_validation_modes(tmp_path, batch_mode="none")

        workflow_path = tmp_path / "jpspec_workflow.yml"
        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # Verify required top-level keys
        assert "version" in data
        assert "workflow" in data
        assert "transitions" in data

        # Verify workflow section
        assert "name" in data["workflow"]
        assert "description" in data["workflow"]

        # Verify transitions structure
        assert isinstance(data["transitions"], list)
        assert len(data["transitions"]) > 0

        # Verify each transition has required fields
        for transition in data["transitions"]:
            assert "name" in transition
            assert "from" in transition
            assert "to" in transition
            assert "via" in transition
            assert "validation" in transition


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios."""

    def test_init_flow_no_prompts(self, tmp_path):
        """Test typical init flow with --no-validation-prompts."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        configure_validation_modes(project_path, no_prompts=True)

        workflow_path = project_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        # Verify it's valid YAML
        with open(workflow_path) as f:
            data = yaml.safe_load(f)
            assert data is not None

    def test_init_flow_batch_keyword(self, tmp_path):
        """Test init flow with --validation-mode keyword."""
        project_path = tmp_path / "test-project"
        project_path.mkdir()

        configure_validation_modes(
            project_path, batch_mode="keyword", batch_keyword="APPROVED"
        )

        workflow_path = project_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # Spot check a transition
        transitions_by_name = {t["name"]: t for t in data["transitions"]}
        if "specify" in transitions_by_name:
            assert transitions_by_name["specify"]["validation"] == 'KEYWORD["APPROVED"]'

    def test_reconfigure_existing_project(self, tmp_path):
        """Test reconfiguring an existing project."""
        project_path = tmp_path / "existing-project"
        project_path.mkdir()

        # Initial configuration
        configure_validation_modes(project_path, batch_mode="none")

        # Reconfigure with different mode
        configure_validation_modes(project_path, batch_mode="keyword")

        workflow_path = project_path / "jpspec_workflow.yml"
        assert workflow_path.exists()

        with open(workflow_path) as f:
            data = yaml.safe_load(f)

        # Should now have KEYWORD validation
        for transition in data["transitions"]:
            assert transition["validation"].startswith("KEYWORD")
