---
title: GCC命令行
description: GCC命令行
---

# GCC命令行

#### 链接的-l与-L

undefined reference to 'xxxxx'错误，非编译错误，而是链接错误 
比如使用数学函数，则编译命令行要加入-lm

- -l参数，紧接着是库名，如：`-lm`（注：库文件名实际上libm.so） 
  若是第三方库，做法一，拷贝到/lib目录或/usr/lib目录或/usr/local/lib目录，然后同上；做法二，见下：
- -L参数，紧接着是库文件所在的目录，如：-`L/aaa/bbb/ccc -ltest`

注意顺序，如specific.o依赖于Libbroad库，而Libbroad库依赖于Libgeneral库，正确写法是： 
`gcc specific.o -lbroad -lgeneral`

#### 头文件的-include与-I参数

- -include参数，用来包含头文件，很少用，一般在源码中#include来实现
- -I参数，紧接着头文件存放的目录，如：-`I/abc/include` 
  /usr/include目录一般不用指定，GCC知道去那里找

#### 一些常用的选项

- -g，加入调试符号。
- -std=gnull，用来提示gcc应该允许符合C11和POSIX标准的代码使用。
- -O3，设置优化级别为三级，也就是尝试已知的所有方式去建立更快的代码。如果调试时发现太多变量被优化掉了，那么可换成-O0，以方便跟踪执行情况。
- -Wall，添加编译器警告。

#### 运行时连接

```
export LD_LIBRARY_PATH=libpath:$LD_LIBRARY_PATH
```