from uuid import uuid4

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from src.app.schemas import UserOut, UserAuth, TokenSchema, SystemUser
from src.app.utils import get_hashed_password, create_access_token, verify_password
from src.app.deps import get_current_user

from database import Person, get_db, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/signup', summary="Create new user", status_code=201, response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.login == data.login).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this login already exists"
        )
    user = Person(
        id=str(uuid4())
        , login=data.login
        , password=get_hashed_password(data.password)
        , salary=data.salary
        , change_date=data.change_date
    )
    db.add(user)
    db.commit()
    return UserOut(**{'salary': data.salary, 'change_date': data.change_date})


@app.post('/login', summary="Create access token for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Person).filter(Person.login == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password"
        )

    password = user.password
    if not verify_password(form_data.password, password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password"
        )

    return {
        "access_token": create_access_token(user.login)
    }


@app.get('/info', summary='Get info about user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
