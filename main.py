# \venv\Scripts\activate

#python
from typing import Optional


#Pydantic
from pydantic import BaseModel

#FASTAPI
from fastapi import FastAPI

app = FastAPI()

#Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

@app.post("/person/new")
def create_person(person: Person):
    return person