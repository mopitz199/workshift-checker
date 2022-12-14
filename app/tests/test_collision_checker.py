from datetime import datetime

from app.collision_checker import CollisionChecker
from app.data_classes import Range, WorkShiftPersonRangeInfo


class TestCollisionChecker:
    def set_up(
        self,
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

    def test_1(self):
        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-10",
            "2022-05-10",
            "2022-05-10",
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
        assert collisions_result.number_of_collisions == 0

    def test_2(self):
        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-10",
            "2022-05-11",
            "2022-05-11",
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

        assert collisions_result.number_of_collisions == 1
        assert collisions_result.number_of_comparisions == 1
        assert collisions_result.collision_ranges == [
            Range(
                datetime.strptime("2022-05-10", "%Y-%m-%d").date(),
                datetime.strptime("2022-05-10", "%Y-%m-%d").date(),
            )
        ]


class TestGetInitialRange:
    def set_up(
        self,
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

    def test_get_initial_range_single_day_and_single_day(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-10",
            "2022-05-11",
            "2022-05-11",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-11", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-11", "%Y-%m-%d").date()

    def test_get_initial_range_single_day_and_multiple_days(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-10",
            "2022-05-11",
            "2022-05-15",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-11", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-11", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_1(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-15",
            "2022-05-17",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-15", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-17", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_2(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-05",
            "2022-05-17",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-09", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-17", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_3(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-15",
            "2022-05-25",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-15", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-21", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_4(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-01",
            "2022-05-10",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-09", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-10", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_5(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-20",
            "2022-05-25",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-20", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-21", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_6(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-21",
            "2022-05-25",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-21", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-21", "%Y-%m-%d").date()

    def test_get_initial_range_multiple_days_and_multiple_days_case_7(self):

        data = self.set_up(
            "22:30",
            "09:30",
            True,
            "08:30",
            "18:30",
            False,
            "2022-05-10",
            "2022-5-20",
            "2022-05-01",
            "2022-05-09",
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

        initial_charge = checker.get_initial_range()

        assert initial_charge[0] == datetime.strptime("2022-05-09", "%Y-%m-%d").date()
        assert initial_charge[1] == datetime.strptime("2022-05-09", "%Y-%m-%d").date()
