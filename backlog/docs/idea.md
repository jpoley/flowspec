Specification: External Issue Tracker Integration ("Satellite Mode")
Status: Draft
Owner: [Your Name/Agent]
Target System: Backlog.md Core
Priority: High
1. Overview
Currently, Backlog.md operates as an isolated, local-only task manager. However, most teams use upstream "Mother Ship" systems like GitHub Issues, Jira, or Notion.
This feature introduces "Satellite Mode": an optional module that allows Backlog.md to:
Ingest (Pull) tasks from upstream systems into the local backlog.
Link local tasks to remote IDs to maintain a "Golden Thread" of traceability.
Sync status updates back to the parent system.
Eject (Push) the final spec.md and implementation details into the upstream PR or Ticket upon completion.
2. Goals & Non-Goals
Goals
Bidirectional Sync: Title, Description, Status, Assignee.
Pluggable Adapters: Support for GitHub, Jira, and Notion.
Auditability: Ensure the "Spec" (requirements) acts as the immutable payload for PR bodies and Ticket resolutions.
Compliance Ready: Support workflows required for high-assurance environments (SLSA, NIST).
Zero-config Fallbacks: If auth fails, degrade gracefully to local-only.
Non-Goals
Real-time Websocket syncing (Polling or on-demand sync is sufficient).
Syncing comments/chat history (Link to the ticket instead).
Complex workflow state mapping (e.g., mapping custom Jira transitions to simple Todo/Doing/Done is out of scope V1).
3. User Stories
ID
Story
Acceptance Criteria
US-1
As a developer, I want to pull a Jira ticket by ID so I can work on it locally.
backlog remote pull PROJ-123 creates a local markdown task with title, desc, and link.
US-2
As a team lead, I want GitHub Issues assigned to me to appear in Backlog.md.
backlog remote sync fetches all "In Progress" or "Assigned" items from upstream.
US-3
As a developer, I want my PR description to automatically include the spec.md content.
Command backlog remote pr <task-id> creates a PR using the linked spec as the body.
US-4
As a Compliance Officer, I want to verify that every PR maps back to an authorized Jira ticket.
The "upstream" metadata field is mandatory for PR generation in strict mode.

4. Technical Architecture
4.1 Data Model Changes
We need to extend the Frontmatter of the Task Markdown files to include an upstream object.
File: backlog/tasks/TASK-001.md
---
id: 1
title: Fix Login Latency
status: In Progress
upstream:
  provider: jira
  id: PROJ-1042
  url: [https://company.atlassian.net/browse/PROJ-1042](https://company.atlassian.net/browse/PROJ-1042)
  last_sync: 2023-10-27T10:00:00Z
  fields:
    story_points: 5
    priority: High
compliance:
  risk_level: low
  requires_approval: false
---


4.2 Configuration (.backlog/config.yml)
Add a new remotes section to handle auth and mapping.
remotes:
  github:
    enabled: true
    repo: owner/repo
    auth_mode: gh_cli # Uses local 'gh' auth
  jira:
    enabled: false
    domain: company.atlassian.net
    email: user@company.com
    # Token stored in env var JIRA_API_TOKEN
    status_map:
      todo: "To Do"
      in_progress: "In Development"
      done: "Closed"


4.3 The Adapter Pattern
We will implement a RemoteProvider interface to normalize interactions.
interface RemoteProvider {
  name: string;
  // Ingest
  fetchTask(externalId: string): Promise<TaskData>;
  fetchAssignedTasks(): Promise<TaskData[]>;
  
  // Sync
  updateStatus(externalId: string, status: Status): Promise<void>;
  
  // Eject
  createPullRequest(task: Task, specContent: string): Promise<string>;
  postComment(externalId: string, body: string): Promise<void>;
}


5. Functional Requirements (CLI)
5.1 Command: backlog remote pull <id>
Input: External ID (e.g., PROJ-123 or #42 or https://notion.so/...).
Logic:
Detect provider based on regex or config.
Call API to get Title/Body.
Create local Task.
Update upstream status to "In Progress" (optional flag).
5.2 Command: backlog remote push <task-id>
Trigger: User has finished work and wants to submit.
Logic:
Read spec.md associated with the task (via naming convention or prompts).
Validate Compliance: Ensure Spec is complete and linked to Upstream.
If GitHub:
Generate PR.
Title = Task Title.
Body = ## Implementation Spec\n\n + Spec Content + \n\nCloses #42.
If Jira/Notion:
Post comment with link to PR (if exists) or link to Commit.
Update status to "Review" or "Done".
6. Compliance & Supply Chain Security
This integration is designed to support high-assurance software supply chains. By strictly linking "Intent" (Ticket) to "Plan" (Spec) to "Implementation" (PR), we satisfy key controls in SLSA and NIST frameworks.
6.1 SLSA (Supply-chain Levels for Software Artifacts)
Provenance (SLSA L2/L3): The backlog remote push command generates a verifiable link between the source code change and the upstream requirement.
Traceability: Every PR generated via this tool includes the full spec.md, serving as an immutable record of why the code was changed, satisfying the "Identified Source" requirement.
6.2 NIST CSF (Cybersecurity Framework)
Identify (ID.AM): Ensures all software changes are mapped to an authorized asset/ticket in the central backlog.
Protect (PR.AC): Enforces authorization by preventing "rogue commits" that lack an upstream parent (via optional git hooks).
Detect (DE.CM): The upstream metadata in frontmatter allows automated auditing of changes against approved work orders.
6.3 SOC2 & ISO 27001
Change Management: The automated injection of the Spec into the PR body provides evidence that the change was designed, documented, and approved before implementation.
7. Implementation Plan
Phase 1: Core Interface & GitHub
Define RemoteProvider interface.
Implement GitHubProvider using gh CLI wrapper.
Add upstream field to Task parser.
Phase 2: The "Spec-to-PR" Pipeline
Implement logic to find the spec.md file for a given task.
Create the createPullRequest function that injects the spec markdown into the PR body.
Phase 3: Atlassian & Notion
Implement JiraProvider (REST API).
Implement NotionProvider (Client API).
Add strict field mapping configuration.
8. Security Considerations
API Tokens: Never store tokens in config.yml. Use environment variables (JIRA_TOKEN, NOTION_KEY) or system keychain.
Write Access: Default to "Safe Mode" (Ask for confirmation before updating upstream tickets).
Sanitization: Ensure external content (Jira descriptions) is sanitized before rendering as Markdown to prevent XSS in local viewers.
