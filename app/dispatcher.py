import logging
from aiogram import Bot, types
from aiogram.utils.i18n import I18n
from core.database.models import User
from settings import settings


logger = logging.getLogger(__name__)
bot = Bot(settings.bot_token.get_secret_value(), parse_mode='HTML')
i18n = I18n(path='locales', default_locale='ru', domain='messages')
i18n.set_current(i18n)


class Dispatcher(object):
    @staticmethod
    async def __send_mailing_msg_to_user(user_id: int, message: types.Message, bot: Bot):
        if message.photo:
            await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)

        elif message.text:
            await bot.send_message(chat_id=user_id, text=message.text)


    @classmethod
    async def send_content_to_users(cls, bot: Bot, message: types.Message | None = None):
        sent_amount = 0

        users_ids = await User.all()
        if not users_ids:
            return sent_amount

        for i in range(0, len(users_ids), settings.mailing_batch_size):
            user_batch = users_ids[i:i + settings.mailing_batch_size]
            for user in user_batch:
                # send admin mailing
                try:
                    await cls.__send_mailing_msg_to_user(user_id=user.user_id, message=message, bot=bot)
                    sent_amount += 1
                except Exception as e:
                    logger.error(f'Error in mailing to all users, user_id={user.user_id}', exc_info=e)

        return sent_amount
