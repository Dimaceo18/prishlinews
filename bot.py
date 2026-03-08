import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

welcome_text = '''
Добро пожаловать в ЧАТ-БОТ канала «Minsk News»!
С помощью бота Вы можете отправить информацию о ЧП, ДТП, важном событии или другой ситуации, которая может быть полезна жителям города.
'''

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📩 Предложить новость"),
            KeyboardButton(text="📸 Отправить фото / видео")
        ],
        [
            KeyboardButton(text="✉️ Связь с редакцией"),
            KeyboardButton(text="💼 Реклама и сотрудничество")
        ]
    ],
    resize_keyboard=True
)

back_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Назад в меню")]],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(welcome_text, reply_markup=menu)


@dp.message(F.text == "⬅️ Назад в меню")
async def back(message: Message):
    await message.answer("Главное меню:", reply_markup=menu)


@dp.message(F.text == "📩 Предложить новость")
async def news(message: Message):
    await message.answer(
        "Напишите текст новости и отправьте сообщение.",
        reply_markup=back_menu
    )


@dp.message(F.text == "📸 Отправить фото / видео")
async def photo_video(message: Message):
    await message.answer(
        "Отправьте фото или видео с места события.",
        reply_markup=back_menu
    )


@dp.message(F.text == "✉️ Связь с редакцией")
async def editor(message: Message):
    await message.answer(
        "Напишите сообщение для редакции.",
        reply_markup=back_menu
    )


@dp.message(F.text == "💼 Реклама и сотрудничество")
async def ads(message: Message):
    await message.answer(
        "Напишите сообщение по рекламе и сотрудничеству.",
        reply_markup=back_menu
    )


@dp.message()
async def forward_to_admin(message: Message):
    user = message.from_user

    caption = f"""
📩 Новое сообщение в предложке

👤 Пользователь: {user.first_name}
🆔 ID: {user.id}
"""

    await bot.send_message(ADMIN_CHAT_ID, caption)

    await message.copy_to(ADMIN_CHAT_ID)

    await message.answer("Спасибо! Сообщение отправлено редакции.", reply_markup=menu)


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
