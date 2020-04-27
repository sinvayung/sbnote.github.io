# Android内存调试工具总结

## 索引[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#_1)

- 系统内存分析, 所有进程内存分析
  - 基本的[logcat](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#logcat)输出中可能包含的GC相关信息, 可以作为系统或某些应用内存状况的参考依据.
  - 在SystemServer启动的情况下, 还可以通过 [dumpsys meminfo](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#meminfo_sys) 从framework层角度查看系统内存的状况, 该部分信息与从系统角度获取的信息存在差异.
  - 对于需要排序并查找内存占用最多的进程, 推荐使用命令 [procrank](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procrank)
  - 在实在缺少工具, 或者RD知道需要什么信息的情况下, 可以查看[/proc/meminfo](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#meminfo)
  - 如果需要连续监控系统的状态(内存/CPU等), 可以考虑工具[vmstat](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#vmstat)
  - 如果需要从共享库或者共享内存的角度分析其内存占用的情况, 可以考虑用 [librank](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#librank), 当然, 如果存在host端的分析工具, 则该工具的输出可以顶替[procrank](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procrank)和[procmem](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procmem).
  - 如果需要查看系统中哪些共享文件别通过缺页错误的方式读到内存, 可以使用工具[dumpcache](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#dumpcache)
  - 如果实在不知道bug原因或者问题可能跟自己无关, 建议使用 [bugreport](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#bugreport), 供其他RD协助分析问题.
- 指定应用(dalvik进程)内存分析
  - [dumpsys meminfo 应用内存](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#meminfo_app) 输出当前进程/应用的所有内存占用情况. 建议只针对dalvik层的进程.
- 指定native进程内存分析
  - native的单个进程内存分析建议使用 [procmem](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procmem)和 [showmap](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#showmap). [showmap](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#showmap) 额外输出了进程的虚拟地址空间, 可以辅助查看由于虚拟地址空间引起的内存问题.
- 应用内存泄露
  - 少部分的泄露, 比如数据库/activity等, 通过[dumpsys meminfo 应用内存](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#meminfo_app), 但只能知道存在泄露.
  - 应用在开启 [strictmode](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#strictmode) 的情况下, 可以发现更多的资源泄露情况. 但仅限于发现.
  - 一个比较推荐的用于定义应用内存泄露的工具是 [LeakCanary](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#LeakCanary)
- native进程内存泄露
  - [基于bionic的内存泄露分析工具](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#mem_leak), 该工具对于RD使用要求偏高.
- bugreport 信息分析
  - 见外部文档.

## 基础概念[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#_2)

```
VSS - Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
RSS - Resident Set Size 实际使用物理内存（包含共享库占用的内存）
PSS - Proportional Set Size 实际使用的物理内存, USS + 比例分配共享库占用的内存（[与其他进程共享的内存(RSS - USS)] / [分享共享内存的进程数量]）.
USS - Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
```

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-0.png) ![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-1.png) ![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-2.png) ![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-3.png)


如果看进程独占内存，　则使用USS. 但是一般考虑到共享内存的情况, 大部分都是依据PSS查看对应进程的内存占用. 

```
shared clean: 干净的共享数据, 也就是说, 当前有多个进程的虚拟地址指向该物理空间, 且当前进程空间该数据与disk上一致.
shared dirty: 脏共享数据, 与上面对应, 该进程空间的共享数据与disk上数据不一致.
private clean: 进程私有干净数据, 与disk数据一致.
private dirty: 进程私有脏数据, 与disk数据不一致.
```

## 系统内存信息分析[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#_3)

### logcat 输出 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#logcat)

#### dalvik日志打印[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#dalvik)

场景: 在应用随机出现慢时, 可以看看那段时间logcat的输出, 是否包含GC的一些信息. GC可能会导致应用慢, 而系统发起的GC则意味着内存不够, 可能出现从磁盘加载的情况.

在logcat中会打印dalvik的垃圾回收信息.

```
D/dalvikvm: <GC_Reason> <Amount_freed>, <Heap_stats>, <External_memory_stats>, <Pause_time>
D/dalvikvm( 9050): GC_CONCURRENT freed 2049K, 65% free 3571K/9991K, external 4703K/5261K, paused 2ms+2ms
```


**GC_Reason**: 
`GC_CONCURRENT` 在您的堆开始占用内存时可以释放内存的并发垃圾回收。 `GC_FOR_MALLOC` 堆已满而系统不得不停止您的应用并回收内存时，您的应用尝试分配内存而引起的垃圾回收。`GC_HPROF_DUMP_HEAP` 当您请求创建 HPROF 文件来分析堆时出现的垃圾回收。 `GC_EXPLICIT` 显式垃圾回收，例如当您调用 gc() 时（您应避免调用，而应信任垃圾回收会根据需要运行）。`GC_EXTERNAL_ALLOC` 这仅适用于 API 级别 10 及更低级别（更新版本会在 Dalvik 堆中分配任何内存）。外部分配内存的垃圾回收（例如存储在原生内存或 NIO 字节缓冲区中的像素数据）。 
**Amount_freed**: 
从此次垃圾回收中回收的内存量。 

**Heap_stats**: 

堆的可用空间百分比与（活动对象数量）/（堆总大小）。


**External_memory_stats**: 

API 级别 10 (Android3.0 以下)及更低级别的外部分配内存（已分配内存量）/（发生回收的限值）. 而新API中, 统一由dalvik管理.


**Pause_time** 

堆越大，暂停时间越长。并发暂停时间显示了两个暂停：一个出现在回收开始时，另一个出现在回收快要完成时。 

#### art日志打印[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#art)

与 Dalvik 不同，ART 不会为未明确请求的垃圾回收记录消息。只有在认为垃圾回收速度较慢时才会打印垃圾回收。更确切地说，仅在垃圾回收暂停时间超过 5ms 或垃圾回收持续时间超过 100ms 时。如果应用未处于可察觉的暂停进程状态，那么其垃圾回收不会被视为较慢。始终会记录显式垃圾回收。

```
I/art: <GC_Reason> <GC_Name> <Objects_freed>(<Size_freed>) AllocSpace Objects, <Large_objects_freed>(<Large_object_size_freed>) <Heap_stats> LOS objects, <Pause_time(s)>

I/art : Explicit concurrent mark sweep GC freed 104710(7MB) AllocSpace objects, 21(416KB) LOS objects, 33% free, 25MB/38MB, paused 1.230ms total 67.216ms
```

**GC_Reason**: 

`Concurrent` 不会暂停应用线程的并发垃圾回收。此垃圾回收在后台线程中运行，而且不会阻止分配。 `Alloc` 您的应用在堆已满时尝试分配内存引起的垃圾回收。在这种情况下，分配线程中发生了垃圾回收。 `Explicit` 由应用明确请求的垃圾回收，例如，通过调用 gc() 或 gc()。与 Dalvik 相同，在 ART 中，最佳做法是您应信任垃圾回收并避免请求显式垃圾回收（如果可能）。不建议使用显式垃圾回收，因为它们会阻止分配线程并不必要地浪费 CPU 周期。如果显式垃圾回收导致其他线程被抢占，那么它们也可能会导致卡顿（应用中出现间断、抖动或暂停）。 `NativeAlloc` 原生分配（如位图或 RenderScript 分配对象）导致出现原生内存压力，进而引起的回收。`CollectorTransition` 由堆转换引起的回收；此回收由运行时切换垃圾回收引起。回收器转换包括将所有对象从空闲列表空间复制到碰撞指针空间（反之亦然）。当前，回收器转换仅在以下情况下出现：在 RAM 较小的设备上，应用将进程状态从可察觉的暂停状态变更为可察觉的非暂停状态（反之亦然）。 `HomogeneousSpaceCompact` 齐性空间压缩是空闲列表空间到空闲列表空间压缩，通常在应用进入到可察觉的暂停进程状态时发生。这样做的主要原因是减少 RAM 使用量并对堆进行碎片整理。 `DisableMovingGc` 这不是真正的垃圾回收原因，但请注意，发生并发堆压缩时，由于使用了 GetPrimitiveArrayCritical，回收遭到阻止。一般情况下，强烈建议不要使用 GetPrimitiveArrayCritical，因为它在移动回收器方面具有限制。 `HeapTrim` 这不是垃圾回收原因，但请注意，堆修剪完成之前回收会一直受到阻止。 

**GC_Name**: 

ART 具有可以运行的多种不同的垃圾回收。 

`Concurrent mark sweep (CMS)` 整个堆回收器，会释放和回收映像空间以外的所有其他空间。`Concurrent partial mark sweep` 几乎整个堆回收器，会回收除了映像空间和 zygote 空间以外的所有其他空间。 `Concurrent sticky mark sweep` 生成回收器，只能释放自上次垃圾回收以来分配的对象。此垃圾回收比完整或部分标记清除运行得更频繁，因为它更快速且暂停时间更短。 `Marksweep + semispace` 非并发、复制垃圾回收，用于堆转换以及齐性空间压缩（对堆进行碎片整理）。 

**Objects_freed**:

此次垃圾回收从非大型对象空间回收的对象数量。

**Size_freed**:

此次垃圾回收从非大型对象空间回收的字节数量。

**Large_objects_freed**:

此次垃圾回收从大型对象空间回收的对象数量。

**Large_object_size_freed**:

此次垃圾回收从大型对象空间回收的字节数量。

**Heap_stats**

空闲百分比与（活动对象数量）/（堆总大小）。

**Pause_time(s)**

通常情况下，暂停时间与垃圾回收运行时修改的对象引用数量成正比。当前，ART CMS 垃圾回收仅在垃圾回收即将完成时暂停一次。移动的垃圾回收暂停时间较长，会在大部分垃圾回收期间持续出现。

### android自带工具[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#android_1)

#### dumpsys meminfo [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#dumpsys-meminfo)

https://developer.android.com/studio/profile/investigate-ram.html http://gityuan.com/2016/01/02/memory-analysis-command/

场景: 查看dalvik等区域内存情况.

```
root@zx1800:/data # dumpsys meminfo
Applications Memory Usage (kB):                                           --- 以下内存单位
Uptime: 618252294 Realtime: 618252294                                     --- Realtime: 系统启动开始计时, 包含休眠, 准确性依赖驱动实现. 在驱动无实现时, 使用Uptime.
                                                                          --- Uptime: 系统启动开始计时, 不包含休眠.

Total PSS by process:                                                     --- 所有进程 PSS 占用排序
    24712 kB: system (pid 445)
    19600 kB: com.china_liantong.upgrade (pid 2660)
    17500 kB: com.china_liantong.video (pid 3002 / activities)
    11100 kB: com.china_liantong.oam (pid 999)
    10627 kB: com.china_liantong.channelmanagerservice (pid 961)
     8733 kB: com.china_liantong.live.service.LiveService (pid 2086)
     8394 kB: com.china_liantong.ocnadservice (pid 942)
     7622 kB: com.android.systemui (pid 677)
     6708 kB: dhcpcd (pid 639)
     6541 kB: com.china_liantong.epg (pid 1235)
     6286 kB: android.process.media (pid 2041)
     5691 kB: com.china_liantong.airsharingservice (pid 2063)
     4466 kB: dvbserver (pid 211)
     4041 kB: mediaserver (pid 196)
     3890 kB: com.china_liantong.xmppservice (pid 887)
     3354 kB: com.china_liantong.tvmediaplayerservice (pid 905)
     3239 kB: com.china_liantong.launcher:SettingContentProvider (pid 1165)
     2466 kB: surfaceflinger (pid 183)
     2214 kB: com.china_liantong.inputmethod.pinyin (pid 773)
     2122 kB: com.china_liantong.dtvsyskeyservice (pid 980)
     1955 kB: logd (pid 178)
     1943 kB: com.china_liantong.tvframe (pid 1066)
     1847 kB: com.china_liantong.playback (pid 923)
     1640 kB: zygote (pid 220)
      615 kB: sdcard (pid 1698)
      473 kB: netd (pid 191)
      415 kB: sysinfod (pid 184)
      392 kB: vold (pid 182)
      364 kB: developed (pid 222)
      356 kB: adbd (pid 224)
      350 kB: sh (pid 12684)
      285 kB: /init (pid 1)
      279 kB: dvbresourceserver (pid 210)
      261 kB: sdcard (pid 223)
      258 kB: avsettingd (pid 215)
      240 kB: sh (pid 1325)
      164 kB: ueventd (pid 159)
      135 kB: keystore (pid 201)
       82 kB: servicemanager (pid 181)
       81 kB: installd (pid 199)
       76 kB: healthd (pid 179)
       62 kB: lmkd (pid 180)
       26 kB: drmserver (pid 195)
       26 kB: systemtaskd (pid 202)
       22 kB: frontpaneld (pid 207)
       15 kB: common_time (pid 189)
       15 kB: frontpadserver (pid 216)
       15 kB: dcaseventsvr (pid 219)
        9 kB: sh (pid 190)
        9 kB: debuggerd (pid 192)

Total PSS by OOM adjustment:                                              --- 以OOM类别划分(TODO: 每个类别依据和含义)
    26301 kB: Native
                6708 kB: dhcpcd (pid 639)
                4466 kB: dvbserver (pid 211)
                4041 kB: mediaserver (pid 196)
                2466 kB: surfaceflinger (pid 183)
                1955 kB: logd (pid 178)
                1640 kB: zygote (pid 220)
                 615 kB: sdcard (pid 1698)
                 473 kB: netd (pid 191)
                 415 kB: sysinfod (pid 184)
                 392 kB: vold (pid 182)
                 364 kB: developed (pid 222)
                 356 kB: adbd (pid 224)
                 350 kB: sh (pid 12684)
                 285 kB: /init (pid 1)
                 279 kB: dvbresourceserver (pid 210)
                 261 kB: sdcard (pid 223)
                 258 kB: avsettingd (pid 215)
                 240 kB: sh (pid 1325)
                 164 kB: ueventd (pid 159)
                 135 kB: keystore (pid 201)
                  82 kB: servicemanager (pid 181)
                  81 kB: installd (pid 199)
                  76 kB: healthd (pid 179)
                  62 kB: lmkd (pid 180)
                  26 kB: drmserver (pid 195)
                  26 kB: systemtaskd (pid 202)
                  22 kB: frontpaneld (pid 207)
                  15 kB: common_time (pid 189)
                  15 kB: frontpadserver (pid 216)
                  15 kB: dcaseventsvr (pid 219)
                   9 kB: sh (pid 190)
                   9 kB: debuggerd (pid 192)
    24712 kB: System
               24712 kB: system (pid 445)
    48956 kB: Persistent
               11100 kB: com.china_liantong.oam (pid 999)
               10627 kB: com.china_liantong.channelmanagerservice (pid 961)
                8394 kB: com.china_liantong.ocnadservice (pid 942)
                7622 kB: com.android.systemui (pid 677)
                3890 kB: com.china_liantong.xmppservice (pid 887)
                3354 kB: com.china_liantong.tvmediaplayerservice (pid 905)
                2122 kB: com.china_liantong.dtvsyskeyservice (pid 980)
                1847 kB: com.china_liantong.playback (pid 923)
    27280 kB: Foreground
               17500 kB: com.china_liantong.video (pid 3002 / activities)
                6541 kB: com.china_liantong.epg (pid 1235)
                3239 kB: com.china_liantong.launcher:SettingContentProvider (pid 1165)
     1943 kB: Visible
                1943 kB: com.china_liantong.tvframe (pid 1066)
     2214 kB: Perceptible
                2214 kB: com.china_liantong.inputmethod.pinyin (pid 773)
     6286 kB: Home
                6286 kB: android.process.media (pid 2041)
    34024 kB: B Services  (注释: 老旧的, 不太可能被使用到的服务进程)
               19600 kB: com.china_liantong.upgrade (pid 2660)
                8733 kB: com.china_liantong.live.service.LiveService (pid 2086)
                5691 kB: com.china_liantong.airsharingservice (pid 2063)

Total PSS by category:                                               --- 以 category 划分
    49530 kB: Native
    35318 kB: Dalvik
    26569 kB: .so mmap
    17158 kB: .oat mmap
    16357 kB: .art mmap
     8144 kB: .dex mmap
     6671 kB: Stack
     2822 kB: Dalvik Other
     2635 kB: Other mmap
     2160 kB: .ttf mmap
     1892 kB: Other dev
     1581 kB: Unknown
      843 kB: .apk mmap
       36 kB: EGL mtrack
        0 kB: Cursor
        0 kB: Ashmem
        0 kB: Gfx dev
        0 kB: .jar mmap
        0 kB: GL mtrack
        0 kB: Other mtrack

Total RAM: 443652 kB (status critical)
 Free RAM: 137634 kB (40310 cached pss + 9492 cached kernel + 87832 free)
 Used RAM: 168782 kB (131406 used pss + 37376 kernel)
 Lost RAM: 137236 kB
     ZRAM: 10684 kB physical used for 32252 kB in swap (196604 kB total swap)
           压缩后内存占用             被压缩内存
      KSM: 39500 kB saved from shared 5844 kB
           85420 kB unshared; 99276 kB volatile
   Tuning: 96 (large 96), oom 10240 kB, restore limit 3413 kB (low-ram)
```

#### procrank [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procrank)

场景: 查看各个进程的PSS/USS 并比较

```
shell@zx1800:/ # procrank
  PID       Vss      Rss      Pss      Uss  cmdline
  884   589628K   89320K   30444K   23128K  com.china_liantong.launcher
  447   617060K   74620K   25695K   20904K  system_server
 1139   572780K   61160K   14848K   10160K  com.china_liantong.browserreceiver
  209   125160K   25312K   13834K   12696K  /system/bin/dvbserver
 1180   549556K   65992K   12433K    6192K  com.china_liantong.upgrade
  807   554556K   48092K    9636K    7160K  com.china_liantong.ocnadservice
  222   516596K   54256K    8960K    3152K  zygote
  864   547692K   47220K    8431K    6024K  com.china_liantong.oam
  827   552092K   46208K    8180K    5840K  com.china_liantong.channelmanagerservice
  223    71580K   18580K    7156K    3928K  /system/bin/developed
  955   529948K   44620K    6591K    4000K  com.china_liantong.epg
  534   525112K   41324K    6233K    3816K  com.android.systemui
  516   523764K   39424K    5949K    3884K  android.process.media
  183    55092K   17936K    5935K    4284K  /system/bin/surfaceflinger
 1066   525392K   41296K    5140K    2712K  com.china_liantong.live.service.LiveService
  771   529900K   40224K    4864K    2888K  com.china_liantong.tvmediaplayerservice
  753   525476K   37228K    4681K    2804K  com.china_liantong.xmppservice
  201    53500K   12232K    4421K    3460K  /system/bin/mediaserver
 1206   521008K   36324K    4288K    2580K  com.china_liantong.mytv
  979   527892K   36256K    4201K    2080K  com.china_liantong.launcher:SettingContentProvider
 1095   526240K   36480K    4145K    2368K  com.china_liantong.airsharingservice
  601   518952K   37128K    3898K    1984K  com.china_liantong.inputmethod.pinyin
  789   526912K   32468K    3309K    1832K  com.china_liantong.playback
 1048   520468K   32616K    2799K     968K  com.china_liantong.live
  846   525972K   32620K    2787K    1336K  com.china_liantong.dtvsyskeyservice
 1252   519376K   31716K    2687K    1260K  com.china_liantong.video
  907   524920K   32120K    2676K    1236K  com.china_liantong.tvframe
  511    19896K    5168K    2350K    1208K  /system/bin/dhcpcd
  210    25496K    6480K    1662K    1316K  /system/bin/avsettingd
  178    18252K    2596K    1509K    1476K  /system/bin/logd
  199    23564K    4880K    1273K    1004K  /system/bin/drmserver
  217    18936K    2864K     826K     740K  /system/bin/frontpadserver
  182    19568K    3176K     816K     636K  /system/bin/vold
  205    12508K    2804K     718K     572K  /system/bin/keystore
  184    16580K    2580K     681K     536K  /system/bin/sysinfod
  197    21796K    1672K     538K     480K  /system/bin/netd
 2135     9192K    1100K     532K     520K  procrank
  189    17484K    1748K     481K     420K  /system/bin/common_time
  208    17492K    1792K     479K     436K  /system/bin/dvbresourceserver
  220    16400K    1672K     434K     388K  /system/bin/dcaseventsvr
  225    16980K     508K     416K     416K  /sbin/adbd
  224    15412K    1048K     356K     336K  /system/bin/sdcard
 1434     9324K    1020K     338K     244K  sh
  186    14820K     428K     336K     332K  /sbin/watchdog
    1     8860K     396K     327K     316K  /init
 1428     9324K    1008K     326K     232K  /system/bin/sh
  206    14460K    1036K     310K     288K  /system/bin/systemtaskd
  203     9412K    1012K     272K     248K  /system/bin/installd
  207    14456K     992K     266K     244K  /system/bin/frontpaneld
  179     9828K     316K     260K     256K  /sbin/healthd
  180    10624K    1664K     184K     116K  /system/bin/lmkd
  181     9460K     792K      98K      76K  /system/bin/servicemanager
  198    10056K    1108K      64K      28K  /system/bin/debuggerd
  160     8852K      56K      11K       4K  /sbin/ueventd
                           ------   ------  ------
                          230106K  155544K  TOTAL

RAM: 443652K total, 38684K free, 0K buffers, 98768K cached, 1384K shmem, 21560K slab
```

#### cat /proc/meminfo [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#cat-procmeminfo)

场景: 系统内存详细信息

```
shell@zx1800:/ # cat /proc/meminfo                                             
MemTotal:         443652 kB                      --- 系统可见的总物理内存
MemFree:           38584 kB                      --- 系统中未使用的物理内存
MemAvailable:     125556 kB                      --- 可用内存 = MemFree + Cached + Buffers
Buffers:               0 kB                      --- 用于文件缓冲的内存大小
Cached:            98768 kB                      --- 用于高速缓存器占用的内存大小
SwapCached:          128 kB                      --- 用于高速缓存器占用的swap大小
Active:           143160 kB                      --- 活跃使用中的内存, 一般不会回收. = anon + file
Inactive:          87104 kB                      --- 最近未被使用的内存, 可以被回收. = anon + file
Active(anon):      94348 kB
Inactive(anon):    38532 kB
Active(file):      48812 kB
Inactive(file):    48572 kB
Unevictable:           0 kB                      
Mlocked:               0 kB
HighTotal:             0 kB                      
HighFree:              0 kB
LowTotal:         443652 kB
LowFree:           38584 kB
SwapTotal:        196604 kB                      --- swap分区大小
SwapFree:         193784 kB                      --- swap分区剩余空间
Dirty:                 0 kB                      
Writeback:             0 kB
AnonPages:        131492 kB                      --- 匿名页
Mapped:            90688 kB                      --- map的内存
Shmem:              1384 kB                      --- 共享内存, 跟文件无关的
Slab:              21604 kB                      --- kernel slab分配器
SReclaimable:       5464 kB
SUnreclaim:        16140 kB
KernelStack:        5424 kB                      --- 内核栈
PageTables:         7932 kB                      --- 管理页的数据结构大小
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:      418428 kB
Committed_AS:    8764944 kB
VmallocTotal:     565248 kB
VmallocUsed:       55952 kB
VmallocChunk:     472068 kB
```

#### vmstat [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#vmstat)

场景: 监控系统状态.

该工具可以查看系统内存信息, 进程队列, 系统切换, CPU时间占比等信息, 周期性动态输出.

```
procs  memory                       system          cpu              
 r  b    free mapped   anon   slab    in   cs  flt  us ni sy id wa ir
 0  0   38628  90844 131992  21688  5268 10257    0   5  0  6 99  0  0
 0  0   38628  90844 132008  21688  5271 10367    0   8  0  9 99  0  0
 0  0   38628  90844 132048  21688  5150 10497    0  10  1  8 99  0  0
 0  0   38628  90844 132100  21688  5112 10180    0   8  0  3 99  0  0
 0  0   38628  90844 132120  21688  5221 10289    0   8  0  4 99  0  0
```

总共15列参数, 个参数含义如下:

- procs(进程)
  - r: Running队列中进程数, 这个值超过cpu个数就会出现cpu瓶颈.
  - b: IO wait 的进程数, 该值过大, 可能是等待文件操作的进程多或者文件读写慢.
- memory(内存)
  - free: 可用内存大小
  - mapped: mmap映射的内存大小
  - anon: 匿名内存大小, 一般由malloc引起, 或者匿名mmap.
  - slab: slab的内存大小.
- system(系统)
  - in: 每个间隔时间的中断次数(包括时钟中断), 这个值越大, 内核消耗的cpu时间越多.需要查看`/proc/interrupts`下中断增长情况.
  - cs: 每个间隔时间上下文切换的次数
  - flt: major page faults. 需要从disk读取数据的缺页错误.
- CPU (处理器)
  - us: user time, 比较高时，说明用户进程消耗的cpu时间多.
  - ni: nice time, 被降低优先级的进程在用户模式下的执行CPU时间百分比.
  - sy: system time, 系统内核消耗的CPU百分比
  - id: idle time, 系统空闲时间百分比
  - wa: iowait time, CPU在等待IO完成时间占比
  - ir: interrupt time, 系统中断耗时占CPU百分比

更多更详细的信息, 请直接查看 `/proc/vmstat`http://blog.csdn.net/macky0668/article/details/6839498

#### librank [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#librank)

场景: 与procrank互补使用, 是procmem的扩展. 显示所有进程的信息, 需要工具统计分类. 也可以用来查看每个库或共享文件真实占用的内存大小.

数据来源与procmem一样, 但是procmem针对的是单个进程的内存占用情况. 而librank是显示某个库或者文件被哪些进程共享, 并显示占用大小. 如下图所示.

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-4.png)![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-5.png)![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-6.png)

#### dumpcache [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#dumpcache)

该工具是android7.0之后才有的工具,用于查看文件系统中有每个文件被cache到内存的大小. 该文件可以用来判断缺页错误时加载的文件.

在Launcher界面时的输出如下:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-7.png)

稳定播放1080P视频时:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-8.png)

按下遥控器确定键显示UI时:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-9.png)

对比, 可以知道在播放过程中, 显示UI时主要加载的文件是:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-10.png)

#### bugreport 信息分析 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#bugreport)

Android系统想要成为一个功能完备，生态繁荣的操作系统，那就必须提供完整的应用开发环境。而在应用开发中，app程序的调试分析是日常生产中进程会进行的工作。Android为了方便开发人员分析整个系统平台和某个app在运行一段时间之内的所有信息，专门开发了bugreport工具。


该工具的缺点是: 1. 耗时过长, 只能抓取当前状态. 2. 抓取过程中可能导致系统异常, 因为其oom会被调高, 在内存不足时导致系统其他应用被kill. 3. 由于bugreport的权限会降低到shell, 而很多服务在会拒绝dumpsys的操作, 导致部分信息无法抓取. 



使用方法:

1. 通过bugreport命令抓取一份bugreport原始的文本log： `shell# bugreport&gt;/data/local/tmp/bugreport.txt`
2. 将上面命令抓取的bugreport.txt文本文件拷贝出来，上传到bugreport分析服务器上面，服务器会自动生成系统当前状态快照，上传方法如下： a. 通过浏览器进入服务器地址：http://10.27.254.108:8080/,如下图：

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-11.png)

b. 点击broswer浏览report.txt文本文件，然后点击upload按钮上传文件，上传后，系统会自动生成系统状态快照，快照名称对应到上传时间，点击快照名称进入系统分析页面，如下：

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-12.png)

**该网页服务器的dockerfile如下:**

```
FROM ubuntu:14.04
 MAINTAINER wertherzhang <werther0331@gmail.com>

 RUN apt-get update

 RUN apt-get -y install openjdk-7-jdk openjdk-7-jre
 RUN apt-get -y install python

 RUN mkdir -p /root/chkbugreport
 RUN apt-get -y install wget
 RUN wget http://10.27.8.54/chkbugreport.tgz -O /root/chkbugreport.tgz
 RUN tar xvf /root/chkbugreport.tgz -C /tmp/
 RUN mkdir -p /root/bin

 ADD server.py /root/chkbugreport/
 ADD chkbugreport.jar /root/bin/
 ADD chkbugreport /usr/local/bin/
 ADD ddmlib.jar /root/bin/

 RUN apt-get clean

 ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64
 ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
 WORKDIR /root/chkbugreport/

 CMD ["python", "server.py"]
```

附件: [chkbugreport-server.zip](https://pengzhang.netlify.com/assets/images/Android-memory-debug-13.png)

## 应用内存分析[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#_4)

### android自带工具[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#android_2)

#### dumpsys meminfo 应用内存 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#dumpsys-meminfo_1)

场景: 查看java进程的不同类别内存占用情况, 特别是确定activity是否泄露等信息.

命令 `dumpsys meminfo com.china_liantong.launcher -d`

输出:

```
shell@zx1800:/ # dumpsys meminfo com.china_liantong.launcher -d                
Applications Memory Usage (kB):
Uptime: 2612261 Realtime: 2612261

** MEMINFO in pid 884 [com.china_liantong.launcher] **
                   Pss  Private  Private  Swapped     Heap     Heap     Heap
                 Total    Dirty    Clean    Dirty     Size    Alloc     Free
                ------   ------   ------   ------   ------   ------   ------
  Native Heap     5915     5440        0        0    24576    16208     8367
  Dalvik Heap    13764    13364        0        0    26989    20896     6093
 Dalvik Other      248      248        0        0                           
        Stack      513      512        0        0                           
    Other dev        4        0        4        0                           
     .so mmap     3392      424      472        0                           
    .apk mmap       94        0        4        0                           
    .ttf mmap     1573        0      568        0                           
    .dex mmap     1188        0      752        0                           
    .oat mmap     1419        0      260        0                           
    .art mmap      979      616        0        0                           
   Other mmap       80        4        0        0                           
   EGL mtrack       17       17        0        0                           
      Unknown      134      128        0        0                           
        TOTAL    29320    20753     2060        0    51565    37104    14460

 Objects
               Views:     1192         ViewRootImpl:        1
         AppContexts:        3           Activities:        1
              Assets:        2        AssetManagers:        2
       Local Binders:       41        Proxy Binders:      220
       Parcel memory:        7         Parcel count:       14
    Death Recipients:       10      OpenSSL Sockets:        0

 SQL
         MEMORY_USED:        0
  PAGECACHE_OVERFLOW:        0          MALLOC_SIZE:        0
```

`Native Heap`: native分配占用的RAM, 通过malloc申请的内存. `Heap Size` 是内存池总大小(向系统申请的内存大小). `Heap Alloc` 已经申请的内存大小(应用向dlmalloc申请的内存). `Heap Free` 内存池剩余可分配内存大小.

`Dalvik Heap`: 应用中Dalvi分配占用的RAM. `Pss Total`: 包含所有Zygote分配(通过进程间共享占用). `Private Dirty`: 仅分配到应用的实际RAM, 由应用分配或者zygote分配页, 这些页自从zygote fork应用进程后被修改过.

`.so map` 和 `.dex map`: mmap的.so和.dex(Dalvik或ART)代码占用的RAM. `Pss Total` 数值包括应用之间共享的平台代码；`Private Clean` 是您的应用自己的代码。通常情况下，实际映射的内存更大 - 此处的 RAM 仅为应用执行的代码当前所需的 RAM。不过，.so mmap 具有较大的私有脏 RAM，因为在加载到其最终地址时对原生代码进行了修改(GOT?!)。 

`.oat mmap`: 代码映像占用的 RAM 量，根据多个应用通常使用的预加载类计算。此文件在所有应用之间共享，不受特定应用影响。 

`.art mmap`: 堆占用的 RAM 量，根据多个应用通常使用的预加载类计算。此映像在所有应用之间共享，不受特定应用影响。尽管 ART 映像包含 Object 实例，它仍然不会计入您的堆大小。 

`Unknown`: 系统无法将其分类到其他更具体的一个项中的任何 RAM 页。 其 `Pss Total` 与 Zygote共享.

`TOTAL`: 上方所有 PSS 字段的总和。表示您的进程占用的内存量占整体内存的比. `Private Dirty` 和 `Private Clean` 是您的进程中的总分配，未与其他进程共享。它们（尤其是 Private Dirty）等于您的进程被破坏后将释放回系统中的 RAM 量。`Dirty`因为已被修改而必须保持在 RAM 中的 RAM 页（因为没有交换）；`Clean` 是已从某个持久性文件（例如正在执行的代码）映射的 RAM 页，如果一段时间不用，可以移出分页。

`ViewRootImpl`: 进程中当前活动的根视图数量。每个根视图都与一个窗口关联，因此有助于确定涉及对话框或其他窗口的内存泄漏。 

`AppContexts` 和 `Activities`: 当前活动的应用 Context 和 Activity 对象数量。快速确定由于存在静态引用（比较常见）而无法进行垃圾回收的已泄漏 Activity 对象。这些对象经常拥有很多关联的其他分配，因此成为跟踪大型内存泄漏的一种不错的方式。

例子见内存泄露部分.

#### procmem  [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#procmem)

场景: 查看指定进程的各部分内存占用情况. 命令: `procmem <pid>` 例子: `procmem 2509` 数据来源: `/proc/<pid>/maps` 和 `/proc/<pid>/pagemap`

```
Vss Rss Pss Uss ShCl ShDi PrCl PrDi Name
```

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-14.png)

各字段含义:

```
ShCl  --  shared clean
ShDi  --  shared dirty
PrCl  --  private clean
PrDi  --  private dirty
```

#### showmap [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#showmap)

场景: 进程虚拟进程空间的内存分配情况 和 详细的干净脏数据信息.

从 `/proc/[pid]/smaps` 获取数据并统计的工具.

命令: `showmap [-a] [-t] [-v] <pid>` 例子: `showmap -a 884` 输出单位: KB

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-15.png)

由于现在内核都使用了动态内存分配的机制, 在大量申请小内存的情况下, 从系统看内存有剩余, 但是进程却无法分配出需要的内存, 这就有可能是由于虚拟地址的内存碎片引起, 无法找到一段大于所请求内存大小的地址空间. 

例子:

#### Android 应用 OOM[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#android-oom)

触发OOM的原因是, java层内存分配失败了.

造成内存分配失败的可能原因如下:

- 内存溢出. 申请的内存超出了虚拟机最大内存.
- 碎片, 导致无法找到连续空间满足申请的内存大小.
- 资源问题, 比如文件节点超过限制, 导致匿名内存申请出错, 错误信息为 "Too many open files"
- 虚拟空间地址空间被占满, 导致OOM.

以上为网上的结论, 在android5.1.1上测试发现:

**fd问题并不会导致OOM**

代码复用下面内存泄露的代码,在asynctask中执行文件打开操作.

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-16.png)

logcat中输出如下, 并没有OOM输出:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-17.png)

但是这段代码的确证明了打开文件太多会导致shmem创建失败.

## 内存泄露分析[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#_5)

### activity 泄露 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#activity)

activity 的泄露基于android自带工具, 可以快速确定, 但是具体泄露的activity, 需要依赖工具 LeakCanary.

代码:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-18.png)

界面:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-19.png)

在第一次进入该应用时:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-20.png)

按下BUTTON, 然后退出应用:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-21.png)

第二次进入该应用:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-22.png)

第二次按下BUTTON:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-23.png)

第二次退出应用:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-24.png)

基于 `dumpsys meminfo` 确认应用有activity泄露后, 单纯通过UI操作基本也可以判断出来哪个activity泄露, 更准确的泄露检测工具是 LeakCanary, 该工具为第三方工具. 具体用法: https://www.liaohuqiu.net/cn/posts/leak-canary-read-me/

还是以上的例子, 额外增加如下代码. 

在MainActivity增加如下代码, 该代码的含义是, 在activity触发onDestroy时, 监控该activity对象.

```
    @Override
    protected void onDestroy() {
        super.onDestroy();
        LeakApplication.getRefWatcher().watch(this);

    }
```

增加application, 如下:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-25.png)

编译运行, 执行上面同样的操作. 在通知中心有如下显示:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-26.png)

点击后可以查看详细的堆栈:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-27.png)

同样在logcat中有如下输出:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-28.png)

### StrictMode检测应用内存泄露 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#strictmode)

同样是上面的例子, 修改代码如下, 增加strickmode的调用:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-29.png)

同样的上面操作方法, logcat中有如下输出:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-30.png)

### 基于libc调试内存泄露 [¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#libc)

内存泄露的检测依据是, 进程退出时, 还有未释放的内存. 所以, valgrind包括bionic libc中, 能精确检测到泄露的前提条件就是进程退出. 但是这个对于系统级别的进程是无用的, 因为系统级进程并不会退出. 从RD角度, 判断系统级进程是否泄露的依据是内存是否持续增长, 特别是在压力测试的情况下. 所以, 这个部分介绍的工具, 实际上是抓取了持续增长的内存信息, 这些信息, 可能是内存泄露, 也可能是进程正常申请的内存, 需要RD介入判断.

附件: [Memleak_tools_android.zip](https://pengzhang.netlify.com/assets/images/no-permission-to-download-this-tool.zip)

依赖工具:

- `libc_malloc_debug_leak.so` , bionic源码下, 需要编译并push到系统中
- `libmemleakutils.so`, 从android提取并更改. 从附件源码下载编译, 需要push到系统中.
- addr2func.py, 该脚本能自动将地址转换成库和堆栈. 在附件中.
- memincrease.py, 该脚本能将上一脚本的输出, 进行统计排序, 按内存增加从大到小排序. 基本最顶上的是存在问题的. 在附件中.

局限:

- 只能调试native进程.
- 进程不能重启.
- 需要压力测试, 长时间运行
- 需要RD介入判断是否存在泄露.

用法:

1. 将libmemleakutils.so库链接到被调试程序中, 调用函数`start_memleak_watcher(memstep)`, 其中memstep表示, pss每增加memstep, 则抓取一次当前内存分配信息.
2. 将libmemleakutils.so 和 `libc_malloc_debug_leak.so` push到/system/lib/下.
3. 将被调试程序push到 /system/bin/ 下.
4. 设置 property `libc.debug.malloc.program` 为 你的调试进程名字.
5. 设置 property `libc.debug.malloc` 为 1
6. stop 或者 kill 被调试进程.
7. start 或者 启动 被调试进程.
8. 压力测试后, 检查 /data/local/tmp/ 底下存在文件 `mem_snapshot_$pid_$memsize.log`, 且个数大于2个(越多越好).
9. `cp /proc/${pid}/maps /data/local/tmp/`
10. 将 /data/local/tmp/ 底下所有文件复制到host机器.
11. 用 diff 命令比较 两个 `mem_snapshot_$pid_$memsize.log`, 并保存输出为 `diff_$pid_$memsize1_$memsize2.log`
12. 执行 `./addr2func.py --root-dir=/remote/ANDROID/hdtv/ --maps-file=./maps --product=zx2000 diff_$pid_$memsize1_$memsize2.log > mem_stack_$pid_$memsize1_$memsize2.log`, 该过程是将diff生成文件中的所有地址转换成库和堆栈信息.
13. 执行 `./memincrease.py mem_stack_$pi_$memsize1_$memsize2.log incr_$pid_$memsize1_$memsize2.log`, 该过程是对12生成的文件进行统计排序, 从大到小排序.

例子:

![img](https://pengzhang.netlify.com/assets/images/Android-memory-debug-32.png)

运行一会儿后, 在 /data/local/tmp/目录下存在文件:

```
mem_snapshot_2158_1.log
mem_snapshot_2158_2.log
mem_snapshot_2158_3.log
mem_snapshot_2158_4.log
```

其内容如下:

```
 Allocation count 5
 Total memory 6293072
size  5242880, dup    1, 0xb6ed36b2, 0xb6f4cd4e, 0xb6f1da44, 0xb6f1de38, 0xb6f1dea0, 0xb6f5104a, 0xb6f4ef92
size  1048576, dup    1, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc8492, 0xb6fc8390, 0xb6f4ce68, 0xb6fc8400
size     1024, dup    1, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc84aa, 0xb6fc8394, 0xb6f4ce68, 0xb6fc8400
size      580, dup    1, 0xb6ed36b2, 0xb6ed391c, 0xb6f4cd0e, 0xb6f510c8, 0xb6f1decc, 0xb6fc838c, 0xb6f4ce68, 0xb6fc8400
size       12, dup    1, 0xb6ed36b2, 0xb6ed391c, 0xb6f4cd0e, 0xb6f14c46, 0xb6f1dd98, 0xb6f1dea0, 0xb6f5104a, 0xb6f4ef92
```

执行diff命令:

```
# diff ./mem_snapshot_2158_1.log ./mem_snapshot_2158_2.log > diff_2158_1_2.log
# 
# diff ./mem_snapshot_2158_3.log ./mem_snapshot_2158_4.log > diff_2158_3_4.log
#
```

得到一个PSS从1M增长到2M和3M增长到4M的两个diff文件. 内容如下:

```
2c2
<  Total memory 6293072
---
>  Total memory 7342672
4,5c4,5
< size  1048576, dup    1, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc8492, 0xb6fc8390, 0xb6f4ce68, 0xb6fc8400
< size     1024, dup    1, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc84aa, 0xb6fc8394, 0xb6f4ce68, 0xb6fc8400
---
> size  1048576, dup    2, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc8492, 0xb6fc8390, 0xb6f4ce68, 0xb6fc8400
> size     1024, dup    2, 0xb6ed36b2, 0xb6f4cd4e, 0xb6fc84aa, 0xb6fc8394, 0xb6f4ce68, 0xb6fc8400
```


执行 addr2func.py :

```
# ./addr2func.py --root-dir=/remote/ANDROID/hdtv/ --maps-file=./maps --product=zx2000 diff_2158_3_4.log > mem_stack_2158_3_4.log
```

生成文件内容如下:

```
2c2                                                                                                                                                                              [0/59466]

<  Total memory 8392272

---

>  Total memory 9441872

4,5c4,5

< size  1048576, dup    3,
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:11
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:25 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
< size     1024, dup    3,
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test1(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:17
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:26 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
---

> size  1048576, dup    4,
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:11
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:25 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
> size     1024, dup    4,
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test1(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:17
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:26 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
```

所有的地址被转换成了队长. 
最后执行 memincrease.py :

```
./memincrease.py mem_stack_2158_3_4.log incr_2158_3_4.log
```

生成的文件 incr_2158_3_4.log 内容如下:

```
Memory increase 1048576 bytes                   ### 内存增加了 1048576 bytes
98990365afa0d71d62949620cc7e3753f386e4e3
old size 1048576 count 3, total memory 3145728       ### 从 3145728
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:11
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:25 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
98990365afa0d71d62949620cc7e3753f386e4e3
new size 1048576 count 4, total memory 4194304      ### 增加到 4194304
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:11
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:25 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?

Memory increase 1024 bytes
833f23c991cc75facaa41fb74f7466b91c27917b
old size 1024 count 3, total memory 3072
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test1(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:17
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:26 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
833f23c991cc75facaa41fb74f7466b91c27917b
new size 1024 count 4, total memory 4096
    leak_malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_leak.cpp:315 (discriminator 1)
    malloc, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/malloc_debug_common.cpp:259
    mem_test1(), /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:17
    main, /home/werther/workspace/ANDROID/hdtv/pdk/memleak/main.cpp:26 (discriminator 1)
    __libc_init, /home/werther/workspace/ANDROID/hdtv/bionic/libc/bionic/libc_init_dynamic.cpp:113
    _start, main.cpp:?
```

基本上, 将最顶上的几个堆栈确认下是否内存泄露即可.

特别注意:

- 类泄露时, 在堆栈上的表现是其成员内存泄露. 需要查看堆栈是否有该类对象的new方法, 并且该方法是否在多处存在.

### valgrind 调试内存泄露[¶](https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D#valgrind)

场景: 对于可退出的进程进行调试比较合适, 可以对应用的native代码进行调试.

目前hdtv代码上的 valgrind 无法获取被调试进程的堆栈, 只能获取它自己库的堆栈, 存在问题. 暂时无法使用.

https://pengzhangdev.github.io/Android-memory-debug/?nsukey=51bo38V797T9bIZtnqae1pe8N7U6foNUBkZLeOFk4GZ%2BUoFEDmMOshrTrOwC%2Fy0HByIi8JSyOlkA3Vw3b86en5MvUkr3SZJGF7QJbiI9snbu75dlz%2BWeuAAwChVVVLNxoZwRGXnBKnKewo3tJvUmbwfrvDGckSrjS1g6YlXy0Xlf0BUycYDu31bufbBzxC3Y0TBwpMckSTWzEbvgztgebg%3D%3D

