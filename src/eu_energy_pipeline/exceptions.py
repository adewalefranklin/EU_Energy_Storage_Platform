class PipelineError(Exception):
    """Base class for exceptions in this module."""

    pass


class ExtractError(PipelineError):
    """Exception raised for errors in the extraction phase."""

    pass


class TransformError(PipelineError):
    """Exception raised for errors in the transformation phase."""

    pass


class LoadError(PipelineError):
    """Exception raised for errors in the loading phase."""

    pass


class ConfigError(PipelineError):
    """Exception raised for errors in the configuration."""

    pass
