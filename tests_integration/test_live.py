"""These tests only work when there is a Rako Bridge on the Network"""
import asyncio
from asyncio import Task

import aiohttp
import aiostream
import pytest

from python_rako import (
    Bridge,
    ChannelStatusMessage,
    Light,
    RequestType,
    SceneStatusMessage,
)
from python_rako.model import LevelCache, LevelCacheItem, RoomChannel, SceneCache


@pytest.mark.asyncio
async def test_discover_lights(bridge: Bridge):
    async with aiohttp.ClientSession() as session:
        i = 0
        async for i, light in aiostream.stream.enumerate(
            bridge.discover_lights(session=session)
        ):
            assert isinstance(light, Light)
        assert i >= 1, "no lights found"


@pytest.mark.asyncio
async def test_set_room_scene(bridge: Bridge, event_loop):
    test_room_id = 5
    test_scene = 1

    async def wait_for_response():
        async with bridge.get_dg_listener() as listener:
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
async def test_set_room_brightness(bridge: Bridge, event_loop):
    test_room_id = 5
    test_brightness = 150

    async def wait_for_response():
        async with bridge.get_dg_listener() as listener:
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
async def test_set_channel_brightness(bridge: Bridge, event_loop):
    test_room_id = 5
    test_channel_id = 5
    test_brightness = 150

    async def wait_for_response():
        async with bridge.get_dg_listener() as listener:
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
async def test_get_cache_state(bridge: Bridge):
    caches = await bridge.get_cache_state(RequestType.SCENE_LEVEL_CACHE)

    assert len(caches) == 2

    level_cache = caches[0]
    assert isinstance(level_cache, LevelCache)
    assert len(level_cache) >= 1
    for rc, lci in level_cache.items():
        assert isinstance(rc, RoomChannel)
        assert isinstance(lci, LevelCacheItem)

    scene_cache = caches[1]
    assert isinstance(scene_cache, SceneCache)
    for room, scene in scene_cache.items():
        assert isinstance(room, int)
        assert isinstance(scene, int)
