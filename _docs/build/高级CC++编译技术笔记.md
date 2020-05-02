---
title: C++编译技术笔记
description: C++编译技术笔记
---

# C++编译技术笔记



**第一章、多任务操作系统基础**

虚拟内存、虚拟地址

进程的内存映射布局：节（section）

代码节（.text节）

数据节：初始化数据节（.data节）、未初始化数据节（.bss节）、只读数据（.rdata节）

堆

栈

二进制文件、编译器、链接器与装载器的作用

 

**第二章 程序生命周期阶段基础**

**编译阶段**

编译的各个阶段：

a. 预处理阶段

  gcc -E <input file> -o <output preprocessed file>.i

  gcc -E -P <input file> -o <output preprocessed file>.i    --简洁输出

b. 语言分析阶段：语法分析、语法分析、语义分析

c. 汇编阶段

  gcc -S -masm=att function.c -o function.s    --AT&T格式(默认)

  gcc -S -masm=intel function.c -o function.s    --Intel格式

d. 优化阶段

e. 代码生成阶段

  gcc -c <input file> -o <output file>.o

  反汇编工具：objdump

  objdump -D <input file>.o    --默认AT&T汇编风格

  objdump -D -M intel <input file>.o    --Intel汇编风格

 

目标文件的属性：

符号（symbol）和节（section）是目标文件的基本组成部分，其中符号表示的是程序中的内存地址或数据内存；节包括代码节（.text）、初始化数据节（.data）、未初始化数据节（.bss）等。

构建程序的目的在于：将编译的每个独立的源代码文件生成的节拼接到一个二进制可执行文件中。

目标文件中每个节的起始地地址都会被临时设置成0，等待链接时调整。

在将目标文件的节拼接到程序内存映射的过程中，其中唯一重要的参数是节的长度（节的地址范围）

 

**链接阶段**

a. 重定位：将分散在单独目标文件中的不同类型的节拼接到程序内存映射节中

b. 解析引用：检查拼接到程序内存映射中的节，找出哪些部分代码产生了外部调用，计算该引用的精确地址（在内存映射中的地址），最后将机器指令中的伪地址替换成程序内存映射的实际地址。

 

gcc -c function.c main.c

gcc function.o main.o -o demoApp

一步到位：

gcc function.c main.c -o demoApp

 

通过objdump命令可看到main.o中有未解析的引用，

 37:  e8 00 00 00 00      call  3c <main+0x3c>

 3c:  66 0f 7e c0       movd  eax,xmm0

 40:  89 45 fc         mov  DWORD PTR [rbp-0x4],eax

 43:  c7 05 00 00 00 00 01   mov  DWORD PTR [rip+0x0],0x1    # 4d <main+0x4d>

 4a:  00 00 00

 4d:  b8 00 00 00 00      mov  eax,0x0

 

而demoApp中已被解析

 4005b2:  e8 6b ff ff ff      call  400522 <add_and_multiply>

 4005b7:  66 0f 7e c0       movd  eax,xmm0

 4005bb:  89 45 fc         mov  DWORD PTR [rbp-0x4],eax

 4005be:  c7 05 74 0a 20 00 01   mov  DWORD PTR [rip+0x200a74],0x1    # 60103c <nCompletionStatus>

 4005c5:  00 00 00

 4005c8:  b8 00 00 00 00      mov  eax,0x0

 

对未初始化数据反编译：

命令：objdump -x -j .bss demoApp

SYMBOL TABLE:

0000000000601038 l  d .bss  0000000000000000       .bss

0000000000601038 l   O .bss  0000000000000001       completed.7259

000000000060103c g   O .bss  0000000000000004       nCompletionStatus

0000000000601040 g    .bss  0000000000000000       _end

0000000000601038 g    .bss  0000000000000000       __bss_start

 

可执行文件属性：

main函数并不是第一入口点，用于启动程序的一部分非常重要的代码片段，是在链接阶段才添加到程序内存映射中

crt0

crt1

 

各种节的类型（P34）

各种符号类型（P36）

 

 

**第三章 加载程序执行阶段**

shell：调用fork()

在程序名后输入一个与符号（&）那么子进程将会在后台执行

 

装载器的作用：将链接器创建的节复制到进程内存映射中，还会根据节的相同装载需求将链接器创建的节组合成段（segment）

查看段命令：readelf --segments demoApp

 

静态编译：gcc -static main.cpp -o main

 

程序执行入口点

<_start>

<__libc_start_main@plt>

__libc_start_main()函数的作用

栈和调用惯例

**第四章 重用概念的作用**

静态库

动态库

位置无关代码（position independent code,  PIC） -> 共享库

动态链接

Windows平台中动态链接的特点：.dll、.lib、.exp

应用程序二进制接口（ABI）

静态库和动态库对比

**第五章 使用静态库**

创建静态库：

gcc -c first.c second.c  

ar rcs libstaticlib.a first.o second.o

使用静态库：

gcc -c main.c

gcc main.o libstaticlib.a -o main

静态库的设计技巧：

提取静态库中的目标文件：

ar -x libstaticlib.a    --得到first.o和second.o

静态库在64位Linux平台上的问题：-fPIC                                                                                 

 

**第六章 设计动态链接库：基础篇** 

创建动态链接库：

gcc -fPIC -c first.c second.c

gcc -shared first.o second.o -o -libdynamiclib.so

理解：-fPIC代表什么（P71）

设计动态库：

理解：C++函数的名称修饰技术

在C++中，C风格的函数，要加extern "C"

问题2：静态初始化顺序问题

问题3：模板

设计应用程序的二进制接口（P79）

控制动态库的可见性：

__attribute__((visibility("hidden")))   隐藏函数接口，改成"default"则为可见

nm -D libdynamiclib.so  查看对外可见的函数符号

Makefile中：

VISIBILITY_FLAGS = -fvisibility=hidden -fvisibility-inlines-hidden

CFLAGS += $(VISIBILITY_FLAGS)

**第七章 定位库文件**

**构建过程中库文件的定位规则**

静态库命名规则：lib + <library name> + .a

动态库命令规则：lib + <library name> + .so + <library version information>

动态库的版本信息：<M>.<m>.<p>     ---分别为主、次、补丁版本

动态库的soname(共享库名称)：lib + <library name> + .so + <library major version digit(s)>    ---只包含主版本号

动态库的soname通常由链接器嵌入二进制文件的专有ELF字段中。通常使用特定的链接器选项，将表示库soname的字符串传递给链接器：

gcc -shared <list of object files> -Wl,-soname,libfoo.so.1 -o libfoo.so.1.0.0

查看soname：readelf -d /lib/i386-linux-gnu/libz.so.1.2.3.4

构建过程中库文件定位规则：链接到../sharedLib目录中的动态库libworkingdemo.so

gcc main.o -L../sharedLib -lworkingdemo -o demo

使用gcc命令一次性完成编译链接两个过程时，应该在链接器选项之前添加-Wl选项，如：

gcc -Wall -fPIC main.cpp -Wl,-L../sharedLib -Wl,-lworkingdemo -o demo

运行时动态库文件的定位规则：

预加载库：export LD_PRELOAD=/home/milan/project/libs/libmilan.so:$LD_PRELOAD

LD_LIBRARY_PATH环境变量：export LD_LIBRARY_PATH=/home/milan/projects:$LD_LIBRARY_PATH

在通过gcc间接调用链接器，而不是直接调用ld时，需要加上“-Wl,”前缀

第八章 动态库的设计：进阶篇（暂不学）

第九章 动态链接时的重复符号处理（暂不学）

第十章动态库的版本控制（暂不学）

**第十二章 Linux工具集**

快速查看工具

file /usr/bin/gst-inspect-0.10

size /usr/lib/i386-linux-gnu/libc-2.15.so   --获取ELF节的字节长度

详细分析工具

ldd /usr/bin/gst-inspect-0.10显示二进制文件启动时需要静态加载的动态库的完整列表

objdump -p /path/to/program | grep NEEDED

readelf -f /path/to/program | grep NEEDED

对比：ldd完成直接依赖项的定位后，会继续递归查找直接依赖项的依赖项

nm工具：列出二进制文件的符号列表

nm <二进制文件路径>    --列表二进制文件的所有符号

nm -D <二进制文件路径>    --只列出动态节中的符号（.dynamic，即共享训中导出的或对外可见的符号）

nm -C <二进制文件路径>     --列表未经过名称修饰的格式 

nm -D --no-demangle <二进制文件路径>   --打印出共享库中名称修饰后的动态符号

nm -A <库文件路径>/* | grep symbol-name  --递归搜索文件集合中是否包含某特定符号，如：

nm -AD * | grep pspell_aspell_dummy

nm -u <二进制文件路径>    --列表库中未定义的符号（库文件本身不包含，但期望在在运行时加载的其他动态库中提供） 

objdump工具

objdump -f ./driverApp/driver    --解析ELF头

objdump -h libmreloc.so    --列出并查看节信息

objdump -t libdemo1.so    --列出所有符号

objdump -T libdemo1.so    --只列出动态符号（与nm -D <二进制文件路径>一样）

objdump -p libdemo1.so    --查看动态节（Dynamic Section）信息

objdump -R libdemo1.so  --查看重定位节(DYNAMIC RELOCATION SECORDS）信息

objdump -s -j <节的名称> <二进制文件路径>  --查看节中的数据，如

objdump -s -j .got driver

objdump -p demoApp    --列出并查看段

objdump -d -M intel libmreloc.so | grep -A 10 ml_    --反编译代码

objdump -d -M intel -j .plt driver    --反编译指定节的代码

readelf工具

readelf -h driverApp/driver  --解析ELF头

readelf -S libmreloc.so    --列出并查看节信息

readelf --symbols libdemo1.so    --列出所有符号

readelf --syn-syms libdemo1.so    --只列表动态符号

readelf -d demoApp    --查看动态节

readelf -r libmreloc.so    --查看重定位节

readelf -x .got driver      --查看节中的数据

readelf --segments libmreloc.so    --列出并查看段

readelf --debug-dump=line <binary file path> | wc -l   --检测二进制文件是否包含调试信息

部署阶段工具（暂不学）

运行时分析工具

strace    --跟踪由进程产生的系统调用与进程接收的信息，有助于查看运行时所需的依赖项

addr2line -C -f -e /usr/mylibs/libxyz.so 0000d8cc6  --将运行时地址转成地址对应的源代码文件信息和行号

gdb（GNU调试器）（待学）

静态库工具

ar -rcs libmystaticlib.a first.o second.o third.o    --创建静态库

ar -t libmystaticlib.a    --列表静态库目标文件

ar -d libmystaticlib.a first.o  --从静态库中删除目标文件

ar -r libmystaticlib.a first.o    --将新的目标文件添加到静态库

 

**第十三章 平台实践**

链接过程调试（待学）

确定二进制文件类型

file <path-of-binary>

readelf -h <path-of-binary> | grep Type

EXEC(可执行文件)、DYN(共享目标文件)、REL(可重定位文件)

objdump -f <path-of-binary>

EXEC_P(可执行文件)、DYNAMIC(共享目标文件)

确定二进制文件入口点

获取可执行文件入口点：

readelf -h <path-of-binary> | grep Entry

objdump -f <path-of-binary> | grep start

获取动态库入口点：

LD_DEBUG=files gdb -q ./driver  

列出符号信息（见上一章）

查看节的信息（见上一章）

查看段的信息（见上一章）

反编译代码

objdump -d -M intel <path-to-binary>

objdump -d -M intel -S <path-to-binary>    --同时查看穿插在汇编指令中的源代码 

objdump -d -M intel -j .plt <path-to-binary>   --反编译某个节（默认会反编译所有包含代码的节）

判断是否为调试构建

readelf --debug-dump=line <path-to-binary>

如果二进制文件使用调试选项(-g)构建，则该命令会给出非空结果

查看加载时依赖项（见上一章）

查看装载器可以找到的库文件

ldconfig -p

即相当于位于/etc/ld.so.cache中的库文件











