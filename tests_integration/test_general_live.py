import aiohttp
import aiostream
import pytest

from python_rako import Light, Bridge, RequestType, LevelCache, RoomChannel, LevelCacheItem, SceneCache


@pytest.mark.asyncio
async def test_discover_lights(udp_bridge: Bridge):
    async with aiohttp.ClientSession() as session:
        i = 0
        async for i, light in aiostream.stream.enumerate(
            udp_bridge.discover_lights(session=session)
        ):
            assert isinstance(light, Light)
        assert i >= 1, "no lights found"


@pytest.mark.asyncio
async def test_get_cache_state(udp_bridge: Bridge):
    level_cache, scene_cache = await udp_bridge.get_cache_state(
        RequestType.SCENE_LEVEL_CACHE
    )

    assert isinstance(level_cache, LevelCache)
    assert len(level_cache) >= 1
    for rc, lci in level_cache.items():
        assert isinstance(rc, RoomChannel)
        assert isinstance(lci, LevelCacheItem)

    assert isinstance(scene_cache, SceneCache)
    for room, scene in scene_cache.items():
        assert isinstance(room, int)
        assert isinstance(scene, int)
