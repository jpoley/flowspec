---
id: task-143
title: Create LLM service wrapper using OpenAI
status: Done
assignee:
  - '@backend-engineer'
created_date: '2025-11-28'
updated_date: '2025-11-29 00:35'
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

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement src/specify_cli/voice/services/llm.py with OpenAILLMService class wrapping pipecat-ai OpenAI integration for GPT-4o with streaming responses and function calling support. Reference: docs/research/pipecat-voice-integration-summary.md LLM Provider section
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 OpenAILLMService class extends pipecat OpenAILLMService with function calling enabled
- [x] #2 Supports streaming responses for token-by-token delivery to TTS
- [x] #3 API key loaded from OPENAI_API_KEY environment variable
- [x] #4 Model defaults to "gpt-4o" with temperature and max_tokens configurable
- [x] #5 LLM errors raise LLMServiceError with OpenAI error code and message
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Summary

Created OpenAI LLM service wrapper in src/specify_cli/voice/services/llm.py that:

1. **Extends Pipecat OpenAILLMService** - Inherits from pipecat.services.openai.llm.OpenAILLMService
2. **Function calling enabled** - Parent class provides register_function, unregister_function, has_function methods
3. **Streaming responses** - Parent class handles token-by-token streaming automatically via get_chat_completions
4. **API key from environment** - Loads from OPENAI_API_KEY env var with fallback to explicit parameter
5. **Configurable parameters** - Model defaults to "gpt-4o", temperature=0.7, max_tokens=1000 all configurable
6. **Enhanced error handling** - process_frame wraps parent method to catch errors and convert to LLMServiceError with proper error codes

## Files Created

- src/specify_cli/voice/exceptions.py - Base exceptions for voice module
- src/specify_cli/voice/services/llm.py - OpenAI LLM service wrapper
- tests/voice/test_llm.py - Comprehensive unit tests (17 tests, all passing)

## Dependencies Added

- pytest-asyncio>=0.21.0 to pyproject.toml dev extras

## Test Coverage

All 17 tests passing:
- Initialization with API key (explicit and env var)
- Configuration error when API key missing
- Custom model, temperature, max_tokens parameters
- Frame processing with success and error scenarios
- Error code extraction from OpenAI exceptions
- Common error patterns (rate limit, invalid key, quota, context length)
- Streaming and function calling capability verification

## Code Quality

- All code formatted with ruff
- Type hints on all public functions
- Comprehensive docstrings
- Follows project patterns from existing codebase
<!-- SECTION:NOTES:END -->
