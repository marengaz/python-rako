from pathlib import Path

import pytest

from python_rako import Bridge, discover_bridge

RESOURCES = Path(__file__).parent / "tests/resources"


@pytest.fixture
def rako_xml() -> str:
    with open(RESOURCES / "rako.xml") as f:
        xml = f.read()

    return xml


@pytest.fixture(autouse=True)
async def bridge() -> Bridge:
    bridge_host = await discover_bridge()
    return Bridge(bridge_host)
