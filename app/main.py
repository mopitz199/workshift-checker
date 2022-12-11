import time
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from app.collision_checker import CollisionChecker
from app.collision_global_result import GlobalCollisionResult
from app.data_classes import WorkShiftPersonRangeInfo


class Data(BaseModel):
    workshifts: dict
    employees_info: list


app = FastAPI()


@app.post("/")
def collision_checker(data: Data):

    workshifts = data.workshifts
    employees_info = data.employees_info

    global_collision_result = GlobalCollisionResult()

    start = time.time()
    total_collisions = 0
    total_number_of_comparisions = 0
    global_day_number_collisions = {}
    total_schedules_detail = {}

    for i in range(0, 1):
        for employee_info in employees_info:
            base_workshifts_person_range = employee_info["base_workshifts_person_range"]
            entrance_workshifts_person_range = employee_info[
                "entrance_workshifts_person_range"
            ]

            for entrance_workshift_person_range in entrance_workshifts_person_range:
                for base_workshift_person_range in base_workshifts_person_range:

                    base_workshift_id = str(base_workshift_person_range["workshift"])
                    entrance_workshift_id = str(
                        entrance_workshift_person_range["workshift"]
                    )

                    base_workshift_person_range_info = WorkShiftPersonRangeInfo(
                        workshift=workshifts[base_workshift_id],
                        workshift_person_range=base_workshift_person_range,
                        workshift_len=len(workshifts[base_workshift_id]["days"].keys()),
                    )

                    entrance_workshift_person_range_info = WorkShiftPersonRangeInfo(
                        workshift=workshifts[entrance_workshift_id],
                        workshift_person_range=entrance_workshift_person_range,
                        workshift_len=len(
                            workshifts[entrance_workshift_id]["days"].keys()
                        ),
                    )

                    collisions_result = global_collision_result.has_key(
                        base_workshift_person_range_info,
                        entrance_workshift_person_range_info,
                    )
                    if not collisions_result:
                        checker = CollisionChecker(
                            base_workshift_person_range_info=base_workshift_person_range_info,
                            entrance_workshift_person_range_info=entrance_workshift_person_range_info,
                        )
                        collisions_result = checker.get_collisions()

                        global_collision_result.add_result(
                            base_workshift_person_range_info,
                            entrance_workshift_person_range_info,
                            collisions_result,
                        )

                    if collisions_result.number_of_collisions > 0:
                        global_collision_result.build_new_workshift_person_ranges(
                            collisions_result.new_base_ranges,
                            base_workshift_person_range_info,
                        )

                    key = f"{entrance_workshift_person_range['uuid']}_{base_workshift_person_range['uuid']}"

                    global_day_number_collisions[
                        key
                    ] = collisions_result.day_number_collisions
                    total_collisions += collisions_result.number_of_collisions
                    total_number_of_comparisions += (
                        collisions_result.number_of_comparisions
                    )
                    total_schedules_detail[key] = collisions_result.collision_schedules

    end = time.time()

    return {
        "time": end - start,
        "collisions": total_collisions,
        "employees_info": len(employees_info),
        "comparisions": total_number_of_comparisions,
        # "global_day_number_collisions": global_day_number_collisions,
        # "total_schedules_detail": total_schedules_detail,
        "total_new_workshift_person_ranges": global_collision_result.total_new_workshift_person_ranges,
    }
