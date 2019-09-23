import asyncio
import logging
import collections
from functools import partial
import urllib.parse

from .constants import BUFSIZE
from .baselistener import BaseListener


class HttpListener(BaseListener):  # pylint: disable=too-many-instance-attributes
    def __init__(self, *,
                 listen_address,
                 listen_port,
                 upstream_url,
                 auth_header,
                 timeout=4,
                 loop=None):
        self._loop = loop if loop is not None else asyncio.get_event_loop()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._listen_address = listen_address
        self._listen_port = listen_port
        self._auth_header = auth_header
        url_components = urllib.parse.urlparse(upstream_url, scheme='https')
        self._upstream_ssl = {
            'http': False,
            'https': True,
        }[url_components.scheme.lower()]
        host, sep, port = url_components.netloc.rpartition(':')
        if sep:
            self._upstream_host = host
            self._upstream_port = int(port)
        else:
            self._upstream_host = port
            self._upstream_port = 443 if self._upstream_ssl else 80
        self._children = set()
        self._server = None
        self._timeout = timeout

    async def stop(self):
        self._server.close()
        await self._server.wait_closed()
        while self._children:
            children = list(self._children)
            self._children.clear()
            self._logger.debug("Cancelling %d client handlers...",
                               len(children))
            for task in children:
                task.cancel()
            await asyncio.wait(children)
            # workaround for TCP server keeps spawning handlers for a while
            # after wait_closed() completed
            await asyncio.sleep(.5)

    async def _pump(self, writer, reader):
        while True:
            try:
                data = await reader.read(BUFSIZE)
            except asyncio.CancelledError:
                raise
            except ConnectionResetError:
                break
            if not data:
                break
            writer.write(data)

            try:
                await writer.drain()
            except ConnectionResetError:
                break
            except asyncio.CancelledError:
                raise

    async def handler(self, reader, writer):
        peer_addr = writer.transport.get_extra_info('peername')
        self._logger.info("Client %s connected", str(peer_addr))
        dst_writer = None
        try:
            dst_reader, dst_writer = await asyncio.wait_for(
                asyncio.open_connection(self._upstream_host,
                                        self._upstream_port,
                                        ssl=self._upstream_ssl),
                self._timeout)
            auth_header = self._auth_header()
            req = await reader.readline()
            print("req=", req)
            if not req:
                return
            dst_writer.write(req)
            for key, value in auth_header.items():
                line = ("%s: %s\r\n" % (key, value)).encode('ascii')
                dst_writer.write(line)
            await asyncio.gather(self._pump(writer, dst_reader),
                                 self._pump(dst_writer, reader))
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except Exception as exc:  # pragma: no cover
            self._logger.exception("Connection handler stopped with exception:"
                                   " %s", str(exc))
        finally:
            self._logger.info("Client %s disconnected", str(peer_addr))
            if dst_writer is not None:
                dst_writer.close()
            writer.close()

    async def start(self):
        def _spawn(reader, writer):
            def task_cb(task, fut):
                self._children.discard(task)
            task = self._loop.create_task(self.handler(reader, writer))
            self._children.add(task)
            task.add_done_callback(partial(task_cb, task))

        self._server = await asyncio.start_server(_spawn,
                                                  self._listen_address,
                                                  self._listen_port)
        self._logger.info("HTTP proxy server listening on %s:%d",
                          self._listen_address, self._listen_port)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
