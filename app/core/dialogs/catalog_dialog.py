from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import Back, Button, Select, SwitchTo
from aiogram_dialog.widgets.input import TextInput
from core.dialogs.custom_content import CustomPager
from core.dialogs.getters import get_categories, get_subcategories, get_products_by_subcategory, get_product_data
from core.dialogs.callbacks import CallBackHandler
from core.states.dialogs import CatalogStateGroup
from core.utils.texts import _
from settings import settings


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
        SwitchTo(Const(text=_('ADD_TO_CART')), id='switch_to_amount', state=CatalogStateGroup.product_amount),
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
