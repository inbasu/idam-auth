from fastapi import FastAPI

app = FastAPI()


@app.get("/whoami")
async def get_user_data():
    pass


@app.get("/auth")
async def authatificate():
    pass


@app.get("/login")
async def login_user():
    pass
