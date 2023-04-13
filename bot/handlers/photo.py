import asyncio
import base64
import os

import aiohttp
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.logs import get_bot_logger
from utils.paths import images_path

logger = get_bot_logger()
router = Router()


@router.message(F.photo)
async def incoming_photo(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    logger.info(f"Got photo from {user_id}")

    user_images_path = os.path.join(images_path, f"{user_id}")
    os.makedirs(user_images_path, exist_ok=True)

    image = message.photo[-1]
    image_file = await bot.get_file(image.file_id)
    file = await bot.download_file(image_file.file_path)

    base64_encoded_data = base64.b64encode(file.read())
    base64_message = base64_encoded_data.decode('utf-8')

    async with aiohttp.request(
            method="post",
            url="http://0.0.0.0:5000/predictions",
            json={"input": {"image": f"data:image/png;base64,{base64_message}"}}
    ) as model_prediction:
        model_prediction = await model_prediction.json()
        logger.info(f"Got prediction for {user_id}: {model_prediction}")
        await message.reply(model_prediction["output"])

    await asyncio.sleep(0.5)
