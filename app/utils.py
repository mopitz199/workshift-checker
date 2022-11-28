from datetime import datetime
from typing import Optional


class Utils:
    @classmethod
    def str_to_date(cls, string) -> datetime:
        """Method to transform an string to a datetime object"""
        return datetime.strptime(string, "%Y-%m-%d").date()

    @classmethod
    def str_to_datetime(cls, date_str, time_str) -> datetime:
        """Method to transform an string to a datetime object"""
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    @classmethod
    def has_collision(
        cls,
        schedule1,
        schedule2,
    ) -> bool:
        """Method to get if two schedule, has collisions"""
        return schedule1[1] >= schedule2[0] and schedule1[0] <= schedule2[1]

    @classmethod
    def get_day_number_from_date(
        cls, workshift_person_range, date_obj, total_days
    ) -> Optional[int]:
        """Method to get the number of the day in thw workshift from the date object"""

        starting_day = workshift_person_range["starting_day"]
        start_date = Utils.str_to_date(workshift_person_range["start_date"])
        end_date = Utils.str_to_date(workshift_person_range["end_date"])
        if start_date <= date_obj <= end_date:
            diff = (date_obj - start_date).days

            index = diff - total_days - starting_day + 2
            if index >= 0:
                day_number = (index % total_days) or total_days
            else:
                day_number = index + total_days
            return day_number
        else:
            return None
