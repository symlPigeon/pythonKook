import logging

from pyKook.Api.baseApi import multiPageAPI
from pyKook.Config.accountConfig import accountConfig


class getGameListAPI(multiPageAPI):
    def __init__(self, config: accountConfig):
        logging.warning(
            "The `getGameListAPI` may contain some bugs, please use it carefully!"
        )
        super().__init__("/api/v3/game", "get", config)

    def _render(self, data: dict) -> list:
        return data["items"]
