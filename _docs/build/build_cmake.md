---
title: JNI开发之CMake使用指南
description: JNI开发之CMake使用指南
---

# JNI开发之CMake使用指南

![96](https://upload.jianshu.io/users/upload_avatars/3009951/4d30a00d55bf.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96)

 

[XuYanjun](https://www.jianshu.com/u/86708106f652)

 

关注

2018.08.31 18:18* 字数 1272 阅读 283评论 0喜欢 0

### 一.简介

> 1、在Android开发过程中，一些功能在Java代码层无法实现，需要借助底层的支持，例如硬件接入，热修复等，通过这些底层的代码都是友C或者C++进行编写的。此时如果需要用调用这些底层的库，就需要用到JNI技术。

> 2、通常情况下，JNI开发需要在C/CC++代码目录新建Android.mk文件，在对应module中的build.gradle中的defaultConfig 节点下配置ndk节点，然后配置相关信息，这种网上已经有很多博客都有介绍，这里不再赘述。本篇主要介绍CMake开发Android JNI技术。

------

### 二、CMake介绍

#### 2.1、CMake官方介绍

> [CMake](https://cmake.org/) is an open-source, cross-platform family of tools designed to build, test and package software. CMake is used to control the software compilation process using simple platform and compiler independent configuration files, and generate native makefiles and workspaces that can be used in the compiler environment of your choice.

**翻译成中文意思是：**

> CMake是一个开源的跨平台工具系列，旨在构建，测试和打包软件。CMake用于使用简单的平台和独立于编译器的配置文件来控制软件编译过程，并生成可在您选择的编译器环境中使用的本机makefile和工作空间。

#### 2.2、使用CMake的好处

> - **1.** 跨平台性
> - **2.** 可以批处理文件，这点对于JNI开发中涉及到非常多的.c/.cpp或者.a文件时简直不要太爽

------

### 三、Android中使用CMake进行JNI开发

下面我们从0开始进行一个JNI工程的开发，来说明CMake在Android中的使用流程。

#### 3.1 创建工程，添加C++支持

Android Studio中进行如下操作：**File--->New--->New Project**，出现如下界面：



![img](https://upload-images.jianshu.io/upload_images/3009951-75d6cadfb7d997ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/912)

添加C++支持



注意：要支持CMake，此时我们需要勾选 **Include C++ support**，然后点击Next--->Finish,完成工程的创建。
创建完成后的截图如下：



![img](https://upload-images.jianshu.io/upload_images/3009951-3f1522ef9a124d61.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/433)

自动生成后的project

这里我们需要关注的是生成的**CMakeLists.txt**文件，自动生成的文件内容如下：

```
# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html

# Sets the minimum version of CMake required to build the native library.

# 设置cmake最小版本
cmake_minimum_required(VERSION 3.4.1)

# Creates and names a library, sets it as either STATIC
# or SHARED, and provides the relative paths to its source code.
# You can define multiple libraries, and CMake builds them for you.
# Gradle automatically packages shared libraries with your APK.

# 配置so库信息
add_library( # Sets the name of the library.
             # 设置生成so库的文件名称，例如此处生成的so库文件名称应该为：libnative-lib.so
             native-lib

             # Sets the library as a shared library.
             # 设置生成的so库类型，类型只包含两种：
             # STATIC:静态库，为目标文件的归档文件，在链接其他目标的时候使用
             # SHARED:动态库，会被动态链接，在运行时被加载    
             SHARED

             # Provides a relative path to your source file(s).
             # 设置源文件的位置，可以是很多个源文件，都要添加进来
             src/main/cpp/native-lib.cpp )

# Searches for a specified prebuilt library and stores the path as a
# variable. Because CMake includes system libraries in the search path by
# default, you only need to specify the name of the public NDK library
# you want to add. CMake verifies that the library exists before
# completing its build.

# 从系统里查找依赖库，可添加多个
find_library( # Sets the name of the path variable.
  # 例如查找系统中的log库liblog.so
  log-lib

  # Specifies the name of the NDK library that
  # you want CMake to locate.
  # liblog.so库指定的名称即为log,如同上面指定生成的libnative-lib.so库名称为native-lib一样
  log )

# Specifies libraries CMake should link to your target library. You
# can link multiple libraries, such as libraries you define in this
# build script, prebuilt third-party libraries, or system libraries.

# 配置目标库的链接，即相互依赖关系
target_link_libraries( # Specifies the target library.
   # 目标库（最终生成的库）
   native-lib

   # Links the target library to the log library
   # included in the NDK.
   # 依赖于log库，一般情况下，如果依赖的是系统中的库，需要加 ${} 进行引用，
   # 如果是第三方库，可以直接引用库名，例如：
   # 引用第三方库libthird.a，引用时直接写成third;注意，引用时，每一行只能引用一个库
   ${log-lib} )
```

以上就是关于CMakeLists.txt文件的说明，在生成的工程中，我们对于的module的build.gradle文件内部也会跟正常情况下的不大一样，可参看[Google官方说明](https://developer.android.google.cn/ndk/guides/cmake)，具体我们来分析一下（省略部分无关部分）：

```
android {
    compileSdkVersion 27
    defaultConfig {
        ...

        //cmake配置
        externalNativeBuild {
            cmake {
                //设置cpp标志，例如支持C++11，就将-std=c++11加上
                cppFlags "-std=c++11"
                //按需求可以配置一些参数,关于参数的说明可参看下面的表格
                arguments '-DANDROID_PLATFORM=android-23',
                    '-DANDROID_TOOLCHAIN=clang', '-DANDROID_STL=gnustl_static'

                //设置最终生成so文件的版本，按需求添加或删减
                abiFilters 'arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64'
            }
        }

    }
    
    ...

    //设置cmake配置文件的位置路径，也就是我们上面说的那个CMakeLists.txt文件
    externalNativeBuild {
        cmake {
            path "CMakeLists.txt"
        }
    }

    ...
}
```

> - **关于arguments参数说明如下：**

| 变量名                               | 参数                                                         | 说明                                                         |
| :----------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| ANDROID_TOOLCHAIN                    | **clang （默认）** **gcc （废弃）**                          | 指定CMake应该使用的编译器工具链                              |
| ANDROID_PLATFORM                     | NDK支持的API级别与Android版本可参考[Android NDK Native API](https://developer.android.google.cn/ndk/guides/stable_apis) | 指定目标Android平台的名称,例如android-23                     |
| ANDROID_STL                          | 默认情况下，CMake使用gnustl_static,具体可参考[C++支持](https://developer.android.google.cn/ndk/guides/cpp-support#hr) | 指定应使用的STL CMake                                        |
| ANDROID_PIE                          | **ON**  **OFF**                                              | 指定是否使用与位置无关的可执行文件                           |
| ANDROID_CPP_FEATURES                 | 默认该变量为空 **rtti** （表示您的代码使用RTTI） **exceptions**（表示您的代码使用C ++异常） | 指定CMake在编译本机库时需要使用的某些C ++特性，例如RTTI（运行时类型信息）和C ++异常。 |
| ANDROID_ALLOW_UNDEFINED_SYMBOLS      | **TRUE**  **FALSE**                                          | 指定如果CMake在构建本机库时遇到未定义的引用，是否抛出未定义的符号错误。要禁用这些类型的错误，请将此变量设置为 TRUE。 |
| ANDROID_ARM_MODE                     | **arm**  **thumb(默认)**                                     | 指定是否以arm 或thumb模式生成ARM目标二进制文件               |
| ANDROID_ARM_NEON                     | **TRUE**  **FALSE(默认)**                                    | 指定CMake是否应构建具有NEON支持的本机库                      |
| ANDROID_DISABLE_NO_EXECUTE           | **TRUE**  **FALSE(默认)**                                    | 指定是否启用NX位或No eXecute安全功能。要禁用此功能，传递 TRUE |
| ANDROID_DISABLE_RELRO                | **TRUE**  **FALSE(默认)**                                    | 指定是否启用只读重定位                                       |
| ANDROID_DISABLE_FORMAT_STRING_CHECKS | **TRUE**  **FALSE(默认)**                                    | 指定是否使用格式字符串保护编译源代码。启用后，如果在printf-style函数中使用非常量格式字符串，则编译器将引发错误 |

在build.gradle文件中配置好了cmake相关配置之后，我们再回过头看第一张图，工程生成的文件中包含一个cpp文件夹，文件夹中包含有一个native-cpp.lib文件，通常情况下编写JNI代码就在改cpp文件中进行编写，下面我们来具体编写一个JNI代码。

------

#### 3.2 编写Java代码

JNI开发中Java中的大概步骤如下：

> - **Step 1:** 创建Java类，引用想要执行的本地so文件
> - **Step 2:** 创建Java native方法，用于链接so库中对应的cpp方法
> - **Step 3:** 使用native方法，执行相关业务操作
> - 接下来按照步骤一一说明

创建一个makeTest类，将最终要引用的 **libnative-lib.so** 文件引用进来，具体如下：

```
public class CmakeTest {

    //step1:创建Java类，引用想要执行的本地so文件
    static {
        System.loadLibrary("native-lib");
    }

    //step 2:创建Java native方法，用于链接so库中对应的cpp方法
    public native int addFunc(int a, int b);
}
```

#### 3.3 编写JNI代码部分

在上面我们创建好了Java的native方法之后，我们需要在与之对应的lib的源文件中（也就是native-lib.cpp文件）添加对应的方法，关于编写JNI代码，需要注意以下几点：

> - 1、返回类型要与Java本地方法返回类型一致
>
> - 2、方法命名规则要与Java本地方法对应的包名位置一致
>
>   **注意：**此时说到的位置一致，只针对常规写法，如果采用动态加载的方式编写，忽略此条

下面我们开始编写JNI部分代码：

```
#include <jni.h>

extern "C"
{
    JNIEXPORT jint JNICALL
    Java_com_study_cmaketest_CmakeTest_addFunc(JNIEnv *env, jobject obj, jint a, jint b) {
        return a + b;
    }
}
```

上述代码说明：

> - 1、返回类型，JNI中jint对应Java中的int（JNI类型与Java类型关系，会在下一篇中进行讲述。）
> - 2、JNI方法Java_com_study_cmaketest_CmakeTest_addFunc表示该方法指定为Java中的com.study.cmaketest包下的CmakeTest类中的addFunc方法，如下图：



![img](https://upload-images.jianshu.io/upload_images/3009951-192db99da771b565.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/846)

本地方法文件结构

至此，我们一个简单的JNI代码就完成了，接下来测试JNI代码是否正确，创建一个测试的Activity,调用Java中对应的native方法来调用JNI部分的代码进行求和计算：

```
public class MainActivity extends Activity {
    private TextView mTvTest;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mTvTest = findViewById(R.id.tv_test);

        CmakeTest cmakeTest = new CmakeTest();
        //调用native方法来执行求和计算
        int result = cmakeTest.addFunc(2, 3);
        mTvTest.setText("计算结果为：" + result);
    }
}
```

运行结果：



![img](https://upload-images.jianshu.io/upload_images/3009951-178456049d5753ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/270)

运行结果

运行结果正确，说明我们使用CMake进行JNI开发完全没问题。

------

### 四、总结

使用CMake进行JNI开发，相对于小的JNI工程感觉不到其优点，如果对于大型的JNI工程，就会体现到其中的优点，总体上进行CMake开发步骤如下：



![img](https://upload-images.jianshu.io/upload_images/3009951-e575c6d4f201ff4a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/418)

CMake开发流程



https://www.jianshu.com/p/712942cbe3c1

