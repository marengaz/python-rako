"""These tests only work when there is a Rako Bridge on the Network"""
import asyncio
from asyncio import Task

import pytest

from python_rako import (
    Bridge,
    ChannelStatusMessage,
    SceneStatusMessage,
)
from python_rako.helpers import get_dg_listener


async def _test_set_room_scene(bridge: Bridge, event_loop):
    test_room_id = 5
    test_scene = 1

    async def wait_for_response():
        async with get_dg_listener(bridge.port) as listener:
            response = await bridge.next_pushed_message(listener)
            assert response == SceneStatusMessage(test_room_id, 0, test_scene)

    task: Task = event_loop.create_task(wait_for_response())
    await bridge.set_room_scene(test_room_id, test_scene)

    while not task.done():
        await asyncio.sleep(1)

    e = task.exception()
    if e:
        raise e


@pytest.mark.asyncio
async def test_set_room_scene_udp(udp_bridge: Bridge, event_loop):
    await _test_set_room_scene(udp_bridge, event_loop)


@pytest.mark.asyncio
async def test_set_room_scene_http(http_bridge: Bridge, event_loop):
    await _test_set_room_scene(http_bridge, event_loop)


async def _test_set_room_brightness(bridge: Bridge, event_loop):
    test_room_id = 5
    test_brightness = 150

    async def wait_for_response():
        async with get_dg_listener(bridge.port) as listener:
            response = await bridge.next_pushed_message(listener)
            assert response == ChannelStatusMessage(
                room=test_room_id, channel=0, brightness=test_brightness
            )

    task: Task = event_loop.create_task(wait_for_response())
    await bridge.set_room_brightness(test_room_id, test_brightness)

    while not task.done():
        await asyncio.sleep(1)

    e = task.exception()
    if e:
        raise e


@pytest.mark.asyncio
async def test_set_room_brightness_udp(udp_bridge: Bridge, event_loop):
    await _test_set_room_brightness(udp_bridge, event_loop)


@pytest.mark.asyncio
async def test_set_room_brightness_http(http_bridge: Bridge, event_loop):
    await _test_set_room_brightness(http_bridge, event_loop)


async def _test_set_channel_brightness(bridge: Bridge, event_loop):
    test_room_id = 5
    test_channel_id = 5
    test_brightness = 150

    async def wait_for_response():
        async with get_dg_listener(bridge.port) as listener:
            response = await bridge.next_pushed_message(listener)
            assert response == ChannelStatusMessage(
                room=test_room_id, channel=test_channel_id, brightness=test_brightness
            )

    task: Task = event_loop.create_task(wait_for_response())
    await bridge.set_channel_brightness(test_room_id, test_channel_id, test_brightness)

    while not task.done():
        await asyncio.sleep(1)

    e = task.exception()
    if e:
        raise e


@pytest.mark.asyncio
async def test_set_channel_brightness_udp(udp_bridge: Bridge, event_loop):
    await _test_set_channel_brightness(udp_bridge, event_loop)


@pytest.mark.asyncio
async def test_set_channel_brightness_http(http_bridge: Bridge, event_loop):
    await _test_set_channel_brightness(http_bridge, event_loop)







