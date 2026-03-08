# Flowspec Redesign - Open Questions

**Date:** 2026-03-08
**Context:** Clean-slate design for a spec-driven AI SDLC inner loop

---

## Architecture Questions

1. **How thin is the spec?** GSD does full PROJECT.md + REQUIREMENTS.md + CONTEXT.md. Is our spec just "what and why" in one file, or does it need structure (acceptance criteria, constraints, non-goals)?

2. **Plan: always or optional?** For a 2-line bug fix, `/spec → /build` should be enough. Does the plan step only activate above a complexity threshold, or is it always there but lightweight?

3. **Where does the spec live?** `.specs/{feature}/` in the repo? Backlog tasks? Both? The artifact needs a home.

4. **How does this relate to backlog.md?** Is a backlog task the "intent" that feeds into `/spec`? Or is backlog a separate tracking layer?

## Composability Questions

5. **Plugin boundary:** Security scanning, PR lifecycle, deployment - are these skills that ship with core, or are they separate tools you compose in?

6. **What's the minimum viable version?** If you could only ship two of the four tools first, which two?

7. **How do external tools plug in?** If this is "a series of tools that assemble," what's the interface contract? Artifacts on disk? CLI pipes? MCP?

## Closed-Loop Questions

8. **What counts as validation?** Tests passing? Lint clean? Coverage threshold? Or is it project-defined?

9. **Escalation policy:** When the closed loop fails N times, what happens? Block? Human prompt? Skip with warning?

10. **Validation for non-code artifacts:** Specs and plans are artifacts too. Do they get validated? By what? (e.g., plan completeness check, spec has acceptance criteria)

## Agent Team Questions

11. **Four roles enough?** Planner, Builder, Validator, Reviewer. Or is even that too many? Could Builder+Validator be one role since validation is always part of building?

12. **Fresh context per task or per feature?** GSD spawns fresh context per atomic task. Is that the right granularity, or is per-feature enough?

13. **Who owns the loop?** The orchestrating command? A dedicated agent? The human?

## Identity Questions

14. **Is flowspec a tool, a protocol, or a methodology?** Tool = CLI you install. Protocol = artifact format + phase contract that any tool can implement. Methodology = a way of working that could be manual.

15. **What does flowspec do that Claude Code alone doesn't?** The answer should be one sentence. If it takes a paragraph, the scope is wrong.
