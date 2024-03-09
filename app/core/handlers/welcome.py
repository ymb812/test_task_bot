import logging
from aiogram import Bot, types, Router, F, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram_dialog import DialogManager, StartMode
from core.utils.texts import set_user_commands, set_admin_commands, _
from core.database.models import User, UserProduct
from core.states.dialogs import CatalogStateGroup, CartStateGroup
from core.keyboards.reply import main_menu_kb
from settings import settings


logger = logging.getLogger(__name__)
router = Router(name='Start router')


@router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()

    # check channel and chat for user
    try:
        await bot.get_chat_member(user_id=message.from_user.id, chat_id=settings.required_chat_id)
        await bot.get_chat_member(user_id=message.from_user.id, chat_id=settings.required_channel_id)
    except exceptions.TelegramBadRequest:
        logger.info(f'user_id={message.from_user.id} is not in the chat')
        chat_link = await bot.create_chat_invite_link(chat_id=settings.required_chat_id)
        channel_link = await bot.create_chat_invite_link(chat_id=settings.required_channel_id)
        await message.answer(
            text=_('NOT_FOLLOWED', channel_link=chat_link.invite_link, chat_link=channel_link.invite_link)
        )
        return

    # add basic info to db
    await User.update_data(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium,
    )

    user = await User.get(user_id=message.from_user.id)
    await set_user_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
    if user.status == 'admin':
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))

    await message.answer(text=_('REGISTERED'), reply_markup=main_menu_kb())


@router.message(F.text == '📋 Каталог', StateFilter(None))
async def catalog(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=CatalogStateGroup.categories, mode=StartMode.RESET_STACK)


@router.message(F.text == '📦 Корзина', StateFilter(None))
async def cart(message: types.Message, dialog_manager: DialogManager):
    products = await UserProduct.get_user_cart(user_id=message.from_user.id)
    if products:
        await dialog_manager.start(state=CartStateGroup.products, mode=StartMode.RESET_STACK)
    else:
        await message.answer(text=_('CART_IS_EMPTY'), reply_markup=main_menu_kb())


@router.message(F.text == '❓ Часто задаваемые вопросы', StateFilter(None))
async def FAQ(message: types.Message, bot: Bot, state: FSMContext):
    pass
