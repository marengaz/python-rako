from dataclasses import dataclass
from typing import Dict, List

from python_rako.const import CommandType, MessageType


@dataclass(frozen=True)
class RoomChannel:
    room_id: int
    channel_id: int


@dataclass
class Light:
    room_id: int
    room_title: str
    channel_id: int
    channel_type: str
    channel_name: str
    channel_levels: str

    @property
    def room_channel(self):
        return RoomChannel(self.room_id, self.channel_id)


@dataclass
class BridgeInfo:
    version: str
    buildDate: str
    hostName: str
    hostIP: str
    hostMAC: str
    hwStatus: str
    dbVersion: str
    requirepassword: str
    passhash: str
    charset: str


# Message: Bridge to Client
class EOFResponse:
    pass


@dataclass
class LevelCacheItem:
    active_deleted_reserved: int
    room: int
    channel: int
    scene_levels: Dict[int, int]  # scene, level


class LevelCache(Dict[RoomChannel, LevelCacheItem]):
    """dict of: RoomChannel, LevelCacheItem"""

    pass


class SceneCache(Dict[int, int]):
    """dict of: room id, scene number"""

    pass


@dataclass
class StatusMessage:
    room: int
    channel: int


@dataclass
class SceneStatusMessage(StatusMessage):
    scene: int


@dataclass
class ChannelStatusMessage(StatusMessage):
    brightness: int


# Message: Client to Bridge
@dataclass
class Command:
    room: int
    channel: int
    command: CommandType
    data: List[int]
    message_type: MessageType = MessageType.REQUEST
