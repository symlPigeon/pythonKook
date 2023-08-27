from typing import Callable

from pyKook.Utils.websocketHandler import websocketHandler


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class websocketMsgHandler():
    def __init__(self):
        self._event_handlers = {}
        self._ws_pool = {}
        
    def register(self, event: str, handler: Callable[[dict], dict]):
        self._event_handlers[event] = handler