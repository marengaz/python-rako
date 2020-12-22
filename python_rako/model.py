from dataclasses import dataclass
from typing import List

from python_rako.const import MessageType, CommandType


@dataclass
class Light:
    room_id: str
    room_title: str
    channel_id: str
    channel_type: str
    channel_name: str
    channel_levels: str


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


### Message: Bridge to Client
@dataclass
class CacheMessage:
    pass

@dataclass
class LevelCacheMessage(CacheMessage):
    pass

@dataclass
class SceneCacheMessage(CacheMessage):
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


### Message: Client to Bridge
@dataclass
class Command:
    room: int
    channel: int
    command: CommandType
    data: List[int]
    message_type: MessageType = MessageType.REQUEST



