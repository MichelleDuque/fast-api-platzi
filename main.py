# \venv\Scripts\activate

#python
from typing import Optional


#Pydantic
from pydantic import BaseModel

#FASTAPI
from fastapi import FastAPI, Query
from fastapi import Body, Query, Path

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
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required."
        )
):
    return{name: age}


#Validations: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person ID",
        description="This is the person ID. It's required and must be greater than 0."
        )
):
    return{person_id: "It exits!"}