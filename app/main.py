import time
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from app.classes import WorkShiftPersonRangeInfo
from app.collision_checker import CollisionChecker


class Data(BaseModel):
    workshifts: dict
    employees_info: list


app = FastAPI()


@app.post("/")
def read_root(data: Data):

    workshifts = data.workshifts
    employees_info = data.employees_info

    start = time.time()
    total_collisions = 0
    total_comparisions = 0

    total_collisions_detail = {}

    # process = CollisionProcess()
    for i in range(0, 3000):
        for employee_info in employees_info:
            base_workshifts_person_range = employee_info[
                "base_workshifts_person_rangecascask calks cklasmcklmasklcmaklsmcaslmclkasmcklasmkclmsamkcas"
            ]
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
                        workshift_len=len(workshifts[base_workshift_id].keys()),
                    )

                    entrance_workshift_person_range_info = WorkShiftPersonRangeInfo(
                        workshift=workshifts[entrance_workshift_id],
                        workshift_person_range=entrance_workshift_person_range,
                        workshift_len=len(workshifts[entrance_workshift_id].keys()),
                    )

                    checker = CollisionChecker(
                        base_workshift_person_range_info=base_workshift_person_range_info,
                        entrance_workshift_person_range_info=entrance_workshift_person_range_info,
                    )
                    collisions_result = checker.get_collisions()

                    key = f"{entrance_workshift_person_range['uuid']}_{base_workshift_person_range['uuid']}"

                    total_collisions_detail[key] = collisions_result.collisions_detail
                    total_collisions += collisions_result.collisions
                    total_comparisions += collisions_result.comparisions

    end = time.time()

    return {
        "time": end - start,
        "collisions": total_collisions,
        "employees_info": len(employees_info),
        "comparisions": total_comparisions,
        "total_collisions_detail": total_collisions_detail,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
