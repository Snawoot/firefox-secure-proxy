#!/usr/bin/env python3

import json
import os.path

from . import token
from . import utils

def main():
    out_dir = os.path.join(os.path.expanduser("~"),
                           '.config',
                           'fxsp')
    os.makedirs(out_dir, exist_ok=True)
    refresh_token_data = token.get_refresh_token()
    out_file = os.path.join(out_dir, 'refresh_token')
    utils.update_file(out_file, json.dumps(refresh_token_data))

if __name__ == '__main__':
    main()
