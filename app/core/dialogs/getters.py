import math
from aiogram.enums import ContentType
from core.database.models import Category, SubCategory, Product, UserProduct
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment


async def get_categories(dialog_manager: DialogManager, **kwargs) -> dict[str, list[Category]]:
    return {
        'categories': await Category.all()
    }


async def get_subcategories(dialog_manager: DialogManager, **kwargs) -> dict[str, list[SubCategory]]:
    return {
        'subcategories': await SubCategory.filter(parent_category_id=dialog_manager.dialog_data['category_id']).all()
    }


async def get_products_by_subcategory(dialog_manager: DialogManager, **kwargs) -> dict[str, list[Product]]:
    return {
        'products': await Product.filter(parent_category_id=dialog_manager.dialog_data['subcategory_id']).all()
    }


async def get_product_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Product | MediaAttachment | int]:
    data = dialog_manager.dialog_data
    product = await Product.get(id=data['product_id'])

    media_content = None
    if product.media_content:
        media_content = MediaAttachment(ContentType.PHOTO, url=product.media_content)

    # handle confirm
    product_amount = 0
    if data.get('product_amount'):
        product_amount = int(data['product_amount'])

    return {
        'product': product,
        'media_content': media_content,
        'product_amount': product_amount,
        'total_price': math.ceil(product_amount * product.price)
    }


async def get_products_by_user(**kwargs) -> dict[str, list[UserProduct]]:
    user_id = kwargs['event_from_user'].id
    products = await UserProduct.get_user_cart(user_id=user_id)

    return {
        'products': products
    }


async def get_order_data(dialog_manager: DialogManager, **kwargs) -> dict[str, int]:
    user_id = kwargs['event_from_user'].id
    user_products: list[UserProduct] = await UserProduct.get_user_cart(user_id=user_id, return_products=False)

    product_amount, total_price = 0, 0
    for user_product in user_products:
        product_amount += user_product.amount
        total_price += (await user_product.product).price * user_product.amount

    dialog_manager.dialog_data['total_price'] = math.ceil(total_price)
    dialog_manager.dialog_data['product_amount'] = product_amount

    return {
        'product_types_amount': len(user_products),
        'product_amount': product_amount,
        'total_price': math.ceil(total_price)
    }
