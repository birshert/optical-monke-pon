import asyncio
import os

from PIL import Image
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.logs import get_bot_logger
from utils.paths import images_path

logger = get_bot_logger()
router = Router()


def save_image(image, path):
    images_count = len(os.listdir(path))
    image_path = os.path.join(path, f"{images_count + 1:>04}.png")

    image.save(image_path)
    logger.info(f"Downloaded image: {image_path}")


@router.message(F.photo)
async def incoming_photo(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    user_images_path = os.path.join(images_path, f"{user_id}")
    os.makedirs(user_images_path, exist_ok=True)

    image = message.photo[-1]
    image_file = await bot.get_file(image.file_id)
    file = await bot.download_file(image_file.file_path)

    img = Image.open(file)

    save_image(img, user_images_path)

    await asyncio.sleep(0.5)

    await message.reply("Фотография загружена")
