import jwt
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from idam.idam import IDAM

idam = IDAM("", "", "", "")
app = FastAPI()


@app.get("/whoami")
async def get_user_data():
    pass


@app.get("/login")
async def authatificate(request: Request, code: str | None = None):
    if user := request.cookies.get("user"):
        return RedirectResponse("" + f"?user={user}")
    elif code is not None:
        token = idam.request_token(code=code)
        data = idam.decode_token(token)
        idam_user: dict = idam.create_user(data).model_dump()
        jwt_user = jwt.encode(idam_user, "", algorithm="HS256")
        response = RedirectResponse("" + f"?user={jwt_user}")
        response.set_cookie("user", jwt_user)
        request.cookies.pop("redirect")
        return response
    else:
        response = RedirectResponse(idam.code_url)
        response.set_cookie("redirect", "from")
        return response

    print(request.cookies.get("session"))
