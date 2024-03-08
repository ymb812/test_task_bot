from aiogram.fsm.state import State, StatesGroup


class CatalogStateGroup(StatesGroup):
    categories = State()
    subcategories = State()
    products = State()
    product_interaction = State()
