查看是否启动 

```
cat /proc/kallsyms | grep register_kprobe
```

### 一、kprobe简介

kprobe是一个动态地收集调试和性能信息的工具，它从Dprobe项目派生而来，是一种非破坏性工具，用户用它几乎可以跟踪任何函数或被执行的指令以及一些异步事件（如timer）。它的基本工作机制是：用户指定一个探测点，并把一个用户定义的处理函数关联到该探测点，当内核执行到该探测点时，相应的关联函数被执行，然后继续执行正常的代码路径。

kprobe实现了三种类型的探测点: kprobes, jprobes和kretprobes (也叫返回探测点)。 kprobes是可以被插入到内核的任何指令位置的探测点，jprobes则只能被插入到一个内核函数的入口，而kretprobes则是在指定的内核函数返回时才被执行。

一般，使用kprobe的程序实现作一个内核模块，模块的初始化函数来负责安装探测点，退出函数卸载那些被安装的探测点。kprobe提供了接口函数（APIs）来安装或卸载探测点。

### 二、kprobe实现原理

当安装一个kprobes探测点时，kprobe首先备份被探测的指令，然后使用断点指令(即在i386和x86_64的int3指令)来取代被探测指令的头一个或几个字节。当CPU执行到探测点时，将因运行断点指令而执行trap操作，那将导致保存CPU的寄存器，调用相应的trap处理函数，而trap处理函数将调用相应的notifier_call_chain（内核中一种异步工作机制）中注册的所有notifier函数，kprobe正是通过向trap对应的notifier_call_chain注册关联到探测点的处理函数来实现探测处理的。当kprobe注册的notifier被执行时，它首先执行关联到探测点的pre_handler函数，并把相应的kprobe struct和保存的寄存器作为该函数的参数，接着，kprobe单步执行被探测指令的备份，最后，kprobe执行post_handler。等所有这些运行完毕后，紧跟在被探测指令后的指令流将被正常执行。

### 三、kprobe的接口函数

#### 1. kprobe的注册与解除函数

```
#include <linux/kprobes.h>
int register_kprobe(struct kprobe *p);
void unregister_kprobe(struct kprobe *p);
```

#### 2. kprobe结构体

```
struct kprobe {
    /* location of the probe point */
    kprobe_opcode_t *addr;
    /* Allow user to indicate symbol name of the probe point */
    const char *symbol_name;
    /* Offset into the symbol */
    unsigned int offset;
    /* Called before addr is executed. */
    kprobe_pre_handler_t pre_handler;
    /* Called after addr is executed, unless... */
    kprobe_post_handler_t post_handler;
    /* copy of the original instruction */
    struct arch_specific_insn ainsn;
    //...
};
```

函数的查找

```
#include <linux/kallsyms.h> 
/* Lookup the address for a symbol. Returns 0 if not found. */
unsigned long kallsyms_lookup_name(const char *name);
```

必须启用 CONFIG_KALLSYMS 编译内核

一个探测点处理函数能够修改被探测函数的上下文，如修改内核数据结构，寄存器等。因此，kprobe可以用来安装bug解决代码或注入一些错误或测试代码。

其中pre_handler与post_handler的函数原型，如下：

```
#include <linux/kprobes.h>
#include <linux/ptrace.h>
int pre_handler(struct kprobe *p, struct pt_regs *regs);
void post_handler(struct kprobe *p, struct pt_regs *regs, unsigned long flags);
```

寄存器结构体（以32位的系统为例）：

```
struct pt_regs {
    long uregs[18];
};
```

```
#define ARM_cpsr    uregs[16]    //存储状态寄存器的值
#define ARM_pc        uregs[15]    //存储当前的执行地址
#define ARM_lr        uregs[14]    //存储返回地址
#define ARM_sp        uregs[13]    //存储当前的栈顶地址
#define ARM_ip        uregs[12]
#define ARM_fp        uregs[11]    //帧指针
#define ARM_r10        uregs[10]
#define ARM_r9        uregs[9]
#define ARM_r8        uregs[8]
#define ARM_r7        uregs[7]
#define ARM_r6        uregs[6]
#define ARM_r5        uregs[5]
#define ARM_r4        uregs[4]
#define ARM_r3        uregs[3]    //(函数调用时)第4个参数
#define ARM_r2        uregs[2]    //(函数调用时)第3个参数
#define ARM_r1        uregs[1]    //(函数调用时)第2个参数
#define ARM_r0        uregs[0]    //(函数调用时)第1个参数，或返回值
#define ARM_ORIG_r0    uregs[17]
```

寄存器的修改：

堆栈的修改：

```
SYSCALL_DEFINE3(write, unsigned int, fd, const char __user *, buf, size_t, count)
{
    struct fd f = fdget_pos(fd);
    ssize_t ret = -EBADF;

    if (f.file) {
        loff_t pos = file_pos_read(f.file);
        ret = vfs_write(f.file, buf, count, &pos);
        if (ret >= 0)
            file_pos_write(f.file, pos);
        fdput_pos(f);
    }

    return ret;
}
```

参考： 
 <https://www.kernel.org/doc/Documentation/kprobes.txt>