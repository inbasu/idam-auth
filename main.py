import datetime
import os

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse

from idam import IDAM, TokenHandler

app = FastAPI(root_path="/auth")


idam = IDAM(
    client_id="",
    realm_id="",
    redirect_uri="",
    client_secret=os.getenv["IDAM_SECRET"],
)
token_handler = TokenHandler(
    secret="Lina Invers",
    algorithm="HS256",
    lifetime=datetime.timedelta(hours=8),
)


@app.get("/whoami")
async def get_user_data(request: Request, response: Response):
    if user_jwt_data := request.cookies.get("idam_user", False):
        return token_handler.decode_token(user_jwt_data)
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"401", "Unauthorized"}


@app.get("/login")
async def authatificate(request: Request, code: str | None = None):
    if code is not None:
        token = await idam.request_token(code)
        user_data = idam.decode_token(token)
        response = RedirectResponse(request.cookies.pop("redirect_uri"))
        response.set_cookie("idam_user", token_handler.generate_token(user_data))
        return response
    else:
        response = RedirectResponse(idam.code_url)
        response.set_cookie("redirect", request.headers.get("referer", ""))
        return response
