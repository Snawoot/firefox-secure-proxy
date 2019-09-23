FROM haproxy
LABEL maintainer="Vladislav Yarmak <vladislav-ex-src@vm-0.com>"

RUN apt-get update && apt-get install ca-certificates -y --no-install-recommends

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
