import logging
from typing import AsyncGenerator, Generator

import aiohttp
import asyncio_dgram
import xmltodict
from aiohttp import ClientError
from asyncio_dgram.aio import DatagramClient, DatagramServer

from python_rako.const import RAKO_BRIDGE_DEFAULT_PORT
from python_rako.exceptions import RakoBridgeError
from python_rako.helpers import deserialise_byte_list
from python_rako.model import BridgeInfo, Light

_LOGGER = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 5


class Bridge:
    def __init__(self, host: str, port: int = RAKO_BRIDGE_DEFAULT_PORT):
        self.host = host
        self.port = port
        self._dg_server: DatagramServer = None
        self._dg_client: DatagramClient = None

    @property
    def _discovery_url(self):
        return f"http://{self.host}/rako.xml"

    @property
    def _command_url(self):
        return f"http://{self.host}/rako.cgi"

    @property
    def dg_server(self):
        return self._dg_server

    @property
    def dg_client(self):
        return self._dg_client

    async def connect_dg_listener(self, listen_host: str = "0.0.0.0") -> DatagramServer:
        return await asyncio_dgram.bind((listen_host, self.port))

    async def disconnect_dg_listener(self) -> None:
        if self._dg_server:
            await self._dg_server.close()
            self._dg_server = None

    async def connect_dg_commander(self, command_host: str) -> DatagramServer:
        return await asyncio_dgram.connect((command_host, self.port))

    async def disconnect_dg_commander(self) -> None:
        if self._dg_client:
            await self._dg_client.close()
            self._dg_client = None

    async def shutdown(self):
        await self.disconnect_dg_listener()
        await self.disconnect_dg_commander()

    async def get_rako_xml(self, session: aiohttp.ClientSession) -> str:
        async with session.get(self._discovery_url) as response:
            rako_xml = await response.text()
        return rako_xml

    async def discover_lights(
        self, session: aiohttp.ClientSession
    ) -> AsyncGenerator[Light, None]:
        rako_xml = await self.get_rako_xml(session)
        for light in self.get_lights_from_discovery_xml(rako_xml):
            yield light

    async def get_info(self, session: aiohttp.ClientSession) -> BridgeInfo:
        try:
            rako_xml = await self.get_rako_xml(session)
            info = self.get_bridge_info_from_discovery_xml(rako_xml)
        except KeyError as ex:
            raise RakoBridgeError(f"unsupported bridge: {ex}")
        except ClientError as ex:
            raise RakoBridgeError(f"cannot connect to bridge: {ex}")
        return info

    @staticmethod
    def get_bridge_info_from_discovery_xml(xml: str) -> BridgeInfo:
        xml_dict = xmltodict.parse(xml)
        info = xml_dict["rako"]["info"]
        config = xml_dict["rako"]["config"]
        return BridgeInfo(
            version=info.get("version"),
            buildDate=info.get("buildDate"),
            hostName=info.get("hostName"),
            hostIP=info.get("hostIP"),
            hostMAC=info["hostMAC"],
            hwStatus=info.get("hwStatus"),
            dbVersion=info.get("dbVersion"),
            requirepassword=config.get("requirepassword"),
            passhash=config.get("passhash"),
            charset=config.get("charset"),
        )

    @staticmethod
    def get_lights_from_discovery_xml(xml: str) -> Generator[Light, None, None]:
        xml_dict = xmltodict.parse(xml)
        for room in xml_dict["rako"]["rooms"]["Room"]:
            room_id = room["@id"]
            room_type = room["Type"]
            if room_type != "Lights":
                _LOGGER.info(
                    "Unsupported room type. room_id=%s room_type=%s", room_id, room_type
                )
                continue
            room_title = room["Title"]
            for channel in room["Channel"]:
                channel_id = channel["@id"]
                channel_type = channel["type"]
                channel_name = channel["Name"]
                channel_levels = channel["Levels"]
                yield Light(
                    room_id,
                    room_title,
                    channel_id,
                    channel_type,
                    channel_name,
                    channel_levels,
                )

    async def next_pushed_message(self):
        resp = await self.dg_server.recv()
        if not resp:
            return None

        data, (remote_ip, _) = resp
        if remote_ip != self.host:
            return None

        byte_list = list(data)
        return deserialise_byte_list(byte_list)

    # async def set_channel_brightness(self, light: Light):
