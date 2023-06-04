import pyodbc
import pandas
from threading import Lock
import jwt

with open("securecode.txt", "r", encoding="utf8") as f:
    secure_code = f.read()

def encode_jwt(value):
    return jwt.encode(
        value,
        secure_code,
        algorithm="HS256"
    )

def decode_jwt(jw_token):
    return jwt.decode(
        jw_token,
        secure_code,
        algorithms=["HS256"]
    )

db_lock = Lock()
# sqlsa
# 12345
# sa


conn = pyodbc.connect(
    (
        "DRIVER={SQL Server};"
        r"SERVER=DESKTOP-M6R1M10\SQLSA;"
        "DATABASE=Кино;"
        "UID=sa;"
        "PWD=12345;"
    )
)

def execute_sql_data(sql, *params):
    with db_lock:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return pandas.DataFrame(
                list(map(list, rows)),
                columns=list(map(lambda x: x[0], cursor.description))
            )

def execute_sql_mutual(sql, *params):
    with db_lock:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()

# if __name__ == "__main__":
#     print(execute_sql_data("select count(*) from Билет").iloc[0][0])
    # print(encode_jwt(dict(tp="user", tp_id=3)))