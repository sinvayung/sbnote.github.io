# SELinux文件访问安全策略和app权限配置

```
Android开发
```

------



# 基于android6.0版本的SELinux文件访问安全策略

在android6.0以后的版本，google采用了SELinux的文件访问安全策略，想比较以前，绝对提高了文件的安全，不像以前那样， 
对文件访问可以是无条件的。本篇文章就分享下常用的一些安全策略。



## 1.linux传统设备文件访问控制方法

传统的 Linux设备文件访问控制机制通过设置用户权限来实现.

- 超级用户（root），具有最高的系统权限，UID为0。
- 系统伪用户，Linux操作系统出于系统管理的需要，但又不愿赋予超级用户的权限，需要将某些关键系统应用文件所有权赋予某些系统伪用户，其UID范围为1～ 499，系统的伪用户不能登录系统。
- 普通用户，只具备有限的访问权限，UID 为 500 ～ 6000，可以登录系统获得shell。在Linux权限模型下，每个文件属于一个用户和一个组，由UID与GID标识其所有权。针对于文件的具体访问权限定义为可读(r)、可写(w)与可执行(x)，并由三组读、写、执行组成的权限三元组来描述相关权限。 
  第一组定义文件所有者（用户）的权限，第二组定义同组用户（GID相同但UID不同的用户）的权限，第三组定义其他用户的权限（GID与UID都不同的用户）。



## 2.SElinux采用主体对客体的强制访问控制

SELinux 拥有三个基本的操作模式

- Disabled：禁用SELinux策略
- Permissive：在Permissive模式下，SELinux会被启用但不会实施安全性策略，而只会发出警告及记录行动。Permissive模式在排除SELinux的问题时很有用.
- Enforcing：这个缺省模式会在系统上启用并实施SELinux的安全性策略，拒绝访问及记录行动. 
  adb shell getenforce 查看selinuc模式 
  adb shell setenforce 0 命令进入permissive模式 
  adb shell setenforce 1 命令进入Enforcing模式



## 3.类型强制(TE)访问控制

```
在SELinux中，所有访问都必须明确授权，SELinux默认不允许任何访问，不管Linux用户/组ID是什么。这就意味着在SELinux中，没有默认的超级用户了，与标准Linux中的root不一样，通过指定主体类型（即域）和客体类型使用allow规则授予访问权限，allow规则由四部分组成：
```

- 源类型（Source type(s) ） 通常是尝试访问的进程的域类型
- 目标类型（Target type(s) ） 被进程访问的客体的类型
- 客体类别（Object class(es)） 指定允许访问的客体的类型
- 许可（Permission(s)）象征目标类型允许源类型访问客体类型的访问种类

举例如下: 
![此处输入图片的描述](http://blog.chinaunix.net/attachment/201609/2/7213935_1472782105wTR1.png)

这个规则解释如下： 
拥有域类型user_t的进程可以读/执行或获取具有bin_t类型的文件客体的属性.



## 4.如何排除SELinux安全策略引起的问题

a. 首先排除DAC权限的问题，使用“ls –l”检查相关文件的属主和权限。如果DAC的权限许可，则就是SELinux的策略显式地拒绝了当前操作的执行。 
b. 通过“setenforce 0”命令进入permissive模式（getenforce命令查看模式）。此操作可暂时关闭selinux强制访问控制，可直接进行调试，若此时操作还是不允许,则与selinux无关。 
c. 通过“adb shell dmesg | grep avc > avc_log.txt”查看 AVC log，在android6.0 版本中，这个用的最多。从分析失败操作相应的AVC Denied Msg入手区分问题的根源，以下为一条拒绝信息： 
d. 使用 external/selinux/prebuilts/bin/audit2allow tool 直接生成policy. 



```
audit2allow -i avc_log.txt  
```

即可自动输出生成的policy

![此处输入图片的描述](http://blog.chinaunix.net/attachment/201609/2/7213935_1472782299ZQBs.png) 
可在/device/qcom/sepolicy/common/untrusted_app.te文件中增加如下语句解决此问题: 
allow untrusted_app sysfs_irdev : file { write };



------



# SELinux app权限配置



## 1.SEAndroid app分类

SELinux(或SEAndroid)将app划分为主要三种类型(根据user不同，也有其他的domain类型)：

1)untrusted_app 第三方app，没有Android平台签名，没有system权限 
2)platform_app 有android平台签名，没有system权限

3)system_app 有android平台签名和system权限

从上面划分，权限等级，理论上：untrusted_app < platform_app < system_app

user=system seinfo=platform，domain才是system_app

user=_app，可以是untrusted_app或platform_app，如果seinfo=platform，则是platform_app。

- Android.mk 有定义LOCAL_CERTIFICATE := platform，则为platform_app
- 且AndroidManifest.xml 有定义android:sharedUserId="android.uid.system"，则为system_app

app对应的te文件

- system_app -> external\sepolicy\system_app.te
- untrusted_app -> external\sepolicy\untrusted_app.te
- platform_app -> external\sepolicy\platform_app.te

https://www.zybuluo.com/guhuizaifeiyang/note/772144