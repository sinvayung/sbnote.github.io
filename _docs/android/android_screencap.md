---
title: Android 截屏方式整理
description: Android 截屏方式整理
---

# Android 截屏方式整理

 Android 实现截屏方式整理

**可能的需求：**

- 截自己的屏
- 截所有的屏

- 带导航栏截屏
- 不带导航栏截屏
- 截屏并编辑选取一部分
- 自动截取某个空间或者布局
- 截取长图
- 在后台去截屏

### 1.只截取自己应用内部界面

##### 1.1 截取除了导航栏之外的屏幕

```
View dView = getWindow().getDecorView();
dView.setDrawingCacheEnabled(true);
dView.buildDrawingCache();
Bitmap bitmap = Bitmap.createBitmap(dView.getDrawingCache());
if (bitmap != null) {
    try {
        // 获取内置SD卡路径
        String sdCardPath = Environment.getExternalStorageDirectory().getPath();
        // 图片文件路径
        String filePath = sdCardPath + File.separator + "screenshot.png";
        File file = new File(filePath);
        FileOutputStream os = new FileOutputStream(file);
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, os);
        os.flush();
        os.close();
        DebugLog.d("a7888", "存储完成");
    } catch (Exception e) {
    }
}
```

##### 1.2 截取某个控件或者区域

两种方案：

- 跟上面差不多，只不过view不适用根view，而是使用某个某个控件。

```
View dView = title;
dView.setDrawingCacheEnabled(true);
dView.buildDrawingCache();
Bitmap bitmap = Bitmap.createBitmap(dView.getDrawingCache());
```

- 手动draw

```
View dView = titleTv;
Bitmap bitmap = Bitmap.createBitmap(dView.getWidth(), dView.getHeight(), Bitmap.Config.ARGB_8888);
//使用Canvas，调用自定义view控件的onDraw方法，绘制图片
Canvas canvas = new Canvas(bitmap);
dView.draw(canvas);
```

##### 1.3 截取带导航栏的整个屏幕

 这一小节会将一些理论上可以，但是**实践会特别复杂，不太推荐使用**。可以学习了解。

- adb 命令

  这里指的不是连接电脑进行adb操控，而是在App内部实现adb命令的操控

  在APK中调用“adb shell screencap -pfilepath” 命令

  该命令读取系统的framebuffer，需要获得系统权限：

  > （1）. 在AndroidManifest.xml文件中添加
  >
  > <uses-permissionandroid:name="android.permission.READ_FRAME_BUFFER"/>
  >
  > （2）. 修改APK为系统权限，将APK放到源码中编译， 修改Android.mk
  >
  > LOCAL_CERTIFICATE := platform

```
publicvoid takeScreenShot(){ 
    String mSavedPath = Environment.getExternalStorageDirectory()+File. separator + "screenshot.png" ; 
try {                     
           Runtime. getRuntime().exec("screencap -p " + mSavedPath); 
    } catch (Exception e) { 
           e.printStackTrace(); 
    } 
```

- 利用系统的隐藏API，实现Screenshot,这部分代码是系统隐藏的，需要在源码下编译。

  ```
  1).修改Android.mk， 添加系统权限
            LOCAL_CERTIFICATE := platform
  2).修改AndroidManifest.xml 文件，添加权限
  <uses-permissionandroid:name="android.permission.READ_FRAME_BUFFER"/>
  ```

  ```
   public boolean takeScreenShot(String imagePath){
                       
                      
                       
               if(imagePath.equals("" )){
                        imagePath = Environment.getExternalStorageDirectory()+File. separator+"Screenshot.png" ;
               }
                       
            Bitmap mScreenBitmap;
            WindowManager mWindowManager;
            DisplayMetrics mDisplayMetrics;
            Display mDisplay;
                    
            mWindowManager = (WindowManager) mcontext.getSystemService(Context.WINDOW_SERVICE);
            mDisplay = mWindowManager.getDefaultDisplay();
            mDisplayMetrics = new DisplayMetrics();
            mDisplay.getRealMetrics(mDisplayMetrics);
                                   
            float[] dims = {mDisplayMetrics.widthPixels , mDisplayMetrics.heightPixels };
            mScreenBitmap = Surface. screenshot((int) dims[0], ( int) dims[1]);
                       
            if (mScreenBitmap == null) {  
                   return false ;
            }
                    
         try {
            FileOutputStream out = new FileOutputStream(imagePath);
            mScreenBitmap.compress(Bitmap.CompressFormat. PNG, 100, out);
               
          } catch (Exception e) {
                  
                  
            return false ;
          }       
                              
         return true ;
  }
  ```

- Android本地编程（Native Programming）读取framebuffer

命令行，框架的截屏功能是通过framebuffer来实现的，所以我们先来介绍一下framebuffer。

**framebuffer介绍**
帧缓冲（framebuffer）是[Linux](https://link.jianshu.com/?t=http://lib.csdn.net/base/linux)为显示设备提供的一个接口，把显存抽象后的一种设备，他允许上层应用程序在图形模式下直接对显示缓冲区进行 读写操作。这种操作是抽象的，统一的。用户不必关心物理显存的位置、换页机制等等具体细节。这些都是由Framebuffer设备驱动来完成的。
[linux](https://link.jianshu.com/?t=http://lib.csdn.net/base/linux) FrameBuffer 本质上只是提供了对图形设备的硬件抽象，在开发者看来，FrameBuffer 是一块显示缓存，往显示缓存中写入特定格式的数据就意味着向屏幕输出内容。所以说FrameBuffer就是一块白板。例如对于初始化为16 位色的FrameBuffer 来说， FrameBuffer中的两个字节代表屏幕上一个点，从上到下，从左至右，屏幕位置与内存地址是顺序的线性关系。
帧缓存有个地址，是在内存里。我们通过不停的向frame buffer中写入数据， 显示控制器就自动的从frame buffer中取数据并显示出来。全部的图形都共享内存中同一个帧缓存。

**android截屏实现思路**
Android系统是基于Linux内核的，所以也存在framebuffer这个设备，我们要实现截屏的话只要能获取到framebuffer中的数据，然后把数据转换成图片就可以了，android中的framebuffer数据是存放在 **/dev/graphics/fb0** 文件中的，所以我们只需要来获取这个文件的数据就可以得到当前屏幕的内容。
现在我们的[测试](https://link.jianshu.com/?t=http://lib.csdn.net/base/softwaretest)代码运行时候是通过RC(remote controller)方式来运行被测应用的，那就需要在PC机上来访问模拟器或者真机上的framebuffer数据，这个的话可以通过android的ADB命令来实现。

- 各大手机自带的按键组合进行截屏

  Android源码中对按键的捕获位于文件PhoneWindowManager.java（alps\frameworks\base\policy\src\com\android\internal\policy\impl）中，这个类处理所有的键盘输入事件，其中函数interceptKeyBeforeQueueing（）会对常用的按键做特殊处理。

- 具体实现源码讲解可以参考：

  [http://blog.csdn.net/woshinia/article/details/11520403](https://link.jianshu.com/?t=http://blog.csdn.net/woshinia/article/details/11520403)

### 2. 截取非含当前应用的屏幕部分（最佳官方方案）

 Android 在5.0 之后支持了实时录屏的功能。通过实时录屏我们可以拿到截屏的图像。同时可以通过在Service中处理实现后台的录屏。具体的类讲解大家自行网上查阅。

大体步骤：

1.初始化一个`MediaProjectionManager`。

```
MediaProjectionManager mMediaProjectionManager = (MediaProjectionManager)getApplication().getSystemService(Context.MEDIA_PROJECTION_SERVICE);
```

2.创建intent,并启动`Intent`。注意这里是`startActivityForResult`

```
startActivityForResult(mMediaProjectionManager.createScreenCaptureIntent(), REQUEST_MEDIA_PROJECTION);
```

3.在`onActivityResult`中拿到Mediaprojection。

```
mResultCode = resultCode;
mResultData = data;
mMediaProjection = mMediaProjectionManager.getMediaProjection(mResultCode, mResultData);
```

4.设置VirtualDisplay 将图像和展示的View关联起来。一般来说我们会将图像展示到SurfaceView，这里为了为了便于拿到截图，我们使用ImageReader，他内置有SurfaceView。

```
mImageReader = ImageReader.newInstance(windowWidth, windowHeight, 0x1, 2); //ImageFormat.RGB_565
mVirtualDisplay = mMediaProjection.createVirtualDisplay("screen-mirror",
                windowWidth, windowHeight, mScreenDensity,             DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
                mImageReader.getSurface(), null, null);
```

5.通过ImageReader拿到截图

```
strDate = dateFormat.format(new java.util.Date());
nameImage = pathImage+strDate+".png";

Image image = mImageReader.acquireLatestImage();
int width = image.getWidth();
int height = image.getHeight();
final Image.Plane[] planes = image.getPlanes();
final ByteBuffer buffer = planes[0].getBuffer();
int pixelStride = planes[0].getPixelStride();
int rowStride = planes[0].getRowStride();
int rowPadding = rowStride - pixelStride * width;
Bitmap bitmap = Bitmap.createBitmap(width+rowPadding/pixelStride, height, Bitmap.Config.ARGB_8888);
bitmap.copyPixelsFromBuffer(buffer);
bitmap = Bitmap.createBitmap(bitmap, 0, 0,width, height);
image.close();
```

6.注意截屏之后要及时关闭VirtualDisplay ，因为VirtualDisplay 是十分消耗内存和电量的。

```
if (mVirtualDisplay == null) {
            return;
}
mVirtualDisplay.release();
mVirtualDisplay = null;
```

ps: 具体可以参考Google官方给的demo以及其他开发者写的Demo

- [https://github.com/googlesamples/android-ScreenCapture](https://link.jianshu.com/?t=https://github.com/googlesamples/android-ScreenCapture)
- [https://github.com/VincentWYJ/CaptureScreen](https://link.jianshu.com/?t=https://github.com/VincentWYJ/CaptureScreen)

### 3. 截取长屏

 截取长屏其实原理就是截取整个ScrollView或者ListView的视图，因此实现原理跟上面中提到的截取某个控件的View基本一致。

- ScrollView 实现截屏

```
    /**
     * 截取scrollview的屏幕
     * **/
    public static Bitmap getScrollViewBitmap(ScrollView scrollView) {
        int h = 0;
        Bitmap bitmap;
        for (int i = 0; i < scrollView.getChildCount(); i++) {
            h += scrollView.getChildAt(i).getHeight();
        }
        // 创建对应大小的bitmap
        bitmap = Bitmap.createBitmap(scrollView.getWidth(), h,
                Bitmap.Config.ARGB_8888);
        final Canvas canvas = new Canvas(bitmap);
        scrollView.draw(canvas);
        return bitmap;
    }
```

- ListView实现截屏

```
 /**
     *  截图listview
     * **/
    public static Bitmap getListViewBitmap(ListView listView,String picpath) {
        int h = 0;
        Bitmap bitmap;
        // 获取listView实际高度
        for (int i = 0; i < listView.getChildCount(); i++) {
            h += listView.getChildAt(i).getHeight();
        }
        Log.d(TAG, "实际高度:" + h);
        Log.d(TAG, "list 高度:" + listView.getHeight());
        // 创建对应大小的bitmap
        bitmap = Bitmap.createBitmap(listView.getWidth(), h,
                Bitmap.Config.ARGB_8888);
        final Canvas canvas = new Canvas(bitmap);
        listView.draw(canvas);
        return bitmap;
    }
```

- WebView实现截屏

```
//这是webview的，利用了webview的api
private static Bitmap captureWebView(WebView webView) {
        Picture snapShot = webView.capturePicture();
        Bitmap bmp = Bitmap.createBitmap(snapShot.getWidth(),
                snapShot.getHeight(), Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bmp);
        snapShot.draw(canvas);
        return bmp;
    }
```

- 有时候我们可能需要去滚动屏幕，然后再滚动到某一个地方时停止截屏，这样就会去截取从开始到滚动结束位置的view，而不是整个ScrollView，这个时候就需要进行一些控制，具体原理跟上面讲的差不多，可以参考一下下面的实现：

  [https://android-notes.github.io/2016/12/03/android%E9%95%BF%E6%88%AA%E5%B1%8F%E5%8E%9F%E7%90%86/](https://link.jianshu.com/?t=https://android-notes.github.io/2016/12/03/android%E9%95%BF%E6%88%AA%E5%B1%8F%E5%8E%9F%E7%90%86/)

### 4. 实时截屏

 可参考2中Android 在5.0的做法，进行实时录制。

[原文](https://www.jianshu.com/u/fb5ee6c7113e)