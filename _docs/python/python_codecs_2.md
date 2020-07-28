---
title: 编码转换测试
description: 编码转换测试
---

# 编码转换测试

```python
# -*-coding:utf8-*-

import codecs
from urllib import parse
import base64
import ast

def test():
    print('中国China123')  # 中国China123

    # str --encode-->unocodeBytes
    print('中国China123'.encode('unicode_escape'))  # b'\\u4e2d\\u56fdChina123'
    # unocodeBytes --decode--> str
    print(b'\\u4e2d\\u56fdChina123'.decode('unicode_escape')) # 中国China123

    # str --encode--> utf8Bytes
    print('中国China123'.encode('utf-8'))  # b'\xe4\xb8\xad\xe5\x9b\xbdChina123'
    print(bytes('中国China123', 'utf-8'))  # b'\xe4\xb8\xad\xe5\x9b\xbdChina123'
    # utf8Bytes --decode--> str
    print(b'\xe4\xb8\xad\xe5\x9b\xbdChina123'.decode('utf-8'))  # 中国China123
    print(str(b'\xe4\xb8\xad\xe5\x9b\xbdChina123', 'utf-8'))  # 中国China123
    
    # str --encode--> gbkBytes
    print('中国China123'.encode('gbk'))  # b'\xd6\xd0\xb9\xfaChina123'
    print(bytes('中国China123', 'gbk'))
    # gbkBytes --decode--> str
    print(b'\xd6\xd0\xb9\xfaChina123'.decode('gbk'))  # 中国China123
    print(str(b'\xd6\xd0\xb9\xfaChina123', 'gbk'))  # 中国China123

    # hexStr --> bytes
    print(bytes.fromhex('aabbcc112233')) # b'\xaa\xbb\xcc\x11"3'
    # bytes --> hexStr
    print(b'\xaa\xbb\xcc\x11"3'.hex())  # aabbcc112233
    print(''.join(['%02x' % b for b in b'\xaa\xbb\xcc\x11"3']))  # aabbcc112233
    
    # bytes --encode--> hexBytes
    print(codecs.encode(b'\xaa\xbb\xcc\x11"3', 'hex')) # b'aabbcc112233'
    # hexBytes --decode--> bytes
    print(codecs.decode(b'aabbcc112233', 'hex'))  # b'\xaa\xbb\xcc\x11"3'

    utf8Str = '中国China123'.encode('utf-8') # b'\xe4\xb8\xad\xe5\x9b\xbdChina123'
    # bytes --encode--> base64Bytes
    print(base64.b64encode(utf8Str)) # b'5Lit5Zu9Q2hpbmExMjM='
    # base64Bytes --decode--> bytes
    print(base64.b64decode(b'5Lit5Zu9Q2hpbmExMjM=')) # b'\xe4\xb8\xad\xe5\x9b\xbdChina123'    

    # urlencode
    print(parse.quote('?中国&China=123')) # %3F%E4%B8%AD%E5%9B%BD%26China%3D123
    # urldecode
    print(parse.unquote('%3F%E4%B8%AD%E5%9B%BD%26China%3D123')) # ?中国&China=123
    # urlencode dict
    data = {
        'ch': '中国',
        'en': 'China'
    }
    print(parse.urlencode(data))  # ch=%E4%B8%AD%E5%9B%BD&en=China

    # char --> ascii
    print(ord('a'), ord('A'), ord('1'), ord('&'), ord('\t'), ord(' '), ord('\n')) # 97 65 49 38 9 32 10
    print(chr(97), chr(65), chr(49), chr(38), chr(9), chr(32), chr(10)) # a A 1 &     

    # print(ast.literal_eval("b'\xe4\xb8\xad\xe5\x9b\xbdChina123'")) # SyntaxError: bytes can only contain ASCII literal characters.
    print(list("b'\xe4\xb8\xad\xe5\x9b\xbdChina123'"))
    print(ast.literal_eval(r"b'\xe4\xb8\xad\xe5\x9b\xbdChina123'")) # b'\xe4\xb8\xad\xe5\x9b\xbdChina123'
    print(list(r"b'\xe4\xb8\xad\xe5\x9b\xbdChina123'"))

    bb = b'\\u4e2d\\u56fdChina123'
    with open('tmp.txt', 'w') as fp:
        fp.write(str(bb))
    with open('tmp.txt', 'r') as fp:
        ss = fp.readline()
    assert ast.literal_eval(ss) == bb
    # link: https://stackoverflow.com/questions/59777657/how-to-convert-python-bytes-string-representation-to-bytes

    with open('qpxcBooking_req.json', 'r') as fp:
        aa = fp.readline()
    aa = ast.literal_eval(aa)
    aa = aa.decode('utf-8')
    print(aa)

def test2():
    # s = b'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'
    # print(base64.b64decode(s).decode('utf-8'))

    with open('aa', 'r') as fp:
        s = fp.readline()
    print(ast.literal_eval(s))

    # s = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    # with open('a.gif', 'wb') as fp:
    #     fp.write(s)

    # with open('agif', 'r') as fp:
    #     s = fp.readline()
    # s = ast.literal_eval(s)
    # with open('a.gif', 'wb') as fp:
    #     fp.write(s)

if __name__ == '__main__':
    # test()
    test2() 
```