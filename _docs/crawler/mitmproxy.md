---
title: mitmproxy
description: mitmproxy
---

# mitmproxy

```py
import os
import sys
from mitmproxy import ctx
import mitmproxy


def request(flow: mitmproxy.http.HTTPFlow):
    print('request', type(flow))
    ctx.log.error(flow.request.url)
    ctx.log.warn(flow.request.method)
    ctx.log.info(flow.request.query)
    ctx.log.info(str(flow.request.headers))
    ctx.log.warn(str(flow.request.cookies))
    ctx.log.info(flow.request.text)
    

def response(flow: mitmproxy.http.HTTPFlow):
    print('response', type(flow))
    ctx.log.error(flow.response.status_code)
    ctx.log.warn(flow.response.text)

def main():
    print('aaa')

if __name__ == '__main__':
    main()
```