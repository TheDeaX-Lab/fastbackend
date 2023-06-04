from fastapi import APIRouter, Request
from db import execute_sql_data, execute_sql_mutual, decode_jwt

router = APIRouter(
    prefix="/bilets",
    tags=["bilets"],
    responses={404: {"description": "Not found"}},
)

@router.get("/free_places_for_seance/{seance_id}")
async def free_places_for_seance(seance_id):
    if execute_sql_data("select count(*) from Сеанс where ID_Сеанса = ?", seance_id).iloc[0][0] == 0:
        return dict(
            status="ERROR",
            message="Такого сеанса нет"
        )
    rs = execute_sql_data("(select ID_Места from Место) except (select Место from Билет where Сеанс = ?)", seance_id)
    return dict(
        status="OK",
        items=list(rs["ID_Места"]),
        count=len(rs),
        countAll=int(execute_sql_data("select count(*) from Место").iloc[0][0])
    )

@router.post("/add_bilet")
async def add_bilet(request: Request):
    data = await request.json()
    try:
        user = decode_jwt(data["token"])
        user["tp"]
        user["tp_id"]
    except:
        return dict(
            status="ERROR",
            message="Некорректный token"
        )
    if execute_sql_data("select count(*) from Сеанс where ID_Сеанса = ?", data["seance"]).iloc[0][0] == 0:
        return dict(
            status="ERROR",
            message="Такого сеанса нет"
        )
    if execute_sql_data("select count(*) from Место where ID_Места = ?", data["place"]).iloc[0][0] == 0:
        return dict(
            status="ERROR",
            message="Такого места нет"
        )
    if user["tp"] == "user":
        if execute_sql_data("select count(*) from Билет where Сеанс = ? and Место = ?", data["seance"], data["place"]).iloc[0][0] > 0:
            return dict(
                status="ERROR",
                message="Билет не может быть зарегистрирован на указанное место в сеансе"
            )
        else:
            execute_sql_mutual("insert into Билет(Статус, Место, Стоимость, Сеанс, Покупатель) values (?, ?, ?, ?, ?)",
                "Забронирован" if not data["is_buy"] else "Куплен",
                data["place"],
                execute_sql_data("""select Цена * (
                    select [множитель стоимости]
                    from Место
                    where ID_Места = ?
                ) from Сеанс where ID_Сеанса = ?""", data["place"], data["seance"]).iloc[0][0],
                data["seance"],
                user["tp_id"]
            )
            return dict(
                status="OK",
                message="Билет зарегистрирован"
            )
    else:
        return dict(
            status="ERROR",
            message="У вас нет доступа к данной функции"
        )

@router.post("/get_bilets")
async def get_bilets(request: Request):
    data = await request.json()
    try:
        user = decode_jwt(data["token"])
        user["tp"]
        user["tp_id"]
    except:
        return dict(
            status="ERROR",
            message="Некорректный token"
        )
    if user["tp"] == "user":
        rs = execute_sql_data("select * from Билет join Сеанс on Сеанс.ID_Сеанса = Билет.Сеанс join Фильм on Сеанс.Фильм = Фильм.ID_Фильма where Покупатель = ?", user["tp_id"])
        return dict(
            status="OK",
            items=rs.to_dict("records"),
            count=len(rs)
        )
    else:
        return dict(
            status="ERROR",
            message="У вас нет доступа к данной функции"
        )


@router.post("/apply_bilet")
async def get_bilets(request: Request):
    data = await request.json()
    try:
        user = decode_jwt(data["token"])
        user["tp"]
        user["tp_id"]
    except:
        return dict(
            status="ERROR",
            message="Некорректный token"
        )
    if execute_sql_data("select count(*) from Билет where ID_Билета = ? and Статус = 'Забронирован'", data["id_bilet"]).iloc[0][0] == 0:
        return dict(
            status="ERROR",
            message="Такого билета нет"
        )
    if user["tp"] == "worker":
        execute_sql_mutual(
            "update Билет set Статус = 'Куплен' where ID_Билета = ?", data["id_bilet"]
        )
        execute_sql_mutual(
            "insert into ПродажаБилета(Сотрудник, Билет) values (?, ?)", user["tp_id"], data["id_bilet"]
        )
        return dict(
            status="OK",
            message="Статус билета изменен на куплен"
        )
    else:
        return dict(
            status="ERROR",
            message="У вас нет доступа к данной функции"
        )