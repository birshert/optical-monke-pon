import functools
from contextlib import contextmanager

from loguru import logger

from utils.logs.bot_logger import __init_logs__ as __init_bot_logs__
from utils.logs.bot_logger import get_logger as get_bot_logger
from utils.logs.model_logger import __init_logs__ as __init_model_logs__
from utils.logs.model_logger import get_logger as get_model_logger


def log_function(current_logger, message: str = None, level: str = "INFO"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            current_logger.opt(depth=1).log(level, "[START] '{}' - [{}]", name, message)

            result = func(*args, **kwargs)

            current_logger.opt(depth=1).log(level, "[END] '{}' - [{}]", name, message)

            return result

        return wrapped

    return wrapper


@contextmanager
def log_block(current_logger, message: str = None, level: str = "INFO"):
    current_logger.opt(depth=2).log(level, "[START] - [{}]", message)
    yield
    current_logger.opt(depth=2).log(level, "[END] - [{}]", message)


if __name__ == "__main__":
    logger.debug("сообщение для отладки")
    logger.info("информационное сообщение")
    logger.warning("предупреждающее сообщение")
    logger.error("сообщение об ошибке")
    logger.critical("сообщение о критической ошибке")
