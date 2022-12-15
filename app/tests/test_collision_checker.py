from datetime import datetime

import pytest

from app.collision_checker import CollisionChecker
from app.data_classes import Range, WorkShiftPersonRangeInfo


def set_up(
    start_time_1,
    end_time_1,
    is_nightly_1,
    start_time_2,
    end_time_2,
    is_nightly_2,
    start_date_1,
    end_date_1,
    start_date_2,
    end_date_2,
):
    data = {
        "workshifts": {
            "1": {
                "id": 1,
                "uuid": "547f3c54-267d-4720-b6a2-de420662135c",
                "days": {
                    "1": {
                        "start_time": start_time_1,
                        "end_time": end_time_1,
                        "is_nightly": is_nightly_1,
                    }
                },
            },
            "2": {
                "id": 2,
                "uuid": "a9a1fb94-f932-4373-8afa-de5684ac6827",
                "days": {
                    "1": {
                        "start_time": start_time_2,
                        "end_time": end_time_2,
                        "is_nightly": is_nightly_2,
                    }
                },
            },
        },
        "employees_info": [
            {
                "person": 1,
                "base_workshifts_person_range": [
                    {
                        "id": 1,
                        "uuid": "a49a8c27-9caa-4379-a2b9-cf29d0adf471",
                        "person_id": 1,
                        "workshift_id": 1,
                        "starting_day": 1,
                        "start_date": start_date_1,
                        "end_date": end_date_1,
                    }
                ],
                "entrance_workshifts_person_range": [
                    {
                        "uuid": "8a2695d8-33d4-48c5-97d2-0cca79c45162",
                        "person_id": 1,
                        "workshift_id": 2,
                        "starting_day": 1,
                        "start_date": start_date_2,
                        "end_date": end_date_2,
                    }
                ],
            }
        ],
    }
    return data


class TestCollisionChecker:
    @pytest.mark.parametrize(
        "start_time1, end_time1, is_nightly1, start_time2, end_time2, is_nightly2,  start_date1, end_date1, start_date2, end_date2, result",
        [
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-10",
                "2022-05-10",
                "2022-05-10",
                0,
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-10",
                "2022-05-11",
                "2022-05-11",
                1,
            ),
        ],
    )
    def test_1(
        self,
        start_time1,
        end_time1,
        is_nightly1,
        start_time2,
        end_time2,
        is_nightly2,
        start_date1,
        end_date1,
        start_date2,
        end_date2,
        result,
    ):
        data = set_up(
            start_time1,
            end_time1,
            is_nightly1,
            start_time2,
            end_time2,
            is_nightly2,
            start_date1,
            end_date1,
            start_date2,
            end_date2,
        )

        base_workshift_person_range_info = WorkShiftPersonRangeInfo(
            workshift=data["workshifts"]["1"],
            workshift_person_range=data["employees_info"][0][
                "base_workshifts_person_range"
            ][0],
            workshift_len=len(data["workshifts"]["1"]["days"].keys()),
        )

        entrance_workshift_person_range_info = WorkShiftPersonRangeInfo(
            workshift=data["workshifts"]["2"],
            workshift_person_range=data["employees_info"][0][
                "entrance_workshifts_person_range"
            ][0],
            workshift_len=len(data["workshifts"]["2"]["days"].keys()),
        )

        checker = CollisionChecker(
            base_workshift_person_range_info=base_workshift_person_range_info,
            entrance_workshift_person_range_info=entrance_workshift_person_range_info,
        )
        collisions_result = checker.get_collisions()
        assert collisions_result.number_of_collisions == result


class TestGetInitialRange:
    @pytest.mark.parametrize(
        "start_time1, end_time1, is_nightly1, start_time2, end_time2, is_nightly2,  start_date1, end_date1, start_date2, end_date2, initial_range_0, initial_range_1",
        [
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-10",
                "2022-05-11",
                "2022-05-11",
                "2022-05-11",
                "2022-05-11",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-10",
                "2022-05-11",
                "2022-05-15",
                "2022-05-11",
                "2022-05-11",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-15",
                "2022-05-17",
                "2022-05-15",
                "2022-05-17",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-05",
                "2022-05-17",
                "2022-05-09",
                "2022-05-17",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-15",
                "2022-05-25",
                "2022-05-15",
                "2022-05-21",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-01",
                "2022-05-10",
                "2022-05-09",
                "2022-05-10",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-20",
                "2022-05-25",
                "2022-05-20",
                "2022-05-21",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-21",
                "2022-05-25",
                "2022-05-21",
                "2022-05-21",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-01",
                "2022-05-09",
                "2022-05-09",
                "2022-05-09",
            ),
            (
                "22:30",
                "09:30",
                True,
                "08:30",
                "18:30",
                False,
                "2022-05-10",
                "2022-05-20",
                "2022-05-24",
                "2022-05-28",
                None,
                None,
            ),
        ],
    )
    def test_get_initial_range(
        self,
        start_time1,
        end_time1,
        is_nightly1,
        start_time2,
        end_time2,
        is_nightly2,
        start_date1,
        end_date1,
        start_date2,
        end_date2,
        initial_range_0,
        initial_range_1,
    ):

        data = set_up(
            start_time1,
            end_time1,
            is_nightly1,
            start_time2,
            end_time2,
            is_nightly2,
            start_date1,
            end_date1,
            start_date2,
            end_date2,
        )

        base_workshift_person_range_info = WorkShiftPersonRangeInfo(
            workshift=data["workshifts"]["1"],
            workshift_person_range=data["employees_info"][0][
                "base_workshifts_person_range"
            ][0],
            workshift_len=len(data["workshifts"]["1"]["days"].keys()),
        )

        entrance_workshift_person_range_info = WorkShiftPersonRangeInfo(
            workshift=data["workshifts"]["2"],
            workshift_person_range=data["employees_info"][0][
                "entrance_workshifts_person_range"
            ][0],
            workshift_len=len(data["workshifts"]["2"]["days"].keys()),
        )

        checker = CollisionChecker(
            base_workshift_person_range_info=base_workshift_person_range_info,
            entrance_workshift_person_range_info=entrance_workshift_person_range_info,
        )

        initial_range = checker.get_initial_range()

        if initial_range_0 is not None or initial_range_1 is not None:
            assert (
                initial_range[0]
                == datetime.strptime(initial_range_0, "%Y-%m-%d").date()
            )
            assert (
                initial_range[1]
                == datetime.strptime(initial_range_1, "%Y-%m-%d").date()
            )
        else:
            assert initial_range[0] is None
            assert initial_range[1] is None
