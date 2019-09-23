import urllib.request
import urllib.error
import json
import codecs
import random
import time

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr
from oic.oic.message import AuthorizationResponse, RegistrationResponse

from . import constants
from . import utils


def get_refresh_token(*, user_agent=constants.USER_AGENT):
    client = Client(client_authn_method=None)
    client.store_registration_info(RegistrationResponse(client_id=constants.CLIENT_ID))
    provider_info = client.provider_config(constants.FXA_PROVIDER_URL)
    ch_args, cv = utils.make_verifier()
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
                                          http_args={"headers": {"User-Agent": user_agent}})
    return resp.to_dict()

def get_proxy_token(refresh_token_data, *,
                    user_agent=constants.USER_AGENT,
                    scope=constants.FXA_PROXY_SCOPE,
                    resource=constants.DEFAULT_PROXY_URL,
                    ttl=constants.FXA_EXP_TOKEN_TIME,
                    timeout=10.):
    client = Client(client_authn_method=None)
    provider_info = client.provider_config(constants.FXA_PROVIDER_URL)
    token_endpoint = client.token_endpoint
    #return resp.to_dict()

    http_req = urllib.request.Request(
        token_endpoint,
        data=json.dumps({
            "client_id": constants.CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token_data["refresh_token"],
            "scope": scope,
            "ttl": ttl,
            "ppid_seed": random.randrange(1024),
            "resource": resource,
        }).encode('ascii'),
        headers={
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }
    )
    with urllib.request.urlopen(http_req, None, timeout) as resp:
        coding = resp.headers.get_content_charset()
        coding = coding if coding is not None else 'utf-8-sig'
        decoder = codecs.getreader(coding)(resp)
        res = json.load(decoder)
    res["received_at"] = int(time.time())
    return res
