from dataclasses import dataclass, field

from .utils import get_logging_config


@dataclass(slots=True, frozen=True, kw_only=True)
class LoggingConfig:
    """Logging configuration."""
    dict_config: dict = field(default_factory=get_logging_config)
