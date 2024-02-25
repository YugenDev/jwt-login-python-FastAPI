from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import Annotated

from jose import jwt, JWTError


SECRET_KEY = "a7bba3231648f6e791aa55c0af139564a106670a50715900b3ce2863e72bc06c"

db_users = {
    "yugoso": {
        "id": 0,
        "username": "yugoso",
        "password": "1234#hasshed"
    },
    "uretra": {
        "id": 1,
        "username": "uretra",
        "password": "4321#hasshed"
    }
}

app = FastAPI()

jinja2_templates = Jinja2Templates(directory="templates")

def get_user(username: str, db: list):
    if username in db:
        return db[username]

def auth(password: str, password_plane: str):
    password_clean= password.split("#")[0]
    if password_plane == password_clean:
        return True
    return False

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return jinja2_templates.TemplateResponse("index.html", {"request": request})


@app.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return jinja2_templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/users/login", )
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = get_user(username, db_users)
    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail="Alalo mr robot"
        )
    if not auth(user_data["password"], password):
        raise HTTPException(
            status_code=401,
            detail="Alalo mr robot eahhhh"
        )

    return {
        "username": username,
        "password": password
    }