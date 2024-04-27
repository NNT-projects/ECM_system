from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()


password = "1234"
database_name = "testDB"
DB_table = "data_engine"
username = "postgres"


class Item(BaseModel):
    parameters: str
    time_start: datetime
    time_end: datetime


@app.post("/items")
async def request_in_db(item: Item):
    connection = psycopg2.connect(
        dbname='testDB',
        user='postgres',
        host='localhost',
        password='1234',
        port='5432',
        cursor_factory=RealDictCursor
    )
    cursor = connection.cursor()

    cursor.execute(f"SELECT reportts, {item.parameters}" +
                   " " +
                   f"FROM {DB_table}" +
                   " " +
                   f"WHERE reportts >= '{item.time_start}' and reportts <= '{item.time_end}'" +
                   " " +
                   f"ORDER BY reportts")


    response = cursor.fetchall()

    cursor.close()
    connection.close()
    return response


