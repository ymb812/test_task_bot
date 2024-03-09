import logging
from aiogram import types, Router
from core.utils.texts import _


logger = logging.getLogger(__name__)
router = Router(name='Inline-mode router')


@router.inline_query()
async def show_faq(inline_query: types.InlineQuery):
    results = []
    questions = _('QUESTIONS').split('\n\n')
    answers = _('ANSWERS').split('\n\n')

    for i, answer in enumerate(answers):
        results.append(types.InlineQueryResultArticle(
            id=str(i),
            title=questions[i],
            input_message_content=types.InputTextMessageContent(
                message_text=answer,
                parse_mode='HTML',
            )
        ))

    await inline_query.answer(results, is_personal=True, cache_time=10)
