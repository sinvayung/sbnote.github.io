---
title: ★01.介绍
description: ★01.介绍
---

# ★01.介绍

# Java平台与宿主环境

- **Java平台** 是一个编程环境，包括一个 **Java虚拟机** 和一套 **Java API** 。
- **Java虚拟机** 可以使得 **Java应用程序** 不用考虑与 **宿主环境（操作系统）** 的兼容性问题，保证了 **Java应用程序** 与 **宿主环境（操作系统）** 的隔离。
- **Java应用程序** 使用 **Java** 编写，被编译为可以在 **Java虚拟机** 上运行的二进制格式，所以只要 **宿主环境（操作系统）** 能运行 **Java虚拟机** 。
- 原生应用使用 **C/C++** 这样的原生编程语言编写，编译成为 **宿主环境（操作系统）**相关的字节码。

# JNI的角色

- JNI 是一种双向接口，既允许 Java应用程序 \调用原生代码，同时也允许原生代码调用 Java代码。

  

  ![img](https://upload-images.jianshu.io/upload_images/4603989-7a5c269cd1955fe2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/571)

  JNI的角色

# 使用JNI的潜在风险

- 使用了 **JNI** 的 **Java应用程序** 便丢失了 **可移植性** 。
- **Java** 是类型安全的，但是 **C/C++** 则不是，一个原生方法的运行时错误，可能让整个程挂掉。

# 使用JNI的场景

- 若不选择JNI ，可以使用以下几种方式来允许 Java应用程序与其他语言完成的应用程序进行通信：
  1. 可以通过TCP/IP连接或者通过其他IPC通信机制与原生应用进行通信。
  2. 可以通过JDBC连接到一个传统的数据库上。
  3. 可以使用Java IDL API等分布式对象策略的优势。
- 上述几种方式主要利用了 **进程隔离** 甚至是 **设备隔离** 来避免了原生程序的错误传递到 **Java应用程序** 。
- 对于以下几种场景，Java应用程序和原生代码存在于相同进程空间是有必要的，这也是JNI的价值所在：
  1. 一个应用程序想使用一些 **Java API** 不支持文件操作，而通过另一个进程操作文件又是繁杂且低效的。
  2. 一个自身跨进程实现的应用可能导致不可接受的内存占用，尤其是当这些进程需要运行在同一台宿主机器上时候。
  3. 一个3D应用程序大多数时间都消耗在图形渲染上，你会想要将这部分渲染代码使用汇编语言实现来达到最好的性能。



# ★02.入门

# 简介

- 本节示例怎么使 **Java应用程序** 通过 **JNI** 调用 **C语言** 输出`Hello World!`。

# 流程

1. 创建一个`HelloWorld.java`文件并声明原生方法。
2. 使用 **javac** 编译`HelloWorld.java`，生成`HelloWorld.class`文件。
3. 使用 **javah** 生成C头文件`HelloWorld.h`，该头文件包含了原生函数实现的原型。
4. 新建文件`HelloWorld.c`并按照`HelloWorld.h`中声明的原生函数原型实现原生代码。
5. 将`HelloWorld.c`构建成为一个原生库，生成`HelloWorld.dll`或者`HelloWorld.so`。
6. 使用 **Java** 运行HelloWorld程序，`HelloWorld.class`和`HelloWorld.dll/so`会在运行时被加载。



![img](https://upload-images.jianshu.io/upload_images/4603989-95c0a1d11a561415.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/643)

JNI Hello World 示意图

# HelloWorld示例

## 1. 创建HelloWorld.java

### 代码

```
public class HelloWorld {
    static {
        // "HelloWorld" 表明载入HelloWorld.dll
        System.loadLibrary("HelloWorld");
    }

    public static void main(String[] args) {
        new HelloWorld().print();
    }

    private native void print();
}
```

### 解说

- 上述代码主要包含三个部分：
  1. 一个静态代码块，用来加载 **动态链接库** 。
  2. 一个主函数作为 **Java应用程序** 入口，并在主函数中调用`print`。
  3. 一个原生函数`print`的声明，由原生代码实现。
- 包含原生代码的 **动态链接库** 一定要提前加载。
- `print`函数声明中的`native`修饰符表示该函数是使用其他语言实现的。

## 2. 生成HelloWorld.class

- 编译产生`HelloWorld.class`。

## 3. 使用CLion创建C/C++项目

- 保证 **CLion** 使用的是 **MinGW-w64** 而不是  **MinGW-32** 。
- 设置`JAVAHOME`环境变量，指向 **jdk** 目录。
- 通过`CMakeList.txt`设置 **JNI** 包含目录。
- 通过`CMakeList.txt`设置构建完毕后自动复制 **DLL** 到 **Java** 项目目录下。
- `CMakeList.txt`文件参考，

```
cmake_minimum_required(VERSION 3.7)
project(JNI_c)

set(CMAKE_C_STANDARD 11)

# 相当于 SOURCE_FILES = "HelloWorld.h HelloWorld.c"
set(SOURCE_FILES HelloWorld.h HelloWorld.c)
add_library(JNI_c SHARED ${SOURCE_FILES})

include_directories($ENV{JAVAHOME}/include)
include_directories($ENV{JAVAHOME}/include/win32)

# 设置输出DLL的名字前缀
set_target_properties(JNI_c PROPERTIES PREFIX "")
# 设置输出DLL的名字，此处输出HelloWorld.dll
set_target_properties(JNI_c PROPERTIES OUTPUT_NAME "HelloWorld")

# 构建完后复制DLL到指定目录
add_custom_command(TARGET JNI_c POST_BUILD                     # JNI_c是项目名称
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE_DIR:JNI_c>/HelloWorld.dll"           # input dir
        "C:/ProgramProjects/Java/JNI")                         # output dir
```

## 4. 生成HelloWorld.h

### 1. 配置 IDEA 中生成头文件规则（已配置则跳过）

1. File -> Settings -> External Tools。
2. 点击“+” 按钮。
   1. **Name** : `生成头文件`。
   2. **Group** : `JNI`。
   3. **Options** : 全部勾选。
   4. **Show in** : 全部勾选。
   5. **Program** : `$JDKPath$\bin\javah.exe`。
   6. **Parameters** : `-jni -v -d $FileDir$ $FileClass$`。`$FileDir$`表示输出目录，将`$FileDir$`设置为 **CLion** 项目目录。
   7. **Working directory** : `$SourcepathEntry$`。
3. 点击确定。

### 2. 生成

1. 选择对应的java文件。
2. 右键 -> JNI -> Generate Header File。
3. 在`$FileDir$`对应的目录里生成了`HelloWorld.h`。

### 3. 解说HelloWorld.h文件

#### 代码

```
/*
 * Class:     HelloWorld
 * Method:    print
 * Signature: ()V
 */
JNIEXPORT void JNICALL Java_HelloWorld_print
  (JNIEnv * , jobject);
```

#### 解说

- 注释部分：
  - **Class** ：函数来自的那一个类的名字。
  - **Method** ：这个函数的名字。
  - **Signature**：这个函数的签名。
    - `()V`：函数的签名为`void ()`。
    - `(IFC)D`：这个函数的`double (int, float, char)`。
- 代码部分：
  - `void`：原方法的返回值。
  - `JNIEnv *`：一个`JNIEnv`接口指针。
  - `jobject`：`HelloWorld`对象本身，有点像 **C++** 中的`this`指针。

## 5. 实现HelloWorld.c

```
#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Class:     HelloWorld
 * Method:    print
 * Signature: ()V
 */
JNIEXPORT void JNICALL Java_HelloWorld_print(JNIEnv * env, jobject obj) {
    printf("Hello World!\n");
}

#ifdef __cplusplus
}
#endif
```

## 5. 生成动态链接库并运行

- 在 **Clion** 中构建项目，生成 **DLL** 到对应目录。
- 设置IDEA 中的 Run/Debug Configurations ：
  - 将 **VM Options** 设置为`-Djava.library.path=C:\ProgramProjects\Java\JNI\`
- 运行程序。





# ★03.一个简单的Native方法

# Prompt.java

```
public class Prompt {
    static {
        System.loadLibrary("Prompt");
    }

    public static void main(String[] args) {
        Prompt p = new Prompt();
        String input = p.getLine("Type a line: ");
        System.out.println("User typed: " + input);
    }

    private native String getLine(String prompt);
}
```

# Prompt.c

```
#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif
/*
 * Class:     Prompt
 * Method:    getLine
 * Signature: (Ljava/lang/String;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_Prompt_getLine(JNIEnv * env, jobject obj, jstring str) {
}

#ifdef __cplusplus
}
#endif
```

# 解说

- 原生函数总是比Java中声明的方法多两个参数。
- 第一个参数：`JNIEnv *`类型，是 **JNIEnv** 接口指针，指向一个地址，该地址包含了指向函数表的指针。
- 第二个参数：根据原生函数是否是静态函数而有所不同。
  1. 如果该原生函数不是 **静态函数** ，则是`jobject`，对应着调用该原生函数的 **Java**对象，有点像 **C++** 中的`this`指针。
  2. 如果该原生函数是 **静态函数** ，则是`jclass`，对应着调用该原生函数的 **Java**类。

# 类型映射

- `boolean` - `jboolean`
- `char` - `jchar`
- `short` - `jshort`
- `int` - `jint`
- `long` - `jlong`
- `float` - `jfloat`
- `double` - `jdouble`

# 其他

- 所有的 **JNI** 引用都是`jobject`类型。





# ★04.访问Strings

# 函数表

| JNI 函数                  | 描述                                                         | 加入版本     |
| ------------------------- | ------------------------------------------------------------ | ------------ |
| Get/ReleaseStringChars    | 获取或者释放一个Unicode格式的字符串，可能返回原始字符串的拷贝 | JDK1.1       |
| Get/ReleaseStringUTFChars | 获取或者释放一个UTF-8格式的字符串，可能返回原始字符串的拷贝  | JDK1.1       |
| GetStringLength           | 返回Unicode字符串的字符个数                                  | JDK1.1       |
| GetStringUTFLength        | 返回用于表示某个UTF-8字符串所需要的字节个数（不包括结束的0） | JDK1.1       |
| NewString                 | 创建一个java.lang.String对象，该对象与指定的Unicode字符串具有相同的字符序列 | JDK1.1       |
| NewStringUTF              | 创建一个java.lang.String对象，该对象与指定的UTF-8字符串具有相同的字符序列 | JDK1.1       |
| Get/ReleaseStringCritical | 获取或者释放一个Unicode格式的字符串的内容，可能返回原始字符串的拷贝，在Get/ReleaseStringCritical之间的代码必须不能阻塞 | Java2 SDK1.2 |
| Get/SetStringRegion       | 将一个字符串拷贝到预先开辟的空间，或者从一个预先开辟的空间复制字符串，字符使用Unicode编码 | Java2 SDK1.2 |
| Get/SetStringUTFRegion    | 将一个字符串拷贝到预先开辟的空间，或者从一个预先开辟的空间复制字符串，字符使用UTF-8编码 | Java2 SDK1.2 |

# jstring

- `jstring`不同于 **C语言** 的`char *`，不能像使用`char *`那样使用`jstring`。

# 简单示例

```
#include <jni.h>

#ifdef __cplusplus
extern "C" {
#endif
/*
 * Class:     Prompt
 * Method:    getLine
 * Signature: (Ljava/lang/String;)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_Prompt_getLine(JNIEnv * env, jobject obj, jstring prompt) {
    char buf[128];
    const char * str = (* env)->GetStringUTFChars(env, prompt, NULL);
    // 需要检查，可能因为内存分配失败抛出异常
    if (!str) {
        return NULL;
    }
    printf("%s", str);
    fflush(stdout);
    (* env)->ReleaseStringUTFChars(env, prompt, str);
    scanf("%s", buf);
    return (* env)->NewStringUTF(env, buf);
}

#ifdef __cplusplus
}
#endif
```

# 函数解说

## 转换成为Native Strings

- `GetStringUTFChars()`：用`jstring`类型对象生成`const char *`类型对象。 需要检查是否获取成功，因为可能会因为内存分配失败抛出异常。
- 无法预测`GetStringUTFChars()`的返回值是指向一个拷贝还是指向原来的`jstring`对象。
- `GetStringUTFChars()`的第三个参数是一个`jboolean *`类型，用于接收一个布尔值，若调用完`GetStringUTFChars()`后，此实参为`JNI_TRUE`，则代表着返回的指针指向原来`jstring`的拷贝，即可以修改；若为`JNI_FALSE`，则代表着返回的指针指向原来`jstring`的对象，即不可修改。可以传入`NULL`代表着自己不在乎。
- `GetStringUTFRegion()`：将字符串内容拷贝到一个预先申请好的缓冲区中，和`GetStringUTFChars()`不一样，不需要事后释放资源。
- `GetStringUTFRegion()`示例：

```
JNIEXPORT jstring JNICALL Java_Prompt_getLine(JNIEnv * env, jobject obj, jstring prompt) {
    char outbuf[128], inbuf[128];
    int len = (* env)->GetStringLength(env, prompt);
    (* env)->GetStringUTFRegion(env, prompt, 0, len, outbuf);
    printf("%s", outbuf);
    scanf("%s", inbuf);
    return (* env)->NewStringUTF(env, inbuf);
}
```

## 释放Native Strings资源

- `ReleaseStringUTFChars()`：当原生代码使用完了通过`GetStringUTFChars()`获取的 **UTF-8** 字符串，应当使用`ReleaseStringUTFChars()`释放它。
- `ReleaseStringUTFChars()`的调用失败将会导致内存泄露。

## 创建新的Strings

- `NewStringUTF()`：用`char *`类型对象生成`jstring`类型对象。
- `NewStringUTF()`可能会分配内存失败而抛出异常。

## 获取Strings字符个数

- `GetStringUTFLength()`：用于获取`jstring`字符串的字符个数。

# Unicode String相关的其他JNI函数

- `GetStringChars()`：类似`GetStringUTFChars()`。
- `ReleaseStringChars()`：类似`ReleaseStringUTFChars()`。
- `GetStringRegion()`：类似`GetStringUTFRegion()`。
- `GetStringLength()`：类似`GetStringUTFLength()`。
- `GetStringCritical()`：类似GetStringUTFRegion()
  - 相对比于`GetStringChars()`，倾向于返回指向原来的字符串而不是拷贝。
  - 同样需要检查是否获取成功。
  - 不能调用阻塞线程或可能阻塞线程的函数，比如获取输入，文件读写（可能被加锁导致阻塞）。
- `ReleaseStringCritical()`：释放通过`GetStringCritical()`获取的字符串资源。

# 其它

## 获取Strings字节个数

- 直接使用`strlen()`，传入`GetStringUTFChars()`的返回值。

## 异常

- 如果在 **C语言** 函数中，抛出异常，会在函数运行完毕时，在 **Java** 代码中传递抛出的异常。







# ★05.访问Arrays

# 基础类型数组 与 对象数组

```
int[] iarr;             // 基础类型数组
float[] farr;           // 基础类型数组
Object[] oarr;          // 对象数组
int[][] iarr2;          // 对象数组
```

# 基础类型数组

## 函数表

|            JNI函数            |                             描述                             |    加入版本    |
| :---------------------------: | :----------------------------------------------------------: | :------------: |
|     Get<Type>ArrayRegion      |               复制基础类型数组的内容到C缓冲区                |     JDK1.1     |
|     Set<Type>ArrayRegion      |            将C缓冲区的内容设置到基础类型数组中去             |     JDK1.1     |
|    Get<Type>ArrayElements     |  获取指向基础类型数组内容的指针，可能返回原始数组内容的拷贝  |     JDK1.1     |
|  Release<Type>ArrayElements   |  释放Get<Type>ArrayElements获取的指向基础类型数组内容的指针  |     JDK1.1     |
|        GetArrayLength         |                     返回数组中元素的个数                     |     JDK1.1     |
|        New<Type>Array         |                      创建指定长度的数组                      |     JDK1.1     |
|   GetPrimitiveArrayCritical   | 获取基础类型数组的内容，可能禁止垃圾回收，可能返回原始数组的一份拷贝 | Java 2 SDK 1.2 |
| ReleasePrimitiveArrayCritical |    释放GetPrimitiveArrayCritical获取的基础类型数组的内容     | Java 2 SDK 1.2 |

## 简单示例：`Get<Type>ArrayRegion()`

```
public class IntArray {
static {
        System.loadLibrary("IntArray");
    }

    public static void main(String[] args) {
        IntArray p = new IntArray();
        int[] arr = new int[10];
        for (int i = 0; i < 10; i++) {
            arr[i] = i;
        }
        int sum = p.sumArray(arr);
        System.out.println("sum = " + sum);
    }

    private native int sumArray(int[] arr);
}
JNIEXPORT jint JNICALL Java_IntArray_sumArray(JNIEnv * env, jobject obj, jintArray arr) {
    jint buf[10], sum = 0;

    // 获取数组长度
    const int length = (* env)->GetArrayLength(env, arr);

    // 获取数组到buf中
    (* env)->GetIntArrayRegion(env, arr, 0, length, buf);
    for (int i = 0; i < 10; i++) {
        sum += buf[i];
    }
    return sum;
}
```

## 简单示例：`Get<Type>ArrayElements()`

```
public class IntArray {
    static {
        System.loadLibrary("IntArray");
    }

    public static void main(String[] args) {
        IntArray p = new IntArray();
        int[] arr = new int[10];
        for (int i = 0; i < 10; i++) {
            arr[i] = i;
        }
        int sum = p.sumArray(arr);
        System.out.println("sum = " + sum);
    }

    private native int sumArray(int[] arr);
}
JNIEXPORT jint JNICALL Java_IntArray_sumArray(JNIEnv * env, jobject obj, jintArray arr) {
    jint sum = 0;

    // 返回数组指针，可能是本体也可能是拷贝。
    jint * carr = (* env)->GetIntArrayElements(env, arr, NULL);
    if (!carr) {
        return 0;
    }

    // 获取数组长度
    const int length = (* env)->GetArrayLength(env, arr);
    for (int i = 0; i < length; i++) {
        sum += carr[i];
    }

    // 释放数组资源
    (* env)->ReleaseIntArrayElements(env, arr, carr, 0);
    return sum;
}
```

## 函数解说

- `Get<Type>ArrayRegion()`：复制基础类型数组的内容到 **C缓冲区** 。
- `Set<Type>ArrayRegion()`：将 **C缓冲区** 的内容设置到基础类型数组中去。
- `Get<Type>ArrayElements()`：获取指向基础类型数组内容的指针，可能返回原始数组内容的拷贝。
- `Release<Type>ArrayElements()`：释放`Get<Type>ArrayElements()`获取的指向基础类型数组内容的指针。
- `GetArrayLength()`：返回数组中元素的个数。
- `New<Type>Array()`：创建指定长度的数组。
- `GetPrimitiveArrayCritical()`：获取基础类型数组的内容，可能禁止垃圾回收，可能返回原始数组的一份拷贝。
- `ReleasePrimitiveArrayCritical()`：释放`GetPrimitiveArrayCritical()`获取的基础类型数组的内容。

## 函数选择策略

- 关于以下三种函数的选择策略：

  - `Get<Type>ArrayRegion()`和`Set<Type>ArrayRegion()`：通常用于小的，固定长度的数组，也可以用于访问大数组中的一小部分。
  - `Get<Type>ArrayElements()`和`Release<Type>ArrayElements()`：通常用于大小未知，面向release1.1或release1.2但有阻塞的情况。
  - `GetPrimitiveArrayCritical()`和`ReleasePrimitiveArrayCritical()`：通常用于大小未知，代码没有阻塞，面向release1.2的情况

- 示意图：

  

  ![img](https://upload-images.jianshu.io/upload_images/4603989-5bf2a959e842f418.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/596)

# 对象数组

## 简单示例

```
public class ObjectArrayTest {
    static {
        System.loadLibrary("ObjectArrayTest");
    }

    public static void main(String[] args) {
        int[][] i2arr = initInt2DArray(3);
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; j++) {
                System.out.print(" " + i2arr[i][j]);
            }
            System.out.println();
        }
    }

    private static native int[][] initInt2DArray(int size);
}
JNIEXPORT jobjectArray JNICALL Java_ObjectArrayTest_initInt2DArray(JNIEnv * env, jclass cls, jint size) {
    // 获取一个"int[]"对应的类
    jclass intArrCls = (* env)->FindClass(env, "[I");
    if (!intArrCls) {
        return NULL;
    }

    // 创建一个元素为intArrCls类对象的对象数组result
    jobjectArray result = (* env)->NewObjectArray(env, size, intArrCls, NULL);
    if (!result) {
        return NULL;
    }

    for (int i = 0; i < size; ++i) {
        // 创建一个Int元素的基本类型数组iarr
        jintArray iarr = (* env)->NewIntArray(env, size);
        if (!iarr) {
            return NULL;
        }

        jint tmp[256];
        for (int j = 0; j < size; j++) {
            tmp[j] = i + j;
        }

        (* env)->SetIntArrayRegion(env, iarr, 0, size, tmp);
        // 设置对象数组result中索引i的元素为iarr
        (* env)->SetObjectArrayElement(env, result, i, iarr);
        // 释放资源，确保虚拟机不会因为需要持有大量像iarr这样的JNI引用而发生out-of-memory异常
        (* env)->DeleteLocalRef(env, iarr);
    }

    return result;
}
```

## 函数解说

- `FindClass()`：通过类描述符来获取`jclass`。
- `NewObjectArray()`：创建对象数组。
- `GetObjectArrayElement()`：获取对象数组元素。
- `SetObjectArrayElement()`：设置对象数组。





# ★06.访问属性

# 实例属性 与 静态属性

- **实例属性**：同一个类每一个对象都会拥有一份的属性。
- **静态属性**：同一个类的所有对象都共享的属性。

# 实例属性

## 简单示例

```
public class InstanceFieldAccess {
    static {
        System.loadLibrary("InstanceFieldAccess");
    }

    public static void main(String[] args) {
        InstanceFieldAccess c = new InstanceFieldAccess();
        c.s = "abc";
        c.accessField();
        System.out.println("In Java:");
        System.out.println("c.s = \"" + c.s + "\"");
    }

    private native void accessField();

    private String s;
}
JNIEXPORT void JNICALL Java_InstanceFieldAccess_accessField(JNIEnv * env, jobject obj) {
    // 使用jobject来获取其对应的jclass
    jclass cls = (* env)->GetObjectClass(env, obj);

    // 使用jclass、属性名、属性描述符来获取类中的属性ID
    jfieldID fid = (* env)->GetFieldID(env, cls, "s", "Ljava/lang/String;");
    if (!fid) {
        return;
    }

    // 使用属性ID和jobject来获取属性值
    jstring jstr = (* env)->GetObjectField(env, obj, fid);

    // 使用获取的属性值
    const char * str = (* env)->GetStringUTFChars(env, jstr, NULL);
    if (!str) {
        return;
    }
    printf("In C: \n");
    printf("c.s = \"%s\"\n", str);
    (* env)->ReleaseStringUTFChars(env, jstr, str);

    // 创建新的属性值
    jstring newJstr = (* env)->NewStringUTF(env, "123");
    if (!newJstr) {
        return;
    }

    // 将新的属性值赋值给属性
    (* env)->SetObjectField(env, obj, fid, newJstr);
}
```

## 示例解说

- 属性描述符

   

  ：描述属性类型的j符串。简单例子如下：

  - 使用`"F"`表示`float`。
  - 使用`"D"`表示`double`。
  - 使用`"Z"`表示`boolean`。
  - 使用`"[I"`表示`int[]`。
  - 使用`"Ljava/lang/String;"`表示`java.lang.String`。

- 创建查看属性描述符的便捷工具，可以避免手写属性描述符：

  1. File -> Settings -> External Tools。
  2. 点击“+”按钮。
     1. **Name** : `输出类描述符`。
     2. **Group** : `JNI`。
     3. **Options** : 全部勾选。
     4. **Show in** : 全部勾选。
     5. **Program** : `$JDKPath$\bin\javap.exe`。
     6. **Parameters** : `-s -p $FileClass$`。`-p`选项用于输出私有成员。
     7. **Working directory** : `$OutputPath$`。
  3. 点击确定。

- 示例步骤：

  1. 使用`jobject`获取其对应的`jclass`。
  2. 使用`jclass`、 **属性名** 和 **属性描述符** 来获取属性的`jfieldID`。
  3. 使用`jfieldID`和`jobject`来获取属性值。
  4. 使用`jobject`、`jfieldID`和 **新属性值** 来给属性赋值。

## 函数解说

- `GetObjectClass()`：用于获取`jobject`对应的`jclass`。
- `GetFieldID()`：用于获取 **实例属性** ID`jfieldID`。
- `Get<Type>Field()`：用于获取`jobject`中的属性。
- `Set<Type>Field()`：用于给`jobject`中的属性赋值。

# 静态属性

## 简单示例

```
public class StaticFieldAccess {
    static {
        System.loadLibrary("StaticFieldAccess");
    }

    public static void main(String args[]) {
        StaticFieldAccess c = new StaticFieldAccess();
        StaticFieldAccess.si = 100;
        c.accessField();
        System.out.println("In Java:");
        System.out.println("StaticFieldAccess.si = " + si);
    }

    private native void accessField();

    private static int si;
}
JNIEXPORT void JNICALL Java_StaticFieldAccess_accessField(JNIEnv * env, jobject obj) {
    // 使用jobject来获取其对应的jclass
    jclass cls = (* env)->GetObjectClass(env, obj);

    // 使用jclass、属性名、属性描述符来获取类中的属性ID
    jfieldID fid = (* env)->GetStaticFieldID(env, cls, "si", "I");
    if (!fid) {
        return;
    }

    // 使用属性ID和jclass来获取属性值
    jint si = (* env)->GetStaticIntField(env, cls, fid);

    // 使用获取的属性值
    printf("In C:\n");
    printf("StaticFieldAccess.si = %li\n", si);

    // 给属性设置新属性值
    (* env)->SetStaticIntField(env, cls, fid, 200);
}
```

## 示例解说

- 示例步骤：
  1. 使用`jobject`获取其对应的`jclass`。
  2. 使用`jclass`、 **属性名** 和 **属性描述符** 来获取属性的`jfieldID`。
  3. 使用`jfieldID`和`jclass`来获取属性值。
  4. 使用`jclass`、`jfieldID`和 **新属性值** 来给属性赋值。

## 函数解说

- `GetStaticFieldID()`：用于获取 **静态属性** ID`jfieldID`。
- `GetStatic<Type>Field()`：用于获取`jclass`中的属性。
- `SetStatic<Type>Field()`：用于给`jclass`中的属性赋值。





# ★07.调用方法

# 简介

- **原生代码** 中调用 **Java** 方法也被称为 **native回调** 。

# 访问普通方法

## 简单示例

```
public class InstanceMethodCall {
    static {
        System.loadLibrary("InstanceMethodCall");
    }

    public static void main(String[] args) {
        InstanceMethodCall c = new InstanceMethodCall();
        c.nativeMethod();
    }

    private native void nativeMethod();

    private void callback() {
        System.out.println("In Java");
    }
}
JNIEXPORT void JNICALL Java_InstanceMethodCall_nativeMethod(JNIEnv * env, jobject obj) {
    // 通过jobject获取jclass
    jclass cls = (* env)->GetObjectClass(env, obj);

    // 通过jclass获取jmethodID
    jmethodID mid = (* env)->GetMethodID(env, cls, "callback", "()V");
    if (!mid) {
        return;
    }
    printf("In C\n");
    // 通过jobject和jmethodID调用方法
    (* env)->CallVoidMethod(env, obj, mid);
}
```

## 示例解说

1. `GetObjectClass()`：通过`jobject`获取`jclass`。
2. `GetMethodID()`：通过`jclass`、 **方法名** 和 **方法描述符** 获取`jmethodID`。如果没有找到对应方法会抛出`NoSuchMethodError`。 **方法描述符** 的获取方法可以参考 **★06.访问属性** 。
3. `CallVoidMethod()`：通过`jobject`和`jmethodID`调用方法。`CallVoidMethod()`用于调用返回`void`类型的方法。

## 函数解说

- `GetObjectClass()`：用于获取`jclass`。
- `GetMethodID()`：用于获取`jmethodID`。
- `Call<Type>Method`：用于调用返回`<Type>`类型的方法。

# 访问静态方法

## 简单示例

```
public class StaticMethodCall {
    static {
        System.loadLibrary("StaticMethodCall");
    }

    public static void main(String[] args) {
        StaticMethodCall c = new StaticMethodCall();
        c.nativeMethod();
    }

    private static void callback() {
        System.out.println("In Java");
    }

    private native void nativeMethod();
}
JNIEXPORT void JNICALL Java_StaticMethodCall_nativeMethod(JNIEnv * env, jobject obj) {
    // 通过jobject获取jclass
    jclass cls = (* env)->GetObjectClass(env, obj);

    // 通过jclass、方法名和方法描述符来获取jmethodID
    jmethodID mid = (* env)->GetStaticMethodID(env, cls, "callback", "()V");
    if (!mid) {
        return;
    }
    printf("In C\n");
    // 通过jclass和jmethodID获取方法
    (* env)->CallStaticVoidMethod(env, cls, mid);
}
```

## 示例解说

1. `GetObjectClass()`：通过`jobject`获取`jclass`。
2. `GetMethodID()`：通过`jclass`、 **方法名** 和 **方法描述符** 获取`jmethodID`。如果没有找到对应方法会抛出`NoSuchMethodError`。 **方法描述符** 的获取方法可以参考 **★06.访问属性** 。
3. `CallStaticVoidMethod()`：通过`jobject`和`jmethodID`调用方法。`CallVoidMethod()`用于调用返回`void`类型的方法。

## 函数解说

- `GetObjectClass()`：用于获取`jclass`。
- `GetMethodID()`：用于获取`jmethodID`。
- `CallStatic<Type>Method`：用于调用返回`<Type>`类型的静态方法。

# 调用基类方法

- `CallNonvirtual<Type>Method()`：用于调用基类方法，相当于 **Java** 代码中的`super.fun()`。

# 调用构造函数

## 简单示例

```
jstring MyNewString(JNIEnv * env, jchar * chars, jint len) {
    // 通过类型描述符获取jclass
    jclass stringClass = (* env)->FindClass(env, "java/lang/String");
    if (!stringClass) {
        return 0;
    }
    // 通过jclass、"<init>"和方法描述符获取构造函数的jmethodID
    jmethodID cid = (* env)->GetMethodID(env, stringClass, "<init>", "([C)V");
    if (!cid) {
        return 0;
    }
    // 创建数组
    jcharArray elemArr = (* env)->NewCharArray(env, len);
    if (!elemArr) {
        return 0;
    }
    // 设置数组
    (* env)->SetCharArrayRegion(env, elemArr, 0, len, chars);

    // 通过jclass、构造函数jmethodID和构造函数参数来调用构造函数创建对象
    jstring result = (* env)->NewObject(env, stringClass, cid, elemArr);

    // 清理
    (* env)->DeleteLocalRef(env, elemArr);
    (* env)->DeleteLocalRef(env, stringClass);
    return result;
}
```

## 示例解说

1. `FindClass()`：通过 **类型描述符** 获取对应的`jclass`
2. `GetMethodID()`：通过`jclass`、`"<init>"`和 **方法描述符** 获取构造函数的`jmethodID`。
3. `NewObject()`：通过`jclass`、构造函数`jmethodID`和构造函数 **参数** 来调用构造函数创建对象。

## 函数解说

- `FindClass()`：通过 **类型描述符** 获取对应的`jclass`。
- `GetMethodID()`：通过`jclass`、`"<init>"`和 **方法描述符** 获取构造函数的`jmethodID`。
- `NewObject()`：通过`jclass`、构造函数`jmethodID`和构造函数 **参数** 来调用构造函数创建对象。

## 注意事项

- 我们可以通过`NewObject()`调用构造函数来构造一个`String`，但是 **JNI** 仍然内置`NewString()`，因为内置版本更高效。





# ★08.缓存属性和方法ID

# 简介

- 在获取一个 **属性/方法ID** 的时候需要基于名称或者 **属性/方法描述符** 的 **符号查找** ， **符号查找** 的代价相对来说是比较昂贵的（消耗时间和资源），优化主要思路的是计算 **属性/方法ID** 通过缓存以供后续使用。
- 有两种缓存方式，如有可能应该尽量使用后者： **用时缓存** 、 **类静态初始化器缓存**。

# 用时缓存

## 简单示例

```
JNIEXPORT void JNICALL Java_InstanceFieldAccess_accessField(JNIEnv * env, jobject obj) {
    // 静态局部变量以便于一次获取，以后就不必重新获取
    static jfieldID fid_s = NULL;

    jclass cls = (* env)->GetObjectClass(env, obj);

    // 只有从来没获取fid_s才会获取
    if (!fid_s) {
        fid_s = (* env)->GetFieldID(env, cls, "s", "Ljava/lang/String;");
        if (!fid_s) {
            return;
        }
    }

    jstring jstr = (* env)->GetObjectField(env, obj, fid_s);
    const char * str = (* env)->GetStringUTFChars(env, jstr, NULL);
    if (!str) {
        return;
    }
    printf("In C: \n");
    printf("c.s = \"%s\"\n", str);
    (* env)->ReleaseStringUTFChars(env, jstr, str);
    jstring newJstr = (* env)->NewStringUTF(env, "123");
    if (!newJstr) {
        return;
    }
    (* env)->SetObjectField(env, obj, fid_s, newJstr);
}
```

## 示例解说

- 示例中的属性ID`fid_s`使用了静态局部存储，用以缓存，重复使用时不再重新获取。

## 优缺点

- **优点** ：非侵入性的，即在对 **Java** 代码没有控制权的时候，仍然可以用 **用时缓存** ，而 **类静态初始化器缓存** 的方法则不可以。
- 缺点：
  - 在多线程的情况下，可能会出现`fid_s`被 **重复计算/缓存/检查** 的问题。在此处`fid_s`被 **重复计算/缓存** 除了有一部分性能开销以外，基本是无害的。
  - 当类被载出时，缓存的ID不再有效，需要获取，在使用 **用时缓存** 的方法时，是需要保证当原生代码仍然在用缓存ID时，类不会被载出或重新加载。

# 类静态初始化器缓存

## 简单示例

```
public class InstanceMethodCall {
    static {
        System.loadLibrary("InstanceMethodCall");
        // 在类静态初始化代码块中缓存ID
        initIDs();
    }

    public static void main(String args[]) {
        InstanceMethodCall c = new InstanceMethodCall();
        c.nativeMethod();
    }

    // 类静态函数，实现交给原生代码，用于缓存ID
    private static native void initIDs();

    private native void nativeMethod();

    private void callback() {
        System.out.println("In Java");
    }
}
// 创建全局变量，以便于ID可以在多个不同的原生函数中传递
jmethodID MID_InstanceMethodCall_callback;

JNIEXPORT void JNICALL Java_InstanceMethodCall_initIDs(JNIEnv * env, jclass cls) {
    // 获取所有需要缓存的ID到全局变量中
    MID_InstanceMethodCall_callback = (* env)->GetMethodID(env, cls, "callback", "()V");
}

JNIEXPORT void JNICALL Java_InstanceMethodCall_nativeMethod(JNIEnv * env, jobject obj) {
    printf("In C\n");
    // 使用缓存的ID
    (* env)->CallVoidMethod(env, obj, MID_InstanceMethodCall_callback);
}
```

## 示例解说

- 在 **Java** 代码中声明一个静态`native`函数`initIDs()`用于缓存ID。
- 在 **Java** 代码中 **类静态构造代码块** 中调用`initIDs()`。
- 在原生代码中实现`initIDs()`，缓存ID到全局变量。

## 优缺点

- **优点** ：不需要手动获取缓存ID，当类载入或重新加载时，ID会自动缓存。
- **缺点** ：侵入性，无法在对 **Java** 代码没有控制权的情况下使用。

# 两种方法的性能比较

## 概念

- **Java/native调用** ：原生代码调用 **Java** 函数。
- **native/Java调用** ： **Java** 代码调用原生函数。
- **Java/Java调用** ： **Java** 代码调用 **Java** 函数。

## Java/native调用

- Java/native调用可能慢于Java/Java调用，原因是：
  - 不得不执行额外的操作。
  - 原生代码调用 **Java** 函数难以内联。
- 经典的虚拟机执行 **Java/native调用** 会2-3倍慢于 **Java/Java调用** ，但是构建一个虚拟机使得二者的性能开销接近甚至相等也是可能的。

## native/Java调用

- 理论上 **native/Java调用** 相比 **Java/Java调用** 会慢2-3倍，但是 **native/Java调用**比较罕见。





# ★09.局部引用与全局引用

# 简介

- 通常不必关心内部对象释放内存问题，因为已经交由 **Java虚拟机** 负责。
- **JNI** 支持3中不透明引用： **局部引用** 、 **全局引用** 、 **弱全局引用** 。

# 局部引用

## 简介

- **局部引用** 可以由一系列 **JNI函数** 获取。
- **局部引用** 会在原生函数返回时被自动释放。
- 只能在创建了 **局部引用** 的线程使用此 **局部引用** ，不该使用全局变量存储 **局部引用**指望别的线程能使用此引用。
- 不要使用 **静态存储生命周期变量** （即全局变量，局部静态变量）存储 **局部引用** ，然后指望下次使用此静态变量时， **局部引用** 仍然有效。
- **局部引用** 可以通过`DeleteLocalRef()`手动释放。

## 手动释放局部引用

- 通常情况下不必手动释放局部引用 ，但是在以下情况则需要手动释放：
  - 创建了大量的 **局部引用** ，如数组元素等，可以每用完一个释放一个。
  - 这个 **局部引用** 是在 **效用函数** 中创建的。
  - 这个 **局部引用** 指向一个巨大的对象。
  - 原生函数永远都不会返回，比如一个永久循环。

## 管理局部引用

### 函数解说

- `EnsureLocalCapacity()`：用于确保有足够的空间给某个数量的 **局部引用** 。
- `PushLocalFrame() / PopLocalFrame()`：
  - 开始一段区域，在此区域创建的 **局部引用** 都会被记录，在随后调用`PopLocalFrame()`时会释放这段区域创建的所有 **局部引用** 。
  - `PushLocalFrame() / PopLocalFrame()`十分有效率，可以在进入 **效用函数** 时调用`PushLocalFrame()`，在`return`的地方调用`PopLocalFrame()`。若有多个`return`的时候，每个`return`处都需要调用`PopLocalFrame()`。
  - `PopLocalFrame()`的第二个参数十分有用，在碰见需要释放所有 **局部引用** 除了其中一个保留并返回时，可以将此引用传递`PopLocalFrame()`第二个参数。
- `NewLocalRef()`：用于在 **效用函数** 中返回一个 **局部引用** 。

### `EnsureLocalCapacity()`示例

```
// 开始获取局部引用前先确保有足够的空间
if (((* env)->EnsureLocalCapacity(env, len)) < 0) {
    // 内存不足
}
for (int i = 0; i < len; i++) {
    jstring jstr = (* env)->GetObjectArrayElement(env, arr, i);
}
```

### `PushLocalFrame() / PopLocalFrame()`示例

```
jobject f(JNIEnv * env, ...) {
    jobject result = NULL;
    // 开始一段区域，并保证有足够的空间
    if ((*env)->PushLocalFrame(env, 10) < 0) {
        return NULL;
    }
    // ...
    result = ...;
    if (...) {
        // 结束这段区域，区域中获取的局部引用全部释放，result通过传入传出得到了保留
        result = (* env)->PopLocalFrame(env, result);
        return result;
    }
    // 保证所有的return前都调用了PopLocalFrame
    result = (* env)->PopLocalFrame(env, result);
    return result;
}
```

### `NewLocalRef()`示例

```
jstring MyNewString(JNIEnv * env, jchar * chars, jint len) {
    static jstring result;
    if (wstrncmp("CommonString", chars, len) == 0) {
        static jstring cachedString = NULL;
        if (cachedString == NULL) {
            jstring cachedStringLocal = ...;
            cachedString = (* env)->NewGlobalRef(env, cachedStringLocal);
        }
        // 将全局引用cachedString转换为局部引用后返回
        return (* env)->NewLocalRef(env, cachedString);
    }
    return result;
}
```

# 全局引用

- 和 **局部引用** 不一样， **全局引用** 只需要一个 **JNI函数** 便能获取，即`NewGlobalRef()`。
- 可以使用 **全局引用** 在多个函数调用间或多个线程间共享。
- **全局引用** 不会被自动释放，需要手动使用`DeleteGlobalRef()`释放。

```
jstring MyNewString(JNIEnv * env, jchar * chars, jint len) {
    // 可以使用局部静态变量来存储全局引用
    static jclass stringClass = NULL;
    if (stringClass == NULL) {
        jclass localRefCls = (* env)->FindClass(env, "java/lang/String");
        if (localRefCls == NULL) {
            return NULL;
        }

        // 通过局部引用来获取全局引用
        stringClass = (* env)->NewGlobalRef(env, localRefCls);
        // 先释放局部引用，再检查是否成功获取全局引用
        // 因为无论是否成功，局部引用都不再有效
        (* env)->DeleteLocalRef(env, localRefCls);
        if (stringClass == NULL) {
            return NULL;
        }
    }
    // ...
}
```

# 弱全局引用

- **弱全局引用** 使用`NewWeakGlobalRef()`来获取。
- **弱全局引用** 和 **全局引用** 一样，可以在多个函数调用间或多个线程间共享。
- **弱全局引用** 可能会被垃圾回收器回收。
- **弱全局引用** 虽然可能会被自动释放，但仍然需要使用`DeleteWeakGlobalRef()`来手动释放。
- 像`java.lang.String`这样的系统类永远不会被垃圾回收器回收。

```
JNIEXPORT void JNICALL Java_mypkg_MyCls_f(JNIEnv * env, jobject self) {
    static jclass myCls2 = NULL;
    if (myCls2 == NULL) {
        jclass myCls2Local = (* env)->FindClass(env, "mypkg/MyCls2");
        if (myCls2Local == NULL) {
            return;
        }

        // 使用局部引用获取弱全局引用
        myCls2 = (* env)->NewWeakGlobalRef(env, myCls2Local);
        if (myCls2 == NULL) {
            return;
        }
    }
    // ...
}
```

# 比较引用

- 可以使用`IsSameObject()`来检查两个引用（局部、全局或弱全局）是否指向同一个对象。如果返回`JNI_TRUE`，则两个引用指向同一个对象。如果返回`JNI_FALSE`，则相反。
- 若引用的值为`NULL`，则此引用指向 **Java** 中的`null`对象。
- 对于 **局部引用** 和 **全局引用** 可以通过`(* env)->IsSameObject(env, obj, NULL)`来判断引用是否指向`null`对象。若返回`JNI_TRUE`则指向`null`对象。
- 对于 **弱全局引用** 可以通过`(* env)->IsSameObject(env, wobj, NULL)`来检查到更多。若返回`JNI_TRUE`，则表明引用要么指向`null`对象，要么被垃圾回收器回收了。无论哪一种，引用都不能再使用了。

# 管理引用的规则

- JNI代码中有三种类型的函数：
  1. **JNI函数** ： **JNI** 的 **API** 函数。
  2. **原生函数** ：实现 **Java** 代码中 **native方法声明** 的 **C** 函数。
  3. **效用函数** ： **C** 工具函数。
- 对于原生函数 ，应该注意：
  - 避免大量创建 **局部引用** 。
  - 避免不返回的 **原生函数** 创建了不必要的 **局部引用** 。
- 对于 效用函数，应该注意：
  - 尽量避免内存泄漏。
  - 如果此 **效用函数** 返回 **原始类型** ，应该释放所有的 **局部引用** 。
  - 如果此 **效用函数** 返回 **引用类型** ，应该释放除了要返回的 **引用类型** 以外所有的 **局部引用** 。
  - 不应该偶尔返回 **局部引用** ，偶尔返回 **全局引用** ，因为调用此 **效用函数** 的调用者需要知道返回的 **引用类型** ，以便管理这个引用。
  - 可以使用`NewLocalRef()`来保证 **效用函数** 返回的 **引用类型** 总是 **局部引用** 。

```
while (JNI_TRUE) {
    // GetInfoString是一个效用函数，infoString是由此效用函数创建的
    jstring infoString = GetInfoString(info);

    // 使用infoString

    // 使用完毕后，在此处需要根据infoString的引用类型（局部引用、全局引用或弱全局引用）来释放infoString。
}
```





# ★10.异常处理

# 简述

- 写 **JNI** 代码时，需要时刻考虑每一个 **JNI函数** 可能抛出的异常。
- 在原生代码中，一旦发生异常，需要马上处理。

# 简单示例

```
public class CatchThrow {
    static {
        System.loadLibrary("CatchThrow");
    }

    public static void main(String args[]) {
        CatchThrow c = new CatchThrow();
        try {
            c.doit();
        } catch (Exception e) {
            System.out.println("In Java:\n\t" + e);
        }
    }

    private native void doit() throws IllegalArgumentException;

    private void callback() throws NullPointerException {
        throw new NullPointerException("CatchThrow.callback");
    }
}
JNIEXPORT void JNICALL Java_CatchThrow_doit(JNIEnv * env, jobject obj) {
    jclass cls = (* env)->GetObjectClass(env, obj);
    jmethodID mid = (* env)->GetMethodID(env, cls, "callback", "()V");
    if (mid == NULL) {
        return;
    }

    // 注意此调用会抛出异常
    (* env)->CallVoidMethod(env, obj, mid);

    // 尝试获取已抛出的异常
    jthrowable exc = (* env)->ExceptionOccurred(env);

    // 通过此处的判断，检查是否真的抛出了异常
    if (exc) {
        // 输出异常描述
        (* env)->ExceptionDescribe(env);

        // 清除异常
        (* env)->ExceptionClear(env);

        // 创建新的异常
        jclass newExcCls = (* env)->FindClass(env, "java/lang/IllegalArgumentException");
        if (newExcCls == NULL) {
            return;
        }

        // 抛出新的异常取代旧的异常
        (* env)->ThrowNew(env, newExcCls, "thrown from C code");
    }
}
```

# 示例解说

- 示例演示了如何声明一个可能抛出异常的 **原生方法** 。
- 在原生代码中，通过`ThrowNew()`抛出异常时，不会马上中断执行流程。若在 **Java**代码中抛出异常则会马上中断执行流程，转到最近的`try/catch`块执行代码。

# 函数解说

- `ExceptionOccurred()`：若有异常，则返回一个`jthrowable`对象，否则返回`NULL`。
- `ExceptionCheck()`：若有异常，则返回`JNI_TRUE`，否则返回`JNI_FALSE`。
- `ExceptionDescribe()`：若有异常，输出异常描述，相当于 **Java** 代码中的`Exception.printStackTrace()`。
- `ExceptionClear()`：清除队列中的异常，后续代码不会在获取到。
- `ThrowNew()`：抛出异常。

# 异常检查

## 第一种

### 简介

- 大多数 **JNI函数** 会直接通过返回值（如返回`NULL`）来说明是否遇到了错误，同时也暗示了此线程的队列中有待处理的异常。

### 简单示例

```
public class Window {
    static native void initIDs();

    static {
        initIDs();
    }

    long handle;
    int length;
    int width;
}
jfieldID FID_Window_handle;
jfieldID FID_Window_length;
jfieldID FID_Window_width;

JNIEXPORT void JNICALL Java_Window_initIDs(JNIEnv * env, jclass classWindow) {
    // 即便可以确保Window类中有这些字段，也必须要检查，因为仍然可能会因为内存不足而失败
    FID_Window_handle = (* env)->GetFieldID(env, classWindow, "handle", "J");
    if (FID_Window_handle == NULL) {
        return;
    }

    FID_Window_length = (* env)->GetFieldID(env, classWindow, "length", "I");
    if (FID_Window_length == NULL) {
        return;
    }

    FID_Window_width = (* env)->GetFieldID(env, classWindow, "width", "I");
    // 此处没有检测的必要，无论成功与否都是直接return
}
```

## 第二种

### 简介

- 有些 **JNI函数** 的返回值无法表明错误是否发生，因为这类 **JNI函数** 的返回值可能另作他用，如`CallIntMethod()`，此时可以通过`ExceptionOccurred()`或`ExceptionCheck()`来检测。

### 简单示例

```
public class Fraction {
    public int floor() {
        return (int) Math.floor((double) over / under);
    }

    int over, under;
}
void Java_Fraction_floor(JNIEnv * env, jobject fraction) {
    // ...
    jint floor = (* env)->CallIntMethod(env, fraction, MID_Fraction_floor);

    // 检查是否有异常
    if ((* env)->ExceptionCheck(env)) {
        // 处理异常
        return;
    }
    // ...
}
```

# 异常处理

- 有两种处理异常的方法：
  1. 立即返回，让异常传递至 **Java** 代码。
  2. 使用`ExceptionClear()`清除异常，然后处理异常
- 在调用一些 **JNI函数** 前，检查、处理、清理异常很重要。
- 大部分 **JNI函数** 在队列中有待处理异常时，调用会导致一些无法预料的错误，另一小部分 **JNI函数** 之所以能在这种情况下调用是因为这些函数为了处理异常而设计的。
- 通常很有必要在发生异常的时候清理资源。

```
JNIEXPORT void JNICALL Java_pkg_Cls_f(JNIEnv * env, jclass cls, jstring jstr) {
    const jchar * cstr = (* env)->GetStringChars(env, jstr);
    if (c_str == NULL) {
        return;
    }

    // ...

    if (/* ... */) {
        // 发生异常，释放资源
        (* env)->ReleaseStringChars(env, jstr, cstr);
        return;
    }

    // 函数结束时，释放资源
    (* env)->ReleaseStringChars(env, jstr, cstr);
}
```

# 效用函数里的异常

- 对于 **效用函数** 里的异常，应该要确保异常能够传播到 **原生函数** 调用者中。
- 通常情况下， **效用函数** 应该提供一个特殊的返回值来表明异常在 **效用函数** 里发生了。
- 应该在 **效用函数** 的异常处理代码中，处理好 **局部引用** 。

# 相关工具函数

## 用于便捷抛出异常

```
// name是异常的类型描述符，msg是抛出异常时需要输出的信息
void JNU_ThrowByName(JNIEnv * env, const char * name, const char * msg) {
    // 此处若FindClass失败，会抛出NoClassDefFoundError异常
    jclass cls = (* env)->FindClass(env, name);
    if (cls != NULL) {
        (* env)->ThrowNew(env, cls, msg);
    }
    // 若cls是NULL，DeleteLocalRef不会执行任何操作
    (* env)->DeleteLocalRef(env, cls);
}
```

## 通用调用函数

### 代码

```
// 参数说明：
// hasException：用来接收异常是否抛出的信息，若非NULL，则代表着调用者关心是否有异常抛出
// obj：方法所属的对象
// name：方法名字
// descriptor：方法描述符
jvalue
JNU_CallMethodByName(JNIEnv * env, jboolean * hasException, jobject obj, const char * name, const char * descriptor,
                     ...) {
    va_list args;
    // 联合体
    jvalue result = NULL;
    if ((* env)->EnsureLocalCapacity(env, 2) == JNI_OK) {
        jclass clazz = (* env)->GetObjectClass(env, obj);
        jmethodID mid = (* env)->GetMethodID(env, clazz, name, descriptor);
        if (mid) {
            const char * p = descriptor;
            while (* p != ')') p++;
            p++;
            va_start(args, descriptor);
            switch (* p) {
                case 'V':
                    (* env)->CallVoidMethodV(env, obj, mid, args);
                    break;
                case '[':
                case 'L':
                    // result任意一个字段被初始化，都代表着有错误发生
                    result.l = (* env)->CallObjectMethodV(env, obj, mid, args);
                    break;
                case 'Z':
                    result.z = (* env)->CallBooleanMethodV(env, obj, mid, args);
                    break;
                case 'B':
                    result.b = (* env)->CallByteMethodV(env, obj, mid, args);
                    break;
                case 'C':
                    result.c = (* env)->CallCharMethodV(env, obj, mid, args);
                    break;
                case 'S':
                    result.s = (* env)->CallShortMethodV(env, obj, mid, args);
                    break;
                case 'I':
                    result.i = (* env)->CallIntMethodV(env, obj, mid, args);
                    break;
                case 'J':
                    result.j = (* env)->CallLongMethodV(env, obj, mid, args);
                    break;
                case 'F':
                    result.f = (* env)->CallFloatMethodV(env, obj, mid, args);
                    break;
                case 'D':
                    result.d = (* env)->CallDoubleMethodV(env, obj, mid, args);
                    break;
                default:
                    (* env)->FatalError(env, "illegal descriptor");
            }
            va_end(args);
        }
        (* env)->DeleteLocalRef(env, clazz);
    }
    // 若调用者关心是否有异常抛出，则检查是否有异常抛出
    if (hasException) {
        * hasException = (* env)->ExceptionCheck(env);
    }

//    // JDK release 1.1版本
//    if (hasException) {
//        jthrowable exc = (* env)->ExceptionOccurred(env);
//        * hasException = (jboolean) (exc != NULL);
//        (* env)->DeleteLocalRef(env, exc);
//    }

    return result;
}
```

### 使用例子

```
JNIEXPORT void JNICALL Java_InstanceMethodCall_nativeMethod(JNIEnv * env, jobject obj) {
    printf("In C\n");
    JNU_CallMethodByName(env, NULL, obj, "callback", "()V");
    // 这里之所以不检查错误是因为无论是否发生错误，都会直接return
}
```



https://www.jianshu.com/nb/14042835