from enum import Enum

RAKO_BRIDGE_DEFAULT_PORT = 9761
sentinel = object()


class MessageType(Enum):
    QUERY = ord("Q")  # 81
    SCENE_CACHE = ord("C")  # 67
    LEVEL_CACHE = ord("X")  # 88
    REQUEST = ord("R")  # 82
    STATUS = ord("S")  # 83


class DataRecordType(Enum):
    DATA = 4
    EOF = 255


class RequestType(Enum):
    SCENE_CACHE = 1
    LEVEL_CACHE = 32
    SCENE_LEVEL_CACHE = 33


class Flags(Enum):
    USE_DEFAULT_FADE_RATE = 1


class CommandType(Enum):
    OFF = 0
    # FADE_UP = 1  # unsupported
    # FADE_DOWN = 2  # unsupported
    SC1_LEGACY = 3
    SC2_LEGACY = 4
    SC3_LEGACY = 5
    SC4_LEGACY = 6
    # IDENT = 8  # unsupported
    LEVEL_SET_LEGACY = 12
    # STORE = 13  # unsupported
    # STOP_FADING = 15  # unsupported
    # CUSTOM_232 = 45  # unsupported
    # HOLIDAY = 47  # unsupported
    SET_SCENE = 49
    # FADE = 50  # unsupported
    SET_LEVEL = 52


COMMAND_SUCCESS_RESPONSE = "AOK"


SCENE_NUMBER_TO_COMMAND = {
    1: CommandType.SC1_LEGACY,
    2: CommandType.SC2_LEGACY,
    3: CommandType.SC3_LEGACY,
    4: CommandType.SC4_LEGACY,
    0: CommandType.OFF,
}
SCENE_COMMAND_TO_NUMBER = {v: k for k, v in SCENE_NUMBER_TO_COMMAND.items()}
