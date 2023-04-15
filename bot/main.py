import os
from asyncio import run
from warnings import filterwarnings

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from torch.multiprocessing import set_start_method

from bot.handlers import base_commands
from bot.handlers import photo
from utils.logs import __init_bot_logs__
from utils.logs import get_bot_logger

filterwarnings("ignore")

logger = get_bot_logger()


async def main():
    __init_bot_logs__()

    bot = Bot(token=os.environ.get("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.GLOBAL_USER)

    dp.include_router(base_commands.router)
    dp.include_router(photo.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать работу"),
            BotCommand(command="i_wanna_random_monkey_sticker", description="Отправим вам стикер с бибзяной"),
            BotCommand(command="pon", description="пон")
        ]
    )
    logger.info("Starting bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    set_start_method("spawn", force=True)
    run(main())
