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


'''
@app.get("/ml")
def run_ml():
    fleet = ['BGU', 'BDU']
    for acnum in fleet:
        merged_predictions = make_predictions(csv_file_path, acnum)
        if merged_predictions is not None:
            merged_predictions.to_csv(f'data/X_with_predictions_{acnum}.csv', index=False)
            print("Predictions saved successfully.")
        else:
            print("Failed to make predictions.")
'''


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

    split_string_pos = item.pos.split(", ")
    quoted_string_pos = "', '".join(split_string_pos)
    pos = f"'{quoted_string_pos}'"

    split_string_acnum = item.acnum.split(", ")
    quoted_string_acnum = "', '".join(split_string_acnum)
    acnum = f"'{quoted_string_acnum}'"

    cursor.execute(f"SELECT reportts, acnum, pos, {item.parameters}" +
                   " " +
                   f"FROM {table_name}" +
                   " " +
                   f"WHERE reportts >= '{item.time_start}' and reportts <= '{item.time_end}'"
                   f" and acnum IN ({acnum})" +
                   f" and pos IN ({pos})" +
                   " " +
                   f"ORDER BY reportts")

    response = cursor.fetchall()

    cursor.close()
    connection.close()
    return response
