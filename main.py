# uvicorn main:app --reload
# .\venv\Scripts\activate

#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI, File, Header, UploadFile, status, HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

app = FastAPI()

# Models

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

class personBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)
    

class Person(personBase): 
    password: str = Field(
        ..., 
        min_length=8,
        example = "soymiguel"
        )

    # class Config: 
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 21, 
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }

class PersonOut(personBase): 
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example = "miguel2021")
    message: str = Field(default="Login Succesfully!")



@app.get(
    path = "/", 
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary= "API Home Page"
    )
def home():
    """
    API Home Page

    This path operation takes you to the home page of the API

    No parameters are required

    Returns the message: Hellow World
    """ 
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path = "/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database
    
    Parameters:
    - Request body parameter:
        - **person: Person**  -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """ 
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary= "Get person details",
    deprecated= True
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocío"
        ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
): 
    """
    Show person details

    This path operation shows you the different details of a person as the name and age taken from the data base of the API

    Parameters:
        - Query Parameter:
            - **name: str** -> The name of the person you are looking for. It must be between 1 to 50 characters.
            - **age: int** -> The age of the person you are looking for. It's required. 

    Returns a json with the name and age of the person you are looking for.  
    """
    return {name: age}

# Validaciones: Path Parameters

persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}",
    status_code= status.HTTP_200_OK,
    tags=["Persons"],
    summary="Look for a person through the ID"
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
):
    """
    Shows if a person exits on the data base

    This path operation shows if the person you are looking for is in the data base of the API

    Parameters:
        - **person_id : int** -> It's the id of the person you are looking for. It is required. I must be greater than 0.
    
    It returns "person_id: It exists!" if the person you are looking for it was found in the data base of the Api, on the contrary it will show the next message "This person doesn't exist".
    """
    if person_id not in persons:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "This person doesn't exist"
            )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Persons"],
    summary="Update a person details"
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
): 
    """
    Update a person details

    This endpoint recevies a person_id and updates the information of that person

    Parameters:
        - Path parameter:
            - **person_id: int** -> It's the id of the person who you want to update the information. It is required. It must be greater than 0.
        - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color, is married, email, payment card number, favorite color and password.
        - **location: Location** -> A location model with city, state and country.

    Returns a JSON with the person's ID, its model and location.
    """
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person


#Forms

@app.post(
    path="/login",
    response_model= LoginOut,
    status_code= status.HTTP_200_OK,
    tags=["Persons"],
    summary="User Log In"
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    User Log In

    This path operation allows the user to log in to the app

    Parameters:
        - **username: str** -> This is the username to enter in the form. It is required.
        - **password: str** -> This is the password of the username to enter in the form. It is required.

    It returns a JSON with the username and a message    
    """
    return LoginOut(username=username)


#Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code= status.HTTP_200_OK,
    tags=["Contact"],
    summary="Contact"
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
        last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
    Contact

    This path operation allows the usert to contact the company

    Parameters:
        - user_agent: The browser that the user is using.
    - ads: The cookies that this website uses.
    - Request body parameter:
        - **first_name: str** -> This is the first name to enter in the form. It's required.
        - **last_name: str** -> This is the last name to enter in the form. It's required.
        - **email: EmailStr** -> This is the email to enter in the form. It's required.
        - **message: str** -> This is the message to enter in the form. It's required.

    It returns the information of the browser that the user is using for the app
    """
    return user_agent


#Files

@app.post(
    path="/post-image",
    tags=["Upload File"],
    summary= "Upload File"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Upload File

    This path operation allows you to upload a file in the app database.

    Parameters:
        - Request body parameter:
        - **image: UploadFile** -> This is the file to upload. It's required.

    It returns a JSON with the information of the file uploaded as the filename, format and size (kb)
    """
    return{
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }