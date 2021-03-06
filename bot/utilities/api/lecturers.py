from json.decoder import JSONDecodeError

from typing import Optional
from typing import Union
from typing import Dict
from typing import List
from typing import Tuple

from requests import get
from requests.exceptions import ConnectionError

from bot.models.settings import Settings

from bot.utilities.api.helpers.schedule import beautify_lecturers_classes
from bot.utilities.api.helpers.schedule import beautify_lecturers_exams
from bot.utilities.api.constants import LECTURERS_SCHEDULE_URL
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.types import ResponseError


def get_lecturers_names() -> Tuple[Optional[List[Dict[str, str]]], Optional[ResponseError]]:
    try:
        lecturers_names: List[Dict[str, str]] = get(LECTURERS_SCHEDULE_URL, timeout=(6, 6), params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": "getLecturersURL",
            "query": "_"  # Underscore symbol to get all the names
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    else:
        return (lecturers_names, None)

def get_lecturers_schedule(lecturer_id: str, schedule_type: ScheduleType, user_id: int, dates: Optional[List[str]] = None) -> Tuple[Optional[Union[List[str], str]], Optional[str]]:
    try:
        response: [{str, str}] = get(url=LECTURERS_SCHEDULE_URL, timeout=(6, 6), params={
            "p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
            "p_p_lifecycle": "2",
            "p_p_resource_id": schedule_type.value,
            "prepodLogin": lecturer_id
        }).json()
    except (ConnectionError, Timeout, JSONDecodeError):
        return (None, ResponseError.NO_RESPONSE)
    
    if not response:
        return (None, ResponseError.NO_DATA)
    
    settings: Settings = Settings.get(Settings.user_id == user_id)
    
    if schedule_type is ScheduleType.CLASSES:
        return (beautify_lecturers_classes(raw_schedule=response, dates=dates, settings=settings), None)
    
    if schedule_type is ScheduleType.EXAMS:
        return (beautify_lecturers_exams(raw_schedule=response, settings=settings), None)
