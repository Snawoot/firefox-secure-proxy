# firefox-secure-proxy

Standalone wrapper for Firefox Secure Proxy. Offers plain HTTP-proxy interface for all compatible applications.

## Walkthrough

Install `firefox-secure-proxy` package. Within source directory run: `pip3 install .`. Python 3.5+ required.

Login into Firefox Accounts. Run `fxsp-login` and follow instructions on screen. It's OK if OAuth2 redirected URL is dead, just copy its address into console.

Update proxy token with command `fxsp-getproxytoken`.

Run HTTP stub proxy server based on haproxy. There is docker-compose recipe in `stub_server` directory. Get into it, copy file `~/.config/haproxy_maps` into it and run `docker-compose up`. Local proxy will be running on port 8080, wrapping and authenticating connections to Firefox Secure proxy.

**TBD**: invoke `fxsp-getproxytoken` and reload haproxy maps periodically in order to keep proxy token up to date. For now it is left as an exercise for reader.
