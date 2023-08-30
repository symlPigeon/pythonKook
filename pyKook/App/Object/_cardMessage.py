import json
from pyKook.Utils.loggingTool import logging


class Card:
    def __init__(self, theme: str = "primary", size: str = "lg"):
        self._groups = [{"type": "card", "size": size, "theme": theme, "modules": []}]
        self._callbacks = {}

    def addCard(self, theme: str = "primary", size: str = "lg"):
        self._groups.append(
            {"type": "card", "size": size, "theme": theme, "modules": []}
        )

    def __str__(self):
        return json.dumps(self._groups)

    def __repr__(self):
        return json.dumps(self._groups)

    def _get_card(self, card_index: int = -1):
        try:
            _body = self._groups[card_index]
        except IndexError:
            logging.error("Invalid card index!")
            return self._groups[0]
        return _body

    def addText(self, text: str, card_index: int = -1):
        _body = self._get_card(card_index)
        _body["modules"].append(
            {"type": "section", "text": {"type": "plain-text", "content": text}}
        )

    def addRichText(self, text: str, card_index: int = -1):
        _body = self._get_card(card_index)
        _body["modules"].append(
            {"type": "section", "text": {"type": "kmarkdown", "content": text}}
        )

    def addMultiColumn(self, data: list[tuple], card_index: int = -1):
        """
        添加多列文本，data的格式为[(type1, data1), (type2, data2), ...]
        :param data:
        :param card_index:
        :return:
        """
        _body = self._get_card(card_index)
        try:
            _body["modules"].append(
                {
                    "type": "section",
                    "fields": [
                        {"type": data[i][0], "content": data[i][1]}
                        for i in range(len(data))
                    ],
                }
            )
        except:
            logging.error("Invalid data format in addMultiColumn!")
            logging.error("Data: {}".format(data))
            return

    def addTextWithButton(
        self,
        text: str,
        button_label: str,
        text_type: str = "kmarkdown",
        button_theme: str = "primary",
        button_action: str = "",
        button_value: str = "",
        callback: callable = None,
        card_index: int = -1,
        **args,
    ):
        """
        添加带有文本和按钮的消息
        :param text: 文本内容
        :param button_label: 按钮标签
        :param text_type: 文本类型，默认kmarkdown,也可以是plain-text
        :param button_theme: 按钮的颜色主题
        :param button_action: 按钮的类型，如果是link的话，button_value应该是一个URL，
        如果是return-val，那么callback应该传进来一个函数，同时button_value应该是一个字符串，唯一标识这个button
        要是空的话，那这个按钮就会什么东西都不做
        :param button_value: 如button_action所示
        :param callback: 如button_action所示
        :param card_index: 卡片的索引
        :param args: 传给callback的参数
        :return:
        """
        _body = self._get_card(card_index)
        _body["modules"].append(
            {
                "type": "section",
                "text": {"type": text_type, "content": text},
                "mode": "right",
                "accessory": {
                    "type": "button",
                    "theme": button_theme,
                    "text": {"type": "plain-text", "content": button_label},
                    "value": button_value,
                    "click": button_action,
                },
            }
        )
        if callback is not None:
            self._callbacks[button_value] = (callback, args)

    def addTextWithImage(
        self,
        text: str,
        image_url: str,
        text_type: str = "kmarkdown",
        card_index: int = -1,
    ):
        """
        添加带有文本和图片的消息
        :param text: 文本
        :param image_url: 图片地址
        :param text_type: 文本类型，默认kmarkdown,也可以是plain-text
        :param card_index: 卡片索引
        :return:
        """
        _body = self._get_card(card_index)
        _body["modules"].append(
            {
                "type": "section",
                "text": {"type": text_type, "content": text},
                "mode": "right",
                "accessory": {"type": "image", "src": image_url, "size": "lg"},
            }
        )

    def addImage(self, image_url: str | list[str], card_index: int = -1):
        """
        添加图片/一堆图片
        :param image_url:
        :param card_index:
        :return:
        """
        _body = self._get_card(card_index)
        if type(image_url) == str:
            _body["modules"].append(
                {
                    "type": "container",
                    "elements": [
                        {
                            "type": "image",
                            "src": image_url,
                        }
                    ],
                }
            )
        else:
            _body["modules"].append(
                {
                    "type": "image-group",
                    "elements": [{"type": "image", "src": i} for i in image_url],
                }
            )

    def addHeader(self, header: str, card_index: int = -1):
        """
        添加标题
        :param header:
        :param card_index:
        :return:
        """
        _body = self._get_card(card_index)
        _body["modules"].append(
            {"type": "header", "text": {"type": "plain-text", "content": header}}
        )

    def addDivider(self, card_index: int = -1):
        """
        添加分割线
        :param card_index:
        :return:
        """
        _body = self._get_card(card_index)
        _body["modules"].append({"type": "divider"})

    def addButtonGroup(self, buttons: list[dict], card_index: int = -1):
        """
        添加按钮组
        :param buttons: 按钮的列表，每个按钮是一个字典，格式如下：
        {
            "theme": "按钮颜色主题",
            "value": "按钮的值，对于return-val为其回调函数标识，对于link，为链接地址"
            "click": "return-val"或者"link",
            "text": {
                "type": "plain-text"或者"kmarkdown",
                "content": "按钮名字"
            },
            "args": {xxx:xxx}, # 传给回调函数的参数
            "callback": callback,
        }
        :param card_index:
        :return:
        """
        _body = self._get_card(card_index)
        _body["modules"].append(
            {
                "type": "action-group",
                "elements": [
                    {
                        "type": "button",
                        "theme": element["theme"],
                        "value": element["value"],
                        "click": element["click"],
                        "text": element["text"],
                    }
                    for element in buttons
                ],
            }
        )
        for i in buttons:
            if i["click"] == "return-val":
                self._callbacks[i["value"]] = (i["callback"], i["args"])

    def addCountDown(
        self,
        end_time: int,
        style: str = "normal",
        card_index: int = -1,
        start_time: int = None,
    ):
        """
        添加倒计时
        :param end_time: 结束时间，时间戳ms
        :param style: 样式 normal | hour | second
        :param card_index:
        :param start_time: 开始时间，仅second模式需要
        :return:
        """
        _body = self._get_card(card_index)
        match style:
            case "normal":
                _body["modules"].append(
                    {"type": "countdown", "mode": "day", "end_time": end_time}
                )
            case "hour":
                _body["modules"].append(
                    {"type": "countdown", "mode": "hour", "end_time": end_time}
                )
            case "second":
                _body["modules"].append(
                    {
                        "type": "countdown",
                        "mode": "second",
                        "end_time": end_time,
                        "start_time": start_time,
                    }
                )

    def addFileDownloader(self):
        # TODO
        ...

    def addAudioPlayer(self):
        # TODO
        ...

    def addVideoPlayer(self):
        # TODO
        ...

    def getCallbacks(self):
        return self._callbacks
