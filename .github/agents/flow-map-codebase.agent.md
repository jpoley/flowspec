---
name: "flow-map-codebase"
description: "Generate bounded directory tree listings and feature maps for codebase areas."
target: "chat"
tools:
  - "Read"
  - "Write"
  - "Edit"
  - "Grep"
  - "Glob"
  - "Bash"
  - "mcp__backlog__*"
  - "mcp__serena__*"
  - "Skill"

handoffs:
  - label: "Generate PRP"
    agent: "flow-generate-prp"
    prompt: "The codebase map is ready. Generate a complete PRP using this map."
    send: false
---
## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command generates bounded directory tree listings for relevant parts of the codebase. It creates readable maps that support PRP generation and feature context.

### Argument Parsing

Parse the user input for paths and flags:

```bash
# Expected formats:
# /flow:map-codebase src/commands           # Single path
# /flow:map-codebase src/ tests/            # Multiple paths
# /flow:map-codebase src/ --depth 3         # With depth flag
# /flow:map-codebase src/ --output docs/feature-maps/task-123.md
# /flow:map-codebase src/ --prp task-123    # Update PRP file

PATHS=""
DEPTH=3
OUTPUT=""
PRP_TASK=""

# Parse arguments
for arg in $ARGUMENTS; do
  case "$arg" in
    --depth)
      # Next arg is depth value
      ;;
    --output)
      # Next arg is output path
      ;;
    --prp)
      # Next arg is task ID
      ;;
    *)
      # Treat as path if doesn't start with --
      if [[ ! "$arg" =~ ^-- ]]; then
        PATHS="$PATHS $arg"
      fi
      ;;
  esac
done
```

### Default Values

If no arguments provided, show usage:

```
Usage: /flow:map-codebase <paths...> [options]

Options:
  --depth <n>     Maximum directory depth (default: 3)
  --output <path> Write to specific file
  --prp <task-id> Update CODEBASE SNAPSHOT in docs/prp/<task-id>.md

Examples:
  /flow:map-codebase src/
  /flow:map-codebase src/ tests/ --depth 4
  /flow:map-codebase src/commands --prp task-123
  /flow:map-codebase src/ --output docs/feature-maps/auth.md
```

### Step 1: Validate Paths

Verify all specified paths exist:

```bash
for path in $PATHS; do
  if [ ! -e "$path" ]; then
    echo "ERROR: Path not found: $path"
    exit 1
  fi
done

echo "Mapping paths: $PATHS"
echo "Depth: $DEPTH"
```

### Step 2: Generate Directory Tree

Generate a bounded directory tree for each path, excluding common non-essential directories:

```bash
# Exclusion patterns
EXCLUDES="--exclude node_modules --exclude __pycache__ --exclude .git --exclude .venv --exclude venv --exclude .mypy_cache --exclude .pytest_cache --exclude .ruff_cache --exclude dist --exclude build --exclude *.egg-info --exclude .tox --exclude coverage --exclude .coverage --exclude htmlcov"

# Generate tree for each path
for path in $PATHS; do
  echo ""
  echo "## $path"
  echo ""

  # Use tree if available, otherwise fall back to find
  if command -v tree &> /dev/null; then
    tree -L $DEPTH $EXCLUDES --dirsfirst -I '__pycache__|node_modules|.git|.venv|venv|*.egg-info|.mypy_cache|.pytest_cache|.ruff_cache|dist|build|.tox|coverage|.coverage|htmlcov' "$path"
  else
    # Fallback to find with depth limit
    find "$path" -maxdepth $DEPTH -type f \
      -not -path "*/__pycache__/*" \
      -not -path "*/node_modules/*" \
      -not -path "*/.git/*" \
      -not -path "*/.venv/*" \
      -not -path "*/venv/*" \
      -not -path "*/.mypy_cache/*" \
      -not -path "*/.pytest_cache/*" \
      -not -name "*.pyc" \
      | sort
  fi
done
```

### Step 3: Identify Key Entry Points

For each path, identify key files that serve as entry points:

```bash
echo ""
echo "### Key Entry Points"
echo ""
echo "| Entry Point | Location | Purpose |"
echo "|-------------|----------|---------|"

# Look for common entry point patterns
for path in $PATHS; do
  # Python entry points
  find "$path" -maxdepth 3 -name "__main__.py" -o -name "main.py" -o -name "cli.py" -o -name "app.py" 2>/dev/null | while read f; do
    echo "| $(basename $f) | $f | Application entry |"
  done

  # Config files
  find "$path" -maxdepth 2 -name "pyproject.toml" -o -name "setup.py" -o -name "package.json" 2>/dev/null | while read f; do
    echo "| $(basename $f) | $f | Project config |"
  done
done
```

### Step 4: Identify Integration Points

Look for files that handle integrations (APIs, databases, external services):

```bash
echo ""
echo "### Integration Points"
echo ""
echo "| Integration | File | Function/Method | Notes |"
echo "|-------------|------|-----------------|-------|"

for path in $PATHS; do
  # API endpoints
  grep -rl "@app\.\(get\|post\|put\|delete\)" "$path" 2>/dev/null | head -5 | while read f; do
    echo "| REST API | $f | endpoint handlers | HTTP routes |"
  done

  # Database models
  grep -rl "class.*Model\|Base\)" "$path" 2>/dev/null | head -5 | while read f; do
    echo "| Database | $f | ORM models | Data layer |"
  done
done
```

### Step 5: Generate File Type Summary

Summarize the types of files found:

```bash
echo ""
echo "### File Type Summary"
echo ""

for path in $PATHS; do
  echo "**$path**:"
  find "$path" -type f \
    -not -path "*/__pycache__/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10 | while read count ext; do
    echo "- .$ext: $count files"
  done
done
```

### Step 6: Output Results

Based on flags, either:

1. **Print to stdout** (default):
   ```
   [tree output displayed in terminal]
   ```

2. **Write to file** (`--output`):
   ```bash
   # Write full output to specified file
   echo "Codebase map written to: $OUTPUT"
   ```

3. **Update PRP** (`--prp`):
   ```bash
   # Find the PRP file
   PRP_FILE="docs/prp/$PRP_TASK.md"

   if [ ! -f "$PRP_FILE" ]; then
     echo "ERROR: PRP not found at $PRP_FILE"
     echo "Run /flow:generate-prp $PRP_TASK first"
     exit 1
   fi

   # Replace CODEBASE SNAPSHOT section
   # (implementation details for section replacement)

   echo "Updated CODEBASE SNAPSHOT in: $PRP_FILE"
   ```

### Example Output

```
## src/specify_cli/

src/specify_cli/
├── __init__.py
├── cli.py
├── commands/
│   ├── __init__.py
│   ├── init.py
│   ├── dev_setup.py
│   └── workflow.py
├── models/
│   ├── __init__.py
│   └── config.py
└── utils/
    ├── __init__.py
    └── files.py

### Key Entry Points

| Entry Point | Location | Purpose |
|-------------|----------|---------|
| cli.py | src/specify_cli/cli.py | Application entry |
| pyproject.toml | pyproject.toml | Project config |

### Integration Points

| Integration | File | Function/Method | Notes |
|-------------|------|-----------------|-------|
| CLI | src/specify_cli/cli.py | click commands | User interface |

### File Type Summary

**src/specify_cli/**:
- .py: 15 files
- .md: 2 files
```

## Deliverables

This command produces:
1. **Directory Tree**: Bounded, filtered view of specified paths
2. **Entry Points Table**: Key files that serve as entry points
3. **Integration Points Table**: Files handling external integrations
4. **File Summary**: Count of file types

## Use Cases

- **PRP Generation**: Feed into `/flow:generate-prp` for context
- **Code Review**: Understand scope of changes
- **Onboarding**: Help new developers navigate codebase
- **Documentation**: Generate architecture overviews
