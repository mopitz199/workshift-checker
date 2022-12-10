from datetime import datetime, timedelta
from typing import Tuple

from app.data_classes import Range


class CollisionsResults:
    """This class has all the necessary to colect and process all the colissions
    between an specific base workshift person range, and the entrance workshift person range"""

    def __init__(
        self,
        day_number_collisions: dict = None,
        number_of_comparisions: int = 0,
        number_of_collisions: int = 0,
    ) -> None:

        # Dict the get days number that collision with the base range
        if day_number_collisions is None:
            self.day_number_collisions = {}

        # The number of day comparission. Does not matter if the days collisioned or not
        self.number_of_comparisions = number_of_comparisions

        # The number of day collisions. Only counts the days that collisioned
        self.number_of_collisions = number_of_collisions

        # A list with all the collisioned schedules
        self.collision_schedules: list[Tuple[datetime, datetime]] = []

        # A list with all the dates that collisioned in the base range
        self.collision_base_dates: list[datetime.date] = []

        # All the date ranges that collisioned in the base range
        self.collision_ranges: list[Range] = []

        """The new ranges that should be created(and remove the base range) in order
        to does not have collisions with the entrance range"""
        self.new_base_ranges = []

    def append_collision_schedule(
        self,
        entrance_schedule: Tuple[datetime, datetime],
        base_schedule: Tuple[datetime, datetime],
    ):
        self.collision_schedules.append(
            {
                "entrance": entrance_schedule,
                "base": base_schedule,
            }
        )

    def append_base_date(self, base_schedule: Tuple[datetime, datetime]):
        date_obj = base_schedule[0].date()
        self.collision_base_dates.append(date_obj)

    def create_range(self, start_date, end_date):
        return Range(start_date=start_date, end_date=end_date)

    def join_base_dates(self):
        collision_base_dates = list(set(self.collision_base_dates))
        collision_base_dates.sort()

        collision_ranges = []

        if collision_base_dates:
            start = collision_base_dates[0]
            prev = collision_base_dates[0]
            for date_obj in collision_base_dates:
                if date_obj - timedelta(days=1) > prev:
                    date_range = self.create_range(start, prev)
                    collision_ranges.append(date_range)
                    start = date_obj
                prev = date_obj

            date_range = self.create_range(start, prev)
            collision_ranges.append(date_range)
        self.collision_ranges = collision_ranges

    def get_new_base_ranges(
        self, base_start_date: datetime.date, base_end_date: datetime.date
    ):
        result = []
        aux_date_range = self.create_range(base_start_date, base_end_date)
        for date_range in self.collision_ranges:
            if aux_date_range.start_date != date_range.start_date:
                new_date_range = self.create_range(
                    aux_date_range.start_date,
                    max(
                        aux_date_range.start_date,
                        date_range.start_date - timedelta(days=1),
                    ),
                )
                result.append(new_date_range)

            aux_date_range = self.create_range(
                min(base_end_date, date_range.end_date + timedelta(days=1)),
                base_end_date,
            )

        result.append(aux_date_range)

        self.new_base_ranges = result

    def update_day_number_collisions(
        self,
        entrance_day_number,
        base_day_number,
        collision_type,
    ):
        if entrance_day_number not in self.day_number_collisions:
            self.day_number_collisions[entrance_day_number] = {}

        self.day_number_collisions[entrance_day_number][
            collision_type
        ] = base_day_number

    def add_comparision(self):
        self.number_of_comparisions += 1

    def add_collision(self):
        self.number_of_collisions += 1
