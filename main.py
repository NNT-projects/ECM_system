from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from params_for_DB import *


app = FastAPI()


class Item(BaseModel):
    parameters: str
    time_start: datetime
    time_end: datetime
    acnum: str
    pos: str


@app.post("/items")
async def request_in_db(item: Item):
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password,
        port=port,
        cursor_factory=RealDictCursor
    )
    cursor = connection.cursor()

    split_string = item.pos.split(", ")
    quoted_string = "', '".join(split_string)
    pos = f"'{quoted_string}'"

    cursor.execute(f"SELECT reportts, acnum, pos, {item.parameters}" +
                   " " +
                   f"FROM {table_name}" +
                   " " +
                   f"WHERE reportts >= '{item.time_start}' and reportts <= '{item.time_end}'"
                   f" and acnum = '{item.acnum}'"
                   f" and pos IN ({pos})" +
                   " " +
                   f"ORDER BY reportts")

    response = cursor.fetchall()

    cursor.close()
    connection.close()
    return response
