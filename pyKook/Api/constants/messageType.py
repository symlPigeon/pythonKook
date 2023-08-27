from enum import IntEnum


class MSG_TYPE(IntEnum):
    TEXT = 1
    IMAGE = 2
    VIDEO = 3
    FILE = 4
    AUDIO = 8
    KMARKDOWN = 9
    CARD = 10
    SYSTEM = 255