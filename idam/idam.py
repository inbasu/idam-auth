import aiohttp
import jwt

from .model import User


class IDAM:

    _idam_url = ""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, realm_id: str) -> None:
        self.client_id = client_id
        self.__client_secret = client_secret
        self.data = {
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "user_type": "EMP",
            "realm_id": realm_id,
            "scope": f"clnt={self.client_id}",
        }

    @property
    def code_url(self) -> str:
        params = [f"{key}={value}" for key, value in self.data.items()]
        data = ["response_type=code", *params]
        return f"{self._idam_url}/authorize/api/oauth/authorization?{'&'.join(data)}"

    async def request_token(self, code: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=self._idam_url,
                auth=aiohttp.BasicAuth(self.client_id, self.__client_secret),
                data={
                    "grant_type": "code",
                    "code": code,
                    **self.data,
                },
            )
        result = await response.json()
        return result.get("access_token", None)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})

    def create_user(self, data: dict) -> User:
        roles = {list(item.keys())[0]: list(item.values())[0] for item in data["authorization"]}
        return User(
            email=data["email"],
            username=data["email"].split("@")[0],
            roles=list(roles.keys()),
            store_role=self._get_stores(roles),
        )

    def _get_stores(self, roles: dict[str, list]) -> list[str]:
        stores = []
        for store in roles.get("MCC_RU_INSIGHT_STORE_ROLE", [{"store": []}])[0]["store"]:
            if store == "9999":
                stores.append("8001")
            elif len(store) == 3:
                stores.append("1" + store)
            else:
                stores.append("10" + store)
        return stores
