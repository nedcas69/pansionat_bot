from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot


class IsAdm(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        admin_types = [562847836, 479467128]
        if user_id in admin_types:
            return True
