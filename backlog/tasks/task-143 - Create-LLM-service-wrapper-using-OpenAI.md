---
id: task-143
title: Create LLM service wrapper using OpenAI
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - us1
  - llm
  - phase3
dependencies:
  - task-140
priority: high
---

## Description

Implement src/specify_cli/voice/services/llm.py with OpenAILLMService class wrapping pipecat-ai OpenAI integration for GPT-4o with streaming responses and function calling support. Reference: docs/research/pipecat-voice-integration-summary.md LLM Provider section

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 OpenAILLMService class extends pipecat OpenAILLMService with function calling enabled
- [ ] #2 Supports streaming responses for token-by-token delivery to TTS
- [ ] #3 API key loaded from OPENAI_API_KEY environment variable
- [ ] #4 Model defaults to "gpt-4o" with temperature and max_tokens configurable
- [ ] #5 LLM errors raise LLMServiceError with OpenAI error code and message
<!-- AC:END -->
