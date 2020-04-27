# [ zeromq的三种简单模式（python实现）](https://segmentfault.com/a/1190000012010573)

  

## 简介

> ZMQ (以下 ZeroMQ 简称 ZMQ)是一个简单好用的传输层，像框架一样的一个 socket library，他使得 Socket 编程更加简单、简洁和性能更高。是一个消息处理队列库，可在多个线程、内核和主机盒之间弹性伸缩。ZMQ 的明确目标是“成为标准网络协议栈的一部分，之后进入 Linux 内核”。现在还未看到它们的成功。但是，它无疑是极具前景的、并且是人们更加需要的“传统”BSD 套接字之上的一层封装。ZMQ 让编写高性能网络应用程序极为简单和有趣。

`zeromq` 并不是类似`rabbitmq`消息列队，它实际上只一个消息列队组件，一个库。

## zeromq的几种模式

### Request-Reply模式：

客户端在请求后，服务端必须回响应
![943117-20160705143136264-1243355308.png](assets/Untitled/bVYtOm.png)
Python实现：
server端：

```
# -*- coding=utf-8 -*-
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print("Received: %s" % message)
    socket.send("I am OK!")
```

client端：

```
# -*- coding=utf-8 -*-

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send('Are you OK?')
response = socket.recv();
print("response: %s" % response)
```

输出：

```
$ python app/server.py 
Received: Are you OK?

$ python app/client1.py 
response: I am OK!
```

### Publish-Subscribe模式:

广播所有client，没有队列缓存，断开连接数据将永远丢失。client可以进行数据过滤。
![943117-20160705143357999-601098470.png](assets/Untitled/bVYv21.png)

Python实现
server端：

```
# -*- coding=utf-8 -*-
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

while True:
    print('发送消息')
    socket.send("消息群发")
    time.sleep(1)    
```

client端1：

```
# -*- coding=utf-8 -*-

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE,'')  # 消息过滤
while True:
    response = socket.recv();
    print("response: %s" % response)
```

client端2：

```
# -*- coding=utf-8 -*-

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE,'') 
while True:
    response = socket.recv();
    print("response: %s" % response)
```

输出：

```
$ python app/server.py 
发送消息
发送消息
发送消息

$ python app/client2.py 
response: 消息群发
response: 消息群发
response: 消息群发

$ python app/client1.py 
response: 消息群发
response: 消息群发
response: 消息群发
```

### Parallel Pipeline模式：

由三部分组成，push进行数据推送，work进行数据缓存，pull进行数据竞争获取处理。区别于Publish-Subscribe存在一个数据缓存和处理负载。

当连接被断开，数据不会丢失，重连后数据继续发送到对端。
![943117-20160705143418983-31884127.png](assets/Untitled/bVYv3q.png)

Python实现

server端：

```
# -*- coding=utf-8 -*-
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5557")

while True:
    socket.send("测试消息")
    print "已发送"    
    time.sleep(1)    
```

work端：

```
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()

recive = context.socket(zmq.PULL)
recive.connect('tcp://127.0.0.1:5557')

sender = context.socket(zmq.PUSH)
sender.connect('tcp://127.0.0.1:5558')

while True:
    data = recive.recv()
    print "正在转发..."
    sender.send(data)
```

client端：

```
# -*- coding=utf-8 -*-

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5558")

while True:
    response = socket.recv();
    print("response: %s" % response)
```

输出结果：



```
$ python app/server.py 
已发送
已发送
已发送

$ python app/work.py 
正在转发...
正在转发...
正在转发...

$ python app/client1.py
response: 测试消息
response: 测试消息
response: 测试消息
```

https://segmentfault.com/a/1190000012010573