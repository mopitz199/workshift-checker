from dataclasses import dataclass
from datetime import datetime, timedelta


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

    def collisioned(self, date_range):
        return (
            self.end_date >= date_range.start_date
            and self.start_date <= date_range.end_date
        )

    def is_next_to_right(self, date_range):
        if not self.collisioned(date_range=date_range):
            return self.end_date + timedelta(days=1) == date_range.start_date
        else:
            return False

    def is_next_to_left(self, date_range):
        if not self.collisioned(date_range=date_range):
            return self.start_date - timedelta(days=1) == date_range.end_date
        else:
            return False

    def extract(self, start_date, end_date):
        other_range = Range(start_date, end_date)
        result = None
        if self.collisioned(other_range):
            extracted_start_date = max(start_date, self.start_date)
            extracted_end_date = min(end_date, self.end_date)
            result = Range(extracted_start_date, extracted_end_date)
        return result
