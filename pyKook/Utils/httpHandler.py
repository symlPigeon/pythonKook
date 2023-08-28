import requests
from pyKook.Config.config import accountConfig
from pyKook.Utils.rateLimitRender import rateLimitRender
import logging


class httpHandler:
    def __init__(self, url: str, method: str, config: accountConfig, args: dict = {}):
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

    def setArgs(self, args: dict):
        self._args = args

    def request(self) -> dict:
        header = self._createHeader()
        try:
            logging.info("Sending request to {}".format(self._url))
            # 根据请求方法发送请求
            if self._method == "post":
                req = requests.post(self._url, headers=header, json=self._args)
            elif self._method == "get":
                req = requests.get(self._url, headers=header, params=self._args)
            else:
                raise Exception("Invalid method!")
            # 处理返回数据
            resp = req.json()
            code = resp["code"]
            message = resp["message"]
            data = resp["data"]
            # 处理速率限制
            resp_header = dict(req.headers)
            self._rateLimit.update(resp_header)
            # 处理错误码
            if code != 0:
                logging.warning(
                    "API request failed with code {} and message: {}".format(
                        code, message
                    )
                )
                logging.warning(req.request.body)
                return data
            else:
                return data
        except ConnectionError:
            logging.error("Connection Error when requesting to {}".format(self._url))
            return {}
        except requests.exceptions.JSONDecodeError:
            logging.error(
                "Response from {} seems not contain valid information!".format(
                    self._url
                )
            )
            return {}
        except KeyError as e:
            logging.error("Response does not obey the standard format! Missing keys!")
            logging.error(str(e))
            return {}
