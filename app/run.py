import asyncio
import core.middlewares
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from settings import settings
from setup import register
from core.handlers import routers
from aiogram.fsm.storage.redis import RedisStorage


bot = Bot(settings.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))


storage = RedisStorage.from_url(f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_name}')
dp = Dispatcher(storage=storage)
core.middlewares.i18n.setup(dp)


for _r in routers:
    dp.include_router(_r)


async def main():
    async with register():
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
