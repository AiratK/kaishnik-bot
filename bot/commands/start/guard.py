from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import guards

from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text == Commands.START.value
)
async def guard(message: Message):
    await message.delete()
