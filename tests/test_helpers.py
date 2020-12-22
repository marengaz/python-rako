import pytest

from python_rako.const import CommandType
from python_rako.helpers import (
    command_to_byte_list,
    deserialise_byte_list,
    deserialise_status_message,
)
from python_rako.model import ChannelStatusMessage, Command, SceneStatusMessage


@pytest.mark.parametrize(
    "in_bytes,exp_obj",
    [
        ([83, 7, 0, 13, 1, 12, 42, 42, 136], ChannelStatusMessage(13, 1, 42)),
        # todo: scene cache and level cache
    ],
)
def test_deserialise_byte_list(in_bytes, exp_obj):
    payload_result = deserialise_byte_list(in_bytes)
    assert payload_result == exp_obj


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
    payload_result = deserialise_status_message(in_bytes)
    assert payload_result == exp_obj


@pytest.mark.parametrize(
    "in_cmd,exp_out",
    [
        (Command(7, 0, CommandType.OFF, []), [82, 5, 0, 7, 0, 0, 244]),
        (
            Command(276, 5, CommandType.SET_LEVEL, [0, 255]),
            [82, 7, 1, 20, 5, 52, 0, 255, 172],
        ),
    ],
)
def test_command_to_byte_list(in_cmd, exp_out):
    bytes_list = command_to_byte_list(in_cmd)
    assert bytes_list == exp_out
