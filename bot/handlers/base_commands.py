from random import randint

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.logs import get_bot_logger

logger = get_bot_logger()

router = Router()

with open('bot/handlers/monkey_stickers_ids.txt') as f:
    monkey_stickers_ids = f.read().split('\n')


@router.message(Command(commands=["start", "info"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Started for user {message.from_user.id}")
    await message.answer("Добро пожаловать!")


@router.message(Command(commands=["i_wanna_random_monkey_sticker"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"monke user {message.from_user.id}")

    sticker_id = monkey_stickers_ids[randint(0, 9)]

    await message.answer_sticker(sticker=sticker_id)


@router.message(Command(commands=["pon"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"pon user {message.from_user.id}")

    await message.reply(text="пон")
