from aiogram.types import Message
from aiogram.types import CallbackQuery

from bot import dispatcher

from bot.commands.permissions.utilities.helpers import get_bot_member
from bot.commands.permissions.utilities.helpers import check_permissions_in_group_chat_on_command
from bot.commands.permissions.utilities.helpers import check_permissions_in_group_chat_on_callback

from bot.utilities.helpers import top_notification
from bot.utilities.helpers import increment_command_metrics
from bot.utilities.types import Commands


@dispatcher.message_handler(
    check_permissions_in_group_chat_on_command,
    content_types=[ "text" ]
)
@increment_command_metrics(command=Commands.NO_PERMISSIONS)
async def permissions_on_command(message: Message):
    bot_member = await get_bot_member(message=message)
    
    text: str = ""
    
    if not bot_member.is_chat_admin():
        text = "".join([ text, "быть админом" ])
    if not bot_member.can_delete_messages:
        text = ("" if text == "" else " и ").join([ text, "иметь право удалять сообщения" ])
    
    await message.answer(text="".join([
        "Бот должен ", text, ".\n",
        "Это можно изменить в настройках чата.",
    ]))

@dispatcher.callback_query_handler(check_permissions_in_group_chat_on_callback)
@top_notification
async def permissions_on_callback(callback: CallbackQuery):
    await permissions_on_command(callback.message)
