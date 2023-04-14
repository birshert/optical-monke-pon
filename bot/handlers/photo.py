import base64
import random
from io import BytesIO

import aiohttp
from PIL import Image
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.config import config
from utils.logs import get_bot_logger

logger = get_bot_logger()
router = Router()


@router.message(F.photo)
async def incoming_photo(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    logger.info(f"Got photo from {user_id}")

    image = message.photo[-1]
    image_file = await bot.get_file(image.file_id)
    file = await bot.download_file(image_file.file_path)

    price = 300

    if config.deploy.deploy_type == "cog":
        base64_encoded_data = base64.b64encode(file.read())
        base64_message = base64_encoded_data.decode('utf-8')

        async with aiohttp.request(
                method="post",
                url=f"http://localhost:5000/predictions",
                json={"input": {"image": f"data:image/png;base64,{base64_message}"}}
        ) as model_prediction:
            model_prediction = await model_prediction.json()
            logger.info(f"Got prediction for {user_id}: {model_prediction}")
            price = model_prediction["output"]
    elif config.deploy.deploy_type == "fast_api":
        async with aiohttp.request(
                method="post",
                url=f"http://localhost:5000/predict",
                data={"file": file}
        ) as model_prediction:
            model_prediction = await model_prediction.json()
            logger.info(f"Got prediction for {user_id}: {model_prediction}")
            price = model_prediction["price"]

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Сгенерировать похожие картины", callback_data=image_file.file_path)
    )

    if random.random() < 0.5:
        await message.answer_photo(
            photo=FSInputFile("bot/handlers/gachi.jpeg", filename="gachi.jpeg"),
            caption=f"По нашим оценкам картина стоит $300",
            reply_markup=keyboard.as_markup()
        )
    else:
        price_10_percent = price / 10
        price_lower = int((price - price_10_percent) // 100) * 100
        price_upper = int((price + price_10_percent) // 100) * 100

        await message.answer(
            f"По нашим оценкам картина стоит около ${price_lower}-{price_upper}",
            reply_markup=keyboard.as_markup()
        )

        if price < 5000:
            await bot.send_video_note(message.chat.id, video_note=FSInputFile('bot/handlers/video/stalker.mp4'))
        elif 5000 <= price <= 13000:
            await bot.send_video_note(message.chat.id, video_note=FSInputFile('bot/handlers/video/bloodseeker.mp4'))
        else:
            await bot.send_video_note(message.chat.id, video_note=FSInputFile('bot/handlers/video/pudge.mp4'))


@router.callback_query()
async def process_generate(query: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = query.from_user.id
    message = query.message
    file = query.data

    file = await bot.download_file(file)

    logger.info(f"Starting art variations for {user_id}")

    async with aiohttp.request(
            method="post",
            url=f"http://localhost:5000/variate",
            data={"file": file}
    ) as response:
        if response.status != 200:
            await message.answer("Не удалось сгенерировать вариации ;(")

        images = Image.open(BytesIO(await response.content.read()))

        width, height = images.size

        part_height = height // 5

        contents = []

        for i in range(5):
            top = i * part_height
            bottom = (i + 1) * part_height

            part = images.crop((0, top, width, bottom))

            part.save(f"part_{i + 1}.png")

            contents.append(
                InputMediaPhoto(
                    media=FSInputFile(f"part_{i + 1}.png", filename=f"part_{i + 1}.png")
                )
            )
        contents[0].caption = "Сгенерировали вариации вашей картины, они бесценны"
        await message.answer_media_group(contents)

    logger.info(f"Ending art variations for {user_id}")
