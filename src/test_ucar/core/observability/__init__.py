import logging
import logging.config

from .logging_.configs import LoggingConfig

logger: logging.Logger = logging.getLogger(__name__)


def configure(logging_cfg: LoggingConfig) -> None:
    logging.config.dictConfig(logging_cfg.dict_config)
