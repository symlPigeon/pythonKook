from pyKook.Api.baseApi import baseAPI
from pyKook.Config.config import accountConfig
from pyKook.Api.constants.messageType import MSG_TYPE
import logging

class sendChannelMsgAPI(baseAPI):
    def __init__(self, config: accountConfig, channel_id: str, content: str, quote: str | None = None, msg_type: int = MSG_TYPE.TEXT):
        body = { "target_id" : channel_id, "content" : content, "type" : int(msg_type) }
        if quote:
            body["quote"] = quote
        super().__init__("/api/v3/channel/message", "post", config, **body)

    def _render(self, data: dict) -> dict:
        return data

    def send(self):
        return self.getData()