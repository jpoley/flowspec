#!/usr/bin/env bash
# Rename specflow to flowspec across the codebase
# This script is intentionally excluded from content replacements

set -euo pipefail

SCRIPT_NAME="rename-specflow-to-flowspec.sh"
DRY_RUN="${1:-}"

log() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

error() {
    echo "[ERROR] $1" >&2
}

# Phase 1: Rename directories
rename_directories() {
    log "=== Phase 1: Renaming directories ==="

    # Templates commands directory
    if [[ -d "templates/commands/specflow" ]]; then
        if [[ "$DRY_RUN" == "--dry-run" ]]; then
            log "[DRY-RUN] Would rename: templates/commands/specflow -> templates/commands/flow"
        else
            git mv templates/commands/specflow templates/commands/flow
            log "Renamed: templates/commands/specflow -> templates/commands/flow"
        fi
    fi

    # .github/agents files
    for f in .github/agents/specflow-*.agent.md; do
        if [[ -f "$f" ]]; then
            newname="${f//specflow-/flowspec-}"
            if [[ "$DRY_RUN" == "--dry-run" ]]; then
                log "[DRY-RUN] Would rename: $f -> $newname"
            else
                git mv "$f" "$newname"
                log "Renamed: $f -> $newname"
            fi
        fi
    done

    # Test files
    for f in tests/test_specflow_*.py; do
        if [[ -f "$f" ]]; then
            newname="${f//test_specflow_/test_flowspec_}"
            if [[ "$DRY_RUN" == "--dry-run" ]]; then
                log "[DRY-RUN] Would rename: $f -> $newname"
            else
                git mv "$f" "$newname"
                log "Renamed: $f -> $newname"
            fi
        fi
    done

    # Root config files
    if [[ -f "specflow_workflow.yml" ]]; then
        if [[ "$DRY_RUN" == "--dry-run" ]]; then
            log "[DRY-RUN] Would rename: specflow_workflow.yml -> flowspec_workflow.yml"
        else
            git mv specflow_workflow.yml flowspec_workflow.yml
            log "Renamed: specflow_workflow.yml -> flowspec_workflow.yml"
        fi
    fi

    # Schema files
    if [[ -f "schemas/specflow_workflow.schema.json" ]]; then
        if [[ "$DRY_RUN" == "--dry-run" ]]; then
            log "[DRY-RUN] Would rename: schemas/specflow_workflow.schema.json -> schemas/flowspec_workflow.schema.json"
        else
            git mv schemas/specflow_workflow.schema.json schemas/flowspec_workflow.schema.json
            log "Renamed: schemas/specflow_workflow.schema.json -> schemas/flowspec_workflow.schema.json"
        fi
    fi

    # Memory schema files
    if [[ -f "memory/specflow_workflow.schema.json" ]]; then
        if [[ "$DRY_RUN" == "--dry-run" ]]; then
            log "[DRY-RUN] Would rename: memory/specflow_workflow.schema.json -> memory/flowspec_workflow.schema.json"
        else
            git mv memory/specflow_workflow.schema.json memory/flowspec_workflow.schema.json
            log "Renamed: memory/specflow_workflow.schema.json -> memory/flowspec_workflow.schema.json"
        fi
    fi

    if [[ -f "memory/specflow_workflow.yml" ]]; then
        if [[ "$DRY_RUN" == "--dry-run" ]]; then
            log "[DRY-RUN] Would rename: memory/specflow_workflow.yml -> memory/flowspec_workflow.yml"
        else
            git mv memory/specflow_workflow.yml memory/flowspec_workflow.yml
            log "Renamed: memory/specflow_workflow.yml -> memory/flowspec_workflow.yml"
        fi
    fi

    # Docs files with specflow in name (rename specflow -> flowspec for files)
    for f in docs/*/specflow-*.md docs/specflow-*.md; do
        if [[ -f "$f" ]]; then
            newname="${f//specflow-/flowspec-}"
            if [[ "$DRY_RUN" == "--dry-run" ]]; then
                log "[DRY-RUN] Would rename: $f -> $newname"
            else
                git mv "$f" "$newname"
                log "Renamed: $f -> $newname"
            fi
        fi
    done

    # Excalidraw files
    for f in docs/*/specflow-*.excalidraw docs/design/specflow-*.excalidraw; do
        if [[ -f "$f" ]]; then
            newname="${f//specflow-/flowspec-}"
            if [[ "$DRY_RUN" == "--dry-run" ]]; then
                log "[DRY-RUN] Would rename: $f -> $newname"
            else
                git mv "$f" "$newname"
                log "Renamed: $f -> $newname"
            fi
        fi
    done

    # PNG files
    for f in docs/*/specflow-*.png docs/diagrams/specflow-*.png; do
        if [[ -f "$f" ]]; then
            newname="${f//specflow-/flowspec-}"
            if [[ "$DRY_RUN" == "--dry-run" ]]; then
                log "[DRY-RUN] Would rename: $f -> $newname"
            else
                git mv "$f" "$newname"
                log "Renamed: $f -> $newname"
            fi
        fi
    done
}

# Phase 2: Recreate symlinks for .claude/commands/
recreate_symlinks() {
    log "=== Phase 2: Recreating symlinks ==="

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY-RUN] Would remove .claude/commands/specflow/"
        log "[DRY-RUN] Would create .claude/commands/flow/ with updated symlinks"
        return
    fi

    # Remove old specflow symlink directory
    if [[ -d ".claude/commands/specflow" ]]; then
        rm -rf .claude/commands/specflow
        log "Removed: .claude/commands/specflow/"
    fi

    # Create new flow directory
    mkdir -p .claude/commands/flow

    # Create symlinks for all files in templates/commands/flow/
    for f in templates/commands/flow/*.md; do
        if [[ -f "$f" ]]; then
            fname=$(basename "$f")
            ln -s "../../../templates/commands/flow/$fname" ".claude/commands/flow/$fname"
            log "Created symlink: .claude/commands/flow/$fname"
        fi
    done
}

# Phase 3: Content replacements
replace_content() {
    log "=== Phase 3: Replacing content ==="

    # Exclude patterns: this script, .git, node_modules, __pycache__, .pyc files, binary files
    local exclude_patterns=(
        "--exclude-dir=.git"
        "--exclude-dir=node_modules"
        "--exclude-dir=__pycache__"
        "--exclude-dir=.venv"
        "--exclude-dir=dist"
        "--exclude-dir=build"
        "--exclude=*.pyc"
        "--exclude=*.png"
        "--exclude=*.jpg"
        "--exclude=*.jpeg"
        "--exclude=*.gif"
        "--exclude=*.ico"
        "--exclude=*.woff"
        "--exclude=*.woff2"
        "--exclude=*.ttf"
        "--exclude=*.eot"
        "--exclude=*.svg"
        "--exclude=*.excalidraw"
        "--exclude=$SCRIPT_NAME"
    )

    # Find files containing specflow (case sensitive)
    log "Finding files with 'specflow'..."

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "[DRY-RUN] Would replace content in files..."
        grep -rl "specflow" . "${exclude_patterns[@]}" 2>/dev/null | head -20 || true
        return
    fi

    # Replacement patterns (order matters!)
    # 1. /specflow: -> /flow: (command references)
    # 2. specflow_workflow -> flowspec_workflow (config file names)
    # 3. specflow- -> flowspec- (agent files, hyphenated names)
    # 4. specflow: -> flow: (remaining command-style refs)
    # 5. specflow -> flowspec (general text)
    # 6. Specflow -> Flowspec (capitalized)
    # 7. SPECFLOW -> FLOWSPEC (uppercase)

    local replacements=(
        "s|/specflow:|/flow:|g"
        "s|specflow_workflow|flowspec_workflow|g"
        "s|specflow-|flowspec-|g"
        "s|specflow:|flow:|g"
        "s|specflow|flowspec|g"
        "s|Specflow|Flowspec|g"
        "s|SPECFLOW|FLOWSPEC|g"
    )

    # Process each file
    local count=0
    while IFS= read -r file; do
        # Skip this script
        if [[ "$file" == *"$SCRIPT_NAME"* ]]; then
            continue
        fi

        # Skip binary files
        if file "$file" | grep -q "binary"; then
            continue
        fi

        # Apply all replacements
        for pattern in "${replacements[@]}"; do
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "$pattern" "$file" 2>/dev/null || true
            else
                sed -i "$pattern" "$file" 2>/dev/null || true
            fi
        done

        count=$((count + 1))
    done < <(grep -rl "specflow" . "${exclude_patterns[@]}" 2>/dev/null || true)

    log "Processed $count files"
}

# Phase 4: Verify symlinks
verify_symlinks() {
    log "=== Phase 4: Verifying symlinks ==="

    local broken=0
    local total=0

    while IFS= read -r link; do
        total=$((total + 1))
        if [[ ! -e "$link" ]]; then
            warn "Broken symlink: $link"
            broken=$((broken + 1))
        fi
    done < <(find .claude/commands -type l 2>/dev/null)

    log "Symlinks: $total total, $broken broken"

    if [[ $broken -gt 0 ]]; then
        error "Found broken symlinks!"
        return 1
    fi
}

# Main
main() {
    log "Starting specflow -> flowspec rename"

    if [[ "$DRY_RUN" == "--dry-run" ]]; then
        log "DRY RUN MODE - No changes will be made"
    fi

    rename_directories
    recreate_symlinks
    replace_content

    if [[ "$DRY_RUN" != "--dry-run" ]]; then
        verify_symlinks
    fi

    log "=== Rename complete ==="
}

main
