import os
from applications.core.conf import CONFIG
from applications.core.path_conf import LOG_PATH, ROOT_DIR

SERVER_INFO = CONFIG["server_info"]
API_AUTHENTICATION = SERVER_INFO["api_authentication"]
LOG_CONFIG = CONFIG["log"]

# UVICORN_* is setting for uvicorn server
UVICORN_HOST: str = SERVER_INFO["uvicorn_host"]
UVICORN_PORT: int = SERVER_INFO["uvicorn_port"]
UVICORN_RELOAD: bool = SERVER_INFO["uvicorn_reload"]

SERVICE_NAME: str = LOG_CONFIG["service_name"]
LOG_DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y-%H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG'
        },
        'graypy': {
            'level': 'DEBUG',
            'class': 'graypy.GELFUDPHandler',
            'host': LOG_CONFIG.get("gray_host", "10.10.4.51"),
            'port': LOG_CONFIG.get("gray_port", 5555),
            "facility": LOG_CONFIG.get("gray_facility", "poseidon")
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'api.log'),
            'formatter': 'verbose',
            'backupCount': 10,
        },
        'file_api_resp': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'resp_api.log'),
            'formatter': 'verbose',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
        }

    },
    'loggers': {
        '': {
            'handlers': LOG_CONFIG['main_log_handler'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),

        },
        'api_resp': {
            'handlers': LOG_CONFIG["api_resp_log_handler"],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False
        }
    }
}
