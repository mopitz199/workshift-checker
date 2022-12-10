from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkShiftPersonRangeInfo:
    workshift: dict
    workshift_person_range: dict
    workshift_len: int = 0
    initial_day_number: int = None


@dataclass
class Range:
    start_date: datetime.date
    end_date: datetime.date
