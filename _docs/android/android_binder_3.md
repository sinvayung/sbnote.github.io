## 理解Android Binder机制3/3：Java层

 Posted on Mar 15, 2017

[ AndroidAnatomy](http://qiangbo.space/category/#AndroidAnatomy) [ Android](http://qiangbo.space/tags/#Android) [ Binder](http://qiangbo.space/tags/#Binder) [ AIDL](http://qiangbo.space/tags/#AIDL)

------

本文是Android Binder机制解析的第三篇，也是最后一篇文章。本文会讲解Binder Framework Java部分的逻辑。

Binder机制分析的前面两篇文章，请移步这里：

[理解Android Binder机制1/3：驱动篇](http://qiangbo.space/2017-01-15/AndroidAnatomy_Binder_Driver/)

[理解Android Binder机制2/3：C++层)：驱动篇](http://qiangbo.space/2017-02-12/AndroidAnatomy_Binder_CPP/)

下文所讲内容的相关源码，在AOSP源码树中的路径如下：

```
// Binder Framework JNI /frameworks/base/core/jni/android_util_Binder.h /frameworks/base/core/jni/android_util_Binder.cpp /frameworks/base/core/jni/android_os_Parcel.h /frameworks/base/core/jni/android_os_Parcel.cpp // Binder Framework Java接口 /frameworks/base/core/java/android/os/Binder.java /frameworks/base/core/java/android/os/IBinder.java /frameworks/base/core/java/android/os/IInterface.java /frameworks/base/core/java/android/os/Parcel.java
```

# 主要结构

Android应用程序使用Java语言开发，Binder框架自然也少不了在Java层提供接口。

前文中我们看到，Binder机制在C++层已经有了完整的实现。因此Java层完全不用重复实现，而是通过JNI衔接了C++层以复用其实现。

下图描述了Binder Framework Java层到C++层的衔接关系。

![img](assets/android_binder_3/Binder_JNI.png)

这里对图中Java层和JNI层的几个类做一下说明( 关于C++层的讲解请看[这里](http://qiangbo.space/2017-02-12/AndroidAnatomy_Binder_CPP/) )：

| 名称              | 类型      | 说明                                                         |
| ----------------- | --------- | ------------------------------------------------------------ |
| IInterface        | interface | 供Java层Binder服务接口继承的接口                             |
| IBinder           | interface | Java层的IBinder类，提供了transact方法来调用远程服务          |
| Binder            | class     | 实现了IBinder接口，封装了JNI的实现。Java层Binder服务的基类   |
| BinderProxy       | class     | 实现了IBinder接口，封装了JNI的实现。提供transact方法调用远程服务 |
| JavaBBinderHolder | class     | 内部存储了JavaBBinder                                        |
| JavaBBinder       | class     | 将C++端的onTransact调用传递到Java端                          |
| Parcel            | class     | Java层的数据包装器，见C++层的Parcel类分析                    |

这里的IInterface，IBinder和C++层的两个类是同名的。这个同名并不是巧合：它们不仅仅同名，它们所起的作用，以及其中包含的接口都是几乎一样的，区别仅仅在于一个是C++层，一个是Java层而已。

除了IInterface，IBinder之外，这里Binder与BinderProxy类也是与C++的类对应的，下面列出了Java层和C++层类的对应关系：

| C++        | Java层      |
| ---------- | ----------- |
| IInterface | IInterface  |
| IBinder    | IBinder     |
| BBinder    | Binder      |
| BpProxy    | BinderProxy |
| Parcel     | Parcel      |

# JNI的衔接

JNI全称是Java Native Interface，这个是由Java虚拟机提供的机制。这个机制使得native代码可以和Java代码互相通讯。简单来说就是：我们可以在C/C++端调用Java代码，也可以在Java端调用C/C++代码。

关于JNI的详细说明，可以参见Oracle的官方文档：[Java Native Interface](http://docs.oracle.com/javase/8/docs/technotes/guides/jni/) ，这里不多说明。

实际上，在Android中很多的服务或者机制都是在C/C++层实现的，想要将这些实现复用到Java层，就必须通过JNI进行衔接。AOSP源码中，/frameworks/base/core/jni/ 目录下的源码就是专门用来对接Framework层的JNI实现的。

看一下Binder.java的实现就会发现，这里面有不少的方法都是用`native`关键字修饰的，并且没有方法实现体，这些方法其实都是在C++中实现的：

```
public static final native int getCallingPid(); public static final native int getCallingUid(); public static final native long clearCallingIdentity(); public static final native void restoreCallingIdentity(long token); public static final native void setThreadStrictModePolicy(int policyMask); public static final native int getThreadStrictModePolicy(); public static final native void flushPendingCommands(); public static final native void joinThreadPool();
```

在android_util_Binder.cpp文件中的下面这段代码，设定了Java方法与C++方法的对应关系：

```
static const JNINativeMethod gBinderMethods[] = {     { "getCallingPid", "()I", (void*)android_os_Binder_getCallingPid },     { "getCallingUid", "()I", (void*)android_os_Binder_getCallingUid },     { "clearCallingIdentity", "()J", (void*)android_os_Binder_clearCallingIdentity },     { "restoreCallingIdentity", "(J)V", (void*)android_os_Binder_restoreCallingIdentity },     { "setThreadStrictModePolicy", "(I)V", (void*)android_os_Binder_setThreadStrictModePolicy },     { "getThreadStrictModePolicy", "()I", (void*)android_os_Binder_getThreadStrictModePolicy },     { "flushPendingCommands", "()V", (void*)android_os_Binder_flushPendingCommands },     { "init", "()V", (void*)android_os_Binder_init },     { "destroy", "()V", (void*)android_os_Binder_destroy },     { "blockUntilThreadAvailable", "()V", (void*)android_os_Binder_blockUntilThreadAvailable } };
```

这种对应关系意味着：当Binder.java中的`getCallingPid`方法被调用的时候，真正的实现其实是`android_os_Binder_getCallingPid`，当`getCallingUid`方法被调用的时候，真正的实现其实是`android_os_Binder_getCallingUid`，其他类同。

然后我们再看一下`android_os_Binder_getCallingPid`方法的实现就会发现，这里其实就是对接到了libbinder中了：

```
static jint android_os_Binder_getCallingPid(JNIEnv* env, jobject clazz) {     return IPCThreadState::self()->getCallingPid(); }
```

这里看到了Java端的代码是如何调用的libbinder中的C++方法的。那么，相反的方向是如何调用的呢？最关键的，libbinder中的`BBinder::onTransact`是如何能够调用到Java中的`Binder::onTransact`的呢？

这段逻辑就是android_util_Binder.cpp中`JavaBBinder::onTransact`中处理的了。JavaBBinder是BBinder子类，其类结构如下：

![img](assets/android_binder_3/JavaBBinder.png)

`JavaBBinder::onTransact`关键代码如下：

```
virtual status_t onTransact(    uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags = 0) {    JNIEnv* env = javavm_to_jnienv(mVM);    IPCThreadState* thread_state = IPCThreadState::self();    const int32_t strict_policy_before = thread_state->getStrictModePolicy();    jboolean res = env->CallBooleanMethod(mObject, gBinderOffsets.mExecTransact,        code, reinterpret_cast<jlong>(&data), reinterpret_cast<jlong>(reply), flags);    ... }
```

请注意这段代码中的这一行：

```
jboolean res = env->CallBooleanMethod(mObject, gBinderOffsets.mExecTransact,   code, reinterpret_cast<jlong>(&data), reinterpret_cast<jlong>(reply), flags);
```

这一行代码其实是在调用mObject上offset为mExecTransact的方法。这里的几个参数说明如下：

- mObject 指向了Java端的Binder对象
- gBinderOffsets.mExecTransact 指向了Binder类的execTransact方法
- data 调用execTransact方法的参数
- code, data, reply, flags都是传递给调用方法execTransact的参数

而`JNIEnv.CallBooleanMethod`这个方法是由虚拟机实现的。即：虚拟机会提供native方法来调用一个Java Object上的方法（关于Android上的Java虚拟机，今后我们会专门讲解）。

这样，就在C++层的`JavaBBinder::onTransact`中调用了Java层`Binder::execTransact`方法。而在`Binder::execTransact`方法中，又调用了自身的onTransact方法，由此保证整个过程串联了起来：

```
private boolean execTransact(int code, long dataObj, long replyObj,        int flags) {    Parcel data = Parcel.obtain(dataObj);    Parcel reply = Parcel.obtain(replyObj);    boolean res;    try {        res = onTransact(code, data, reply, flags);    } catch (RemoteException|RuntimeException e) {        if (LOG_RUNTIME_EXCEPTION) {            Log.w(TAG, "Caught a RuntimeException from the binder stub implementation.", e);        }        if ((flags & FLAG_ONEWAY) != 0) {            if (e instanceof RemoteException) {                Log.w(TAG, "Binder call failed.", e);            } else {                Log.w(TAG, "Caught a RuntimeException from the binder stub implementation.", e);            }        } else {            reply.setDataPosition(0);            reply.writeException(e);        }        res = true;    } catch (OutOfMemoryError e) {        RuntimeException re = new RuntimeException("Out of memory", e);        reply.setDataPosition(0);        reply.writeException(re);        res = true;    }    checkParcel(this, code, reply, "Unreasonably large binder reply buffer");    reply.recycle();    data.recycle();    StrictMode.clearGatheredViolations();    return res; }
```

# Java Binder服务举例

和C++层一样，这里我们还是通过一个具体的实例来看一下Java层的Binder服务是如何实现的。

下图是ActivityManager实现的类图:

![img](assets/android_binder_3/Binder_ActivityManager.png)

下面是上图中几个类的说明：

| 类名                   | 说明                   |
| ---------------------- | ---------------------- |
| IActivityManager       | Binder服务的公共接口   |
| ActivityManagerProxy   | 供客户端调用的远程接口 |
| ActivityManagerNative  | Binder服务实现的基类   |
| ActivityManagerService | Binder服务的真正实现   |

看过Binder C++层实现之后，对于这个结构应该也是很容易理解的，组织结构和C++层服务的实现是一模一样的。

对于Android应用程序的开发者来说，我们不会直接接触到上图中的几个类，而是使用`android.app.ActivityManager`中的接口。

这里我们就来看一下，`android.app.ActivityManager`中的接口与上图的实现是什么关系。我们选取其中的一个方法来看一下：

```
public void getMemoryInfo(MemoryInfo outInfo) {    try {        ActivityManagerNative.getDefault().getMemoryInfo(outInfo);    } catch (RemoteException e) {        throw e.rethrowFromSystemServer();    } }
```

这个方法的实现调用了`ActivityManagerNative.getDefault()`中的方法，因此我们在来看一下`ActivityManagerNative.getDefault()`返回到到底是什么。

```
static public IActivityManager getDefault() {    return gDefault.get(); } private static final Singleton<IActivityManager> gDefault = new Singleton<IActivityManager>() {    protected IActivityManager create() {        IBinder b = ServiceManager.getService("activity");        if (false) {            Log.v("ActivityManager", "default service binder = " + b);        }        IActivityManager am = asInterface(b);        if (false) {            Log.v("ActivityManager", "default service = " + am);        }        return am;    } };
```

这段代码中我们看到，这里其实是先通过`IBinder b = ServiceManager.getService("activity");` 获取ActivityManager的Binder对象（“activity”是ActivityManagerService的Binder服务标识），接着我们再来看一下`asInterface(b)`的实现：

```
static public IActivityManager asInterface(IBinder obj) {    if (obj == null) {        return null;    }    IActivityManager in =        (IActivityManager)obj.queryLocalInterface(descriptor);    if (in != null) {        return in;    }    return new ActivityManagerProxy(obj); }
```

这里应该是比较明白了：首先通过`queryLocalInterface`确定有没有本地Binder，如果有的话直接返回，否则创建一个`ActivityManagerProxy`对象。很显然，假设在ActivityManagerService所在的进程调用这个方法，那么`queryLocalInterface`将直接返回本地Binder，而假设在其他进程中调用，这个方法将返回空，由此导致其他调用获取到的对象其实就是`ActivityManagerProxy`。而在拿到`ActivityManagerProxy`对象之后在调用其方法所走的路线我想读者应该也能明白了：那就是通过Binder驱动跨进程调用ActivityManagerService中的方法。

这里的`asInterface`方法的实现会让我们觉得似曾相识。是的，因为这里的实现方式和C++层的实现是一样的模式。

# Java层的ServiceManager

源码路径：

```
frameworks/base/core/java/android/os/IServiceManager.java frameworks/base/core/java/android/os/ServiceManager.java frameworks/base/core/java/android/os/ServiceManagerNative.java frameworks/base/core/java/com/android/internal/os/BinderInternal.java frameworks/base/core/jni/android_util_Binder.cpp
```

有Java端的Binder服务，自然也少不了Java端的ServiceManager。我们先看一下Java端的ServiceManager的结构：

![img](assets/android_binder_3/ServiceManager_Java.png)

通过这个类图我们看到，Java层的ServiceManager和C++层的接口是一样的。

然后我们再选取`addService`方法看一下实现：

```
public static void addService(String name, IBinder service, boolean allowIsolated) {    try {        getIServiceManager().addService(name, service, allowIsolated);    } catch (RemoteException e) {        Log.e(TAG, "error in addService", e);    } }         private static IServiceManager getIServiceManager() {    if (sServiceManager != null) {        return sServiceManager;    }    // Find the service manager    sServiceManager = ServiceManagerNative.asInterface(BinderInternal.getContextObject());    return sServiceManager; }
```

很显然，这段代码中，最关键就是下面这个调用：

```
ServiceManagerNative.asInterface(BinderInternal.getContextObject());
```

然后我们需要再看一下BinderInternal.getContextObject和ServiceManagerNative.asInterface两个方法。

BinderInternal.getContextObject是一个JNI方法，其实现代码在android_util_Binder.cpp中：

```
static jobject android_os_BinderInternal_getContextObject(JNIEnv* env, jobject clazz) {     sp<IBinder> b = ProcessState::self()->getContextObject(NULL);     return javaObjectForIBinder(env, b); }
```

而ServiceManagerNative.asInterface的实现和其他的Binder服务是一样的套路：

```
static public IServiceManager asInterface(IBinder obj) {    if (obj == null) {        return null;    }    IServiceManager in =        (IServiceManager)obj.queryLocalInterface(descriptor);    if (in != null) {        return in;    }        return new ServiceManagerProxy(obj); }
```

先通过`queryLocalInterface`查看能不能获得本地Binder，如果无法获取，则创建并返回ServiceManagerProxy对象。

而ServiceManagerProxy自然也是和其他Binder Proxy一样的实现套路：

```
public void addService(String name, IBinder service, boolean allowIsolated)        throws RemoteException {    Parcel data = Parcel.obtain();    Parcel reply = Parcel.obtain();    data.writeInterfaceToken(IServiceManager.descriptor);    data.writeString(name);    data.writeStrongBinder(service);    data.writeInt(allowIsolated ? 1 : 0);    mRemote.transact(ADD_SERVICE_TRANSACTION, data, reply, 0);    reply.recycle();    data.recycle(); }
```

有了上文的讲解，这段代码应该都是比较容易理解的了。

# 关于AIDL

作为Binder机制的最后一个部分内容，我们来讲解一下开发者经常使用的AIDL机制是怎么回事。

AIDL全称是Android Interface Definition Language，它是Android SDK提供的一种机制。借助这个机制，应用可以提供跨进程的服务供其他应用使用。AIDL的详细说明可以参见官方开发文档：https://developer.android.com/guide/components/aidl.html 。

这里，我们就以官方文档上的例子看来一下AIDL与Binder框架的关系。

开发一个基于AIDL的Service需要三个步骤：

1. 定义一个.aidl文件
2. 实现接口
3. 暴露接口给客户端使用

aidl文件使用Java语言的语法来定义，每个.aidl文件只能包含一个interface，并且要包含interface的所有方法声明。

默认情况下，AIDL支持的数据类型包括：

- 基本数据类型（即int，long，char，boolean等）
- String
- CharSequence
- List（List的元素类型必须是AIDL支持的）
- Map（Map中的元素必须是AIDL支持的）

对于AIDL中的接口，可以包含0个或多个参数，可以返回void或一个值。所有非基本类型的参数必须包含一个描述是数据流向的标签，可能的取值是：`in`，`out`或者`inout`。

下面是一个aidl文件的示例：

```
// IRemoteService.aidl package com.example.android; // Declare any non-default types here with import statements /** Example service interface */ interface IRemoteService {     /** Request the process ID of this service, to do evil things with it. */     int getPid();     /** Demonstrates some basic types that you can use as parameters      * and return values in AIDL.      */     void basicTypes(int anInt, long aLong, boolean aBoolean, float aFloat,             double aDouble, String aString); }
```

这个文件中包含了两个接口 ：

- getPid 一个无参的接口，返回值类型为int
- basicTypes，包含了几个基本类型作为参数的接口，无返回值

对于包含.aidl文件的工程，Android IDE（以前是Eclipse，现在是Android Studio）在编译项目的时候，会为aidl文件生成对应的Java文件。

针对上面这个aidl文件生成的java文件中包含的结构如下图所示：

![img](assets/android_binder_3/aidl_java.png)

在这个生成的Java文件中，包括了：

- 一个名称为IRemoteService的interface，该interface继承自android.os.IInterface并且包含了我们在aidl文件中声明的接口方法
- IRemoteService中包含了一个名称为Stub的静态内部类，这个类是一个抽象类，它继承自android.os.Binder并且实现了IRemoteService接口。这个类中包含了一个`onTransact`方法
- Stub内部又包含了一个名称为Proxy的静态内部类，Proxy类同样实现了IRemoteService接口

仔细看一下Stub类和Proxy两个中包含的方法，是不是觉得很熟悉？是的，这里和前面介绍的服务实现是一样的模式。这里我们列一下各层类的对应关系：

| C++   | Java层    | AIDL            |
| ----- | --------- | --------------- |
| BpXXX | XXXProxy  | IXXX.Stub.Proxy |
| BnXXX | XXXNative | IXXX.Stub       |

为了整个结构的完整性，最后我们还是来看一下生成的Stub和Proxy类中的实现逻辑。

Stub是提供给开发者实现业务的父类，而Proxy的实现了对外提供的接口。Stub和Proxy两个类都有一个`asBinder`的方法。

Stub类中的asBinder实现就是返回自身对象：

```
@Override public android.os.IBinder asBinder() { return this; }
```

而Proxy中asBinder的实现是返回构造函数中获取的mRemote对象，相关代码如下：

```
private android.os.IBinder mRemote; Proxy(android.os.IBinder remote) { mRemote = remote; } @Override public android.os.IBinder asBinder() { return mRemote; }
```

而这里的mRemote对象其实就是远程服务在当前进程的标识。

上文我们说了，Stub类是用来提供给开发者实现业务逻辑的父类，开发者者继承自Stub然后完成自己的业务逻辑实现，例如这样：

```
private final IRemoteService.Stub mBinder = new IRemoteService.Stub() {    public int getPid(){        return Process.myPid();    }    public void basicTypes(int anInt, long aLong, boolean aBoolean,        float aFloat, double aDouble, String aString) {        // Does something    } };
```

而这个Proxy类，就是用来给调用者使用的对外接口。我们可以看一下Proxy中的接口到底是如何实现的：

Proxy中`getPid`方法实现如下所示：

```
@Override public int getPid() throws android.os.RemoteException { android.os.Parcel _data = android.os.Parcel.obtain(); android.os.Parcel _reply = android.os.Parcel.obtain(); int _result; try { _data.writeInterfaceToken(DESCRIPTOR); mRemote.transact(Stub.TRANSACTION_getPid, _data, _reply, 0); _reply.readException(); _result = _reply.readInt(); } finally { _reply.recycle(); _data.recycle(); } return _result; }
```

这里就是通过Parcel对象以及transact调用对应远程服务的接口。而在Stub类中，生成的onTransact方法对应的处理了这里的请求：

```
@Override public boolean onTransact(int code, android.os.Parcel data, android.os.Parcel reply, int flags) throws android.os.RemoteException { switch (code) { case INTERFACE_TRANSACTION: { reply.writeString(DESCRIPTOR); return true; } case TRANSACTION_getPid: { data.enforceInterface(DESCRIPTOR); int _result = this.getPid(); reply.writeNoException(); reply.writeInt(_result); return true; } case TRANSACTION_basicTypes: { data.enforceInterface(DESCRIPTOR); int _arg0; _arg0 = data.readInt(); long _arg1; _arg1 = data.readLong(); boolean _arg2; _arg2 = (0 != data.readInt()); float _arg3; _arg3 = data.readFloat(); double _arg4; _arg4 = data.readDouble(); java.lang.String _arg5; _arg5 = data.readString(); this.basicTypes(_arg0, _arg1, _arg2, _arg3, _arg4, _arg5); reply.writeNoException(); return true; } } return super.onTransact(code, data, reply, flags); }
```

`onTransact`所要做的就是：

1. 根据code区分请求的是哪个接口
2. 通过data来获取请求的参数
3. 调用由子类实现的抽象方法

有了前文的讲解，对于这部分内容应当不难理解了。

到这里，我们终于讲解完Binder了。

恭喜你，已经掌握了Android系统最复杂的模块，的其中之一了 ：）

– 以上 –

# 参考资料和推荐读物

- [Android Binder](https://www.nds.rub.de/media/attachments/files/2012/03/binder.pdf)
- [Android Interface Definition Language](https://developer.android.com/guide/components/aidl.html)
- [Android Bander设计与实现 - 设计篇](http://blog.csdn.net/universus/article/details/6211589)
- [Binder系列—开篇](http://gityuan.com/2015/10/31/binder-prepare/)
- [彻底理解Android Binder通信架构](http://gityuan.com/2016/09/04/binder-start-service/)
- [binder驱动——-之内存映射篇](http://blog.csdn.net/xiaojsj111/article/details/31422175)
- [Android Binder机制一 Binder的设计和框架](http://wangkuiwu.github.io/2014/09/01/Binder-Introduce/)
- [Android Binder 分析——内存管理](http://light3moon.com/2015/01/28/Android%20Binder%20%E5%88%86%E6%9E%90%E2%80%94%E2%80%94%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86/)

------

如果你喜欢我写的文章，说不定我写的书： 

《深入剖析Android新特性》

也会对你有帮助。