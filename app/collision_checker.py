from datetime import timedelta

from app.collision_result import CollisionsResults
from app.data_classes import Range, WorkShiftPersonRangeInfo
from app.utils import Utils

smart_collisions = False


class CollisionChecker:
    def __init__(
        self,
        base_workshift_person_range_info: WorkShiftPersonRangeInfo,
        entrance_workshift_person_range_info: WorkShiftPersonRangeInfo,
    ) -> None:

        # If all the possible collision combination were checked
        self.all_traversed = False

        self.base_wpr_info = base_workshift_person_range_info
        self.entrance_wpr_info = entrance_workshift_person_range_info

        # The collision result class were all the result will be saved
        self.collisions_results = CollisionsResults()

        self.aux_entrance_day_number = None
        self.aux_entrance_date = None

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

        base_range = Range(base_start_date, base_end_date)
        entrance_range = Range(entrance_start_date, entrance_end_date)

        if base_range.collisioned(entrance_range):
            max_start_date = max(base_start_date, entrance_start_date) - timedelta(
                days=1
            )
            min_end_date = min(base_end_date, entrance_end_date) + timedelta(days=1)
        elif base_range.is_next_to_right(entrance_range):
            max_start_date = entrance_range.start_date
            min_end_date = entrance_range.start_date
        elif base_range.is_next_to_left(entrance_range):
            max_start_date = entrance_range.end_date
            min_end_date = entrance_range.end_date
        else:
            return None, None

        new_range = entrance_range.extract(max_start_date, min_end_date)

        return new_range.start_date, new_range.end_date

    def process_traverse(self, aux_base_day_number: int, aux_entrance_day_number: int):
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
                self.all_traversed = True

    def get_entrance_day_number(self):
        if (
            self.aux_entrance_day_number is None
            or self.aux_date != self.aux_entrance_date
        ):
            aux_entrance_day_number = Utils.get_day_number_from_date(
                self.entrance_wpr_info.workshift_person_range,
                self.aux_date,
                self.entrance_wpr_info.workshift_len,
            )
            self.aux_entrance_day_number = aux_entrance_day_number
            self.aux_entrance_date = self.aux_date
        return self.aux_entrance_day_number

    def check_prev_schedule(self):
        prev_aux_date = self.aux_date - timedelta(days=1)
        (
            prev_base_schedule,
            prev_base_schedule_is_nightly,
            aux_base_day_number,
        ) = Utils.get_day_schedule(self.base_wpr_info, prev_aux_date)

        if prev_base_schedule and prev_base_schedule_is_nightly:
            aux_entrance_day_number = self.get_entrance_day_number()

            self.process_traverse(aux_base_day_number, aux_entrance_day_number)
            self.collisions_results.add_comparision()

            if Utils.has_collision(prev_base_schedule, self.current_entrance_schedule):
                self.collisions_results.add_collision()

                self.collisions_results.append_collision_schedule(
                    self.current_entrance_schedule,
                    prev_base_schedule,
                )

                self.collisions_results.append_base_date(prev_base_schedule)

                self.collisions_results.update_day_number_collisions(
                    aux_entrance_day_number, aux_base_day_number, "prev"
                )

    def check_current_schedule(self):
        current_base_schedule, _, aux_base_day_number = Utils.get_day_schedule(
            self.base_wpr_info, self.aux_date
        )

        if self.current_entrance_schedule and current_base_schedule:

            aux_entrance_day_number = self.get_entrance_day_number()

            self.process_traverse(aux_base_day_number, aux_entrance_day_number)
            self.collisions_results.add_comparision()

            if Utils.has_collision(
                current_base_schedule, self.current_entrance_schedule
            ):
                self.collisions_results.add_collision()

                self.collisions_results.append_collision_schedule(
                    self.current_entrance_schedule,
                    current_base_schedule,
                )

                self.collisions_results.append_base_date(current_base_schedule)

                self.collisions_results.update_day_number_collisions(
                    aux_entrance_day_number, aux_base_day_number, "current"
                )

    def check_next_schedule(self):
        next_aux_date = self.aux_date + timedelta(days=1)
        next_base_schedule, _, aux_base_day_number = Utils.get_day_schedule(
            self.base_wpr_info, next_aux_date
        )

        if next_base_schedule and self.current_entrance_schedule_is_nightly:
            self.collisions_results.add_comparision()
            if Utils.has_collision(
                next_base_schedule,
                self.current_entrance_schedule,
            ):
                self.collisions_results.add_collision()

                aux_entrance_day_number = self.get_entrance_day_number()

                self.collisions_results.append_collision_schedule(
                    self.current_entrance_schedule,
                    next_base_schedule,
                )

                self.collisions_results.append_base_date(next_base_schedule)

                self.collisions_results.update_day_number_collisions(
                    aux_entrance_day_number, aux_base_day_number, "next"
                )

    def get_collisions(self):
        max_start_date, min_end_date = self.get_initial_range()
        self.aux_date = max_start_date

        while max_start_date is not None and self.aux_date <= min_end_date:
            (
                self.current_entrance_schedule,
                self.current_entrance_schedule_is_nightly,
                _,
            ) = Utils.get_day_schedule(self.entrance_wpr_info, self.aux_date)

            if self.current_entrance_schedule:

                # Check prev
                self.check_prev_schedule()

                # Check current
                self.check_current_schedule()

                # Check next
                self.check_next_schedule()

                if self.all_traversed and smart_collisions:
                    return self.collisions_results

                self.aux_date += timedelta(days=1)

        self.collisions_results.join_base_dates()

        self.collisions_results.get_new_base_ranges(
            Utils.str_to_date(self.base_wpr_info.workshift_person_range["start_date"]),
            Utils.str_to_date(self.base_wpr_info.workshift_person_range["end_date"]),
        )

        return self.collisions_results
