from pyKook.Api.eventAPI.baseEventHandler import baseEventHandler as baseEventHandler
from pyKook.Api.objects import User as User
import logging


class chatMessageHandler(baseEventHandler):
    def __init__(self):
        super().__init__()
        self._event = "text_message"  # 这部分虽然需要“注册”，但是是拎出来单独操作的

    def handle(self, msg: dict, bot_info: User) -> str:
        bot_id = bot_info.getId()
        logging.info(bot_id)
        if bot_id in msg["mention"]:
            # 直接at机器人
            logging.info("Message at me.")
            print("message at me")
            return "isMentioned.atMe"
        if msg["mention_all"]:
            # at全体
            logging.info("Message at all.")
            return "isMentioned.atAll"
        if msg["mention_here"]:
            # at 在线成员
            logging.info("Message at here.")
            return "isMentioned.atHere"
        return "normalMessage"
