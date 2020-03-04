from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import students
from bot import metrics

from bot.commands.login.utilities.keyboards import login_way_chooser

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.callback_query_handler(
    lambda callback: (
            students[callback.message.chat.id].guard.text == Commands.START.value or
            students[callback.message.chat.id].guard.text == Commands.SETTINGS.value
        ) and callback.data == Commands.LOGIN.value
)
@metrics.increment(Commands.LOGIN)
@top_notification
async def login(callback: CallbackQuery):
    # Cleanning the chat
    await callback.message.delete()
    if students[callback.message.chat.id].guard.text == Commands.START.value: await students[callback.message.chat.id].guard.message.delete()
    
    await callback.message.answer(
        text=(
            "{warning}"
            "Студенческий билет и зачётка имеют одинаковый номер😉\n\n"
            "Выбери желаемый путь настройки:"
        ).format(
            # Showing the warning to the old users
            warning="Все текущие данные, включая *заметки* и *изменённое расписание*, будут стёрты.\n\n" if students[callback.message.chat.id].is_setup else ""
        ),
        parse_mode="markdown",
        reply_markup=login_way_chooser(is_old=students[callback.message.chat.id].is_setup)
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN.value
