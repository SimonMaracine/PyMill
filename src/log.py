import logging
import colorlog


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 0
        logger.addHandler(_stream_handler)
    return logger


_colors = {
    "DEBUG": "yellow",
    "INFO": "blue",
    "WARNING": "red",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

_formatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s%(reset)s", log_colors=_colors)
_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)

if not __debug__:
    logging.disable()

if __name__ == "__main__":
    logger = get_logger("Test Logger")
    logger.setLevel(logging.DEBUG)

    logger.debug("A quirky message only developers care about")
    logger.info("Curious users might want to know this")
    logger.warning("Something is wrong and any user should be informed")
    logger.error("Serious stuff, this is red for a reason")
    logger.critical("OH NO everything is on fire")
