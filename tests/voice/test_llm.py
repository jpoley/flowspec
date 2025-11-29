"""Unit tests for OpenAI LLM service wrapper."""

import os
from unittest.mock import AsyncMock, Mock, patch

import pytest

from specify_cli.voice.exceptions import ConfigurationError, LLMServiceError
from specify_cli.voice.services.llm import OpenAILLMService


class TestOpenAILLMService:
    """Test suite for OpenAILLMService."""

    def test_init_with_api_key(self) -> None:
        """Test initialization with explicit API key."""
        service = OpenAILLMService(api_key="test-key-123")

        assert service is not None

    def test_init_with_env_var(self) -> None:
        """Test initialization using OPENAI_API_KEY environment variable."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key-456"}):
            service = OpenAILLMService()

            assert service is not None

    def test_init_missing_api_key(self) -> None:
        """Test initialization fails when API key is not provided."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove OPENAI_API_KEY if it exists
            os.environ.pop("OPENAI_API_KEY", None)

            with pytest.raises(ConfigurationError) as exc_info:
                OpenAILLMService()

            assert "OPENAI_API_KEY" in str(exc_info.value)
            assert exc_info.value.code == "MISSING_API_KEY"

    def test_init_custom_model(self) -> None:
        """Test initialization with custom model."""
        service = OpenAILLMService(model="gpt-4-turbo", api_key="test-key")

        assert service is not None

    def test_init_custom_temperature(self) -> None:
        """Test initialization with custom temperature."""
        service = OpenAILLMService(temperature=0.9, api_key="test-key")

        assert service is not None

    def test_init_custom_max_tokens(self) -> None:
        """Test initialization with custom max_tokens."""
        service = OpenAILLMService(max_tokens=2000, api_key="test-key")

        assert service is not None

    def test_default_parameters(self) -> None:
        """Test that default parameters are correctly set."""
        service = OpenAILLMService(api_key="test-key")

        # Check that params were set (these are internal to parent class)
        assert service is not None

    @pytest.mark.asyncio
    async def test_process_frame_success(self) -> None:
        """Test successful frame processing."""
        service = OpenAILLMService(api_key="test-key")

        # Mock the parent class process_frame method
        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_frame = Mock()
            mock_direction = Mock()

            await service.process_frame(mock_frame, mock_direction)

            mock_process.assert_called_once_with(mock_frame, mock_direction)

    @pytest.mark.asyncio
    async def test_process_frame_rate_limit_error(self) -> None:
        """Test frame processing with rate limit error."""
        service = OpenAILLMService(api_key="test-key")

        # Mock the parent class to raise a rate limit error
        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Rate limit exceeded")
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "rate_limit_exceeded" == exc_info.value.code
            assert "OpenAI LLM service error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_process_frame_invalid_api_key_error(self) -> None:
        """Test frame processing with invalid API key error."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Invalid API key provided")
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "invalid_api_key" == exc_info.value.code

    @pytest.mark.asyncio
    async def test_process_frame_quota_error(self) -> None:
        """Test frame processing with insufficient quota error."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Insufficient quota")
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "insufficient_quota" == exc_info.value.code

    @pytest.mark.asyncio
    async def test_process_frame_context_length_error(self) -> None:
        """Test frame processing with context length exceeded error."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Context length exceeded")
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "context_length_exceeded" == exc_info.value.code

    @pytest.mark.asyncio
    async def test_process_frame_error_with_code_attribute(self) -> None:
        """Test frame processing extracts error code from exception."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Some error")
            mock_error.code = "custom_error_code"
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "custom_error_code" == exc_info.value.code

    @pytest.mark.asyncio
    async def test_process_frame_error_with_status_code(self) -> None:
        """Test frame processing extracts status_code from exception."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("HTTP error")
            mock_error.status_code = 429
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "429" == exc_info.value.code

    @pytest.mark.asyncio
    async def test_process_frame_generic_error(self) -> None:
        """Test frame processing with generic error."""
        service = OpenAILLMService(api_key="test-key")

        with patch.object(
            service.__class__.__bases__[0],
            "process_frame",
            new_callable=AsyncMock,
        ) as mock_process:
            mock_error = Exception("Generic error message")
            mock_process.side_effect = mock_error

            with pytest.raises(LLMServiceError) as exc_info:
                await service.process_frame(Mock(), Mock())

            assert "OpenAI LLM service error" in str(exc_info.value)
            # Generic errors may not have a code
            assert exc_info.value.code is None

    def test_streaming_support(self) -> None:
        """Test that service supports streaming responses.

        Streaming is handled by the parent Pipecat OpenAILLMService,
        so we just verify the service is properly configured.
        """
        service = OpenAILLMService(api_key="test-key")

        # Verify service inherits from streaming-capable parent
        assert hasattr(service, "process_frame")
        assert hasattr(service, "get_chat_completions")

    def test_function_calling_support(self) -> None:
        """Test that service supports function calling.

        Function calling is handled by registering functions with
        the parent class using register_function method.
        """
        service = OpenAILLMService(api_key="test-key")

        # Verify function calling methods are available
        assert hasattr(service, "register_function")
        assert hasattr(service, "unregister_function")
        assert hasattr(service, "has_function")
        assert hasattr(service, "register_direct_function")
