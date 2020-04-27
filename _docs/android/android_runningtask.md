---
title: Android 获取前台应用
description: Android 获取前台应用
---

# Android 获取前台应用

### 一 .背景：

 可以获取到Android设备当前正在显示的前台应用（如果可以，精细到页面）。

### 二.风险点

- 兼容Android 各大版本
- 兼容所有应用

### 三.调研方案

#### 3.1 Android 5.0之前getRunningTasks

 Android5.0以前，使用ActivityManager的getRunningTasks()方法，可以得到应用包名和Activity；

```
ActivityManager activityManager = (ActivityManager)context.getApplicationContext().getSystemService(Context.ACTIVITY_SERVICE);
ComponentName runningTopActivity = activityManager.getRunningTasks(1).get(0).topActivity;
```

 还需要声明权限：

```
<uses-permission android:name="android.permission.GET_TASKS" />
```

 这种方法不止能获取包名，还能获取Activity名。但是在Android 5.0以后，系统就不再对第三方应用提供这种方式来获取前台应用了，虽然调用这个方法还是能够返回结果，但是结果只包含你自己的Activity和Launcher了。

具体可见下面的权限判断：

```
private boolean isGetTasksAllowed(String caller, int callingPid, int callingUid) {  
    boolean allowed = checkPermission(android.Manifest.permission.REAL_GET_TASKS,  
            callingPid, callingUid) == PackageManager.PERMISSION_GRANTED;  
    if (!allowed) {  
        if (checkPermission(android.Manifest.permission.GET_TASKS,  
                callingPid, callingUid) == PackageManager.PERMISSION_GRANTED) {  
            // Temporary compatibility: some existing apps on the system image may  
            // still be requesting the old permission and not switched to the new  
            // one; if so, we'll still allow them full access.  This means we need  
            // to see if they are holding the old permission and are a system app.  
            try {  
                if (AppGlobals.getPackageManager().isUidPrivileged(callingUid)) {  
                    allowed = true;  
                    Slog.w(TAG, caller + ": caller " + callingUid  
                            + " is using old GET_TASKS but privileged; allowing");  
                }  
            } catch (RemoteException e) {  
            }  
        }  
    }  
    if (!allowed) {  
        Slog.w(TAG, caller + ": caller " + callingUid  
                + " does not hold REAL_GET_TASKS; limiting output");  
    }  
    return allowed;  
```

#### 3.2 通过使用量统计功能获取前台应用

 在StackOverFlow上大多数的答案都是使用usage statistics API。

 Android提供了usage statistics API。这个API本来是系统用来统计app使用情况的，包含了每个app最近一次被使用的时间。我们只需要找出距离现在时间最短的那个app，就是当前在前台的app。

```
    private String getForegroundApp(Context context) {
        UsageStatsManager usageStatsManager = 
            (UsageStatsManager) context.getSystemService(Context.USAGE_STATS_SERVICE);
        long ts = System.currentTimeMillis();
        List<UsageStats> queryUsageStats =
            usageStatsManager.queryUsageStats(UsageStatsManager.INTERVAL_BEST, 0, ts);
        UsageEvents usageEvents = usageStatsManager.queryEvents(isInit ? 0 : ts-5000, ts);
        if (usageEvents == null) {
            return null;
        }


        UsageEvents.Event event = new UsageEvents.Event();
        UsageEvents.Event lastEvent = null;
        while (usageEvents.getNextEvent(event)) {
            // if from notification bar, class name will be null
            if (event.getPackageName() == null || event.getClassName() == null) {
                continue;
            }

            if (lastEvent == null || lastEvent.getTimeStamp() < event.getTimeStamp()) {
                lastEvent = event;
            }
        }

        if (lastEvent == null) {
            return null;
        }
        return lastEvent.getPackageName();
    }
```

**问题点：**

- 这种方式只能拿到包名，无法精确到了Activity了。
- 使用这种方发之前，首先要引导用户开启使用量功能：

```
Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
startActivity(intent);
```

- 还要申明权限：

```
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS" />
```

 这个权限试了下Android Studio 直接提示为系统权限，普通App无法申请。

- 另外！因为在一些手机上，应用发起通知栏消息的时候，或者是下拉通知栏，也会被记录到使用量中，就会导致按最近时间排序出现混乱。而且收起通知栏以后，这种混乱并不会被修正，而是必须重新开启一个应用才行。

到这里基本可以先否定这个方案了，步骤复杂，还需要用户手动开启权限，不可能哒！

#### 3.3 通过辅助服务获取前台应用

 Android 辅助服务(AccessibilityService)有很多神奇的妙用，比如辅助点击，比如页面抓取，还有就是获取前台应用。

 这里简单介绍一下如何使用辅助服务，首先要在AndroidManifest.xml中声明：

```
<service
    android:name=".service.AccessibilityMonitorService"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
    >
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>

    <meta-data
        android:name="android.accessibilityservice"
        android:resource="@xml/accessibility" />
</service>
```

然后在res/xml/文件夹下新建文件accessibility.xml，内容如下：

```
<?xml version="1.0" encoding="utf-8"?>
<accessibility-service
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeViewClicked|typeViewLongClicked|typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagRetrieveInteractiveWindows"
    android:canRetrieveWindowContent="true"
    android:canRequestFilterKeyEvents ="true"
    android:notificationTimeout="10"
    android:packageNames="@null"
    android:description="@string/accessibility_des"
    android:settingsActivity="com.pl.recent.MainActivity"
/>
```

关键是typeWindowStateChanged。
新建AccessibilityMonitorService，主要内容如下：

```
public class AccessibilityMonitorService extends AccessibilityService {
    private CharSequence mWindowClassName;
    private String mCurrentPackage;
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        int type=event.getEventType();
        switch (type){
            case AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED:
                mWindowClassName = event.getClassName();
                mCurrentPackage = event.getPackageName()==null?"":event.getPackageName().toString();                
                break;
            case TYPE_VIEW_CLICKED:
            case TYPE_VIEW_LONG_CLICKED:
                break;
        }
    }
}
```

问题点

- 也是需要用户去在“设置里”找到辅助服务并开启即可。

- 辅助服务在一些手机（小米、魅族、华为等国产手机）上，一旦程序被清理后台，就会被关闭。。。

so，这种方案不太稳定而且也是需要用户手动去开启，不可能哒！

#### 3.4 通过设备辅助应用程序获取前台应用（比较鸡肋）

 所谓设备辅助应用程序，是在一些接近原生的系统上，长按Home键就会触发的应用，默认是会触发Google搜索。设备辅助应用程序有点像是需要主动触发的辅助服务，因为应用中是无法主动去触发其功能的，所以说比较鸡肋，

#### 3.5 PS 命令

 在Android 的ADB命令中我们可以通过`PS`命令来获取到一些应用进程信息，看下官方解释：

```
P show scheduling policy, either bg or fg are common, but also un and er for failures to get policy
```

大概意思就是说这个会列出系统调度列表，如果是系统的话，那是不是就说明能够得到界面的调度呢？

------

# Android shell tricks: ps

If you ever played around with the `adb shell` you may have found that the `ps` utility, which lists process lists, is not as verbose as you would expect it to be. And, to make things worse, there’s no inline help or `man` entries. Here’s the `ps` utility usage line: `ps -t -x -P -p -c [pid|name]`.



![img](assets/android_runningtask/580.png)

Android shell tricks: ps

- `-t` show threads, comes up with threads in the list
- `-x` shows time, user time and system time in seconds
- **-P show scheduling policy, either bg or fg are common, but also un and er for failures to get policy**
- **-p show priorities, niceness level**
- `-c` show CPU (may not be available prior to Android 4.x) involved
- `[pid]` filter by PID if numeric, or…
- `[name]` …filter by process name

Android’s core toolbox (shell utilities) are more primitive than the ones you may be used to. Notice how each argument needs to be separated and you can’t just `-txPc`it all, the command line argument parser is non-complex.

It’s a pity how command line arguments are not shown. If you need something that’s not available by the stock `ps` shell utility, try [manually combing through](https://link.jianshu.com/?t=http://archive09.linux.com/feature/126718) the `/proc`directory. For the command line one would do `cat /proc/<pid>/cmdline`.

------

首先我们在cmd命令行模式输入 : adb shell ps 输出一下信息：



![img](assets/android_runningtask/642-20190308010122628.png)

 然后能很清晰的看见各种包名而且都是系统正在运行中的,按照说明如果 **-p **参数可以列出前台进程调度的话,如果我们在切换程序或者对出时包名列表都会有变化。

以下是输入 adb shell ps -p 后输出的信息：



![img](assets/android_runningtask/642.png)

 仔细观察会发现u0开头的都是我们正常程序的包名,而且在程序切换到后台以后，这个列表是有变化的,随便启动一个自己安装的应用,列表也刚好出现那个应用。在此大家应该就已经知道怎么写了，这里也提供一下实现思路:

1、命令行获取控制台输出流
2、找出每行输出的 u0开通的信息获取包名
3、用一个列表存入,与每次获取的当前列表项与上一次列表项对比，如果旧的列表不存在此包名,那就证明这个包就是新启动的了，如果没有就不做任何操作。

测试结论：

- 理论上没什么毛病，但是实践中发现存在不稳定的现象，有时候根本拿不到，有时候获取失败
- 比如：最常用的微信，打开微信到登录页面时并没有捕捉到。
- 因此，该方案存在一些不稳定因素

#### 3.5 大招

 从网络上看到一篇老外大神的做法，中文分析博客已经丢失，google一下也没有啥有效因袭。所以只好自己大概猜测和理解了

上代码：

```
public class SuperRunningPackage {

    /** first app user */
    public static final int AID_APP = 10000;
    /** offset for uid ranges for each user */
    public static final int AID_USER = 100000;
    public static String getForegroundApp() {
        Log.e("PKG","VersionCode:"+Build.VERSION.SDK_INT);
        File[] files = new File("/proc").listFiles();
        int lowestOomScore = Integer.MAX_VALUE;
        String foregroundProcess = null;
        for (File file : files) {
            if (!file.isDirectory()) {
                continue;
            }
            int pid;
            try {
                pid = Integer.parseInt(file.getName());
            } catch (NumberFormatException e) {
                continue;
            }
            try {
                String cgroup = read(String.format("/proc/%d/cgroup", pid));
                String[] lines = cgroup.split("\n");
                String cpuSubsystem;
                String cpuaccctSubsystem;


                for (int i = 0; i < lines.length; i++) {

                    Log.e("PKG",lines[i]);

                }


                if (lines.length == 2) {//有的手机里cgroup包含2行或者3行，我们取cpu和cpuacct两行数据
                    cpuSubsystem = lines[0];
                    cpuaccctSubsystem = lines[1];
                }else if(lines.length==3){
                    cpuSubsystem = lines[0];
                    cpuaccctSubsystem = lines[2];
                }else if(lines.length == 5){//6.0系统
                    cpuSubsystem = lines[2];
                    cpuaccctSubsystem = lines[4];
                }else {
                    continue;
                }
                if (!cpuaccctSubsystem.endsWith(Integer.toString(pid))) {
                    // not an application process
                    continue;
                }
                if (cpuSubsystem.endsWith("bg_non_interactive")) {
                    // background policy
                    continue;
                }
                String cmdline = read(String.format("/proc/%d/cmdline", pid));
                if (cmdline.contains("com.android.systemui")) {
                    continue;
                }
                int uid = Integer.parseInt(
                        cpuaccctSubsystem.split(":")[2].split("/")[1].replace("uid_", ""));
                if (uid >= 1000 && uid <= 1038) {
                    // system process
                    continue;
                }
                int appId = uid - AID_APP;
                int userId = 0;
                // loop until we get the correct user id.
                // 100000 is the offset for each user.
                while (appId > AID_USER) {
                    appId -= AID_USER;
                    userId++;
                }
                if (appId < 0) {
                    continue;
                }
                // u{user_id}_a{app_id} is used on API 17+ for multiple user account support.
                // String uidName = String.format("u%d_a%d", userId, appId);
                File oomScoreAdj = new File(String.format("/proc/%d/oom_score_adj", pid));
                if (oomScoreAdj.canRead()) {
                    int oomAdj = Integer.parseInt(read(oomScoreAdj.getAbsolutePath()));
                    if (oomAdj != 0) {
                        continue;
                    }
                }
                int oomscore = Integer.parseInt(read(String.format("/proc/%d/oom_score", pid)));
                if (oomscore < lowestOomScore) {
                    lowestOomScore = oomscore;
                    foregroundProcess = cmdline;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return foregroundProcess;
    }


    private static String read(String path) throws IOException {
        StringBuilder output = new StringBuilder();
        BufferedReader reader = new BufferedReader(new FileReader(path));
        output.append(reader.readLine());
        for (String line = reader.readLine(); line != null; line = reader.readLine()) {
            output.append('\n').append(line);
        }
        reader.close();
        return output.toString().trim();
    }

}
```



 不详细分析，大概意思就是每次前台应用变动就会改变一个配置文件，因此可以通过读取改配置的方案来获取前台应用。经过测试，基本主流应用在前台时都可以捕捉到。

### 四.大结论

- Android 5.0 以下可以通过`getRunningTasks`获取到前台的包名。
- Android 5.0-6.0 可以通过读取系统配置文件来获取当前前台应用。
- Android 7.0+暂时不确定稳定性，需要后期更多实践，我理解7.0 以下已经基本满足需求。

[原文](https://www.jianshu.com/u/fb5ee6c7113e)