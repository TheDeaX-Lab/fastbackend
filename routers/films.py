from fastapi import APIRouter
from db import execute_sql_data


router = APIRouter(
    prefix="/films",
    tags=["films"],
    responses={404: {"description": "Not found"}},
)

# Получение всех фильмов
@router.post("/")
async def get_films():
    rs = execute_sql_data("select * from Фильм")
    return dict(
        items=rs.to_dict("records"),
        count=len(rs),
        status="OK"
    )