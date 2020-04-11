from bot.shared.calendar.constants import WEEKDAYS
from bot.shared.calendar.constants import MONTHS
from bot.shared.data.helpers import load_data
from bot.shared.data.constants import IS_WEEK_REVERSED_FILE

from datetime import datetime
from datetime import date
from enum import Enum


def is_even() -> bool:
    return datetime.today().isocalendar()[1] % 2 == (1 if is_week_reversed() else 0)

def is_week_reversed() -> bool:
    return load_data(file=IS_WEEK_REVERSED_FILE)


def get_week_number() -> int:
    (current_year, current_week, _) = datetime.today().isocalendar()
    
    semester_1st_day = date(current_year, 2 if datetime.today().month < 9 else 9, 1)
    first_week = semester_1st_day.isocalendar()[1]
    
    return current_week - first_week + (0 if semester_1st_day.isoweekday() == 7 else 1)


def weekday_date() -> (str, str):
    date: datetime = datetime.today()
    weekday: int = date.isoweekday()
    
    return (
        WEEKDAYS[weekday] if weekday < 7 else "Воскресенье",
        "{day} {month}".format(
            day=int(date.strftime("%d")),  # int()-cast is used to replace "01 апреля" with "1 апреля"
            month=MONTHS[date.strftime("%m")]
        )
    )


class WeekType(Enum):
    CURRENT: str = "week-current"
    NEXT: str = "week-next"

class WeekParity(Enum):
    BOTH: str = "both"
    EVEN: str = "even"
    ODD: str = "odd"
