from typing import List

from aiogram.types import CallbackQuery

from bot import dispatcher
from bot import guards

from bot.commands.locations.utilities.keyboards import libraries_dialer
from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.constants import LIBRARIES
from bot.commands.locations.utilities.types import LocationType

from bot.utilities.helpers import top_notification
from bot.utilities.types import Commands


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOCATIONS.value and
        callback.data == LocationType.LIBRARY.value
)
@top_notification
async def libraries(callback: CallbackQuery):
    await callback.message.edit_text(
        text="У родного КАИ 5 библиотек:",
        reply_markup=libraries_dialer()
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Commands.LOCATIONS.value and
        LocationType.LIBRARY.value in callback.data
)
@top_notification
async def send_library(callback: CallbackQuery):
    await callback.message.bot.send_chat_action(chat_id=callback.message.chat.id, action="find_location")
    
    numbers: List[int] = list(map(int, callback.data.split()[1].split(",")))
    
    await callback.message.delete()
    
    for number in numbers:
        building: int = LIBRARIES[number]["building"] - 1
        
        await callback.message.answer_venue(
            latitude=BUILDINGS[building]["latitude"],
            longitude=BUILDINGS[building]["longitude"],
            title=LIBRARIES[number]["title"],
            address=BUILDINGS[building]["address"]
        )
        await callback.message.answer(
            text=LIBRARIES[number]["description"],
            parse_mode="markdown"
        )
    
    guards[callback.message.chat.id].drop()
