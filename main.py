# \venv\Scripts\activate

#python
from dataclasses import field
import imp
from typing import Optional
from enum import Enum


#Pydantic
from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber, HttpUrl

#FASTAPI
from fastapi import FastAPI, Query
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ..., 
        min_length= 1,
        max_length= 115
        )
    state: str = Field(
        ..., 
        min_length= 1,
        max_length= 115
        )
    country: str = Field(
        ..., 
        min_length= 1,
        max_length= 115
        )

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example = "Michelle"
        )
    last_name: str = Field(
        ..., 
        min_length= 1,
        max_length= 50,
        example = "Duque"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example = 27
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example = "black"
    )
    is_married: Optional[bool] = Field(
        default= None,
        example = False
    )
    email: EmailStr = Field(
        ...,
        min_length=1,
        example = "michelle@gmail.com"
    )
    payment_card_number: PaymentCardNumber = Field(
        ...,
        min_length=1,
        example = 53534523
    )
    httpurl: Optional[HttpUrl] = field(
        default=None,
        example = "https://twitter.com/home"
    )

    # class Config:
    #     schema_extra = {
    #         "Facundo": {
    #             "first_name": "Facundo",
    #             "last_name": "Garcia Martoni",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": False,
    #             "email": "facundo@gmail.com",
    #             "payment_card_number": 43244564563453,
    #             "httpurl": "https://platzi.com/"
    #         }
    #     }


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

#Validaciones: Request Body

@app.put("/person({person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(
        ...
        ),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results