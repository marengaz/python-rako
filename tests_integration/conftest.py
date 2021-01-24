import pytest

from python_rako import Bridge, discover_bridge


@pytest.fixture(autouse=True)
async def bridge() -> Bridge:
    bridge_host = await discover_bridge()
    return Bridge(bridge_host)
