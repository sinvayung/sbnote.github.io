# Android.mk文件语法详解

## Android.mk简介：

Android.mk文件用来告知NDK Build系统关于Source的信息。Android.mk将是GNU Makefile的一部分，且将被Build System解析一次或多次。
所以，请尽量少的在Android.mk中声明变量，也不要假定任何东西不会在解析过程中定义。

Android.mk文件语法允许我们将Source打包成一个"modules"，modules可以是：

- 静态库
- 动态库

只有动态库可以被install/copy到应用程序包(APK)， 静态库则可以被链接入动态库。

可以在一个Android.mk中定义一个或多个modules. 也可以将同一份source加进多个modules。

Build System帮我们处理了很多细节而不需要我们再关心。例如：你不需要在Android.mk中列出头文件和外部依赖文件。
NDK Build System自动帮我们提供这些信息。这也意味着，当用户升级NDK后，你将可以受益于新的toolchain/platform而不必再去修改Android.mk。

## Android.mk语法

#### 1. 基本语法

首先看一个最简单的Android.mk的例子：

```makefile
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE    := hello-jni
LOCAL_SRC_FILES := hello-jni.c
include $(BUILD_SHARED_LIBRARY)
```

讲解如下：

```makefile
LOCAL_PATH := $(call my-dir)
```

每个Android.mk文件必须以定义**LOCAL_PATH**为开始，它用于在开发tree中查找源文件；宏**my-dir**则由Build System提供，返回包含Android.mk的目录路径。

```makefile
include $(CLEAR_VARS)
```

**CLEAR_VARS** 变量由Build System提供，并指向一个指定的GNU Makefile，由它负责清理很多LOCAL_xxx。例如：**LOCAL_MODULE, LOCAL_SRC_FILES, LOCAL_STATIC_LIBRARIES**等等。但不清理LOCAL_PATH，这个清理动作是必须的，因为所有的编译控制文件由同一个GNU Make解析和执行，其变量是全局的，所以清理后才能避免相互影响。

```makefile
LOCAL_MODULE    := hello-jni
```

**LOCAL_MODULE**模块必须定义，以表示Android.mk中的每一个模块。名字必须唯一且不包含空格。
Build System会自动添加适当的前缀和后缀。例如，foo，要产生动态库，则生成libfoo.so。 但请注意：如果模块名被定为：libfoo，则生成libfoo.so，不再加前缀。

```makefile
LOCAL_SRC_FILES := hello-jni.c
```

**LOCAL_SRC_FILES** 变量必须包含将要打包如模块的 C/C++ 源码。
不必列出头文件，Build System 会自动帮我们找出依赖文件。
缺省的C++源码的扩展名为.cpp。 也可以修改，通过LOCAL_CPP_EXTENSION。

```makefile
include $(BUILD_SHARED_LIBRARY)
```

**BUILD_SHARED_LIBRARY** 是Build System提供的一个变量，指向一个GNU Makefile Script。
它负责收集自从上次调用 include $(CLEAR_VARS) 后的所有LOCAL_XXX信息，并决定编译为什么。

- BUILD_STATIC_LIBRARY：编译为静态库
- BUILD_SHARED_LIBRARY：编译为动态库
- BUILD_EXECUTABLE：编译为Native C可执行程序

### 2. NDK Build System变量

NDK Build System 保留以下变量名：

- 以**LOCAL_**、**PRIVATE_**，**NDK_**、**APP_** 开头的名字
- 小写字母名字，如：**my-dir**
  如果想要定义自己在Android.mk中使用的变量名，建议添加 **MY_** 前缀。

#### 2.1 NDK提供的变量

此类GNU Make变量是NDK Build System在解析Android.mk之前就定义好了的。

##### 2.1.1 CLEAR_VARS

指向一个编译脚本，必须在新模块前包含之。

```makefile
include $(CLEAR_VARS)
```

##### 2.1.2 BUILD_SHARED_LIBRARY

指向一个编译脚本，它收集自从上次调用include $(CLEAR_VARS) 后的所有LOCAL_XXX信息。
并决定如何将你列出的Source编译成一个动态库。 注意：在包含此文件前，至少应该包含：LOCAL_MODULE and LOCAL_SRC_FILES，例如：

```makefile
include $(BUILD_SHARED_LIBRARY)   
```

##### 2.1.3 BUILD_STATIC_LIBRARY

与前面类似，它也指向一个编译脚本，
收集自从上次调用 include $(CLEAR_VARS) 后的所有LOCAL_XXX信息。
并决定如何将你列出的Source编译成一个静态库。 静态库不能够加入到Project 或者APK中。但它可以用来生成动态库。
LOCAL_STATIC_LIBRARIES and LOCAL_WHOLE_STATIC_LIBRARIES将描述之。

```makefile
include $(BUILD_STATIC_LIBRARY)
```

##### 2.1.4 BUILD_EXECUTABLE

与前面类似，它也指向一个编译脚本，收集自从上次调用 include $(CLEAR_VARS) 后的所有LOCAL_XXX信息。
并决定如何将你列出的Source编译成一个可执行Native程序。

```makefile
include $(BUILD_EXECUTABLE) 
```

##### 2.1.5 PREBUILT_SHARED_LIBRARY

把这个共享库声明为 “一个” 独立的模块。
指向一个build 脚本，用来指定一个预先编译好多动态库。 与BUILD_SHARED_LIBRARY and BUILD_STATIC_LIBRARY不同，
此时模块的LOCAL_SRC_FILES应该被指定为一个预先编译好的动态库，而非source file.

```makefile
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := foo-prebuilt     # 模块名
LOCAL_SRC_FILES := libfoo.so     # 模块的文件路径（相对于 LOCAL_PATH）

include $(PREBUILT_SHARED_LIBRARY) # 注意这里不是 BUILD_SHARED_LIBRARY
```

这个共享库将被拷贝到 $PROJECT/obj/local 和 $PROJECT/libs/ (stripped) 主要是用在将已经编译好的第三方库
使用在本Android Project中。为什么不直接将其copy到libs/armabi目录呢？因为这样做缺陷很多。

##### 2.1.6 PREBUILT_STATIC_LIBRARY

预先编译的静态库，同上。

##### 2.1.7 TARGET_ARCH

目标CPU架构名，如果为“arm” 则声称ARM兼容的指令，与CPU架构版本无关。

```makefile
ifeq ($(TARGET_ARCH),arm)  
  ... 
endif
```

##### 2.1.8 TARGET_PLATFORM

目标平台的名字，对应android版本号，取值包括：android-8、android-9...android-21。

```makefile
ifeq ($(TARGET_PLATFORM),android-8)  
  ... 
endif
```

##### 2.1.9 TARGET_ARCH_ABI

是反应当前的cpu/abi的类型，取值包括：
32位：armeabi、armeabi-v7a、x86、mips；
64位：arm64-v8a、x86_64、mips64；

```makefile
ifeq ($(TARGET_ARCH_ABI),armeabi-v7a)  
  RS_TRIPLE := armv7-none-linux-gnueabi  
endif  
ifeq ($(TARGET_ARCH_ABI),armeabi)  
  RS_TRIPLE := arm-none-linux-gnueabi  
endif  
ifeq ($(TARGET_ARCH_ABI),mips)  
  RS_TRIPLE := mipsel-unknown-linux  
endif  
ifeq ($(TARGET_ARCH_ABI),x86)  
  RS_TRIPLE := i686-unknown-linux  
endif  
```

#### 2.2 NDK提供的功能宏

GNU Make 提供的功能宏，只有通过类似： $(call function) 的方式来得到其值，它将返回文本化的信息。

##### 2.2.1 my-dir

返回最近一次include的Makefile的路径，通常返回Android.mk所在的路径，它用来作为Android.mk的开头来定义LOCAL_PATH。

```makefile
LOCAL_PATH := $(call my-dir)
```

注意：==返回的是最近一次include的Makefile的路径。所以在include其它Makefile后，再调用$(call my-dir)会返回其它Android.mk所在路径。==
例如：

```makefile
LOCAL_PATH := $(call my-dir) # declare one module
...
include $(LOCAL_PATH)/foo/Android.mk   
LOCAL_PATH := $(call my-dir) # declare another module
```

则第二次返回的LOCAL_PATH为：$PATH/foo，而非$PATH。

##### 2.2.2 all-subdir-makefiles

返回一个列表，包含 “my-dir” 中所有子目录中的Android.mk。
例如：
sources/foo/Android.mk
sources/foo/lib1/Android.mk
sources/foo/lib2/Android.mk

在sources/foo/Android.mk中:

```makefile
include $(call all-subdir-makefiles)
```

那则自动include了:
sources/foo/lib1/Android.mk
sources/foo/lib2/Android.mk

##### 2.2.3 this-makefile

当前Makefile的路径。

##### 2.2.4 parent-makefile

返回include tree中父Makefile路径，也就是include当前Makefile的Makefile路径。

##### 2.2.5 import-module

允许寻找并import其它Modules到本Android.mk中来。 它会从**NDK_MODULE_PATH**寻找指定的模块名。

==import-module和include区别：
功能基本一样。
概念区别：include导入的是由我们自己写的Makefile。而import-module导入的是外部库、外部模块提供的Makefile。
用法区别：include的路径是Makefile文件的绝对路径。
而import-module是NDK_MODULE_PATH中路径列表的相对路径。==

```makefile
$(call import-module, 模块名/子目录)
```

**NDK_MODULE_PATH**的配置：
NDK_MODULE_PATH 是一个环境变量，不是Android.mk中设置的变量。

1. 直接将 “NDK_MODULE_PATH=路径1:路径2” 加到 ndk-build命令的参数后面：

```makefile
$ndk-build -C $HELLOWORLD_ROOT NDK_MODULE_PATH=路径1:路径2
```

1. 在Android.mk中设置NDK_MODULE_PATH:

```makefile
$(call import-add-path,$(LOCAL_PATH)/platform/third_party/android/prebuilt)
```

1. 在系统环境里手动添加这个环境变量。

例如：
有一个Android.mk路径如下：
*F:\cocos2d-x\CocosDenshion\android\android.mk* 
已设置：*NDK_MODULE_PATH=/cygdrive/f/cocos2d-x*
那么在Android.mk引入此模块的方法如下：

```makefile
$(call import-module,CocosDenshion/android)
```

#### 2.3 模块描述变量

此类变量用来给Build System描述模块信息。在'include $(CLEAR_VARS)' 和 'include $(BUILD_XXXXX)'之间，必须定义此类变量。

- include $(CLEAR_VARS) 用来清空这些变量。
- include $(BUILD_XXXXX) 收集和使用这些变量。

##### 2.3.1 LOCAL_PATH

这个值用来给定当前目录，必须在Android.mk的开是位置定义之。

例如：

```makefile
LOCAL_PATH := $(call my-dir)  
```

LOCAL_PATH不会被include $(CLEAR_VARS)清理。

##### 2.3.2 LOCAL_MODULE

定义Modules名，在include $(BUILD_XXXXX)之前，必须定义这个变量，此变量必须唯一且不能有空格。通常由此变量名决定最终生成的目标文件名。

##### 2.3.3 LOCAL_MODULE_FILENAME

（可选）即允许用户重新定义最终生成的目标文件名。

```makefile
LOCAL_MODULE := foo-version-1   
LOCAL_MODULE_FILENAME := libfoo
```

##### 2.3.4 LOCAL_SRC_FILES

为Build Modules而提供的Source文件列表，不需要列出依赖文件。
==注意：文件相对于LOCAL_PATH存放，且可以提供相对路径。==

例如：

```makefile
LOCAL_SRC_FILES := foo.c \ 
                   toto/bar.c
```

##### 2.3.5 LOCAL_CPP_EXTENSION

（可选）指出C++扩展名。

```makefile
LOCAL_CPP_EXTENSION := .cxx
```

从NDK R7后，可以写多个：

```makefile
LOCAL_CPP_EXTENSION := .cxx .cpp .cc    
```

##### 2.3.6 LOCAL_CPP_FEATURES

（可选）用来指定C++ features。

```makefile
LOCAL_CPP_FEATURES := rtti  
LOCAL_CPP_FEATURES := exceptions
```

##### 2.3.7 LOCAL_C_INCLUDES

一个可选的path列表，相对于NDK ROOT目录，编译时将会把这些目录附上，主要为了头文件的引用。

```makefile
LOCAL_C_INCLUDES := sources/foo  
LOCAL_C_INCLUDES := $(LOCAL_PATH)/../foo
```

##### 2.3.8 LOCAL_CFLAGS

（可选）在编译C/C++ source 时添加如Flags，用来附加编译选项。

==注意：不要尝试在此处修改编译的优化选项和Debug等级，它会通过您Application.mk中的信息自动指定。==

1. -Wall：是打开警告开关。
2. -O：代表默认优化，可选：-O0不优化，-O1低级优化，-O2中级优化，-O3高级优化，-Os代码空间优化。
3. -g：是生成调试信息，生成的可执行文件具有和源代码关联的可调试的信息。
4. -fopenmp：OpenMp是由OpenMP Architecture Review Board牵头提出的，并已被广泛接受的，用于共享内存并行系统的多处理器程序设计的一套指导性的编译处理方案(Compiler Directive)。OpenMP支持的编程语言包括C语言、C++和Fortran；而支持OpenMp的编译器包括Sun Compiler，GNU Compiler和Intel Compiler等。OpenMp提供了对并行算法的高层的抽象描述，程序员通过在源代码中加入专用的pragma来指明自己的意图，由此编译器可以自动将程序进行并行化，并在必要之处加入同步互斥以及通信。当选择忽略这些pragma，或者编译器不支持OpenMp时，程序又可退化为通常的程序(一般为串行)，代码仍然可以正常运作，只是不能利用多线程来加速程序执行。
5. -D：增加全局宏定义（==常用==）
6. -ffast-math：浮点优化选项，极大地提高浮点运算速度。
7. -mfloat-abi=softfp 浮点运算

```makefile
LOCAL_CFLAGS += -DXXX # 相当于在所有源文件中增加一个宏定义'#define XXX'
```

##### 2.3.10 LOCAL_CPPFLAGS

C++ Source 编译时添加的C Flags，这些Flags将出现在LOCAL_CFLAGS flags 的后面。

##### 2.3.11 LOCAL_STATIC_LIBRARIES

要链接到本模块的静态库list，这仅仅对共享库模块才有意义。

Android.mk 1:

```makefile
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := mylib_static
LOCAL_SRC_FILES := src.c
include $(BUILD_STATIC_LIBRARY)
```

Android.mk 2:

```makefile
include $(CLEAR_VARS)
LOCAL_MODULE := mylib_shared
LOCAL_SRC_FILES := src2.c
LOCAL_STATIC_LIBRARIES := mylib_static
include $(BUILD_SHARED_LIBRARY)
```

要编译Android.mk 2，必须已经先编译mylib_static静态库，即Android.mk 1。

##### 2.3.12 LOCAL_SHARED_LIBRARIES

要链接到本模块的动态库，同上。

##### 2.3.13 LOCAL_WHOLE_STATIC_LIBRARIES

静态库全链接，不同于LOCAL_STATIC_LIBRARIES，类似于使用--whole-archive，LOCAL_WHOLE_STATIC_LIBRARIES在连接静态连接库的时候不会移除"daed code"，何谓dead code呢，就是调用者模块永远都不会用到的代码段和变量。

##### 2.3.14 LOCAL_LDLIBS

链接flags，链接的库不产生依赖关系，一般用于不需要重新编译的库，可以用它来添加系统库。

```makefile
LOCAL_LDLIBS += -lm –lz –lc -lcutils –lutils –llog …
```

##### 2.3.15 LOCAL_ALLOW_UNDEFINED_SYMBOLS

默认情况下，在试图编译一个共享库时，任何未定义的引用将导致一个“未定义的符号”错误。
然而，如果你因为某些原因，需要不启动这项检查，把这个变量设为'true'。注意相应的共享库可能在运行时加载失败。（这个一般尽量不要去设为true）

##### 2.3.16 LOCAL_ARM_MODE

缺省模式下，ARM目标代码被编译为thumb模式。每个指令16位。如果指定此变量为'arm'，则指令为32位。

```makefile
LOCAL_ARM_MODE := arm  
```

其实也可以指定某一个或者某几个文件的ARM指令模式。

##### 2.3.17 LOCAL_ARM_NEON

设置为true时，会讲浮点编译成neon指令。这会极大地加快浮点运算（前提是硬件支持）
只有targeting为'armeabi-v7a'时才可以。

##### 2.3.18 LOCAL_DISABLE_NO_EXECUTE

Android NDK r4版本开始支持这种"NX bit"的安全功能。默认是启用的，你也可以设置该变量的值为true来禁用它。但不推荐这么做。该功能不会修改ABI，只在ARMv6+CPU的设备内核上启用。

##### 2.3.19 LOCAL_EXPORT_CFLAGS

定义这个变量用来记录C/C++编译器标志集合，
并且会被添加到其他任何以LOCAL_STATIC_LIBRARIES和LOCAL_SHARED_LIBRARIES的模块的LOCAL_CFLAGS定义中。

==注意：此处NDK版本为NDK R7C。（不同NDK版本，ndk-build所产生的Makefile并不完全相同）==

[原文](https://www.jianshu.com/p/703ef39dff3f)