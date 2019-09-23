#!/usr/bin/env python3

import urllib.request
import urllib.error
import json
import codecs

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr
from oic.oic.message import AuthorizationResponse, RegistrationResponse

from . import constants

def get_token(*, user_agent=constants.USER_AGENT):
    client = Client(client_authn_method=None)
    client.store_registration_info(RegistrationResponse(client_id=constants.CLIENT_ID))
    provider_info = client.provider_config(constants.FXA_PROVIDER_URL)
    ch_args, cv = client.add_code_challenge()
    session = {
        "state": rndstr(),
        "nonce": rndstr(),
    }
    args = {
        "access_type": "offline",
        "client_id": constants.CLIENT_ID,
        "response_type": "code",
        "scope": [constants.FXA_PROFILE_SCOPE, constants.FXA_PROXY_SCOPE],
        "state": session["state"],
        "nonce": session["nonce"],
        "redirect_uri": constants.FXA_REDIRECT_URL,
    }
    args.update(ch_args)

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)
    print("Please follow this URL, authenticate and paste back URL where you was redirected.")
    print("It's OK if URL leads to dead page, just copy&paste it's URL here.")
    print("")
    print(login_url)
    rp_url = input("Please paste redirect URL:").strip()
    aresp = client.parse_response(AuthorizationResponse, info=rp_url, sformat="urlencoded")
    args = {
        "code": aresp["code"],
        "client_id": constants.CLIENT_ID,
        "code_verifier": cv,
    }
    resp = client.do_access_token_request(state=aresp["state"],
                                          request_args=args,
                                          authn_method=None,
                                          http_args={"headers": { "User-Agent": user_agent}})
    return resp

def main():
    print(get_token())

if __name__ == '__main__':
    main()
