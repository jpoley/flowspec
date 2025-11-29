"""Voice configuration schema and loader.

This module provides configuration dataclasses and loaders for the voice assistant.
Configuration is loaded from JSON files with API keys sourced from environment variables.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class VoiceSettings:
    """Voice synthesis settings."""

    speed: float = 1.0
    stability: float = 0.75


@dataclass
class AssistantConfig:
    """Assistant behavior configuration."""

    name: str
    system_prompt: str = "You are a helpful assistant for JP Spec Kit."
    first_message: str = "Hello! I'm your JP Spec Kit assistant. How can I help?"
    last_message: str = "Goodbye! Let me know if you need anything else."
    voice_settings: VoiceSettings = field(default_factory=VoiceSettings)


@dataclass
class STTConfig:
    """Speech-to-Text configuration."""

    provider: str
    model: str = "nova-3"
    language: str = "en"


@dataclass
class LLMConfig:
    """Language Model configuration."""

    provider: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class TTSConfig:
    """Text-to-Speech configuration."""

    provider: str
    voice_id: str = "default"
    output_format: str = "pcm_16000"


@dataclass
class PipelineConfig:
    """Voice pipeline configuration."""

    stt: STTConfig
    llm: LLMConfig
    tts: TTSConfig


@dataclass
class TransportConfig:
    """Transport layer configuration."""

    type: str = "daily"
    room_url: Optional[str] = None
    token: Optional[str] = None


@dataclass
class APIKeys:
    """API keys loaded from environment variables."""

    deepgram: Optional[str] = None
    openai: Optional[str] = None
    cartesia: Optional[str] = None
    daily: Optional[str] = None
    anthropic: Optional[str] = None
    elevenlabs: Optional[str] = None


@dataclass
class VoiceConfig:
    """Complete voice assistant configuration."""

    assistant: AssistantConfig
    pipeline: PipelineConfig
    transport: TransportConfig = field(default_factory=TransportConfig)
    api_keys: APIKeys = field(default_factory=APIKeys)

    def validate(self) -> None:
        """Validate configuration and check for required API keys.

        Raises:
            ValueError: If required fields are missing or required API keys are not set.
        """
        # Validate required config fields
        if not self.assistant.name:
            raise ValueError("assistant.name is required")
        if not self.pipeline.stt.provider:
            raise ValueError("pipeline.stt.provider is required")
        if not self.pipeline.llm.provider:
            raise ValueError("pipeline.llm.provider is required")
        if not self.pipeline.tts.provider:
            raise ValueError("pipeline.tts.provider is required")

        # Validate API keys based on providers
        missing_keys = []

        # Check STT provider keys
        if self.pipeline.stt.provider == "deepgram" and not self.api_keys.deepgram:
            missing_keys.append("DEEPGRAM_API_KEY")

        # Check LLM provider keys
        if self.pipeline.llm.provider == "openai" and not self.api_keys.openai:
            missing_keys.append("OPENAI_API_KEY")
        elif self.pipeline.llm.provider == "anthropic" and not self.api_keys.anthropic:
            missing_keys.append("ANTHROPIC_API_KEY")

        # Check TTS provider keys
        if self.pipeline.tts.provider == "cartesia" and not self.api_keys.cartesia:
            missing_keys.append("CARTESIA_API_KEY")
        elif (
            self.pipeline.tts.provider == "elevenlabs" and not self.api_keys.elevenlabs
        ):
            missing_keys.append("ELEVENLABS_API_KEY")

        # Check transport keys
        if self.transport.type == "daily" and not self.api_keys.daily:
            missing_keys.append("DAILY_API_KEY")

        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}. "
                f"Please set these environment variables."
            )


def load_api_keys() -> APIKeys:
    """Load API keys from environment variables.

    Returns:
        APIKeys instance with keys loaded from environment.
    """
    return APIKeys(
        deepgram=os.getenv("DEEPGRAM_API_KEY"),
        openai=os.getenv("OPENAI_API_KEY"),
        cartesia=os.getenv("CARTESIA_API_KEY"),
        daily=os.getenv("DAILY_API_KEY"),
        anthropic=os.getenv("ANTHROPIC_API_KEY"),
        elevenlabs=os.getenv("ELEVENLABS_API_KEY"),
    )


def load_config(config_path: Path) -> VoiceConfig:
    """Load voice configuration from JSON file.

    Args:
        config_path: Path to JSON configuration file.

    Returns:
        VoiceConfig instance with configuration loaded.

    Raises:
        FileNotFoundError: If config file does not exist.
        ValueError: If config file is invalid or required fields are missing.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        data = json.load(f)

    # Parse assistant config
    assistant_data = data.get("assistant", {})
    voice_settings_data = assistant_data.get("voice_settings", {})
    assistant_config = AssistantConfig(
        name=assistant_data.get("name", ""),
        system_prompt=assistant_data.get(
            "system_prompt", "You are a helpful assistant for JP Spec Kit."
        ),
        first_message=assistant_data.get(
            "first_message", "Hello! I'm your JP Spec Kit assistant. How can I help?"
        ),
        last_message=assistant_data.get(
            "last_message", "Goodbye! Let me know if you need anything else."
        ),
        voice_settings=VoiceSettings(
            speed=voice_settings_data.get("speed", 1.0),
            stability=voice_settings_data.get("stability", 0.75),
        ),
    )

    # Parse pipeline config
    pipeline_data = data.get("pipeline", {})
    stt_data = pipeline_data.get("stt", {})
    llm_data = pipeline_data.get("llm", {})
    tts_data = pipeline_data.get("tts", {})

    pipeline_config = PipelineConfig(
        stt=STTConfig(
            provider=stt_data.get("provider", ""),
            model=stt_data.get("model", "nova-3"),
            language=stt_data.get("language", "en"),
        ),
        llm=LLMConfig(
            provider=llm_data.get("provider", ""),
            model=llm_data.get("model", "gpt-4o"),
            temperature=llm_data.get("temperature", 0.7),
            max_tokens=llm_data.get("max_tokens", 1000),
        ),
        tts=TTSConfig(
            provider=tts_data.get("provider", ""),
            voice_id=tts_data.get("voice_id", "default"),
            output_format=tts_data.get("output_format", "pcm_16000"),
        ),
    )

    # Parse transport config
    transport_data = data.get("transport", {})
    transport_config = TransportConfig(
        type=transport_data.get("type", "daily"),
        room_url=transport_data.get("room_url"),
        token=transport_data.get("token"),
    )

    # Load API keys from environment
    api_keys = load_api_keys()

    # Create config
    config = VoiceConfig(
        assistant=assistant_config,
        pipeline=pipeline_config,
        transport=transport_config,
        api_keys=api_keys,
    )

    # Validate config
    config.validate()

    return config
