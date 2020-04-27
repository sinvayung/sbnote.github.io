---
title: 理解Android Binder机制2/3：C++层
description: 理解Android Binder机制2/3：C++层
---

## 理解Android Binder机制2/3：C++层

 Posted on Feb 12, 2017

[ AndroidAnatomy](http://qiangbo.space/category/#AndroidAnatomy) [ Android](http://qiangbo.space/tags/#Android) [ Binder](http://qiangbo.space/tags/#Binder) [ libbinder](http://qiangbo.space/tags/#libbinder)

------

本文是Android Binder机制解析的第二篇文章，会讲解Binder Framework的C++部分逻辑。

Binder机制分析的第一篇文章，请移步这里：[理解Android Binder机制1/3：驱动篇](http://qiangbo.space/2017-01-15/AndroidAnatomy_Binder_Driver/)

# 前言

Framework是一个中间层，它对接了底层实现，封装了复杂的内部逻辑，并提供供外部使用的接口。Framework层是应用程序开发的基础。

Binder Framework层分为C++和Java两个部分，为了达到功能的复用，中间通过JNI进行衔接。

Binder Framework的C++部分，头文件位于这个路径：/frameworks/native/include/binder/，实现位于这个路径：/frameworks/native/libs/binder/ 。Binder库最终会编译成一个动态链接库：`libbinder.so`，供其他进程链接使用。

为了便于说明，下文中我们将Binder Framework 的C++部分称之为libbinder。

# 主要结构

libbinder中，将实现分为Proxy和Native两端。Proxy对应了上文提到的Client端，是服务对外提供的接口。而Native是服务实现的一端，对应了上文提到的Server端。类名中带有小写字母p的（例如BpInterface），就是指Proxy端。类名带有小写字母n的（例如BnInterface），就是指Native端。

Proxy代表了调用方，通常与服务的实现不在同一个进程，因此下文中，我们也称Proxy端为“远程”端。Native端是服务实现的自身，因此下文中，我们也称Native端为”本地“端。

这里，我们先对libbinder中的主要类做一个简要说明，了解一下它们的关系，然后再详细的讲解。

| 类名           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| BpRefBase      | RefBase的子类，提供remote方法获取远程Binder                  |
| IInterface     | Binder服务接口的基类，Binder服务通常需要同时提供本地接口和远程接口 |
| BpInterface    | 远程接口的基类，远程接口是供客户端调用的接口集               |
| BnInterface    | 本地接口的基类，本地接口是需要服务中真正实现的接口集         |
| IBiner         | Binder对象的基类，BBinder和BpBinder都是这个类的子类          |
| BpBinder       | 远程Binder，这个类提供transact方法来发送请求，BpXXX实现中会用到 |
| BBinder        | 本地Binder，服务实现方的基类，提供了onTransact接口来接收请求 |
| ProcessState   | 代表了使用Binder的进程                                       |
| IPCThreadState | 代表了使用Binder的线程，这个类中封装了与Binder驱动通信的逻辑 |
| Parcel         | 在Binder上传递的数据的包装器                                 |

下图描述了这些类之间的关系：

另外说明一下，Binder服务的实现类（图中紫色部分）通常都会遵守下面的命名规则：

- 服务的接口使用I字母作为前缀
- 远程接口使用Bp作为前缀
- 本地接口使用Bn作为前缀

![img](assets/android_binder_2/binder_middleware-20190210002634902.png)

看了上面这些介绍，你可能还是不太容易理解。不过不要紧，下面我们会逐步拆分讲解这些内容。

在这幅图中，浅黄色部分的结构是最难理解的，因此我们先从它们着手。

我们先来看看IBinder这个类。这个类描述了所有在Binder上传递的对象，它既是Binder本地对象BBinder的父类，也是Binder远程对象BpBinder的父类。这个类中的主要方法说明如下：

| 方法名                 | 说明                                                   |
| ---------------------- | ------------------------------------------------------ |
| localBinder            | 获取本地Binder对象                                     |
| remoteBinder           | 获取远程Binder对象                                     |
| transact               | 进行一次Binder操作                                     |
| queryLocalInterface    | 尝试获取本地Binder，如何失败返回NULL                   |
| getInterfaceDescriptor | 获取Binder的服务接口描述，其实就是Binder服务的唯一标识 |
| isBinderAlive          | 查询Binder服务是否还活着                               |
| pingBinder             | 发送PING_TRANSACTION给Binder服务                       |

BpBinder的实例代表了远程Binder，这个类的对象将被客户端调用。其中`handle`方法会返回指向Binder服务实现者的句柄，这个类最重要就是提供了`transact`方法，这个方法会将远程调用的参数封装好发送的Binder驱动。

由于每个Binder服务通常都会提供多个服务接口，而这个方法中的`uint32_t code`参数就是用来对服务接口进行编号区分的。**Binder服务的每个接口都需要指定一个唯一的code，这个code要在Proxy和Native端配对好**。当客户端将请求发送到服务端的时候，服务端根据这个code（onTransact方法中）来区分调用哪个接口方法。

BBinder的实例代表了本地Binder，它描述了服务的提供方，所有Binder服务的实现者都要继承这个类（的子类），在继承类中，最重要的就是实现`onTransact`方法，因为这个方法是所有请求的入口。因此，这个方法是和BpBinder中的`transact`方法对应的，这个方法同样也有一个`uint32_t code`参数，在这个方法的实现中，由服务提供者通过code对请求的接口进行区分，然后调用具体实现服务的方法。

IBinder中定义了`uint32_t code`允许的范围：

```
FIRST_CALL_TRANSACTION  = 0x00000001, LAST_CALL_TRANSACTION   = 0x00ffffff,
```

Binder服务要保证自己提供的每个服务接口有一个唯一的code，例如某个Binder服务可以将：add接口code设为1，minus接口code设为2，multiple接口code设为3，divide接口code设为4，等等。

讲完了IBinder，BpBinder和BBinder三个类，我们再来看看BpReBase，IInterface，BpInterface和BnInterface。

每个Binder服务都是为了某个功能而实现的，因此其本身会定义一套接口集（通常是C++的一个类）来描述自己提供的所有功能。而Binder服务既有自身实现服务的类，也要有给客户端进程调用的类。为了便于开发，这两中类里面的服务接口应当是一致的，例如：假设服务实现方提供了一个接口为`add(int a, int b)`的服务方法，那么其远程接口中也应当有一个`add(int a, int b)`方法。因此为了实现方便，本地实现类和远程接口类需要有一个公共的描述服务接口的基类（即上图中的IXXXService）来继承。而这个基类通常是IInterface的子类，IInterface的定义如下：

```
class IInterface : public virtual RefBase { public:             IInterface();             static sp<IBinder>  asBinder(const IInterface*);             static sp<IBinder>  asBinder(const sp<IInterface>&); protected:     virtual                     ~IInterface();     virtual IBinder*            onAsBinder() = 0; };
```

之所以要继承自IInterface类是因为这个类中定义了`onAsBinder`让子类实现。`onAsBinder`在本地对象的实现类中返回的是本地对象，在远程对象的实现类中返回的是远程对象。`onAsBinder`方法被两个静态方法`asBinder`方法调用。有了这些接口之后，在代码中便可以直接通过`IXXX::asBinder`方法获取到不用区分本地还是远程的IBinder对象。这个在跨进程传递Binder对象的时候有很大的作用（因为不用区分具体细节，只要直接调用和传递就好）。

下面，我们来看一下BpInterface和BnInterface的定义：

```
template<typename INTERFACE> class BnInterface : public INTERFACE, public BBinder { public:     virtual sp<IInterface>      queryLocalInterface(const String16& _descriptor);     virtual const String16&     getInterfaceDescriptor() const; protected:     virtual IBinder*            onAsBinder(); }; // ----------------------------------------------------------------------  template<typename INTERFACE> class BpInterface : public INTERFACE, public BpRefBase { public:                                 BpInterface(const sp<IBinder>& remote); protected:     virtual IBinder*            onAsBinder(); };
```

这两个类都是模板类，它们在继承自INTERFACE的基础上各自继承了另外一个类。这里的INTERFACE便是我们Binder服务接口的基类。另外，BnInterface继承了BBinder类，由此可以通过复写`onTransact`方法来提供实现。BpInterface继承了BpRefBase，通过这个类的`remote`方法可以获取到指向服务实现方的句柄。在客户端接口的实现类中，每个接口在组装好参数之后，都会调用`remote()->transact`来发送请求，而这里其实就是调用的BpBinder的transact方法，这样请求便通过Binder到达了服务实现方的onTransact中。这个过程如下图所示：

![img](assets/android_binder_2/BpBinder_BBinder-20190210002634785.png)

基于Binder框架开发的服务，除了满足上文提到的类名规则之外，还需要遵守其他一些共同的规约：

- 为了进行服务的区分，每个Binder服务需要指定一个唯一的标识，这个标识通过`getInterfaceDescriptor`返回，类型是一个字符串。通常，Binder服务会在类中定义`static const android::String16 descriptor;`这样一个常量来描述这个标识符，然后在`getInterfaceDescriptor`方法中返回这个常量。
- 为了便于调用者获取到调用接口，服务接口的公共基类需要提供一个`android::sp<IXXX> asInterface`方法来返回基类对象指针。

由于上面提到的这两点对于所有Binder服务的实现逻辑都是类似的。为了简化开发者的重复工作，在libbinder中，定义了两个宏来简化这些重复工作，它们是：

```
#define DECLARE_META_INTERFACE(INTERFACE)                            \     static const android::String16 descriptor;                       \     static android::sp<I##INTERFACE> asInterface(                    \             const android::sp<android::IBinder>& obj);               \     virtual const android::String16& getInterfaceDescriptor() const; \     I##INTERFACE();                                                  \     virtual ~I##INTERFACE();                                         \ #define IMPLEMENT_META_INTERFACE(INTERFACE, NAME)                    \     const android::String16 I##INTERFACE::descriptor(NAME);          \     const android::String16&                                         \             I##INTERFACE::getInterfaceDescriptor() const {           \         return I##INTERFACE::descriptor;                             \     }                                                                \     android::sp<I##INTERFACE> I##INTERFACE::asInterface(             \             const android::sp<android::IBinder>& obj)                \     {                                                                \         android::sp<I##INTERFACE> intr;                              \         if (obj != NULL) {                                           \             intr = static_cast<I##INTERFACE*>(                       \                 obj->queryLocalInterface(                            \                         I##INTERFACE::descriptor).get());            \             if (intr == NULL) {                                      \                 intr = new Bp##INTERFACE(obj);                       \             }                                                        \         }                                                            \         return intr;                                                 \     }                                                                \     I##INTERFACE::I##INTERFACE() { }                                 \     I##INTERFACE::~I##INTERFACE() { }                                \
```

有了这两个宏之后，开发者只要在接口基类（IXXX）头文件中，使用`DECLARE_META_INTERFACE`宏便完成了需要的组件的声明。然后在cpp文件中使用`IMPLEMENT_META_INTERFACE`便完成了这些组件的实现。

# Binder的初始化

在讲解Binder驱动的时候我们就提到：任何使用Binder机制的进程都必须要对`/dev/binder`设备进行`open`以及`mmap`之后才能使用，这部分逻辑是所有使用Binder机制进程共同的。对于这种共同逻辑的封装便是Framework层的职责之一。libbinder中，ProcessState类封装了这个逻辑，相关代码见下文。

这里是ProcessState构造函数，在这个函数中，初始化mDriverFD的时候调用了`open_driver`方法打开binder设备，然后又在函数体中，通过mmap进行内存映射。

```
ProcessState::ProcessState()     : mDriverFD(open_driver())     , mVMStart(MAP_FAILED)     , mThreadCountLock(PTHREAD_MUTEX_INITIALIZER)     , mThreadCountDecrement(PTHREAD_COND_INITIALIZER)     , mExecutingThreadsCount(0)     , mMaxThreads(DEFAULT_MAX_BINDER_THREADS)     , mStarvationStartTimeMs(0)     , mManagesContexts(false)     , mBinderContextCheckFunc(NULL)     , mBinderContextUserData(NULL)     , mThreadPoolStarted(false)     , mThreadPoolSeq(1) {     if (mDriverFD >= 0) {         mVMStart = mmap(0, BINDER_VM_SIZE, PROT_READ, MAP_PRIVATE | MAP_NORESERVE, mDriverFD, 0);         if (mVMStart == MAP_FAILED) {             // *sigh*             ALOGE("Using /dev/binder failed: unable to mmap transaction memory.\n");             close(mDriverFD);             mDriverFD = -1;         }     }     LOG_ALWAYS_FATAL_IF(mDriverFD < 0, "Binder driver could not be opened.  Terminating."); }
```

`open_driver`的函数实现如下所示。在这个函数中完成了三个工作：

- 首先通过`open`系统调用打开了`dev/binder`设备
- 然后通过ioctl获取Binder实现的版本号，并检查是否匹配
- 最后通过ioctl设置进程支持的最大线程数量

关于这部分逻辑背后的处理，在讲解Binder驱动的时候，我们已经讲解过了。

```
static int open_driver() {     int fd = open("/dev/binder", O_RDWR | O_CLOEXEC);     if (fd >= 0) {         int vers = 0;         status_t result = ioctl(fd, BINDER_VERSION, &vers);         if (result == -1) {             ALOGE("Binder ioctl to obtain version failed: %s", strerror(errno));             close(fd);             fd = -1;         }         if (result != 0 || vers != BINDER_CURRENT_PROTOCOL_VERSION) {             ALOGE("Binder driver protocol does not match user space protocol!");             close(fd);             fd = -1;         }         size_t maxThreads = DEFAULT_MAX_BINDER_THREADS;         result = ioctl(fd, BINDER_SET_MAX_THREADS, &maxThreads);         if (result == -1) {             ALOGE("Binder ioctl to set max threads failed: %s", strerror(errno));         }     } else {         ALOGW("Opening '/dev/binder' failed: %s\n", strerror(errno));     }     return fd; }
```

`ProcessState`是一个Singleton（单例）类型的类，在一个进程中，只会存在一个实例。通过`ProcessState::self()`接口获取这个实例。一旦获取这个实例，便会执行其构造函数，由此完成了对于Binder设备的初始化工作。

# 关于Binder传递数据的大小限制

由于Binder的数据需要跨进程传递，并且还需要在内核上开辟空间，因此允许在Binder上传递的数据并不是无无限大的。mmap中指定的大小便是对数据传递的大小限制：

```
#define BINDER_VM_SIZE ((1*1024*1024) - (4096 *2)) // 1M - 8k  mVMStart = mmap(0, BINDER_VM_SIZE, PROT_READ, MAP_PRIVATE | MAP_NORESERVE, mDriverFD, 0);
```

这里我们看到，在进行mmap的时候，指定了最大size为BINDER_VM_SIZE，即 1M - 8k的大小。 因此我们在开发过程中，一次Binder调用的数据总和不能超过这个大小。

对于这个区域的大小，我们也可以在设备上进行确认。这里我们还之前提到的system_server为例。上面我们讲解了通过procfs来获取映射的内存地址，除此之外，我们也可以通过showmap命令，来确定这块区域的大小，相关命令如下：

```
angler:/ # ps  | grep system_server                                             system    1889  526   2353404 135968 SyS_epoll_ 72972eeaf4 S system_server angler:/ # showmap 1889 | grep "/dev/binder"                                        1016        4        4        0        0        4        0        0    1 /dev/binder
```

这里可以看到，这块区域的大小正是 1M - 8K = 1016k。

Tips: *通过showmap命令可以看到进程的详细内存占用情况。在实际的开发过程中，当我们要对某个进程做内存占用分析的时候，这个命令是相当有用的。建议读者尝试通过showmap命令查看system_server或其他感兴趣进程的完整map，看看这些进程都依赖了哪些库或者模块，以及内存占用情况是怎样的。*

# 与驱动的通信

上文提到`ProcessState`是一个单例类，一个进程只有一个实例。而负责与Binder驱动通信的`IPCThreadState`也是一个单例类。但这个类不是一个进程只有一个实例，而是一个线程有一个实例。

`IPCThreadState`负责了与驱动通信的细节处理。这个类中的关键几个方法说明如下：

| 方法                 | 说明                                            |
| -------------------- | ----------------------------------------------- |
| transact             | 公开接口。供Proxy发送数据到驱动，并读取返回结果 |
| sendReply            | 供Server端写回请求的返回结果                    |
| waitForResponse      | 发送请求后等待响应结果                          |
| talkWithDriver       | 通过ioctl BINDER_WRITE_READ来与驱动通信         |
| writeTransactionData | 写入一次事务的数据                              |
| executeCommand       | 处理binder_driver_return_protocol协议命令       |
| freeBuffer           | 通过BC_FREE_BUFFER命令释放Buffer                |

`BpBinder::transact`方法在发送请求的时候，其实就是直接调用了`IPCThreadState`对应的方法来发送请求到Binder驱动的，相关代码如下：

```
status_t BpBinder::transact(     uint32_t code, const Parcel& data, Parcel* reply, uint32_t flags) {     if (mAlive) {         status_t status = IPCThreadState::self()->transact(             mHandle, code, data, reply, flags);         if (status == DEAD_OBJECT) mAlive = 0;         return status;     }     return DEAD_OBJECT; }
```

而`IPCThreadState::transact`方法主要逻辑如下：

```
status_t IPCThreadState::transact(int32_t handle,                                   uint32_t code, const Parcel& data,                                   Parcel* reply, uint32_t flags) {     status_t err = data.errorCheck();     flags |= TF_ACCEPT_FDS;     if (err == NO_ERROR) {         err = writeTransactionData(BC_TRANSACTION, flags, handle, code, data, NULL);     }     if (err != NO_ERROR) {         if (reply) reply->setError(err);         return (mLastError = err);     }     if ((flags & TF_ONE_WAY) == 0) {         if (reply) {             err = waitForResponse(reply);         } else {             Parcel fakeReply;             err = waitForResponse(&fakeReply);         }     } else {         err = waitForResponse(NULL, NULL);     }     return err; }
```

这段代码应该还是比较好理解的：首先通过`writeTransactionData`写入数据，然后通过`waitForResponse`等待返回结果。`TF_ONE_WAY`表示此次请求是单向的，即：不用真正等待结果即可返回。

而`writeTransactionData`方法其实就是在组装`binder_transaction_data`数据：

```
status_t IPCThreadState::writeTransactionData(int32_t cmd, uint32_t binderFlags,     int32_t handle, uint32_t code, const Parcel& data, status_t* statusBuffer) {     binder_transaction_data tr;     tr.target.ptr = 0; /* Don't pass uninitialized stack data to a remote process */     tr.target.handle = handle;     tr.code = code;     tr.flags = binderFlags;     tr.cookie = 0;     tr.sender_pid = 0;     tr.sender_euid = 0;     const status_t err = data.errorCheck();     if (err == NO_ERROR) {         tr.data_size = data.ipcDataSize();         tr.data.ptr.buffer = data.ipcData();         tr.offsets_size = data.ipcObjectsCount()*sizeof(binder_size_t);         tr.data.ptr.offsets = data.ipcObjects();     } else if (statusBuffer) {         tr.flags |= TF_STATUS_CODE;         *statusBuffer = err;         tr.data_size = sizeof(status_t);         tr.data.ptr.buffer = reinterpret_cast<uintptr_t>(statusBuffer);         tr.offsets_size = 0;         tr.data.ptr.offsets = 0;     } else {         return (mLastError = err);     }     mOut.writeInt32(cmd);     mOut.write(&tr, sizeof(tr));     return NO_ERROR; }
```

对于`binder_transaction_data`在讲解Binder驱动的时候我们已经详细讲解过了。而这里的Parcel我们还不了解，那么接下来我们马上就来看一下这个类。

# 数据包装器：Parcel

Binder上提供的是跨进程的服务，每个服务包含了不同的接口，每个接口的参数数量和类型都不一样。那么当客户端想要调用服务端的接口，参数是如何跨进程传递给服务端的呢？除此之外，服务端想要给客户端返回结果，结果又是如何传递回来的呢？

这些问题的答案就是：Parcel。Parcel就像一个包装器，调用者可以以任意顺序往里面放入需要的数据，所有写入的数据就像是被打成一个整体的包，然后可以直接在Binde上传输。

Parcel提供了所有基本类型的写入和读出接口，下面是其中的一部分：

```
... status_t            writeInt32(int32_t val); status_t            writeUint32(uint32_t val); status_t            writeInt64(int64_t val); status_t            writeUint64(uint64_t val); status_t            writeFloat(float val); status_t            writeDouble(double val); status_t            writeCString(const char* str); status_t            writeString8(const String8& str); status_t            readInt32(int32_t *pArg) const; uint32_t            readUint32() const; status_t            readUint32(uint32_t *pArg) const; int64_t             readInt64() const; status_t            readInt64(int64_t *pArg) const; uint64_t            readUint64() const; status_t            readUint64(uint64_t *pArg) const; float               readFloat() const; status_t            readFloat(float *pArg) const; double              readDouble() const; status_t            readDouble(double *pArg) const; intptr_t            readIntPtr() const; status_t            readIntPtr(intptr_t *pArg) const; bool                readBool() const; status_t            readBool(bool *pArg) const; char16_t            readChar() const; status_t            readChar(char16_t *pArg) const; int8_t              readByte() const; status_t            readByte(int8_t *pArg) const; // Read a UTF16 encoded string, convert to UTF8 status_t            readUtf8FromUtf16(std::string* str) const; status_t            readUtf8FromUtf16(std::unique_ptr<std::string>* str) const; const char*         readCString() const; ...
```

因此对于基本类型，开发者可以直接调用接口写入和读出。而对于非基本类型，需要由开发者将其拆分成基本类型然后写入到Parcel中（读出的时候也是一样）。 Parcel会将所有写入的数据进行打包，Parcel本身可以作为一个整体在进程间传递。接收方在收到Parcel之后，只要按写入同样的顺序读出即可。

这个过程，和我们现实生活中寄送包裹做法是一样的：我们将需要寄送的包裹放到硬纸盒中交给快递公司。快递公司将所有的包裹进行打包，然后集中放到运输车中送到目的地，到了目的地之后然后再进行拆分。

Parcel既包含C++部分的实现，也同时提供了Java的接口，中间通过JNI衔接。Java层的接口其实仅仅是一层包装，真正的实现都是位于C++部分中，它们的关系如下图所示：

![img](assets/android_binder_2/Parcel_JNI-20190210002634740.png)

特别需要说明一下的是，Parcel类除了可以传递基本数据类型，还可以传递Binder对象：

```
status_t Parcel::writeStrongBinder(const sp<IBinder>& val) {     return flatten_binder(ProcessState::self(), val, this); }
```

这个方法写入的是`sp<IBinder>`类型的对象，而IBinder既可能是本地Binder，也可能是远程Binder，这样我们就不可以不用关心具体细节直接进行Binder对象的传递。

这也是为什么IInterface中定义了两个asBinder的static方法，如果你不记得了，请回忆一下这两个方法：

```
static sp<IBinder>  asBinder(const IInterface*); static sp<IBinder>  asBinder(const sp<IInterface>&);
```

而对于Binder驱动，我们前面已经讲解过：Binder驱动并不是真的将对象在进程间序列化传递，而是由Binder驱动完成了对于Binder对象指针的解释和翻译，使调用者看起来就像在进程间传递对象一样。

# Framework层的线程管理

在讲解Binder驱动的时候，我们就讲解过驱动中对应线程的管理。这里我们再来看看，Framework层是如何与驱动层对接进行线程管理的。

`ProcessState::setThreadPoolMaxThreadCount` 方法中，会通过`BINDER_SET_MAX_THREADS`命令设置进程支持的最大线程数量：

```
#define DEFAULT_MAX_BINDER_THREADS 15  status_t ProcessState::setThreadPoolMaxThreadCount(size_t maxThreads) {     status_t result = NO_ERROR;     if (ioctl(mDriverFD, BINDER_SET_MAX_THREADS, &maxThreads) != -1) {         mMaxThreads = maxThreads;     } else {         result = -errno;         ALOGE("Binder ioctl to set max threads failed: %s", strerror(-result));     }     return result; }
```

由此驱动便知道了该Binder服务支持的最大线程数。驱动在运行过程中，会根据需要，并在没有超过上限的情况下，通过`BR_SPAWN_LOOPER`命令通知进程创建线程：

`IPCThreadState`在收到`BR_SPAWN_LOOPER`请求之后，便会调用`ProcessState::spawnPooledThread`来创建线程：

```
status_t IPCThreadState::executeCommand(int32_t cmd) {     ...     case BR_SPAWN_LOOPER:         mProcess->spawnPooledThread(false);         break;     ... }
```

`ProcessState::spawnPooledThread`方法负责为线程设定名称并创建线程：

```
void ProcessState::spawnPooledThread(bool isMain) {     if (mThreadPoolStarted) {         String8 name = makeBinderThreadName();         ALOGV("Spawning new pooled thread, name=%s\n", name.string());         sp<Thread> t = new PoolThread(isMain);         t->run(name.string());     } }
```

线程在run之后，会调用`threadLoop`将自身添加的线程池中：

```
virtual bool threadLoop() {    IPCThreadState::self()->joinThreadPool(mIsMain);    return false; }
```

而`IPCThreadState::joinThreadPool`方法中，会根据当前线程是否是主线程发送`BC_ENTER_LOOPER`或者`BC_REGISTER_LOOPER`命令告知驱动线程已经创建完毕。整个调用流程如下图所示：

![img](assets/android_binder_2/create_thread_sequence-20190210002634769.png)

# C++ Binder服务举例

单纯的理论知识也许并不能让我们非常好的理解，下面我们以一个具体的Binder服务例子来结合上文的知识进行讲解。

下面以PowerManager为例，来看看C++的Binder服务是如何实现的。

下图是PowerManager C++部分的实现类图（PowerManager也有Java层的接口，但我们这里就不讨论了）。

![img](assets/android_binder_2/Binder_PowerManager-20190210002634778.png)

图中Binder Framework中的类我们在上文中已经介绍过了，而PowerManager相关的四个类，便是在Framework的基础上开发的。

`IPowerManager`定义了PowerManager所有对外提供的功能接口，其子类都继承了这些接口。

- `BpPowerManager`是提供给客户端调用的远程接口
- `BnPowerManager`中只有一个`onTransact`方法，该方法根据请求的code来对接每个请求，并直接调用`PowerManager`中对应的方法
- `PowerManager`是服务真正的实现

在IPowerManager.h中，通过`DECLARE_META_INTERFACE(PowerManager);`声明一些Binder必要的组件。在IPowerManager.cpp中，通过`IMPLEMENT_META_INTERFACE(PowerManager, "android.os.IPowerManager");`宏来进行实现。

# 本地实现：Native端

服务的本地实现主要就是实现BnPowerManager和PowerManager两个类，PowerManager是BnPowerManager的子类，因此在BnPowerManager中调用自身的`virtual`方法其实都是在子类PowerManager类中实现的。

BnPowerManager类要做的就是复写`onTransact`方法，这个方法的职责是：根据请求的code区分具体调用的是那个接口，然后按顺序从Parcel中读出打包好的参数，接着调用留待子类实现的虚函数。需要注意的是：**这里从Parcel读出参数的顺序需要和`BpPowerManager`中写入的顺序完全一致**，否则读出的数据将是无效的。

电源服务包含了好几个接口。虽然每个接口的实现**逻辑**各不一样，但从Binder框架的角度来看，它们的实现**结构**是一样。而这里我们并不关心电源服务的实现细节，因此我们取其中一个方法看其实现方式即可。

首先我们来看一下`BnPowerManager::onTransact`中的代码片段：

```
status_t BnPowerManager::onTransact(uint32_t code,                                     const Parcel& data,                                     Parcel* reply,                                     uint32_t flags) {   switch (code) {   ...       case IPowerManager::REBOOT: {       CHECK_INTERFACE(IPowerManager, data, reply);       bool confirm = data.readInt32();       String16 reason = data.readString16();       bool wait = data.readInt32();       return reboot(confirm, reason, wait);     }   ...   } }
```

这段代码中我们看到了实现中是如何根据code区分接口，并通过Parcel读出调用参数，然后调用具体服务方的。

而`PowerManager`这个类才真正是服务实现的本体，reboot方法真正实现了重启的逻辑：

```
status_t PowerManager::reboot(bool confirm, const String16& reason, bool wait) {   const std::string reason_str(String8(reason).string());   if (!(reason_str.empty() || reason_str == kRebootReasonRecovery)) {     LOG(WARNING) << "Ignoring reboot request with invalid reason \""                  << reason_str << "\"";     return BAD_VALUE;   }   LOG(INFO) << "Rebooting with reason \"" << reason_str << "\"";   if (!property_setter_->SetProperty(ANDROID_RB_PROPERTY,                                      kRebootPrefix + reason_str)) {     return UNKNOWN_ERROR;   }   return OK; }
```

通过这样结构的设计，将框架相关的逻辑（BnPowerManager中的实现）和业务本身的逻辑（PowerManager中的实现）彻底分离开了，保证每一个类都非常的“干净”，这一点是很值得我们在做软件设计时学习的。

# 服务的发布

服务实现完成之后，并不是立即就能让别人使用的。上文中，我们就说到过：所有在Binder上发布的服务必须要注册到ServiceManager中才能被其他模块获取和使用。而在`BinderService`类中，提供了`publishAndJoinThreadPool`方法来简化服务的发布，其代码如下：

```
static void publishAndJoinThreadPool(bool allowIsolated = false) {    publish(allowIsolated);    joinThreadPool(); } static status_t publish(bool allowIsolated = false) {    sp<IServiceManager> sm(defaultServiceManager());    return sm->addService(            String16(SERVICE::getServiceName()),            new SERVICE(), allowIsolated); } ... static void joinThreadPool() {    sp<ProcessState> ps(ProcessState::self());    ps->startThreadPool();    ps->giveThreadPoolName();    IPCThreadState::self()->joinThreadPool(); }
```

由此可见，Binder服务的发布其实有三个步骤：

1. 通过`IServiceManager::addService`在ServiceManager中进行服务的注册
2. 通过`ProcessState::startThreadPool`启动线程池
3. 通过`IPCThreadState::joinThreadPool`将主线程加入的Binder中

# 远程接口：Proxy端

Proxy类是供客户端使用的。BpPowerManager需要实现IPowerManager中的所有接口。

我们还是以上文提到的reboot接口为例，来看看`BpPowerManager::reboot`方法是如何实现的：

```
virtual status_t reboot(bool confirm, const String16& reason, bool wait) {    Parcel data, reply;    data.writeInterfaceToken(IPowerManager::getInterfaceDescriptor());    data.writeInt32(confirm);    data.writeString16(reason);    data.writeInt32(wait);    return remote()->transact(REBOOT, data, &reply, 0); }
```

这段代码很简单，逻辑就是：通过Parcel写入调用参数进行打包，然后调用`remote()->transact`将请求发送出去。

其实BpPowerManager中其他方法，甚至所有其他BpXXX中所有的方法，实现都是和这个方法一样的套路。就是：通过Parcel打包数据，通过`remote()->transact`发送数据。而这里的remote返回的其实就是BpBinder对象，由此经由IPCThreadState将数据发送到了驱动层。如果你已经不记得，请重新看一下下面这幅图：

![img](assets/android_binder_2/BpBinder_BBinder-20190210003556671.png)

另外，需要一下的是，这里的`REBOOT`就是请求的code，而这个code是在IPowerManager中定义好的，这样子类可以直接使用，并保证是一致的：

```
enum {    ACQUIRE_WAKE_LOCK            = IBinder::FIRST_CALL_TRANSACTION,    ACQUIRE_WAKE_LOCK_UID        = IBinder::FIRST_CALL_TRANSACTION + 1,    RELEASE_WAKE_LOCK            = IBinder::FIRST_CALL_TRANSACTION + 2,    UPDATE_WAKE_LOCK_UIDS        = IBinder::FIRST_CALL_TRANSACTION + 3,    POWER_HINT                   = IBinder::FIRST_CALL_TRANSACTION + 4,    UPDATE_WAKE_LOCK_SOURCE      = IBinder::FIRST_CALL_TRANSACTION + 5,    IS_WAKE_LOCK_LEVEL_SUPPORTED = IBinder::FIRST_CALL_TRANSACTION + 6,    USER_ACTIVITY                = IBinder::FIRST_CALL_TRANSACTION + 7,    WAKE_UP                      = IBinder::FIRST_CALL_TRANSACTION + 8,    GO_TO_SLEEP                  = IBinder::FIRST_CALL_TRANSACTION + 9,    NAP                          = IBinder::FIRST_CALL_TRANSACTION + 10,    IS_INTERACTIVE               = IBinder::FIRST_CALL_TRANSACTION + 11,    IS_POWER_SAVE_MODE           = IBinder::FIRST_CALL_TRANSACTION + 12,    SET_POWER_SAVE_MODE          = IBinder::FIRST_CALL_TRANSACTION + 13,    REBOOT                       = IBinder::FIRST_CALL_TRANSACTION + 14,    SHUTDOWN                     = IBinder::FIRST_CALL_TRANSACTION + 15,    CRASH                        = IBinder::FIRST_CALL_TRANSACTION + 16, };
```

# 服务的获取

在服务已经发布之后，客户端该如何获取其服务接口然后对其发出请求调用呢？

很显然，客户端应该通过BpPowerManager的对象来请求其服务。但看一眼BpPowerManager的构造函数，我们会发现，似乎没法直接创建一个这类的对象，因为这里需要一个`sp<IBinder>`类型的参数。

```
BpPowerManager(const sp<IBinder>& impl)    : BpInterface<IPowerManager>(impl) { }
```

那么这个`sp<IBinder>`参数我们该从哪里获取呢？

回忆一下前面的内容：Proxy其实是包含了一个指向Server的句柄，所有的请求发送出去的时候都需要包含这个句柄作为一个标识。而想要拿到这个句柄，我们自然应当想到ServiceManager。我们再看一下ServiceManager的接口自然就知道这个`sp<IBinder>`该如何获取了：

```
/** * Retrieve an existing service, blocking for a few seconds * if it doesn't yet exist. */ virtual sp<IBinder>         getService( const String16& name) const = 0; /** * Retrieve an existing service, non-blocking. */ virtual sp<IBinder>         checkService( const String16& name) const = 0;
```

这里的两个方法都可以获取服务对应的`sp<IBinder>`对象，一个是阻塞式的，另外一个不是。传递的参数是一个字符串，这个就是服务在addServer时对应的字符串，而对于PowerManager来说，这个字符串就是”power”。因此，我们可以通过下面这行代码创建出BpPowerManager的对象。

```
sp<IBinder> bs = defaultServiceManager()->checkService(serviceName); sp<IPowerManager> pm = new BpPowerManager(bs);
```

但这样做还会存在一个问题：BpPowerManager中的方法调用是经由驱动然后跨进程调用的。通常情况下，当我们的客户端与PowerManager服务所在的进程不是同一个进程的时候，这样调用是没有问题的。那假设我们的客户端又刚好和PowerManager服务在同一个进程该如何处理呢？

针对这个问题，Binder Framework提供的解决方法是：通过`interface_cast`这个方法来获取服务的接口对象，由这个方法本身根据是否是在同一个进程，来自动确定返回一个本地Binder还是远程Binder。`interface_cast`是一个模板方法，其源码如下：

```
template<typename INTERFACE> inline sp<INTERFACE> interface_cast(const sp<IBinder>& obj) {     return INTERFACE::asInterface(obj); }
```

调用这个方法的时候我们需要指定Binder服务的IInterface，因此对于PowerManager，我们需要这样获取其Binder接口对象：

```
const String16 serviceName("power"); sp<IBinder> bs = defaultServiceManager()->checkService(serviceName); if (bs == NULL) {   return NAME_NOT_FOUND; } sp<IPowerManager> pm = interface_cast<IPowerManager>(bs);
```

我们再回头看一下`interface_cast`这个方法体，这里是在调用`INTERFACE::asInterface(obj)`，而对于IPowerManager来说，其实就是`IPowerManager::asInterface(obj)`。那么`IPowerManager::asInterface`这个方法是哪里定义的呢？

这个正是上文提到的DECLARE_META_INTERFACE和IMPLEMENT_META_INTERFACE两个宏所起的作用。IMPLEMENT_META_INTERFACE宏包含了下面这段代码：

```
android::sp<I##INTERFACE> I##INTERFACE::asInterface(  \        const android::sp<android::IBinder>& obj)      \ {                                                     \    android::sp<I##INTERFACE> intr;                    \    if (obj != NULL) {                                 \        intr = static_cast<I##INTERFACE*>(             \            obj->queryLocalInterface(                  \                    I##INTERFACE::descriptor).get());  \        if (intr == NULL) {                            \            intr = new Bp##INTERFACE(obj);             \        }                                              \    }                                                  \    return intr;                                       \ }                                                     \
```

这里我们将“##INTERFACE”通过“PowerManager”代替，得到的结果就是：

```
android::sp<IPowerManager> IPowerManager::asInterface(         const android::sp<android::IBinder>& obj)       {                                                           android::sp<IPowerManager> intr;                        if (obj != NULL) {                                          intr = static_cast<IPowerManager*>(                         obj->queryLocalInterface(                                       IPowerManager::descriptor).get());         if (intr == NULL) {                                         intr = new BpPowerManager(obj);                     }                                                   }                                                       return intr;                                        }
```

这个便是`IPowerManager::asInterface`方法的实现，这段逻辑的含义就是：

- 先尝试通过`queryLocalInterface`看看能够获得本地Binder，如果是在服务所在进程调用，自然能获取本地Binder，否则将返回NULL
- 如果获取不到本地Binder，则创建并返回一个远程Binder。

由此保证了：我们在进程内部的调用，是直接通过方法调用的形式。而不在同一个进程的时候，才通过Binder进行跨进程的调用。

# C++层的ServiceManager

前文已经两次介绍过ServiceManager了，我们知道这个模块负责了所有Binder服务的管理，并且也看到了Binder驱动中对于这个模块的实现。可以说ServiceManager是整个Binder IPC的控制中心和交通枢纽。这里我们就来看一下这个模块的具体实现。

ServiceManager是一个独立的可执行文件，在设备中的进程名称是`/system/bin/servicemanager`，这个也是其可执行文件的路径。

ServiceManager实现源码的位于这个路径：`frameworks/native/cmds/servicemanager/`，其main函数的主要内容如下：

```
int main() {     struct binder_state *bs;     bs = binder_open(128*1024);     if (!bs) {         ALOGE("failed to open binder driver\n");         return -1;     }     if (binder_become_context_manager(bs)) {         ALOGE("cannot become context manager (%s)\n", strerror(errno));         return -1;     }     ...     binder_loop(bs, svcmgr_handler);     return 0; }
```

这段代码很简单，主要做了三件事情：

1. `binder_open(128*1024);` 是打开Binder，并指定缓存大小为128k，由于ServiceManager提供的接口很简单（下文会讲到），因此并不需要普通进程那么多（1M - 8K）的缓存
2. `binder_become_context_manager(bs)` 使自己成为Context Manager。这里的Context Manager是Binder驱动里面的名称，等同于ServiceManager。`binder_become_context_manager`的方法实现只有一行代码：`ioctl(bs->fd, BINDER_SET_CONTEXT_MGR, 0);` 看过Binder驱动部分解析的内容，这行代码应该很容易理解了
3. `binder_loop(bs, svcmgr_handler);` 是在Looper上循环，等待其他模块请求服务

service_manager.c中的实现与普通Binder服务的实现有些不一样：并没有通过继承接口类来实现，而是通过几个c语言的函数来完成了实现。这个文件中的主要方法如下：

| 方法名称        | 方法说明                                         |
| --------------- | ------------------------------------------------ |
| main            | 可执行文件入口函数，刚刚已经做过说明             |
| svcmgr_handler  | 请求的入口函数，类似于普通Binder服务的onTransact |
| do_add_service  | 注册一个Binder服务                               |
| do_find_service | 通过名称查找一个已经注册的Binder服务             |

ServiceManager中，通过`svcinfo`结构体来描述已经注册的Binder服务：

```
struct svcinfo {     struct svcinfo *next;     uint32_t handle;     struct binder_death death;     int allow_isolated;     size_t len;     uint16_t name[0]; };
```

`next`是一个指针，指向下一个服务，通过这个指针将所有服务串成了链表。`handle`是指向Binder服务的句柄，这个句柄是由Binder驱动翻译，指向了Binder服务的实体（参见驱动中：Binder中的“面向对象”），`name`是服务的名称。

ServiceManager的实现逻辑并不复杂，这个模块就好像在整个系统上提供了一个全局的HashMap而已：通过服务名称进行服务注册，然后再通过服务名称来查找。而真正复杂的逻辑其实都是在Binder驱动中实现了。

## ServiceManager的接口

源码路径：

```
frameworks/native/include/binder/IServiceManager.h frameworks/native/libs/binder/IServiceManager.cpp
```

ServiceManager的C++接口定义如下：

```
class IServiceManager : public IInterface { public:     DECLARE_META_INTERFACE(ServiceManager);     virtual sp<IBinder>         getService( const String16& name) const = 0;     virtual sp<IBinder>         checkService( const String16& name) const = 0;     virtual status_t            addService( const String16& name,                                             const sp<IBinder>& service,                                             bool allowIsolated = false) = 0;     virtual Vector<String16>    listServices() = 0;     enum {         GET_SERVICE_TRANSACTION = IBinder::FIRST_CALL_TRANSACTION,         CHECK_SERVICE_TRANSACTION,         ADD_SERVICE_TRANSACTION,         LIST_SERVICES_TRANSACTION,     }; };
```

这里我们看到，ServiceManager提供的接口只有四个，这四个接口说明如下：

| 接口名称     | 接口说明                                |
| ------------ | --------------------------------------- |
| addService   | 向ServiceManager中注册一个新的Service   |
| getService   | 查询Service。如果服务不存在，将阻塞数秒 |
| checkService | 查询Service，但是不会阻塞               |
| listServices | 列出所有的服务                          |

这其中，最后一个接口是为了调试而提供的。通过`adb shell`连接到设备上之后，可以通过输入`service list` 输出所有注册的服务列表。这里”service”可执行文件其实就是通过调用`listServices`接口获取到服务列表的。

`service`命令的源码路径在这里：frameworks/native/cmds/service

`service list`的输出看起来像下面这样一次输出可能有一百多个服务，这里省略了：

```
255|angler:/ # service list                                                     Found 125 services: 0 sip: [android.net.sip.ISipService] 1 nfc: [android.nfc.INfcAdapter] 2 carrier_config: [com.android.internal.telephony.ICarrierConfigLoader] 3 phone: [com.android.internal.telephony.ITelephony] 4 isms: [com.android.internal.telephony.ISms] 5 iphonesubinfo: [com.android.internal.telephony.IPhoneSubInfo] 6 simphonebook: [com.android.internal.telephony.IIccPhoneBook] 7 telecom: [com.android.internal.telecom.ITelecomService] 8 isub: [com.android.internal.telephony.ISub] 9 contexthub_service: [android.hardware.location.IContextHubService] 10 dns_listener: [android.net.metrics.IDnsEventListener] 11 connmetrics: [android.net.IIpConnectivityMetrics] 12 connectivity_metrics_logger: [android.net.IConnectivityMetricsLogger] 13 bluetooth_manager: [android.bluetooth.IBluetoothManager] 14 imms: [com.android.internal.telephony.IMms] 15 media_projection: [android.media.projection.IMediaProjectionManager] 16 launcherapps: [android.content.pm.ILauncherApps] 17 shortcut: [android.content.pm.IShortcutService] 18 fingerprint: [android.hardware.fingerprint.IFingerprintService] 19 trust: [android.app.trust.ITrustManager] 20 media_router: [android.media.IMediaRouterService] ...
```

普通的Binder服务我们需要通过ServiceManager来获取接口才能调用，那么ServiceManager的接口有如何获得呢？在libbinder中，提供了一个`defaultServiceManager`方法来获取ServiceManager的Proxy，并且这个方法不需要传入参数。原因我们在驱动篇中也已经讲过了：Binder的实现中，为ServiceManager留了一个特殊的位置，不需要像普通服务那样通过标识去查找。`defaultServiceManager`代码如下：

```
sp<IServiceManager> defaultServiceManager() {     if (gDefaultServiceManager != NULL) return gDefaultServiceManager;     {         AutoMutex _l(gDefaultServiceManagerLock);         while (gDefaultServiceManager == NULL) {             gDefaultServiceManager = interface_cast<IServiceManager>(                 ProcessState::self()->getContextObject(NULL));             if (gDefaultServiceManager == NULL)                 sleep(1);         }     }     return gDefaultServiceManager; }
```

# 结束语

本文我们详细讲解了Binder Framework C++层的实现。

但对于Android App开发者来说，绝大部分情况下都是在用Java语言开发。那么，在下一篇文章中，我就来详细讲解Binder Framework Java层的实现。并且也会讲解AIDL与Binder的关系，敬请期待。

------

如果你喜欢我写的文章，说不定我写的书： 

《深入剖析Android新特性》

也会对你有帮助。