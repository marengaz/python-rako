from enum import Enum

RAKO_BRIDGE_DEFAULT_PORT = 9761


class MessageType(Enum):
    QUERY = ord("Q")
    SCENE_CACHE = ord("C")
    LEVEL_CACHE = ord("X")
    REQUEST = ord("R")
    STATUS = ord("S")


class RequestType(Enum):
    SCENE_CAHCE = 1
    LEVEL_CACHE = 32
    SCENE_LEVEL_CAHCE = 33


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


SCENE_NUMBER_TO_COMMAND = {
    1: CommandType.SC1_LEGACY,
    2: CommandType.SC2_LEGACY,
    3: CommandType.SC3_LEGACY,
    4: CommandType.SC4_LEGACY,
    0: CommandType.OFF,
}
SCENE_COMMAND_TO_NUMBER = {v: k for k, v in SCENE_NUMBER_TO_COMMAND.items()}
