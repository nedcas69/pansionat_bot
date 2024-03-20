from datetime import date

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Пансионат бандлигини кўриш.'),
        ],
        [
            KeyboardButton('Буюртмани рақами бўйича текшириш.'),
        ],
        [
            KeyboardButton('Буюртмани рақами бўйича ўзгартириш.'),
        ],
        [
            KeyboardButton('Янги буюртма қилиш.')
        ]

    ],
    resize_keyboard=True
)

month_adm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'Январ'),
            KeyboardButton(text=f'Феврал')
        ],
        [
            KeyboardButton(text=f'Март'),
            KeyboardButton(text=f'Апрел')
        ],
        [
            KeyboardButton(text=f'Май'),
            KeyboardButton(text=f'Июн')
        ],
        [
            KeyboardButton(text=f'Июл'),
            KeyboardButton(text=f'Август')
        ],
        [
            KeyboardButton(text=f'Сентябр'),
            KeyboardButton(text=f'Октябр')
        ],
        [
            KeyboardButton(text=f'Ноябр'),
            KeyboardButton(text=f'Декабр')
        ],
        [
            KeyboardButton(text='Бекор қилиш ❌')
        ],

    ],
    resize_keyboard=True,
)


year_now = date.today()
years_adm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'{year_now.year}'),
            KeyboardButton(text=f'{int(year_now.year) + 1}'),
        ],
        [
            KeyboardButton(text='Бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

res = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Тўлов холатини ўзгартириш.')
        ],
        [
            KeyboardButton(text='Бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

pay_change = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Тўлов қилиш.')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


