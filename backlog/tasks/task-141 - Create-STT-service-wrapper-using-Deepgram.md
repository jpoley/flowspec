---
id: task-141
title: Create STT service wrapper using Deepgram
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - us1
  - stt
  - phase3
dependencies:
  - task-140
priority: high
---

## Description

Implement src/specify_cli/voice/services/stt.py with DeepgramSTTService class wrapping pipecat-ai Deepgram integration. Use Nova 3 model for optimal accuracy and streaming transcription. Reference: docs/research/pipecat-voice-integration-summary.md STT Provider section

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 DeepgramSTTService class extends pipecat DeepgramSTTService with custom configuration
- [ ] #2 Supports streaming transcription returning TranscriptionFrame with word-level timing
- [ ] #3 API key loaded from DEEPGRAM_API_KEY environment variable
- [ ] #4 Model defaults to "nova-3" with language "en" configurable via config
- [ ] #5 Connection errors raise STTServiceError with descriptive message and retry hint
<!-- AC:END -->
