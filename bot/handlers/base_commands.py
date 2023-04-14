from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.logs import get_bot_logger

logger = get_bot_logger()

router = Router()


@router.message(Command(commands=["start", "info"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Started for user {message.from_user.id}")
    await message.answer("Добро пожаловать!")


@router.message(Command(commands=["meme"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Meme user {message.from_user.id}")
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEIlK1kOYMjfpbNqMaupdq0SfakOBeqMwAChxcAAgzwWErywdtxMQ5ycC8E")
