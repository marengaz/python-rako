from typing import List, Dict

from python_rako.const import SCENE_COMMAND_TO_NUMBER, CommandType, MessageType, DataRecordType, sentinel
from python_rako.exceptions import RakoDeserialisationException
from python_rako.model import (
    ChannelStatusMessage,
    Command,
    LevelCache,
    SceneStatusMessage, SceneCache, LevelCacheItem, RoomChannel,
)


def deserialise_byte_list(byte_list):
    try:
        message_type = MessageType(byte_list[0])
    except ValueError:
        raise RakoDeserialisationException(
            f"Unsupported UDP message type: {byte_list=}"
        )

    if message_type == MessageType.STATUS:
        return deserialise_status_message(byte_list)

    if message_type == MessageType.SCENE_CACHE:
        return deserialise_scene_cache_message(byte_list)

    if message_type == MessageType.LEVEL_CACHE:
        if byte_list[1] == DataRecordType.EOF.value:
            return None
        if byte_list[1] == DataRecordType.DATA.value:
            return deserialise_level_cache_message(byte_list)

    raise RakoDeserialisationException(
        f"Unsupported UDP message: {message_type=}, {byte_list=}"
    )


def deserialise_status_message(byte_list):
    data_length = byte_list[1] - 5
    room = byte_list[2] * 256 + byte_list[3]
    channel = byte_list[4]
    command = CommandType(byte_list[5])
    data = byte_list[6 : 6 + data_length]
    if command in (CommandType.LEVEL_SET_LEGACY, CommandType.SET_LEVEL):
        return ChannelStatusMessage(
            room=room,
            channel=channel,
            brightness=data[1],
        )

    if command == CommandType.SET_SCENE:
        scene = data[1]
    else:
        # command is one of SC1_LEGACY, SC2_LEGACY, SC3_LEGACY, SC4_LEGACY
        scene = SCENE_COMMAND_TO_NUMBER[command]

    return SceneStatusMessage(
        room=room,
        channel=channel,
        scene=scene,
    )


def deserialise_level_cache_message(byte_list: List[int]) -> LevelCache:
    scene_cache: Dict[RoomChannel, LevelCacheItem] = {}
    it = iter(byte_list)
    next(it)
    for b in it:
        if b != DataRecordType.DATA.value:
            break
        lc = LevelCacheItem(
            next(it), next(it), next(it),
            {i: next(it) for i in range(1, 18, 1)}
        )
        scene_cache[RoomChannel(lc.room, lc.channel)] = lc
    return LevelCache(scene_cache)


def deserialise_scene_cache_message(byte_list: List[int]) -> SceneCache:
    scene_cache = SceneCache()
    it = iter(byte_list)
    next(it)
    next(it)
    for b in it:
        room = next(it, sentinel)
        if room == sentinel:
            continue
        scene_cache[room] = b / 4
    return scene_cache


def calc_crc(byte_list: List[int]) -> int:
    return 256 - sum(byte_list) % 256


def command_to_byte_list(command: Command) -> List[int]:
    checksum_list: List[int] = [
        5 + len(command.data),
        int(command.room / 256),
        command.room % 256,
        command.channel,
        command.command.value,
    ] + command.data

    byte_list: List[int] = (
        [
            command.message_type.value,
        ]
        + checksum_list
        + [
            calc_crc(checksum_list),
        ]
    )

    return byte_list
