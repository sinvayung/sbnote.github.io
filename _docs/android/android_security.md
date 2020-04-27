## Android 8.0 中的安全增强功能

每个 Android 版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 8.0 中提供的一些主要安全增强功能：

- **加密**：在工作资料中增加了对取消密钥的支持。
- **验证启动**：增加了 Android 验证启动 (AVB)。支持回滚保护（用于引导加载程序）的验证启动代码库已添加到 AOSP 中。建议提供引导加载程序支持，以便为 HLOS 提供回滚保护。建议将引导加载程序设为只能由用户通过实际操作设备来解锁。
- **锁定屏幕**：增加了对使用防篡改硬件验证锁定屏幕凭据的支持。
- **KeyStore**：搭载 Android 8.0+ 的所有设备所需的[密钥认证](https://source.android.google.cn/security/keystore/attestation)。增加了 [ID 认证](https://source.android.google.cn/security/keystore/attestation#id-attestation)支持，以改善零触摸注册。
- **沙盒**：使用 Project Treble 的框架和设备特定组件之间的标准接口更[紧密地对许多组件进行沙盒化处理](https://android-developers.googleblog.com/2017/07/shut-hal-up.html)。将 [seccomp 过滤](https://android-developers.googleblog.com/2017/07/seccomp-filter-in-android-o.html)应用到了所有不信任的应用，以减少内核的攻击面。[WebView](https://android-developers.googleblog.com/2017/06/whats-new-in-webview-security.html) 现在运行在一个独立的进程中，对系统其余部分的访问非常有限。
- **内核加固**：实现了[加固 usercopy](https://android-developers.googleblog.com/2017/08/hardening-kernel-in-android-oreo.html)、PAN 模拟、初始化后只读以及 KASLR。
- **用户空间加固**：为媒体堆栈实现了 CFI。应用叠加层不能再覆盖系统关键型窗口，并且用户有办法关闭它们。
- **流式操作系统更新**：在磁盘空间不足的设备上启用了[更新](https://source.android.google.cn/devices/tech/ota/ab_updates#streaming-updates)。
- **安装未知应用**：用户必须[授予权限](https://developer.android.google.cn/studio/publish/index.html#publishing-unknown)，才能从不是第一方应用商店的来源安装应用。
- **隐私权**：对于设备上的每个应用和每个用户，Android ID (SSAID) 具有不同的值。对于网络浏览器应用，Widevine 客户端 ID 会针对每个应用包名称和网页来源返回不同的值。 `net.hostname` 现在为空，并且 DHCP 客户端不再发送主机名。`android.os.Build.SERIAL` 已被替换为 [`Build.SERIAL` API](https://developer.android.google.cn/reference/android/os/Build.html#getSerial())（受到用户控制权限的保护）。改进了某些芯片组中的 MAC 地址随机化功能。



## Android 7.0 中的安全增强功能

每个 Android 版本中都包含数十项用于保护用户的安全增强功能。以下是 Android 7.0 中提供的一些主要安全增强功能：

- **文件级加密**：在文件级进行加密，而不是将整个存储区域作为单个单元进行加密。这种加密方式可以更好地隔离和保护设备上的不同用户和资料（例如个人资料和工作资料）。
- **直接启动**：通过文件级加密实现，允许特定应用（例如，闹钟和无障碍功能）在设备已开机但未解锁的情况下运行。
- **验证启动**：现在，验证启动会被严格强制执行，从而使遭到入侵的设备无法启动；验证启动支持纠错功能，有助于更可靠地防范非恶意数据损坏。
- **SELinux**：更新后的 SELinux 配置和更高的 Seccomp 覆盖率有助于进一步锁定应用沙盒并减小受攻击面。
- **库加载顺序随机化和经过改进的 ASLR**：更高的随机性可以使一些代码重用攻击得逞的难度增大。
- **内核加固**：通过将内核内存的各个分区标记为只读，限制内核对用户空间地址的访问，并进一步减小现有的受攻击面，为更高版本的内核添加额外的内存保护。
- **APK 签名方案 v2**：引入了一种全文件签名方案，该方案有助于加快验证速度并增强完整性保证。
- **可信 CA 商店**：为了使应用更轻松地控制对其安全网络流量的访问，对于目标 API 级别为 24+ 的应用来说，用户安装的证书授权中心以及通过 Device Admin API 安装的证书授权中心默认情况下不再可信。此外，所有新的 Android 设备必须搭载相同的可信 CA 存储区。
- **网络安全配置**：通过声明式配置文件来配置网络安全设置和传输层安全协议 (TLS)。



## Android 6.0 中的安全增强功能

每个 Android 版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 6.0 中提供的一些主要安全增强功能：

- **运行时权限**：应用在运行时请求权限，而不是在安装时被授予权限。用户可以为 M 及更低版本的 Android 应用启用和停用权限。
- **验证启动**：在执行系统软件之前，先对其进行一系列加密检查，以确保手机从引导加载程序到操作系统均处于正常状况。
- **硬件隔离安全措施**：新的硬件抽象层 (HAL)，Fingerprint API、锁定屏幕、设备加密功能和客户端证书可以利用它来保护密钥免遭内核入侵和/或现场攻击。
- **指纹**：现在，只需触摸一下，即可解锁设备。开发者还可以借助新的 API 来使用指纹锁定和解锁加密密钥。
- **加装 SD 卡**：可将移动媒体设备加装到设备上，以便扩展可用存储空间来存放本地应用数据、照片、视频等内容，但仍受块级加密保护。
- **明文流量**：开发者可以使用新的 StrictMode 来确保其应用不会使用明文。
- **系统加固**：通过由 SELinux 强制执行的政策对系统进行加固。这可以实现更好的用户隔离和 IOCTL 过滤、降低可从设备/系统之外访问的服务面临的威胁、进一步强化 SELinux 域，以及高度限制对 /proc 的访问。
- **USB 访问控制**：必须由用户确认是否允许通过 USB 访问手机上的文件、存储空间或其他功能。现在，默认设置是“仅充电”，如果要访问存储空间，必须获得用户的明确许可。



## Android 5.0 中的安全增强功能

每个 Android 版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 5.0 中提供的一些主要安全增强功能：

- **默认加密：** 在以开箱即用的方式搭载 L 的设备上，会默认启用全盘加密功能，以便更好地保护丢失设备或被盗设备上的数据。对于更新到 L 的设备，可以在**设置** > **安全性**部分进行加密。
- **经过改进的全盘加密功能：** 使用 `scrypt` 保护用户密码免遭暴力破解攻击；在可能的情况下，该密钥会绑定到硬件密钥库，以防范来自设备外的攻击。和以往一样，Android 屏幕锁定密钥和设备加密密钥不会被发送到设备以外，也不会提供给任何应用。
- **通过 SELinux 得到增强的 Android 沙盒**：对于所有域，Android 现在都要求 SELinux 处于强制模式。SELinux 是 Linux 内核中的强制访问控制 (MAC) 系统，用于增强现有的自主访问控制 (DAC) 安全模型。这个新的安全层为防范潜在的安全漏洞提供了额外的保护屏障。
- **Smart Lock：**Android 现在包含一些 Trustlet，它们可以提供更灵活的设备解锁方式。例如，Trustlet 可让设备在靠近其他可信设备（通过 NFC、蓝牙）时或用户拥有可信面孔时自动解锁。
- **面向手机和平板电脑的多用户功能、受限个人资料和访客模式：** Android 现在为手机提供了多用户功能，并包含一个访客模式。利用访客模式，您可以让访客轻松地临时使用您的设备，而不向他们授予对您的数据和应用的访问权限。
- **不使用 OTA 的 WebView 更新方式：** 现在可以独立于框架对 WebView 进行更新，而且无需采用系统 OTA 方式。这有助于更快速地应对 WebView 中的潜在安全问题。
- **经过更新的 HTTPS 和 TLS/SSL 加密功能**：现在启用了 TLSv1.2 和 TLSv1.1，首选是正向加密，启用了 AES-GCM，停用了弱加密套件（MD5、3DES 和导出密码套件）。如需更多详细信息，请访问 [https://developer.android.com/reference/javax/net/ssl/SSLSocket.html](https://developer.android.google.cn/reference/javax/net/ssl/SSLSocket.html)。
- **移除了非 PIE 链接器支持：** Android 现在要求所有动态链接的可执行文件都要支持 PIE（位置无关可执行文件）。这有助于增强 Android 的地址空间布局随机化 (ASLR) 实现。
- **FORTIFY_SOURCE 改进：** 以下 libc 函数现在实现了 FORTIFY_SOURCE 保护功能：`stpcpy()`、`stpncpy()`、`read()`、`recvfrom()`、`FD_CLR()`、`FD_SET()` 和 `FD_ISSET()`。这有助于防范涉及这些函数的内存损坏漏洞。
- **安全修复程序：** Android 5.0 中还包含针对 Android 特有漏洞的修复程序。有关这些漏洞的信息已提供给“开放手机联盟”(Open Handset Alliance) 成员，并且 Android 开放源代码项目中提供了相应的修复程序。为了提高安全性，搭载更低版本 Android 的某些设备可能也会包含这些修复程序。



## Android 4.4 中的安全增强功能

每个 Android 版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 4.4 中提供的一些安全增强功能：

- **通过 SELinux 得到增强的 Android 沙盒。** Android 现在以强制模式使用 SELinux。SELinux 是 Linux 内核中的强制访问控制 (MAC) 系统，用于增强基于自主访问控制 (DAC) 的现有安全模型。这为防范潜在的安全漏洞提供了额外的保护屏障。
- **按用户应用 VPN。** 多用户设备上现在按用户应用 VPN。这样一来，用户就可以通过一个 VPN 路由所有网络流量，而不会影响使用同一设备的其他用户。
- **AndroidKeyStore 中的 ECDSA 提供程序支持。** Android 现在有一个允许使用 ECDSA 和 DSA 算法的密钥库提供程序。
- **设备监测警告。** 如果有任何证书添加到可允许监测已加密网络流量的设备证书库中，Android 都会向用户发出警告。
- **FORTIFY_SOURCE。** Android 现在支持 FORTIFY_SOURCE 第 2 级，并且所有代码在编译时都会受到这些保护。FORTIFY_SOURCE 已得到增强，能够与 Clang 配合使用。
- **证书锁定。** Android 4.4 能够检测安全的 SSL/TLS 通信中是否使用了欺诈性 Google 证书，并且能够阻止这种行为。
- **安全漏洞修复程序。** Android 4.4 中还包含针对 Android 特有漏洞的修复程序。有关这些漏洞的信息已提供给“开放手机联盟”(Open Handset Alliance) 成员，并且 Android 开放源代码项目中提供了相应的修复程序。为了提高安全性，搭载更低版本 Android 的某些设备可能也会包含这些修复程序。



## Android 4.3 中的安全增强功能

每个 Android 版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 4.3 中提供的一些安全增强功能：

- **通过 SELinux 得到增强的 Android 沙盒。** 此版本利用 Linux 内核中的 SELinux 强制访问控制系统 (MAC) 增强了 Android 沙盒。SELinux 强化功能（用户和开发者看不到它）可提高现有 Android 安全模型的可靠性，同时与现有应用保持兼容。为了确保持续兼容，此版本允许以宽容模式使用 SELinux。此模式会记录所有政策违规行为，但不会中断应用或影响系统行为。
- **没有 SetUID/SetGID 程序：** 针对 Android 系统文件添加了对文件系统功能的支持，并移除了所有 SetUID/SetGUID 程序。这可以减小 Root 攻击面，并降低出现潜在安全漏洞的可能性。
- **ADB 身份验证。** 从 Android 4.2.2 起，开始使用 RSA 密钥对为 ADB 连接进行身份验证。这可以防止攻击者在实际接触到设备的情况下未经授权使用 ADB。
- **限制 Android 应用执行 SetUID 程序。** /system 分区现在针对 Zygote 衍生的进程装载了 nosuid，以防止 Android 应用执行 SetUID 程序。这可以减小 Root 攻击面，并降低出现潜在安全漏洞的可能性。
- **功能绑定。** 在执行应用之前，Android Zygote 和 ADB 现在会先使用 prctl(PR_CAPBSET_DROP) 舍弃不必要的功能。这可以防止 Android 应用和从 shell 启动的应用获取特权功能。
- **AndroidKeyStore 提供程序。** Android 现在有一个允许应用创建专用密钥的密钥库提供程序。该程序可以为应用提供一个用于创建或存储私钥的 API，其他应用将无法使用这些私钥。
- **KeyChain isBoundKeyAlgorithm。** Keychain API 现在提供了一种方法 (isBoundKeyType)，可让应用确认系统级密钥是否已绑定到设备的硬件信任根。该方法提供了一个用于创建或存储私钥的位置，即使发生 Root 权限被窃取的情况，这些私钥也无法从设备中导出。
- **NO_NEW_PRIVS。** 在执行应用代码之前，Android Zygote 现在会先使用 prctl(PR_SET_NO_NEW_PRIVS) 禁止添加新权限。这可以防止 Android 应用执行可通过 execve 提权的操作。（此功能需要使用 3.5 或更高版本的 Linux 内核）。
- **FORTIFY_SOURCE 增强功能。** Android x86 和 MIPS 上启用了 FORTIFY_SOURCE，并增强了 strchr()、strrchr()、strlen() 和 umask() 调用。这可以检测潜在的内存损坏漏洞或没有结束符的字符串常量。
- **迁移保护。** 针对静态关联的可执行文件启用了只读迁移 (relro) 技术，并移除了 Android 代码中的所有文本迁移技术。这可以深度防范潜在的内存损坏漏洞。
- **经过改进的 EntropyMixer。** 除了定期执行混合操作之外，EntropyMixer 现在还会在关机/重新启动时写入熵。这样一来，便可以保留设备开机时生成的所有熵，而这对于配置之后立即重新启动的设备来说尤其有用。
- **安全漏洞修复程序。** Android 4.3 中还包含针对 Android 特有漏洞的修复程序。有关这些漏洞的信息已提供给“开放手机联盟”(Open Handset Alliance) 成员，并且 Android 开放源代码项目中提供了相应的修复程序。为了提高安全性，搭载更低版本 Android 的某些设备可能也会包含这些修复程序。



## Android 4.2 中的安全增强功能

Android 提供了一个多层安全模型，[Android 安全性概述](https://source.android.google.cn/security/index.html)中对该模型进行了介绍。每个 Android 更新版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 4.2 中引入的一些安全增强功能：

- **应用验证** - 用户可以选择启用“验证应用”，并且可以选择在应用安装之前由应用验证程序对其进行筛查。如果用户尝试安装的应用可能有害，应用验证功能可以提醒用户；如果应用的危害性非常大，应用验证功能可以阻止安装。
- **加强对付费短信的控制** - 如果有应用尝试向使用付费服务的短代码发送短信（可能会产生额外的费用），Android 将会通知用户。用户可以选择是允许还是阻止该应用发送短信。
- **始终开启的 VPN** - 可以配置 VPN，以确保在建立 VPN 连接之前应用无法访问网络。这有助于防止应用跨其他网络发送数据。
- **锁住证书** - Android 的核心库现在支持[锁住证书](https://developer.android.google.cn/reference/android/net/http/X509TrustManagerExtensions.html)。如果证书未关联到一组应关联的证书，锁住的域将会收到证书验证失败消息。这有助于防范证书授权中心免遭可能的入侵。
- **改进后的 Android 权限显示方式** - 权限划分到了多个对用户来说更清晰明了的组中。在审核权限时，用户可以点击权限来查看关于相应权限的更多详细信息。
- **installd 安全强化** - `installd` 守护进程不会以 Root 用户身份运行，这样可以缩小 Root 提权攻击的潜在攻击面。
- **init 脚本安全强化** - init 脚本现在会应用 `O_NOFOLLOW` 语义来防范与符号链接相关的攻击。
- **FORTIFY_SOURCE** - Android 现在会实现 `FORTIFY_SOURCE`，以供系统库和应用用于防范内存损坏。
- **ContentProvider 默认配置** - 默认情况下，对于每个[内容提供方](https://developer.android.google.cn/reference/android/content/ContentProvider.html)，选择 API 17 级的应用都会将“export”设为“false”，以缩小应用的默认受攻击面。
- **加密** - 修改了 SecureRandom 和 Cipher.RSA 的默认实现，以便使用 OpenSSL。为使用 OpenSSL 1.0.1 的 TLSv1.1 和 TLSv1.2 添加了安全套接字支持
- **安全漏洞修复程序** - 升级了开放源代码库，新增了一些安全漏洞修复程序，其中包括 WebKit、libpng、OpenSSL 和 LibXML。Android 4.2 中还包含针对 Android 特有漏洞的修复程序。有关这些漏洞的信息已提供给“开放手机联盟”(Open Handset Alliance) 成员，并且 Android 开放源代码项目中提供了相应的修复程序。为了提高安全性，部分搭载更低版本 Android 系统的设备可能也会包含这些修复程序。



## Android 1.5 至 4.1 中的安全增强功能

Android 提供了一个多层安全模型，[Android 安全性概述](https://source.android.google.cn/security/index.html)中对该模型进行了介绍。每个 Android 更新版本中都包含数十种用于保护用户的安全增强功能。以下是 Android 1.5 至 4.1 版中引入的一些安全增强功能：

- **Android 1.5**

  ProPolice：旨在防止堆栈缓冲区溢出 (-fstack-protector)safe_iop：旨在减少整数溢出OpenBSD dlmalloc 的扩展程序：旨在防范 double free() 漏洞和连续块攻击。连续块攻击是利用堆损坏的常见攻击方式。OpenBSD calloc：旨在防止在内存分配期间发生整数溢出

- **Android 2.3**

  格式化字符串漏洞防护功能 (-Wformat-security -Werror=format-security)基于硬件的 No eXecute (NX)：旨在防止在堆栈和堆上执行代码Linux mmap_min_addr：旨在降低空指针解引用提权风险（在 Android 4.1 中得到了进一步增强）

- **Android 4.0**

  地址空间布局随机化 (ASLR)：旨在随机排列内存中的关键位置

- **Android 4.1**

  PIE（位置无关可执行文件）支持只读重定位/立即绑定 (-Wl,-z,relro -Wl,-z,now)启用了 dmesg_restrict（避免内核地址泄露）启用了 kptr_restrict（避免内核地址泄露）

