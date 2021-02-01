from aiogram.types import Message
from aiogram.types import ChatType

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is not None and
        Commands.LOGIN.value in guards[message.chat.id].text
)
async def guard(message: Message):
    await message.delete()