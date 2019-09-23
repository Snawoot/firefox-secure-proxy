import enum
import logging

USER_AGENT = "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0"
CLIENT_ID = "a8c528140153d1c6"
FXA_PROVIDER_URL = "https://accounts.firefox.com"
FXA_PROFILE_SCOPE = "profile"
FXA_PROXY_SCOPE = "https://identity.mozilla.com/apps/secure-proxy"
FXA_REDIRECT_URL = "https://cb7cbf5bedba243279adcd23bc6b88de7a304388.extensions.allizom.org/"
DEFAULT_PROXY_URL = "https://firefox.factor11.cloudflareclient.com:2486"
FXA_EXP_TOKEN_TIME = 86400
BUFSIZE = 16 * 1024

class LogLevel(enum.IntEnum):
    debug = logging.DEBUG
    info = logging.INFO
    warn = logging.WARN
    error = logging.ERROR
    fatal = logging.FATAL
    crit = logging.CRITICAL

    def __str__(self):
        return self.name
