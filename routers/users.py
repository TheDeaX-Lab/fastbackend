from fastapi import APIRouter, Request
from db import execute_sql_data, execute_sql_mutual, encode_jwt
import jwt


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Регистрация пользователя
@router.post("/register")
async def register_user(request: Request):
    data = await request.json()
    if execute_sql_data("select count(*) from Покупатель where [эл.почта] = ?", data["email"]).iloc[0][0] > 0:
        return dict(
            status="ERROR",
            message="Такой пользователь с таким email существует"
        )
    if execute_sql_data("select count(*) from Покупатель where телефон = ?", data["phone"]).iloc[0][0] > 0:
        return dict(
            status="ERROR",
            message="Такой пользователь с таким телефоном существует"
        )
    execute_sql_mutual("""
    INSERT INTO Покупатель ([эл.почта], телефон, Возраст)
    VALUES (?, ?, ?)
    """, data["email"], data["phone"], data["age"])

    return dict(
        status="OK",
        message="Пользователь успешно зарегистрирован"
    )

# Авторизация пользователя
@router.post("/authorize")
async def authorize_user(request: Request):
    data = await request.json()
    rs = execute_sql_data(
        "select id_покупателя from Покупатель where телефон = ?", data["phone"]
    )
    if len(rs) > 0:
        token = encode_jwt(dict(
            tp="user",
            tp_id=int(rs["id_покупателя"][0])
        ))
        return dict(
            status="OK",
            message="Авторизация пройдена, используйте токен для доступа к привелигированным функциям.",
            token=token
        )
    else:
        return dict(
            status="ERROR",
            message="Нет такого телефона в базе"
        )
