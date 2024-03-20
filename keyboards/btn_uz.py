from datetime import date

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\"Узметкомбинат\"АЖ ходими"),
        ],
        [
            KeyboardButton('\"Узметкомбинат\"АЖ пенсионери'),
        ],
        [
            KeyboardButton("\"Узметкомбинат\"АЖ ходими эмасман"),
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],

    ],
    resize_keyboard=True
)

conatct_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Телефон рақамингизни юбориш ☎️', request_contact=True),
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True
)

month_uz = ReplyKeyboardMarkup(
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
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
)

year_now = date.today()
years_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'{year_now.year}'),
            KeyboardButton(text=f'{int(year_now.year) + 1}'),
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

room_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Стандарт'),
            KeyboardButton(text='Люкс'),
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ўзимга 35%')
        ],
        [
            KeyboardButton(text='Оилага 70%')
        ],
        [
            KeyboardButton(text='"Ўзметкомбинат" АЖ пенсионерига 30%')
        ],
        [
            KeyboardButton(text='Дўстга 100%')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_selected_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ўзимга 35%'),
            KeyboardButton(text='Оилага 70%')
        ],
        [
            KeyboardButton(text='"Ўзметкомбинат" АЖ пенсионерига 30%'),

        ],
        [
            KeyboardButton(text='Дўстга 100%'),
        ],
        [
            KeyboardButton(text='Йўлланма буюртма беришни тугатиш'),
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_commerc1_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Йўлланма буюртма беришни тугатиш')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_commerc2_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Йўлланма буюртма бериш')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel_uz = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Буюртмани бекор қилиш ❌')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

pays_uz = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Нақт пулга 💵')
        ],
        [
            KeyboardButton(text='Иш ҳақи ҳисобидан 💵')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

pays_commerc_uz = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Нақт пулга 💵')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)