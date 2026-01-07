"""Tests for flowspec init template generation (MCP, VSCode extensions)."""

import json


class TestMCPJsonGeneration:
    """Test the MCP JSON generation functionality."""

    def test_generate_mcp_json_basic(self, tmp_path, monkeypatch):
        """Generate basic .mcp.json with backlog server."""
        from flowspec_cli import generate_mcp_json

        monkeypatch.chdir(tmp_path)
        result = generate_mcp_json(tmp_path)

        # Should return True when file is created
        assert result is True

        mcp_json = tmp_path / ".mcp.json"
        assert mcp_json.exists()

        config = json.loads(mcp_json.read_text())
        assert "mcpServers" in config
        assert "backlog" in config["mcpServers"]
        assert config["mcpServers"]["backlog"]["command"] == "backlog"

    def test_generate_mcp_json_python_project(self, tmp_path, monkeypatch):
        """Generate .mcp.json with the flowspec-security MCP server for Python projects."""
        from flowspec_cli import generate_mcp_json

        # Create a Python project marker
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")

        monkeypatch.chdir(tmp_path)
        result = generate_mcp_json(tmp_path)

        # Should return True when file is created
        assert result is True

        mcp_json = tmp_path / ".mcp.json"
        config = json.loads(mcp_json.read_text())

        assert "flowspec-security" in config["mcpServers"]
        assert config["mcpServers"]["flowspec-security"]["command"] == "uv"

    def test_generate_mcp_json_skips_existing(self, tmp_path, monkeypatch):
        """Skip .mcp.json generation if file already exists."""
        from flowspec_cli import generate_mcp_json

        # Create existing .mcp.json
        existing_config = {"mcpServers": {"custom": {"command": "custom"}}}
        mcp_json = tmp_path / ".mcp.json"
        mcp_json.write_text(json.dumps(existing_config))

        monkeypatch.chdir(tmp_path)
        result = generate_mcp_json(tmp_path)

        # Should return False when file already exists
        assert result is False

        # Should not be modified
        config = json.loads(mcp_json.read_text())
        assert "custom" in config["mcpServers"]
        assert "backlog" not in config["mcpServers"]


class TestUpdateMCPJson:
    """Test the update_mcp_json functionality for upgrade-repo."""

    def test_update_mcp_json_creates_new_file(self, tmp_path, monkeypatch):
        """Create .mcp.json with required servers when file doesn't exist."""
        from flowspec_cli import update_mcp_json

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path)

        # Should return True when file is created
        assert modified is True

        # Check that required servers were added
        assert "backlog" in changes["added"]
        assert "github" in changes["added"]
        assert "serena" in changes["added"]

        # Verify file content
        mcp_json = tmp_path / ".mcp.json"
        assert mcp_json.exists()
        config = json.loads(mcp_json.read_text())
        assert "backlog" in config["mcpServers"]
        assert "github" in config["mcpServers"]
        assert "serena" in config["mcpServers"]

    def test_update_mcp_json_merges_with_existing(self, tmp_path, monkeypatch):
        """Merge required servers with existing .mcp.json, preserving custom config."""
        from flowspec_cli import update_mcp_json

        # Create existing .mcp.json with custom server
        existing_config = {
            "mcpServers": {
                "custom-server": {"command": "my-custom-command", "args": ["--flag"]},
                "backlog": {"command": "old-backlog", "args": []},  # Existing backlog
            }
        }
        mcp_json = tmp_path / ".mcp.json"
        mcp_json.write_text(json.dumps(existing_config))

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path)

        # Should return True when new servers are added
        assert modified is True

        # Only github and serena should be added (backlog already exists)
        assert "github" in changes["added"]
        assert "serena" in changes["added"]
        assert "backlog" in changes["unchanged"]

        # Verify custom server is preserved
        config = json.loads(mcp_json.read_text())
        assert "custom-server" in config["mcpServers"]
        assert config["mcpServers"]["custom-server"]["command"] == "my-custom-command"

        # Existing backlog config should NOT be overwritten
        assert config["mcpServers"]["backlog"]["command"] == "old-backlog"

    def test_update_mcp_json_no_changes_when_complete(self, tmp_path, monkeypatch):
        """Return False when all required servers already exist."""
        from flowspec_cli import update_mcp_json, REQUIRED_MCP_SERVERS

        # Create .mcp.json with all required servers
        existing_config = {"mcpServers": dict(REQUIRED_MCP_SERVERS)}
        mcp_json = tmp_path / ".mcp.json"
        mcp_json.write_text(json.dumps(existing_config))

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path)

        # Should return False when no changes needed
        assert modified is False
        assert len(changes["added"]) == 0
        assert "backlog" in changes["unchanged"]
        assert "github" in changes["unchanged"]
        assert "serena" in changes["unchanged"]

    def test_update_mcp_json_includes_recommended_servers(self, tmp_path, monkeypatch):
        """Include recommended servers when flag is set."""
        from flowspec_cli import update_mcp_json

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path, include_recommended=True)

        assert modified is True

        # Check recommended servers were added
        assert "playwright-test" in changes["added"]
        assert "trivy" in changes["added"]
        assert "semgrep" in changes["added"]

        # Verify file content
        mcp_json = tmp_path / ".mcp.json"
        config = json.loads(mcp_json.read_text())
        assert "playwright-test" in config["mcpServers"]
        assert "trivy" in config["mcpServers"]
        assert "semgrep" in config["mcpServers"]

    def test_update_mcp_json_adds_python_server(self, tmp_path, monkeypatch):
        """Add flowspec-security server for Python projects."""
        from flowspec_cli import update_mcp_json

        # Create a Python project marker
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path)

        assert modified is True
        assert "flowspec-security" in changes["added"]

        # Verify file content
        mcp_json = tmp_path / ".mcp.json"
        config = json.loads(mcp_json.read_text())
        assert "flowspec-security" in config["mcpServers"]
        assert config["mcpServers"]["flowspec-security"]["command"] == "uv"

    def test_update_mcp_json_handles_corrupted_file(self, tmp_path, monkeypatch):
        """Handle corrupted .mcp.json gracefully by starting fresh."""
        from flowspec_cli import update_mcp_json

        # Create corrupted .mcp.json
        mcp_json = tmp_path / ".mcp.json"
        mcp_json.write_text("{ invalid json }")

        monkeypatch.chdir(tmp_path)
        modified, changes = update_mcp_json(tmp_path)

        # Should create valid config despite corrupted input
        assert modified is True
        assert "backlog" in changes["added"]

        # Verify valid JSON was written
        config = json.loads(mcp_json.read_text())
        assert "mcpServers" in config


class TestVSCodeExtensionsGeneration:
    """Test the VSCode extensions.json generation functionality."""

    def test_generate_vscode_extensions_basic(self, tmp_path, monkeypatch):
        """Generate basic extensions.json with base extensions."""
        from flowspec_cli import generate_vscode_extensions

        monkeypatch.chdir(tmp_path)
        result = generate_vscode_extensions(tmp_path)

        # Should return True when file is created
        assert result is True

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        assert extensions_json.exists()

        config = json.loads(extensions_json.read_text())
        assert "recommendations" in config
        assert "github.copilot" in config["recommendations"]
        assert "github.copilot-chat" in config["recommendations"]

    def test_generate_vscode_extensions_python(self, tmp_path, monkeypatch):
        """Generate extensions.json with Python extensions for Python projects."""
        from flowspec_cli import generate_vscode_extensions

        # Create a Python project marker
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'test'\n")

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "ms-python.python" in config["recommendations"]
        assert "ms-python.vscode-pylance" in config["recommendations"]
        assert "charliermarsh.ruff" in config["recommendations"]

    def test_generate_vscode_extensions_javascript(self, tmp_path, monkeypatch):
        """Generate extensions.json with JS/TS extensions for JS projects."""
        from flowspec_cli import generate_vscode_extensions

        # Create a JS project marker
        (tmp_path / "package.json").write_text('{"name": "test"}\n')

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "dbaeumer.vscode-eslint" in config["recommendations"]
        assert "esbenp.prettier-vscode" in config["recommendations"]

    def test_generate_vscode_extensions_docker(self, tmp_path, monkeypatch):
        """Generate extensions.json with Docker extension when Dockerfile exists."""
        from flowspec_cli import generate_vscode_extensions

        # Create a Dockerfile
        (tmp_path / "Dockerfile").write_text("FROM python:3.11\n")

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "ms-azuretools.vscode-docker" in config["recommendations"]

    def test_generate_vscode_extensions_merges_existing(self, tmp_path, monkeypatch):
        """Merge with existing extensions.json recommendations."""
        from flowspec_cli import generate_vscode_extensions

        # Create existing extensions.json with custom extension
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        existing_config = {"recommendations": ["custom.extension"]}
        (vscode_dir / "extensions.json").write_text(json.dumps(existing_config))

        monkeypatch.chdir(tmp_path)
        result = generate_vscode_extensions(tmp_path)

        # Should return False when file already exists (was updated, not created)
        assert result is False

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        # Should have both custom and base extensions
        assert "custom.extension" in config["recommendations"]
        assert "github.copilot" in config["recommendations"]

    def test_generate_vscode_extensions_go(self, tmp_path, monkeypatch):
        """Generate extensions.json with Go extension for Go projects."""
        from flowspec_cli import generate_vscode_extensions

        # Create a Go project marker
        (tmp_path / "go.mod").write_text("module test\n")

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "golang.go" in config["recommendations"]

    def test_generate_vscode_extensions_rust(self, tmp_path, monkeypatch):
        """Generate extensions.json with Rust extension for Rust projects."""
        from flowspec_cli import generate_vscode_extensions

        # Create a Rust project marker
        (tmp_path / "Cargo.toml").write_text('[package]\nname = "test"\n')

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "rust-lang.rust-analyzer" in config["recommendations"]

    def test_generate_vscode_extensions_java(self, tmp_path, monkeypatch):
        """Generate extensions.json with Java extensions for Java projects."""
        from flowspec_cli import generate_vscode_extensions

        # Create a Java project marker (Maven)
        (tmp_path / "pom.xml").write_text(
            '<?xml version="1.0"?>\n<project></project>\n'
        )

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "redhat.java" in config["recommendations"]
        assert "vscjava.vscode-java-pack" in config["recommendations"]

    def test_generate_vscode_extensions_docker_compose_yaml(
        self, tmp_path, monkeypatch
    ):
        """Generate extensions.json with Docker extension when docker-compose.yaml exists."""
        from flowspec_cli import generate_vscode_extensions

        # Create a docker-compose.yaml file (not .yml)
        (tmp_path / "docker-compose.yaml").write_text("version: '3'\n")

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "ms-azuretools.vscode-docker" in config["recommendations"]

    def test_generate_vscode_extensions_docker_compose_yml(self, tmp_path, monkeypatch):
        """Generate extensions.json with Docker extension when docker-compose.yml exists."""
        from flowspec_cli import generate_vscode_extensions

        # Create a docker-compose.yml file (the common .yml variant)
        (tmp_path / "docker-compose.yml").write_text("version: '3'\n")

        monkeypatch.chdir(tmp_path)
        generate_vscode_extensions(tmp_path)

        extensions_json = tmp_path / ".vscode" / "extensions.json"
        config = json.loads(extensions_json.read_text())

        assert "ms-azuretools.vscode-docker" in config["recommendations"]


class TestCopilotAgentNamingConvention:
    """Test VSCode Copilot agent naming convention (ADR-001).

    Verifies agents use dot-notation filenames (flow.specify.agent.md)
    and PascalCase name fields (FlowSpecify) per ADR-001.
    """

    def test_copilot_agent_templates_use_dot_notation_filenames(self):
        """Verify COPILOT_AGENT_TEMPLATES keys use dot notation (not hyphens).

        Note: 'submit-n-watch-pr' is an exception - the command name itself
        contains hyphens (it's "submit-n-watch" not "submitnwatch").
        """
        from flowspec_cli import COPILOT_AGENT_TEMPLATES

        for filename in COPILOT_AGENT_TEMPLATES.keys():
            # Should follow pattern: flow.{command}.agent.md
            assert filename.endswith(".agent.md"), (
                f"Agent template filename '{filename}' should end with .agent.md"
            )
            assert filename.startswith("flow."), (
                f"Agent template filename '{filename}' should start with 'flow.'"
            )

            # Extract the command part: flow.{command}.agent.md -> {command}
            command_part = filename.replace("flow.", "").replace(".agent.md", "")

            # Filenames should use dot notation for word separation
            # The exception is 'submit-n-watch-pr' where hyphens are part of the command name
            if "submit-n-watch" not in command_part:
                assert "-" not in command_part, (
                    f"Agent template filename '{filename}' uses hyphen notation. "
                    f"Per ADR-001, should use dot notation (e.g., flow.specify.agent.md)"
                )

    def test_copilot_agent_templates_use_pascalcase_names(self):
        """Verify agent templates use PascalCase name fields (not quoted strings)."""
        from flowspec_cli import COPILOT_AGENT_TEMPLATES
        import re

        for filename, content in COPILOT_AGENT_TEMPLATES.items():
            # Extract the name field from YAML frontmatter
            name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
            assert name_match, f"Agent template '{filename}' missing name field"

            name_value = name_match.group(1).strip()

            # Name should be PascalCase without quotes: FlowSpecify
            # NOT quoted string: "flow-specify"
            assert not name_value.startswith('"'), (
                f"Agent '{filename}' name '{name_value}' should not be quoted. "
                f"Per ADR-001, use PascalCase without quotes (e.g., FlowSpecify)"
            )
            assert name_value[0].isupper(), (
                f"Agent '{filename}' name '{name_value}' should be PascalCase "
                f"(start with uppercase). Per ADR-001, use FlowSpecify not flow-specify"
            )
            assert "-" not in name_value, (
                f"Agent '{filename}' name '{name_value}' uses hyphens. "
                f"Per ADR-001, use PascalCase (e.g., FlowSpecify not flow-specify)"
            )

    def test_copilot_agent_handoffs_use_dot_notation(self):
        """Verify agent handoffs reference other agents using dot notation.

        Note: 'submit-n-watch-pr' is an exception - the command name itself
        contains hyphens (it's "submit-n-watch" not "submitnwatch").
        """
        from flowspec_cli import COPILOT_AGENT_TEMPLATES
        import re

        for filename, content in COPILOT_AGENT_TEMPLATES.items():
            # Find all handoff agent references
            handoff_matches = re.findall(r'agent:\s*"([^"]+)"', content)

            for agent_ref in handoff_matches:
                # Extract the command part after "flow."
                if agent_ref.startswith("flow."):
                    command_part = agent_ref.replace("flow.", "")
                else:
                    command_part = agent_ref

                # Handoff references should use dot notation: flow.plan
                # The exception is 'submit-n-watch-pr' where hyphens are part of the name
                if "submit-n-watch" not in command_part:
                    assert "-" not in command_part, (
                        f"Agent '{filename}' has handoff to '{agent_ref}' using hyphen. "
                        f'Per ADR-001, use dot notation (e.g., agent: "flow.plan")'
                    )

    def test_init_creates_agents_with_dot_notation_filenames(
        self, tmp_path, monkeypatch
    ):
        """Verify flowspec init creates agent files with dot-notation filenames."""
        from typer.testing import CliRunner
        from flowspec_cli import app

        runner = CliRunner()
        monkeypatch.chdir(tmp_path)

        # Run flowspec init with required flags
        result = runner.invoke(
            app,
            [
                "init",
                str(tmp_path / "test-project"),
                "--ai",
                "claude",
                "--ignore-agent-tools",
                "--constitution",
                "light",
            ],
            input="n\n",  # Answer 'no' to backlog-md install prompt
        )

        # Check init succeeded
        assert result.exit_code == 0, f"Init failed: {result.stdout}"

        # Verify .github/agents/ directory exists
        agents_dir = tmp_path / "test-project" / ".github" / "agents"
        assert agents_dir.exists(), "Agents directory was not created"

        # List all agent files
        agent_files = list(agents_dir.glob("*.agent.md"))
        assert len(agent_files) > 0, "No agent files were created"

        # Verify all agent filenames use dot notation (not hyphens)
        for agent_file in agent_files:
            filename = agent_file.name
            # Remove the .agent.md suffix to check the command part
            command_part = filename.replace(".agent.md", "")

            # Should NOT have hyphens in the command part (except submit-n-watch)
            # flow.specify.agent.md is correct
            # flow-specify.agent.md is wrong
            if "submit-n-watch" not in filename:
                assert "-" not in command_part, (
                    f"Agent file '{filename}' uses hyphen notation. "
                    f"Per ADR-001, should use dot notation (e.g., flow.specify.agent.md)"
                )

    def test_init_agents_have_correct_name_fields(self, tmp_path, monkeypatch):
        """Verify created agent files have PascalCase name fields."""
        from typer.testing import CliRunner
        from flowspec_cli import app
        import re

        runner = CliRunner()
        monkeypatch.chdir(tmp_path)

        # Run flowspec init with required flags
        result = runner.invoke(
            app,
            [
                "init",
                str(tmp_path / "test-project"),
                "--ai",
                "claude",
                "--ignore-agent-tools",
                "--constitution",
                "light",
            ],
            input="n\n",  # Answer 'no' to backlog-md install prompt
        )

        assert result.exit_code == 0, f"Init failed: {result.stdout}"

        agents_dir = tmp_path / "test-project" / ".github" / "agents"
        agent_files = list(agents_dir.glob("*.agent.md"))

        for agent_file in agent_files:
            content = agent_file.read_text()
            name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)

            assert name_match, f"Agent '{agent_file.name}' missing name field"
            name_value = name_match.group(1).strip()

            # Verify PascalCase (no quotes, no hyphens, starts uppercase)
            assert not name_value.startswith('"'), (
                f"Agent '{agent_file.name}' name should not be quoted"
            )
            assert name_value[0].isupper(), (
                f"Agent '{agent_file.name}' name should start with uppercase"
            )
