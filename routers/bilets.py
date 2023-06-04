from fastapi import APIRouter
from db import execute_sql_data

router = APIRouter(
    prefix="/bilets",
    tags=["bilets"],
    responses={404: {"description": "Not found"}},
)

@router.get("/free_bilets_for_seance/{seance_id}")
async def read_bilets(seance_id):
    rs = execute_sql_data("(select ID_Места from Место) except (select Место from Билет where Сеанс = ?)", seance_id)
    return dict(
        items=rs.to_dict("records"),
        count=len(rs)
    )