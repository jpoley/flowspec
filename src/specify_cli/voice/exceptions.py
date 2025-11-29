"""Voice module exceptions."""


class VoiceServiceError(Exception):
    """Base exception for voice service errors."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """Initialize voice service error.

        Args:
            message: Error message
            code: Optional error code from provider
        """
        self.message = message
        self.code = code
        super().__init__(message)


class LLMServiceError(VoiceServiceError):
    """Exception raised when LLM service encounters an error."""

    pass


class STTServiceError(VoiceServiceError):
    """Exception raised when STT service encounters an error."""

    pass


class TTSServiceError(VoiceServiceError):
    """Exception raised when TTS service encounters an error."""

    pass


class ConfigurationError(VoiceServiceError):
    """Exception raised for configuration-related errors."""

    pass
