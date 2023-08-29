import asyncio

import websockets
import logging
import json
from typing import Callable


class websocketHandler:
    def __init__(self, url: str, handler: callable):
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

                        # 目前的消息格式是这样的：
                        # {
                        #     "s" : 1,  // int, 信令，详情参照信令说明
                        #     "d" : {}, // 数据字段mixed
                        #     "sn" : 0, // int, 该字段并不一定有，只在s=0时有，与webhook一致。
                        # }
                        if message["s"] == 0:  # 仅交由上层处理事件包
                            message = message["d"]
                            await self._message_handler(message)
                    except json.JSONDecodeError:
                        logging.error(
                            "JSON decode error! Seems server sent a wrong message?"
                        )
                        logging.error("Message: {}".format(message))
                    except websockets.ConnectionClosedOK:
                        logging.warning(
                            "Connection closed! [Normal Connection Closure]"
                        )
                        await asyncio.sleep(3)
                    except websockets.ConnectionClosedError:
                        logging.error(
                            "Connection closed! [Network Error or Protocol Error]"
                        )
                        await asyncio.sleep(3)
                    except Exception as e:
                        logging.error("Unknown error!")
                        logging.error(str(e))
                        await asyncio.sleep(3)
                        break

    def stopHandler(self):
        self._onlineFlag = False
        if self._ws_handler:
            self._ws_handler.close()
        logging.info("Stopping websocket handler...")
