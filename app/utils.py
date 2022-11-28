from datetime import datetime, timedelta
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

    @classmethod
    def get_day_schedule(cls, wpr_info, date_obj):
        day_number = cls.get_day_number_from_date(
            workshift_person_range=wpr_info.workshift_person_range,
            date_obj=date_obj,
            total_days=wpr_info.workshift_len,
        )

        if day_number:
            day_schedule = wpr_info.workshift[str(day_number)]
            if day_schedule:
                start_datetime = cls.str_to_datetime(
                    str(date_obj), day_schedule["start_time"]
                )
                if day_schedule["is_nightly"]:
                    next_date = date_obj + timedelta(days=1)
                else:
                    next_date = date_obj
                end_datetime = cls.str_to_datetime(
                    str(next_date), day_schedule["end_time"]
                )
                return (start_datetime, end_datetime), day_schedule["is_nightly"]
        return None, None
