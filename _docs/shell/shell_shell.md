5. netstat - 检验各端口的网络连接情况

netstat命令用于显示TP，TCP，UDP和ICMP等协议相关的统计数据，一般用于检验本机各端口的网络连接情况。

语  法：netstat [选项]

参  数：
  -a  显示所有选项，默认不显示LISTEN相关
  -t  仅显示TCP相关选项
  -u  仅显示UDP相关选项
  -n  拒绝显示别名，能显示数字的全部转化成数字
  -l  仅列出有在Listen的服务状态
  -p  显示建立相关连接的程序名
  -r  显示路由信息，路由表
  -e  显示扩展信息，例如uid等
  -s  按各个协议进行统计
  -c  每隔一个固定时间，执行该netstat命令

注： LISTEN和LISTENING的状态只有用-a或者-l才能看到 
常用的查看网络TCP网络连接命令为netstat -ntlp ，我们能查看其连接状态，IP地址，以及连接的端口号等信息。

https://blog.csdn.net/Hairy_Monsters/article/details/80538303 





# 3. 查看磁盘状况

df -h
查看某个目录的大小
du -sh dir
查看当前目录下所有文件的大小
du -sh *



# 7. 后台执行

nohup ./program&

https://blog.csdn.net/okiwilldoit/article/details/78296631

