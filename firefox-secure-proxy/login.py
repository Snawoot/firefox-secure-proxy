#!/usr/bin/env python3

import urllib.request
import urllib.error
import json
import codecs

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr
from oic.oic.message import AuthorizationResponse, RegistrationResponse

USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'

CLIENT_ID = "a8c528140153d1c6"

def main():
    client = Client(client_authn_method=None)
    client.store_registration_info(RegistrationResponse(client_id=CLIENT_ID))
    provider_info = client.provider_config('https://accounts.firefox.com')
    ch_args, cv = client.add_code_challenge()
    session = {}
    session["state"] = rndstr()
    session["nonce"] = rndstr()
    args = {
        "access_type": "offline",
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": ["profile", "https://identity.mozilla.com/apps/secure-proxy"],
        "state": session["state"],
        "nonce": session["nonce"],
        "redirect_uri": "https://cb7cbf5bedba243279adcd23bc6b88de7a304388.extensions.allizom.org/",
    }
    args.update(ch_args)

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)
    print("Please follow this URL, authenticate and paste back URL where you was redirected.")
    print("")
    print(login_url)
    rp_url = input("Please paste redirect URL:").strip()
    print("rp_url=", repr(rp_url))
    aresp = client.parse_response(AuthorizationResponse, info=rp_url, sformat="urlencoded")
    print("aresp=", repr(aresp))
    args = {
        "code": aresp["code"],
        "client_id": CLIENT_ID,
        "code_verifier": cv,
    }
    resp = client.do_access_token_request(state=aresp["state"],
                                          request_args=args,
                                          authn_method=None)
    print(resp)

if __name__ == '__main__':
    main()
