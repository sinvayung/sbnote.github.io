---
title: 解析二进制的Shell命令
description: 解析二进制的Shell命令
---

解析二进制的Shell命令



#### 进制转换

使用$((BASE#NUMBER))的形式：

 

```
$ echo $((013))    #八进制转十进制
$ echo $((0xA4))   #16进制转十进制
$ echo $((8#13))    #八进制转十进制
$ echo $((16#A4))   #16进制转十进制
```

使用BC计算：

 

```
$ echo 'obase=16; 47' | bc
2F
$ echo 'obase=10; ibase=16; A03' | bc
2563
```

#### ascii转16进制

 

```
rongxinhua@ubuntu:~$ echo -n "ELF" | od -A n -t x1
 45 4c 46
```

 

```
rongxinhua@ubuntu:~$ echo -n 'ELF' | xxd -ps
454c46
```

 

```
rongxinhua@ubuntu:~$ echo -n 'ELF' | xxd -ps | sed 's/[[:xdigit:]]\{2\}/\\x&/g'
\x45\x4c\x46

```

#### 搜索Byte

 

```
Usage: grep [OPTION]... PATTERN [FILE]...
Search for PATTERN in each FILE or standard input
```

判断是否ELF文件：

 

```
grep -a -b -o -P '\x7f\x45\x4c\x46' vmlinux
```

解析：

- -a，支持二进制文件，默认只支持文本文件
- -b，匹配偏移
- -o，仅显示匹配的部分，其他不显示
- -P， PATTERN is a Perl regular expression

从zImage中查找ELF头：

 

```
rongxinhua@ubuntu:~$ dd if=zImage of=vmlinux bs=1 skip=22663168
2419120+0 records in
2419120+0 records out
2419120 bytes (2.4 MB) copied, 6.22087 s, 389 kB/s
```

#### 文件属性

 

```
rongxinhua@ubuntu:~$ file vmlinux
vmlinux: ELF 64-bit LSB  shared object, ARM aarch64, version 1 (SYSV), dynamically linked, stripped
```