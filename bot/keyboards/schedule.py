from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from bot.constants import WEEK
from bot.constants import MONTHS

from datetime import datetime
from datetime import timedelta

# /lecturers
def choose_lecturer(names):
    choose_lecturer_keyboard = InlineKeyboardMarkup(row_width=1)

    choose_lecturer_keyboard.add(*[
        InlineKeyboardButton(text=name["lecturer"], callback_data="lecturer {}".format(name["id"])) for name in names
    ])

    return choose_lecturer_keyboard

def lecturer_schedule_type(prepod_login):
    lecturer_schedule_type_keyboard = InlineKeyboardMarkup(row_width=1)

    lecturer_schedule_type_keyboard.add(
        InlineKeyboardButton(text="занятий", callback_data="l-classes {}".format(prepod_login)),
        InlineKeyboardButton(text="экзаменов", callback_data="l-exams {}".format(prepod_login))
    )

    return lecturer_schedule_type_keyboard

def lecturer_classes_week_type(prepod_login):
    week_type_keyboard = InlineKeyboardMarkup(row_width=1)

    week_type_keyboard.add(
        InlineKeyboardButton(text="текущую неделю", callback_data="l-weekdays crnt {}".format(prepod_login)),
        InlineKeyboardButton(text="следующую неделю", callback_data="l-weekdays next {}".format(prepod_login))
    )

    return week_type_keyboard

def lecturer_certain_date_chooser(todays_weekday, type, prepod_login):
    certain_date_keyboard = InlineKeyboardMarkup()
    
    certain_date_keyboard.row(
        InlineKeyboardButton(
            text="Показать все",
            callback_data="l-weekly {type} {prepod_login}".format(
                type=type,
                prepod_login=prepod_login
            )
        )
    )
    
    today = datetime.today()
    
    for weekday in WEEK:
        date = today + timedelta(days=(weekday - todays_weekday) + (7 if type == "next" else 0))
        
        certain_date_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEK[weekday],
                    day=int(date.strftime("%d")),
                    month=MONTHS[date.strftime("%m")],
                    is_today=" •" if today.strftime("%d") == date.strftime("%d") else ""
                ),
                callback_data="l-daily {type} {weekday} {prepod_login}".format(
                    type=type,
                    weekday=weekday,
                    prepod_login=prepod_login
                )
            )
        )
    
    return certain_date_keyboard


# /classes
def schedule_type():
    schedule_type_keyboard = InlineKeyboardMarkup()

    schedule_type_keyboard.row(
        InlineKeyboardButton(text="сегодня", callback_data="daily crnt {}".format(datetime.today().isoweekday())),
        InlineKeyboardButton(text="завтра", callback_data="daily crnt {}".format(datetime.today().isoweekday() + 1))
    )
    schedule_type_keyboard.row(InlineKeyboardButton(text="текущую неделю", callback_data="weekdays crnt"))
    schedule_type_keyboard.row(InlineKeyboardButton(text="следующую неделю", callback_data="weekdays next"))

    return schedule_type_keyboard

def certain_date_chooser(todays_weekday, type):
    certain_date_keyboard = InlineKeyboardMarkup()
    
    certain_date_keyboard.row(InlineKeyboardButton(text="Показать все", callback_data="weekly {}".format(type)))
    
    today = datetime.today()
    
    for weekday in WEEK:
        date = today + timedelta(days=(weekday - todays_weekday) + (7 if type == "next" else 0))
        
        certain_date_keyboard.row(
            InlineKeyboardButton(
                text="{weekday}, {day} {month}{is_today}".format(
                    weekday=WEEK[weekday],
                    day=int(date.strftime("%d")),
                    month=MONTHS[date.strftime("%m")],
                    is_today=" •" if today.strftime("%d") == date.strftime("%d") else ""
                ),
                callback_data="daily {type} {weekday}".format(type=type, weekday=weekday)
            )
        )
    
    return certain_date_keyboard