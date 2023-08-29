from pyKook.Config.accountConfig import accountConfig
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

    async def _request(self) -> dict:
        logging.info("Requesting to {}".format(self._url))
        return (await self._handler.request())[0]

    def setArgs(self, **args):
        self._args = args
        self._handler.setArgs(self._args)

    def addArgs(self, **args):
        for key in args.keys():
            self._args[key] = args[key]
        self._handler.setArgs(self._args)

    async def getData(self):
        return self._render(await self._request())


class multiPageAPI(baseAPI):
    """
    用于处理包含了多页数据的API
    会自动根据页数请求每一页的数据
    注意实现时_render方法处理的是整个data结构体，包含了meta等部分，而不是仅data中的数据部分
    使用了cached_data字段避免重复请求
    """

    def __init__(self, url: str, method: str, config: accountConfig, **args):
        super().__init__(url, method, config, **args)
        self._cached_data = []  # 缓存数据避免请求
        self._cached_resp = False  # 如果服务器返回空值，为了避免程序认为没有数据而重复请求，需要设置这个值为True
        self._cached_partial_resp = False

    def _render(self, data: dict) -> list:
        raise NotImplementedError("This method must be implemented by subclass!")

    async def _request(self) -> list:
        logging.info("Requesting to {}".format(self._url))
        return await self._handler.request()

    async def getData(self) -> list:
        data = []
        # 在默认情况下会先请求第一页的数据
        resp = (await self._request())[0]
        data += self._render(resp)  # to be implemented by subclass
        self._cached_partial_resp = True
        try:
            # 获取meta data
            meta = resp["meta"]
            total_page = meta["page_total"]
            page_size = meta["page_size"]
            total_items = meta["total"]
            logging.info(
                "Total {} items found in {} pages.".format(total_items, total_page)
            )
        except KeyError as e:
            # 发生了这个问题说明meta字段有问题
            logging.error("No meta data or corrupted data found for multi-page API!")
            logging.error("KeyError: {}".format(e))
            self._cached_data = data
            self._cached_resp = True
            # 既然这样的话，直接返回第一页的数据
            return data
        logging.info("Begin requesting for {} pages of data".format(total_page))
        arg_list = []
        for p in range(2, total_page + 1):
            arg_list.append(self._args.update(page=p))
        if not arg_list:
            # 如果没有需要请求的数据，说明只有一页
            self._cached_data = data
            self._cached_resp = True
            return data
        self._handler.setArgs(arg_list)  # ignore this type hint...
        resp = await self._handler.request()
        for resp_ in resp:
            data += self._render(resp_)
        while {} in data:
            data.remove({})
        logging.info("Finished requesting for {} pages of data".format(total_page))
        self._cached_data = data
        self._cached_resp = True
        return data

    async def getOnePageData(self) -> list:
        data = []
        # 在默认情况下会先请求第一页的数据
        resp = (await self._request())[0]
        data += self._render(resp)  # to be implemented by subclass
        self._cached_partial_resp = True
        return data

    async def getCached(self) -> list:
        """
        获取缓存的数据
        :return:
        """
        if self._cached_data == [] and not self._cached_resp:
            return await self.getData()
        return self._cached_data
