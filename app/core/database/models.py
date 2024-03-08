import logging
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
    name = fields.CharField(max_length=32, null=True)


class SubCategory(Model):
    class Meta:
        table = 'subcategories'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=32, null=True)
    parent_category = fields.ForeignKeyField(model_name='models.Category', to_field='id', null=True)


class Product(Model):
    class Meta:
        table = 'products'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=32, null=True)
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
        item = await cls.filter(product_id=product_id, user_id=user_id).first()
        if item:
            item.amount = expressions.F('amount') + amount
            await item.save()
        else:
            item = await cls.create(product_id=product_id, user_id=user_id, amount=amount)

        return item


class Order(Model):
    class Meta:
        table = 'orders'

    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', to_field='user_id')
    is_approved = fields.BooleanField(default=None, null=True)
    price = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
