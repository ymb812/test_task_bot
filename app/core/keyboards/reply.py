from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from core.utils.texts import _


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('MENU_CATALOG_BUTTON'))
    kb.button(text=_('MENU_CART_BUTTON'))
    kb.button(text=_('MY_ORDERS_BUTTON'))
    kb.button(text=_('MENU_FAQ_BUTTON'))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
