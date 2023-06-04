from fastapi import APIRouter
from db import execute_sql_data


router = APIRouter(
    prefix="/seances",
    tags=["seances"],
    responses={404: {"description": "Not found"}},
)

# Получение всех сеансов
@router.post("/")
async def get_seances():
    rs = execute_sql_data("select * from Сеанс where getdate() <= ДатаИВремя")
    return dict(
        items=rs.to_dict("records"),
        count=len(rs),
        status="OK"
    )