from pyKook.Api.eventAPI.msgHandler import websocketMsgHandler


class baseEventHandler():
    def __init__(self, event: str):
        self._event = event
        websocketMsgHandler().register(self._event, self.handle)
        
    def handle(self, msg: dict):
        raise NotImplementedError