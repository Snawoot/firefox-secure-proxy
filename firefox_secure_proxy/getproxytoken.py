#!/usr/bin/env python3

import sys
import json
import os.path

from . import token


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
    with open(os.path.join(out_dir, 'proxy_token'), 'w') as f:
        json.dump(proxy_token_data, f)
        

if __name__ == '__main__':
    main()
