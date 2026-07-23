# History — Decision and Reference Logging

## Decision Log Format
Log non-trivial decisions to `.logs/decisions/<topic>.jsonl`:

```json
{
  "timestamp": "2026-05-23T10:00:00Z",
  "task": "TASK-606",
  "phase": "implementation",
  "decision": "Use dataclass CheckResult instead of TypedDict",
  "rationale": "dataclass gives free __repr__ and supports default values; CheckResult is instantiated 8x per run",
  "actor": "@claude",
  "alternatives_considered": ["TypedDict", "NamedTuple"],
  "references": [".claude/plans/task-606-flowspec-doctor.md"]
}
```

## When to Log
- Architecture choices (why a submodule over inline code)
- Trade-offs with meaningful alternatives (why not X)
- Rejected approaches and the reason
- Discovered constraints that changed the plan

## When NOT to Log
- Obvious implementation steps
- Minor style choices covered by ruff
- Things that are self-evident from the code

## Task Notes vs Decision Log
- **backlog task notes** (`backlog task edit <id> --append-notes`) — PR-ready summary, what was built
- **decision log** (`.logs/decisions/`) — architectural/trade-off reasoning for future agents
