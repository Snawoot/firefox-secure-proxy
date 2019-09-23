#!/usr/bin/env python3

import sys
import json
import os.path

from . import token
from . import utils


def main():
    try:
        out_dir = os.path.join(os.path.expanduser("~"),
                               '.config',
                               'fxsp')
        with open(os.path.join(out_dir, 'refresh_token')) as f:
            refresh_token_data = json.load(f)
    except KeyboardInterrupt:
        raise
    except:
        print("No refresh token loaded: can't (re)issuer proxy token. Please run fxsp-login")
        sys.exit(3)
    proxy_token_data = token.get_proxy_token(refresh_token_data)
    print("Proxy-Authorization: %s %s" % (proxy_token_data["token_type"],
                                          proxy_token_data["access_token"]))
    utils.update_file(os.path.join(out_dir, 'proxy_token'), json.dumps(proxy_token_data))
    haproxy_map = "proxy_auth_header %s %s" % (proxy_token_data["token_type"],
                                               proxy_token_data["access_token"])
    utils.update_file(os.path.join(out_dir, 'haproxy_map'), haproxy_map)
        

if __name__ == '__main__':
    main()
