# Backlog.md — Local RAG (DuckDB + HNSW) for Claude Code Subagents

## 0. Core Outcome

Implement a tool-first, per-subagent, local RAG system using DuckDB + HNSW where each Claude Code subagent has its own isolated knowledge base, and can only access it via a coding tool (no giant prompts, no hidden context hacks).

---

## 1. High-Level Requirements

- Each subagent has:
  - Its own knowledge corpus
  - Its own DuckDB database and vector index (HNSW)
  - Its own logical agent_id
- Claude (or any coding agent runtime) interacts via:
  - A single RAG tool endpoint (e.g., subagent_rag_search)
  - Optional write/update tools (e.g., subagent_rag_insert)
- RAG is:
  - Local (runs on your infra)
  - Testable (retrieval quality measurable)
  - Swappable (change corpora without rewriting prompts)
- Prompts define:
  - Behavior, style, responsibilities
- RAG defines:
  - Facts, internal docs, standards, patterns, code idioms

---

## 2. Phase 1 — Subagent Strategy & Design

### 2.1 Identify Pilot Subagent

- [ ] Pick a single pilot subagent (e.g., security-agent)
- [ ] Define its scope:
  - Responsibilities (security patterns, guardrails, policies)
  - Types of questions it should answer
  - Types of artifacts it should generate (policies, code snippets, reviews)
- [ ] Define clear out-of-scope areas to avoid overlap with other agents

### 2.2 Define Behavior vs Knowledge Split

- [ ] Write a short system/persona description for the pilot agent:
  - How it should behave
  - How cautious or strict it should be
  - How to reference internal policies
- [ ] Explicitly state in persona:
  - The agent must call the RAG tool when it needs organization-specific knowledge
  - It must not hallucinate policy details when RAG returns nothing
- [ ] Document what belongs in:
  - The prompt (behavior, style, meta-rules)
  - The RAG corpus (facts, patterns, examples, policies)

### 2.3 Define Required Corpora

- [ ] List initial corpora for the pilot agent:
  - Internal security standards
  - Common code patterns (approved, non-approved)
  - Infrastructure baselines (e.g., standard EKS/ECS patterns)
  - Triaged issues and historical incident writeups
- [ ] Estimate size (pages, files) and change frequency
- [ ] Confirm that:
  - Size > a trivial cheat sheet
  - Knowledge is expected to evolve over time

---

## 3. Phase 2 — Data Model & DuckDB / HNSW Layout

### 3.1 Per-Agent Storage Layout

- [ ] Decide base directory for RAG storage:
  - Example:
      - /rag/security/security.duckdb
      - /rag/security/security.hnsw
      - /rag/infra/infra.duckdb
      - /rag/infra/infra.hnsw
- [ ] Decide naming conventions:
  - <agent_id>.duckdb
  - <agent_id>.hnsw
- [ ] Document how mapping agent_id to DB/index path works

### 3.2 DuckDB Schema Design

- [ ] Create table: documents
  - Columns (example):
      - doc_id: BIGINT PRIMARY KEY
      - source: TEXT (e.g., "confluence", "git", "manual")
      - uri: TEXT (original URL or file path)
      - title: TEXT
      - metadata: JSON (arbitrary structured data)
      - chunk_index: INTEGER (chunk number within the source)
      - text: TEXT (chunk content)
- [ ] Create table: embeddings
  - Columns (example):
      - embedding_id: BIGINT PRIMARY KEY
      - doc_id: BIGINT (foreign key to documents.doc_id)
      - vector: FLOAT[DIM] (embedding vector; DIM is model-specific)
      - norm: FLOAT (optional; used for faster similarity)
- [ ] Decide:
  - Exact dimension DIM (based on embedding model)
  - Indexes on doc_id, source, uri for fast lookup

### 3.3 HNSW Index Strategy

- [ ] Decide whether HNSW is:
  - Implemented via a DuckDB extension (native index)
  - Implemented via external library (e.g., hnswlib) with embedding_id as key
- [ ] Define:
  - HNSW parameters (M, ef_construction, ef_search)
  - How index is stored on disk and loaded in memory
- [ ] Document how to:
  - Build index from scratch
  - Incrementally update index when new embeddings are inserted

---

## 4. Phase 3 — Ingestion Pipeline

### 4.1 Source Collection

- [ ] Enumerate content sources for pilot agent:
  - Git repos (markdown, code comments, docs folders)
  - Confluence / wiki pages
  - PDFs / external standards (if allowed)
- [ ] Define access method:
  - API, git clone, local filesystem, or sync job
- [ ] Define update cadence:
  - On commit hook
  - Nightly batch
  - Manual reindex command

### 4.2 Normalization & Chunking

- [ ] Implement parsing for:
  - Markdown
  - Plaintext
  - HTML
  - PDFs (if necessary)
- [ ] Implement chunking:
  - Choose chunk size (e.g., 300–800 tokens; decide one)
  - Define overlap size (e.g., 10–20 percent or N sentences)
- [ ] Store:
  - text (chunk content)
  - chunk_index (within source)
  - metadata (section heading, file name, repo, tags)

### 4.3 Embedding

- [ ] Select embedding model:
  - Local vs remote
  - Dimension and cost/latency
- [ ] Implement embedding service/component:
  - Accepts batches of text
  - Returns vectors and error info
- [ ] Integrate embeddings with DuckDB:
  - Insert into embeddings table with correct doc_id
  - Commit transaction on success
  - Handle partial failures and retry logic

### 4.4 Index Build / Refresh

- [ ] Implement script to:
  - Scan embeddings table
  - Build initial HNSW index from scratch
- [ ] Implement incremental update logic:
  - Add new embeddings only
  - Mark old embeddings as retired if content removed
- [ ] Define:
  - Threshold for rebuild vs incremental update
- [ ] Add metrics/tracing:
  - Index size
  - Build time
  - Last updated timestamp

---

## 5. Phase 4 — Local RAG Microservice

### 5.1 Service Contract

- [ ] Define API endpoint (example):
  - POST /rag/query
- [ ] Define request schema:
  - agent_id: string
  - query: string
  - top_k: integer (optional; default, max)
  - filters: object (optional; key-value filter hints)
- [ ] Define response schema:
  - results: array of:
      - content: string
      - score: float (similarity/relevance)
      - source: string
      - uri: string
      - metadata: object
- [ ] Define error envelope:
  - error_code
  - error_message
  - optional details

### 5.2 Query Processing Flow

- [ ] Implement pipeline:
  - Validate agent_id and query
  - Map agent_id to:
      - DB path
      - HNSW index
  - Embed query using same embedding model
  - Run ANN search using HNSW
  - Retrieve top_k embedding_ids
  - Map to doc_id and then documents table
  - Apply filters (if any)
  - Optionally rerank results
  - Return JSON response
- [ ] Implement safety checks:
  - Max top_k
  - Timeouts
  - Graceful handling of empty results

### 5.3 Operational Concerns

- [ ] Implement logging:
  - agent_id
  - query (possibly redacted)
  - latency
  - number of hits
- [ ] Implement basic metrics:
  - qps
  - p95 / p99 latency
  - index load times
- [ ] Implement health endpoint:
  - GET /health
- [ ] Document operational runbook:
  - How to restart
  - How to rebuild index
  - Debugging slow queries

---

## 6. Phase 5 — Tool Adapter for Claude Code / Subagents

### 6.1 Tool Schema Definition

- [ ] Define tool function (example):

  Name:
    subagent_rag_search

  Description:
    Search this subagent's private knowledge base using semantic search. Returns the most relevant knowledge chunks for the given query.

  Input:
    - agent_id: string
    - query: string
    - top_k: integer (optional)
    - filters: object (optional)

  Output:
    - results: array of structured chunks (content, source, score, metadata)

- [ ] Ensure schema is explicit and minimal
- [ ] Add documentation explaining when the agent should call this tool

### 6.2 Implementation of Adapter

- [ ] Implement MCP server or local tool bridge:
  - Receives tool call from Claude / runtime
  - Validates input
  - Makes HTTP/gRPC call to RAG microservice
  - Returns structured JSON to model
- [ ] Implement error handling:
  - Map HTTP/gRPC errors to tool errors
  - Provide clear error messages on bad agent_id
- [ ] Implement timeouts:
  - Reasonable per-query timeout
  - Fallback behavior (e.g., return no results rather than hang)

### 6.3 Agent Configuration

- [ ] Configure pilot subagent with:
  - agent_id = "security" (example)
  - Allowed tools: subagent_rag_search (plus other relevant coding tools)
- [ ] In system prompt:
  - Instruct agent to:
      - Call subagent_rag_search when domain-specific information is needed
      - Prefer tool result over generic knowledge
      - Decline to guess if tool returns nothing relevant
- [ ] Ensure:
  - No cross-agent corpus access from this agent unless explicitly designed

---

## 7. Phase 6 — Testing, Evaluation, and Comparison to Prompt-Only

### 7.1 Retrieval Quality Test Suite

- [ ] Create test set:
  - 20–50 queries representative of real work
  - For each query:
      - Expected doc(s)
      - Expected key facts
- [ ] Implement script to:
  - Run each query against RAG endpoint
  - Record top_k results
  - Measure:
      - Recall of expected docs
      - Precision at k
- [ ] Iterate on:
  - Chunk size
  - Embedding model
  - HNSW parameters

### 7.2 Agent Behavior Tests

- [ ] Define 10–20 tasks for the pilot agent:
  - Example tasks:
      - "Generate a secure EKS config based on our org patterns"
      - "Review this Terraform snippet for violations against our security standards"
      - "Explain our recommended pattern for IAM roles for service X"
- [ ] Run each task in two modes:
  - With RAG tool enabled
  - With RAG tool disabled but same persona prompt
- [ ] Compare results:
  - Accuracy of internal details
  - Number of hallucinations
  - Ability to reference specific policies or patterns
  - Context size and token usage

### 7.3 Decide Worthwhile vs Overkill

- [ ] Evaluate:
  - Does RAG significantly reduce hallucinations?
  - Does it enable tasks that were not reliably solvable via prompts?
  - Is maintenance overhead acceptable?
- [ ] If no clear win:
  - Identify whether:
      - Corpus is too small/simple (prompt might be enough)
      - Retrieval is misconfigured
- [ ] If clear win:
  - Proceed to multi-agent rollout (next phase)

---

## 8. Phase 7 — Multi-Agent Rollout

### 8.1 Add New Subagents

- [ ] Identify additional agents:
  - infra-agent
  - data-agent
  - frontend-agent
  - etc.
- [ ] For each new agent:
  - Define scope and persona
  - Define corpora
  - Create DuckDB DB and HNSW index
  - Configure agent_id and tools

### 8.2 Shared vs Private Corpora

- [ ] Decide which knowledge is:
  - Global (shared among agents)
  - Domain-specific (per agent)
- [ ] Implement one of:
  - Separate DBs and indexes:
      - Each agent queries its own DB only
  - Hybrid model:
      - Global DB plus per-agent DB
      - Tool can query one or both depending on agent_id

### 8.3 Cross-Agent Collaboration

- [ ] Define handoff patterns:
  - Security agent passes a task to infra agent with:
      - Natural language summary
      - List of relevant URIs
  - Infra agent runs its own RAG queries using those URIs
- [ ] Avoid direct sharing of chunks between agents:
  - Encourage each agent to re-query its own KB with passed hints

---

## 9. Phase 8 — Maintenance, Governance, and Hardening

### 9.1 Operational Playbooks

- [ ] Document:
  - How to add new content to corpora
  - How to rebuild the index
  - How to roll back a bad content update
- [ ] Create simple CLI:
  - reindex-agent <agent_id>
  - list-sources <agent_id>
  - test-query <agent_id> "query text"

### 9.2 Access Control & Auditing

- [ ] If needed, restrict:
  - Which subagent can query which corpus
- [ ] Log:
  - agent_id
  - query hash or redacted query
  - top URIs returned
- [ ] Add basic guardrails:
  - Prevent RAG from returning sensitive blobs that should never leave a secure context unless properly authorized, if applicable

### 9.3 Upgrade Paths

- [ ] Plan for:
  - Swapping embedding model
  - Changing vector index (HNSW to something else) without API change
- [ ] Keep tool API stable:
  - So agent behaviors don’t need rewriting

---

## 10. Implementation Checklist Snapshot (Condensed)

- [ ] Define pilot subagent scope and persona
- [ ] Define knowledge corpora and confirm they justify RAG
- [ ] Design DuckDB schema (documents + embeddings)
- [ ] Design per-agent DB and index layout
- [ ] Implement ingestion & chunking pipeline
- [ ] Implement embedding integration
- [ ] Build and persist HNSW index
- [ ] Implement local RAG microservice (query endpoint)
- [ ] Implement tool adapter (subagent_rag_search)
- [ ] Configure pilot agent with tool and agent_id
- [ ] Build retrieval test suite and run evaluations
- [ ] Compare RAG-based vs prompt-only behaviors
- [ ] If successful, replicate pattern across multiple subagents
