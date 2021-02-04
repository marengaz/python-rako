import aiohttp
import pytest

from python_rako import Bridge, discover_bridge, RAKO_BRIDGE_DEFAULT_PORT
from python_rako.bridge import BridgeCommanderHTTP


@pytest.fixture
async def udp_bridge() -> Bridge:
    bridge_host = await discover_bridge()
    return Bridge(bridge_host)


@pytest.fixture
async def http_bridge() -> Bridge:
    bridge_host = await discover_bridge()
    async with aiohttp.ClientSession() as session:
        bridge_commander = BridgeCommanderHTTP(bridge_host, RAKO_BRIDGE_DEFAULT_PORT, session)
        yield Bridge(bridge_host, bridge_commander=bridge_commander)
