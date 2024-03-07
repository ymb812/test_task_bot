import logging
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from core.utils.texts import _


logger = logging.getLogger(__name__)
router = Router(name='FAQ router')


@router.message(F.text == '❓ Часто задаваемые вопросы', StateFilter(None))
async def send_rules(message: types.Message):
    await message.answer(text=_('FAQ'))
