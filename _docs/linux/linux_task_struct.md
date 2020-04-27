# 进程描述符

漏洞利用的核心都是通过修改task_struct中的一些字段来达到任意地址读写和提权操作的。

进程描述符task_struct数据结构包含了与一个进程相关的所有信息，在`kernel/include/linux/sched.h`中定义，其中有很多字段是通过预定义形式来定义填充在结构体中，所以在每个系统版本中其数据结构也会不同。

把task_struct中的数据全部打印出来，会看到很多有趣的东西，这些特征可以用来定位重要的结构。

## 定位cred

漏洞提权过程中修改的cred.security信息，需要先定位到cred。

```
+0x4d0 = 0xffffffc0461ce4d0: 0xffffffc0461ce4d0    // cpu_timers[0]
+0x4d8 = 0xffffffc0461ce4d8: 0xffffffc0461ce4d0
+0x4e0 = 0xffffffc0461ce4e0: 0xffffffc0461ce4e0    // cpu_timers[1]
+0x4e8 = 0xffffffc0461ce4e8: 0xffffffc0461ce4e0
+0x4f0 = 0xffffffc0461ce4f0: 0xffffffc0461ce4f0    // cpu_timers[2]
+0x4f8 = 0xffffffc0461ce4f8: 0xffffffc0461ce4f0
+0x500 = 0xffffffc0461ce500: 0xffffffc0101f4900    // real_cred 
+0x508 = 0xffffffc0461ce508: 0xffffffc0101f4900    // cred 
+0x510 = 0xffffffc0461ce510: 0x363130322d657663    // char comm[TASK_COMM_LEN]
+0x518 = 0xffffffc0461ce518: 0x652d333534322d
```

通过cpu_timers的特征就有了通用的定位方法，也是所有提权代码中都用到的：

```
if (task->cpu_timers[0].next == task->cpu_timers[0].prev &&
    task->cpu_timers[1].next == task->cpu_timers[1].prev &&
    task->cpu_timers[2].next == task->cpu_timers[2].prev &&
    (unsigned long)task->cpu_timers[0].next > KERNEL_START &&
    (unsigned long)task->cpu_timers[1].next > KERNEL_START &&
    (unsigned long)task->cpu_timers[2].next > KERNEL_START &&
    task->real_cred == task->cred &&
    (unsigned long)task->cred > KERNEL_START) {
    // do something...
}
```

其中`comm[TASK_COMM_LEN]`字段是进程名，也可以通过这个特征来找到cred，找到进程名的地址，然后减8(x64)就是cred的地址了。

## 遍历进程tasks

task_struct结构中定义了一个list_head类型的tasks。

```
task_struct {
    ...
    struct list_head tasks;
#ifdef CONFIG_SMP
    struct plist_node pushable_tasks;
#endif
    ...
}

struct list_head
{
    struct list_head *next;
    struct list_head *prev;
};
```

list_head为一个双向链表，可以遍历到所有进程的tasks结构。


如何定位到tasks地址?

tasks下边有个预定义变量pushable_tasks，在多核手机总是存在的，第一个值为优先级prio，打印出来，

```
+0x290 = 0xffffffc0461ce290: 0xffffffc000ee05e0    // struct list_head tasks
+0x298 = 0xffffffc0461ce298: 0xffffffc0a98b2290
+0x2a0 = 0xffffffc0461ce2a0: 0x8c    // pushable_tasks.prio
+0x2a8 = 0xffffffc0461ce2a8: 0xffffffc0461ce2a8
+0x2b0 = 0xffffffc0461ce2b0: 0xffffffc0461ce2a8
```

在我目前所看到的值都为0x8c，因此可以通过该值来定位tasks地址。

## bypass selinux

在不考虑selinux保护的时候，提权只需要简单的将security.osid和security.sid置1，这样得到的只是kernel权限，并不是真正的init最高权限。
内核中u:r:kernel:s0始终为1，而u:r:init:s0是变化的，每个内核不同。
因此要获取该值就要先找到init进程的task_struct。

如何定位init进程?

### 内核符号表导出

在`/arch/arm/kernel/init_task.c`中定义有

```
struct task_struct init_task = INIT_TASK(init_task);
```

有些内核会在内核符号表kallsyms中导出init_task地址。

### 遍历内核tasks

在漏洞利用提权过程中，获取的当前进程的task_struct，就能拿到tasks地址，然后遍历所有进程的tasks，通过comm判断是否为init进程。

### 暴力搜索

在task_struct结构中有个几个字段定义了进程的一些特性，其中kernel thread的一些特征值。

```
struct task_struct {
    volatile long state; /* -1 unrunnable, 0 runnable, >0 stopped */
    void *stack; // 2-page (8K) aligned address,栈指针，指向当前thread_info结构。
    atomic_t usage; // 0x2
    unsigned int flags; // 0x200000, I am a kernel thread
    ...
}
```

搜索范围可以通过`/proc/iomem`中的kernel data字段获取，通过这些特征值就可以找到内核进程swapper/0的task_struct结构。

```
for (pos = begin; pos < end; pos += sizeof(unsigned long)) {
    if ( task_struct_buf.stack & 0x1ff == 0 && 
         task_struct_buf.usage == 0x2 && 
         task_struct_buf.flags == 0x200000) {

        printf("\tfound swapper/0 task_struct_address: %lp\n", pos);
        break;
    }

}
```

最后找到tasks依次遍历内核进程定位init进程。

## 父进程

task_struct中通过`struct task_struct __rcu *real_parent`定义了该进程的父进程，通过如下方法可以将父进程改为init进程。

```
void main() {
    int pid = fork();
    if (pid == 0) {
        while (getppid() != 1) {
            sleep(1);
        }
        // do something...
        // my parent is init...
    }
    if (pid > 0) {
      // waitpid(pid, NULL, 0);
    }
    exit(0);
}
```

所以也可以通过这种方法获取init进程的task_struct，至于其他的用处，对方不想说话并向你扔了一头猪。。。

## 内核栈

task_struct中`void *stack`指向当前进程的内核栈，进程通过alloc_thread_info函数分配它的内核栈，通过free_thread_info函数释放所分配的内核栈。

Linux内核通过thread_union联合体来表示进程的内核栈，其中THREAD_SIZE宏的大小为8192。

```
union thread_union {  
    struct thread_info thread_info;  
    unsigned long stack[THREAD_SIZE/sizeof(long)];  
};
```

当进程从用户态切换到内核态时，进程的内核栈总是空的，所以ARM的sp寄存器指向这个栈的顶端。因此，内核能够轻易地通过sp寄存器获得当前正在CPU上运行的进程。
由于堆栈是向下增长的，esp和thread_info位于同一个8KB或者4KB的块当中，也就是thread_union的长度了。
如果是8KB，屏蔽esp的低13位就可以得到thread_info的地址，也就是8KB块的开始位置。4KB的话，就屏蔽低12位。

```
static inline struct thread_info *current_thread_info(void)
{
      register unsigned long sp asm ("sp");
      return (struct thread_info *)(sp & ~(THREAD_SIZE - 1));
}
```

汇编:

```
mov R2, #0xffffe000
and R3, R2, esp  

或 

BIC R3, R2, #0x1FC0
BIC R3, R3, #0x3F
```

thread_info结构中也有很多重要的字段，如进程描述符task，获取任意地址读写能力的addr_limit等。

## 待续

待更…

[原文]( http://blog.idhyt.com/2016/06/09/exploit-process-descriptor/)



# Linux 内核的 thread_info 结构

本文基于Linux 3.5.4源代码。

对每个进程，Linux内核都把两个不同的数据结构紧凑的存放在一个单独为进程分配的内存区域中：一个是内核态的进程堆栈，另一个是紧挨着进程描述符的小数据结构thread_info，叫做线程描述符。在较新的内核代码中，这个存储区域的大小通常为8192个字节（两个页框）。在linux/arch/x86/include/asm/page_32_types.h中，

```c
#define task_thread_info(task)    ((struct thread_info *)(task)->stack)
```

出于效率考虑，内核让这8K空间占据连续的两个页框并让第一个页框的起始地址是213的倍数。

内核态的进程访问处于内核数据段的栈，这个栈不同于用户态的进程所用的栈。用户态进程所用的栈，是在进程线程地址空间中；而内核栈是当进程从用户空间进入内核空间时，特权级发生变化，需要切换堆栈，那么内核空间中使用的就是这个内核栈。因为内核控制路径使用很少的栈空间，所以只需要几千个字节的内核态堆栈。需要注意的是，内核态堆栈仅用于内核例程，Linux内核另外提供了单独的硬中断栈和软中断栈。

下图中显示了在物理内存中存放两种数据结构的方式。线程描述符驻留与这个内存区的开始，而栈顶末端向下增长。 下图摘自ULK3，但是较新的内核代码中，进程描述符task_struct结构中没有直接指向thread_info结构的指针，而是用一个void指针类型的成员表示，然后通过类型转换来访问thread_info结构。相关代码在include/linux/sched.h中：

```c
#define task_thread_info(task)    ((struct thread_info *)(task)->stack)
```

![0_1271584604XTJq.gif](assets/linux_task_struct/ad5acdddf43b4b5910f31151e5ebe113.gif)

在这个图中，esp寄存器是CPU栈指针，用来存放栈顶单元的地址。在80×86系统中，栈起始于顶端，并朝着这个内存区开始的方向增长。从用户态刚切换到内核态以后，进程的内核栈总是空的。因此，esp寄存器指向这个栈的顶端。

一旦数据写入堆栈，esp的值就递减。在Linux3.5.4内核中，thread_info结构是72个字节长（ULK3时代的内核中，这个结构的大小是52个字节），因此内核栈能扩展到8120个字节。thread_info结构的定义如下：

```c
struct thread_info {
    struct task_struct    *task;           /* main task structure */
    struct exec_domain    *exec_domain;    /* execution domain */
    __u32            flags;                /* low level flags */
    __u32            status;               /* thread synchronous flags */
    __u32            cpu;                  /* current CPU */
    int            preempt_count;          /* 0 => preemptable, <0 => BUG */
    mm_segment_t            addr_limit;
    struct restart_block     restart_block;
    void __user             *sysenter_return;
#ifdef CONFIG_X86_32
    unsigned long previous_esp; /* ESP of the previous stack in
                                   case of nested (IRQ) stacks
                                   */
    __u8                supervisor_stack[0];
#endif
    unsigned int        sig_on_uaccess_error:1;
    unsigned int        uaccess_err:1;    /* uaccess failed */
};
```

Linux内核中使用一个联合体来表示一个进程的线程描述符和内核栈：

```c
union thread_union {
    struct thread_info thread_info;
    unsigned long stack[THREAD_SIZE/sizeof(long)];
};
```

下面来说说如何通过esp栈指针来获取当前在CPU上正在运行进程的thread_info结构。实际上，上面提到，thread_info结构和内核态堆栈是紧密结合在一起的，占据两个页框的物理内存空间。而且，这两个页框的起始起始地址是213对齐的。所以，内核通过简单的屏蔽掉esp的低13位有效位就可以获得thread_info结构的基地址了。在文件linux/arch/x86/include/asm/thread_info.h中，有如下代码：

```c
#ifndef __ASSEMBLY__


/* how to get the current stack pointer from C */
register unsigned long current_stack_pointer asm("esp") __used;

/* how to get the thread information struct from C */
static inline struct thread_info *current_thread_info(void)
{
    return (struct thread_info *)
        (current_stack_pointer & ~(THREAD_SIZE - 1));
}

#else /* !__ASSEMBLY__ */

/* how to get the thread information struct from ASM */
#define GET_THREAD_INFO(reg)     \
    movl $-THREAD_SIZE, reg; \
    andl %esp, reg

/* use this one if reg already contains %esp */
#define GET_THREAD_INFO_WITH_ESP(reg) \
    andl $-THREAD_SIZE, reg

#endif
```

在上面的代码中，当前的栈指针current_stack_pointer就是esp，

THREAD_SIZE为8K，二进制的表示为0000 0000 0000 0000 0010 0000 0000 0000。

~(THREAD_SIZE-1)的结果刚好为1111 1111 1111 1111 1110 0000 0000 0000，第十三位是全为零，也就是刚好屏蔽了esp的低十三位，最终得到的是thread_info的地址。

进程最常用的是进程描述符结构task_struct而不是thread_info结构的地址。为了获取当前CPU上运行进程的task_struct结构，内核提供了current宏，该宏本质上等价于current_thread_info()->task，在include/asm-generic/current.h中定义：

```c
#define get_current() (current_thread_info()->task)
#define current get_current()
```

[原文](http://blog.jobbole.com/107656/)