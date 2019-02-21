from utils.aioudp import open_remote_endpoint 
import asyncio, queue
import logging, time, datetime
from logging import \
  getLogger, FileHandler, StreamHandler,Formatter

q = queue.Queue(maxsize=3)

def lg():
  logger = getLogger("app")
  logger.setLevel(logging.DEBUG)
  fh = FileHandler("log/tello.log")
  fh.setLevel(logging.DEBUG)
  sh = StreamHandler()
  sh.setLevel(logging.DEBUG)
  handler_format = Formatter(
      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  sh.setFormatter(handler_format)
  fh.setFormatter(handler_format)
  logger.addHandler(sh)
  logger.addHandler(fh)
  return logger

logger =lg()
async def main():
  remote1 = await open_remote_endpoint('192.168.0.101', 8889)
  #remote2 = await open_remote_endpoint('192.168.0.113', 8889)
  logger.debug('remote1,2 initialized')

  print( datetime.datetime.now().strftime("%M:%S") )
  remote1.send(b'9 taskA')
  remote1.send(b'8 taskA')
  remote1.send(b'2 taskA')
  remote1.send(b'1 taskA')
  t1 = asyncio.wait_for(remote1.receive(), 5)
  t2 = asyncio.create_task(remote1.receive())
  t3 = asyncio.create_task(remote1.receive())
  t4 = asyncio.create_task(remote1.receive())
  #tasks = await asyncio.gather(t1, t2, t3, t4)
  for task in asyncio.as_completed({t1,t2,t3,t4}):
    try:
      ret = await task
      logger.debug(f"ret:{ret}")
    except asyncio.TimeoutError as exc:
      logger.debug(f"timeout:{exc}")
      breakpoint()
      asyncio.wait_for(remote1.receive(), 5)
    else:
      logger.debug(f"done:{task}")

  print( datetime.datetime.now().strftime("%M:%S") )

  remote1.send(b'1 taskB')
  t3 = await remote1.receive()
  logger.debug(t3)

  remote1.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()