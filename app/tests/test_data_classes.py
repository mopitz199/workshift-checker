from datetime import datetime

import pytest

from app.data_classes import Range


class TestRangeCollisioned:
    @pytest.mark.parametrize(
        "start_date1,end_date1,start_date2,end_date2,result",
        [
            ("2022-05-10", "2022-05-10", "2022-05-10", "2022-05-10", True),
            ("2022-05-10", "2022-05-15", "2022-05-10", "2022-05-15", True),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-14", True),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-20", True),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-12", True),
            ("2022-05-10", "2022-05-15", "2022-05-16", "2022-05-18", False),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-09", False),
            ("2022-05-10", "2022-05-15", "2022-05-20", "2022-05-25", False),
            ("2022-05-10", "2022-05-15", "2022-05-01", "2022-05-05", False),
        ],
    )
    def test_collisioned(self, start_date1, end_date1, start_date2, end_date2, result):
        r1 = Range(
            datetime.strptime(start_date1, "%Y-%m-%d").date(),
            datetime.strptime(end_date1, "%Y-%m-%d").date(),
        )

        r2 = Range(
            datetime.strptime(start_date2, "%Y-%m-%d").date(),
            datetime.strptime(end_date2, "%Y-%m-%d").date(),
        )
        assert r1.collisioned(r2) is result

    @pytest.mark.parametrize(
        "start_date1,end_date1,start_date2,end_date2,result",
        [
            ("2022-05-10", "2022-05-10", "2022-05-10", "2022-05-10", False),
            ("2022-05-10", "2022-05-15", "2022-05-10", "2022-05-15", False),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-14", False),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-20", False),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-12", False),
            ("2022-05-10", "2022-05-15", "2022-05-16", "2022-05-18", True),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-09", False),
            ("2022-05-10", "2022-05-15", "2022-05-20", "2022-05-25", False),
            ("2022-05-10", "2022-05-15", "2022-05-01", "2022-05-05", False),
        ],
    )
    def test_is_next_to_right(
        self, start_date1, end_date1, start_date2, end_date2, result
    ):
        r1 = Range(
            datetime.strptime(start_date1, "%Y-%m-%d").date(),
            datetime.strptime(end_date1, "%Y-%m-%d").date(),
        )

        r2 = Range(
            datetime.strptime(start_date2, "%Y-%m-%d").date(),
            datetime.strptime(end_date2, "%Y-%m-%d").date(),
        )
        assert r1.is_next_to_right(r2) is result

    @pytest.mark.parametrize(
        "start_date1,end_date1,start_date2,end_date2,result",
        [
            ("2022-05-10", "2022-05-10", "2022-05-10", "2022-05-10", False),
            ("2022-05-10", "2022-05-15", "2022-05-10", "2022-05-15", False),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-14", False),
            ("2022-05-10", "2022-05-15", "2022-05-13", "2022-05-20", False),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-12", False),
            ("2022-05-10", "2022-05-15", "2022-05-16", "2022-05-18", False),
            ("2022-05-10", "2022-05-15", "2022-05-05", "2022-05-09", True),
            ("2022-05-10", "2022-05-15", "2022-05-20", "2022-05-25", False),
            ("2022-05-10", "2022-05-15", "2022-05-01", "2022-05-05", False),
        ],
    )
    def test_is_next_to_left(
        self, start_date1, end_date1, start_date2, end_date2, result
    ):
        r1 = Range(
            datetime.strptime(start_date1, "%Y-%m-%d").date(),
            datetime.strptime(end_date1, "%Y-%m-%d").date(),
        )

        r2 = Range(
            datetime.strptime(start_date2, "%Y-%m-%d").date(),
            datetime.strptime(end_date2, "%Y-%m-%d").date(),
        )
        assert r1.is_next_to_left(r2) is result
