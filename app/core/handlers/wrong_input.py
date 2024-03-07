import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from core.utils.texts import _
from core.keyboards.reply import main_menu_kb


logger = logging.getLogger(__name__)
router = Router(name='Wrong_msg router')


@router.message()
async def wrong_input(message: types.Message, state: FSMContext):
    await message.answer(text=_('WRONG_INPUT'), reply_markup=main_menu_kb())
