---
title: Linux Shell脚本应用学习笔记
description: Linux Shell脚本应用学习笔记
---

Linux Shell脚本应用学习笔记



**1. 初识Shell脚本**

**1.1 初识Shell脚本**

useradd stanyung

echo 123456 | passwd --stdin stanyung

**1.2 创建Shell脚本**

\#!/bin/bash

\#2013-02-28, by stanyung.

echo "xxx"

useradd stanyung

echo 123456 | passwd --stdin stanyung

**1.3 执行Shell脚本**

方法1：

chmod +x uad.sh

./uad.sh

方法2：

sh uad.sh

方法3：

source uad.sh

**2. Shell命令的组合运用**

**2.1 管道操作**

find /etc -name "*.conf" -type f

find /etc -name "*.conf" -type f | wc -l

ps aux | grep httpd

**2.2 重定向操作**

重定向输入： <  （从指定文件读取数据，而不是从键盘输入）

重定向输出： >、>>  （将输出结果覆盖、追加到指定文件）

标准错误输出：2>、2>>  （将错误信息覆盖、追加到指定文件）

混合输出：&>、&>>  （将标准输出和错误信息覆盖、追加到指定的文件）

如：

username -r > version.txt

cat version.txt version2.txt 2> error.txt

**2.3 命令分隔**

逻辑与： &&

逻辑或： ||

顺序执行： ;

如：

mkdir /mulu/a 2> dev/null && echo "Success."

mkdir /mulu/a 2> dev/null || echo "Fail."

cd /boot/grub ; ls -lh grub.conf

**3. 使用变量**

**3.1 引号**

双引号：允许引用、\转义

echo "$Title Group"

单引号：禁止引用、转义

echo '$TitleGroup'  原样输出

反撇号，或者$()：以命令输出进行替换

Ver=`uname -r`   

echo $Ver

**3.2 常用的环境变量**

env   输出环境变量

echo $USER $HOME SHELL

echo $LANG

用来记录/设置运行参数：

系统赋值：USER、LOGNAME、HOME、SHELL、……

用户操作：PATH、LANG、CLASSPATH、……

**3.3 其他特殊变量**

$?：前一条命令的状态值，0为正常，非0异常

$0：脚本自身的程序名

$1-$9：第1-第9个位置参数

$*：命令行的所有位置参数的内容

$#：命令行的位置参数个数

如：./test.sh Hello Everybody!

在test.sh中可打印上面的值

**4. 数值运算及处理**

**4.1 整数运算操作**

expr 45 + 21

expr 45 - 21

expr 45 \* 21

expr 45 / 21

expr 45 % 21

X=45; Y=21; expr $X - $Y

**4.2 使用$[]**

echo $[45+21]

echo $[45*21]

X=45; Y=21; echo $[X-Y]

**4.3 递增、随机数、序列**

变量递增处理：let 变量名++、let 变量名--

使用随机数：RANDOM 变量，如：echo $RANDOM; echo $[RANDOM%100]

生成数字序列：seq 首数 末数、seq 首数 增量 末数

**4.4 将表达式给bc命令处理**

echo "45.67-21.05" | bc

echo "scale=4; 10/3" | bc   其中scale用来约束结果的小数位数

**5. 字符串处理**

**5.1 路径分割**

Var1 = "/etc/httpd/config/httpd.conf"

dirname $Var1

basename $Var1

**5.2 使用expr命令**

expr substr $Var1 起始位置(从1开始) 截取长度

${Var1:起始位置(从0开始):截取长度}

如：

Var1=ABCEDFGHIJKLMN

expr substr $Var1 4 6

**5.3 字符串替换**

${Var1/old/new}  把变量Var1中的第一个old替换成new

${Var1//old/new} 把变量Var1中的所有的old替换成new

**5.4 使用随机字符串**

随机设备：/dev/urandom

MD5转换：/usr/bin/md5sum

字符串切割：/bin/cut

随机字符->ASCII字符：

head -1 /dev/urandom | md5sum

使用cut切割字符串：

echo $Var1 | cut -b 起始位置-结束位置    （起始位置或结束位置可省略）

head -1 /dev/urandom | md5sum | cut -b -8

**6. 条件测试**

**6.1 测试操作规范**

$? 根据返回值判断条件是否成立

格式一：test 条件表达式

格式二：[ 条件表达式 ]

[ 条件表达式 ] && echo YES

[ -d "/etc/grub" ] && echo YES    判断是否是一个目录

**6.2 文件状态的检测**

-e: 目录是否存在（Exist）

-d: 是否为目录(Directory)

-f: 是否为文件(File)

-r: 是否有读取(Read)的权限

-w: 是否有写入(Write)的权限

-x: 是否有可执行(eXcute)的权限

-s:如果文件存在且文件大小大于零，则返回真

**6.3 整数值比较、字串匹配**

-eq: 等于(Equal)

-ne: 不等于(Not Equal)

-gt: 大于(Greater Than)

-lt: 小于(Lesser Than)

-ge: 大于或等于(Greater or Equal)

-le:小于或等于(Lesser or Equal)

who | wc -l   当前登录用户数

[ $(who | wc -l) -eq 2 ] && echo YES

字符串匹配：

=: 可个字符串相同

!=:可个字符串不相同

[$USER = "root"] && echo YES

**7. 使用if判断结构**

**1. 单分支/双分支的if应用**

if 条件测试

  then 命令序列1

  else 命令序列2

fi

**2. 多条件**

elif 条件测试2

  then 命令序列2

**8. 使用for循环**

for 变量名 in  取值列表

do

  命令序列

done

例如：

\#!/bin/bash

for i in "lst" "2nd" "3rd"

do

  echo $i

done

for i in $(cat /etc/host.conf)

for IP in $(seq 1 5)