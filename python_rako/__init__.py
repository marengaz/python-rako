import asyncio
import logging
import socket

import asyncio_dgram

from python_rako.bridge import Bridge  # noqa
from python_rako.const import RAKO_BRIDGE_DEFAULT_PORT
from python_rako.exceptions import RakoBridgeError
from python_rako.model import (  # noqa
    BridgeInfo,
    CacheMessage,
    ChannelStatusMessage,
    LevelCacheMessage,
    Light,
    SceneCacheMessage,
    SceneStatusMessage,
    StatusMessage,
)

_LOGGER = logging.getLogger(__name__)


async def discover_bridge() -> str:
    server = await asyncio_dgram.bind(("0.0.0.0", RAKO_BRIDGE_DEFAULT_PORT))

    server.send(b"D", ("255.255.255.255", RAKO_BRIDGE_DEFAULT_PORT))
    resp = await server.recv()
    server.close()
    if resp:
        _, (host, _) = resp
        _LOGGER.debug("Found rako bridge at %s", host)
        return host

    raise RakoBridgeError("Cannot find a rakobrige")


def discover_bridge_sync():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)

    resp = broadcast_and_listen_for_response(sock)
    if resp:
        _, (host, _) = resp
        _LOGGER.debug("found rako bridge at %s", host)
        return host

    _LOGGER.error("Cannot find a rakobrige")
    return None


def broadcast_and_listen_for_response(sock):
    # bind to the default ip address using a system provided ephemeral port
    sock.bind(("", 0))
    i = 1
    while i <= 3:
        _LOGGER.debug("Broadcasting to try and find rako bridge...")
        sock.sendto(b"D", ("255.255.255.255", RAKO_BRIDGE_DEFAULT_PORT))
        try:
            resp = sock.recvfrom(256)
            _LOGGER.debug(resp)
            return resp
        except socket.timeout:
            _LOGGER.debug("No rako bridge found on try #%s", i)
            i = i + 1


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(discover_bridge()))


if __name__ == "__main__":
    main()
