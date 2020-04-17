from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ClassesOptionType
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.calendar.week import WeekType
from bot.shared.commands import Commands

from datetime import datetime
from datetime import timedelta


def lecturer_chooser(names: [{str: str}]) -> InlineKeyboardMarkup:
    lecturer_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    lecturer_chooser_keyboard.row(cancel_button())
    
    lecturer_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=name["lecturer"], callback_data=" ".join([ Commands.LECTURERS.value, name["id"] ])
        ) for name in names
    ])
    
    return lecturer_chooser_keyboard

def lecturer_info_type_chooser(lecturer_id: str) -> InlineKeyboardMarkup:
    lecturer_info_type_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    lecturer_info_type_chooser_keyboard.row(cancel_button())
    
    lecturer_info_type_chooser_keyboard.add(
        InlineKeyboardButton(text="занятия", callback_data=" ".join([ ScheduleType.CLASSES.value, lecturer_id ])),
        InlineKeyboardButton(text="экзамены", callback_data=" ".join([ ScheduleType.EXAMS.value, lecturer_id ]))
    )
    
    return lecturer_info_type_chooser_keyboard


def lecturer_weektype_chooser(lecturer_id: str) -> InlineKeyboardMarkup:
    lecturer_weektype_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    # Decrementing to turn both variables into schedule array indices
    today_weekday: int = datetime.today().isoweekday() - 1
    tomorrow_weekday: int = today_weekday + 1
    should_show_next_week: bool = tomorrow_weekday > 6
    
    lecturer_weektype_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text="сегодня",
            callback_data=" ".join([
                ClassesOptionType.DAILY.value,
                WeekType.CURRENT.value,
                str(today_weekday),
                lecturer_id
            ])
        ),
        InlineKeyboardButton(
            text="завтра",
            callback_data=" ".join([
                ClassesOptionType.DAILY.value,
                WeekType.NEXT.value if should_show_next_week else WeekType.CURRENT.value,
                str(0 if should_show_next_week else tomorrow_weekday),
                lecturer_id
            ])
        )
    ])
    lecturer_weektype_chooser_keyboard.row(
        InlineKeyboardButton(text="текущую неделю", callback_data=" ".join([
            ClassesOptionType.WEEKDAYS.value, WeekType.CURRENT.value, lecturer_id
        ]))
    )
    lecturer_weektype_chooser_keyboard.row(
        InlineKeyboardButton(text="следующую неделю", callback_data=" ".join([
            ClassesOptionType.WEEKDAYS.value, WeekType.NEXT.value, lecturer_id
        ]))
    )
    
    lecturer_weektype_chooser_keyboard.row(cancel_button())
    
    return lecturer_weektype_chooser_keyboard


def lecturer_weekday_chooser(is_next: bool, lecturer_id: str) -> InlineKeyboardMarkup:
    lecturer_weekday_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    lecturer_weekday_chooser_keyboard.row(
        cancel_button(),
        InlineKeyboardButton(
            text="показать все",
            callback_data=" ".join([
                ClassesOptionType.WEEKLY.value,
                WeekType.NEXT.value if is_next else WeekType.CURRENT.value,
                lecturer_id
            ])
        )
    )
    
    today: datetime = datetime.today()
    today_weekday: int = today.isoweekday()
    
    for weekday in WEEKDAYS:
        date: datetime = today + timedelta(days=(weekday - today_weekday) + (7 if is_next else 0))
        
        lecturer_weekday_chooser_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEKDAYS[weekday],
                    day=int(date.strftime("%d")), month=MONTHS[date.strftime("%m")],
                    is_today=" •" if today == date else ""
                ),
                callback_data=" ".join([
                    ClassesOptionType.DAILY.value,
                    WeekType.NEXT.value if is_next else WeekType.CURRENT.value,
                    str(weekday - 1),  # Decrementing to turn the variable into schedule array index
                    lecturer_id
                ])
            )
        )
    
    return lecturer_weekday_chooser_keyboard
