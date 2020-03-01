from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import dispatcher

from bot import students
from bot import metrics

from bot.shared.helpers import top_notification
from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message: message.chat.id in students,
    commands=[ Commands.CANCEL.value ]
)
@metrics.increment(Commands.CANCEL)
async def cancel_on_command(message: Message):
    if students[message.chat.id].guard.text is None:
        await message.answer(text="Запущенных команд нет. Отправь какую-нибудь☺️")
        return
    
    students[message.chat.id].guard.drop()
    
    await message.answer(text="Отменено!")

@dispatcher.callback_query_handler(
    lambda callback:
        callback.message.chat.id in students and
        callback.data == Commands.CANCEL.value
)
@top_notification
async def cancel_on_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    await cancel_on_command(callback.message)
