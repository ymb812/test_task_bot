from aiogram.types import InlineKeyboardButton
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Column, Next, Row, ScrollingGroup, Select, Start
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.getters import get_categories, get_subcategories, get_products_by_subcategory, get_product_data
from core.dialogs.callbacks import CallBackHandler
from core.states.dialogs import CatalogStateGroup
from core.utils.texts import _
from settings import settings


class CustomPager(ScrollingGroup):
    async def _render_page(
            self,
            page: int,
            keyboard: list[list[InlineKeyboardButton]],
    ) -> list[list[InlineKeyboardButton]]:
        pages = self._get_page_count(keyboard)
        last_page = pages - 1
        current_page = min(last_page, page)
        page_offset = current_page * self.height

        return keyboard[page_offset: page_offset + self.height]

    async def _render_pager(
            self,
            pages: int,
            manager: DialogManager,
    ):
        if self.hide_pager:
            return []
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return []

        last_page = pages - 1
        current_page = min(last_page, await self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)

        if current_page == pages - 1:
            next_page = 0
        elif current_page == 0:
            prev_page = pages - 1

        return [
            [
                InlineKeyboardButton(
                    text=_('BACK_PAGER'),
                    callback_data=self._item_callback_data(prev_page),
                ),
                InlineKeyboardButton(
                    text=_('FORWARD_PAGER'),
                    callback_data=self._item_callback_data(next_page),
                ),
            ],
        ]


catalog_dialog = Dialog(
    # categories
    Window(
        Const(text=_('PICK_CATEGORY')),
        CustomPager(
            Select(
                id='_category_select',
                items='categories',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=CallBackHandler.selected_content,
            ),
            id='categories_group',
            height=settings.categories_per_page_height,
            width=settings.categories_per_page_width,
            hide_on_single_page=True,
            hide_pager=False
        ),
        getter=get_categories,
        state=CatalogStateGroup.categories,
    ),

    # subcategories
    Window(
        Const(text=_('PICK_SUBCATEGORY')),
        CustomPager(
            Select(
                id='_subcategory_select',
                items='subcategories',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=CallBackHandler.selected_content,
            ),
            id='subcategories_group',
            height=settings.categories_per_page_height,
            width=settings.categories_per_page_width,
            hide_on_single_page=True,
        ),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_subcategories,
        state=CatalogStateGroup.subcategories,
    ),

    # products
    Window(
        Const(text=_('PICK_PRODUCT')),
        CustomPager(
            Select(
                id='_product_select',
                items='products',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=CallBackHandler.selected_content,
            ),
            id='products_group',
            height=settings.products_per_page_height,
            width=settings.products_per_page_width,
            hide_on_single_page=True,
        ),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_products_by_subcategory,
        state=CatalogStateGroup.products,
    ),

    # products interactions
    Window(
        DynamicMedia(selector='media_content'),
        Format(text=_('PRODUCT_PAGE',
                      product_name='{product.name}',
                      product_description='{product.description}',
                      product_price='{product.price}')
               ),
        Button(Const(text=_('ADD_TO_CART')), id='add_to_cart', on_click=CallBackHandler.product_to_cart),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_product_data,
        state=CatalogStateGroup.product_interaction,
    ),

    # input amount
    Window(
        Const(text=_('INPUT_AMOUNT')),
        TextInput(
            id='product_amount',
            type_factory=str,
            on_success=CallBackHandler.entered_product_amount
        ),
        Back(Const(text=_('BACK_BUTTON'))),
        state=CatalogStateGroup.product_amount,
    ),

    # confirm
    Window(
        DynamicMedia(selector='media_content'),
        Format(text=_('CONFIRM_PRODUCT',
                      product_name='{product.name}',
                      product_amount='{product_amount}',
                      total_price='{total_price}')
               ),
        Button(Const(text=_('CONFIRM_BUTTON')), id='product_confirm', on_click=CallBackHandler.product_confirm_and_end),
        Back(Const(text=_('BACK_BUTTON'))),
        getter=get_product_data,
        state=CatalogStateGroup.product_confirm,
    ),
)
