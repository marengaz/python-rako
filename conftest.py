from pathlib import Path

import pytest

RESOURCES = Path(__file__).parent / "tests/resources"


@pytest.fixture
def rako_xml() -> str:
    with open(RESOURCES / "rako.xml") as f:
        xml = f.read()

    return xml


@pytest.fixture
def rako_xml2() -> str:
    with open(RESOURCES / "rako2.xml") as f:
        xml = f.read()

    return xml
