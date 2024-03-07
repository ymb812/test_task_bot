from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.texts import _


def confirm_kb(user_id: int, task_id: int | None = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('APPROVE_BUTTON'), callback_data=f'approve_task_{task_id}-user_{user_id}')
    kb.button(text=_('REJECT_BUTTON'), callback_data=f'reject_task_{task_id}-user_{user_id}')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def tasks_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('TASKS_BUTTON'), callback_data=f'missed_tasks')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def start_task_kb(task_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('START_TASK_BUTTON'), callback_data=f'start_task_{task_id}')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def json_task_kb(buttons: list[str], task_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for button in buttons:
        kb.button(text=button, callback_data=f'{button}_{task_id}')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def support_answer_kb(link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('SUPPORT_ANSWER_BUTTON'), url=link)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def mailing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('MAILING_BUTTON'), callback_data='start_mailing')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
