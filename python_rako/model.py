from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

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

    @property
    def room_channel(self):
        return RoomChannel(self.room_id, self.channel_id)


@dataclass
class RoomLight(Light):
    channel_id: int = 0


@dataclass
class ChannelLight(Light):
    channel_type: str
    channel_name: str
    channel_levels: str


@dataclass(frozen=True)
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


# pylint: disable=E1101
class LevelCache(Dict[RoomChannel, LevelCacheItem]):
    """dict of: RoomChannel, LevelCacheItem"""

    def get_channel_level(self, room_channel: RoomChannel, scene: int) -> int:
        level_cache_item = self.get(room_channel)
        if level_cache_item:
            return level_cache_item.scene_levels.get(scene, 0)
        return 0

    def get_channel_levels(self, room: int, scene: int) -> Iterable[Tuple[int, int]]:
        for lci in self.values():
            if lci.room == room:
                brightness = lci.scene_levels.get(scene, 0)
                yield lci.channel, brightness


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
