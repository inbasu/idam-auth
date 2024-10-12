from typing import Iterable


class IDAM:
    __roles: set[str]

    def __init__(self, client_id: str, clietn_secret: str) -> None:
        self.__client_id = client_id
        self.__clietn_secret = client_secret

    def set_roles(self, roles: Iterable) -> None:
        self.__roles.update(roles)


    def decod_token(self, token: str) -> dict:
