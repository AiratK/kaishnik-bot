from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.shared.keyboards import cancel_button
from bot.shared.commands import Commands


def semester_chooser(semesters_number: int) -> InlineKeyboardMarkup:
    semester_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    
    semester_chooser_keyboard.row(cancel_button())
    
    semester_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=str(semester + 1),
            callback_data=" ".join([ Commands.SCORE_SEMESTER.value, str(semester + 1) ])
        ) for semester in range(semesters_number)
    ])
    
    return semester_chooser_keyboard

def subjects_type_chooser(has_exams: bool, has_tests: bool, has_graded_tests: bool) -> InlineKeyboardMarkup:
    subjects_type_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    if has_exams or has_tests or has_graded_tests:
        subjects_type_chooser_keyboard.row(
            cancel_button(),
            InlineKeyboardButton(
                text="показать все", callback_data=Commands.SCORE_ALL.value
            )
        )
    
    if has_exams:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="экзамены", callback_data=Commands.SCORE_EXAMS.value
        ))
    if has_tests:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="зачёты", callback_data=Commands.SCORE_TESTS.value
        ))
    if has_graded_tests:
        subjects_type_chooser_keyboard.row(InlineKeyboardButton(
            text="зачёты с оценкой", callback_data=Commands.SCORE_GRADED_TESTS.value
        ))
    
    return subjects_type_chooser_keyboard

def subject_chooser(subjects: [str], type: str) -> InlineKeyboardMarkup:
    subject_chooser_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    
    subject_chooser_keyboard.row(
        cancel_button(),
        InlineKeyboardButton(
            text="показать все",
            callback_data=" ".join([ type, "None" ])
        )
    )
    
    subject_chooser_keyboard.add(*[
        InlineKeyboardButton(
            text=title, callback_data=" ".join([ type, str(index) ])
        ) for (index, title) in enumerate(subjects)
    ])
    
    return subject_chooser_keyboard
