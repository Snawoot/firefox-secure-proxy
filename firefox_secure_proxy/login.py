#!/usr/bin/env python3

import argparse
import json
import os.path

from . import token
from . import utils


def parse_args():
    default_datadir = os.path.join(os.path.expanduser("~"),
                                   ".config",
                                   "fxsp")
    parser = argparse.ArgumentParser(
        description="Performs login into Firefox services and retrieves "
        "permanent authentication token, which is used to refresh proxy "
        "service token",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--datadir",
                        default=default_datadir,
                        help="data directory location")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.datadir, exist_ok=True)
    refresh_token_data = token.get_refresh_token()
    out_file = os.path.join(args.datadir, 'refresh_token')
    utils.update_file(out_file, json.dumps(refresh_token_data))


if __name__ == '__main__':
    main()
