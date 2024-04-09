from typing import Optional, List

from fastapi import FastAPI, Query
from fastapi.params import Path
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str]


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
