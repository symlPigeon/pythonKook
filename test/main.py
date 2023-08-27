from pyKook.Config.config import accountConfig
from pyKook.Api.gateway.gateway import getGatewayAPI
from pyKook.Utils.websocketHandler import websocketHandler

from IGNORE_ME import token # private information
import asyncio

async def main():
    conf = accountConfig("Bot", token, "zh-CN")
    gateway = getGatewayAPI(conf)

    ws_handler = websocketHandler(gateway.getGateway(), handler=lambda msg: print(msg))
    await ws_handler.createHandler()


if __name__ == "__main__":
    asyncio.run(main())