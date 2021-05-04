from typing import AsyncGenerator

import aiohttp
import pytest

from python_rako import Bridge, discover_bridge
from python_rako.bridge import BridgeCommanderHTTP


@pytest.fixture
async def udp_bridge() -> Bridge:
    bridge_desc = await discover_bridge()
    return Bridge(**bridge_desc)


@pytest.fixture
async def http_bridge() -> AsyncGenerator[Bridge, None]:
    bridge_desc = await discover_bridge()
    async with aiohttp.ClientSession() as session:
        bridge_commander = BridgeCommanderHTTP(
            bridge_desc["host"], bridge_desc["port"], session
        )
        yield Bridge(**bridge_desc, bridge_commander=bridge_commander)
