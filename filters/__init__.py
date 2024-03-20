from aiogram import Dispatcher
from .admin import IsAdm
from .private_chat import IsPrivate

# Функция которая выполняет установку кастомных фильтров
def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdm)