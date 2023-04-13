from loguru import logger


def get_logger():
    return logger.bind(task="model")


def __init_logs__():
    logger.add(
        "artifacts/logs/train/{time:YYYY-MM-DD_HH:mm:ss}.log",
        enqueue=True,
        filter=lambda x: x["extra"]["task"] == "model",
    )
