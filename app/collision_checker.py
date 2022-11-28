from datetime import datetime, timedelta

from app.classes import CollisionsResults
from app.utils import Utils

smart_collisions = True


class CollisionChecker:
    def __init__(
        self, base_workshift_person_range_info, entrance_workshift_person_range_info
    ) -> None:
        self.all_traversed = False

        self.base_wpr_info = base_workshift_person_range_info
        self.entrance_wpr_info = entrance_workshift_person_range_info
        self.collisions_results = CollisionsResults()

        self.current_entrance_schedule = None
        self.current_entrance_schedule_is_nightly = None
        self.aux_date = None

    def get_initial_range(self):
        base_start_date = Utils.str_to_date(
            self.base_wpr_info.workshift_person_range["start_date"]
        )
        base_end_date = Utils.str_to_date(
            self.base_wpr_info.workshift_person_range["end_date"]
        )

        entrance_start_date = Utils.str_to_date(
            self.entrance_wpr_info.workshift_person_range["start_date"]
        )
        entrance_end_date = Utils.str_to_date(
            self.entrance_wpr_info.workshift_person_range["end_date"]
        )

        max_start_date = max(base_start_date, entrance_start_date)
        min_end_date = min(base_end_date, entrance_end_date)

        return max_start_date, min_end_date

    def process_traverse(self, aux_base_day_number, aux_entrance_day_number):
        if (
            not self.base_wpr_info.initial_day_number
            or not self.entrance_wpr_info.initial_day_number
        ):
            self.base_wpr_info.initial_day_number = aux_base_day_number
            self.entrance_wpr_info.initial_day_number = aux_entrance_day_number
        else:
            if (
                aux_base_day_number == self.base_wpr_info.initial_day_number
                and self.entrance_wpr_info.initial_day_number == aux_entrance_day_number
            ):
                # Traverse all
                self.all_traversed = True

    def check_prev_schedule(self):
        aux_collision_detail = {}
        prev_aux_date = self.aux_date - timedelta(days=1)
        prev_base_schedule, prev_base_schedule_is_nightly = Utils.get_day_schedule(
            self.base_wpr_info, prev_aux_date
        )

        if prev_base_schedule and prev_base_schedule_is_nightly:
            aux_base_day_number = Utils.get_day_number_from_date(
                self.base_wpr_info.workshift_person_range,
                prev_aux_date,
                self.base_wpr_info.workshift_len,
            )
            aux_entrance_day_number = Utils.get_day_number_from_date(
                self.entrance_wpr_info.workshift_person_range,
                self.aux_date,
                self.entrance_wpr_info.workshift_len,
            )

            self.process_traverse(aux_base_day_number, aux_entrance_day_number)
            self.collisions_results.add_comparision()

            if Utils.has_collision(prev_base_schedule, self.current_entrance_schedule):
                self.collisions_results.add_collision()
                aux_collision_detail["prev"] = aux_base_day_number
        return aux_collision_detail

    def check_current_schedule(self):
        aux_collision_detail = {}
        current_base_schedule, _ = Utils.get_day_schedule(
            self.base_wpr_info, self.aux_date
        )

        if self.current_entrance_schedule:
            aux_base_day_number = Utils.get_day_number_from_date(
                self.base_wpr_info.workshift_person_range,
                self.aux_date,
                self.base_wpr_info.workshift_len,
            )
            aux_entrance_day_number = Utils.get_day_number_from_date(
                self.entrance_wpr_info.workshift_person_range,
                self.aux_date,
                self.entrance_wpr_info.workshift_len,
            )

            self.process_traverse(aux_base_day_number, aux_entrance_day_number)
            self.collisions_results.add_comparision()

            if Utils.has_collision(
                current_base_schedule, self.current_entrance_schedule
            ):
                self.collisions_results.add_collision()
                aux_collision_detail["current"] = aux_base_day_number
            return aux_collision_detail

    def check_next_schedule(self):
        aux_collision_detail = {}
        next_aux_date = self.aux_date + timedelta(days=1)
        next_base_schedule, _ = Utils.get_day_schedule(
            self.base_wpr_info, next_aux_date
        )

        if next_base_schedule and self.current_entrance_schedule_is_nightly:
            self.collisions_results.add_comparision()
            if Utils.has_collision(
                next_base_schedule,
                self.current_entrance_schedule,
            ):
                self.collisions_results.add_collision()
                aux_base_day_number = Utils.get_day_number_from_date(
                    self.base_wpr_info.workshift_person_range,
                    next_aux_date,
                    self.base_wpr_info.workshift_len,
                )
                aux_collision_detail["next"] = aux_base_day_number
        return aux_collision_detail

    def update_collisions_detail(self, collision_detail):
        if collision_detail:
            aux_entrance_day_number = Utils.get_day_number_from_date(
                self.entrance_wpr_info.workshift_person_range,
                self.aux_date,
                self.entrance_wpr_info.workshift_len,
            )

            self.collisions_results.update_collisions_detail(
                day_number=aux_entrance_day_number, collision_detail=collision_detail
            )

    def get_collisions(self):
        max_start_date, min_end_date = self.get_initial_range()
        self.aux_date = max_start_date

        while self.aux_date <= min_end_date:
            collision_detail = {}

            (
                self.current_entrance_schedule,
                self.current_entrance_schedule_is_nightly,
            ) = Utils.get_day_schedule(self.entrance_wpr_info, self.aux_date)

            if self.current_entrance_schedule:

                # Check prev
                aux_collision_detail = self.check_prev_schedule()
                collision_detail.update(aux_collision_detail)

                # Check current
                aux_collision_detail = self.check_current_schedule()
                collision_detail.update(aux_collision_detail)

                # Check next
                aux_collision_detail = self.check_next_schedule()
                collision_detail.update(aux_collision_detail)

                self.update_collisions_detail(collision_detail)

                if self.all_traversed and smart_collisions:
                    return self.collisions_results

                self.aux_date += timedelta(days=1)

        return self.collisions_results
