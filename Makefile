# JP Spec Kit - Makefile
# Development and maintenance commands

.PHONY: help install test lint format clean dogfood-validate dogfood-fix dogfood-status

# Default target
help:
	@echo "JP Spec Kit - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Development:"
	@echo "  make install          - Install dependencies with uv"
	@echo "  make test             - Run all tests"
	@echo "  make lint             - Run linter (ruff check)"
	@echo "  make format           - Format code (ruff format)"
	@echo "  make clean            - Clean build artifacts"
	@echo ""
	@echo "Dogfood Management:"
	@echo "  make dogfood-validate - Validate dogfood setup"
	@echo "  make dogfood-fix      - Fix dogfood setup (recreate symlinks)"
	@echo "  make dogfood-status   - Show dogfood status"
	@echo ""
	@echo "CLI:"
	@echo "  make cli-install      - Install CLI locally"
	@echo "  make cli-uninstall    - Uninstall CLI"
	@echo ""

# ============================================================
# DEVELOPMENT COMMANDS
# ============================================================

install:
	@echo "Installing dependencies..."
	uv sync

test:
	@echo "Running tests..."
	uv run pytest tests/ -v

test-dogfood:
	@echo "Running dogfood-specific tests..."
	uv run pytest tests/test_dogfood_*.py -v

lint:
	@echo "Running linter..."
	uv run ruff check .

format:
	@echo "Formatting code..."
	uv run ruff format .

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned"

# ============================================================
# DOGFOOD MANAGEMENT
# ============================================================

dogfood-validate:
	@echo "Validating dogfood setup..."
	@./scripts/bash/pre-commit-dogfood.sh
	@echo ""
	@echo "Running dogfood tests..."
	@uv run pytest tests/test_dogfood_validation.py tests/test_dogfood_init_equivalence.py -v

dogfood-fix:
	@echo "Fixing dogfood setup..."
	@echo ""
	@echo "Step 1: Backing up current state..."
	@if [ -d .claude/commands/jpspec ]; then \
		echo "  - Found jpspec directory"; \
	fi
	@if [ -d .claude/commands/speckit ]; then \
		echo "  - Found speckit directory"; \
	fi
	@echo ""
	@echo "Step 2: Removing existing symlinks..."
	@rm -rf .claude/commands/jpspec .claude/commands/speckit 2>/dev/null || true
	@echo "  ✓ Removed"
	@echo ""
	@echo "Step 3: Recreating symlinks with dogfood command..."
	@uv run specify dogfood --force
	@echo ""
	@echo "Step 4: Validating new setup..."
	@./scripts/bash/pre-commit-dogfood.sh
	@echo ""
	@echo "=========================================="
	@echo "✓ Dogfood setup restored successfully"
	@echo "=========================================="

dogfood-status:
	@echo "=========================================="
	@echo "Dogfood Status"
	@echo "=========================================="
	@echo ""
	@echo "=== .claude/commands/ structure ==="
	@ls -la .claude/commands/ 2>/dev/null || echo "Directory does not exist"
	@echo ""
	@if [ -d .claude/commands/speckit ]; then \
		echo "=== speckit commands ==="; \
		ls -la .claude/commands/speckit/ | grep -E '\.md$$' || echo "No .md files"; \
		echo ""; \
	fi
	@if [ -d .claude/commands/jpspec ]; then \
		echo "=== jpspec commands ==="; \
		ls -la .claude/commands/jpspec/ | grep -E '\.md$$' || echo "No .md files"; \
		echo ""; \
	fi
	@echo "=== Symlink verification ==="
	@TOTAL=$$(find .claude/commands -name "*.md" 2>/dev/null | wc -l); \
	SYMLINKS=$$(find .claude/commands -name "*.md" -type l 2>/dev/null | wc -l); \
	FILES=$$(find .claude/commands -name "*.md" -type f 2>/dev/null | wc -l); \
	echo "Total .md files: $$TOTAL"; \
	echo "Symlinks: $$SYMLINKS"; \
	echo "Regular files: $$FILES"; \
	if [ $$FILES -gt 0 ]; then \
		echo ""; \
		echo "❌ WARNING: Found regular files (should be symlinks):"; \
		find .claude/commands -name "*.md" -type f; \
	fi
	@echo ""

# ============================================================
# CLI COMMANDS
# ============================================================

cli-install:
	@echo "Installing CLI..."
	uv tool install . --force
	@echo "✓ CLI installed"
	@echo ""
	@echo "Verify with: specify --version"

cli-uninstall:
	@echo "Uninstalling CLI..."
	uv tool uninstall specify-cli || true
	@echo "✓ CLI uninstalled"

# ============================================================
# CI/CD SIMULATION
# ============================================================

ci-local:
	@echo "Running local CI simulation..."
	@echo ""
	@echo "Step 1: Linting..."
	@make lint
	@echo ""
	@echo "Step 2: Testing..."
	@make test
	@echo ""
	@echo "Step 3: Dogfood validation..."
	@make dogfood-validate
	@echo ""
	@echo "=========================================="
	@echo "✓ Local CI simulation passed"
	@echo "=========================================="
