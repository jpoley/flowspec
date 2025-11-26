# Satellite Mode User Research Materials

**Related Task:** task-012 - Product Discovery - User Interviews

---

## 1. Interview Question Template

### Opening (2 min)
- Thanks for taking the time. We're researching how teams manage tasks across local and remote trackers.
- Everything shared is confidential and used only for product development.

### Current Workflow (10 min)

1. **What task tracking tools does your team use?**
   - [ ] GitHub Issues
   - [ ] Jira
   - [ ] Notion
   - [ ] Linear
   - [ ] Other: _______

2. **Do you use Backlog.md or similar local task files?**
   - If yes: How do you keep them in sync with remote trackers?
   - If no: Would local markdown tasks be useful? Why/why not?

3. **Walk me through your typical task workflow:**
   - Where do tasks originate?
   - How do they move between systems?
   - Who updates what?

### Pain Points (10 min)

4. **What's the most frustrating part of managing tasks across multiple systems?**
   - Probe: copy-paste fatigue, status sync, field mapping, context switching

5. **How much time do you spend weekly on manual sync between systems?**
   - [ ] < 30 min
   - [ ] 30 min - 1 hour
   - [ ] 1-2 hours
   - [ ] 2-4 hours
   - [ ] 4+ hours

6. **Have you lost work or had issues due to out-of-sync tasks?**
   - Examples?

7. **What workarounds have you tried?**
   - Scripts, integrations, manual processes?

### Feature Validation (10 min)

8. **If you could pull a remote issue (GitHub/Jira/Notion) into a local markdown file with one command, how valuable would that be?**
   - Scale 1-5 (1=not useful, 5=extremely useful)

9. **What fields are essential to sync?**
   - [ ] Title/description
   - [ ] Status
   - [ ] Assignee
   - [ ] Labels/tags
   - [ ] Due dates
   - [ ] Story points/estimates
   - [ ] Comments
   - [ ] Attachments

10. **How would you want to handle conflicts (local vs remote changes)?**
    - [ ] Local always wins
    - [ ] Remote always wins
    - [ ] Ask me each time
    - [ ] Smart merge (try to combine)

### Adoption (5 min)

11. **How likely would your team adopt a bidirectional sync tool between local markdown and remote trackers?**
    - Scale 1-10 (1=never, 10=definitely)

12. **What would prevent adoption?**
    - Security concerns, learning curve, reliability?

13. **Would you pay for this feature?**
    - [ ] No - must be free/OSS
    - [ ] Maybe - depends on price
    - [ ] Yes - if it saves time

### Close (3 min)
- Any other thoughts on local/remote task management?
- Can we follow up with a survey to your team?
- Would you beta test this feature?

---

## 2. Survey Structure (Google Forms / Typeform)

### Section A: Demographics
- Role (Developer, PM, Lead, etc.)
- Team size
- Primary task tracker used
- Years using current workflow

### Section B: Current State
- Hours/week on manual sync (slider: 0-10)
- Number of systems used (1-5+)
- Pain level with current workflow (1-5 scale)

### Section C: Feature Interest
For each capability, rate importance (1-5):
- Pull single task from remote
- Sync all assigned tasks
- Create PR with task spec injected
- Compliance/audit trail

### Section D: Adoption Likelihood
- Likelihood to try (1-10 NPS-style)
- Likelihood to recommend (1-10 NPS-style)
- Willingness to pay (categorical)

### Section E: Open Feedback
- What would make this essential for your workflow?
- Concerns or blockers?

---

## 3. Persona Templates

### Persona 1: Solo Developer
**Name:** Alex
**Role:** Full-stack developer, 1-person team
**Tools:** GitHub Issues, local notes
**Pain Points:**
- Switches between browser and editor constantly
- Loses context when moving between tools
- Wants everything in one place (IDE)

**Needs:**
- Simple pull/push commands
- Minimal configuration
- Works offline

**Quote:** "I just want my tasks where I code."

---

### Persona 2: Team Lead
**Name:** Jordan
**Role:** Engineering lead, 6-person team
**Tools:** Jira (mandated by org), prefers markdown
**Pain Points:**
- Spends 2+ hrs/week updating Jira from actual work
- Team resists Jira, uses personal notes
- Status reporting is painful

**Needs:**
- Bidirectional sync (team's local work → Jira)
- Status mapping (e.g., "In Progress" → Jira workflow)
- Bulk operations

**Quote:** "Jira is where tasks go to be forgotten. I need sync, not copy-paste."

---

### Persona 3: Compliance-Conscious PM
**Name:** Sam
**Role:** Product Manager, regulated industry
**Tools:** Jira + Confluence, audit trails required
**Pain Points:**
- Must prove work lineage (spec → task → PR → deploy)
- Manual documentation for audits
- Fear of losing traceability

**Needs:**
- Spec injection in PRs
- Audit log of all syncs
- Compliance mode with SLSA/NIST alignment

**Quote:** "If it's not documented, it didn't happen."

---

### Persona 4: Open Source Maintainer
**Name:** Riley
**Role:** OSS maintainer, distributed contributors
**Tools:** GitHub Issues exclusively
**Pain Points:**
- Too many issues to track in browser
- Wants to triage locally
- Contributors need visibility

**Needs:**
- Offline-first workflow
- Quick issue pulling
- No auth complexity (use existing gh CLI)

**Quote:** "I review 50+ issues/week. I need them in my terminal."

---

## 4. Pain Point Collection Framework

| Category | Pain Point | Severity (1-5) | Frequency | Affected User Stories |
|----------|------------|----------------|-----------|----------------------|
| Sync | Manual copy-paste between systems | | | US-1, US-2 |
| Context | Switching between tools | | | All |
| Status | Keeping status in sync | | | US-2 |
| Fields | Custom field mapping complexity | | | US-1 |
| Compliance | Proving work lineage | | | US-4 |
| PR | Adding spec context to PRs | | | US-3 |

---

## 5. Baseline Metrics Template

### Time Tracking (Per Participant)

| Activity | Time (min/week) | Notes |
|----------|-----------------|-------|
| Manually copying task details | | |
| Updating status in remote tracker | | |
| Cross-referencing local/remote | | |
| Creating PRs with task context | | |
| Compliance documentation | | |
| **Total** | | |

### Aggregate Targets
- Interview goal: **5+ teams**
- Survey goal: **20+ respondents**
- Baseline metric: **Average hours/week on manual sync**

---

## Next Steps

1. [ ] Recruit 5+ teams for interviews (via Slack, Twitter, existing users)
2. [ ] Conduct interviews (30-40 min each)
3. [ ] Deploy survey to broader audience
4. [ ] Compile findings into task-012 notes
5. [ ] Create persona cards for design phase

---

*Created for task-012 - Product Discovery - User Interviews*
