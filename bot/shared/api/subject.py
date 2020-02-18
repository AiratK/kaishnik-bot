from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from enum import Enum


class Subject(ABC):
    def __init__(self):
        self._time: str       = "\n\n*[ {begin_time} - {end_time} ]"
        self._building: str   = "[ {building}"
        self._auditorium: str = "{auditorium} ]"
        self._dates: str      = "\n[ {dates} ]"
        self._title: str      = "\n{title}*"
        self._type: str       = "\n_{type}_"
        
        self._begin_time: int = None
        self._begin_hour: int = None
    
    
    @property
    def time(self) -> str:
        return self._time
    
    @property
    def building(self) -> str:
        return self._building[2:]
    
    @property
    def auditorium(self) -> str:
        return self._auditorium[:-2]
    
    @property
    def dates(self) -> str:
        return self._dates[3:-2]
    
    @property
    def title(self) -> str:
        return self._title[1:-1]
    
    @property
    def type(self) -> str:
        return self._type[2:-1]
    
    
    @time.setter
    def time(self, timeAndType: (str, str)):
        try:
            (time, type) = timeAndType
        except (TypeError, ValueError):
            time = timeAndType
            type = None
        
        (hours, minutes) = (int(time.split(":")[0]), int(time.split(":")[1]))
        
        self._begin_time = time
        self._begin_hour = hours
        
        begin_time: datetime = datetime(1, 1, 1, hours, minutes)  # Year, month, day are filled with nonsence
        
        if type == SubjectType.LAB.value:
            duration: timedelta = timedelta(hours=3)  # Lab duration is 3h with a 40/10m long break
            duration += timedelta(minutes=40) if begin_time.hour == 11 else timedelta(minutes=10)
        else:
            duration: timedelta = timedelta(hours=1, minutes=30)  # Class duration is 1.5h
        
        end_time: datetime = begin_time + duration
        
        self._time = self._time.format(begin_time=begin_time.strftime("%H:%M"), end_time=end_time.strftime("%H:%M"))
    
    @building.setter
    def building(self, building: str):
        self._building = self._building.format(building="СК Олимп" if "ОЛИМП" in building.upper() else (building + "ка"))
    
    @auditorium.setter
    def auditorium(self, auditorium: str):
        self._auditorium = self._auditorium.format(auditorium=(", " + auditorium) if auditorium and self.building != "СК Олимп" else "")
    
    @dates.setter
    def dates(self, dates: str):
        self._dates = self._dates.format(dates=dates) if "." in dates or "/" in dates or "(" in dates else ""
    
    @title.setter
    def title(self, title: str):
        self._title = self._title.format(title=title)
    
    @type.setter
    def type(self, type: str):
        if type == SubjectType.LECTURE.value: self._type = self._type.format(type="лекция")
        elif type == SubjectType.PRACTICE.value: self._type = self._type.format(type="практика")
        elif type == SubjectType.LAB.value: self._type = self._type.format(type="лабораторная работа")
        elif type == SubjectType.CONSULTATION.value: self._type = self._type.format(type="консультация")
        else: self._type = type
    
    
    @abstractmethod
    def get(self):
        pass


class StudentSubject(Subject):
    def __init__(self):
        super().__init__()
        
        self._lecturer: str   = "\n@ {lecturer}"
        self._department: str = "\n§ {department}"
        
        self._is_even: bool = None
        self._weekday: str = None
        self._begin_hour: int = None
    
    
    @property
    def lecturer(self) -> str:
        return self._lecturer
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def is_even(self) -> bool:
        return self._is_even
    
    @property
    def weekday(self) -> str:
        return self._weekday
    
    @property
    def begin_hour(self) -> int:
        return self._begin_hour
    
    
    @lecturer.setter
    def lecturer(self, new_value: str):
        self._lecturer = self._lecturer.format(lecturer=new_value.title()) if new_value else ""
    
    @department.setter
    def department(self, new_value: str):
        self._department = self._department.format(department=new_value) if new_value else ""
    
    @is_even.setter
    def is_even(self, new_value: bool):
        self._is_even = new_value
    
    @weekday.setter
    def weekday(self, new_value: str):
        self._weekday = new_value
    
    @begin_hour.setter
    def begin_hour(self, new_value: int):
        self._begin_hour = new_value
    
    
    def get(self) -> str:
        return "".join([
            self._time,
            self._building,
            self._auditorium,
            self._dates,
            self._title,
            self._type,
            self._lecturer,
            self._department
        ])

    def get_simple(self) -> str:
        return " ".join([ self._begin_time, self._title ]).replace("\n", "").replace("*", "")


class LecturerSubject(Subject):
    def __init__(self):
        super().__init__()
        
        self._groups: [str] = []
    
    
    @property
    def groups(self) -> [str]:
        return self._groups
    
    
    def get(self) -> str:
        groups_output: str = ""
        
        for group in self._groups:
            groups_output = "".join([ groups_output, "\n• У группы {}".format(group) ])
        
        return "".join([
            self._time,
            self._building,
            self._auditorium,
            self._dates,
            self._title,
            self._type,
            groups_output
        ])


class SubjectType(Enum):
    LECTURE: str = "лек"
    PRACTICE: str = "пр"
    LAB: str = "л.р."
    CONSULTATION: str = "конс"
