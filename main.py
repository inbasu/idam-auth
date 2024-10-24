import datetime
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
from idam import IDAM, TokenHandler, User

load_dotenv()
app = FastAPI(root_path="/auth")


idam = IDAM(
    client_id=os.getenv("client_id", ""),
    realm_id=os.getenv("realm_id", ""),
    redirect_uri="https://asset-tool.metro-cc.ru/auth/sso",
    client_secret=os.getenv("client_secret", ""),
)
token_handler = TokenHandler(
    secret="Lina Invers",
    algorithm="HS256",
    lifetime=datetime.timedelta(hours=8),
)


@app.get("/whoami")
async def get_user_data(request: Request, response: Response):
    if token := token_handler.decode_token(request.cookies.get("idam_user", None)):
        return token
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"401", "Unauthorized"}


@app.get("/login")
async def authatificate(redirect_uri: str = "/"):
    response = RedirectResponse(idam.code_url)
    response.set_cookie("redirect_uri", redirect_uri)
    return response


@app.get("/sso")
async def code_handling(request: Request, code: str | None = None):
    if code is None:
        return {}
    token = await idam.request_token(code)
    data = idam.decode_token(token)
    user: User = idam.create_user(data)
    response = RedirectResponse(request.cookies.get("redirect_uri"))
    response.set_cookie("idam_user", token_handler.generate_token(user.model_dump()))
    response.delete_cookie("redirect_uri")
    return response


@app.get("/logout")
async def delete_cookie(request: Request, response: Response):
    response = RedirectResponse(request.headers.get("referer", "/"))
    response.delete_cookie("idam_user")
    return response
