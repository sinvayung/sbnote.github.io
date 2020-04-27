# SEAndroid规则介绍[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#seandroid)

来源: https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/

history:

- version 1.0 by werther zhang @2016-12-12
- version 1.1 by werther zhang @2017-06-27 总结项目中遇到问题和解决方案

## 前言[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#_1)

sepolicy的语法是gnu m4, 是unix系统的宏处理器， 跟C的宏类似。

以下出现的所有与系统进程名字一样的， 除非特别指出进程， 否则都只是名字， 不与特定进程关联。

下面， 先整理下概念.. 知道这么个东西就行，不用理解，后面会详细提到。

在linux系统中，　所有单元(文件，目录，文件系统，进程等),可以分为两类，主动单元和被动单元．进程属于主动单元（不完全，进程的资源在被访问时，属于被动单元的概念），　而其他的无法发起动作的都属于被动单元．而sepolicy定义的分别是主动单元的行为规则和被动单元的继承规则(还是由主动单元发起)．

在提到domain这个概念时，一则表示主动单元scontext中第三个字段，比如，下一个例子中sdcard进程的domain就是sdcardd；一则指的是属性，具体出现在规则语句中，比如后文的`type sdcardd domain` 是指讲sdcardd与属性domain关联，而属性domain就可以表示所有的与之关联的类型，因为所有被规则了的进程都会与domain属性关联，所以domain在规则语句中有时候指代所有进程。

在提到type这个概念时，一则是表示被动单元scontext中第三个字段，比如下一个例子中sdcard这个文件的type为sdcard_exec。一则，指的是打标签的关键字，定义domain/type的关键字，比如上面的sdcardd的例子。

attribute: domain/type 的集合，与type/domain 相同命名空间，因为m4就是个宏解释器，attribute就是为一群相同权限或者规则的主动单元或被动单元集合定义了个新名字，这个新名字在sepolicy中被定义为attribute. 在m4编译过程中attribute都会被分解成实际的type/domain，后文会在例子中提到。

```
# 被动单元分组
sdcard_type -|
             |-|- fuse  -|-|
             |-|- vfat  -|-|
               |- sysfs -|-|
               |- tmpfs -|-|
                           |- fs_type

# 主动单元分组，　也会做被动单元，比如被访问，被kill
netdomain -|
           |-|- netd -|-|
           |-|- dhcp -|-|
             |- vold -|-|
             |- logd -|-|
                        |- domain
```

打标签: 就是给被动单元定义type，　给主动单元定义domain． domain只有init是定义的其他都是fork之后通过DT转换的．而type只有已知是定义的，由进程创建的都是通过TT转换的． DT和TT在后面会介绍．

## sepolicy规则介绍[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#sepolicy)

sepolicy的规则针对的是linux系统中的进程和文件。进程是主动的， 而文件是被动的。 所以，有对应的进程规则和文件规则， 分别定义进程的合法行为和文件被访问的权限。

SELinux中， 每个对象（进程和文件）被赋予安全属性，官方说法是 Security Context(以下简称SContext)。 SContext是一个字符串， 对于进程的SContext，SContext的格式是”u:r:type[:range]“. 可以使用 `ps -Z` 获得， 对于文件的SContext， 可以通过 `ls -Z` 获得。 如下为相应命令的输出。

```
# ps -Z
u:r:logd:s0                    logd      198   1     /system/bin/logd
u:r:healthd:s0                 root      199   1     /sbin/healthd
u:r:lmkd:s0                    root      200   1     /system/bin/lmkd
u:r:servicemanager:s0          system    201   1     /system/bin/servicemanager
u:r:vold:s0                    root      202   1     /system/bin/vold
u:r:surfaceflinger:s0          system    203   1     /system/bin/surfaceflinger
u:r:common_time:s0             root      204   1     /system/bin/common_time
u:r:shell:s0                   shell     205   1     /system/bin/sh
u:r:kernel:s0                  root      206   2     kworker/1:1H
u:r:netd:s0                    root      207   1     /system/bin/netd
u:r:debuggerd:s0               root      208   1     /system/bin/debuggerd
u:r:drmserver:s0               drm       209   1     /system/bin/drmserver
u:r:mediaserver:s0             media     210   1     /system/bin/mediaserver
u:r:installd:s0                install   211   1     /system/bin/installd
u:r:keystore:s0                keystore  213   1     /system/bin/keystore
u:r:zygote:s0                  root      214   1     zygote
u:r:sdcardd:s0                 media_rw  215   1     /system/bin/sdcard
u:r:adbd:s0                    shell     216   1     /sbin/adbd
u:r:kernel:s0                  root      228   2     kauditd
```

左边一列是进程的 SContext， 以sdcard进程为例子， 其值为 u:r:sdcardd:s0， 其中：

- u 为 user 的意思。 SEAndroid（指修改了的SELinux） 中只定义了一个SELinux用户， 值为u
- r 为 role 的意思。 role 是角色意思， 它是 SELinux总一种比较高层次， 更方便的权利管理思路， 即 Role Based Access Control（基于角色访问控制， 简称为RBAC， 在后文会详细讨论）。user与role的权限， 简单点说， 就是 u 可以属于多个 role， 然后不同的 role 可以有不同的权限， 就跟一个人可以兼职多份工作一样。
- sdcardd， 代表进程 sdcard 所属的 Domain 为 sdcardd，可以理解为这是一个进程组的名字， 该字符串的名字可以随意， 只要在规则文件中定义好映射关系， 规则文件的说明在稍后讨论。对于进程访问的权限控制， 在linux上， 我们熟知的是， 如果以root权限启动一个进程， 则该进程具有root权限， 这就是root的原因， 该安全模型叫做DAC（Discretionary Access Control）。 而SELinux对于进程访问的控制， 类似白名单机制， 只有写入规则的进程才有对应的访问权限， 所以， 在这种机制下， 即使是root权限的sdcardd， 也无法访问规则， 该安全模型叫MAC（Mandatory Access Control）。而MAC的基本管理单位是 Type Enforcement Access Control (基于类型的强制访问控制，简称TEAC， 也叫TE)， 这些只是概念名字而已。
- S0 是 SELinux为了满足军用和教育行业设计的 Multi-Level Security(MLS)机制有关。MLS将进程和文件进行了分级， 不同级别的资源需要不同级别的进程访问， 后文会介绍。

```
 # ls -Z

 # /
-rw-r--r-- root     root              u:object_r:rootfs:s0 property_contexts
drwxr-xr-x root     root              u:object_r:rootfs:s0 res
drwx------ root     root              u:object_r:rootfs:s0 root
-rw-r--r-- root     root              u:object_r:rootfs:s0 s3g.ko
-rw-r--r-- root     root              u:object_r:rootfs:s0 s3g_core.ko
drwxr-x--- root     root              u:object_r:rootfs:s0 sbin
lrwxrwxrwx root     root              u:object_r:rootfs:s0 sdcard -> /storage/emulated/legacy
-rw-r--r-- root     root              u:object_r:rootfs:s0 seapp_contexts
-rw-r--r-- root     root              u:object_r:rootfs:s0 selinux_version
-rw-r--r-- root     root              u:object_r:rootfs:s0 sepolicy
-rw-r--r-- root     root              u:object_r:rootfs:s0 service_contexts
drwxr-x--x root     sdcard_r          u:object_r:rootfs:s0 storage
dr-xr-xr-x root     root              u:object_r:sysfs:s0 sys
drwxr-xr-x root     root              u:object_r:system_file:s0 system
-rw-r--r-- root     root              u:object_r:rootfs:s0 ueventd.rc
-rw-r--r-- root     root              u:object_r:rootfs:s0 ueventd.zx2000.rc
lrwxrwxrwx root     root              u:object_r:rootfs:s0 vendor -> /system/vendo

# system/bin/
-rwxr-xr-x root     shell             u:object_r:system_file:s0 screenrecord
-rwxr-xr-x root     shell             u:object_r:sdcardd_exec:s0 sdcard
lrwxr-xr-x root     shell             u:object_r:system_file:s0 sendevent -> toolbox
-rwxr-xr-x root     shell             u:object_r:system_file:s0 sensorservice
-rwxr-xr-x root     shell             u:object_r:system_file:s0 service
```

上面是zx2000上，我们以 storage 目录为例子简单看下，信息为 u:object_r:rootfs:s0.

- u 同样是user意思， 代表创建该文件的SELinux user
- object_r: 该字段与 ps -Z 的一样，表示 role，但是文件是被动访问的， 无法称为一个角色， 所以， 所有文件的role都用object_r表示
- rootfs: type, 和 domain 一个意思， 就是一个分类的标签。 所有的文件（包括文件系统）都要么有标签，要么就是unlabeled。
- s0： MLS的级别。

所以，后面会介绍TE， RBAC, MLS 等的规则。

### Labeling介绍（一）[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#labeling)

基于上面的SContext信息，先介绍下打标签， 也就是主动单元的domain和被动单元的type初始化的动作。对于新创建的进程和新创建的文件的SContext，我们会在介绍了TE规则后，再在Labeling介绍（二）介绍。

#### domain初始化[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#domain)

domain跟进程的上下文一样，可以被继承，也可以被改变。所以，它与进程上下文一样，在需要改变的时候，显示地切换，而这个切换动作在sepolicy中定义。所以， 只有init进程有初始的domain，其他进程都是根据DT(Domain Transition)规则切换的，后文会详细介绍。

```
# init.rc
on early-init    
   # Set the security context for the init process.    
   # This should occur before anything else (e.g. ueventd) is started.
   setcon u:r:init:s0
```

这里就将init的domain设置为init。

#### Filesystem/File 的初始化[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#filesystemfile)

上面通过`ls -Z`看到的SContext，文件部分是在`external/sepolicy/file_contexts`中定义的.这个文件最终会作为mkext4fs工具的参数,被设置到system.img中.

```
# 格式: regexp <-type> ( <file_label> | <<none>> )
# <-type> 中的type与 ls -la 的输出的第一个字符匹配.比如:
# -rw-r--r-- 1 root    root    11208 Mar 11 11:13 te_macros
# drwxr-xr-x 3 root    root     4096 Mar 11 11:13 tools
# 则 -- 表示匹配文件， -d 表示匹配目录．
# 因为前面是正则表达式，　所以　<-type>　可以进一步过滤需要的文件类型，　将匹配正则表达式和文件类型打上标签．
/           u:object_r:rootfs:s0 

# Data files
/adb_keys       u:object_r:adb_keys_file:s0
/default\.prop      u:object_r:rootfs:s0


/system(/.*)?       u:object_r:system_file:s0
# 这里的--, 个人理解是，　通过透过软链接，将标签打在实际的文件上．
/system/bin/sh      --  u:object_r:shell_exec:s0
/system/bin/run-as  --  u:object_r:runas_exec:s0

/system/bin/sdcard      u:object_r:sdcardd_exec:s0
```

所有新添加的文件，建议在这边查看下，是否需要设置新的标签．　一般新的可执行程序会需要设置额外的type，并且有xx.te　对应的规则文件和与type对应的domain．

再来看文件系统的标签初始化，这个不好理解，感觉跟内核selinux模块的定义也扯上关系了，以下只是个人理解：

```
# The fs_use_xattr statement is used to allocate a security context to filesystems
# 给文件系统打标签，　该标签是作为 target_type, 会在规则里被使用．
# 比如：vold.te: allow vold labeledfs:filesystem { mount unmount remount };
#      file.te: allow file_type labeledfs:filesystem associate; 
#               允许 file_type 属性的文件在labeledfs类型的文件系统中创建
# 个人理解，这类文件系统上所创建的文件/目录，会继承自父目录规则，同时受TT规则影响。
 fs_use_xattr yaffs2 u:object_r:labeledfs:s0;
 fs_use_xattr jffs2 u:object_r:labeledfs:s0;
 fs_use_xattr ext2 u:object_r:labeledfs:s0;
 fs_use_xattr ext3 u:object_r:labeledfs:s0;
 fs_use_xattr ext4 u:object_r:labeledfs:s0;
 fs_use_xattr xfs u:object_r:labeledfs:s0;
 fs_use_xattr btrfs u:object_r:labeledfs:s0;
 fs_use_xattr f2fs u:object_r:labeledfs:s0;

 #　The fs_use_task statement is used to allocate a security context to pseudo filesystems 
 #　that support task related services such as pipes and sockets.
 # 使用fs_use_task描述的字段只有下面两条，　具体的含义还没理解．
 fs_use_task pipefs u:object_r:pipefs:s0;
 fs_use_task sockfs u:object_r:sockfs:s0;

 #　The fs_use_trans statement is used to allocate a security context to pseudo filesystems 
 #　such as pseudo terminals and temporary objects. The assigned context is derived from 
 #　the creating process and that of the filesystem type based on transition rules.
 # 从描述是给伪文件系统的，　比如／dev/等．
 # 该规则描述了在定义的文件系统下面所创建的文件的SContext，　但该规则又可以被ＴＴ规则影响．比如：
 # type_transition sdcardd devpts:{ chr_file } media_rw_data_file; 如果有这条语句，　则sdcardd
 # 类型的进程的devpts下创建的字符设备文件的SContext为media_rw_data_file；　如果没有这句，则SContext为
 # devpts. 这里的规则和前面目录的规则类似，　但这里是基于文件系统的，　规则继承自文件系统，而不是目录．比如：
 # 如果有修改以上TT的object class 为 dir, 另一进程在sdcardd进程所创建的目录里面所创建的文件，不会继承media_rw_data_file,
 # 其SContext依然为devpts．
 fs_use_trans devpts u:object_r:devpts:s0;
 fs_use_trans tmpfs u:object_r:tmpfs:s0;
 fs_use_trans devtmpfs u:object_r:device:s0;
 fs_use_trans shm u:object_r:shm:s0;
 fs_use_trans mqueue u:object_r:mqueue:s0;
```

上面关于[TT](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#TT)的规则，还有`target_type`的概念，可以在后面介绍了TE语法后，再回过头理解下。以上介绍了文件，文件系统打标签，但是，我们发现，文件系统不完整，起码rootfs和proc都没介绍到，下面我们介绍下， 因为rootfs和proc无法用上面函数打标签(不知道为啥)... 其中一个可能原因是， 这些文件系统的SContext是被定死的，不希望被TT规则改变。使用的关键字是`genfscon`

```
#　格式：　genfscon　fstype partial_path fs_context
# 在fstype为proc时，　partial_path　指定为proc下的路径，其他文件系统统一为 / ．
 # Label inodes with the fs label.
 genfscon rootfs / u:object_r:rootfs:s0

 # proc labeling can be further refined (longest matching prefix).
 genfscon proc / u:object_r:proc:s0
 genfscon proc /net u:object_r:proc_net:s0
```

#### 网络端口/数据包初始化[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#_2)

SEAndroid中没有个数据包和端口打标签．`selinux-network.sh`和`port_contexts`都存在，但规则都注释了，　不确定是否支持．有需求的童鞋验证下．．．

### TE介绍[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#te)

TE就是给上面的domain和type定义访问规则。

先来看下TE的基本格式：

```
rule_name source_type target_type : object_class perm_set;
```

来段[selinux wiki](http://selinuxproject.org/)的解释。

| 域                        | 说明                                                         |
| :------------------------ | :----------------------------------------------------------- |
| rule_name                 | The applicable allow, dontaudit, auditallow, and neverallow rule keyword. |
| source_type / target_type | One or more source / target type, typealias or attribute identifiers. Multiple entries consist of a space separated list enclosed in braces ({}). Entries can be excluded from the list by using the negative operator (-). The target_type can have the self keyword instead of type, typealias or attribute identifiers. This means that the target_type is the same as the source_type. The neverallow rule also supports the wildcard operator (*) to specify that all types are to be included and the complement operator (~) to specify all types are to be included except those explicitly listed. |
| class_object              | One or more object classes. Multiple entries consist of a space separated list enclosed in braces ({}). |
| perm_set                  | The access permissions the source is allowed to access for the target object (also known as the Acess Vector). Multiple entries consist of a space separated list enclosed in braces ({}). The optional wildcard operator (*) specifies that all permissions for the object class can be used. The complement operator (~) is used to specify all permissions except those explicitly listed (although the compiler issues a warning if the dontaudit rule has '~'). |

下面来几个例子来熟悉格式和概念。

```
allow sdcardd rootfs:dir mounton;
```

- allow： TE的allow语句， 表示授权。除了allow之外， 还有allowaudit、dontaudit、neverallow等。
- sdcardd： source type。 也叫 domain。 与上面进程显示的domain一致。
- rootfs： target type。 也就是文件的标签， 与上面文件显示的type一致。
- dir： 代表 Ojbect Class. 它表示能够给domain操作的一类东西。每个文件分类里面可以包含各种不同属性的，比如文件，管道，目录等， 这些是由Object Class定义和区分。在android里，还而外定义了一个Object Class， 叫做Binder。
- mounton： 在该类 Object Class 中所定义的操作。

以上的整句含义是， 允许sdcardd将所有rootfs标签下的目录作为挂载点。

```
 allow vold system_file:file x_file_perms;
# 允许vold域中的进程执行system_file（所有/system/ 和 /vendor/ 目录下）类型的文件。

allow vdc dumpstate:unix_stream_socket { read write getattr };
# 允许vdc域中的进程read write 和 getattr dumpstate标签中unix域的socket。

neverallow netd dev_type:blk_file { read write };
# 不允许netd域的进程读写/dev/底下的块设备文件。
```

之前我们提到， TE是类似白名单形式的，只有被记录的规则才被允许， 未被记录的行为都是拒绝的， 那么neverallow其实是没有意义的了。 其实neverallow的存在是在生成（编译）安全策略文件时检查allow语句是否违反了neverallow，防止由于开发人员的失误导致某些域权限过高。该错误会在编译阶段出错。

#### Object class 和其 Perm_set[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#object-class-perm95set)

```
The object classes have matching declarations in the kernel, meaning that it is not trivial to add or change object class details. The same is true for permissions. Development work is ongoing to make it possible to dynamically register and unregister classes and permissions.
```

这里是摘抄一段CentOS里的介绍， 对于object class和permission的定义的说明， 这两者都是在kernel中定义与映射的， 也就是说， 这两个是跟设备相关的， 不允许随意更改。

首先， Object class 定义在文件external/sepolicy/security_classes， 简单摘取如下。该文件中只是一堆定义， 至于怎么跟linux中实际的文件映射的呢？（请参考：内核代码）

```
# file-related classes
class filesystem
class file
class dir
class fd
class lnk_file
class chr_file
class blk_file
class sock_file
class fifo_file

# Property service
class property_service          # userspace

# Service manager
class service_manager           # userspace
```

所有的 Object class 需要通过class语句申明。

这里userspace，注意下， 后文会提到android里特殊定义的这些userspace的object class，所有标注了userspace的，都是进程运行时通过selinux的标准API动态检查，跟android的xml中permission检查类似。

下面看下 `perm_set`。 所谓`perm_set`也叫做 access vectors， 指某个object class所支持的操作。 该操作都是在kernel里预定义的， 也是无法增加或改变其行为， 但可以将它们与对应的object class 绑定。注意：一些object class会不支持某些permission， 比如 file 不支持 mounton。

这些映射定义在external/sepolicy/access_vectors， 简单摘取如下。

```
 common file
 {
     ioctl
     read
     write
     create
     getattr
     setattr
     lock
     relabelfrom
     relabelto
     append
     unlink
     link
     rename
     execute
     swapon
     quotaon
     mounton
 }

class dir
 inherits file
 {   
     add_name
     remove_name
     reparent
     search
     rmdir
     open
     audit_access
     execmod
 } 
```

`perm_set`的定义有2种， 如上， 一种是common定义的， 类似面向对象的基类， 另一种是class定义的， 可以继承commen定义的集合。

#### type， attribute 和 allow 等关键字说明[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#type-attribute-allow)

首先， 我们看type的定义：

```
type type_id [,attribute_id]
```

上面是type的完整命令格式， 指定`type_id`, 并关联到`attribute_id`， `attribute_id`可以多个。

而SEAndroid的属性定义如下：

```
attribute domain
attribute file_type
```

除了通过type定义时绑定属性， 还可以通过如下， 将vold类型与mlstrustedsubject属性关联起来

```
typeattribute vold mlstrustedsubject;
```

type和attribute关联起来具体是什么含义呢？ 其实， attribute 可以理解为分组的意思， 也就是将一堆的`type_id` 归到不同的组， `type_id` 和 `attribute_id` 位于同一个命名空间， 也就是说， 不能用type定义在attribute中已有的名字， 也不能用attribute定义type中已有的名字。 下面看个例子， 来更深入理解`type_id`和`attribute_id`的关系，读者可以结合下面的例子和开头的树形例子来理解。

```
# 内容来自 dhcp.te 
net_domain(dhcp)

# 内容来自 netd.te
net_domain(netd)

# 内容来自 te_macros, 意思是定义一个宏函数net_domain， 通过typeattribute 将参数 与 netdomain 关联。
#####################################
# net_domain(domain)
# Allow a base set of permissions required for network access.
define(`net_domain', `
typeattribute $1 netdomain;
')

# 内容来自 net.te, 定义了 netdomain 这个attribute所有permissions， 以下简单列出。
allow netdomain self:tcp_socket create_stream_socket_perms;
```

以上例子的含义是， 将 dhcp 与 netdomain关联， 将netd与netdomain关联。 然后只要通过允许netdomain执行某些权限， 就可以做到让dhcp和netd同时具备某些权限。所以， attribute 属性在用于 source_type 时， 是指赋予某一组的`type_id` 权限。 通过m4语法， 以上例子展开的结果是：

```
# 这里的 create_stream_socket_perms 是在global_macros中定义的宏， 被展开就是具体的tcp_socket的permissions
# 这里的 self 就是指与 source_type 一致。
allow dhcp dhcp:tcp_socket { create listen accept ioctl read getattr write setattr lock append bind connect getopt setopt shutdown };
allow netd netd:tcp_socket { create listen accept ioctl read getattr write setattr lock append bind connect getopt setopt shutdown };
```

再来看一个，同样是netdomain， 但是作为`target_type`的例子

```
allow netd netdomain:{tcp_socket udp_socket rawip_socket dccp_socket tun_socket} {read write getattr setattr getopt setopt};

# m4 展开， 这里只定义了dhcp和netd属于netdomain， 实际上android中还有好多网络服务属于该domain
allow netd {dhcp netd}:{tcp_socket udp_socket rawip_socket dccp_socket tun_socket} {read write getattr setattr getopt setopt};
```

这句的意思是， 允许netd对所有netdomain属性成员的{tcp_socket udp_socket rawip_socket dccp_socket tun_socket} 执行 {read write getattr setattr getopt setopt}. 这里的{}是集合的意思。`source_type`, `target_type`, `object class`和`perm_set` 都可以用集合表示， 而attribute，其实是给某个集合定义了个宏别名。

所以， attribute 是便利开发人员写sepolicy的工具。对于所以SEAndroid中定义的attribute， 可以参考 external/sepolicy/attribute 这个文件。

最后， 我们看TE中的`rule_name`， 一共有如下4种：

- allow: 赋予某项权限
- allowaudit： audit含义就是记录某项操作。 默认情况下是 SELinux 只记录哪些权限检查失败的操作， 也就是终端和logcat中打印的所有deny的打印。而该字段就是在allow的基础上， 再将信息打印出来。
- dontaudit： 对那些检查失败的不做记录， 静默地拒绝访问， 并且不应该引起程序退出。该字段在SEAndroid中并未使用。基于SELinux的白名单原则， 只要不在规则内的操作都拒绝， 所以该字段的实际效果就是，对其后失败的权限不做记录。
- neverallow： 用来检查安全策略中是否违反该规则的allow语句， 避免sepolicy的书写异常。 在编译阶段报错， 不会编译进最终的策略文件中。

#### RBAC 和 constrain[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#rbac-constrain)

前文我们提到的都是TEAC。在第一个例子中，我们通过`ps -Z` 看到了user和role， 在SEAndroid中， 只有1个user和1个role。而基于role的安全策略， 就叫做RBAC（Role Based Access Control）。我们先来看下android定义的user和role。

```
# external/sepolicy/roles
# 定义一个role

role r;
# 将role和attribute domain 关联。
role r types domain;
# external/sepolicy/users
user u roles { r } level s0 range s0 - mls_systemhigh;
```

以上是支持MLS（Multi-Leve Security）的user定义。上面这个定义的意思是， 将user u和 roles r关联， 并且其安全级别是s0， 最高是mls_systemhigh。 这里u可以跟多个role关联。

然后， 我们看下user和role有怎样的权限控制。 其实通俗地讲， user和role的关系， 就跟人与工作的关系， role决定了职能分类。因为android只有一个role， 所以，后文提到的role转换和控制关系， 我们只是简单说明下， 我也不是很懂。

首先， 我们看如何从一个role切换到另一个role。

```
# 这里的allow和TE的allow不同
allow from_role_id to_role_id
```

角色之间的关系， 在SELinux中， Role和Role的关系跟职场的管理人员层级一致。例如

```
# 这句的意思是， super_r dominate sysadm_r 和 secadm_r 这两个角色
# 从 type 角度来看， super_r 将自动继承 sysadm_r 和 secadm_r 所关联的type(或attribute)
dominance { role super_r {role sysadm_r; role secadm_r; }}
```

接下来， 我们看下， 是如何实现基于Role或User的权限控制的。在selinux中有新关键词constrain。

```
constrain file write (u1 == u2 and r1 == r2);
# 格式：
# constrain object_class perm_set expression；
```

重点是expression。它包含如下关键字：

- u1,r1,t1: 代表source的user， role 和 type
- u2, r2, t2: 代表target的user， role 和 type
- == 和 ！= ： 对于 u，r 来说， == 和 ！= 分别表示相等或者不等。 而对于 t 来说， == 和 ！= 分别表示源type属于或不属于目标attribute。

在SEAndroid， 并没有使用constrain关键字， 而是mlsconstrain。后文在介绍mls时会详细提到。

constrain是对TE的加强。因为TE仅针对type和domain，并没有针对user和role。在selinux检查权限时， 先检查TE， 再检查RBAC。

### Labeling 介绍（二）[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#labeling_1)

#### domain/type Transition 宏 和 新添加进程[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#domaintype-transition)

在Android/Linux系统中， 进程都是由父进程fork生成的。在Android中， 所有的应用都是通过zygote创建，并执行相同的程序， 只是最后加载的java包不同而已。而fork系统调用，会使子进程继承父进程的domain， 也就是说SContext会被继承。所以， 对于init进程而言，必须完成type/domain的转换，从而降低子进程的权限。而对于zygote而言， 由于不同应用只是资源不同，对于内核而言是同一种进程， 所以需要显示调用selinux的函数进行type/domain转换。下面针对init进程的fork和zygote进程的fork说明下域是如何转换的。

------

##### INIT 启动进程并切换DOMAIN[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#init-domain)

init有自己的scontext， 并且查看init.te， 会发现其权限非常高。 而由init.rc中启动的进程，具有各自不同的权限，应该运行在各自的scontext中，降低权限。

init启动子进程经历的系统调用为， fork， execv， 在这个过程中， 内核会有3个Security检查点， 分别是， 允许init执行目标程序， 允许init执行DT（Domain Transition）转换， 通知selinux针对的切换文件。即如下3条指令：

```
# 来源 external/sepolicy/init.te
# 格式 domain_trans(olddomain, type, newdomain)
# shell 的 type 和domain， 可以看 shell.te
# "
# type shell, domain, mlstrustedsubject;  # shell是domain这个attribute的成员。
# type shell_exec, exec_type, file_type;  # type 是 shell_exec
# "
domain_trans(init, shell_exec, shell)

# 来源 external/sepolicy/te_macros
define(`domain_trans', `
# $1 为init， $2 为 shell_exec， $3为shell
allow $1 $2:file { getattr open read execute };
allow $1 $3:process transition;
allow $3 $2:file { entrypoint open read execute getattr };
...
')

# domain_trans 展开来如下，去除无关permissions， domain 切换相关的如下：
# 允许 init域进程 执行 shell_exec 类型的进程
allow init shell_exec:file { execute };
允许init域进程对shell域的进程执行DT
allow init shell:process transition;
# 设置新domain shell的入口为类型 shell_exec 的文件。
allow shell shell_exec:file { entrypoint execute };
```

对应的type可以在file_contexts 中查找， 当然，如果是新添加进程，则需要在该文件中绑定可执行程序与type。 以上(domain_trans宏)只是申明了可以进行DT的权限，但并没有真正执行转换。

```
# external/sepolicy/file_contests
# 绑定system底下所有文件为 system_file
/system(/.*)?       u:object_r:system_file:s0
# 绑定vold可执行程序的type为vold_exec。
/system/bin/vold    u:object_r:vold_exec:s0
```

一般涉及到新启进程，和domain转换的话， 用到的宏如下：

```
# 从非init进程启动一个新进程， 在父进程的sepolicy中调用， 这里的olddomain为父进程的domain， type为子进程的type， newdomain为子进程的domain。
# external/sepolicy/te_macros
# domain_auto_trans(olddomain, type, newdomain)
define(`domain_auto_trans', `
# Allow the necessary permissions.
domain_trans($1,$2,$3)
# Make the transition occur by default.
# 这句是真正进行转换，而且是自动的...
type_transition $1 $2:process $3;
'

# 从init进程启动一个新进程， 在子进程的sepolicy中调用。这里的domain为子进程的domain
# init_daemon_domain(domain)

define(`init_daemon_domain', `
domain_auto_trans(init, $1_exec, $1)
tmpfs_domain($1)
')
```

以上提到的在哪个sepolicy中调用，其实对于最终的规则文件没有影响， 区分不同的sepolicy文件，只是属于开发人员的分类和易于维护。 你完全可以在vold.te 中写个规则允许sdcardd类型的进程执行某个操作， 该规则依然会生效。

另外 ，从上面这个宏，我们可以看到Android中的一个命名习惯，一般domain加上后缀_exec就是关联的type。

```
type  shell domain;
type  shell_exec exec_type file_type;
```

然后，我们看下， 在init.te中，存在domain_trans的声明，如果再看init_shell.te的内容的话，我们会发现存在DT的冲突（第一次看的时候）：

```
# init_shell.te
# 自动从init切换到init_shell当执行的程序是shell_exec,因为该宏包含了type_transition
# 这个te是给所有从init.*.rc中启动的脚本定义的
domain_auto_trans(init, shell_exec, init_shell)
# init.te
# 与上面类似，少了type_transition, 也就是说不是自动切换, 只是申明了权限。
# 这个是给init.rc中console服务定义的
domain_trans(init, shell_exec, shell)
```

在看init.rc，有如下内容：

```
service console /system/bin/sh
    class core
    console
    disabled
    user shell
    group shell log
    seclabel u:r:shell:s0
```

也就是说，init显示切换了sh的domain。 所以，个人理解是，sh启动的时候，先默认切换到init_shell，然后被init进程切换到shell。 这么理解的话，type_transition的声明不能有冲突。（未验证）

------

##### ZYGOTE 启动进程并切换DOMAIN[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#zygote-domain)

首先， 我们已经知道， 所有的app和framework server都是zygote通过fork的形式创建的。下面简单看下这个函数。

```
static pid_t ForkAndSpecializeCommon(JNIEnv* env, uid_t uid, gid_t gid, jintArray javaGids,
                                     jint debug_flags, jobjectArray javaRlimits,
                                     jlong permittedCapabilities, jlong effectiveCapabilities,
                                     jint mount_external, 
                                     jstring java_se_info, jstring java_se_name,
                                     bool is_system_server, jintArray fdsToClose, 
                                     jstring instructionSet, jstring dataDir) { 
 pid_t pid = fork();
 if (pid == 0) {
  // ....
   rc = selinux_android_setcontext(uid, is_system_server, se_info_c_str, se_name_c_str);
  // ....
}                               
```

这段代码设置进程上下文的核心参数是 `is_system_server` 和 `se_info_xxx`。

```
int selinux_android_setcontext(uid_t uid,
       int isSystemServer,
       const char *seinfo, 
       const char *pkgname)
{
// ....
rc = seapp_context_lookup(SEAPP_DOMAIN, uid, isSystemServer, seinfo, pkgname, NULL, ctx); // seinfo is se_info_c_str and pkgname is se_name_c_str
// ....
}
```

`seapp_context_lookup` 这个函数的任务就是根据参数找到对应该app/server的规则，然后设置安全上下文。如果想详细了解查找规则， 可以看下具体实现。下面简单介绍下，对于由zygote创建的app/server的规则文件。

该函数是基于文件 external/sepolicy/seapp_contexts 查找对应应用的进程域和文件type。

```
 isSystemServer=true domain=system_server
 user=system domain=system_app type=system_app_data_file
 user=bluetooth domain=bluetooth type=bluetooth_data_file
 user=nfc domain=nfc type=nfc_data_file
 user=radio domain=radio type=radio_data_file
 user=shared_relro domain=shared_relro
 user=shell domain=shell type=shell_data_file
 user=_isolated domain=isolated_app
 user=_app seinfo=platform domain=platform_app type=app_data_file
 user=_app domain=untrusted_app type=app_data_file
```

举个例子， 如果 isSystemServer 为 true， 则domain为`system_server`。 如果user是`_app`， 并且签名是platform（从源码编译的应用）， 则domain是`platform_app`， 对应的文件type为`app_data_file`。 如果是第三方应用， user也为`_app`， 但因为不满足platform签名，所以， 域是`untrusted_app`。除了user固定，其余的字段都是字符串，只要匹配就行。比如domain要跟xx.te中的匹配， type同理。seinfo只要跟后文的`mac_permissions.xml`匹配。

上面的例子中出现了seinfo， 这个信息是存放在external/sepolicy/mac_permissions.xml, 内容如下。定义了签名的key与seinfo值的关系。

```
<policy>
    <!-- Platform dev key in AOSP -->
    <signer signature="@PLATFORM">
      <seinfo value="platform"/>
    </signer>
    <!-- All other keys -->
    <default>
      <seinfo value="default"/>
    </default>
</policy>
```

该文件是由pkms读取，并在安装应用时，立即给被安装的应用分配seinfo信息。上面的只是一个版本，简单看了下pkms的实现， 可以做到如下的方式：

```
<policy>
    <!-- Platform dev key in AOSP -->
    <signer signature="@PLATFORM">
       <package name="com.abc.d">
         <seinfo value="platform"/>
       </package>
    </signer>
    <!-- All other keys -->
    <default>
      <seinfo value="default"/>
    </default>
</policy>
```

也就是说， 既可以基于签名， 也可以更详细的根据包名，再指定更细致的seinfo分类。当然必须在`seapp_contexts`中添加相应的规则，并且参考`system_server.te`添加对应域的权限控制。

以上`seapp_contexts`中domain的值，都可以在external/sepolicy/xxx.te 中找到， 详细的可以自行查看。

对于新添加的一个应用，就可以基于以上信息，通过pkms添加相应规则。

但是对于新添加一个服务， 则需要在external/sepolicy/service_context.te 或者 external/sepolicy/service.te 中添加在`service_manager`注册的名字和对应的域/类型， 否则`service_manager`会拒绝注册。同样，如果不将新添加的服务关联到`service_manager_type`中， 就无法被查找和获取。

```
# external/sepolicy/service.te

 type surfaceflinger_service,    service_manager_type;
 type system_app_service,        service_manager_type;
 type system_server_service,     service_manager_type;
```

将不同的type都跟`service_manager_type`属性关联， 后面会使用该属性进行权限控制。

```
# external/sepolicy/service_contexts
SurfaceFlinger                            u:object_r:surfaceflinger_service:s0
display.qservice                          u:object_r:surfaceflinger_service:s0
window                                    u:object_r:system_server_service:s0
*                                         u:object_r:default_android_service:s0
```

这个文件的规则与file_contexts类似，关联了服务与{user， role， type， level}。最后 * 是匹配所有以上规则无法匹配的服务， 其type为 default_android_service。

下面我们看下，`service_manager`的权限控制。

```
# domain.te
# 不允许service_manager对default_android_service属性的服务执行add操作。非规则，编译保护。
neverallow domain default_android_service:service_manager add;

# 允许domain域的进程请求service_manager执行find操作。
allow domain service_manager_type:service_manager find;
```

我们前面的例子看到， 每个te规则文件开头都会把该类型与domain域关联，所以，实际上，这里是允许了所有有规则的进程请求`service_manager`操作。该object class 和 `perm_set`， 是android新添加的，在前文提到属于userspace， 在service manager的代码中， `svc_can_xxx` 函数就是在用户层检查该规则是否满足。未仔细研究，有兴趣的可以看下。

上面介绍了创建进程和DT, 是针对进程的,下面介绍下TT,针对文件的,同样在创建文件的时候,需要指定type.同样用到的也是`type_transition`.

```
define(`file_type_trans', `
# Allow the domain to add entries to the directory.
allow $1 $2:dir ra_dir_perms;
# Allow the domain to create the file.
allow $1 $3:notdevfile_class_set create_file_perms;
allow $1 $3:dir create_dir_perms;
')


 #####################################
 # file_type_auto_trans(domain, dir_type, file_type)
 # Automatically label new files with file_type when
 # they are created by domain in directories labeled dir_type.
 #
 define(`file_type_auto_trans', `
 # Allow the necessary permissions.
 file_type_trans($1, $2, $3)
 # Make the transition occur by default.
 type_transition $1 $2:dir $3;
 type_transition $1 $2:notdevfile_class_set $3;
 ')
```

匹配进程的domain和目录的type的情况下所创建的文件,其SContext(安全上下文)就会被指定为`file_type`. android中并没有在使用这两个宏,也就是说使用了默认的规则, 也就是继承父目录的SContext.上文的filesystem打标签中提到过TT，`genfscon`能够禁制TT规则，强制将所有文件的SContext指定为需要的。还有一个`fs_use_trans`， 其默认规则不是继承父目录的规则，而是继承文件系统的规则。[文件系统标签初始化](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#fslabel).

### MLS(Multi-level Security)[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#mlsmulti-level-security)

这东西不好理解，　在android中，基本也不会改，　把我的理解简单介绍下．安全分级就跟保密分级一样，对主动单元和被动单元都有相同的分级．而高级别的主动单元可以读取低级别的被动单元，但不允许往地级别的被动单元写数据，防止泄密．而低级别的主动单元可以往高级别的被动单元写数据但不能读取高级别被动单元．形象点描述就是 no write down 和　no read up.

我们来看个格式，在未启用MLS和启用了MLS的SContext格式差异：

```
# 未启用MLS
user_u:role_r:type_t

# 启用了MLS
# - 表示范围
# 左侧，我们称为最低安全级别，也是当前主动单元／被动单元的级别
# 右侧，我们称为最高安全级别，也就是当前主动单元／被动单元可能获得的最高级别
user_u:role_r:type_t:sensitivity[:category...]-sensitivity[:category...]
```

结合开头的例子，android是启用了MLS，但是，如果把所有的规则过一遍，就会发现所有的sensitivity都为s0,　所以，虽然启用了，但并没有分级, 也没有分类(category)．　所以，　关于这块，我们也是简单介绍下，可能有理解不到位．

如果出现分级和分类，　会使用 level　关键字定义:

```
level s0:c0.c255  #表示s0, category从c0一直到c255
```

分级有高低， s0 < s1，　分类没有高低，只有包含，　比如 c0.c255　包含 c10.c25. 个人感觉这块的功能是对Role的强化，　更细致的阶级关系．

下面看个例子来辅助理解．

```
 # Datagram send: Sender must be dominated by receiver unless one of them is
 # trusted.
 mlsconstrain unix_dgram_socket { sendto }
          (l1 domby l2 or t1 == mlstrustedsubject or t2 == mlstrustedsubject);
# mlstrustedsubject 是attribute
```

首先，android中主要用到了mlsconstrain, 其语法如下，　与constrain一样：

```
mlsconstrain object_class perm_set expression
```

expression有u1, u2, r1, r2, t1, t2, l1, l2, h1, h2 跟Role的权限控制很像, 只是多了l1, l2, h1, h2：

- l1, h1, 表示source的low sensitivity level, high sensitivity level
- l2, h2, 表示target的low sensitivity level, high sensitivity level
- 关系：
- dom: l1 dom l2, 表示l1 sensitivity >= l2 sensitivity, l1的category包含l2的category
- domby: 跟dom相反
- eq: sensitivity 相等，　category　相等
- incomp: 不可比．具体含义未知...

### 规则文件关系总结[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#_3)

`file_contexts`: 关联文件系统上文件与type， 或者说，指定文件属于某个type。被动单元的scontext。比如：

```
# netd属于netd_exec。所有要执行netd进程的程序必须申请 netd_exec 的 execute 权限。

/system/bin/netd    u:object_r:netd_exec:s0
```

`*.te`: TE权限规则文件。指定了每个domain的权限，同时也指定了不同domain的入口。比如上文提到的`init_daemon_domain`, 就指定了对应domain的入口为某个type。几乎所有该文件的开头都会与domain关联， 也就是说都属于domain这个属性。

```
# 指定了domain为shell的入口是shell_exec， 也就是绑定了type和domain的关系。
allow shell shell_exec:file { entrypoint execute };
```

------

从上面两类文件，就说明了指定的二进制文件和对应的安全上下文是如何关联的。所以， 如果新添加进程， 必须动上面提到的文件， 才能正确设置指定进程的安全上下文。

------

`mac_permissions.xml`： pkms解析的文件，描述了seinfo字段与签名/包名的关系。

`seapp_contexts`： zygote解析， 用于根据user和seinfo， 确定应用或系统服务的domain和type。

所以， 对于有特殊权限需求的应用， 需要同时增加上面两个文件，当然TE的规则，需要修改或增加te文件。

------

`service_contexts`： 类似`file_contexts`文件， 关联了android系统的服务与type。 该文件的内容由service manager在运行时通过selinux的接口动态检查权限。

`service.te`: 将不同类型的服务与`service_manager_type` 关联。

如果新添加framework的服务， 必须修改这两个文件，否则无法注册service manager， 无法被获取bp。

------

`file.te`　所有跟文件和文件系统相关的分组的标签(type).如果涉及到新添加文件系统或者新的/data/底下目录权限，建议在这个文件里将其与相关的type关联，否则可能导致某些系统服务无法访问或者文件无法创建。

------

`tools/` 一些检查和分析工具， 都是基于语法类的，还有几个是针对应用的规则生成和编辑工具，未研究代码。

## device 相关sepolicy修改的方法[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#device-sepolicy)

路径： 由 BoardConfig.mk 中的 BOARD_SEPOLICY_DIRS 定义

文件： 由 BoardConfig.mk 中的 BOARD_SEPOLICY_UNION

device底下的sepolicy不是overlay， 而是会与external/sepolicy的规则合并。 所以， 可以在device底下创建同名文件，添加设备相关的规则。

比如， 添加vold.te， 内容如下， 赋予vold类型的进程执行ntfs3g_exec类型的程序，并自动切换domain。（ntfs3g_exec类型和domain在后面介绍）

```
 domain_auto_trans(vold, ntfs3g_exec, ntfs3g)
 allow vold ntfs3g_exec:file rx_file_perms;
```

如果是新添加进程和sepolicy， 则额外需要在file_context中将可执行程序和type绑定。

```
# device/s3graphics/zx2000/sepolicy/file_contexts
/system/bin/ntfs-3g u:object_r:ntfs3g_exec:s0
```

## SELinux 的调试和错误分析说明[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#selinux)

第三方工具： [apol](https://github.com/TresysTechnology/setools3/wiki) , 用于分析最终生成的sepolicy。

------

external/sepolicy/tools 下面有一些工具，但缺少使用文档，可以看源码研究。

------

对于由于selinux的权限问题导致运行异常，可以在对应的te文件中加入如下内容, 将对应进程设置为permissive，在运行后，终端会输出所有selinux的警告，但程序可以正常运行。基于锁输出的警告，设置对应的规则。

```
permissive $domain;
type=1400 audit(946684810.610:4): avc: denied { write } for pid=707 comm="m.coship.hotkey" name="property_service" dev="tmpfs" ino=7244 scontext=u:r:platform_app:s0 tcontext=u:object_r:property_socket:s0 tclass=sock_file permissive=1
perm_set` 为 `{ write }`， 程序为`m.coship.hotkey`， `target class`为 `sock_file`，`source context`为 `u:r:platform_app:s0`， `target context`为 `u:object_r:property_socket:s0
```

上面将TE规则的4个相关字段都分析了， 只要添加相应的规则就行。看下面te规则。

```
# - 是排除的意思
# 不合适的改法： 添加 -platform_app。 然后再添加 allow platfor_app property_socket:sock_file write；
 neverallow { appdomain -bluetooth -radio -shell -system_app -nfc }
     property_socket:sock_file write;
```

不过，这个错误由于是app， 所以，不适合直接添加到`platform_app`这个域， 因为会对所有从源码编译的应用产生影响。如果需要，可以额外设置一个seinfo。

------

如果SContext中出现`unlabeled`， 则表面该文件/目录/文件系统未打标签，参考以上介绍在对应文件内添加标签。

------

如果是修改打标签的文件，编译后，system.img需要重新刷，如果是修改TE的规则文件，编译后，只需要重新刷boot.img

## 实际项目中遇到的问题和解决方案[¶](https://pengzhangdev.github.io/SEAndroid%E8%A7%84%E5%88%99%E4%BB%8B%E7%BB%8D/#_4)

- 在Android中, 理论上格式化分区会导致所有文件的scontex相关信息丢失, 而如果需恢复(比如格式化userdata后), 需要在init.rc中显示调用`restorecon_recursive`, 以恢复指定目录的secontext.
- 上文只提到了Android中的常见labeling方法, 在实际项目中, 出现了需要对ext4文件系统等的外部存储挂载并控制权限. 需要动态地指定secontex, 这里就使用了 mountpoint labeling 方法(直接google该关键字). 其使用场景是同一文件系统在不同挂载点可以有不同的secontext.相关代码如下:

```
int Ext::doMount(const char *fsPath, const char *fstype, const char *mountPoint,
                 unsigned long fsFlags, int ownerUid, int ownerGid, int permMask)
{
    int rc;
    // labeling mountpoint for ext fs when mounting udisk. man 8 mount for more options
    const char *mountoption = "context=u:object_r:extfs:s0";
    unsigned long mountflags = MS_NOATIME | MS_NODEV | MS_NOSUID | MS_DIRSYNC;
    unsigned long remountflags = mountflags | fsFlags;
    mountflags |= fsFlags;

    if (mountflags & MS_RDONLY) {  // readonly
        // Mount as writable so that we can update the Uid/Gid and permission
        mountflags &= ~MS_RDONLY;
    }

    rc = mount(fsPath, mountPoint, fstype, mountflags, mountoption);
    if (rc && errno == EROFS) {
        SLOGE("%s appers to be a read only filesystem - retrying mount RO", fsPath);
        mountflags |= MS_RDONLY;
        rc = mount(fsPath, mountPoint, fstype, mountflags, mountoption);
    }

    if (rc == 0) {
        // mount success, remount to the mount flags we want
        chmod(mountPoint, 0770);
        chown(mountPoint, ownerUid, ownerGid);
        SLOGI("remount as user option");
        rc = Ext::remount(mountPoint, remountflags);
    }

    if (rc) {
        SLOGE("%s remount to user option failed - retrying mount with default option\n", fsPath);
        rc = mount(fsPath, mountPoint, fstype, mountflags, mountoption);
    }

    // Dirty Patch : fix permission of pvr files
    fixPermission(mountPoint);
    // Dirty Patch end

    return rc;
}
```

https://pengzhangdev.github.io/SEAndroid规则介绍/

