---
id: task-139
title: Implement voice configuration schema and loader
status: To Do
assignee:
  - '@pm-planner'
created_date: '2025-11-28'
labels:
  - implement
  - voice
  - foundational
  - phase2
dependencies:
  - task-138
priority: high
---

## Description

Create src/specify_cli/voice/config.py with dataclasses for AssistantConfig (name, system_prompt, first_message, last_message, voice_settings) and PipelineConfig (stt, llm, tts providers). Load from JSON config file and environment variables for API keys. Reference: docs/research/pipecat-voice-integration-summary.md Configuration Architecture section

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 VoiceConfig dataclass validates required fields: assistant.name, pipeline.stt.provider, pipeline.llm.provider, pipeline.tts.provider
- [ ] #2 Environment variables DEEPGRAM_API_KEY, OPENAI_API_KEY, CARTESIA_API_KEY, DAILY_API_KEY loaded when present
- [ ] #3 Missing required API key raises ValueError with message listing all missing keys
- [ ] #4 JSON config template created at templates/voice-config.json with all fields documented in comments
- [ ] #5 Unit test tests/voice/test_config.py achieves 90%+ line coverage on config.py
<!-- AC:END -->
