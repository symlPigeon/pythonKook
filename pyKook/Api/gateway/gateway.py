from pyKook.Api.baseApi import baseAPI
from pyKook.Config.config import accountConfig
import logging


class getGatewayAPI(baseAPI):
    """
    获取Gateway接口
    """

    def __init__(self, config: accountConfig):
        super().__init__("/api/v3/gateway/index", "get", config, compress=0)

    def _render(self, data: dict) -> str:
        try:
            gateway = data["url"]
        except KeyError:
            logging.error("Invalid gateway response!")
            gateway = ""
        return gateway

    async def getGateway(self) -> str:
        """
        获取网关地址
        :return: 网关地址，如果获取失败了应该会得到一个空串
        """
        return await self.getData()
