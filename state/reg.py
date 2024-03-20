from aiogram.dispatcher.filters.state import StatesGroup, State


class regis(StatesGroup):
    work = State()
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype= State()
    tel = State()
    telx = State()
    cat_room = State()


class not_work(StatesGroup):
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype = State()
    tel = State()
    cat_room = State()


class work_pen(StatesGroup):
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype = State()
    tel = State()
    cat_room = State()



