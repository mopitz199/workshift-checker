import uuid as uuid_library

from app.collision_result import CollisionsResults
from app.data_classes import Range, WorkShiftPersonRangeInfo


class GlobalCollisionResult:
    def __init__(self) -> None:

        """The hashmap with all the CollisionsResults of each pair with a unique collision"""
        self.global_collision_hash_map = {}

        """The dict that will have all the workshift person range(by their uuid)
        that should be deleted with the list of new workshift person range that should
        be created in order to have no collisions with the entrance workshift person range"""
        self.total_new_workshift_person_ranges = {}

    def get_key(
        self,
        base_workshift_person_range_info: WorkShiftPersonRangeInfo,
        entrance_workshift_person_range_info: WorkShiftPersonRangeInfo,
    ) -> str:
        base_workshift_uuid = base_workshift_person_range_info.workshift["uuid"]
        base_start_date = base_workshift_person_range_info.workshift_person_range[
            "start_date"
        ]
        base_end_date = base_workshift_person_range_info.workshift_person_range[
            "end_date"
        ]
        base_starting_day = base_workshift_person_range_info.workshift_person_range[
            "starting_day"
        ]

        entrance_workshift_uuid = entrance_workshift_person_range_info.workshift["uuid"]
        entrance_start_date = (
            entrance_workshift_person_range_info.workshift_person_range["start_date"]
        )
        entrance_end_date = entrance_workshift_person_range_info.workshift_person_range[
            "end_date"
        ]
        entrance_starting_day = (
            entrance_workshift_person_range_info.workshift_person_range["starting_day"]
        )

        base_key = f"{base_workshift_uuid}_{base_start_date}_{base_end_date}_{base_starting_day}"
        entrance_key = f"{entrance_workshift_uuid}_{entrance_start_date}_{entrance_end_date}_{entrance_starting_day}"

        key = f"{base_key}_{entrance_key}"
        return key

    def has_key(
        self,
        base_workshift_person_range_info: WorkShiftPersonRangeInfo,
        entrance_workshift_person_range_info: WorkShiftPersonRangeInfo,
    ) -> bool:
        key = self.get_key(
            base_workshift_person_range_info, entrance_workshift_person_range_info
        )
        if key in self.global_collision_hash_map:
            return self.global_collision_hash_map[key]
        else:
            return None

    def build_new_workshift_person_ranges(
        self,
        new_base_ranges: list,
        base_workshift_person_range_info: WorkShiftPersonRangeInfo,
    ) -> None:
        new_workshift_person_ranges = []
        for date_range in new_base_ranges:
            wpr = {
                "uuid": uuid_library.uuid4(),
                "start_date": str(date_range.start_date),
                "end_date": str(date_range.end_date),
                "wokshift_id": base_workshift_person_range_info.workshift["id"],
                "person_id": base_workshift_person_range_info.workshift_person_range[
                    "person_id"
                ],
            }
            new_workshift_person_ranges.append(wpr)

        uuid = base_workshift_person_range_info.workshift_person_range["uuid"]
        self.total_new_workshift_person_ranges[uuid] = new_workshift_person_ranges

    def add_result(
        self,
        base_workshift_person_range_info: WorkShiftPersonRangeInfo,
        entrance_workshift_person_range_info: WorkShiftPersonRangeInfo,
        result: CollisionsResults,
    ) -> None:
        key = self.get_key(
            base_workshift_person_range_info, entrance_workshift_person_range_info
        )
        self.global_collision_hash_map[key] = result
