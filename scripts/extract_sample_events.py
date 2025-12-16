#!/usr/bin/env python3
"""Extract sample events from specification to test fixture.

Parses build-docs/jsonl-event-system.md and extracts all JSON examples
into tests/fixtures/sample_events_v1_1.jsonl for automated testing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def is_valid_event(event_dict: dict) -> bool:
    """Check if JSON object is a valid event (has required fields).

    Args:
        event_dict: Parsed JSON dictionary.

    Returns:
        True if has required event fields, False otherwise.
    """
    required_fields = {"version", "event_type", "timestamp", "agent_id"}
    return required_fields.issubset(event_dict.keys())


def extract_json_examples(md_file: Path) -> list[str]:
    """Extract JSON examples from markdown code blocks.

    Args:
        md_file: Path to markdown file containing JSON examples.

    Returns:
        List of JSON string examples (one per event).
    """
    content = md_file.read_text()

    # Find all ```json or ```jsonl code blocks
    pattern = r"```json(?:l)?\s*\n(.*?)\n```"
    matches = re.findall(pattern, content, re.DOTALL)

    events = []
    for match in matches:
        # Each match might be a single event or multiple lines
        for line in match.strip().split("\n"):
            line = line.strip()
            if line and line.startswith("{"):
                # Validate it's valid JSON and has required event fields
                try:
                    event_dict = json.loads(line)
                    if is_valid_event(event_dict):
                        events.append(line)
                except json.JSONDecodeError:
                    # Skip malformed JSON
                    pass

    return events


def main() -> None:
    """Main entry point."""
    spec_file = Path("build-docs/jsonl-event-system.md")
    output_file = Path("tests/fixtures/sample_events_v1_1.jsonl")

    if not spec_file.exists():
        print(f"Error: Spec file not found: {spec_file}", file=sys.stderr)
        sys.exit(1)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    events = extract_json_examples(spec_file)

    with output_file.open("w") as f:
        for event in events:
            f.write(event + "\n")

    print(f"Extracted {len(events)} sample events to {output_file}")


if __name__ == "__main__":
    main()
