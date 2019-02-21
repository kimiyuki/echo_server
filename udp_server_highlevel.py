import asyncio
import sys, time, socket, re

#logging
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
logger = getLogger("udp_server")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)
file_handler = FileHandler("log/udp_server.log")
file_handler.setLevel(logging.DEBUG)
handler_format = Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(handler_format)
file_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class EchoServerProtocol:
  def connection_made(self, transport):
    self.transport = transport

  def datagram_received(self, data, addr):
    message = data.decode()
    logger.debug('Received %r from %s' % (message, addr))
    if message[0] == 'e':
      # simulate error not to send back
      return
    m = re.match('^\d', message[0])
    w = int(m[0]) if m else 3
    msg = f'{ip}:{port}/recv2:{data}'
    asyncio.create_task(self.delay_back(msg, addr, w))

  async def delay_back(self, data, addr, w):
    await asyncio.sleep(w)
    self.transport.sendto(data.encode(), addr)


#get variables needed for reply
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8890
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # udp does not send a packet with connect()
#ip for a reply message
ip = s.getsockname()[0]

loop = asyncio.get_event_loop()
print("Starting UDP server")
adr = ('0.0.0.0', port)
listen = loop.create_datagram_endpoint(EchoServerProtocol, local_addr=adr)
transport, protocol = loop.run_until_complete(listen)

try:
  loop.run_forever()
except KeyboardInterrupt:
  pass

transport.close()
loop.close()
