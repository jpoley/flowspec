"""Tests for workflow configuration migration functionality.

Tests cover:
- detect_workflow_version function
- migrate_workflow_config function
- WorkflowMigrationResult dataclass
- v1.0 to v2.0 migration scenarios
- Backup mechanism
- Preservation of custom configurations
"""

import yaml

from flowspec_cli.workflow.migration import (
    TARGET_VERSION,
    WorkflowMigrationResult,
    detect_workflow_version,
    migrate_workflow_config,
)


class TestWorkflowMigrationResult:
    """Tests for WorkflowMigrationResult dataclass."""

    def test_empty_result(self):
        """Test that empty result has expected properties."""
        result = WorkflowMigrationResult()
        assert not result.migrated
        assert result.from_version is None
        assert result.to_version is None
        assert result.changes == []
        assert result.backup_path is None
        assert result.errors == []
        assert result.summary() == "no migration needed"

    def test_already_at_v2(self):
        """Test result when already at v2.0."""
        result = WorkflowMigrationResult(
            from_version="2.0",
            to_version="2.0",
        )
        assert result.summary() == "already at v2.0"

    def test_migrated_result(self):
        """Test result after migration."""
        result = WorkflowMigrationResult(
            migrated=True,
            from_version="1.0",
            to_version="2.0",
            changes=["Added roles section", "Removed operate workflow"],
        )
        assert "v1.0 -> v2.0" in result.summary()
        assert "2 changes" in result.summary()

    def test_error_result(self):
        """Test result with errors."""
        result = WorkflowMigrationResult(
            errors=["Failed to parse YAML"],
        )
        assert "1 errors" in result.summary()


class TestDetectWorkflowVersion:
    """Tests for detect_workflow_version function."""

    def test_explicit_version_2(self):
        """Test detection of explicit v2.0."""
        config = {"version": "2.0", "workflows": {}}
        assert detect_workflow_version(config) == "2.0"

    def test_explicit_version_1(self):
        """Test detection of explicit v1.0."""
        config = {"version": "1.0", "workflows": {}}
        assert detect_workflow_version(config) == "1.0"

    def test_infer_v2_from_roles(self):
        """Test inference of v2.0 from roles section."""
        config = {"roles": {"primary": "dev"}}
        assert detect_workflow_version(config) == "2.0"

    def test_infer_v2_from_custom_workflows(self):
        """Test inference of v2.0 from custom_workflows section."""
        config = {"custom_workflows": {"quick_build": {}}}
        assert detect_workflow_version(config) == "2.0"

    def test_infer_v2_from_agent_loops(self):
        """Test inference of v2.0 from agent_loops section."""
        config = {"agent_loops": {"inner": []}}
        assert detect_workflow_version(config) == "2.0"

    def test_infer_v1_from_operate(self):
        """Test inference of v1.0 from operate workflow."""
        config = {"workflows": {"operate": {"command": "/flow:operate"}}}
        assert detect_workflow_version(config) == "1.0"

    def test_infer_v1_from_deployed_state(self):
        """Test inference of v1.0 from Deployed state."""
        config = {"states": ["To Do", "In Progress", "Deployed"]}
        assert detect_workflow_version(config) == "1.0"

    def test_default_to_v1(self):
        """Test default to v1.0 when unknown."""
        config = {"workflows": {}}
        assert detect_workflow_version(config) == "1.0"


class TestMigrateWorkflowConfig:
    """Tests for migrate_workflow_config function."""

    def test_no_workflow_file(self, tmp_path):
        """Test migration when no workflow file exists."""
        result = migrate_workflow_config(tmp_path)
        assert not result.migrated
        assert result.errors == []

    def test_already_v2(self, tmp_path):
        """Test that v2.0 configs are not migrated."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        config = {
            "version": "2.0",
            "roles": {"primary": "dev"},
            "workflows": {"implement": {}},
            "agent_loops": {"inner": []},
        }
        with open(workflow_file, "w") as f:
            yaml.dump(config, f)

        result = migrate_workflow_config(tmp_path)
        assert not result.migrated
        assert result.from_version == "2.0"
        assert result.to_version == "2.0"

    def test_migrate_v1_to_v2(self, tmp_path):
        """Test full migration from v1.0 to v2.0."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {
            "version": "1.0",
            "states": ["To Do", "In Progress", "Deployed", "Done"],
            "workflows": {
                "implement": {"command": "/flow:implement"},
                "operate": {"command": "/flow:operate"},
            },
            "transitions": [
                {"name": "implement", "from": "Planned", "to": "In Implementation"},
                {"name": "operate", "from": "Validated", "to": "Deployed"},
                {"name": "complete_from_deployed", "from": "Deployed", "to": "Done"},
            ],
        }
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path)

        assert result.migrated
        assert result.from_version == "1.0"
        assert result.to_version == TARGET_VERSION
        assert result.backup_path is not None
        assert result.backup_path.exists()

        # Verify migrated config
        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        assert migrated["version"] == "2.0"
        assert "operate" not in migrated["workflows"]
        assert "Deployed" not in migrated["states"]
        assert "roles" in migrated
        assert "agent_loops" in migrated
        assert "custom_workflows" in migrated

        # Verify deprecated transitions removed
        transition_names = [t["name"] for t in migrated.get("transitions", [])]
        assert "operate" not in transition_names
        assert "complete_from_deployed" not in transition_names

    def test_dry_run(self, tmp_path):
        """Test dry run does not modify files."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        original_content = {
            "version": "1.0",
            "workflows": {"operate": {}},
        }
        with open(workflow_file, "w") as f:
            yaml.dump(original_content, f)

        result = migrate_workflow_config(tmp_path, dry_run=True)

        assert result.migrated
        assert result.backup_path is None  # No backup in dry run

        # File should be unchanged
        with open(workflow_file) as f:
            content = yaml.safe_load(f)
        assert content["version"] == "1.0"

    def test_preserves_custom_workflows(self, tmp_path):
        """Test that custom workflow definitions are preserved."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {
            "version": "1.0",
            "workflows": {
                "implement": {"command": "/flow:implement", "agents": ["custom-agent"]},
                "operate": {"command": "/flow:operate"},
                "custom_workflow": {"command": "/custom", "custom_option": True},
            },
        }
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path)

        assert result.migrated

        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        # Custom agent should be preserved
        assert migrated["workflows"]["implement"]["agents"] == ["custom-agent"]
        # Custom workflow should be preserved
        assert "custom_workflow" in migrated["workflows"]
        assert migrated["workflows"]["custom_workflow"]["custom_option"] is True

    def test_backup_location(self, tmp_path):
        """Test backup is created in specified directory."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        backup_dir = tmp_path / "backups"
        backup_dir.mkdir()

        v1_config = {"version": "1.0", "workflows": {"operate": {}}}
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path, backup_dir=backup_dir)

        assert result.migrated
        assert result.backup_path is not None
        assert result.backup_path.parent == backup_dir

    def test_invalid_yaml(self, tmp_path):
        """Test handling of invalid YAML."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        workflow_file.write_text("invalid: yaml: content:")

        result = migrate_workflow_config(tmp_path)

        assert not result.migrated
        assert len(result.errors) > 0
        assert "Failed to parse" in result.errors[0]

    def test_adds_roles_section(self, tmp_path):
        """Test that roles section is added."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {"version": "1.0", "workflows": {}}
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path)

        assert result.migrated
        assert "Added roles section" in " ".join(result.changes)

        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        assert "roles" in migrated
        assert migrated["roles"]["primary"] == "dev"
        assert "definitions" in migrated["roles"]

    def test_adds_agent_loops_section(self, tmp_path):
        """Test that agent_loops section is added."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {"version": "1.0", "workflows": {}}
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        migrate_workflow_config(tmp_path)

        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        assert "agent_loops" in migrated
        assert "inner" in migrated["agent_loops"]
        assert "outer" in migrated["agent_loops"]

    def test_adds_custom_workflows_section(self, tmp_path):
        """Test that custom_workflows section is added."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {"version": "1.0", "workflows": {}}
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        migrate_workflow_config(tmp_path)

        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        assert "custom_workflows" in migrated
        assert "quick_build" in migrated["custom_workflows"]
        assert "full_design" in migrated["custom_workflows"]
        assert "ship_it" in migrated["custom_workflows"]

    def test_updates_metadata(self, tmp_path):
        """Test that metadata is updated during migration."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {
            "version": "1.0",
            "states": ["To Do", "Deployed", "Done"],
            "workflows": {"operate": {}},
            "metadata": {
                "schema_version": "1.0",
                "state_count": 3,
                "workflow_count": 1,
            },
        }
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        migrate_workflow_config(tmp_path)

        with open(workflow_file) as f:
            migrated = yaml.safe_load(f)

        assert migrated["metadata"]["schema_version"] == "2.0"
        # State count should be updated (Deployed removed)
        assert migrated["metadata"]["state_count"] == 2  # To Do, Done
        # Workflow count should be updated (operate removed)
        assert migrated["metadata"]["workflow_count"] == 0


class TestMigrationChangesTracking:
    """Tests for tracking changes during migration."""

    def test_changes_tracked(self, tmp_path):
        """Test that all changes are tracked."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        v1_config = {
            "version": "1.0",
            "states": ["To Do", "Deployed"],
            "workflows": {"operate": {}},
            "transitions": [{"name": "operate", "via": "operate"}],
        }
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path)

        assert "Added version: 2.0" in result.changes
        assert any("operate" in c for c in result.changes)
        assert any("roles" in c.lower() for c in result.changes)
        assert any("agent_loops" in c.lower() for c in result.changes)
        assert any("custom_workflows" in c.lower() for c in result.changes)


class TestEdgeCases:
    """Tests for edge cases in migration."""

    def test_empty_config(self, tmp_path):
        """Test migration of empty config file."""
        workflow_file = tmp_path / "flowspec_workflow.yml"
        workflow_file.write_text("")

        result = migrate_workflow_config(tmp_path)

        # Empty file should result in error (yaml.safe_load returns None)
        assert not result.migrated
        assert len(result.errors) > 0

    def test_yaml_extension(self, tmp_path):
        """Test migration works with .yaml extension."""
        workflow_file = tmp_path / "flowspec_workflow.yaml"
        v1_config = {"version": "1.0", "workflows": {"operate": {}}}
        with open(workflow_file, "w") as f:
            yaml.dump(v1_config, f)

        result = migrate_workflow_config(tmp_path)

        assert result.migrated


class TestCompareWorkflowAfterExtraction:
    """Tests for compare_workflow_after_extraction function."""

    def test_new_workflow_file_added(self, tmp_path):
        """Test comparison when new workflow file is added."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project with new workflow config (after extraction)
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        workflow_file.write_text("version: '2.0'\nworkflows: {}")

        # Create backup (before extraction - no workflow)
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert result.migrated
        assert "New flowspec_workflow.yml added" in result.changes
        assert result.to_version == "2.0"

    def test_unchanged_workflow(self, tmp_path):
        """Test comparison when workflow is unchanged."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project with workflow config
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        config = {"version": "2.0", "workflows": {"implement": {}}}
        with open(workflow_file, "w") as f:
            yaml.dump(config, f)

        # Create backup with identical config
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        backup_file = backup_dir / "flowspec_workflow.yml"
        with open(backup_file, "w") as f:
            yaml.dump(config, f)

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert not result.migrated
        assert len(result.changes) == 0

    def test_version_upgrade_detected(self, tmp_path):
        """Test comparison detects version upgrade."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project with v2.0 config (after extraction)
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        v2_config = {"version": "2.0", "roles": {"primary": "dev"}}
        with open(workflow_file, "w") as f:
            yaml.dump(v2_config, f)

        # Create backup with v1.0 config
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        backup_file = backup_dir / "flowspec_workflow.yml"
        v1_config = {"version": "1.0", "workflows": {"operate": {}}}
        with open(backup_file, "w") as f:
            yaml.dump(v1_config, f)

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert result.migrated
        assert result.from_version == "1.0"
        assert result.to_version == "2.0"
        assert "Version updated: 1.0 -> 2.0" in result.changes

    def test_new_section_added(self, tmp_path):
        """Test comparison detects new sections added."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project with roles section added
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        new_config = {"version": "2.0", "workflows": {}, "roles": {"primary": "dev"}}
        with open(workflow_file, "w") as f:
            yaml.dump(new_config, f)

        # Create backup without roles section
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        backup_file = backup_dir / "flowspec_workflow.yml"
        old_config = {"version": "2.0", "workflows": {}}
        with open(backup_file, "w") as f:
            yaml.dump(old_config, f)

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert result.migrated
        assert "Added section: roles" in result.changes

    def test_deprecated_workflow_removed(self, tmp_path):
        """Test comparison detects deprecated workflow removal."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project without operate workflow (after extraction)
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        new_config = {"version": "2.0", "workflows": {"implement": {}}}
        with open(workflow_file, "w") as f:
            yaml.dump(new_config, f)

        # Create backup with operate workflow
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        backup_file = backup_dir / "flowspec_workflow.yml"
        old_config = {"version": "1.0", "workflows": {"implement": {}, "operate": {}}}
        with open(backup_file, "w") as f:
            yaml.dump(old_config, f)

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert result.migrated
        assert "Removed deprecated workflow: operate" in result.changes

    def test_no_workflow_file(self, tmp_path):
        """Test comparison when no workflow file exists."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project without workflow config
        project_root = tmp_path / "project"
        project_root.mkdir()

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert not result.migrated
        assert len(result.changes) == 0

    def test_invalid_new_yaml(self, tmp_path):
        """Test comparison handles invalid YAML in new file."""
        from flowspec_cli.workflow.migration import compare_workflow_after_extraction

        # Create project with invalid YAML
        project_root = tmp_path / "project"
        project_root.mkdir()

        workflow_file = project_root / "flowspec_workflow.yml"
        workflow_file.write_text("invalid: yaml: content:")

        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()

        result = compare_workflow_after_extraction(project_root, backup_dir)

        assert not result.migrated
        assert len(result.errors) > 0
        assert "Failed to parse" in result.errors[0]
