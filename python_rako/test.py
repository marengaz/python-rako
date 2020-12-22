import asyncio
import socket
import asyncio_dgram
from asyncio_dgram.aio import DatagramServer, Protocol

from python_rako.aioudp import open_local_endpoint

DEFAULT_TIMEOUT = 5
PORT = 9761
HOST = '192.168.1.100'


async def listen_for_state_updates(bridge: Bridge):
    stream = await asyncio_dgram.bind(("0.0.0.0", PORT))
    print(f"Serving on {stream.sockname}")

    while True:
        resp = await stream.recv()
        if not resp:
            continue

        data, (remote_ip, remote_port) = resp
        if remote_ip != HOST:
            continue

        print(list(data))
        processed_bytes = Bridge.process_udp_bytes(byte_list)
        if not processed_bytes:
            continue

    await asyncio.sleep(0.5)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(udp_echo_server()))
    # loop.run_until_complete(asyncio.gather(udp_echo_server(), aioudp(), udp_socket_server()))


if __name__ == "__main__":
    main()
