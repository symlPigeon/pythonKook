from typing import Tuple

from pyKook.Api.eventAPI.baseEventHandler import baseEventHandler as baseEventHandler
from pyKook.Api.objects import User as User
from pyKook.Utils.loggingTool import logging


class cardButtonClickMessageHandler(baseEventHandler):
    def __init__(self):
        super().__init__()
        self._event = "message_btn_click"

    def handle(self, msg: dict, bot_info: User) -> Tuple[dict, str]:
        logging.info("Card button clicked.")
        logging.info(
            "User {} clicked at card {} on button {}.".format(
                msg["extra"]["body"]["user_id"],
                msg["extra"]["body"]["msg_id"],
                msg["extra"]["body"]["value"],
            )
        )
        msg["author_id"] = msg["extra"]["body"]["user_id"]  # 采用触发事件者的身份替代系统
        msg["channel_id"] = msg["extra"]["body"]["target_id"]  # 标识位置，便于后续处理

        return msg, "cardClicked.{}.{}".format(
            msg["extra"]["body"]["msg_id"], msg["extra"]["body"]["value"]
        )
