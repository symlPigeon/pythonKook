import websockets
import logging

class websocketHandler:
    def __init__(self, url: str, handler):
        self._url = url
        self._message_handler = handler
        self._onlineFlag = True

    async def createHandler(self):
        while self._onlineFlag:
            logging.info("Connecting to websocket server: {}".format(self._url))
            async with websockets.connect(self._url) as websocket:
                logging.info("Connected!")
                while self._onlineFlag:
                    try:
                        message = await websocket.recv()
                        self._message_handler(message)
                    except websockets.ConnectionClosedError:
                        logging.warning("Connection closed!")
                        break
                    except Exception as e:
                        logging.error("Unknown error!")
                        logging.error(str(e))
                        break
