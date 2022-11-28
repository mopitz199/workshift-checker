from dataclasses import dataclass
from datetime import datetime


@dataclass
class CollisionsResults:
    collisions_detail: dict
    comparisions: int
    collisions: int

    def __init__(self, collisions_detail=None, comparisions=0, collisions=0) -> None:
        if collisions_detail is None:
            self.collisions_detail = {}
        self.comparisions = comparisions
        self.collisions = collisions

    def update_collisions_detail(self, day_number: int, collision_detail: dict):
        if day_number not in self.collisions_detail:
            self.collisions_detail[day_number] = collision_detail
        else:
            self.collisions_detail[day_number].update(collision_detail)

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
