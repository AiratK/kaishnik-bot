from bot import bot
from bot import students

from bot.commands.edit.utilities.keyboards import weektype_chooser
from bot.commands.edit.utilities.keyboards import weekday_chooser
from bot.commands.edit.utilities.keyboards import edit_chooser

from bot.shared.helpers import top_notification
from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.week import WeekParity
from bot.shared.commands import Commands


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        callback.data in [ Commands.EDIT_SHOW.value, Commands.EDIT_DELETE.value ]
)
@top_notification
def choose_weetype(callback):
    if callback.data == Commands.EDIT_SHOW.value: ACTION = Commands.EDIT_SHOW_WEEKTYPE
    elif callback.data == Commands.EDIT_DELETE.value: ACTION = Commands.EDIT_DELETE_WEEKTYPE
    
    (classes_on_both, classes_on_even, classes_on_odd) = (0, 0, 0)
    
    for edited_subject in students[callback.message.chat.id].edited_subjects:
        if edited_subject.is_even is None: classes_on_both += 1
        elif edited_subject.is_even is True: classes_on_even += 1
        elif edited_subject.is_even is False: classes_on_odd += 1
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=(
            "В скобках указано количество отредактированных пар.\n\n"
            "Выбери тип недели:"
        ),
        reply_markup=weektype_chooser(
            classes_on_both=classes_on_both,
            classes_on_even=classes_on_even,
            classes_on_odd=classes_on_odd,
            ACTION=ACTION
        )
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and (
            Commands.EDIT_SHOW_WEEKTYPE.value in callback.data or
            Commands.EDIT_DELETE_WEEKTYPE.value in callback.data
        )
)
@top_notification
def choose_weekday(callback):
    if Commands.EDIT_SHOW_WEEKTYPE.value in callback.data: ACTION = Commands.EDIT_SHOW_WEEKDAY
    elif Commands.EDIT_DELETE_WEEKTYPE.value in callback.data: ACTION = Commands.EDIT_DELETE_WEEKDAY
    
    weektype = callback.data.split()[1]
    
    if weektype == WeekParity.BOTH.value: is_even = None
    elif weektype == WeekParity.EVEN.value: is_even = True
    elif weektype == WeekParity.ODD.value: is_even = False
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери день:",
        reply_markup=weekday_chooser(
            weektype=callback.data.split()[1],
            subjects_number_by_weekdays=[ sum(
                1 for subject in students[callback.message.chat.id].edited_subjects if subject.is_even == is_even and subject.weekday == weekday
            ) for weekday in WEEKDAYS ],
            ACTION=ACTION
        )
    )

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and (
            Commands.EDIT_SHOW_WEEKDAY.value in callback.data or
            Commands.EDIT_DELETE_WEEKDAY.value in callback.data
        )
)
@top_notification
def choose_edit(callback):
    if Commands.EDIT_SHOW_WEEKDAY.value in callback.data: ACTION = Commands.EDIT_SHOW_EDIT
    elif Commands.EDIT_DELETE_WEEKDAY.value in callback.data: ACTION = Commands.EDIT_DELETE_EDIT
    
    (weektype, weekday) = callback.data.split()[1:]
    
    if weektype == WeekParity.BOTH.value: is_even = None
    elif weektype == WeekParity.EVEN.value: is_even = True
    elif weektype == WeekParity.ODD.value: is_even = False
    
    subjects = { index: subject for (index, subject) in enumerate(students[callback.message.chat.id].edited_subjects) if subject.is_even == is_even and subject.weekday == int(weekday) }
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Выбери пару:",
        reply_markup=edit_chooser(
            weektype=weektype,
            weekday=weekday,
            subjects=subjects,
            ACTION=ACTION
        )
    )


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SHOW_ALL.value in callback.data
)
@top_notification
def show_all(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    request_enities = callback.data.split()[1:]
    
    weektypes = { "каждая": None, "чётная": True, "нечётная": False }
    weekdays = WEEKDAYS
    
    if len(request_enities) > 0:
        if request_enities[0] == WeekParity.BOTH.value: weektypes = { "каждая": None }
        elif request_enities[0] == WeekParity.EVEN.value: weektypes = { "чётная": True }
        elif request_enities[0] == WeekParity.ODD.value: weektypes = { "нечётная": False }
    
    if len(request_enities) > 1:
        requested_weekday = int(request_enities[1])
        weekdays = { requested_weekday: WEEKDAYS[requested_weekday] }
    
    subjects_number = 0
    
    for (weektype, is_even) in weektypes.items():
        weektype_weekdays = [ "*{} неделя*".format(weektype) ]
        
        for (weekday, weekday_name) in weekdays.items():
            weekday_classes = [ subject.get() for subject in students[callback.message.chat.id].edited_subjects if subject.weekday == weekday and subject.is_even == is_even ]
            
            if len(weekday_classes) > 0:
                subjects_number += len(weekday_classes)
                weektype_weekdays.append("".join([ "*", weekday_name, "*", ] + weekday_classes))
        
        if len(weektype_weekdays) > 1:
            for weektype_weekday in weektype_weekdays:
                bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=weektype_weekday,
                    parse_mode="Markdown"
                )
    
    if subjects_number == 1: grammatical_entity = "а"
    elif subjects_number in range(2, 5): grammatical_entity = "ы"
    else: grammatical_entity = ""
    
    bot.send_message(
        chat_id=callback.message.chat.id,
        text="*{}* пар{} всего!".format(subjects_number, grammatical_entity),
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_SHOW_EDIT.value in callback.data
)
@top_notification
def show_edit(callback):
    index = int(callback.data.split()[1])
    subject = students[callback.message.chat.id].edited_subjects[index]

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=subject.get(),
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].guard.drop()


@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_DELETE_ALL.value in callback.data
)
@top_notification
def delete_all(callback):
    request_enities = callback.data.split()[1:]
    
    weektypes = { "каждая": None, "чётная": True, "нечётная": False }
    weekdays = WEEKDAYS
    
    if len(request_enities) > 0:
        if request_enities[0] == WeekParity.BOTH.value: weektypes = { "каждая": None }
        elif request_enities[0] == WeekParity.EVEN.value: weektypes = { "чётная": True }
        elif request_enities[0] == WeekParity.ODD.value: weektypes = { "нечётная": False }
    
    if len(request_enities) > 1:
        requested_weekday = int(request_enities[1])
        weekdays = { requested_weekday: WEEKDAYS[requested_weekday] }
    
    subjects_number = 0
    
    for (weektype, is_even) in weektypes.items():
        for (weekday, weekday_name) in weekdays.items():
            for subject in list(students[callback.message.chat.id].edited_subjects):
                if subject.weekday == weekday and subject.is_even == is_even:
                    students[callback.message.chat.id].edited_subjects.remove(subject)
    
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!",
        parse_mode="Markdown"
    )
    
    students[callback.message.chat.id].guard.drop()

@bot.callback_query_handler(
    func=lambda callback:
        students[callback.message.chat.id].guard.text == Commands.EDIT.value and
        Commands.EDIT_DELETE_EDIT.value in callback.data
)
@top_notification
def delete_edit(callback):
    index = int(callback.data.split()[1])
    students[callback.message.chat.id].edited_subjects.pop(index)

    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Удалено!",
        parse_mode="Markdown"
    )

    students[callback.message.chat.id].guard.drop()