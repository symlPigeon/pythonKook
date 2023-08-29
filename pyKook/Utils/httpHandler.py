import grequests
import requests
from pyKook.Config.accountConfig import accountConfig
from pyKook.Utils.rateLimitRender import rateLimitRender
import logging


class httpHandler:
    def __init__(
        self, url: str, method: str, config: accountConfig, args: dict | list[dict]
    ):
        self._url = url
        self._config = config
        self._method = method
        self._args = args
        self._rateLimit = rateLimitRender()

    def _createHeader(self):
        header = {
            "Authorization": self._config.getAuthToken(),
            "Accept-Language": self._config.getLang(),
        }
        if self._method == "post":
            header["Content-type"] = "application/json"
        return header

    def setArgs(self, args: dict | list[dict]):
        self._args = args

    async def request(self) -> list:
        header = self._createHeader()
        try:
            logging.info("Sending request to {}".format(self._url))
            # 根据请求方法发送请求
            if self._method == "post":
                if type(self._args) == dict:
                    req = [
                        grequests.post(self._url, headers=header, json=self._args),
                    ]
                else:
                    req = []
                    for arg in self._args:
                        req.append(grequests.post(self._url, headers=header, json=arg))
            elif self._method == "get":
                if type(self._args) == dict:
                    req = [grequests.get(self._url, headers=header, params=self._args)]
                else:
                    req = []
                    for arg in self._args:
                        req.append(grequests.get(self._url, headers=header, params=arg))
            else:
                raise Exception("Invalid method!")
            data = []
            for resp_ in grequests.imap(req, size=5):
                # 处理返回数据
                resp = resp_.json()
                code = resp["code"]
                message = resp["message"]
                data_ = resp["data"]
                # 处理速率限制
                resp_header = dict(resp_.headers)
                self._rateLimit.update(resp_header)
                # 处理错误码
                if code != 0:
                    logging.warning(
                        "API request failed with code {} and message: {}".format(
                            code, message
                        )
                    )
                    logging.warning(resp)
                    logging.warning("Request URL: {}".format(self._url))
                    logging.warning("Request data: {}".format(self._args))
                    data.append(data_)
                else:
                    data.append(data_)
            if not data:
                return [{}]
            return data
        except ConnectionError:
            logging.error("Connection Error when requesting to {}".format(self._url))
            return [{}]
        except requests.exceptions.JSONDecodeError:
            logging.error(
                "Response from {} seems not contain valid information!".format(
                    self._url
                )
            )
            return [{}]
        except KeyError as e:
            logging.error("Response does not obey the standard format! Missing keys!")
            logging.error(str(e))
            return [{}]


class httpRequest:
    def __init__(self, url: str, header=None):
        if header is None:
            header = {}
        self._url = url
        self._header = header

    async def request(self, args=None):
        if args is None:
            args = {}
        resp = grequests.post(self._url, headers=self._header, json=args)
        grequests.map(resp)
        return resp
