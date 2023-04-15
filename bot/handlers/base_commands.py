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


@router.message(Command(commands=["start"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"Started for user {message.from_user.id}")
    await message.answer(
        "Приветствую! Я - бот-оценщик картин. Если вы ищете примерную стоимость своей картины, я готов вам помочь! "
        "Чтобы получить оценку стоимости картины, отправьте её фотографию боту."
        "Кроме того, я могу создать для вас похожие картины с помощью искуственного интеллекта. А еще я умею "
        "поднимать настроение с помощью забавных мемов про обезьян. Давайте начнем!"
    )

    await message.answer("А сейчас мы споем песню про обезьяну")

    await message.answer(text="""
В картинную галерею, вдруг вошла обезьяна,
Она была весела, шумна и задорна.
Она глядела на картины, словно не с этого мира,
И кричала каждый раз, словно была пьяной.

Пон, пон, пон, пон - это ее слово,
Она говорит цену, за каждую картину,
Пон, пон, пон, пон - и все вокруг смеются,
От такой обезьяны, с дикими забавами.

Но обезьяна не слышит, как над ней смеются,
Она продолжает свой путь, смелее и бесстрашней.
Она говорит цену, за каждую картину,
Будто знает толк в искусстве, словно самый гений.

Пон, пон, пон, пон - это ее слово,
Она говорит цену, за каждую картину,
Пон, пон, пон, пон - и все вокруг смеются,
От такой обезьяны, с дикими забавами.

А после всех приключений, с настроением хорошим,
Обезьяна ушла, оставив здесь свои следы.
И люди в галерее, вспоминают этот день,
Как день сумасшедшей обезьяны, которую знают все.

Пон, пон, пон, пон - это ее слово,
Она говорит цену, за каждую картину,
Пон, пон, пон, пон - и все вокруг смеются,
От такой обезьяны, с дикими забавами.
""")


@router.message(Command(commands=["i_wanna_random_monkey_sticker"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"monke user {message.from_user.id}")

    sticker_id = monkey_stickers_ids[randint(0, 9)]

    await message.answer_sticker(sticker=sticker_id)


@router.message(Command(commands=["pon"]))
async def info(message: Message, state: FSMContext):
    logger.info(f"pon user {message.from_user.id}")

    await message.reply(text="пон")

    await message.answer(text="""
В центре салуна веселый ковбой-обезьяна
Танцует и пляшет, словно сама свобода.
Оценщик картин взглядом привлечен ею,
Расценивая ее как произведение искусства своего.

Они наливают стаканы виски до краев,
И поют вместе песню про пони и океан.
Все зовут коварного ковбоя в этом городе,
Но только они знают, как он спасает людей.

И никто не поймет, что счастье его
В том, что он живет, словно вечная игра.
Он мчится верхом на своем коне,
Сияя свободой, которую знает только он сам.
""")
