import pytest

from python_rako.const import CommandType
from python_rako.helpers import (
    command_to_byte_list,
    convert_to_brightness,
    convert_to_scene,
    deserialise_byte_list,
)
from python_rako.model import (
    ChannelStatusMessage,
    CommandUDP,
    EOFResponse,
    LevelCache,
    LevelCacheItem,
    RoomChannel,
    SceneCache,
    SceneStatusMessage,
    UnsupportedMessage,
)


@pytest.mark.parametrize(
    "in_cmd,exp_out",
    [
        (CommandUDP(7, 0, CommandType.OFF, []), [82, 5, 0, 7, 0, 0, 244]),
        (
            CommandUDP(276, 5, CommandType.SET_LEVEL, [0, 255]),
            [82, 7, 1, 20, 5, 52, 0, 255, 172],
        ),
    ],
)
def test_command_to_byte_list(in_cmd, exp_out):
    bytes_list = command_to_byte_list(in_cmd)
    assert bytes_list == exp_out


@pytest.mark.parametrize(
    "in_bytes,exp_obj",
    [
        ([83, 7, 0, 13, 1, 12, 42, 42, 136], ChannelStatusMessage(13, 1, 42)),
        ([83, 7, 0, 5, 1, 52, 1, 255, 198], ChannelStatusMessage(5, 1, 255)),
        ([83, 7, 0, 13, 1, 12, 16, 16, 136], ChannelStatusMessage(13, 1, 16)),
        ([83, 7, 0, 10, 2, 12, 16, 16, 136], ChannelStatusMessage(10, 2, 16)),
        ([83, 5, 0, 13, 0, 6, 237], SceneStatusMessage(13, 0, 4)),
        ([83, 7, 0, 17, 0, 49, 0, 2, 188], SceneStatusMessage(17, 0, 2)),
        ([83, 5, 0, 13, 0, 4, 239], SceneStatusMessage(13, 0, 2)),
        ([83, 5, 0, 21, 0, 6, 229], SceneStatusMessage(21, 0, 4)),
        ([83, 5, 0, 21, 0, 0, 235], SceneStatusMessage(21, 0, 0)),
    ],
    ids=[
        "base level legacy",
        "base level",
        "diff brightness legacy",
        "diff room channel legacy",
        "scene base legacy",
        "base scene",
        "diff scene legacy",
        "diff room legacy",
        "room off",
    ],
)
def test_deserialise_status_message(in_bytes, exp_obj):
    payload_result = deserialise_byte_list(in_bytes)
    assert payload_result == exp_obj


@pytest.mark.parametrize(
    "in_bytes,exp_obj",
    [
        ([83, 6, 0, 10, 0, 50, 128, 68], UnsupportedMessage()),
        ([1, 2, 3, 4], UnsupportedMessage()),
    ],
)
def test_deserialise_unsupported_message(in_bytes, exp_obj):
    payload_result = deserialise_byte_list(in_bytes)
    assert payload_result == exp_obj


def test_deserialise_scene_cache_message():
    payload_result = deserialise_byte_list(
        [67, 13, 4, 5, 0, 21, 8, 17, 0, 9, 0, 10, 0, 13, 156]
    )
    exp_obj = SceneCache({5: 1, 21: 0, 17: 2, 9: 0, 10: 0, 13: 0})
    assert payload_result == exp_obj


def test_deserialise_eof_message():
    payload_result = deserialise_byte_list([88, 255])
    assert payload_result == EOFResponse()


def test_deserialise_level_cache_message():
    res = deserialise_byte_list(
        [
            88,
            4,
            128,
            9,
            1,
            255,
            191,
            127,
            37,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            4,
            128,
            9,
            2,
            255,
            191,
            127,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            123,
        ]
    )

    padding = {i: 0 for i in range(5, 18, 1)}
    exp = LevelCache(
        {
            RoomChannel(9, 1): LevelCacheItem(
                128, 9, 1, {**{1: 255, 2: 191, 3: 127, 4: 37}, **padding}
            ),
            RoomChannel(9, 2): LevelCacheItem(
                128, 9, 2, {**{1: 255, 2: 191, 3: 127, 4: 0}, **padding}
            ),
        }
    )
    assert res == exp


@pytest.mark.parametrize(
    "in_scene,exp_brightness",
    [
        (1, 255),
        (0, 0),
    ],
)
def test_convert_to_brightness(in_scene, exp_brightness):
    res = convert_to_brightness(in_scene)
    assert res == exp_brightness


@pytest.mark.parametrize(
    "in_brightness,exp_scene",
    [
        (255, 1),
        (0, 0),
    ],
)
def test_convert_to_scene(in_brightness, exp_scene):
    res = convert_to_scene(in_brightness)
    assert res == exp_scene
