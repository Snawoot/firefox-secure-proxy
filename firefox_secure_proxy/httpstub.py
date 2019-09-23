#!/usr/bin/env python3

import sys
import argparse
import asyncio
import logging
import signal
from functools import partial
import os.path
import json

from sdnotify import SystemdNotifier

from .constants import LogLevel, DEFAULT_PROXY_URL
from . import utils
from .httplistener import HttpListener


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generic HTTP Proxy wrapper for Firefox Secure Proxy",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-v", "--verbosity",
                        help="logging verbosity",
                        type=utils.check_loglevel,
                        choices=LogLevel,
                        default=LogLevel.info)
    parser.add_argument("-l", "--logfile",
                        help="log file location",
                        metavar="FILE")
    parser.add_argument("--disable-uvloop",
                        help="do not use uvloop even if it is available",
                        action="store_true")
    parser.add_argument("-w", "--timeout",
                        default=4,
                        type=utils.check_positive_float,
                        help="server connect timeout")
    parser.add_argument("-U", "--url",
                        default=DEFAULT_PROXY_URL,
                        help="Firefox Secure Proxy URL")

    listen_group = parser.add_argument_group('listen options')
    listen_group.add_argument("-a", "--bind-address",
                              default="127.0.0.1",
                              help="bind address")
    listen_group.add_argument("-p", "--bind-port",
                              default=8080,
                              type=utils.check_port,
                              help="bind port")


    return parser.parse_args()


async def amain(args, loop):  # pragma: no cover
    logger = logging.getLogger('MAIN')
    with open(os.path.join(os.path.expanduser("~"),
                           ".config",
                           "fxsp",
                           "proxy_token")) as f:
        proxy_token_data = json.load(f)
    proxy_header = {"Proxy-Authorization": "%s %s" % (proxy_token_data["token_type"],
                                                      proxy_token_data["access_token"])}

    server = HttpListener(listen_address=args.bind_address,
                          listen_port=args.bind_port,
                          auth_header=lambda: proxy_header,
                          upstream_url=args.url,
                          timeout=args.timeout,
                          loop=loop)
    async with server:
        logger.info("Server started.")

        exit_event = asyncio.Event()
        beat = asyncio.ensure_future(utils.heartbeat())
        sig_handler = partial(utils.exit_handler, exit_event)
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
        notifier = await loop.run_in_executor(None, SystemdNotifier)
        await loop.run_in_executor(None, notifier.notify, "READY=1")
        await exit_event.wait()

        logger.debug("Eventloop interrupted. Shutting down server...")
        await loop.run_in_executor(None, notifier.notify, "STOPPING=1")
        beat.cancel()


def main():  # pragma: no cover
    args = parse_args()
    with utils.AsyncLoggingHandler(args.logfile) as log_handler:
        logger = utils.setup_logger('MAIN', args.verbosity, log_handler)
        utils.setup_logger('HttpListener', args.verbosity, log_handler)

        logger.info("Starting eventloop...")
        if not args.disable_uvloop:
            if utils.enable_uvloop():
                logger.info("uvloop enabled.")
            else:
                logger.info("uvloop is not available. "
                            "Falling back to built-in event loop.")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(amain(args, loop))
        loop.close()
        logger.info("Server finished its work.")


if __name__ == '__main__':
    main()
