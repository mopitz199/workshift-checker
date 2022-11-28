from dataclasses import dataclass
from datetime import datetime


@dataclass
class CollisionsResults:
    collisions_detail: dict
    comparisions: int
    collisions: int
    collision_schedules = list

    def __init__(self, collisions_detail=None, comparisions=0, collisions=0) -> None:
        if collisions_detail is None:
            self.collisions_detail = {}
        self.comparisions = comparisions
        self.collisions = collisions
        self.collision_schedules = []

    def append_collision_schedule(self, entrance_schedule, base_schedule):
        self.collision_schedules.append(
            {
                "entrance": entrance_schedule,
                "base": base_schedule,
            }
        )

    def update_collisions_detail(
        self,
        entrance_day_number,
        base_day_number,
        collision_type,
    ):
        if entrance_day_number not in self.collisions_detail:
            self.collisions_detail[entrance_day_number] = {}

        self.collisions_detail[entrance_day_number][collision_type] = base_day_number

    def add_comparision(self):
        self.comparisions += 1

    def add_collision(self):
        self.collisions += 1


@dataclass
class WorkShiftPersonRangeInfo:
    workshift: dict
    workshift_person_range: dict
    workshift_len: int = 0
    initial_day_number: int = None
