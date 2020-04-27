---
title: 一句话讲透epoll
description: 一句话讲透epoll
---

# 一句话讲透epoll

## 1. epoll概念

在Linux的Man文档中，我们可以看到如下定义

> **Epoll - I/O event notification facility**
>  epoll是一种I/O事件通知机制

#### I/O事件

- I/O
   输入输出(input/output)，输入输出的对象可以是  文件(file),  网络(socket), 进程之间的管道(pipe),  在linux系统中，都用文件描述符(fd)来表示
- 事件
  - 可读事件， 当文件描述符关联的内核读缓冲区可读，则触发可读事件
     什么是可读呢？  **就是内核缓冲区非空，有数据可以读取** 
  - 可写事件,   当文件描述符关联的内核写缓冲区可写，则触发可写事件
     什么是可写呢？**就是内核缓冲区不满，有空闲空间可以写入** 

#### 通知机制

- 通知机制，就是当事件发生的时候，去通知他
- 通知机制的反面，就是轮询机制

以上两点结合起来理解

> **epoll是一种当文件描述符的内核缓冲区非空的时候，发出可读信号进行通知，当写缓冲区不满的时候，发出可写信号通知的机制**

## 2. 水平触发与边缘触发

#### 水平触发(level-trggered)

- 只要文件描述符关联的读内核缓冲区非空，有数据可以读取，就一直发出可读信号进行通知，
- 当文件描述符关联的内核写缓冲区不满，有空间可以写入，就一直发出可写信号进行通知

#### 边缘触发(edge-triggered)

- 当文件描述符关联的读内核缓冲区由空转化为非空的时候，则发出可读信号进行通知，
- 当文件描述符关联的内核写缓冲区由满转化为不满的时候，则发出可写信号进行通知

> 两者的区别在哪里呢？水平触发是只要读缓冲区有数据，就会一直触发可读信号，而边缘触发仅仅在空变为非空的时候通知一次，举个例子：

1. 读缓冲区刚开始是空的
2. 读缓冲区写入2KB数据
3. 水平触发和边缘触发模式此时都会发出可读信号
4. 收到信号通知后，读取了1kb的数据，读缓冲区还剩余1KB数据
5. 水平触发会再次进行通知，而边缘触发不会再进行通知

**所以边缘触发需要一次性的把缓冲区的数据读完为止，也就是一直读，直到读到EGAIN为止，EGAIN说明缓冲区已经空了，因为这一点，边缘触发需要设置文件句柄为非阻塞**

```c
//水平触发
ret = read(fd, buf, sizeof(buf));

//边缘触发
while(true) {
    ret = read(fd, buf, sizeof(buf);
    if (ret == EAGAIN) break;
}
```

## 3. epoll接口介绍

- epoll_create

  - 创建epoll实例，会创建所需要的红黑树，以及就绪链表，以及代表epoll实例的文件句柄 

    > int epoll_create(int size);
    >  Man文档中说明了在老的内核版本中，入参size用来指出创建的内部数据结构的大小，目前已经可以动态调整，但是为了兼容老的版本，所以仍然保留，这个size其实意义已经不大

- epoll_ctl

  - 添加，修改，或者删除 注册到epoll实例中的文件描述符上的监控事件

    > int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event)
    >  对于添加到epfd的文件描述符fd,  添加或者删除或者修改， 对应的event

    - epfd:  通过epoll_create创建的文件描述符

    - op:操作类型
       EPOLL_CTL_ADD, 为相应fd添加事件
       EPOLL_CTL_MOD, 修改fd的事件
       EPOLL_CTL_DEL，删除fd上的某些事件

    - fd: 操作的目标文件描述符

    - event: 要操作的事件 

      ```c
      typedef union epoll_data {
          void  *ptr;
          int  fd;
          uint32_t     u32;
          uint64_t     u64;
      } epoll_data_t;
        
      struct epoll_event {
          uint32_t  events;    /* Epoll events */
          epoll_data_t data;    /* User data variable */
      };
      
      /*
      events可以是一组bit的组合
          EPOLLIN：可读
          EPOLLOUT: 可写
          EPOLLET: 边缘触发，默认是水平触发
      */
      ```

- epoll_wait

  > int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout)
  >  等待注册的事件发生，返回事件的数目，并将触发的事件写入events数组中

  - epfd: epoll实例文件描述符
  - events: 数组出参，用来记录被触发的events，其大小应该和maxevents一致
  - maxevents: 返回的events的最大个数，如果最大个数大于实际触发的个数，则下次epoll_wait的时候仍然可以返回
  - timeout: 等待事件，毫秒为单位 -1:无限等待 0:立即返回

## 4. 示例代码

```c
/* 
使用 epoll 写的回射服务器 
将从client中接收到的数据再返回给client 
 
*/  
#include <iostream>  
#include <sys/socket.h>  
#include <sys/epoll.h>  
#include <netinet/in.h>  
#include <arpa/inet.h>  
#include <fcntl.h>  
#include <unistd.h>  
#include <stdio.h>  
#include <errno.h>  
  
using namespace std;  
  
#define MAXLINE 100  
#define OPEN_MAX 100  
#define LISTENQ 20  
#define SERV_PORT 5000  
#define INFTIM 1000  
  
void setnonblocking(int sock)  
{  
    int opts;  
     opts=fcntl(sock,F_GETFL);  
    if(opts<0)  
    {  
        perror("fcntl(sock,GETFL)");  
        exit(1);  
    }  
     opts = opts|O_NONBLOCK;  
    if(fcntl(sock,F_SETFL,opts)<0)  
    {  
        perror("fcntl(sock,SETFL,opts)");  
        exit(1);  
    }  
}  
  
int main(int argc, char* argv[])  
{  
    int i, maxi, listenfd, connfd, sockfd,epfd,nfds, portnumber;  
    ssize_t n;  
    char line[MAXLINE];  
    socklen_t clilen;  
    string szTemp("");  
  
    if ( 2 == argc )  
    {  
        if( (portnumber = atoi(argv[1])) < 0 )  
        {  
            fprintf(stderr,"Usage:%s portnumber\a\n",argv[0]);  
            return 1;  
        }  
    }  
    else  
    {  
        fprintf(stderr,"Usage:%s portnumber\a\n",argv[0]);  
        return 1;  
    }  
  
  
  
    //声明epoll_event结构体的变量,ev用于注册事件,数组用于回传要处理的事件  
    struct epoll_event ev, events[20];  
      
    //创建一个epoll的句柄，size用来告诉内核这个监听的数目一共有多大  
    epfd = epoll_create(256); //生成用于处理accept的epoll专用的文件描述符  
      
    struct sockaddr_in clientaddr;  
    struct sockaddr_in serveraddr;  
    listenfd = socket(AF_INET, SOCK_STREAM, 0);  
      
    //把socket设置为非阻塞方式  
    //setnonblocking(listenfd);  
  
    //设置与要处理的事件相关的文件描述符  
    ev.data.fd=listenfd;  
      
    //设置要处理的事件类型  
    ev.events=EPOLLIN|EPOLLET;  
  
    //注册epoll事件  
    epoll_ctl(epfd,EPOLL_CTL_ADD,listenfd,&ev);  
      
    bzero(&serveraddr, sizeof(serveraddr)); /*配置Server socket的相关信息 */  
    serveraddr.sin_family = AF_INET;  
    char *local_addr="127.0.0.1";  
    inet_aton(local_addr,&(serveraddr.sin_addr));//htons(portnumber);  
    serveraddr.sin_port=htons(portnumber);  
    bind(listenfd,(sockaddr *)&serveraddr, sizeof(serveraddr));  
      
    listen(listenfd, LISTENQ);  
      
    maxi = 0;  
      
    for ( ; ; ) {  
          
        //等待epoll事件的发生  
        //返回需要处理的事件数目nfds，如返回0表示已超时。  
        nfds=epoll_wait(epfd,events,20,500);  
          
        //处理所发生的所有事件  
        for(i=0; i < nfds; ++i)  
        {  
            //如果新监测到一个SOCKET用户连接到了绑定的SOCKET端口，建立新的连接。  
            if(events[i].data.fd == listenfd)  
            {  
                connfd = accept(listenfd,(sockaddr *)&clientaddr, &clilen);  
                if(connfd < 0)  
                {  
                    perror("connfd < 0");  
                    exit(1);  
                }  
                //setnonblocking(connfd);  
                char *str = inet_ntoa(clientaddr.sin_addr);  
                cout << "accapt a connection from " << str << endl;  
                  
                //设置用于读操作的文件描述符  
                  ev.data.fd=connfd;  
                  
                //设置用于注册的读操作事件  
                  ev.events=EPOLLIN|EPOLLET;  
  
                //注册ev  
                epoll_ctl(epfd,EPOLL_CTL_ADD,connfd,&ev); /* 添加 */  
            }  
            //如果是已经连接的用户，并且收到数据，那么进行读入。  
            else if(events[i].events&EPOLLIN)  
            {  
                cout << "EPOLLIN" << endl;  
                if ( (sockfd = events[i].data.fd) < 0)  
                    continue;  
                if ( (n = recv(sockfd, line, sizeof(line), 0)) < 0)   
                {    
                    // Connection Reset:你连接的那一端已经断开了，而你却还试着在对方已断开的socketfd上读写数据！  
                    if (errno == ECONNRESET)  
                    {  
                        close(sockfd);  
                        events[i].data.fd = -1;  
                    }   
                    else  
                        std::cout<<"readline error"<<std::endl;  
                }   
                else if (n == 0) //读入的数据为空  
                {  
                    close(sockfd);  
                    events[i].data.fd = -1;  
                }  
                  
                szTemp = "";  
                szTemp += line;  
                szTemp = szTemp.substr(0,szTemp.find('\r')); /* remove the enter key */  
                memset(line,0,100); /* clear the buffer */  
                //line[n] = '\0';  
                cout << "Readin: " << szTemp << endl;  
                  
                //设置用于写操作的文件描述符  
                ev.data.fd=sockfd;  
                  
                //设置用于注册的写操作事件  
                ev.events=EPOLLOUT|EPOLLET;  
                  
                //修改sockfd上要处理的事件为EPOLLOUT  
                epoll_ctl(epfd,EPOLL_CTL_MOD,sockfd,&ev); /* 修改 */  
  
            }  
            else if(events[i].events&EPOLLOUT) // 如果有数据发送  
  
            {  
                sockfd = events[i].data.fd;  
                szTemp = "Server:" + szTemp + "\n";  
                send(sockfd, szTemp.c_str(), szTemp.size(), 0);  
                  
                  
                //设置用于读操作的文件描述符  
                ev.data.fd=sockfd;  
                 
                //设置用于注册的读操作事件  
                ev.events=EPOLLIN|EPOLLET;  
                  
                //修改sockfd上要处理的事件为EPOLIN  
                epoll_ctl(epfd,EPOLL_CTL_MOD,sockfd,&ev); /* 修改 */  
            }  
        } //(over)处理所发生的所有事件  
    } //(over)等待epoll事件的发生  
      
    close(epfd);  
    return 0;  
}  
```



[^一句话讲透epoll]: https://www.jianshu.com/p/41dc33b97419



