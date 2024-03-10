import logging
import uuid
from datetime import datetime
from tortoise import fields, expressions
from tortoise.models import Model

logger = logging.getLogger(__name__)


class User(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']

    user_id = fields.BigIntField(pk=True, index=True)
    username = fields.CharField(max_length=32, index=True, null=True)
    status = fields.CharField(max_length=32, null=True)  # admin
    first_name = fields.CharField(max_length=64)
    last_name = fields.CharField(max_length=64, null=True)
    language_code = fields.CharField(max_length=2, null=True)
    is_premium = fields.BooleanField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @classmethod
    async def update_data(cls, user_id: int, first_name: str, last_name: str, username: str, language_code: str,
                          is_premium: bool):
        user = await cls.filter(user_id=user_id).first()
        if user is None:
            await cls.create(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                language_code=language_code,
                is_premium=is_premium,
            )
        else:
            await cls.filter(user_id=user_id).update(
                first_name=first_name,
                last_name=last_name,
                username=username,
                language_code=language_code,
                is_premium=is_premium,
                updated_at=datetime.now()
            )

    @classmethod
    async def set_status(cls, user_id: int, status: str | None):
        await cls.filter(user_id=user_id).update(status=status)


class Category(Model):
    class Meta:
        table = 'categories'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=32)


class SubCategory(Model):
    class Meta:
        table = 'subcategories'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=32)
    parent_category = fields.ForeignKeyField(model_name='models.Category', to_field='id', null=True)


class Product(Model):
    class Meta:
        table = 'products'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=32)
    description = fields.CharField(max_length=1024)
    price = fields.IntField()
    media_content = fields.CharField(max_length=256, null=True)
    parent_category = fields.ForeignKeyField(model_name='models.SubCategory', to_field='id', null=True)


class UserProduct(Model):
    class Meta:
        table = 'products_by_users'

    product = fields.ForeignKeyField('models.Product', to_field='id')
    user = fields.ForeignKeyField('models.User', to_field='user_id')
    amount = fields.IntField()
    order = fields.ForeignKeyField('models.Order', to_field='id', null=True)

    @classmethod
    async def add_or_update_product_to_the_cart(cls, product_id: int, user_id: int, amount: int) -> "UserProduct":
        item = await cls.filter(product_id=product_id, user_id=user_id, order_id=None).first()
        if item:
            item.amount = expressions.F('amount') + amount
            await item.save()
        else:
            item = await cls.create(product_id=product_id, user_id=user_id, amount=amount)

        return item


    # return Product for cart display or return UserProduct for order creating
    @classmethod
    async def get_user_cart(cls, user_id: int, return_products: bool = True) -> list[Product or "UserProduct"]:
        if return_products:
            return [await product.product for product in await cls.filter(user_id=user_id, order_id=None).all()]

        return [product for product in await cls.filter(user_id=user_id, order_id=None).all()]


    @classmethod
    async def add_cart_to_order(cls, user_id: int, order_id: uuid.UUID):
        for product in await UserProduct.filter(user_id=user_id, order_id=None).all():
            product.order_id = order_id
            await product.save()


class Order(Model):
    class Meta:
        table = 'orders'

    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', to_field='user_id')
    is_paid = fields.BooleanField(default=False)
    price = fields.IntField()
    product_amount = fields.IntField()
    delivery_data = fields.CharField(max_length=256)
    created_at = fields.DatetimeField(auto_now_add=True)


class Dispatcher(Model):
    class Meta:
        table = 'mailings'
        ordering = ['id']

    id = fields.BigIntField(pk=True)
    post = fields.ForeignKeyField('models.Post', to_field='id')
    send_at = fields.DatetimeField()


class Post(Model):
    class Meta:
        table = 'mailings_content'

    id = fields.BigIntField(pk=True)
    text = fields.CharField(max_length=256, null=True)
    photo_file_id = fields.CharField(max_length=256, null=True)
    video_file_id = fields.CharField(max_length=256, null=True)
    sticker_file_id = fields.CharField(max_length=256, null=True)
    photo_filename = fields.CharField(max_length=256, null=True)
    video_filename = fields.CharField(max_length=256, null=True)
    sticker_filename = fields.CharField(max_length=256, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)


    @classmethod
    async def get_posts_by_scenario(cls, scenario_id: int):
        return await cls.filter(id=scenario_id).all()