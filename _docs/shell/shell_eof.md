# linux shell脚本EOF妙用

2017年05月11日 20:36:25 [Zacy](https://me.csdn.net/zongshi1992) 阅读数：27184



在平时的运维工作中，我们经常会碰到这样一个场景：
执行脚本的时候，需要往一个文件里自动输入N行内容。如果是少数的几行内容，还可以用echo追加方式，但如果是很多行，那么单纯用echo追加的方式就显得愚蠢之极了！
这个时候，就可以使用EOF结合cat命令进行行内容的追加了。

下面就对EOF的用法进行梳理：
EOF是END Of File的缩写,表示自定义终止符.既然自定义,那么EOF就不是固定的,可以随意设置别名,在linux按ctrl-d就代表EOF.
EOF一般会配合cat能够多行文本输出.
其用法如下:
<<EOF        //开始
....
EOF            //结束

还可以自定义，比如自定义：
<<BBB        //开始
....
BBB              //结束

通过cat配合重定向能够生成文件并追加操作,在它之前先熟悉几个特殊符号:
< :输入重定向
\> :输出重定向
\>> :输出重定向,进行追加,不会覆盖之前内容

<< :标准输入来自命令行的一对分隔号的中间内容.

先举一个简单的例子，例1：
\# cat << EOF
在出现输入提示符">"，输入以下内容：
\> Hello
\> EOF
输入结束后，在终端显示以下内容：
Hello

思考：
我们可以从cat命令的说明中知道，cat的操作对象是文件，但是例1中cat的操作对象不是文件，而是用户输入。

那么我们可以这样理解例1：先在文件file中输入“Hello”，再用cat file输出其中的内容。

也就是说我们可以用一个文件来替代"<< EOF EOF"。

反过来说，如果操作命令中的文件是输入对象，也可以用"<< EOF EOF"来替代的。

为了验证上面的思考，我们试验两个例子：

例2. 假设有如下的磁盘分区脚本：

sfdisk -uM /dev/sda << EOF

,2048,b

,1024,83

,1024,83

EOF

根据之前的思考，将"<< EOF"和"EOF"之间的内容保存到文件part中，然后将脚本修改为：

sfdisk -uM /dev/sda < part

经测试，修改后的方式可以达到同样的分区结果。

例3. 将一个文件的内容输出到另一个文件中：

\# cat fileA > fileB

按照之前的思考，将"<< EOF EOF"替代输入对象文件fileA：

\# cat << EOF > fileB

经测试，命令执行后提示用户输入内容，输入结束后，用户的输入内容被保存到了fileB中。

综上所述，“<< EOF EOF”的作用是在命令执行过程中用户自定义输入，它类似于起到一个临时文件的作用，只是比使用文件更方便灵活。



下面通过具体实例来感受下EOF用法的妙处：
1）向文件test.sh里输入内容。
[root@slave-server opt]# cat << EOF >test.sh 
> 123123123
> 3452354345
> asdfasdfs
> EOF
[root@slave-server opt]# cat test.sh 
123123123
3452354345
asdfasdfs

追加内容
[root@slave-server opt]# cat << EOF >>test.sh 
> 7777
> 8888
> EOF
[root@slave-server opt]# cat test.sh 
123123123
3452354345
asdfasdfs
7777
8888

覆盖
[root@slave-server opt]# cat << EOF >test.sh
> 55555
> EOF
[root@slave-server opt]# cat test.sh 
55555

2）自定义EOF，比如自定义为wang
[root@slave-server opt]# cat << wang > haha.txt
> ggggggg
> 4444444
> 6666666
> wang
[root@slave-server opt]# cat haha.txt 
ggggggg
4444444
6666666

3）可以编写脚本，向一个文件输入多行内容
[root@slave-server opt]# touch /usr/local/mysql/my.cnf               //文件不提前创建也行，如果不存在，EOF命令中也会自动创建
[root@slave-server opt]# vim test.sh
\#!/bin/bash

cat > /usr/local/mysql/my.cnf << EOF                                      //或者cat << EOF > /usr/local/mysql/my.cnf
[client]
port = 3306
socket = /usr/local/mysql/var/mysql.sock

[mysqld]
port = 3306
socket = /usr/local/mysql/var/mysql.sock

basedir = /usr/local/mysql/
datadir = /data/mysql/data
pid-file = /data/mysql/data/mysql.pid
user = mysql
bind-address = 0.0.0.0
server-id = 1
sync_binlog=1
log_bin = mysql-bin

[myisamchk]
key_buffer_size = 8M
sort_buffer_size = 8M
read_buffer = 4M
write_buffer = 4M

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES 
port = 3306
EOF

[root@slave-server opt]# sh test.sh           //执行上面脚本
[root@slave-server opt]# cat /usr/local/mysql/my.cnf    //检查脚本中的EOF是否写入成功
[client]
port = 3306
socket = /usr/local/mysql/var/mysql.sock

[mysqld]
port = 3306
socket = /usr/local/mysql/var/mysql.sock

basedir = /usr/local/mysql/
datadir = /data/mysql/data
pid-file = /data/mysql/data/mysql.pid
user = mysql
bind-address = 0.0.0.0
server-id = 1
sync_binlog=1
log_bin = mysql-bin

[myisamchk]
key_buffer_size = 8M
sort_buffer_size = 8M
read_buffer = 4M
write_buffer = 4M

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES 
port = 3306

\---------------------------------------------------------------------------------
下面分享一个自动新建分区并挂载的脚本：

`[root@es-node1 ~]``# cat auto_add_disk.sh         ``#!/bin/bash``fdisk` `/dev/sdb` `<<EOF``n``p``1`  `wq``EOF` `/sbin/mkfs``.ext4 ``/dev/sdb1` `&&  ``/bin/mkdir` `-p ``/data` `&& ``/bin/mount` `/dev/sdb1` `/data``echo` `'LABEL=data_disk /data ext4 defaults 0 2'` `>> ``/etc/fstab`



https://blog.csdn.net/zongshi1992/article/details/71693045