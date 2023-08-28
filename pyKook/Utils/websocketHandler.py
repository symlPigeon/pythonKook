import websockets
import logging
import json
from typing import Callable


class websocketHandler:
    def __init__(self, url: str, handler: Callable[[dict], None]):
        self._url = url
        self._message_handler = handler
        self._onlineFlag = True
        self._ws_handler = None

    async def runHandler(self):
        while self._onlineFlag:
            logging.info("Connecting to websocket server: {}".format(self._url))
            async with websockets.connect(self._url) as websocket:
                self._ws_handler = websocket  # 留着方便外面关
                logging.info("Connected!")
                while self._onlineFlag:
                    try:
                        message = await websocket.recv()
                        # 理论上这里传回来的是一个str
                        if type(message) == bytes:
                            logging.debug("Message is bytes, decoding...")
                            message = message.decode()
                        message = json.loads(message)
                        self._message_handler(message)
                    except json.JSONDecodeError:
                        logging.error(
                            "JSON decode error! Seems server sent a wrong message?"
                        )
                        logging.error("Message: {}".format(message))
                    except websockets.ConnectionClosedOK:
                        logging.warning(
                            "Connection closed! [Normal Connection Closure]"
                        )
                    except websockets.ConnectionClosedError:
                        logging.error(
                            "Connection closed! [Network Error or Protocol Error]"
                        )
                    except Exception as e:
                        logging.error("Unknown error!")
                        logging.error(str(e))
                        break

    def stopHandler(self):
        self._onlineFlag = False
        if self._ws_handler:
            self._ws_handler.close()
        logging.info("Stopping websocket handler...")
