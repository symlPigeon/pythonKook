from pyKook.Config.config import accountConfig
from pyKook.Utils.httpHandler import httpHandler
import logging

baseUrl = "https://www.kookapp.cn"


class baseAPI:
    def __init__(self, url: str, method: str, config: accountConfig, **args):
        self._url = baseUrl + url
        self._method = method
        self._config = config
        self._args = args
        self._handler = httpHandler(self._url, self._method, self._config, self._args)

    def _render(self, data: dict):
        raise NotImplementedError("This method must be implemented by subclass!")

    def _request(self) -> dict:
        logging.info("Requesting to {}".format(self._url))
        return self._handler.request()

    def setArgs(self, **args):
        self._args = args
        self._handler.setArgs(self._args)

    def addArgs(self, **args):
        for key in args.keys():
            self._args[key] = args[key]
        self._handler.setArgs(self._args)

    def getData(self):
        return self._render(self._request())


class multiPageAPI(baseAPI):
    """
    用于处理包含了多页数据的API
    会自动根据页数请求每一页的数据
    注意实现时_render方法处理的是整个data结构体，包含了meta等部分，而不是仅data中的数据部分
    """

    def __init__(self, url: str, method: str, config: accountConfig, **args):
        super().__init__(url, method, config, **args)

    def _render(self, data: dict) -> list:
        raise NotImplementedError("This method must be implemented by subclass!")

    def _request(self) -> dict:
        logging.info("Requesting to {}".format(self._url))
        return self._handler.request()

    def getData(self) -> list:
        data = []
        # 在默认情况下会先请求第一页的数据
        resp = self._request()
        data += self._render(resp)  # to be implemented by subclass
        try:
            # 获取meta data
            meta = resp["meta"]
            total_page = meta["page_total"]
            page_size = meta["page_size"]
            total_items = meta["total_items"]
        except KeyError:
            # 发生了这个问题说明meta字段有问题
            logging.error("No meta data found for multi-page API!")
            # 既然这样的话，直接返回第一页的数据
            return data
        logging.info("Begin requesting for {} pages of data".format(total_page))
        for p in range(2, total_page + 1):
            self.addArgs(page=p, page_size=page_size)
            resp = self._request()
            data += self._render(resp)
        return data
