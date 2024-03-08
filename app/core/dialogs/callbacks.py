from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from core.states.dialogs import CatalogStateGroup
from core.database.models import UserProduct
from core.keyboards.reply import main_menu_kb
from core.utils.texts import _


class CallBackHandler:
    __dialog_data_key = ''
    __switch_to_state = None

    @classmethod
    async def selected_content(
            cls,
            callback_query: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):

        if '_category_' in callback_query.data:
            cls.__dialog_data_key = 'category_id'
            cls.__switch_to_state = CatalogStateGroup.subcategories
        elif '_subcategory_' in callback_query.data:
            cls.__dialog_data_key = 'subcategory_id'
            cls.__switch_to_state = CatalogStateGroup.products
        elif '_product' in callback_query.data:
            cls.__dialog_data_key = 'product_id'
            cls.__switch_to_state = CatalogStateGroup.product_interaction

        dialog_manager.dialog_data[cls.__dialog_data_key] = item_id
        await dialog_manager.switch_to(cls.__switch_to_state)


    @classmethod
    async def product_to_cart(
            cls,
            callback_query: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        await dialog_manager.switch_to(CatalogStateGroup.product_amount)


    @staticmethod
    async def entered_product_amount(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        value: str
        if value.isdigit():
            dialog_manager.dialog_data['product_amount'] = value
            await dialog_manager.switch_to(state=CatalogStateGroup.product_confirm)


    @staticmethod
    async def product_confirm_and_end(
            callback_query: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # add data to db
        data = dialog_manager.dialog_data
        await UserProduct.add_or_update_product_to_the_cart(
            product_id=data['product_id'],
            user_id=callback_query.from_user.id,
            amount=data['product_amount']
        )

        await callback_query.message.answer(text=_('PRODUCT_IS_ADDED'))
        await dialog_manager.done()
        await callback_query.message.answer(text=_('REGISTERED'), reply_markup=main_menu_kb())
