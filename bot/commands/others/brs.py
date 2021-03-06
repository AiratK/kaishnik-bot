from aiogram.types import Message
from aiogram.types import ChatType

from bot import dispatcher
from bot import guards

from bot.commands.others.utilities.constants import BRS

from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Commands.BRS.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Commands.BRS.value ]
)
@increment_command_metrics(command=Commands.BRS)
async def brs(message: Message):
    await message.answer(
        text=BRS,
        parse_mode="markdown"
    )
