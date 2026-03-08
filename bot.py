import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()

WELCOME_TEXT = (
    "Добро пожаловать в ЧАТ-БОТ канала «Minsk News»!\n"
    "С помощью бота Вы можете отправить информацию о ЧП, ДТП, важном событии "
    "или другой ситуации, которая может быть полезна жителям города."
)

MAIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📰 Отправить новость / фото / видео")],
        [KeyboardButton(text="✉️ Связь с редакцией")],
        [KeyboardButton(text="💼 Реклама и сотрудничество")],
    ],
    resize_keyboard=True,
)

BACK_MENU = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]],
    resize_keyboard=True,
)

mode = {}


@dp.message(CommandStart())
async def start(message: Message):
    mode[message.from_user.id] = None
    await message.answer(WELCOME_TEXT, reply_markup=MAIN_MENU)


@dp.message(F.text == "⬅️ Назад в меню")
async def back(message: Message):
    mode[message.from_user.id] = None
    await message.answer("Главное меню:", reply_markup=MAIN_MENU)


@dp.message(F.text == "📰 Отправить новость / фото / видео")
async def news(message: Message):
    mode[message.from_user.id] = "Новость"
    await message.answer(
        "Отправьте текст, фото или видео.",
        reply_markup=BACK_MENU
    )


@dp.message(F.text == "✉️ Связь с редакцией")
async def editor(message: Message):
    mode[message.from_user.id] = "Редакция"
    await message.answer(
        "Напишите сообщение для редакции.",
        reply_markup=BACK_MENU
    )


@dp.message(F.text == "💼 Реклама и сотрудничество")
async def ads(message: Message):
    await message.answer(
        "По вопросам рекламы и сотрудничества напишите менеджеру:\n\n@stridiv",
        reply_markup=MAIN_MENU
    )


@dp.message()
async def forward(message: Message):
    if message.from_user.id not in mode or mode[message.from_user.id] is None:
        await message.answer("Пожалуйста выберите раздел в меню.", reply_markup=MAIN_MENU)
        return

    user = message.from_user

    header = (
        f"📩 Новое сообщение\n\n"
        f"Раздел: {mode[user.id]}\n"
        f"Имя: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )

    await bot.send_message(ADMIN_CHAT_ID, header)
    await message.copy_to(ADMIN_CHAT_ID)

    await message.answer(
        "Спасибо. Сообщение отправлено редакции.",
        reply_markup=MAIN_MENU
    )

    mode[user.id] = None


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
