from aiogram.dispatcher.filters.state import StatesGroup, State


class not_work_uz(StatesGroup):
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype = State()
    tel = State()
    cat_room = State()


class uz_regis(StatesGroup):
    work = State()
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype = State()
    tel = State()
    telx = State()
    cat_room = State()


class work_pen_uz(StatesGroup):
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype = State()
    tel = State()
    cat_room = State()