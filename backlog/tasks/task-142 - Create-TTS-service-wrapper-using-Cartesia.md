---
id: task-142
title: Create TTS service wrapper using Cartesia
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - us1
  - tts
  - phase3
dependencies:
  - task-140
priority: high
---

## Description

Implement src/specify_cli/voice/services/tts.py with CartesiaTTSService class wrapping pipecat-ai Cartesia integration for low-latency speech synthesis. Reference: docs/research/pipecat-voice-integration-summary.md TTS Provider section

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 CartesiaTTSService class extends pipecat CartesiaTTSService with custom configuration
- [ ] #2 Supports WebSocket streaming for real-time audio output
- [ ] #3 API key loaded from CARTESIA_API_KEY environment variable
- [ ] #4 Voice ID and output format (pcm_16000) configurable via VoiceConfig
- [ ] #5 Synthesis errors raise TTSServiceError with provider error details
<!-- AC:END -->
