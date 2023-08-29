from pyKook.Api.baseApi import baseAPI
from pyKook.Config.accountConfig import accountConfig
from pyKook.Api.constants.messageType import MSG_TYPE
import logging


class sendChannelMsgAPI(baseAPI):
    def __init__(
        self,
        config: accountConfig,
        channel_id: str,
        content: str,
        quote: str | None = None,
        msg_type: int = MSG_TYPE.TEXT,
    ):
        body = {"target_id": channel_id, "content": content, "type": int(msg_type)}
        if quote:
            body["quote"] = quote
        super().__init__("/api/v3/channel/message", "post", config, **body)

    def _render(self, data: dict) -> dict:
        return data

    async def send(self):
        return await self.getData()


class deleteChannelMsgAPI(baseAPI):
    def __init__(self, config: accountConfig, msg_id: str):
        super().__init__("/api/v3/message/delete", "post", config, msg_id=msg_id)

    def _render(self, data: dict) -> dict:
        return {}

    async def delete(self):
        return await self.getData()
