---
title: HttpConn
description: HttpConn
---

# HttpConn

```python

# -*-coding:utf8-*-

import fire
import requests
import urllib
import json
import ast

P_LOGIN = """
POST https://xxx/xxx/xxx?appid=xxx&channel=xxx
Host: xxx.xxx.com
sessionId: xxx_xxx
Content-Type: application/json
Accept-Encoding: br, gzip, deflate
Connection: keep-alive
Accept: */*
User-Agent: Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c30) NetType/WIFI Language/zh_CN
Referer: https://xxx/xxx.html
Content-Length: 41
Accept-Language: zh-cn

b'{"sss":"xxx"}'
"""

class Protocal:

    def __init__(self, s:str=None, header:dict=None, content=None, method=None, url=None, status_code=None):
        self.header = header
        self.content = content
        self.url = url
        self.method = method
        self.status_code = status_code
        if s is not None:
            self.parse(s)

    @property
    def content(self):
        if self.json is not None:
            content = json.dumps(self.json).encode('utf-8')
        else:
            content = self._content
        return content

    @content.setter
    def content(self, content):
        if content is not None:
            if type(content) == str:
                if content.startswith('b\'') and content.endswith('\''):
                    # content = content[2:-1]
                    # content = str(content, 'utf-8')
                    # print('content:::', content)
                    # with open('aa', 'r') as fp:
                    #     sss = fp.readline()
                    # print(sss)
                    content = ast.literal_eval(content)
                    print('content:::', content)
                else:
                    content = content.encode('utf-8')
            if (content.startswith(b'{') and content.endswith(b'}')) or (content.startswith(b'[') and content.endswith(b']')):
                self.json = json.loads(str(content, 'utf-8'))
            else:
                self.json = None
        self._content = content

    @property
    def url(self):
        if self.url_without_query is not None:
            parts = []
            for key, value in self.query.items():
                parts.append('%s=%s' % (key, value))
            url = self.url_without_query + '?' + '&'.join(parts)
        else:
            url = self._url
        return url

    @url.setter
    def url(self, url):
        if url is not None:
            url_without_query = None
            query = {}
            q_idx = url.find('?')
            if q_idx > 0:
                url_without_query = url[:q_idx]
                query_parts = url[q_idx+1:].split('&')
                for query_part in query_parts:
                    qp = query_part.split('=')
                    query[qp[0]] = qp[1]
            self.url_without_query = url_without_query
            self.query = query
        self._url = url

    def parse(self, s:str):
        idx = s.find('\n\n')
        s_of_header = s[:idx]
        s_of_content = s[idx+2:]
        lines = s_of_header.strip().split('\n')
        first_line_parts = lines[0].split(' ')
        self.method = first_line_parts[0]
        self.url = first_line_parts[1]
        lines = lines[1:]
        header = {}
        for idx, line in enumerate(lines):
            line = line.strip()
            if line == '':  # content
                break
            pair = line.split(': ')
            key = pair[0]
            value = pair[1]
            header[key] = value
        self.header = header
        # content = '\n'.join(lines[idx+1:])
        self.content = s_of_content.strip()

    def text(self):
        return str(self.content, 'utf-8')

    def __str__(self):
        lines = []
        if self.method is not None:
            lines.append('%s %s' % (self.method, self.url))
        elif self.status_code is not None:
            lines.append('%s' % self.status_code)
        for key, value in self.header.items():
            lines.append('%s: %s' % (key, value))
        ss = '\n'.join(lines)
        ss += '\n\n'
        try:
            ss += str(self.content, 'utf-8')  # 有些返回加密的内容，转不成文本，出现错误 
        except UnicodeDecodeError:
            ss += '<bytes: %s>' % len(self.content)
        return ss

    def __repr__(self):
        return str(self)

class Connection:

    def __init__(self):
        self.session = requests.Session()

    def send(self, p: Protocal, auto_close=True) -> Protocal:
        print('\n%s' % (50*'>'))
        # print(p)
        r = None
        rsp = None
        if p.method == 'GET':
            # rsp = self.session.get(url=p.url, headers=p.header, verify=False)
            rsp = self.session.get(url=p.url, headers=p.header)
        elif p.method == 'POST':
            # rsp = self.session.post(url=p.url, headers=p.header, data=p.content, verify=False)
            rsp = self.session.post(url=p.url, headers=p.header, data=p.content)
        r = Protocal(header=rsp.headers, content=rsp.content, status_code=rsp.status_code)
        if auto_close:
            self.close()
        print('%s' % (50*'<'))
        return r

    def close(self):
        self.session.close()


def test():
    p = Protocal(P_LOGIN)
    print(p.url)
    print(p.query)
    print(p.url_without_query)
    p.url = 'http://www.xxx.com?a=b&c=d'
    print(p.url)
    print(p.query)
    print(p.url_without_query)    
    p.query = {'aa': 'bb', 'cc': 'dd'}
    print(p.url)
    print(p.query)
    print(p.url_without_query)

    print(p.content)
    p.json['sss'] = 'aaabbbccc'
    print(p.content)
    p.content = b'{"sss": "aaabbbccc"}'
    print(p.content)
    p.content = '{"sss": "aaabbbccc"}'
    print(p.content)
    p.content = 'b\'{"sss": "aaabbbccc"}\''
    print(p.content)
    # r = Connection().send(p)
    # print(r)
    # print(json.loads(str(r.content, 'utf-8')))

def test_login(sessionId):
    p = Protocal(API_LOGIN_LOGIN)
    p.header['sessionId'] = sessionId
    r = httpconn.Connection().send(p)
    print(r)
    sessionId = r.json['sessionId']
    print('NEW_sessionId = %s' % sessionId)
    return sessionId

def test2():
    mss = range(3,8)
    for idx in range(10000):
        xxx()
        ms = random.choice(mss)
        print('sleep %s' % ms)
        time.sleep(ms)    


if __name__ == '__main__':
    test()

```