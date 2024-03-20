from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

lang_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Ўзбекча 🇺🇿'),
        ],
        [
            KeyboardButton('Русский 🇷🇺')
        ]

    ],
    resize_keyboard=True
)