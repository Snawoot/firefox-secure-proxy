# firefox-secure-proxy

Standalone wrapper for [Firefox Secure Proxy](https://private-network.firefox.com/). Offers plain HTTP proxy interface for all compatible applications.

## Walkthrough

1. Install `firefox-secure-proxy` package. Within source directory run: `pip3 install .`. Python 3.5+ required.
2. Login into Firefox Accounts. Run `fxsp-login` and follow instructions on screen. It's OK if OAuth2 redirected URL is dead, just copy its address into console.
3. Update proxy token with command `fxsp-getproxytoken`.
4. Run HTTP stub proxy server based on haproxy. There is docker-compose recipe in `stub-server` directory. Get into it, copy file `~/.config/haproxy_maps` into it and run `docker-compose up`. Local proxy will be running on port 8080, wrapping and authenticating connections to Firefox Secure Proxy.

### Updating proxy access token

Proxy access tokens requested by firefox-secure-proxy are valid for 24 hours. In order to update it run in following commands in `stub-server` directory:

```sh
cp -v ~/.config/haproxy_maps .
docker-compose kill -s HUP haproxy
```

These actions can be scheduled to be performed automatically. Running haproxy server will be reloaded with no downtime.

## See also

* [transocks](https://github.com/cybozu-go/transocks) - transparent proxy adapter which can be used to redirect network traffic into HTTP/SOCKS5 proxy on gateway or a single Linux host. Compatible with firefox-secure-proxy.
* [python-proxy](https://github.com/qwj/python-proxy) - HTTP/Socks4/Socks5/Shadowsocks/ShadowsocksR/SSH/Redirect/Pf TCP/UDP asynchronous tunnel proxy implemented in Python3 asyncio. Can be used to wrap firefox-secure-proxy to SOCKS5 and other protocols.
