from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType

from bot import dispatcher
from bot import students

from bot.commands.login.menu import finish_login
from bot.commands.login.utilities.keyboards import againer
from bot.commands.login.utilities.keyboards import guess_approver

from bot.shared.keyboards import canceler
from bot.shared.helpers import top_notification
from bot.shared.constants import BOT_ADDRESSING
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.student import Student
from bot.shared.commands import Commands

from random import choice
from re import Match
from re import search


@dispatcher.callback_query_handler(
    lambda callback:
        callback.message.chat.type != ChatType.PRIVATE and
        students[callback.message.chat.id].guard.text == Commands.LOGIN.value and
        callback.data == Commands.LOGIN_COMPACT.value
)
@top_notification
async def login_compact_guess_group(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id] = Student()  # Resetting user
    students[callback.message.chat.id].type = Student.Type.GROUP_CHAT
    
    guess: Match = search("[0-9][0-9][0-9][0-9][0-9]?[0-9]?", callback.message.chat.title)
    
    if guess is not None:
        students[callback.message.chat.id].group = guess.group()
    
    # If the guess was unsuccessful, go the usual login way (including user reset)
    if students[callback.message.chat.id].group_schedule_id is None:
        await login_compact(callback=callback)
        return
    
    await callback.message.edit_text(
        text="*{possible_group}* — это твоя группа, верно?".format(possible_group=guess.group()),
        reply_markup=guess_approver(),
        parse_mode="markdown"
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_COMPACT.value
    students[callback.message.chat.id].guard.message = callback.message

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LOGIN_COMPACT.value and
        callback.data == Commands.LOGIN_CORRECT_GROUP_GUESS.value
)
@top_notification
async def finish_login_compact_with_correct_group_guess(callback: CallbackQuery):
    await finish_login(message=callback.message)


@dispatcher.callback_query_handler(
    lambda callback: (
            students[callback.message.chat.id].guard.text == Commands.LOGIN.value and
            callback.data == Commands.LOGIN_COMPACT.value
        ) or (
            students[callback.message.chat.id].guard.text == Commands.LOGIN_COMPACT.value and
            callback.data == Commands.LOGIN_WRONG_GROUP_GUESS.value
        )
)
@top_notification
async def login_compact(callback: CallbackQuery):
    students[callback.message.chat.id] = Student()  # Resetting user
    students[callback.message.chat.id].type = Student.Type.COMPACT if callback.message.chat.type == ChatType.PRIVATE else Student.Type.GROUP_CHAT
    
    guard_message: Message = await callback.message.edit_text(
        text="Отправь номер своей группы.",
        reply_markup=canceler()
    )
    
    students[callback.message.chat.id].guard.text = Commands.LOGIN_COMPACT.value
    students[callback.message.chat.id].guard.message = guard_message

@dispatcher.message_handler(
    lambda message:
        message.chat.type != ChatType.PRIVATE and (
            message.text is not None and message.text.startswith(BOT_ADDRESSING) or
            message.reply_to_message is not None and message.reply_to_message.from_user.is_bot
        ) and students[message.chat.id].guard.text == Commands.LOGIN_COMPACT.value
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        students[message.chat.id].guard.text == Commands.LOGIN_COMPACT.value
)
async def set_group(message: Message):
    # Getting rid of the bot addressing
    if message.chat.type != ChatType.PRIVATE: message.text = message.text.replace(BOT_ADDRESSING, "")
    
    await message.delete()
    await students[message.chat.id].guard.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[message.chat.id].group = message.text
    
    if students[message.chat.id].group_schedule_id is None:
        await students[message.chat.id].guard.message.edit_text(
            text=ResponseError.NO_GROUP.value,
            reply_markup=againer(),
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        students[message.chat.id].guard.text = Commands.LOGIN.value  # Return to /login after the data drop
        return
    
    await finish_login(message=message)
