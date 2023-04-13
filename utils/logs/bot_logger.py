from loguru import logger


def get_logger():
    return logger.bind(task="bot")


def __init_logs__():
    logger.add(
        "artifacts/logs/bot/{time:YYYY-MM-DD_HH:mm:ss}.log",
        enqueue=True,
        filter=lambda x: x["extra"]["task"] == "bot",
    )
