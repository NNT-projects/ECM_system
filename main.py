from datetime import datetime
from typing import Optional, List

import psycopg2

import os

from fastapi import FastAPI, Query
from fastapi.params import Path
from pydantic import BaseModel

app = FastAPI()

users = []
items = []

db_name = os.getenv('POSTGRES_DB', 'testDB')

connection = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB', 'testDB'),
    user=os.getenv('POSTGRES_USER', 'user'),
    host=os.getenv('POSTGRES_HOST', 'project-db'),
    password=os.getenv('POSTGRES_PASSWORD', '123'),
    port=os.getenv('POSTGRES_PORT', '5432')
)

cursor = connection.cursor()

create_table_query = '''CREATE TABLE IF NOT EXISTS my_table (
                            id SERIAL PRIMARY KEY,
                            field1 VARCHAR(255),
                            field2 VARCHAR(255)
                        );'''

cursor.execute(create_table_query)
connection.commit()

# Вставка пары значений в таблицу
insert_query = f"INSERT INTO my_table (field1, field2) VALUES (%s, %s);"
record_to_insert = ('значение1', 'значение2')
cursor.execute(insert_query, record_to_insert)
connection.commit()

# Закрытие курсора и соединения
cursor.close()
connection.close()


class User(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


class Item(BaseModel):
    parameters: str
    time_start: datetime
    time_end: datetime

@app.post("/items")
async def request_in_db(item: Item):

    return "SELECT " + item.parameters + " FROM " + db_name


@app.get("/items", response_model=List[Item])
async def return_items():
    return items


@app.get("/users", response_model=List[User])
async def root():
    return users


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return "Successfully created"


@app.get("/users/{id}")
async def get_user(id: int = Path(..., description="The ID of user you want to get"),
                   q: str = Query(None, max_length=5)):
    return {"user": users[id], "query": q}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
