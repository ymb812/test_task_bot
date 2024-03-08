from core.database.models import Category, SubCategory
from aiogram_dialog import DialogManager

async def get_categories(dialog_manager: DialogManager, **kwargs):
    return {'categories': await Category.all()}

async def get_subcategories(dialog_manager: DialogManager, **kwargs):
    return {
        'subcategories': await SubCategory.filter(parent_category_id=dialog_manager.dialog_data['category_id']).all()
    }
