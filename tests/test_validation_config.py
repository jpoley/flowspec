"""Tests for validation configuration management."""

import pytest
import yaml

from specify_cli.workflow.validation_config import (
    ValidationConfig,
    get_default_config,
    load_config,
    save_config,
)


class TestValidationConfig:
    """Tests for ValidationConfig dataclass."""

    def test_init_default(self):
        """Test ValidationConfig initialization with defaults."""
        config = ValidationConfig()
        assert config.version == "1.0"
        assert config.transitions == {}

    def test_init_with_transitions(self):
        """Test ValidationConfig initialization with transitions."""
        transitions = {
            "specify": "KEYWORD[PRD_APPROVED]",
            "plan": "PULL_REQUEST",
        }
        config = ValidationConfig(version="1.0", transitions=transitions)
        assert config.version == "1.0"
        assert config.transitions == transitions

    def test_get_validation_mode_existing(self):
        """Test getting validation mode for existing transition."""
        config = ValidationConfig(transitions={"specify": "KEYWORD[PRD_APPROVED]"})
        assert config.get_validation_mode("specify") == "KEYWORD[PRD_APPROVED]"

    def test_get_validation_mode_missing(self):
        """Test getting validation mode for missing transition returns NONE."""
        config = ValidationConfig()
        assert config.get_validation_mode("specify") == "NONE"

    def test_set_validation_mode_valid(self):
        """Test setting valid validation mode."""
        config = ValidationConfig()
        config.set_validation_mode("specify", 'KEYWORD["APPROVED"]')
        assert config.transitions["specify"] == 'KEYWORD["APPROVED"]'

    def test_set_validation_mode_none(self):
        """Test setting NONE validation mode."""
        config = ValidationConfig()
        config.set_validation_mode("specify", "NONE")
        assert config.transitions["specify"] == "NONE"

    def test_set_validation_mode_pull_request(self):
        """Test setting PULL_REQUEST validation mode."""
        config = ValidationConfig()
        config.set_validation_mode("plan", "PULL_REQUEST")
        assert config.transitions["plan"] == "PULL_REQUEST"

    def test_set_validation_mode_invalid(self):
        """Test setting invalid validation mode raises ValueError."""
        config = ValidationConfig()
        with pytest.raises(ValueError, match="Invalid validation mode"):
            config.set_validation_mode("specify", "INVALID")

    def test_to_dict(self):
        """Test converting config to dictionary format."""
        config = ValidationConfig(
            version="1.0",
            transitions={
                "specify": "KEYWORD[PRD_APPROVED]",
                "plan": "PULL_REQUEST",
            },
        )
        data = config.to_dict()
        assert data["version"] == "1.0"
        assert len(data["transitions"]) == 2
        assert {"name": "specify", "validation": "KEYWORD[PRD_APPROVED]"} in data[
            "transitions"
        ]
        assert {"name": "plan", "validation": "PULL_REQUEST"} in data["transitions"]

    def test_from_dict_valid(self):
        """Test creating config from valid dictionary."""
        data = {
            "version": "1.0",
            "transitions": [
                {"name": "specify", "validation": "KEYWORD[PRD_APPROVED]"},
                {"name": "plan", "validation": "PULL_REQUEST"},
            ],
        }
        config = ValidationConfig.from_dict(data)
        assert config.version == "1.0"
        assert config.transitions["specify"] == "KEYWORD[PRD_APPROVED]"
        assert config.transitions["plan"] == "PULL_REQUEST"

    def test_from_dict_empty_transitions(self):
        """Test creating config from dict with empty transitions."""
        data = {"version": "1.0", "transitions": []}
        config = ValidationConfig.from_dict(data)
        assert config.version == "1.0"
        assert config.transitions == {}

    def test_from_dict_missing_version(self):
        """Test creating config from dict without version uses default."""
        data = {
            "transitions": [
                {"name": "specify", "validation": "NONE"},
            ]
        }
        config = ValidationConfig.from_dict(data)
        assert config.version == "1.0"
        assert config.transitions["specify"] == "NONE"

    def test_from_dict_invalid_transition_format(self):
        """Test creating config from dict with invalid transition format."""
        data = {
            "version": "1.0",
            "transitions": ["invalid"],
        }
        with pytest.raises(ValueError, match="Invalid transition format"):
            ValidationConfig.from_dict(data)

    def test_from_dict_missing_transition_name(self):
        """Test creating config from dict with missing transition name."""
        data = {
            "version": "1.0",
            "transitions": [
                {"validation": "NONE"},
            ],
        }
        with pytest.raises(ValueError, match="missing 'name' field"):
            ValidationConfig.from_dict(data)


class TestGetDefaultConfig:
    """Tests for get_default_config function."""

    def test_returns_config_with_all_transitions(self):
        """Test that default config includes all known transitions."""
        config = get_default_config()
        assert isinstance(config, ValidationConfig)
        assert config.version == "1.0"
        # Check that all known transitions are present
        assert "assess" in config.transitions
        assert "specify" in config.transitions
        assert "research" in config.transitions
        assert "plan" in config.transitions
        assert "implement" in config.transitions
        assert "validate" in config.transitions
        assert "operate" in config.transitions
        assert "complete" in config.transitions

    def test_all_transitions_set_to_none(self):
        """Test that all default transitions are set to NONE."""
        config = get_default_config()
        for transition_name, mode in config.transitions.items():
            assert mode == "NONE", f"Transition {transition_name} should be NONE"


class TestSaveConfig:
    """Tests for save_config function."""

    def test_save_config_creates_file(self, tmp_path):
        """Test that save_config creates a YAML file."""
        config = ValidationConfig(transitions={"specify": "KEYWORD[APPROVED]"})
        config_path = tmp_path / "jpspec_workflow.yml"

        save_config(config, config_path)

        assert config_path.exists()

    def test_save_config_creates_parent_directories(self, tmp_path):
        """Test that save_config creates parent directories."""
        config = ValidationConfig()
        config_path = tmp_path / "subdir" / "jpspec_workflow.yml"

        save_config(config, config_path)

        assert config_path.exists()
        assert config_path.parent.exists()

    def test_save_config_valid_yaml(self, tmp_path):
        """Test that saved config is valid YAML."""
        config = ValidationConfig(
            version="1.0",
            transitions={
                "specify": "KEYWORD[PRD_APPROVED]",
                "plan": "PULL_REQUEST",
            },
        )
        config_path = tmp_path / "jpspec_workflow.yml"

        save_config(config, config_path)

        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert data["version"] == "1.0"
        assert len(data["transitions"]) == 2

    def test_save_and_load_roundtrip(self, tmp_path):
        """Test that save and load preserve config data."""
        original = ValidationConfig(
            version="1.0",
            transitions={
                "specify": "KEYWORD[PRD_APPROVED]",
                "plan": "PULL_REQUEST",
                "assess": "NONE",
            },
        )
        config_path = tmp_path / "jpspec_workflow.yml"

        save_config(original, config_path)
        loaded = load_config(config_path)

        assert loaded.version == original.version
        assert loaded.transitions == original.transitions


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_file_not_found(self, tmp_path):
        """Test that load_config raises FileNotFoundError for missing file."""
        config_path = tmp_path / "nonexistent.yml"
        with pytest.raises(FileNotFoundError, match="not found"):
            load_config(config_path)

    def test_load_config_valid_file(self, tmp_path):
        """Test loading valid configuration file."""
        config_path = tmp_path / "jpspec_workflow.yml"
        data = {
            "version": "1.0",
            "transitions": [
                {"name": "specify", "validation": "KEYWORD[PRD_APPROVED]"},
                {"name": "plan", "validation": "PULL_REQUEST"},
            ],
        }
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)

        config = load_config(config_path)

        assert config.version == "1.0"
        assert config.transitions["specify"] == "KEYWORD[PRD_APPROVED]"
        assert config.transitions["plan"] == "PULL_REQUEST"

    def test_load_config_empty_file(self, tmp_path):
        """Test loading empty configuration file raises ValueError."""
        config_path = tmp_path / "jpspec_workflow.yml"
        config_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="Invalid configuration format"):
            load_config(config_path)

    def test_load_config_invalid_yaml(self, tmp_path):
        """Test loading invalid YAML raises appropriate error."""
        config_path = tmp_path / "jpspec_workflow.yml"
        config_path.write_text("invalid: yaml: content:", encoding="utf-8")

        with pytest.raises(yaml.YAMLError):
            load_config(config_path)


class TestIntegration:
    """Integration tests for validation config workflow."""

    def test_default_config_workflow(self, tmp_path):
        """Test complete workflow with default config."""
        # Get default config
        config = get_default_config()
        assert all(mode == "NONE" for mode in config.transitions.values())

        # Modify some transitions
        config.set_validation_mode("specify", 'KEYWORD["PRD_APPROVED"]')
        config.set_validation_mode("plan", "PULL_REQUEST")

        # Save to file
        config_path = tmp_path / ".specify" / "jpspec_workflow.yml"
        save_config(config, config_path)

        # Load and verify
        loaded = load_config(config_path)
        assert loaded.get_validation_mode("specify") == 'KEYWORD["PRD_APPROVED"]'
        assert loaded.get_validation_mode("plan") == "PULL_REQUEST"
        assert loaded.get_validation_mode("assess") == "NONE"

    def test_update_existing_config(self, tmp_path):
        """Test updating an existing configuration."""
        config_path = tmp_path / "jpspec_workflow.yml"

        # Create initial config
        config = get_default_config()
        config.set_validation_mode("specify", 'KEYWORD["APPROVED"]')
        save_config(config, config_path)

        # Load and modify
        loaded = load_config(config_path)
        loaded.set_validation_mode("specify", "PULL_REQUEST")
        loaded.set_validation_mode("plan", 'KEYWORD["PLAN_APPROVED"]')
        save_config(loaded, config_path)

        # Verify changes
        final = load_config(config_path)
        assert final.get_validation_mode("specify") == "PULL_REQUEST"
        assert final.get_validation_mode("plan") == 'KEYWORD["PLAN_APPROVED"]'
