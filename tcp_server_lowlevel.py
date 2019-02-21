import asyncio
import sys, time, socket, re

#logging
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
logger = getLogger("tcp_server_lowlevel")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
file_handler = FileHandler("log/tcp_server.log")
file_handler.setLevel(logging.DEBUG)
handler_format = Formatter(
  '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)
file_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class myProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        addr = transport.get_extra_info('peername')
        logger.info(f"con_made {addr}")
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        logger.info(f"date_rec {message}")
        self.transport.write(data)
        self.transport.close()


async def main():
    loop = asyncio.get_event_loop()
    addr = ('0.0.0.0', 8891)
    server = await loop.create_server(
        protocol_factory=myProtocol,
        host="0.0.0.0",
        port=8891,
        family=socket.AF_INET)
    async with server:
        await server.serve_forever()


asyncio.run(main())