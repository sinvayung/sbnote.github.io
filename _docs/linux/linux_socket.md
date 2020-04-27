---
title: Linux socket 编程，第一部分
description: Linux socket 编程，第一部分
---

# Linux socket 编程，第一部分



## 在开始之前

### 关于这本教程

IP socket 是在其上建立高级 Internet 协议的最低级的层：从 HTTP 到 SSL 到 POP3 到 Kerberos 再到 UDP-Time，每种 Internet 协议都建立在它的基础上。为了实现自定义的协议，或定制众所周知的协议的实现，程序员需要掌握基本的 socket 基础结构的工作知识。虽然本教程主要集中在 C 编程上，而且还使用 Python 作为例子中的代表性高级语言，不过类似的 API 在许多语言中都可用。

本教程将向您介绍使用跨平台的 Berkeley Sockets Interface 编写自定义的网络工具程序的基本知识。几乎所有 Linux 和其他基于 UNIX 的操作系统上的网络工具都依赖这个接口。

学习本教程需要具备最低限度的 C 语言知识，同时熟悉 Python 则更理想（主要是为了下面的第二部分）。然而，如果您对任何一种编程语言都不熟悉，那么您就应该付出一点额外的努力来学习一点编程语言；一种编程语言的大多数基本概念都可以同样应用到其它语言上，而且在诸如 Ruby、Perl、TCL 之类的大多数高级脚本语言中的称呼都相当类似。

尽管本教程介绍的是IP (Internet Protocol，Internet 协议)网络背后的基本概念，但预先熟悉某些网络协议和层的概念将会有所帮助（相关背景文献请参阅本教成末尾的 [参考资料](https://www.ibm.com/developerworks/cn/education/linux/l-sock/l-sock.html#artrelatedtopics) ）。

## 了解 IP 网络和网络层

### 网络是什么？

##### 网络层



我们通常所称的计算机网络由许多 *网络层* 组成的（请参阅 [参考资料](https://www.ibm.com/developerworks/cn/education/linux/l-sock/l-sock.html#artrelatedtopics) 了解详细解释这些概念的有用参考资料）。其中的每个网络层都提供关于该层的数据的不同限制和/或保证。每个网络层的协议一般都有它们自己的包、包头和布局格式。

传统的七个网络层被分为两组：高层和低层。Socket 接口对网络的低层提供了统一的 API （应用程序接口），并且允许您在 socket 应用程序内部实现高层协议。而且，应用程序的数据格式本身可以组成进一步的层。例如 SOAP 就建立在 XML 之上，并且 ebXML 本身可以利用 SOAP。无论如何，超过第 4 层的任何内容都超出了本教程的内容范围。

### Socket 是做什么的？

虽然 socket 接口理论上还允许访问除 IP 以外的*协议系列*，然而在实际上，socket应用程序中使用的每个网络层都将使用 IP。对于本教程来说，我们仅介绍 IPv4；将来 IPv6 也会变得很重要，但是它们在原理是相同的。在传输层，socket 支持两个特殊协议：TCP (transmission control protocol，传输控制协议) 和 UDP (user datagram protocol，用户数据报协议)。

Socket不能用来访问较低（或较高）的网络层。例如，socket 应用程序不知道它是运行在以太网、令牌环网还是拨号连接上。Socket 的伪层（pseudo-layer）也不知道高层协议（比如 NFS、HTTP、FTP等）的任何情况（除非您自己编写一个 socket 应用程序来实现那些高层协议）。 

在很多情况下，socket接口并不是用于网络编程 API 的最佳选择。特别地，由于存在很多很优秀的库可以直接使用高层协议，您不必关心 socket 的细节；那些库会为您处理 socket 的细节。例如，虽然编写您自己的 SSH 客户机并没有什么错，但是对于仅只是为了让应用程序安全地传输数据来说，就没有必要做得这样复杂。低级层比 socket 所访问的层更适合归入设备驱动程序编程领域。

### IP、TCP 和 UDP

正如上一小节所指出的，当您编写 socket 应用程序的时候，您可以在使用 TCP 还是使用 UDP 之间做出选择。它们都有各自的优点和缺点。

TCP 是流协议，而UDP是数据报协议。换句话说，TCP 在客户机和服务器之间建立持续的开放连接，在该连接的生命期内，字节可以通过该连接写出（并且保证顺序正确）。然而，通过 TCP 写出的字节没有内置的结构，所以需要高层协议在被传输的字节流内部分隔数据记录和字段。

另一方面，UDP 不需要在客户机和服务器之间建立连接，它只是在地址之间传输报文。UDP 的一个很好特性在于它的包是自分隔的（self-delimiting），也就是一个数据报都准确地指出它的开始和结束位置。然而，UDP 的一个可能的缺点在于，它不保证包将会按顺序到达，甚至根本就不保证。当然，建立在 UDP 之上的高层协议可能会提供握手和确认功能。

对于理解 TCP 和 UDP 之间的区别来说，一个有用的类比就是电话呼叫和邮寄信件之间的区别。在呼叫者用铃声通知接收者，并且接收者拿起听筒之前，电话呼叫不是活动的。只要没有一方挂断，该电话信道就保持活动，但是在通话期间，他们可以自由地想说多少就说多少。来自任何一方的谈话都按临时的顺序发生。另一方面，当你发一封信的时候，邮局在投递时既不对接收方是否存在作任何保证，也不对信件投递将花多长时间做出有力保证。接收方可能按与信件的发送顺序不同的顺序接收不同的信件，并且发送方也可能在他们发送信件是交替地接收邮件。与（理想的）邮政服务不同，无法送达的信件总是被送到死信办公室处理，而不再返回给发送者。

### 对等方、端口、名称和地址

除了 TCP 和 UDP 协议以外，通信一方（客户机或者服务器）还需要知道的关于与之通信的对方机器的两件事情：IP 地址或者端口。IP 地址是一个 32 位的数据值，为了人们好记，一般用圆点分开的 4 组数字的形式来表示，比如：`64.41.64.172`。端口是一个 16 位的数据值，通常被简单地表示为一个小于 65536 的数字。大多数情况下，该值介于 10 到 100 的范围内。一个 IP 地址获取送到某台机器的一个数据包，而一个端口让机器决定将该数据包交给哪个进程/服务（如果有的话）。这种解释略显简单，但基本思路是正确的。

上面的描述几乎都是正确的，但它也遗漏了一些东西。大多数时候，当人们考虑 Internet 主机（对等方）时，我们都不会记忆诸如 `64.41.64.172`这样的数字，而是记忆诸如 `gnosis.cx` 这样的名称。为了找到与某个特定主机名称相关联的 IP 地址，一般都使用域名服务器（DNS），但是有时会首先使用本地查找（经常是通过 /etc/hosts 的内容）。对于本教程，我们将一般地假设有一个 IP 地址可用，不过下一小节将讨论编写名称/地址查找代码。

### 主机名称解析

命令行实用程序 `nslookup` 可以被用来根据符号名称查找主机 IP地址。实际上，许多常见的实用程序，比如 `ping` 或者网络配置工具，也会顺便做同样的事情。但是以编程方式做这样的事情很简单。

在 Python 或者其他非常高级的脚本语言中，编写一个查找主机 IP 地址的实用程序是微不足道的事情： 

```
`#!/usr/bin/env python``"USAGE: nslookup.py <``inet_address``>"``import socket, sys``print socket.gethostbyname(sys.argv[1])`
```

这里的窍门是使用相同 `gethostbyname())` 函数的包装版本，该函数也可以在 C 中找到。它的用法非常简单：

```
`$ ./nslookup.py gnosis.cx``64.41.64.172`
```

### 主机名称解析（继续）

在 C 中，标准库调用 `gethostbyname()` 用于名称查找。下面是 `nslookup` 的一个简单的命令行工具实现；要改编它以用于大型应用程序是一件简单的事情。当然，使用 C 要比使用 Python 稍微复杂一点。

```
`/* Bare nslookup utility (w/ minimal error checking) */``#include <``stdio.h``>          /* stderr, stdout */``#include <``netdb.h``>          /* hostent struct, gethostbyname() */``#include <``arpa``/inet.h>      /* inet_ntoa() to format IP address */``#include <``netinet``/in.h>     /* in_addr structure */` `int main(int argc, char **argv) {``  ``struct hostent *host;     /* host information */``  ``struct in_addr h_addr;    /* Internet address */``  ``if (argc != 2) {``    ``fprintf(stderr, "USAGE: nslookup <``inet_address``>\n");``    ``exit(1);``  ``}``  ``if ((host = gethostbyname(argv[1])) == NULL) {``    ``fprintf(stderr, "(mini) nslookup failed on '%s'\n", argv[1]);``    ``exit(1);``  ``}``  ``h_addr.s_addr = *((unsigned long *) host->h_addr_list[0]);``  ``fprintf(stdout, "%s\n", inet_ntoa(h_addr));``  ``exit(0);``}`
```

注意，`gethostbyname()` 的返回值是一个 `hostent` 结构，它描述该名称的主机。该结构的成员 `host->h_addr_list` 包含一个地址表，其中的每一项都是一个按照“网络字节顺序”排列的 32 位值；换句话说，字节顺序可能是也可能不是机器的本机顺序。为了将这个 32 位值转换成圆点隔开的四组数字的形式，请使用 `inet_ntoa()` 函数。 

## 使用 C 编写客户机应用程序

### 编写 socket 客户机的步骤

我的客户机和服务器例子都将使用尽可能最简单的应用程序：发送数据和接收回完全相同的数据。事实上，很多机器出于调试目的而运行“回显服务器”；这对我们的最初客户机来说是很方便的，因为它可以在我们开始讲述服务器部分之前被使用（假设您有一台运行着 `echo` 的机器）。

我想感谢 Donahoo 和 Calvert 编写的 *TCP/IP Sockets in C* 》一书（参阅 [参考资料](https://www.ibm.com/developerworks/cn/education/linux/l-sock/l-sock.html#artrelatedtopics)）。我已经改编了他们提供的几个例子。我推荐这本书，但是不可否认，echo 服务器/客户机很快就会i在介绍 socket 编程的大多数书籍中出现。

编写客户机应用程序所涉及的步骤在 TCP 和 UDP 之间稍微有些区别。对于二者来说，您首先都要创建一个 socket；单对 TCP 来说，下一步是建立一个到服务器的连接；向该服务器发送一些数据；然后再将这些数据接收回来；或许发送和接收会在短时间内交替；最后，在 TCP 的情况下，您要关闭连接。 

### TCP 回显客户机（客户机设置）

首先，我们来看一个 TCP 客户机。在本教程系列的第二部分，我们将做一些调整，用 UDP 来（粗略地）做同样的事情。我们首先来看前面几行：一些 include 语句，以及创建 socket 的语句。

```
`#include <``stdio.h``>``#include <``sys``/socket.h>``#include <``arpa``/inet.h>``#include <``stdlib.h``>``#include <``string.h``>``#include <``unistd.h``>``#include <``netinet``/in.h>` `#define BUFFSIZE 32``void Die(char *mess) { perror(mess); exit(1); }`
```

这里没有太多的设置，只是分配了特定的缓冲区大小，它限定了每个过程中回显的数据量（但如果必要的话，我们可以循环通过多个过程）。我们还定义了一个小的错误函数。 

### TCP 回显客户机（创建 socket）

`socket()`调用的参数决定了 socket 的类型：`PF_INET` 只是意味着它使用 IP（您将总是使用它）； `SOCK_STREAM` 和 `IPPROTO_TCP` 配合用于创建 TCP socket。

```
`int main(int argc, char *argv[]) {``int sock;``struct sockaddr_in echoserver;``char buffer[BUFFSIZE];``unsigned int echolen;``int received = 0;` `if (argc != 4) {``  ``fprintf(stderr, "USAGE: TCPecho <``server_ip``> <``word``> <``port``>\n");``  ``exit(1);``}``/* Create the TCP socket */``if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {``  ``Die("Failed to create socket");``}`
```

说返回的值是一个 socket 句柄，它类似于文件句柄。特别地，如果 socket 创建失败，它将返回 -1 而不是正数形式的句柄。

### TCP 回显客户机（建立连接）

现在我们已经创建了一个 `socket` 句柄，还需要建立与服务器的连接。连接需要有一个描述服务器的 sockaddr 结构。特别地，我们需要使用`echoserver.sin_addr.s_addr` 和 `echoserver.sin_port` 来指定要连接的服务器和端口。我们正在使用 IP 地址这一事实是通过`echoserver.sin_family` 来指定的，但它总是被设置为 `AF_INET`。

```
`/* Construct the server sockaddr_in structure */``memset(&echoserver, 0, sizeof(echoserver));       /* Clear struct */``echoserver.sin_family = AF_INET;                  /* Internet/IP */``echoserver.sin_addr.s_addr = inet_addr(argv[1]);  /* IP address */``echoserver.sin_port = htons(atoi(argv[3]));       /* server port */``/* Establish connection */``if (connect(sock,``            ``(struct sockaddr *) &echoserver,``            ``sizeof(echoserver)) < 0) {``  ``Die("Failed to connect with server");``}`
```

与创建 socket 类似，在尝试建立连接时，如果失败，则返回-1，否则 socket 现在就准备好发送或接收数据了。有关端口号的参考资料请参阅[参考资料](https://www.ibm.com/developerworks/cn/education/linux/l-sock/l-sock.html#artrelatedtopics) 。 

### TCP回显客户机（发送/接收数据）

现在连接已经建立起来，我们准备好可以发送和接收数据了。`send()` 调用接受套接字句柄本身、要发送的字符串、所发送的字符串的长度（用于验证）和一个标记作为参数。一般情况下，表记的默认值为 0。`send()` 调用的返回值是成功发送的字节的数目。

```
`/* Send the word to the server */``echolen = strlen(argv[2]);``if (send(sock, argv[2], echolen, 0) != echolen) {``  ``Die("Mismatch in number of sent bytes");``}``/* Receive the word back from the server */``fprintf(stdout, "Received: ");``while (received < echolen) {``  ``int bytes = 0;``  ``if ((bytes = recv(sock, buffer, BUFFSIZE-1, 0)) < 1) {``    ``Die("Failed to receive bytes from server");``  ``}``  ``received += bytes;``  ``buffer[bytes] = '\0';        /* Assure null terminated string */``  ``fprintf(stdout, buffer);``}`
```

`rcv()` 调用不保证会获得某个特定调用中传输的每个字节。在接收到某些字节之前，它只是处于阻塞状态。所以我们让循环一直进行，直到收回所发送的全部字节。很明显，不同的协议可能决定以不同的方式（或许是字节流中的分隔符）决定何时终止接收字节。

### TCP 回显客户机（包装）

对 `send()` 和 `recv()` 的调用在默认的情况下都是阻塞的，但是通过改变套接字的选项以允许非阻塞的套接字是可能的。然而，本教程不会介绍创建非阻塞套接字的细节，也不介绍在生产服务器中使用的诸如分支、线程或者一般异步处理（建立在非阻塞套接字基础上）之类的细节。这些问题将在本教程的第二部分介绍。

在这个过程的末尾，我们希望在套接字上调用 `close()` ，这很像我们对文件句柄所做的那样：

```
`  ``fprintf(stdout, "\n");``  ``close(sock);``  ``exit(0);``}`
```

## 使用 C 编写服务器应用程序

### 编写套接字服务器的步骤

套接字服务器比客户机稍微复杂一点，这主要是因为服务器通常需要能够处理多个客户机请求。服务器基本上包括两个方面：处理每一个已建立的连接，以及要建立的连接。

在我们的例子中，以及在大多数情况下，都可以将特定连接的处理划分为支持函数，这看起来有点像 TCP 客户机所做的事情。我们将这个函数命名为 `HandleClient()`。

对新连接的监听与客户机有一点不同，其诀窍在于，最初创建并绑定到某个地址或端口的套接字并不是实际连接的套接字。这个最初的套接字的作用更像一个套接字工厂，它根据需要产生新的已连接的套接字。这种安排在支持派生的、线程化的或异步的分派处理程序（使用 `select()`)函数）方面具有优势；不过对于这个入门级的教程，我们将仅按同步的顺序处理未决的已连接套接字。

### TCP 回显服务器（应用程序设置）

我们的回显服务器与客户机非常类似，都以几个 `#include` 语句开始，并且定义了一些常量和错误处理函数：

```
`#include <``stdio.h``>``#include <``sys``/socket.h>``#include <``arpa``/inet.h>``#include <``stdlib.h``>``#include <``string.h``>``#include <``unistd.h``>``#include <``netinet``/in.h>` `#define MAXPENDING 5    /* Max connection requests */``#define BUFFSIZE 32``void Die(char *mess) { perror(mess); exit(1); }`
```

常量 `BUFFSIZE` 限定了每次循环所发送的数据量。常量 `MAXPENDING` 限定了在某一时间将要排队等候的连接的数量（在我们的简单的服务器中，一次仅提供一个连接服务）。函数 `Die()` 与客户机中的相同。 

### TCP 回显服务器（连接处理程序）

用于回显连接的处理器程序很简单。它所做的工作就是接收任何可用的初始字节，然后循环发回数据并接收更多的数据。对于短的（特别是小于 `BUFFSIZE`) 的）回显字符串和典型的连接，`while` 循环只会执行一次。但是底层的套接字接口 （以及 TCP/IP） 不对字节流将如何在 `recv()` 调用之间划分做任何保证。 

```
`void HandleClient(int sock) {``  ``char buffer[BUFFSIZE];``  ``int received = -1;``  ``/* Receive message */``  ``if ((received = recv(sock, buffer, BUFFSIZE, 0)) < ``0``) {``    ``Die("Failed to receive initial bytes from client");``  ``}``  ``/* Send bytes and check for more incoming data in loop */``  ``while (received > 0) {``    ``/* Send back received data */``    ``if (send(sock, buffer, received, 0) != received) {``      ``Die("Failed to send bytes to client");``    ``}``    ``/* Check for more data */``    ``if ((received = recv(sock, buffer, BUFFSIZE, 0)) < 0) {``      ``Die("Failed to receive additional bytes from client");``    ``}``  ``}``  ``close(sock);``}`
```

传入处理函数的套接字是已经连接到发出请求的客户机的套接字。一旦完成所有数据的回显，就应该关闭这个套接字。父服务器套接字被保留下来，以便产生新的子套接字，就像刚刚被关闭那个套接字一样。

### TCP 回显服务器（配置服务器套接字）

就像前面所介绍的，创建套接字的目的对服务器和对客户机稍有不同。服务器创建套接字的语法与客户机相同，但结构 `echoserver` 是用服务器自己的信息而不是用它想与之连接的对等方的信息来建立的。您通常需要使用特殊常量 `INADDR_ANY` ，以支持接收服务器提供的任何 IP 地址上的请求；原则上，在诸如这样的多重主机服务器中，您可以相应地指定一个特定的 IP 地址。

```
`int main(int argc, char *argv[]) {``  ``int serversock, clientsock;``  ``struct sockaddr_in echoserver, echoclient;` `  ``if (argc != 2) {``    ``fprintf(stderr, "USAGE: echoserver <``port``>\n");``    ``exit(1);``  ``}``  ``/* Create the TCP socket */``  ``if ((serversock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {``    ``Die("Failed to create socket");``  ``}``  ``/* Construct the server sockaddr_in structure */``  ``memset(&echoserver, 0, sizeof(echoserver));       /* Clear struct */``  ``echoserver.sin_family = AF_INET;                  /* Internet/IP */``  ``echoserver.sin_addr.s_addr = htonl(INADDR_ANY);   /* Incoming addr */``  ``echoserver.sin_port = htons(atoi(argv[1]));       /* server port */`
```

注意，无论是IP地址还是端口，它们都要被转换为用于 `sockaddr_in` 结构的网络字节顺序。转换回本机字节顺序的逆向函数是 `ntohs()` 和 `ntohl()`。这些函数在某些平台上不可用，但是为跨平台兼容性而使用它们是明智的。

### TCP 回显服务器（绑定和监听）

虽然客户机应用程序 `connect()` 到某个服务器的 IP 地址和端口，但是服务器却 `bind()` 到它自己的地址和端口。

```
`/* Bind the server socket */``if (bind(serversock, (struct sockaddr *) &echoserver,``                             ``sizeof(echoserver)) < 0) {``  ``Die("Failed to bind the server socket");``}``/* Listen on the server socket */``if (listen(serversock, MAXPENDING) < 0) {``  ``Die("Failed to listen on server socket");``}`
```

一旦帮定了服务器套接字，它就准备好可以 `listen()` 了。与大多数套接字函数一样，如果出现问题，`bind()` 和 `listen()` 函数都返回 -1。一旦服务器套接字开始监听，它就准备 `accept()` 客户机连接，充当每个连接上的套接字的工厂。

### TCP 回显服务器（套接字工厂）

为客户机连接创建新的套接字是服务器的一个难题。函数 `accept()` 做两件重要的事情：返回新的套接字的套接字指针；填充指向`echoclient`（在我们的例子中） 的 `sockaddr_in` 结构。

```
`  ``/* Run until cancelled */``  ``while (1) {``    ``unsigned int clientlen = sizeof(echoclient);``    ``/* Wait for client connection */``    ``if ((clientsock =``         ``accept(serversock, (struct sockaddr *) &echoclient,``                ``&clientlen)) < 0) {``      ``Die("Failed to accept client connection");``    ``}``    ``fprintf(stdout, "Client connected: %s\n",``                    ``inet_ntoa(echoclient.sin_addr));``    ``HandleClient(clientsock);``  ``}``}`
```

我们可以看到 `echoclient` 中已填充的结构，它调用访问客户机 IP 地址的 `fprintf()`。客户机套接字指针被传递给 `HandleClient()`，我们在本节的开头看到了这点。

## 使用 Python 编写套接字应用程序

### 套接字和 SocketServer 模块

Python 的标准模块的 `socket `提供了可从 C scoket 中找到的几乎完全相同的功能。不过该接口通常更加灵活，主要是因为它有动态类型化的优点。此外，它还使用了面向对象的风格。例如，一旦您创建一个套接字对象，那么诸如 `.bind()`、 `.connect()` 和 `.send()` 之类的方法都是该对象的方法，而不是在某个套接字上执行操作的全局函数。 

在相比于 `socket `的更高层次上，模块 `SocketServer` 提供了用于编写服务器的框架。这仍然是相对低级的，还有可用于为更高级的协议提供服务的更高级接口。比如 `SimpleHTTPServer`、 `DocXMLRPCServer`和 `CGIHTTPServer`。

### 使用 Python 编写的 TCP 回显客户机

让我们来看一下这个完整的客户机，然后做一些解释：

```
`#!/usr/bin/env python``"USAGE: echoclient.py <``server``> <``word``> <``port``>"``from socket import *    # import *, but we'll avoid name conflict``import sys``if len(sys.argv) != 4:``    ``print __doc__``    ``sys.exit(0)``sock = socket(AF_INET, SOCK_STREAM)``sock.connect((sys.argv[1], int(sys.argv[3])))``message = sys.argv[2]``messlen, received = sock.send(message), 0``if messlen != len(message)``    ``print "Failed to send complete message"``print "Received: ",``while received < messlen:``    ``data = sock.recv(32)``    ``sys.stdout.write(data)``    ``received += len(data)``print``sock.close()`
```

初看起来，我们似乎从 C 版本中省去了一些错误捕捉代码。但是由于 Python 为我们在用 C 编写的客户机中检查的每种情形都给出了描述性的错误，我们可以让内置的异常（exception）为我们做这些工作。当然，如果我们希望准确描述以前的错误，那就不得不围绕这些调用向这个 socket 对象的方法添加几个 `try`/`except` 子句。

### 使用 Python 编写的 TCP 回显客户机（续）

虽然这个 Python 客户机比较短，但在某种程度上是功能强大的。特别地，我们馈送给 `.connect()` 调用的地址既可以是用圆点隔开的四段数字式的IP地址，也可以是是符号名称，而不需要额外的查找工作。例如： 

```
`$ ./echoclient 192.168.2.103 foobar 7``Received: foobar``$ ./echoclient.py fury.gnosis.lan foobar 7``Received: foobar`
```

我们还可以在 `.send()`和 `.sendall()` 之间做出选择。前者一次发送尽可能多的字节数，后者发送整个报文（如果不能发送就会引发一个异常）。对于这样的客户机，我们要说明的是，如果没有发送整个报文，那么就取回实际发送的准确字节数量。

### 使用 Python 编写的 TCP 回显服务器（SocketServer）

使用 Python 编写 TCP 回显服务器的最简单方法是使用 `SocketServer` 模块。使用这个模块式是如此容易，以致它几乎就像是在欺骗一样。在后面的几个小节中，我们将介绍遵循 C 实现的低级版本，不过现在让我们来看看使用它究竟有多简单：

```
`#!/usr/bin/env python``"USAGE: echoserver.py <``port``>"``from SocketServer import BaseRequestHandler, TCPServer``import sys, socket` `class EchoHandler(BaseRequestHandler):``    ``def handle(self):``        ``print "Client connected:", self.client_address``        ``self.request.sendall(self.request.recv(2**16))``        ``self.request.close()` `if len(sys.argv) != 2:``    ``print __doc__``else:``    ``TCPServer(('',int(sys.argv[1])), EchoHandler).serve_forever()`
```

唯一需要我们提供的就是具有一个 `.handle()` 方法的 `SocketServer.BaseRequestHandler` 的一个孩子。self 实例具有一些有用的属性，比如  `.client_address` 和 `.request`，后者本身是一个已连接的套接字对象。

### 使用 Python 编写的 TCP 回显服务器（套接字）

如果我们希望采用“避易就难”的实现方式，并且希望获得更精细的控制，我们可以使用 Python 来编写几乎跟使用 C 所编写的完全一样（不过具有更少的代码行）的回显服务器：

```
`#!/usr/bin/env python``"USAGE: echoclient.py <``server``> <``word``> <``port``>"``from socket import *    # import *, but we'll avoid name conflict``import sys` `def handleClient(sock):``    ``data = sock.recv(32)``    ``while data:``        ``sock.sendall(data)``        ``data = sock.recv(32)``    ``sock.close()` `if len(sys.argv) != 2:``    ``print __doc__``else:``    ``sock = socket(AF_INET, SOCK_STREAM)``    ``sock.bind(('',int(sys.argv[1])))``    ``sock.listen(5)``    ``while 1:    # Run until cancelled``        ``newsock, client_addr = sock.accept()``        ``print "Client connected:", client_addr``        ``handleClient(newsock)`
```

实在地说，这种“避易就难”的方式仍然不是很难。但是就像在 C 实现中一样，我们使用 `.listen()` 制造了新的已连接的套接字，并且调用了每个这样的连接的处理程序。

## 结束语和参考资料

### 结束语

在本教程中介绍的服务器和客户机很简单，但是它们展示了编写 TCP 套接字应用程序的每个基本要素。如果所传输的数据更复杂，或者应用程序中的对等方（客户机和服务器）之间的交互更高深，那就是另外的应用程序编程问题了。即使这样，所交换的数据仍然遵循 `connect()` 和 `bind()` 然后再 `send()` 和 `recv()` 的模式。

本教程没有谈及的一件事情是 UDP 套接字的使用，虽然我们在本教程开头的摘要中提到了。比起 UDP，TCP 使用得更普遍，不过同时理解 UDP 套接字以作为你编写应用程序的选择也是很重要的。在本教程的第二部分，我们将考察 UDP，同时也会介绍使用 Python 实现套接字应用程序，此外还会介绍一些其他的中间主题。

### 反馈

请告诉我们本教程是否对您有帮助，以及我们应该如何改进它。我们还想知道您希望我们提供关于其他哪些主题的教程。

关于本教程内容的问题，请通过 [mertz@gnosis.cx](mailto:mertz@gnosis.cx)与作者 David Mertz 联系。



#### 相关主题

- 关于使用 C 进行套接字编程的一本优秀入门读物是 Michael J. Donahoo 和 Kenneth L. Calvert 所著的[TCP/IP Sockets in C ](http://www.ussg.iu.edu/usail/network/nfs/layers.html)一书 (Morgan-Kaufmann, 2001)。例子和更多的信息可在该书的[作者页面](http://cs.ecs.baylor.edu/~donahoo/practical/CSockets/)找到。

  UNIX 系统支持组的文档 [Network Layers](http://www.ussg.iu.edu/usail/network/nfs/layers.html) 解释了较低网络层的功能。 

  传输控制协议（TCP）在 [RFC 793](http://www.rfc-editor.org/rfc/rfc793.txt) 中介绍。

  用户数据报协议（UDP）是 [RFC 768](http://www.rfc-editor.org/rfc/rfc768.txt) 的主题。

  读者可以在 IANA（Internet Assigned Numbers Authority ） Web 站点上找到[广泛使用的端口分配](http://www.iana.org/assignments/port-numbers)的列表。 

  "[Understanding Sockets in Unix, NT, and Java](http://www.ibm.com/developerworks/linux/library/j-sockets/understanding-sockets.html)" (*developerWorks*)用 C 和 Java 示例源代码阐述了套接字的基本原理。 

  "[RunTime: Programming sockets](http://www.ibm.com/developerworks/linux/library/l-rt6/)" (*developerWorks*) 比较了 Windows 和 Linux 上的套接字的性能。 

  AIX C 编程书籍 “*Communications Programming Concepts*”的 [Sockets ](http://publib16.boulder.ibm.com/pseries/en_US/aixprggd/progcomc/ch9_sockets.htm)部分深入地讨论了许多相关问题。 

  " *AIX 5L Version 5.2 Technical Reference* "的第 2 卷集中介绍了[通信](http://publib16.boulder.ibm.com/pseries/en_US/libs/commtrf2/mastertoc.htm#mtoc)，当然包括大量关于套接字编程的内容。 

  [Robocode 项目](http://robocode.alphaworks.ibm.com/home/home.html) (*alphaWorks*) 有一篇关于"[Using Serialization with Sockets](http://robocode.alphaworks.ibm.com/docs/jdk1.3/guide/serialization/examples/sockets/index3.html)" 的文章，其中包括 Java 源代码和例子。

  套接字、网络层次、UDP以及其他许多内容也在对话形式的 [Beej's Guide to Network Programming](http://www.ecst.csuchico.edu/~beej/guide/net/html/intro.html)中进行了讨论。

  您会发现 Gordon McMillan 的 [Socket Programming HOWTO](http://www.amk.ca/python/howto/sockets/) 和 Jim Frost 的 [BSD Sockets: A Quick and Dirty Primer](http://world.std.com/~jimf/papers/sockets/sockets.html) 也很有用。 

  在 developerWorks 的 [Linux 专区](http://www.ibm.com/developerworks/linux/)可以找到为 Linux 开发者准备的更多参考资料。





https://www.ibm.com/developerworks/cn/education/linux/l-sock/l-sock.html