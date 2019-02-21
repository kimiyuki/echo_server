## from https://docs.python.org/3/library/asyncio-stream.html
import asyncio
import sys, time, socket, re

#logging
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
logger = getLogger("tcp_server_highlevel")
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


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")
    writer.write(data)
    await writer.drain()
    print("Close the connection")
    writer.close()


async def main(port):
    server = await asyncio.start_server(handle_echo, '0.0.0.0', int(port))
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8892
asyncio.run(main(port))
