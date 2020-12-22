import asyncio
import logging
import socket
import asyncio_dgram
from typing import Iterable, Callable


from python_rako.bridge import Bridge
from python_rako.helpers import deserialise_byte_list
from python_rako.model import Light, StatusMessage

_LOGGER = logging.getLogger(__name__)


def discover_bridge():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(DEFAULT_TIMEOUT)

    resp = broadcast_and_listen_for_response(sock)
    if resp:
        _, (host, _) = resp
        _LOGGER.debug(f'found rako bridge at {host}')
        return host
    else:
        _LOGGER.error('Cannot find a rakobrige')
        return None


def broadcast_and_listen_for_response(sock):
    # bind to the default ip address using a system provided ephemeral port
    sock.bind(('', 0))
    i = 1
    while i <= 3:
        _LOGGER.debug("Broadcasting to try and find rako bridge...")
        sock.sendto(b'D', ('255.255.255.255', RAKO_BRIDGE_DEFAULT_PORT))
        try:
            resp = sock.recvfrom(256)
            _LOGGER.debug(resp)
            return resp
        except socket.timeout:
            _LOGGER.debug(f"No rako bridge found on try #{i}")
            i = i + 1




