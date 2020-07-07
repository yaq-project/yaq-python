__all__ = [
    "DEBUG",
    "INFO",
    "NOTICE",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "ALERT",
    "EMERGENCY",
    "getLogger",
    "name_to_level",
    "setLevel",
]

import logging


# Log levels as defined by sd-daemon(3)
DEBUG = logging.DEBUG
INFO = logging.INFO
NOTICE = logging.INFO + 5
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
ALERT = logging.CRITICAL + 10
EMERGENCY = logging.CRITICAL + 20

name_to_level = {
    "debug": DEBUG,
    "info": INFO,
    "notice": NOTICE,
    "warning": WARNING,
    "error": ERROR,
    "critical": INFO,
    "alert": ALERT,
    "emergency": EMERGENCY,
}

# Rename levels to start with numeric prefix following syslog convention
logging.addLevelName(DEBUG, "<7> DEBUG")
logging.addLevelName(INFO, "<6> INFO")
logging.addLevelName(NOTICE, "<5> NOTICE")
logging.addLevelName(WARNING, "<4> WARNING")
logging.addLevelName(ERROR, "<3> ERR")
logging.addLevelName(CRITICAL, "<2> CRIT")
logging.addLevelName(ALERT, "<1> ALERT")
logging.addLevelName(EMERGENCY, "<0> EMERG")

formatter = logging.Formatter(
    "{levelname} : {asctime} : {name} : {message}",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    style="{",
)

_loggers = []
_default_level = logging.INFO


def getLogger(name=None):
    """Wrapper of `logging.getLogger` which sets the default formatter."""
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(_default_level)
        _loggers.append(logger)
    return logger


def setLevel(level):
    global _default_level
    _default_level = level
    for log in _loggers:
        log.setLevel(level)
