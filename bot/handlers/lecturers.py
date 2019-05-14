from bot import kbot
from bot import students
from bot import metrics
from bot import top_notification

from bot.constants import WEEKDAYS
from bot.constants import MAX_LECTURERS_NUMBER

from bot.keyboards.lecturers import choose_lecturer
from bot.keyboards.lecturers import lecturer_info_type
from bot.keyboards.lecturers import lecturer_classes_week_type
from bot.keyboards.lecturers import lecturer_certain_date_chooser

from bot.helpers import get_lecturers_names
from bot.helpers import get_lecturers_schedule

from datetime import datetime


@kbot.message_handler(
    commands=["lecturers"],
    func=lambda message: students[message.chat.id].previous_message is None
)
@metrics.increment("lecturers")
def lecturers(message):
    students[message.chat.id].previous_message = "/lecturers name"  # Gate System (GS)
    
    kbot.send_message(
        chat_id=message.chat.id,
        text="Введи ФИО преподавателя полностью или частично."
    )

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers name")
def find_lecturer(message):
    names = get_lecturers_names(message.text)
    
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass
    
    if names is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Сайт kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[message.chat.id].previous_message = None  # Gate System (GS)
    elif names != []:
        if len(names) <= MAX_LECTURERS_NUMBER:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Выбери преподавателя:",
                reply_markup=choose_lecturer(names)
            )
            
            students[message.chat.id].previous_message = "/lecturers"  # Gate System (GS)
        else:
            kbot.send_message(
                chat_id=message.chat.id,
                text="Слишком мало букв, слишком много преподавателей…"
            )
            
            students[message.chat.id].previous_message = None  # Gate System (GS)
    else:
        kbot.send_message(
            chat_id=message.chat.id,
            text="Ничего не найдено :("
        )
        
        students[message.chat.id].previous_message = None  # Gate System (GS)

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "lecturer" in callback.data
)
@top_notification
def lecturers_schedule_type(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type(callback.data.replace("lecturer ", ""))
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-classes" in callback.data
)
@top_notification
def lecturers_week_type_classes(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Преподавателево расписание занятий на:",
        reply_markup=lecturer_classes_week_type(callback.data.replace("l-classes ", ""))
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekdays" in callback.data
)
@top_notification
def certain_date_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери нужный день:",
        reply_markup=lecturer_certain_date_chooser(
            todays_weekday=datetime.today().isoweekday(),
            type=callback.data.replace("l-weekdays ", "")[:4],
            prepod_login=callback.data[16:]
        )
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-daily" in callback.data
)
@top_notification
def one_day_lecturer_schedule(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=get_lecturers_schedule(
            prepod_login=callback.data[15:],
            type="l-classes",
            weekday=int(callback.data[13]),
            next="next" in callback.data
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-weekly" in callback.data
)
@top_notification
def weekly_lecturer_schedule(callback):
    kbot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    for weekday in WEEKDAYS:
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text=get_lecturers_schedule(
                prepod_login=callback.data[14:],
                type="l-classes",
                weekday=weekday,
                next="next" in callback.data
            ),
            parse_mode="Markdown"
        )
    
    students[callback.message.chat.id].previous_message = None


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/lecturers" and
        "l-exams" in callback.data
)
@top_notification
def send_lecturers_exams(callback):
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=get_lecturers_schedule(
            prepod_login=callback.data.replace("l-exams ", ""),
            type="l-exams"
        ),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].previous_message = None


@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/lecturers")
def gs_lecturers(message): kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
