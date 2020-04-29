---
title: FFMpeg版本相关信息
description: FFMpeg版本相关信息
---

#### FFMpeg版本相关信息

```sh
ffmpeg -version
```

#### 显示可用的格式（包括设备）

```sh
ffmpeg -formats
```

#### 显示可用的解复用器

```sh
ffmpeg -demuxers
```

#### 显示可用的复用器

```sh
ffmpeg -muxers
```

#### 显示可用的设备：音视频采集（摄像头，麦克风）

```sh
ffmpeg -devices
```

#### 显示所有的编解码器

```sh
ffmpeg -codecs
```

#### 显示所有的编码器

```sh
ffmpeg -encoders
```

#### 显示所有的解码器

```sh
ffmpeg -decoders
```

#### 显示可用的协议

```sh
ffmpeg -protocols
```

#### 显示可用的libavfilter过滤器

```sh
ffmpeg -filters
```

#### 显示可用的比特流filter

```sh
ffmpeg -bsfs
```

#### 显示可用的像素格式

```sh
ffmpeg -pix_fmts
```

#### 显示可用的采样格式

```sh
ffmpeg -sample_fmts
```

## 

### 查看支持的设备索引号

```sh
ffmpeg -f avfoundation -list_devices true -i ""
```

> avfundation是mac媒体框架

**log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffmpeg -f avfoundation -list_devices true -i ""
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.1 (clang-1001.0.46.4)
  configuration: 
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
[AVFoundation input device @ 0x7fa6de404400] AVFoundation video devices:
[AVFoundation input device @ 0x7fa6de404400] [0] FaceTime HD Camera
[AVFoundation input device @ 0x7fa6de404400] [1] Capture screen 0
[AVFoundation input device @ 0x7fa6de404400] AVFoundation audio devices:
[AVFoundation input device @ 0x7fa6de404400] [0] MacBook Pro 麦克风
: Input/output error
```



视频原始数据格式yuv，音频原始数据格式pcm



### 录屏

```sh
ffmpeg -f avfoundation -i 1 -r 30 out.yuv
```

**参数说明：**

- -f：指定使用avfoundation采集数据
- -i：指定从哪采集数据，它是一个文件索引号，在MAC上，1代表桌面，0代表摄像头
- -r，-framerate：指定帧率

**录制开始的log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffmpeg -f avfoundation -i 1 -r 30 out.yuv
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.1 (clang-1001.0.46.4)
  configuration: 
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
[AVFoundation input device @ 0x7fabde404400] Configuration of video device failed, falling back to default.
[avfoundation @ 0x7fabde800000] Selected pixel format (yuv420p) is not supported by the input device.
[avfoundation @ 0x7fabde800000] Supported pixel formats:
[avfoundation @ 0x7fabde800000]   uyvy422
[avfoundation @ 0x7fabde800000]   yuyv422
[avfoundation @ 0x7fabde800000]   nv12
[avfoundation @ 0x7fabde800000]   0rgb
[avfoundation @ 0x7fabde800000]   bgr0
[avfoundation @ 0x7fabde800000] Overriding selected pixel format to use uyvy422 instead.
[avfoundation @ 0x7fabde800000] Stream #0: not enough frames to estimate rate; consider increasing probesize
Input #0, avfoundation, from '1':
  Duration: N/A, start: 3905.818667, bitrate: N/A
    Stream #0:0: Video: rawvideo (UYVY / 0x59565955), uyvy422, 3360x2100, 1000k tbr, 1000k tbn, 1000k tbc
```

这里打印出了录制的象素格式为uyvy422，视频尺寸为3360x2100，注意，播放时必需指定与录制时一致的值，才能正常播放，否则可能会花屏。



```text
全屏录像 ( dshow录屏, H264编码 )
ffmpeg -f dshow -i video="screen-capture-recorder" -f dshow -i audio="virtual-audio-capturer" -vcodec libx264 -acodec libmp3lame -s 1280x720 -r 15 e:/temp/temp.mkv

全屏录像 ( gdigrab录屏, H264编码 )
ffmpeg -f gdigrab -i desktop -f dshow -i audio="virtual-audio-capturer" -vcodec libx264 -acodec libmp3lame -s 1280x720 -r 15 e:/temp/temp.mkv

全屏录像 ( gdigrab录屏, vp9编码 )( 注 : dshow不支持vp9 )
ffmpeg -f gdigrab -i desktop -f dshow -i audio="virtual-audio-capturer" -vcodec libvpx-vp9 -acodec libmp3lame -s 1280x720 -r 15 e:/temp/temp.mkv

区域录像 ( 起点:100,60 width:600 width:480 )
ffmpeg -f gdigrab -i desktop -f dshow -i audio="virtual-audio-capturer" -vcodec libx264 -acodec libmp3lame -video_size 600x480 -offset_x 100 -offset_y 60 -r 15 e:/temp/temp.mkv
```





### 播放录屏文件

```sh
ffplay -pixel_format uyvy422 -video_size 3360x2100 out.yuv
```

**参数说明：**

- -pixel_format：指定对应的像素格式
- -video_size：指定对应的视频尺寸（分辨率）

**播放开始的log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffplay -pixel_format uyvy422 -video_size 3360x2100 out.yuv
ffplay version 4.2.2-tessus  https://evermeet.cx/ffmpeg/  Copyright (c) 2003-2019 the FFmpeg developers
  built with Apple clang version 11.0.0 (clang-1100.0.33.16)
  configuration: --cc=/usr/bin/clang --prefix=/opt/ffmpeg --extra-version=tessus --enable-avisynth --enable-fontconfig --enable-gpl --enable-libaom --enable-libass --enable-libbluray --enable-libdav1d --enable-libfreetype --enable-libgsm --enable-libmodplug --enable-libmp3lame --enable-libmysofa --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenh264 --enable-libopenjpeg --enable-libopus --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvmaf --enable-libvo-amrwbenc --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-version3 --pkg-config-flags=--static --enable-librtmp --enable-ffplay --enable-sdl2 --disable-ffmpeg --disable-ffprobe
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
  libpostproc    55.  5.100 / 55.  5.100
[rawvideo @ 0x7f9abe008000] Estimating duration from bitrate, this may be inaccurate
Input #0, rawvideo, from 'out.yuv':
  Duration: 00:00:43.56, start: 0.000000, bitrate: 2822400 kb/s
    Stream #0:0: Video: rawvideo (UYVY / 0x59565955), uyvy422, 3360x2100, 2822400 kb/s, 25 tbr, 25 tbn, 25 tbc 
```

这里打印出了播放的象素格式为uyvy422，视频尺寸为3360x2100。



### 录音

```sh
ffmpeg -f avfoundation -i :0 out.wav
```

**参数说明：**

- -f：指定使用avfoundation采集数据
- -i：指定从哪采集数据，它是一个文件索引号，视频设备号在“:”前面，音频设备号在“:”后面。如：":0"表示只录音频，"1:0"表示同时录音视频

**录制开始的log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffmpeg -f avfoundation -i :0 out.wav
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.1 (clang-1001.0.46.4)
  configuration: 
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
Input #0, avfoundation, from ':0':
  Duration: N/A, start: 4815.193000, bitrate: 1536 kb/s
    Stream #0:0: Audio: pcm_f32le, 48000 Hz, mono, flt, 1536 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (pcm_f32le (native) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, wav, to 'out.wav':
  Metadata:
    ISFT            : Lavf58.29.100
    Stream #0:0: Audio: pcm_s16le ([1][0][0][0] / 0x0001), 48000 Hz, mono, s16, 768 kb/s
    Metadata:
      encoder         : Lavc58.54.100 pcm_s16le
size=     529kB time=00:00:05.64 bitrate= 768.1kbits/s speed=   1x    
video:0kB audio:529kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.014399%
```



### 分解与复用

输入文件——>解封装——> 操作——> 封装 ——>输出文件

转换格式：

```sh
# 将mov文件转换成mp4文件
ffmpeg -i xx.mov -acodec copy -vcodec copy out.mp4
```

提取音频：

```sh
ffmpeg -i xx.mov -acodec copy -vn out.aac
```

提取视频：

```sh
ffmpeg -i xx.mov -an -vcodec copy out.h264
```

**参数说明：**

- -i：输入文件
- -acodec copy：对音频编码文件进行拷贝
- -vcodec copy：对视频编码文件进行拷贝
- -an：audio no  // 不包含音频
- -vn：video no // 不包含视频



### 处理原始数据

这里的原始数据指的是FFmpeg解码后的数据，对于音频就是PCM数据，对于视频就是YUV数据。

**FFmpeg提取YUV数据**

```sh
# 提取
ffmpeg -i input.mp4 -an -c:v rawvideo -pix_fmts yuv420p out.yuv
# 播放
ffplay -s 624x1160 out.yuv 
```



常用的YUV格式
 为节省带宽起见，大多数YUV格式平均使用的每像素位数都少于24位。主要的抽样（subsample）格式有YCbCr4:2:0、YCbCr4:2:2、YCbCr4:1:1和YCbCr4:4:4。YUV的表示法称为A:B:C表示法：

4:4:4表示完全取样。

4:2:2表示2:1的水平取样，垂直完全采样。

4:2:0表示2:1的水平取样，垂直2：1采样。

4:1:1表示4:1的水平取样，垂直完全采样。



**FFmpeg提取PCM数据**

```sh
# 提取
ffmpeg -i out.mp4 -vn -ar 44100 -ac2 -f s16le out.pcm
# 播放
ffplay -ar 44100 -ac 2 -f s16le out.pcm
```

**参数说明：**

- -ar：指定采样率;
- -ac：指定声道数；
- -f s16le：表示每个采样点用16位浮点数来表示（le表示小端，be表示大端）





### 摄像头录制视频

```sh
ffmpeg -framerate 30 -f avfoundation -i 0 out.mp4
```

**参数说明：**

- -f：指定使用avfoundation采集数据
- -i：指定从哪采集数据，它是一个文件索引号，在MAC上，1代表桌面，0代表摄像头
- -r，-framerate：指定帧率  （奇怪此参数放后面不行）

**录制开始的log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffmpeg -framerate 30 -f avfoundation -i 0 out.mp4
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.1 (clang-1001.0.46.4)
  configuration: 
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
[avfoundation @ 0x7fa2de001800] Selected pixel format (yuv420p) is not supported by the input device.
[avfoundation @ 0x7fa2de001800] Supported pixel formats:
[avfoundation @ 0x7fa2de001800]   uyvy422
[avfoundation @ 0x7fa2de001800]   yuyv422
[avfoundation @ 0x7fa2de001800]   nv12
[avfoundation @ 0x7fa2de001800]   0rgb
[avfoundation @ 0x7fa2de001800]   bgr0
[avfoundation @ 0x7fa2de001800] Overriding selected pixel format to use uyvy422 instead.
Input #0, avfoundation, from '0':
  Duration: N/A, start: 9490.089800, bitrate: N/A
    Stream #0:0: Video: rawvideo (UYVY / 0x59565955), uyvy422, 1280x720, 30 tbr, 1000k tbn, 1000k tbc
Stream mapping:
  Stream #0:0 -> #0:0 (rawvideo (native) -> mpeg4 (native))
Press [q] to stop, [?] for help
Output #0, mp4, to 'out.mp4':
  Metadata:
    encoder         : Lavf58.29.100
    Stream #0:0: Video: mpeg4 (mp4v / 0x7634706D), yuv420p, 1280x720, q=2-31, 200 kb/s, 30 fps, 15360 tbn, 30 tbc
    Metadata:
      encoder         : Lavc58.54.100 mpeg4
    Side data:
      cpb: bitrate max/min/avg: 0/0/200000 buffer size: 0 vbv_delay: -1
frame=  968 fps= 30 q=31.0 size=    2048kB time=00:00:32.23 bitrate= 520.5kbits/s speed=   1x  
```



### 录制音频原始数据

```sh
ffmpeg -f avfoundation -i :0 -ar 44100 -f s16le out.pcm
```

**参数说明：**

- -ar : 音频采样率为44.1K 

**录制开始的log信息：**

```txt
XINHUARONG-MB0:fftest simba$ ffmpeg -f avfoundation -i :0 -ar 44100 -f s16le out.pcm
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.1 (clang-1001.0.46.4)
  configuration: 
  libavutil      56. 31.100 / 56. 31.100
  libavcodec     58. 54.100 / 58. 54.100
  libavformat    58. 29.100 / 58. 29.100
  libavdevice    58.  8.100 / 58.  8.100
  libavfilter     7. 57.100 /  7. 57.100
  libswscale      5.  5.100 /  5.  5.100
  libswresample   3.  5.100 /  3.  5.100
Input #0, avfoundation, from ':0':
  Duration: N/A, start: 10020.003417, bitrate: 1536 kb/s
    Stream #0:0: Audio: pcm_f32le, 48000 Hz, mono, flt, 1536 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (pcm_f32le (native) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, s16le, to 'out.pcm':
  Metadata:
    encoder         : Lavf58.29.100
    Stream #0:0: Audio: pcm_s16le, 44100 Hz, mono, s16, 705 kb/s
    Metadata:
      encoder         : Lavc58.54.100 pcm_s16le
size=     356kB time=00:00:04.13 bitrate= 705.6kbits/s speed=   1x    
video:0kB audio:356kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.000000%
Exiting normally, received signal 2.
```







======================

# FFMpeg常用命令总结

## 分解与复用

#### 提取音频流

```
ffmpeg -i 1578361708648565.mp4 -acodec copy -vn out3.aac

-i : 输入文件
-acodec : 指定音频编码器，copy 为只拷贝，不编码
-vn : v代表视频 n代表no 无视频
复制代码
```

#### 提取视频流

```
ffmpeg -i 1578361708648565.mp4 -vcodec copy -an out4.h264

-an : 无音频
-vcodec : 拷贝视频
复制代码
```

#### 格式转换

```
ffmpeg -i 1578361708648565.mp4 -vcodec copy -acodec copy 3333.flv

音频和视频数据都通过拷贝，不做编解码处理。 重新muxer为新的格式
复制代码
```

#### 音频流视频流合并

```
ffmpeg -i out4.h264 -i out3.aac -vcodec copy -acodec copy 4444.mp4

音视频数据通过拷贝，不做编解码处理，直接muxer为新的文件
复制代码
```

## 处理原始数据

#### 提取YUV数据

```
ffmpeg -i 1578361708648565.mp4 -an -c:v rawvideo -pixel_format yuv420p 555.yuv

-c:v rawvideo : 将视频转为原始数据
-pixel_format : 指定yuv格式为yuv420p
复制代码
```

#### YUV转H264

```
ffmpeg -f rawvideo -pix_fmt yuv420p -s 320x240 -r 30 -i out.yuv -c:v libx264 -f rawvideo out.h264
复制代码
```

#### 提取PCM数据

```
ffmpeg -i 1578361708648565.mp4 -vn -ar 44100 -ac 2 -f s16le 666.pcm

-ac : audio channl 音频双通道
-f s16le : 音频格式，silk格式为16位有符号小端存储模式

播放： ffplay -ar 44100 -ac 2 -f s16le -i 666.pcm
复制代码
```

#### PCM转WAV

```
ffmpeg -f s16be -ar 44100 -ac 2 -acodec pcm_s16be -i 666.pcm output.wav

播放：ffplay -f s16be -ar 44100 -ac 2 -i output.wav
复制代码
```

## 滤镜

#### 添加水印

```
$ ffmpeg -i 1578361708648565.mp4 -vf "movie=logo.png,scale=64:48[watermask];[in][watermask] overlay=30:10 [out]" water.mp4

-vf中的 movie 指定logo位置。scale 指定 logo 大小。overlay 指定 logo 摆放的位置
复制代码
```

#### 删除水印

先找到水印的位置

```
ffplay -i water.mp4 -vf delogo=x=806:y=20:w=70:h=80:show=1
复制代码
```

使用delogo滤镜删除

```
ffmpeg -i test.flv -vf delogo=x=806:y=20:w=70:h=80 output.flv
复制代码
```

#### 视频裁剪

```
ffmpeg -i VR.mov  -vf crop=in_w-200:in_h-200 -c:v libx264 -c:a copy -video_size 1280x720 vr_new.mp4

//crop 格式：crop=out_w:out_h:x:y
//•	out_w: 输出的宽度。可以使用 in_w 表式输入视频的宽度。
//•	out_h: 输出的高度。可以使用 in_h 表式输入视频的高度。
//•	x : X坐标
//•	y : Y坐标
//如果 x和y 设置为 0,说明从左上角开始裁剪。如果不写是从中心点裁剪。
复制代码
```

#### 倍速播放

```
ffmpeg -i out.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" speed2.0.mp4

//-filter_complex 复杂滤镜，[0:v]表示第一个（文件索引号是0）文件的视频作为输入。setpts=0.5*PTS表示每帧视频的pts时间戳都乘0.5 ，也就是差少一半。[v]表示输出的别名。音频同理就不详述了。
//map 可用于处理复杂输出，如可以将指定的多路流输出到一个输出文件，也可以指定输出到多个文件。"[v]" 复杂滤镜输出的别名作为输出文件的一路流。上面 map的用法是将复杂滤镜输出的视频和音频输出到指定文件中。
复制代码
```

#### 对称视频

```
ffmpeg  -i out.mp4 -filter_complex "[0:v]pad=w=2*iw[a];[0:v]hflip[b];[a][b]overlay=x=w" duicheng.mp4

//hflip为水平翻转  vflip为垂直翻转
复制代码
```

#### 画中画

```
ffmpeg -i out.mp4 -i out1.mp4 -filter_complex "[1:v]scale=w=176:h=144:force_original_aspect_ratio=decrease[ckout];[0:v][ckout]overlay=x=W-w-10:y=0[out]" -map "[out]" -movflags faststart new.mp4
复制代码
```

## 音视频拼接与裁剪

#### 裁剪

```
ffmpeg -i out.mp4 -ss 00:00:00 -t 10 out1.mp4

-ss : 指定开始裁剪的实践
-t : 裁剪后的时长
复制代码
```

#### 合并

创建filelist.txt文件

```
file '1.flv'
file '2.flv'
file '3.flv'
复制代码
```

然后执行命令

```
ffmpeg -f concat -i filelist.txt -c copy output.flv
复制代码
```

## 视频与图片转换

#### 视频转jpeg

```
ffmpeg -i test.flv -r 1 -f image2 image-%3d.jpeg
复制代码
```

#### 视频转gif

```
ffmpeg -i out.mp4 -ss 00:00:00 -t 10 out.gif
复制代码
```

#### 图片合并为视频

```
ffmpeg  -f image2 -i image-%3d.jpeg images.mp4
复制代码
```

关注下面的标签，发现更多相似文章



https://juejin.im/post/5e13f53ae51d45414c769c2e#heading-39