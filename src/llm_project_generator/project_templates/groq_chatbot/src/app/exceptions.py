class ApplicationError(Exception):
    """Base class for known application failures."""


class LLMError(ApplicationError):
    """Raised when an LLM operation cannot be completed."""