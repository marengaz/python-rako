import asyncio
import logging
import socket
from asyncio.trsock import TransportSocket  # noqa

import asyncio_dgram

from python_rako.bridge import Bridge, BridgeCommanderHTTP, BridgeCommanderUDP  # noqa
from python_rako.const import RAKO_BRIDGE_DEFAULT_PORT, MessageType, RequestType  # noqa
from python_rako.exceptions import RakoBridgeError  # noqa
from python_rako.model import (  # noqa
    BridgeInfo,
    ChannelLight,
    ChannelStatusMessage,
    LevelCache,
    LevelCacheItem,
    Light,
    RoomChannel,
    RoomLight,
    SceneCache,
    SceneStatusMessage,
)

_LOGGER = logging.getLogger(__name__)


async def discover_bridge() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server = await asyncio_dgram.from_socket(sock)
    await server.send(b"D", ("255.255.255.255", RAKO_BRIDGE_DEFAULT_PORT))
    _, (host, _) = await server.recv()
    return host


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(discover_bridge()))


if __name__ == "__main__":
    main()
