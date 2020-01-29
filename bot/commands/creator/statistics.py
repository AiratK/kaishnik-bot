from aiogram.types import Chat
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.creator.utilities.helpers import parse_creator_query
from bot.commands.creator.utilities.helpers import update_progress_bar
from bot.commands.creator.utilities.constants import CREATOR
from bot.commands.creator.utilities.constants import USERS_STATS
from bot.commands.creator.utilities.constants import COMMAND_REQUESTS_STATS
from bot.commands.creator.utilities.constants import USER_DATA
from bot.commands.creator.utilities.types import DataOption
from bot.commands.creator.utilities.types import Suboption

from bot.shared.api.constants import INSTITUTES
from bot.shared.api.student import Student
from bot.shared.commands import Commands

from datetime import datetime


@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.USERS.value ]
)
async def users(message: Message):
    institutes_stats: [str] = [ student.institute for student in students.values() ]
    years_stats: [str] = [ student.year for student in students.values() ]
    
    institutes_names: [str] = list(INSTITUTES.values())
    years_names: [str] = [ str(i) for i in range(1, 7) ]  # 6 years maximum
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=USERS_STATS.format(
            faculty_1=institutes_names[0], number_faculty_1=institutes_stats.count(institutes_names[0]),
            faculty_2=institutes_names[1], number_faculty_2=institutes_stats.count(institutes_names[1]),
            faculty_3=institutes_names[2], number_faculty_3=institutes_stats.count(institutes_names[2]),
            faculty_4=institutes_names[3], number_faculty_4=institutes_stats.count(institutes_names[3]),
            faculty_5=institutes_names[4], number_faculty_5=institutes_stats.count(institutes_names[4]),
            faculty_6=institutes_names[5], number_faculty_6=institutes_stats.count(institutes_names[5]),
            year_1=years_names[0], number_year_1=years_stats.count(years_names[0]),
            year_2=years_names[1], number_year_2=years_stats.count(years_names[1]),
            year_3=years_names[2], number_year_3=years_stats.count(years_names[2]),
            year_4=years_names[3], number_year_4=years_stats.count(years_names[3]),
            year_5=years_names[4], number_year_5=years_stats.count(years_names[4]),
            year_6=years_names[5], number_year_6=years_stats.count(years_names[5]),
            number_group_only=sum(1 for student in students.values() if not student.is_full),
            number_unsetup=sum(1 for student in students.values() if not student.is_setup),
            total=len(students)
        ),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.METRICS.value ]
)
async def get_metrics(message: Message):
    options: {str: str} = parse_creator_query(message.text)
    
    if options.get("", "") == "drop" or metrics.day != datetime.today().isoweekday(): metrics.drop()
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=COMMAND_REQUESTS_STATS.format(
            classes_request_number=metrics.classes,
            score_request_number=metrics.score,
            lecturers_request_number=metrics.lecturers,
            week_request_number=metrics.week,
            notes_request_number=metrics.notes,
            exams_request_number=metrics.exams,
            locations_request_number=metrics.locations,
            card_request_number=metrics.card,
            brs_request_number=metrics.brs,
            me_request_number=metrics.me,
            cancel_request_number=metrics.cancel,
            start_request_number=metrics.start,
            login_request_number=metrics.login,
            unlogin_request_number=metrics.unlogin,
            edit_request_number=metrics.edit,
            help_request_number=metrics.help,
            donate_request_number=metrics.donate,
            unknown_request_number=metrics.unknown,
            total_request_number=metrics.sum
        ),
        parse_mode="markdown"
    )

@dispatcher.message_handler(
    lambda message: message.chat.id == CREATOR,
    commands=[ Commands.DATA.value ]
)
async def data(message: Message):
    async def collect_asked_users() -> [int]:
        options: {str: str} = parse_creator_query(message.text)
        
        full_users_list: [int] = list(students)[::-1]  # Reversing list of students to show the new users first
        asked_users_list: [int] = []
        
        if DataOption.IDS.value in options:
            if options[DataOption.IDS.value] == Suboption.ALL.value:
                return full_users_list
            if options[DataOption.IDS.value] == Suboption.UNLOGIN.value:
                asked_users_list += [ chat_id for chat_id in full_users_list if not students[chat_id].is_setup ]
            if options[DataOption.IDS.value] == Suboption.ME.value:
                asked_users_list.append(message.chat.id)
            
            asked_users_list += [ chat_id for chat_id in full_users_list if str(chat_id) in options[DataOption.IDS.value] ]
        
        if DataOption.USERNAME.value in options or DataOption.FIRSTNAME.value in options:
            progress_bar: str = ""
            
            loading_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Started searching..."
            )
            
            for (index, chat_id) in enumerate(full_users_list):
                progress_bar = await update_progress_bar(
                    loading_message=loading_message, current_progress_bar=progress_bar,
                    values=full_users_list, index=index
                )
                
                try:
                    chat: Chat = await bot.get_chat(chat_id=chat_id)
                except Exception:
                    pass
                
                if (DataOption.USERNAME.value in options and options[DataOption.USERNAME.value] in chat.username) or (DataOption.FIRSTNAME.value in options and options[DataOption.FIRSTNAME.value] in chat.first_name):
                    asked_users_list.append(chat_id)
        
        if DataOption.NUMBER.value in options:
            asked_users_number: int = 0
            
            try:
                asked_users_number = int(options[DataOption.NUMBER.value])
            except Exception:
                pass
            
            asked_users_list += full_users_list[:asked_users_number]
        
        if DataOption.INDEX.value in options:
            try:
                index = int(options[DataOption.INDEX.value])
                asked_index_user = full_users_list[index]
            except Exception:
                pass
            else:
                asked_users_list.append(asked_index_user)
        
        if DataOption.NAME.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].name is not None and options[DataOption.NAME.value] in students[chat_id].name ]
        
        if DataOption.GROUP.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].group is not None and options[DataOption.GROUP.value] in students[chat_id].group ]
        
        if DataOption.YEAR.value in options:
            asked_users_list += [ chat_id for chat_id in full_users_list if students[chat_id].year == options[DataOption.YEAR.value] ]
        
        return asked_users_list
    
    asked_users_list: [int] = await collect_asked_users()
    inactives_list: [int] = []
    progress_bar: str = ""
    
    loading_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Started showing..."
    )
    
    for (index, chat_id) in enumerate(asked_users_list):
        progress_bar = await update_progress_bar(
            loading_message=loading_message, current_progress_bar=progress_bar,
            values=asked_users_list, index=index
        )
        
        try:
            chat: Chat = await bot.get_chat(chat_id=chat_id)
        except Exception:
            inactives_list.append(chat_id)
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USER_DATA.format(
                    firstname=chat.first_name, lastname=chat.last_name, username=chat.username,
                    chat_id=chat_id,
                    institute=students[chat_id].institute,
                    year=students[chat_id].year,
                    group_number=students[chat_id].group,
                    name=students[chat_id].name,
                    card=students[chat_id].card,
                    notes_number=len(students[chat_id].notes),
                    edited_classes_number=len(students[chat_id].edited_subjects),
                    fellow_students_number=len(students[chat_id].names),
                    is_full=students[chat_id].is_full,
                    guard_text=students[chat_id].guard.text,
                    is_guard_message_none=students[chat_id].guard.message is None,
                    hashtag="data"
                )
            )
    
    if len(inactives_list) == 1:
        await bot.send_message(
            chat_id=message.chat.id,
            text="There is *1* inactive user.",
            parse_mode="markdown"
        )
    elif len(inactives_list) != 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text="There are *{number}* inactive users.".format(number=len(inactives_list)),
            parse_mode="markdown"
        )
    
    await bot.send_message(
        chat_id=message.chat.id,
        text="*{shown}/{total}* users were shown!".format(shown=len(asked_users_list), total=len(students)),
        parse_mode="markdown"
    )
