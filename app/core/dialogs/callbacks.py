from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select
from core.states.dialogs import CatalogStateGroup


async def selected_category(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data['category_id'] = item_id
    await dialog_manager.switch_to(CatalogStateGroup.subcategories)


async def selected_subcategory(
    callback_query: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
):
    dialog_manager.dialog_data['subcategory_id'] = item_id
    await dialog_manager.switch_to(CatalogStateGroup.products)
