import pyodbc
import pandas
from threading import Lock

db_lock = Lock()
# sqlsa
# 12345
# sa


conn = pyodbc.connect(
    (
        "DRIVER={SQL Server};"
        r"SERVER=DESKTOP-M6R1M10\SQLSA;"
        "DATABASE=Кино;"
        r"UID=sa;"
        r"PWD=12345;"
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
#     print(execute_sql_data("select * from Билет"))