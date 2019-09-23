#!/usr/bin/env python3

import base64
import os
import hashlib

def b64e(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def make_verifier(length=64):
    rnd = os.urandom((length + 3) // 4 * 3)
    verifier = b64e(rnd)[:length]
    challenge = b64e(hashlib.sha256(verifier.encode('ascii')).digest())
    return (
        {
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        },
        verifier,
    )
