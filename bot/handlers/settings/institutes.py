from bot import kbot
from bot import students
from bot import top_notification

from bot.keyboards.settings import year_setter
from bot.keyboards.settings import group_number_setter
from bot.keyboards.settings import name_setter
from bot.keyboards.settings import set_card_skipper

from bot.helpers           import save_to
from bot.helpers.student   import Student
from bot.helpers.datatypes import ScoreDataType
from bot.helpers.constants import INSTITUTES
from bot.helpers.constants import GUIDE_MESSAGE
from bot.helpers.constants import LOADING_REPLIES

from re import fullmatch
from random import choice


@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-institute-" in callback.data and "КИТ" not in callback.data
)
@top_notification
def set_institute(callback):
    # Setting institute
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    institute_id = callback.data.replace("set-institute-", "")
    
    students[callback.message.chat.id] = Student(
        institute=INSTITUTES[institute_id],
        institute_id=institute_id
    )
    
    students[callback.message.chat.id].previous_message = "/settings"  # Gates System (GS)
    
    # Asking for year
    years = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.years)
    
    if years is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери свой курс:",
        reply_markup=year_setter(years)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-year-" in callback.data
)
@top_notification
def set_year(callback):
    # Setting year
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].year = callback.data.replace("set-year-", "")
    
    # Asking for group
    groups = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.groups)
    
    if groups is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
    
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    if groups == {}:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=(
                "Здесь ничего нет, начни сначала —\n"
                "/settings"
            )
        )

        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери свою группу:",
        reply_markup=group_number_setter(groups)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-group-" in callback.data
)
@top_notification
def set_group_number(callback):
    # Setting group
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].group_number = callback.data.replace("set-group-", "")
    
    if students[callback.message.chat.id].group_number is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    if students[callback.message.chat.id].group_number == "non-existing":
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Такой группы нет🤔"
        )
        kbot.send_message(
            chat_id=callback.message.chat.id,
            text="Возможно, она появится позже, когда её внесут в каёвскую базу🤓"
        )
    
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for name
    names = students[callback.message.chat.id].get_dictionary_of(ScoreDataType.names)
    
    if names is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return

    if names == {}:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Здесь ничего нет. Начни сначала."
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return

    students[callback.message.chat.id].names = { name_id: name for name, name_id in names.items() }
        
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери себя:",
        reply_markup=name_setter(names)
    )

@kbot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].previous_message == "/settings" and
        "set-name-" in callback.data
)
@top_notification
def set_name(callback):
    # Setting name
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    students[callback.message.chat.id].name = students[callback.message.chat.id].names[callback.data.replace("set-name-", "")]
    
    if students[callback.message.chat.id].name is None:
        kbot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[callback.message.chat.id] = Student()  # Drop all the entered data
        return
    
    # Asking for student card number
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "Отправь номер своей зачётки "
            "(интересный факт — студенческий билет и зачётка имеют одинаковый номер!)."
            "\n\n"
            "Либо пропусти, но баллы показать не смогу."
        ),
        reply_markup=set_card_skipper()
    )

    students[callback.message.chat.id].previous_message = "/settings student-card-number"  # Gate System (GS)

@kbot.message_handler(func=lambda message: students[message.chat.id].previous_message == "/settings student-card-number")
def set_student_card_number(message):
    students[message.chat.id].student_card_number = message.text
    
    # The very 1st semester might be empty, so check the 1st one of the current year
    prelast_semester = int(students[message.chat.id].year)*2 - 1
    scoretable = students[message.chat.id].get_scoretable(prelast_semester)
    
    # Cleanning the chat
    try:
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        kbot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except Exception:
        pass
    
    if scoretable is None:
        kbot.send_message(
            chat_id=message.chat.id,
            text="kai.ru не отвечает🤷🏼‍♀️",
            disable_web_page_preview=True
        )
        
        students[message.chat.id] = Student()  # Drop all the entered data
        return

    if scoretable == []:
        kbot.send_message(
            chat_id=message.chat.id,
            text=(
                "Неверный номер зачётки. Исправляйся."
                "\n\n"
                "Либо пропусти, но баллы показать не смогу."
            ),
            reply_markup=set_card_skipper()
        )
        
        students[message.chat.id].student_card_number = None
        return

    students[message.chat.id].previous_message = None  # Gates System (GS)
    save_to(filename="data/users", object=students)

    kbot.send_message(
        chat_id=message.chat.id,
        text="Запомнено!"
    )
    kbot.send_message(
        chat_id=message.chat.id,
        text=GUIDE_MESSAGE,
        parse_mode="Markdown"
    )

@kbot.callback_query_handler(
    func=lambda callback: (
        students[callback.message.chat.id].previous_message == "/settings student-card-number" or
        students[callback.message.chat.id].previous_message == "/card"
    ) and callback.data == "skip-set-card"
)
@top_notification
def save_without_student_card_number(callback):
    students[callback.message.chat.id].student_card_number = "unset"
    students[callback.message.chat.id].previous_message = None  # Gates System (GS)
    save_to(filename="data/users", object=students)
    
    kbot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Запомнено без зачётки!"
    )
    kbot.send_message(
        chat_id=callback.message.chat.id,
        text=GUIDE_MESSAGE,
        parse_mode="Markdown"
    )
