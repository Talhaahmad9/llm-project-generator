class GeneratorError(Exception):
    """Base class for expected generator failures."""


class UnsupportedProviderError(GeneratorError):
    """The requested provider is not supported."""


class InvalidProjectNameError(GeneratorError):
    """The destination name is not a valid project name."""


class UnsafeDestinationError(GeneratorError):
    """The destination cannot be safely generated."""


class TemplateError(GeneratorError):
    """The packaged template is invalid."""


class GenerationError(GeneratorError):
    """Writing the generated project failed."""
