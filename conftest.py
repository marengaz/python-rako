from pathlib import Path

import pytest

RESOURCES = Path(__file__).parent / "tests/resources"


@pytest.fixture
def rako_xml() -> str:
    with open(RESOURCES / "rako.xml") as f:
        xml = f.read()

    return xml
