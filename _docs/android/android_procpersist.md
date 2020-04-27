---
title: Android_常驻进程（杀不死的进程）
description: Android_常驻进程（杀不死的进程）
---

# Android_常驻进程（杀不死的进程）

​        Android常驻进程，就是要让进程在内存中永远存在，让进程保活，不被杀死。可能这时都会喷，这不是流氓软件吗？刚接触android的时候，我也是认为这是很流氓的做法，可是慢慢发现很多场景（应用），要为用户服务，就必须用到常驻进程，就好像[微信](https://www.baidu.com/s?wd=%E5%BE%AE%E4%BF%A1&tn=24004469_oem_dg&rsv_dl=gh_pl_sl_csd)，QQ，360安全[手机卫士](https://www.baidu.com/s?wd=%E6%89%8B%E6%9C%BA%E5%8D%AB%E5%A3%AB&tn=24004469_oem_dg&rsv_dl=gh_pl_sl_csd)这些现在比较火，比较常用的软件来说，他们都是实现了常驻进程的。所以说，有时候常驻进程在开发中是必须的，比如锁屏应用，就必须在进程中接收锁屏的广播，因此要保证进程常驻，像QQ,微信那些IM类应用，也需要长期在后台维护一个长链接，因此进程常驻又是必须的！

​        因为最近开发的应用需要用到常驻进程，因此一开始的猜想在java层是不能解决的，必须得在native解决，可是现在对linux和android系统理解还不够深入，而且ndk开发才刚入门，因此在网上搜了一大堆资料，总得来说，给出的解决方法不就外乎下面的几种：

**1、将Service设置为前台进程**
       相关资料和Demo可以查看之前的博客：<http://blog.csdn.net/Two_Water/article/details/52084372>

​       本质是修改了Service所在进程的进程优先级。有了前台进程的优先级，在android系统清理内存的时候，他被杀死的优先级仅高于前台的activity，也就是正在和用户交互的页面，而且使用ddms杀进程他也可以自己启动起来。首先ddms杀进程和在系统设置的正在运行中杀进程本身就不具威胁，在系统设置的所有应用中选择强行停止，仍然可以强停掉，360，cm等软杀更是能[轻而易举](https://www.baidu.com/s?wd=%E8%BD%BB%E8%80%8C%E6%98%93%E4%B8%BE&tn=24004469_oem_dg&rsv_dl=gh_pl_sl_csd)杀死他。而且他还有一个缺点，在api17以上，设置了一个前台服务，他会以一个无法消除的notification的样式出现在用户的手机状态栏里，大大降低了用户体验。可是前台服务适合做一些音乐播放器，天气类的应用！

2、在service的onStartCommand方法里返回 STATR_STICK
       主要的几个返回值：
       1. START_STICKY_COMPATIBILITY：START_STICKY的兼容版本，但不保证服务被kill后一定能重启。 
       2. START_STICKY：系统就会重新创建这个服务并且调用onStartCommand()方法，但是它不会重新传递最后的Intent对象，这适用于不执行命令的媒体播放器（或类似的服务），它只是无限期的运行着并等待工作的到来。
       3. START_NOT_STICKY：直到接受到新的Intent对象，才会被重新创建。这是最安全的，用来避免在不需要的时候运行你的服务。
       4. START_REDELIVER_INTENT：系统就会重新创建了这个服务，并且用最后的Intent对象调。等待中的Intent对象会依次被发送。这适用于如下载文件。

​       测试的service是一个最基本的service，在相应的生命周期的触发函数上做了输出。在普通的服务使用还是可以的，做常驻进程的话就不行了，force close和一些清理软件很容易就清理掉!

**3、添加Manifest文件属性值为android:persistent=“true”**
       app.persistent = true不仅仅标志着此apk不能轻易的被kill掉，亦或在被kill掉后能够自动restart，并且还涉及到了进程的优先级。将被设置为CORE_SERVER_ADJ，此值为-12，而核心进程init的值为-16。当前正在前台运行的进程的值为0。如果应用能设置这个属性，那就真的可以做到保活，因为他真的可以杀不死，像系统的keyguard进程，media进程，且这些进程的adj都是负数，代表了前台activity黑屏了他们也不会死。但是这个属性需要系统shareuid，然后编译不过，因为需要系统签名！
因此，要弄这个属性需获取两个关键的信息： 
       (1).在apk的AndroidManifest.xml文件中设置android:persistent=true 
       (2).此apk需要放入到system/app目录下，成为一个systemapp

​       最主要的是让程序成为系统程序，这个可以做到吗？如果你技术过硬是可以尝试下的！首先弄个自动root的apk，加壳放到程序中，然后程序运行的时候，自动运行自动root的apk，获取root权限，然后在native层中，使用命令的方式把程序移到system/app目录下，成为系统程序！

**4、覆写Service的onDestroy方法**

​      在设置里面的正在运行，注意是正在运行里面，点击关闭，会走onDestroy回调方法，你在这里可以把自己启动起来。注意是正常关闭的时候是会自己启动起来，可是使用第三方的清理软件360，root过的360，force close这些来搞，压根不会走到onDestory的方法，例子在之前service的博客中也有！可以去试试的!

**5、添加广播监听android.intent.action.USER_PRESENT事件以及其他一些可以允许的事件**
       android.intent.action.USER_PRESENT，这是一个android解锁的广播事件。注意，这不是SCREEN_ON\SCREEN_OFF广播，,这不是SCREEN_ON\SCREEN_OFF广播，这不是SCREEN_ON\SCREEN_OFF广播。这是一个可以静态注册的广播。所以在manifest里面注册之后不需要任何前提，理论上用户每次开屏解锁都会触发我们的onReceive事件，在这里我们可以检查进程服务是否在，不在就拉起来。
但是，这个事件只有解锁才有，如果用户的没有设置锁屏，那么这个事件就是没有的，而且我们的目标是保证进程一直存活，而不是尽可能多的活起来。所以这个当作一个补充的手段也不错，另外所有那些可以静态注册的广播都可以这样搞，前提是你不怕用户看到你申请了好多权限，当然这个USER_PRESENT事件是不需要权限的。
以下是几个常见可以静态注册的广播
android.intent.action.USER_PRESENT
android.net.conn.CONNECTIVITY_CHANGE
android.intent.action.MEDIA_MOUNTED
android.intent.action.MEDIA_UNMOUNTED
android.net.wifi.RSSI_CHANGED
android.net.wifi.STATE_CHANGE

android.net.wifi.WIFI_STATE_CHANGED

**6、服务互相绑定**

​      这个是android里面一个特性，跨进程bind一个service之后，如果被bind的service挂掉，bind他的service会把他拉起来！可以考虑使用远程服务来实现，可是还是不能保活进程，可以被杀掉！

**7、设置闹钟，定时唤醒**
      一开始个人认为这个效果还是可以的，个人测试的时候，使用360清理，他是可以保活的，开机也能重启，可是有时会失灵，而且面对force close直接挂掉！具体的例子和实现也就一个监听开机的广播，和一个周期性的闹钟！
相关的知识点可以看我之前的博客：
Android_AlarmManager(全局定时器)::<http://blog.csdn.net/Two_Water/article/details/52004414>
Android_Service(2)前台服务(service)和远程服务(service):<http://blog.csdn.net/Two_Water/article/details/52084372>

Demo的下载地址：<http://download.csdn.net/detail/two_water/9595724>

![img](assets/android_procpersist/Center.png)

![img](assets/android_procpersist/Center-20190308010748477.png)



**8、账户同步，定时唤醒**

      这个是找了很久才发现有这个东西的，android系统里有一个账户系统，设置一个自己的账户，android会定期唤醒账户更新服务，我们可以自己设定同步的事件间隔。且发起更新的是系统，不会受到任何限制。
可是它还是有局限性：
      1. 用户会在系统设置的账户列表里面看到一个不认识的账户；
      2. 同步的事件间隔是有限制的，最短1分钟，见源码，如果小雨60秒，置为60秒。而且各种国产机怎么改的源码我们未可知，是不是都能用仍然未可知；
      3. 很致命，某些手机比如note3需要手动设置账户，你如何骗你的用户给你手动设置账户完了之后不卸载你；
      4. 也很致命，必须联网！google提供这个组件是让你同步账户信息，不联网你同步个鬼，我们要保活，可以不联网不做事，但是不能不联网就死

**9、native层保活（守护进程）**

​       至于native层保活，一开始是在github上找个这个开源项目的：https://github.com/Coolerfall/Android-AppDaemon
 Demo下载地址：<http://download.csdn.net/detail/two_water/9595967>
​       可是这个只能在5.0以下的使用，更重要的一点是他没有进程守护，然后再寻找资源，找到了下面的这个大神的项目：
 https://github.com/Marswin/MarsDaemon
 Demo下载地址：<http://download.csdn.net/detail/two_water/9595966>
​       这个项目的原理和他的想法都在他的博客有详细的介绍，我这个菜鸟就不作分析了：
​       Android 进程常驻（0）----MarsDaemon使用说明：[http://blog.csdn.net/marswin89/article/details/50917098
](http://blog.csdn.net/marswin89/article/details/50917098)       Android 进程常驻（1）----开篇：<http://blog.csdn.net/marswin89/article/details/48015453>
​       Android 进程常驻（2）----细数利用android系统机制的保活手段：http://blog.csdn.net/marswin89/article/details/50890708
​       Android 进程常驻（3）----native保活5.0以下方案推演过程以及代码详述：http://blog.csdn.net/marswin89/article/details/50899838
​       Android 进程常驻（4）----native保活5.0以上方案推演过程以及代码详述：<http://blog.csdn.net/marswin89/article/details/50916631>
​       Android 进程常驻（5）----开机广播的简单守护以及总结：<http://blog.csdn.net/marswin89/article/details/50917409>
​      最后感谢大神，让我学习了！不过建议大家不必要使用常驻进程的软件还是不要使用！影响用户的体验，用来研究玩玩还是可以的！

​     pdf：<http://download.csdn.net/detail/two_water/9596051>



[原文](https://blog.csdn.net/Two_Water/article/details/52126855)