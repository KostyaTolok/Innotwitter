from enum import Enum


class MessageTypes(Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3


class StatusCodes(Enum):
    SUCCESS = 200

