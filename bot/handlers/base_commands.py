from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from random import randint

from utils.logs import get_bot_logger

logger = get_bot_logger()

router = Router()


@router.message(Command(commands=["start", "info"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Started for user {message.from_user.id}")
    await message.answer("Добро пожаловать!")
    

@router.message(Command(commands=["I_wanna_random_monkey_sticker"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Meme user {message.from_user.id}")
    
    with open('monkey_stickers_ids.txt') as f:
        monkey_stickers_ids = f.read().split('\n')
    sticker_id = monkey_stickers_ids[randint(0, 9)]
    
    await message.answer_sticker(sticker=sticker_id)
