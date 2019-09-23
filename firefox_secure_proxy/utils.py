import base64
import os
import os.path
import hashlib
import tempfile


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


def update_file(filename, content):
    absname = os.path.abspath(filename)
    dirname = os.path.dirname(absname)
    tmp = tempfile.NamedTemporaryFile(mode='w', dir=dirname, delete=False)
    tmp_filename = tmp.name
    tmp.write(content)
    tmp.close()
    os.replace(tmp_filename, absname)
