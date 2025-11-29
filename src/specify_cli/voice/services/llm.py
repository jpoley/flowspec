"""LLM service wrapper using OpenAI for JP Spec Kit voice integration.

This module provides an OpenAI-based LLM service with:
- GPT-4o model with streaming responses
- Function calling support for JP Spec Kit operations
- Token-by-token delivery to TTS
- Configurable temperature and max_tokens
- Proper error handling with OpenAI error codes
"""

import os
from typing import Any

from pipecat.services.openai.base_llm import BaseOpenAILLMService
from pipecat.services.openai.llm import OpenAILLMService as PipecatOpenAILLMService

from specify_cli.voice.exceptions import ConfigurationError, LLMServiceError


class OpenAILLMService(PipecatOpenAILLMService):
    """OpenAI LLM service wrapper for JP Spec Kit voice integration.

    This class extends Pipecat's OpenAILLMService with:
    - Function calling enabled by default
    - Streaming responses for token-by-token TTS delivery
    - Configuration from environment variables
    - Enhanced error handling with OpenAI error codes

    The service wraps OpenAI's GPT-4o model with appropriate defaults
    for conversational voice interaction.
    """

    def __init__(
        self,
        *,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize OpenAI LLM service for voice interaction.

        Args:
            model: OpenAI model to use (default: gpt-4o)
            temperature: Sampling temperature 0.0-2.0 (default: 0.7)
            max_tokens: Maximum tokens to generate (default: 1000)
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            **kwargs: Additional arguments passed to PipecatOpenAILLMService

        Raises:
            ConfigurationError: If API key is not provided and OPENAI_API_KEY
                               environment variable is not set
        """
        # Load API key from environment if not provided
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ConfigurationError(
                    "OPENAI_API_KEY environment variable must be set or "
                    "api_key parameter must be provided",
                    code="MISSING_API_KEY",
                )

        # Configure input parameters for LLM
        params = BaseOpenAILLMService.InputParams(
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Initialize parent with function calling enabled
        # The parent class handles streaming responses automatically
        super().__init__(
            model=model,
            params=params,
            api_key=api_key,
            **kwargs,
        )

    async def process_frame(self, frame: Any, direction: Any) -> None:
        """Process frames with enhanced error handling.

        This method wraps the parent's process_frame to catch and convert
        OpenAI API errors into LLMServiceError exceptions with proper error
        codes and messages.

        Args:
            frame: Frame to process
            direction: Processing direction (upstream/downstream)

        Raises:
            LLMServiceError: If OpenAI API returns an error
        """
        try:
            await super().process_frame(frame, direction)
        except Exception as e:
            # Extract OpenAI error details if available
            error_code = None
            error_message = str(e)

            # Check if this is an OpenAI API error with a code attribute
            if hasattr(e, "code"):
                error_code = str(e.code)
            elif hasattr(e, "status_code"):
                error_code = str(e.status_code)

            # Check for common OpenAI error patterns in message
            error_message_lower = error_message.lower()
            if not error_code:
                if (
                    "rate_limit" in error_message_lower
                    or "rate limit" in error_message_lower
                ):
                    error_code = "rate_limit_exceeded"
                elif (
                    "invalid_api_key" in error_message_lower
                    or "invalid api key" in error_message_lower
                ):
                    error_code = "invalid_api_key"
                elif (
                    "insufficient_quota" in error_message_lower
                    or "insufficient quota" in error_message_lower
                ):
                    error_code = "insufficient_quota"
                elif (
                    "context_length_exceeded" in error_message_lower
                    or "context length exceeded" in error_message_lower
                ):
                    error_code = "context_length_exceeded"

            # Re-raise as LLMServiceError
            raise LLMServiceError(
                f"OpenAI LLM service error: {error_message}",
                code=error_code,
            ) from e


__all__ = ["OpenAILLMService"]
