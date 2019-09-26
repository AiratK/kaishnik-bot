from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.commands.locations.utilities.constants import BUILDINGS
from bot.commands.locations.utilities.constants import LIBRARIES
from bot.commands.locations.utilities.constants import SPORTSCOMPLEX
from bot.commands.locations.utilities.constants import DORMS
from bot.commands.locations.utilities.types import LocationType


def location_type_chooser():
    location_type_chooser_keyboard = InlineKeyboardMarkup()
    
    location_type_chooser_keyboard.row(InlineKeyboardButton(
        text="Учебные здания", callback_data=LocationType.BUILDING.value
    ))
    location_type_chooser_keyboard.row(InlineKeyboardButton(
        text="Библиотеки", callback_data=LocationType.LIBRARY.value
    ))
    location_type_chooser_keyboard.row(InlineKeyboardButton(
        text="СК «Олимп»", callback_data=LocationType.SPORTSCOMPLEX.value
    ))
    location_type_chooser_keyboard.row(InlineKeyboardButton(
        text="Общежития", callback_data=LocationType.DORM.value
    ))
    
    return location_type_chooser_keyboard


def buildings_dialer():
    buildings_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    buildings_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=building, callback_data=" ".join([ LocationType.BUILDING.value, building ])
        ) for building in BUILDINGS
    ])
    
    return buildings_dialer_keyboard

def libraries_dialer():
    libraries_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    libraries_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=library, callback_data=" ".join([ LocationType.LIBRARY.value, library ])
        ) for library in LIBRARIES
    ])
    
    return libraries_dialer_keyboard

def sportscomplex_dialer():
    sportscomplex_dialer_keyboard = InlineKeyboardMarkup(row_width=1)
    
    sportscomplex_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=sportscomplex, callback_data=" ".join([ LocationType.SPORTSCOMPLEX.value, sportscomplex ])
        ) for sportscomplex in SPORTSCOMPLEX
    ])
    
    return sportscomplex_dialer_keyboard

def dorms_dialer():
    dorms_dialer_keyboard = InlineKeyboardMarkup(row_width=4)
    
    dorms_dialer_keyboard.add(*[
        InlineKeyboardButton(
            text=dorm, callback_data=" ".join([ LocationType.DORM.value, dorm ])
        ) for dorm in DORMS
    ])
    
    return dorms_dialer_keyboard