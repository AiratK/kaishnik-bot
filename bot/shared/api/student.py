from aiogram.types import Message

from bot.shared.api.helpers import beautify_classes
from bot.shared.api.helpers import beautify_exams
from bot.shared.api.helpers import beautify_scoretable
from bot.shared.api.constants import SCHEDULE_URL
from bot.shared.api.constants import SCORE_URL
from bot.shared.api.constants import P_SUB
from bot.shared.api.types import ScheduleType
from bot.shared.api.types import ScoreDataType
from bot.shared.api.subject import StudentSubject

from requests import get
from requests import post
from requests.exceptions import ConnectionError

from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup
from bs4.element import Tag

from enum import Enum


class SettingsOption(Enum):
    IS_SCHEDULE_SIZE_FULL: str = "is-schedule-size-full"
    ARE_CLASSES_ON_DATES: str = "are-classes-on-dates"


class Settings:
    def __init__(self):
        self._is_schedule_size_full: bool = True
        self._are_classes_on_dates: bool = True
    
    
    @property
    def is_schedule_size_full(self) -> bool:
        return self._is_schedule_size_full
    
    @property
    def are_classes_on_dates(self) -> bool:
        return self._are_classes_on_dates
    
    
    @is_schedule_size_full.setter
    def is_schedule_size_full(self, new_value):
        self._is_schedule_size_full = new_value
    
    @are_classes_on_dates.setter
    def are_classes_on_dates(self, new_value):
        self._are_classes_on_dates = new_value
    
    
    def drop(self):
        self.__init__()


class Guard:
    def __init__(self):
        self._text: str = None
        self._message: Message = None
    
    
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def message(self) -> Message:
        return self._message
    
    
    @text.setter
    def text(self, text: str):
        self._text = text
    
    @message.setter
    def message(self, message: Message):
        self._message = message
    
    
    def drop(self):
        self.__init__()


class Student:
    def __init__(self):
        self._is_setup: bool = False
        self._is_full: bool = None
        
        self._institute: str = None
        self._institute_id: str = None
        
        self._year: str = None
        
        self._group: str = None
        self._group_schedule_id: str = None
        self._group_score_id: str = None
        
        self._another_group: str = None
        
        self._name: str = None
        self._name_id: str = None
        self._names: {str, str} = {}
        
        self._card: str = None
        
        self._scoretable: [(str, str)] = None
        
        self._notes: [str] = []
        
        self._edited_subjects: [StudentSubject] = []
        self._edited_subjectSubject: StudentSubject = None
        
        self._settings: {Settings: bool} = Settings()
        
        self._guard: Guard = Guard()
    
    
    @property
    def is_setup(self) -> bool:
        return self._is_setup
    
    @property
    def is_full(self) -> bool:
        return self._is_full
    
    @property
    def institute(self) -> str:
        return self._institute
    
    @property
    def institute_id(self) -> str:
        return self._institute_id
    
    @property
    def year(self) -> str:
        return self._year
    
    @property
    def group(self) -> str:
        return self._group
    
    @property
    def group_schedule_id(self) -> str:
        return self._group_schedule_id
    
    @property
    def group_score_id(self) -> str:
        return self._group_score_id
    
    @property
    def another_group(self) -> str:
        return self._another_group
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def name_id(self) -> str:
        return self._name_id
    
    @property
    def names(self) -> {str, str}:
        return self._names
    
    @property
    def card(self) -> str:
        return self._card
    
    @property
    def scoretable(self) -> [(str, str)]:
        return self._scoretable
    
    @property
    def notes(self) -> [str]:
        return self._notes
    
    @property
    def edited_subjects(self) -> [StudentSubject]:
        return self._edited_subjects
    
    @property
    def edited_subject(self) -> StudentSubject:
        return self._edited_subject
    
    @property
    def settings(self) -> {str: bool}:
        return self._settings
    
    @property
    def guard(self) -> Guard:
        return self._guard
    
    
    @is_setup.setter
    def is_setup(self, new_value: bool):
        self._is_setup = new_value
    
    @is_full.setter
    def is_full(self, new_value: bool):
        self._is_full = new_value
    
    @institute.setter
    def institute(self, new_value: str):
        self._institute = new_value

    @institute_id.setter
    def institute_id(self, new_value: str):
        self._institute_id = new_value
    
    @year.setter
    def year(self, new_value: str):
        self._year = new_value
    
    @group.setter
    def group(self, new_value: str):
        self._group = new_value
        self._group_schedule_id = self.get_schedule_id(group=new_value)
        self._group_score_id = self.get_dictionary_of(ScoreDataType.GROUPS).get(new_value) if self._is_full else None
    
    @another_group.setter
    def another_group(self, new_value: str):
        self._another_group = None if new_value is None else self.get_schedule_id(group=new_value)
    
    @name.setter
    def name(self, new_value: str):
        self._name = new_value
        self._name_id = self.get_dictionary_of(ScoreDataType.NAMES).get(new_value)
    
    @names.setter
    def names(self, new_value: {str, str}):
        self._names = new_value
    
    @card.setter
    def card(self, new_value: str):
        self._card = new_value
    
    @scoretable.setter
    def scoretable(self, new_value: [(str, str)]):
        self._scoretable = new_value
    
    @notes.setter
    def notes(self, new_value: [str]):
        self._notes = new_value
    
    @edited_subjects.setter
    def edited_subjects(self, new_value: [StudentSubject]):
        self._edited_subjects = new_value
    
    @edited_subject.setter
    def edited_subject(self, new_value: StudentSubject):
        self._edited_subject = new_value
    
    
    def get_schedule_id(self, group: str) -> str:
        try:
            return get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": "getGroupsURL",
                "query": group
            }).json()[0]["id"]
        except (ConnectionError, JSONDecodeError, IndexError, KeyError):
            return None
    
    def get_schedule(self, TYPE: ScheduleType, is_next: bool = False) -> [str]:
        is_own_group_asked: bool = self._another_group is None
        
        try:
            response: [{int: {str: str}}] = get(url=SCHEDULE_URL, params={
                "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                "p_p_lifecycle": "2",
                "p_p_resource_id": TYPE.value,
                "groupId": self._group_schedule_id if is_own_group_asked else self._another_group
            }).json()
        except (ConnectionError, JSONDecodeError, IndexError, KeyError):
            return None
        
        if not response:
            return []
        
        self._another_group = None
        
        if TYPE is ScheduleType.CLASSES:
            return beautify_classes(response, is_next, self._edited_subjects if is_own_group_asked else [], self._settings)
        
        if TYPE is ScheduleType.EXAMS:
            return beautify_exams(response)
    
    
    def get_dictionary_of(self, TYPE: ScoreDataType) -> {str: str}:
        try:
            page: str = get(url=SCORE_URL, params={
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id
            }).content.decode("CP1251")
            
            soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
            selector: Tag = soup.find(name="select", attrs={ "name": TYPE.value })
            
            keys: [str] = [ option.text for option in selector.find_all("option") ][1:]
            values: [str] = [ option["value"] for option in selector.find_all("option") ][1:]
            
            # Fixing bad quality response
            for i in range(1, len(keys)): keys[i - 1] = keys[i - 1].replace(keys[i], "")
            for (i, key) in enumerate(keys): keys[i] = key[:-1] if key.endswith(" ") else key
        except (ConnectionError, AttributeError, KeyError, IndexError):
            return dict()
        else:
            return dict(zip(keys, values))
    
    def get_last_available_semester(self) -> int:
        try:
            page: str = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id,
                "p_stud": self._name_id,
                "p_zach": self._card
            }).content.decode("CP1251")
            
            soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
            selector: Tag = soup.find(name="select", attrs={ "name": "semestr" })
            
            if not selector: return 0
            
            return max([ int(option["value"]) for option in selector.find_all("option") ])
        except ConnectionError:
            return None
    
    def get_scoretable(self, semester: str) -> [(str, str)]:
        try:
            page: str = post(SCORE_URL, data={
                "p_sub": P_SUB,
                "p_fac": self._institute_id,
                "p_kurs": self._year,
                "p_group": self._group_score_id,
                "p_stud": self._name_id,
                "p_zach": self._card,
                "semestr": semester
            }).content.decode("CP1251")
            
            soup: BeautifulSoup = BeautifulSoup(page, features="html.parser")
            table: Tag = soup.html.find(name="table", attrs={ "id": "reyt" })
            
            if not table: return []
            
            raw_scoretable: [[str]] = [ [ (data.text if data.text else "-") for data in row.find_all("td") ] for row in table.find_all("tr") ][2:]
            
            return beautify_scoretable(raw_scoretable)
        except ConnectionError:
            return None
