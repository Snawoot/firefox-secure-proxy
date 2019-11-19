#!/usr/bin/env python3

import argparse
import sys
import json
import os.path
import time

from . import token
from . import utils


def parse_args():
    def check_nonnegative_int(val):
        def fail():
            raise argparse.ArgumentTypeError("%s is not nonnegative integer value" % (repr(val),))
        try:
            ival = int(val)
        except ValueError:
            fail()
        if ival < 0:
            fail()
        return ival

    default_datadir = os.path.join(os.path.expanduser("~"),
                                   ".config",
                                   "fxsp")
    parser = argparse.ArgumentParser(
        description="Retrieves or updates proxy service token using persistent"
        " Firefox refresh token (login token)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--datadir",
                        default=default_datadir,
                        help="data directory location")
    parser.add_argument("-a", "--age",
                        default=0,
                        type=check_nonnegative_int,
                        help="update token if it's age greater than AGE seconds")
    return parser.parse_args()


def check_age_valid(datadir, age):
    try:
        with open(os.path.join(datadir, 'proxy_token')) as f:
            proxy_token_data = json.load(f)
        received_at = proxy_token_data['received_at']
        expires_in = proxy_token_data['expires_in']
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        print("local validation of proxy token failed with error: %s" % str(exc))
        return False
    else:
        deadline = received_at + min(expires_in, age)
        if time.time() >= deadline:
            return False
        return True


def main():
    args = parse_args()
    if check_age_valid(args.datadir, args.age):
        return
    try:
        with open(os.path.join(args.datadir, 'refresh_token')) as f:
            refresh_token_data = json.load(f)
    except KeyboardInterrupt:
        raise
    except:
        print("No refresh token loaded: can't (re)issuer proxy token. Please run fxsp-login")
        sys.exit(3)
    proxy_token_data = token.get_proxy_token(refresh_token_data)
    print("Proxy-Authorization: %s %s" % (proxy_token_data["token_type"],
                                          proxy_token_data["access_token"]))
    utils.update_file(os.path.join(args.datadir, 'proxy_token'), json.dumps(proxy_token_data))
    haproxy_map = "proxy_auth_header %s %s" % (proxy_token_data["token_type"],
                                               proxy_token_data["access_token"])
    utils.update_file(os.path.join(args.datadir, 'haproxy_map'), haproxy_map)
        

if __name__ == '__main__':
    main()
