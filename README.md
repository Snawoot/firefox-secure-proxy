# firefox-secure-proxy

Standalone wrapper for [Firefox Secure Proxy](https://private-network.firefox.com/). Offers plain HTTP proxy interface for all compatible applications.

## Walkthrough

1. Install `firefox-secure-proxy` package. Use command `pip3 install firefox-secure-proxy` to install package from PyPI or run: `pip3 install .` within source directory. Python 3.5+ is required.
2. Login into Firefox Accounts. Run `fxsp-login` and follow instructions on screen. It's OK if OAuth2 redirected URL is dead, wait for it to bail out and just copy its address into console.
3. Update proxy token with command `fxsp-getproxytoken`.
4. Run HTTP stub proxy server based on haproxy. There is docker-compose recipe in [**stub-server**](https://github.com/Snawoot/firefox-secure-proxy/tree/master/stub-server) directory. Get into it, copy file `~/.config/fxsp/haproxy_maps` into it and run `docker-compose up`. Local proxy will be running on port 8080, wrapping and authenticating connections to Firefox Secure Proxy.

### Updating proxy access token

Proxy access tokens requested by firefox-secure-proxy are valid for 24 hours. In order to update it run in following commands in your local `stub-server` directory:

```sh
cp -v ~/.config/fxsp/haproxy_map .
docker-compose kill -s HUP haproxy
```

These actions can be scheduled to be performed automatically. Running haproxy server will be reloaded with no downtime.

## Synopsis

```
$ fxsp-login --help
usage: fxsp-login [-h] [-d DATADIR]

Performs login into Firefox services and retrieves permanent authentication
token, which is used to refresh proxy service token

optional arguments:
  -h, --help            show this help message and exit
  -d DATADIR, --datadir DATADIR
                        data directory location (default:
                        /home/user/.config/fxsp)
```

```
$ fxsp-getproxytoken --help
usage: fxsp-getproxytoken [-h] [-d DATADIR] [-a AGE]

Retrieves or updates proxy service token using persistent Firefox refresh
token (login token)

optional arguments:
  -h, --help            show this help message and exit
  -d DATADIR, --datadir DATADIR
                        data directory location (default:
                        /home/user/.config/fxsp)
  -a AGE, --age AGE     update token if it's age greater than AGE seconds
                        (default: 0)
```

## See also

* [transocks](https://github.com/cybozu-go/transocks) - transparent proxy adapter which can be used to redirect network traffic into HTTP/SOCKS5 proxy on gateway or a single Linux host. Compatible with firefox-secure-proxy.
* [python-proxy](https://github.com/qwj/python-proxy) - HTTP/Socks4/Socks5/Shadowsocks/ShadowsocksR/SSH/Redirect/Pf TCP/UDP asynchronous tunnel proxy implemented in Python3 asyncio. Can be used to wrap firefox-secure-proxy to SOCKS5 and other protocols.
