from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.texts import _


def mailing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('MAILING_BUTTON'), callback_data='start_mailing')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
