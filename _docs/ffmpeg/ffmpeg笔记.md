---
title: 录屏
description: 录屏
---

#### 录屏

```sh
ffmpeg -f avfoundation -i 1 -r 30 out.yuv
ffmpeg -f avfoundation -i 1 -r 30 out.mp4
```

- -f：指定使用avfoundation采集数据
- -i：指定从哪采集数据，它是一个文件索引号，在MAC上，1代表桌面，0代表摄像头
- -r，-framerate：指定帧率

> 从LOG中找到pixel_format为uyvy422， video_size为3360x2100，此两值在播放时要用到
>
> ```verilog
> Input #0, avfoundation, from '1':
>   Duration: N/A, start: 76899.671833, bitrate: N/A
> Stream #0:0: Video: rawvideo (UYVY / 0x59565955), uyvy422, 3360x2100, 1000k tbr, 1000k tbn, 1000k tbc
> ```



#### 播放

```sh
ffplay -pixel_format uyvy422 -video_size 3360x2100 out.yuv
ffplay out.mp4
```

- -pixel_format，简-pix_fmt
- -video_size

> 错误1：Picture size 0x0 is invalid out.yuv: Invalid argument
>
> 原因：YUV是纯RAW数据，必须指定-video_size才能播放

> 错误2：播放花屏现象
>
> 原因：YUV是纯RAW数据, 需要指定pixel_format

> 通过YUV文件无法知道视频真实的pixel_format值和video_size的值，此两值在录屏时打印的LOG中可以看到。ffplay之前，需事先知道此两值才行。



#### 查看视频文件信息

```sh
ffmpeg -i out.mp4
```

> 部分LOG:
>
> ```verilog
>     Stream #0:0(und): Video: mpeg4 (Simple Profile) (mp4v / 0x7634706D), yuv420p, 3360x2100 [SAR 1:1 DAR 8:5], 5729 kb/s, 30 fps, 30 tbr, 15360 tbn, 30 tbc (default)
> ```



#### 裁剪视频区域

```sh
ffmpeg -i input.mp4 -vf "crop=1000:800:1000:1000" out.mp4
# 注：pixel_format变成了1000x800
ffmpeg -i out.mp4 -vf "crop=iw/3:ih/3:1000:1000" out2.mp4
# 注：iw表示输入视频的宽度，ih表示输入视频的高度
```

- `crop=w:h:x:y`, 分别表示裁剪框的宽、高、X坐标，Y坐标。



#### 改变视频比例

```sh
ffmpeg -i in.mp4 -aspect 4:3 out.mp4
# 并没有改变pixel_format，而是将画面拉伸了或压缩了的效果
```



#### 裁剪视频片段（按时间）

```sh
ffmpeg -i input.mp4 -ss 00:00:10 -codec copy -t 30 out.mp4
```

- -ss, 指定视频片段的开始时间
- -t, 指定视频片段的持续时间，单位为秒



### 增加Padding

```sh
ffmpeg -i input.mp4 -vf "pad=iw:ih+500:0:(oh-ih)/2:black" out.mp4
# 注：iw表示输入视频的宽度，ih表示输入视频的高度, ow表示输出视频的宽度，oh表示输出视频的高度
```

- `pad=w:h:x:y`, 分别表示增加Padding之后的宽、高、X坐标、Y坐标



#### 改变视频播放速度（音频不受影响）

```sh
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" out6.mp4 
```



#### 加字幕



> 附：SRT字幕格式，示例：
>
> ```.srt
> 5
> 00:00:45,590 --> 00:00:48,120
> 那段时间我经常会梦到自己在飞翔
> I started having these dreams of flying.
> 
> 6
> 00:00:49,740 --> 00:00:51,520
> 终获自由
> I was free.
> ```
>
> 每一个字幕段，包含以下部分：
>
> - 字幕序号
> - 字幕显示的起始时间
> - 字幕内容（可多行）
> - 空白行（表示本字幕段的结束）



#### 格式转换



#### 尺寸转换



#### 区域裁剪



#### 加字幕



#### 加声音





#### 参考：

[偶遇FFmpeg(二)——常用命令]: https://www.jianshu.com/p/c5bfd55a312d

