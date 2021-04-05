from python_rako import LevelCache, LevelCacheItem, RoomChannel
from python_rako.model import CommandLevelHTTP, CommandSceneHTTP, Light


# pylint: disable=E1137
def test_get_channel_level():
    r1 = RoomChannel(1, 1)
    lci1 = LevelCacheItem(0, 1, 1, {1: 1, 2: 2})
    r2 = RoomChannel(1, 2)
    lci2 = LevelCacheItem(0, 1, 2, {1: 3, 2: 4})
    r3 = RoomChannel(2, 1)
    lci3 = LevelCacheItem(0, 2, 1, {1: 5, 2: 6})

    level_cache = LevelCache()
    level_cache[r1] = lci1
    level_cache[r2] = lci2
    level_cache[r3] = lci3

    res = level_cache.get_channel_level(r1, 2)
    assert res == 2
    res = level_cache.get_channel_level(r2, 1)
    assert res == 3
    res = level_cache.get_channel_level(RoomChannel(99, 99), 99)
    assert res == 0


# pylint: disable=E1137
def test_get_channel_levels():
    r1 = RoomChannel(1, 1)
    lci1 = LevelCacheItem(0, 1, 1, {1: 1, 2: 2})
    r2 = RoomChannel(1, 2)
    lci2 = LevelCacheItem(0, 1, 2, {1: 3, 2: 4})
    r3 = RoomChannel(2, 1)
    lci3 = LevelCacheItem(0, 2, 1, {1: 5, 2: 6})

    level_cache = LevelCache()
    level_cache[r1] = lci1
    level_cache[r2] = lci2
    level_cache[r3] = lci3

    res = list(level_cache.get_channel_levels(1, 1))
    assert (1, 1) in res
    assert (2, 3) in res
    assert len(res) == 2

    res = list(level_cache.get_channel_levels(99, 99))
    assert res == list()


def test_command_scene_http():
    exp = {
        "room": 1,
        "ch": 2,
        "sc": 3,
    }
    scene = CommandSceneHTTP(1, 2, 3)

    assert scene.as_params() == exp


def test_command_level_http():
    exp = {
        "room": 1,
        "ch": 2,
        "lev": 3,
    }
    scene = CommandLevelHTTP(1, 2, 3)

    assert scene.as_params() == exp


def test_light():
    light = Light(1, "aaa", 2)
    assert light.room_channel == RoomChannel(1, 2)
