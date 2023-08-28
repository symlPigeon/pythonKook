from pyKook.Api.baseApi import baseAPI, multiPageAPI
from pyKook.Config.config import accountConfig
from pyKook.Api.objects.User import User


class getCurrentUserInfoAPI(baseAPI):
    def __init__(self, conf: accountConfig):
        super().__init__("/api/v3/user/me", "get", conf)

    def _render(self, data: dict) -> dict:
        return data

    async def getUserInfo(self) -> User:
        user = await self.getData()
        return User(**user)


class getUserInfoAPI(baseAPI):
    def __init__(self, conf: accountConfig, user_id: str, guild_id: str | None):
        args = {"user_id": user_id}
        if guild_id:
            args["guild_id"] = guild_id
        super().__init__("/api/v3/user/view", "get", conf, **args)

    def _render(self, data: dict) -> dict:
        return data

    async def getUserInfo(self) -> User:
        user = await self.getData()
        return User(**user)
