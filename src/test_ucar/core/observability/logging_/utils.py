import os


def get_logging_config(
    log_level: str = os.getenv('APP_LOGGING_LEVEL', default='INFO'),
) -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'text': {
                'format': '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z'
            },
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'text',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'stdout',
                ]
            },
        }
    }
