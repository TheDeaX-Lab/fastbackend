from fastapi import APIRouter, Request
from db import execute_sql_data, encode_jwt
import jwt


router = APIRouter(
    prefix="/workers",
    tags=["workers"],
    responses={404: {"description": "Not found"}},
)

# Авторизация сотрудника
@router.post("/authorize")
async def authorize_user(request: Request):
    data = await request.json()
    rs = execute_sql_data(
        "select ID_Сотрудника from Сотрудник where ID_Сотрудника = ? and ФИО = ?", data["id"], data["fio"]
    )
    if len(rs) > 0:
        token = encode_jwt(dict(
            tp="worker",
            tp_id=int(rs["ID_Сотрудника"][0])
        ))
        return dict(
            status="OK",
            message="Авторизация пройдена, используйте токен для доступа к привелигированным функциям.",
            token=token
        )
    else:
        return dict(
            status="ERROR",
            message="Нет такого сотрудника в базе"
        )
