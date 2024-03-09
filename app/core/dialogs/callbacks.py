import uuid
from aiogram.types import CallbackQuery, Message, LabeledPrice
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from core.states.dialogs import CatalogStateGroup, CartStateGroup
from core.database.models import UserProduct, Order
from core.keyboards.reply import main_menu_kb
from core.utils.texts import _
from settings import settings


class CallBackHandler:
    __dialog_data_key = ''
    __switch_to_state = None

    @classmethod
    async def selected_content(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):
        # catalog handlers
        if '_category_' in callback.data:
            cls.__dialog_data_key = 'category_id'
            cls.__switch_to_state = CatalogStateGroup.subcategories
        elif '_subcategory_' in callback.data:
            cls.__dialog_data_key = 'subcategory_id'
            cls.__switch_to_state = CatalogStateGroup.products
        elif '_product_' in callback.data:
            cls.__dialog_data_key = 'product_id'
            cls.__switch_to_state = CatalogStateGroup.product_interaction

        # cart handlers
        elif '_products_in_cart_select' in callback.data:
            cls.__dialog_data_key = 'product_id'
            cls.__switch_to_state = CartStateGroup.product_interaction

        dialog_manager.dialog_data[cls.__dialog_data_key] = item_id
        await dialog_manager.switch_to(cls.__switch_to_state)


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
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # add data to db
        data = dialog_manager.dialog_data
        await UserProduct.add_or_update_product_to_the_cart(
            product_id=data['product_id'],
            user_id=callback.from_user.id,
            amount=data['product_amount']
        )

        await callback.message.answer(text=_('PRODUCT_IS_ADDED'))
        await dialog_manager.done()
        await callback.message.answer(text=_('REGISTERED'), reply_markup=main_menu_kb())


    @classmethod
    async def delete_from_cart(
            cls,
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # delete data from db
        data = dialog_manager.dialog_data
        await UserProduct.filter(
            product_id=data['product_id'],
            user_id=callback.from_user.id,
        ).delete()

        await dialog_manager.switch_to(CartStateGroup.products)


    @staticmethod
    async def get_delivery_data(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value,
    ):
        dialog_manager.dialog_data['delivery_data'] = value
        await dialog_manager.switch_to(state=CartStateGroup.payment)


    @staticmethod
    async def order_payment(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        # create order
        data = dialog_manager.dialog_data

        order = await Order.create(
            id=uuid.uuid4(),
            user_id=callback.from_user.id,
            is_paid=False,
            price=data['total_price'],
            product_amount=data['product_amount'],
            delivery_data=data['delivery_data']
        )
        await UserProduct.add_cart_to_order(user_id=callback.from_user.id, order_id=order.id)

        # send invoice
        await dialog_manager.done()
        await dialog_manager.event.bot.send_invoice(
            chat_id=callback.message.chat.id,
            title=_('INVOICE_TITLE', order_id=order.id),
            description=_('INVOICE_DESCRIPTION', delivery_data=data['delivery_data']),
            provider_token=settings.payments_provider_token.get_secret_value(),
            currency='rub',
            prices=[LabeledPrice(label=_('INVOICE_TITLE', order_id=order.id), amount=data['total_price'] * 100)],
            start_parameter=f'{order.id}',
            payload=f'{order.id}'
            )
