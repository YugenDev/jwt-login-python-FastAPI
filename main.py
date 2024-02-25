from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta

from typing import Annotated

from jose import jwt, JWTError


SECRET_KEY = "a7bba3231648f6e791aa55c0af139564a106670a50715900b3ce2863e72bc06c"
TOKEN_SECONDS_EXP = 20

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

def create_token(data: list):
    data_token = data.copy()
    data_token["exp"] = datetime.utcnow() + timedelta(seconds=TOKEN_SECONDS_EXP)
    token_jwt = jwt.encode(data_token, key=SECRET_KEY, algorithm="HS256")
    return token_jwt

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
    token = create_token({"username": user_data["username"]})
    return RedirectResponse(
        "/users/dashboard",
        status_code=302,
        headers={"set-cookie": f"accsess_token={token}; Max-Age = {TOKEN_SECONDS_EXP}"}

    )