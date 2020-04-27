---
title: 深入理解Davilk字节码指令及Smali文件
description: 深入理解Davilk字节码指令及Smali文件
---

# 深入理解Davilk字节码指令及Smali文件

今天来介绍有关Davilk虚拟机相关的知识,首先便是介绍我们最关心的Davilk字节码相关知识,进而深入到Android逆向领域.之所以写这篇文章,是因为有姑娘要学习这,再加上网上的许多资料太过零散和片面,当然,更重要的是为以前做个总结.

可以关注我看心情更新的博客[江湖人称小白哥](https://link.jianshu.com/?t=http://blog.csdn.net/dd864140130/article/)

------

# Davilk描述符

与JVM相类似,Davilk字节码中同样有一套用于描述类型,方法,字段的方法,这些方法结合Davilk的指令便形成了完整的汇编代码.

## 字节码和数据类型

Davilk字节码只有两种类型:基本类型和引用类型.对象和数组都是引用类型,Davilk中对字节码类型的描述和JVM中的描述符规则一致:对于基本类型和无返回值的void类型都是用一个大写字母表示,对象类型则用字母L加对象的全限定名来表示.数组则用[来表示,具体规则如下所示:

> 全限定名是什么
> 以String为例,其完整名称是java.lang.String,那么其全限定名就是`java/lang/String;`,即java.lang.String的"."用"/"代替,并在末尾添加分号";"做结束符.

| java类型 | 类型描述符 |
| -------- | ---------- |
| boolean  | Z          |
| byte     | B          |
| short    | S          |
| char     | C          |
| int      | I          |
| long     | J          |
| float    | F          |
| double   | D          |
| void     | V          |
| 对象类型 | L          |
| 数组类型 | [          |

这里我们重点解释对象类型和数组类型:

### 对象类型

L可以表示java类型中的任何类.在java代码中以package.name.ObjectName的方式引用,而在Davilk中其描述则是以`Lpackage/name/ObjectName;`的形式表示.L即上面定义的java类类型,表示后面跟着的是累的全限定名.比如java中的java.lang.String对应的描述是`Ljava/lang/String;`.

### 数组类型

[类型用来表示所有基本类型的数组,[后跟着是基本类型的描述符.每一维度使用一个前置的[.
比如java中的int[] 用汇编码表示便是`[I;`.二维数组int[][]为`[[I;`,三维数组则用`[[[I;`表示.

对于对象数组来说,[后跟着对应类的全限定符.比如java当中的String[]对应的是`[java/lang/String;`.

## 字段的描述

Davilk中对字段的描述分为两种,对基本类型字段的描述和对引用类型的描述,但两者的描述格式一样:
`对象类型描述符->字段名:类型描述符;`
比如com.sbbic.Test类中存在String类型的name字段及int类型的age字段,那么其描述为:

```
Lcom/sbbic/Test;->name:Ljava/lang/String;
Lcom/sbbic/test;->age:I
```

## 方法的描述

java中方法的签名包括方法名,参数及返回值,在Davilk相应的描述规则为:
`对象类型描述符->方法名(参数类型描述符)返回值类型描述符`

下面我们通过几个例子来说明,以java.lang.String为例:

```
java方法:public char charAt(int index){...}
Davilk描述:Ljava/lang/String;->charAt(I)C

java方法:public void getChars(int srcBegin,int srcEnd,char dst[],int dstBegin){...}
Davilk描述:Ljava/lang/String;->getChars(II[CI)V

java方法:public boolean equals(Object anObject){...}
Davilk描述:Ljava/lang/String;->equals(Ljava/lang/Object)Z
```

------

# Davilk指令集

掌握以上的字段和方法的描述,只能说我们懂了如何描述一个字段和方法,而关于方法中具体的逻辑则需要了解Dalvik中的指令集.因为Dalvik是基于寄存器的架构的,因此指令集和JVM中的指令集区别较大,反而更类似x86的中的汇编指令.

## 数据定义指令

数据定义指令用于定义代码中使用的常量,类等数据,基础指令是const

| 指令                         | 描述                                        |
| ---------------------------- | ------------------------------------------- |
| const/4 vA,#+B               | 将数值符号扩展为32后赋值给寄存器vA          |
| const-wide/16 vAA,#+BBBB     | 将数值符号扩展为64位后赋值个寄存器对vAA     |
| const-string vAA,string@BBBB | 通过字符串索引高走字符串赋值给寄存器vAA     |
| const-class vAA,type@BBBB    | 通过类型索引获取一个类的引用赋值给寄存器vAA |

## 数据操作指令

move指令用于数据操作,其表示move destination,source,即数据数据从source寄存器(源寄存器)移动到destionation寄存器(源寄存器),可以理解java中变量间的赋值操作.根据字节码和类型的不同,move指令后会跟上不同的后缀.

| 指令                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| move vA,vB             | 将vB寄存器的值赋值给vA寄存器,vA和vB寄存器都是4位             |
| move/from16 vAA,VBBBB  | 将vBBBB寄存器(16位)的值赋值给vAA寄存器(7位),from16表示源寄存器vBBBB是16位的 |
| move/16 vAAAA,vBBBB    | 将寄存器vBBBB的值赋值给vAAAA寄存器,16表示源寄存器vBBBB和目标寄存器vAAAA都是16位 |
| move-object vA,vB      | 将vB寄存器中的对象引用赋值给vA寄存器,vA寄存器和vB寄存器都是4位 |
| move-result vAA        | 将上一个invoke指令(方法调用)操作的单字(32位)非对象结果赋值给vAA寄存器 |
| move-result-wide vAA   | 将上一个invoke指令操作的双字(64位)非对象结果赋值给vAA寄存器  |
| mvoe-result-object vAA | 将上一个invoke指令操作的对象结果赋值给vAA寄存器              |
| move-exception vAA     | 保存上一个运行时发生的异常到vAA寄存器                        |

## 对象操作指令

与对象实例相关的操作,比如对象创建,对象检查等.

| 指令                          | 描述                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| `new-instance vAA,type@BBBB`  | 构造一个指定类型的对象将器引用赋值给vAA寄存器.此处不包含数组对象 |
| `instance-of vA,vB,type@CCCC` | 判断vB寄存器中对象的引用是否是指定类型,如果是,将v1赋值为1,否则赋值为0 |
| `check-cast vAA,type@BBBB`    | 将vAA寄存器中对象的引用转成指定类型,成功则将结果赋值给vAA,否则抛出ClassCastException异常. |

## 数组操作指令

在实例操作指令中我们并没有发现创建对象的指令.Davilk中设置专门的指令用于数组操作.

| 指令                          | 说明                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| new-array vA,vB,type@CCCC     | 创建指定类型与指定大小(vB寄存器指定)的数组,并将其赋值给vA寄存器 |
| fill-array-data vAA,+BBBBBBBB | 用指定的数据填充数组,vAA代表数组的引用(数组的第一个元素的地址) |

## 数据运算指令

数据运算主要包括两种:算数运算和逻辑运算.
**1. 算术运算指令**

| 指令     | 说明     |
| -------- | -------- |
| add-type | 加法指令 |
| sub-type | 减法指令 |
| mul-type | 乘法指令 |
| div-type | 除法指令 |
| rem-type | 求       |

**2. 逻辑元算指令**

| 指令     | 说明         |
| -------- | ------------ |
| and-type | 与运算指令   |
| or-type  | 或运算指令   |
| xor-type | 异或元算指令 |

**3. 位移指令**

| 指令      | 说明           |
| --------- | -------------- |
| shl-type  | 有符号左移指令 |
| shr-type  | 有符号右移指令 |
| ushr-type | 无符号右移指令 |

上面的-type表示操作的寄存器中数据的类型,可以是-int,-float,-long,-double等.

## 比较指令

比较指令用于比较两个寄存器中值的大小,其基本格式格式是`cmp+kind-type vAA,vBB,vCC`,type表示比较数据的类型,如-long,-float等;kind则代表操作类型,因此有`cmpl,cmpg,cmp`三种比较指令.coml是compare less的缩写,cmpg是compare greater的缩写,因此cmpl表示vBB小于vCC中的值这个条件是否成立,是则返回1,否则返回-1,相等返回0;cmpg表示vBB大于vCC中的值这个条件是否成立,是则返回1,否则返回-1,相等返回0.
cmp和cmpg的语意一致,即表示vBB大于vCC寄存器中的值是否成立,成立则返回1,否则返回-1,相等返回0
来具体看看Davilk中的指令:

| 指令                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `cmpl-float vAA,vBB,vCC`  | 比较两个单精度的浮点数.如果vBB寄存器中的值大于vCC寄存器的值,则返回-1到vAA中,相等则返回0,小于返回1 |
| `cmpg-float vAA,vBB,vCC`  | 比较两个单精度的浮点数,如果vBB寄存器中的值大于vCC的值,则返回1,相等返回0,小于返回-1 |
| `cmpl-double vAA,vBB,vCC` | 比较两个双精度浮点数,如果vBB寄存器中的值大于vCC的值,则返回-1,相等返回0,小于则返回1 |
| `cmpg-double vAA,vBB,vCC` | 比较双精度浮点数,和cmpl-float的语意一致                      |
| `cmp-double vAA,vBB,vCC`  | 等价与cmpg-double vAA,vBB,vCC指令                            |

## 字段操作指令

字段操作指令表示对对象字段进行设值和取值操作,就像是你在代码中长些的set和get方法.基本指令是iput-type,iget-type,sput-type,sget-type.type表示数据类型.

### 普通字段读写操作

前缀是i的iput-type和iget-type指令用于字段的读写操作.

| 指令                        | 说明                                                 |
| --------------------------- | ---------------------------------------------------- |
| iget-byte vX,vY,filed_id    | 读取vY寄存器中的对象中的filed_id字段值赋值给vX寄存器 |
| iput-byte vX,vY,filed_id    | 设置vY寄存器中的对象中filed_id字段的值为vX寄存器的值 |
| iget-boolean vX,vY,filed_id |                                                      |
| iput-boolean vX,vY,filed_id |                                                      |
| iget-long vX,vY,filed_id    |                                                      |
| iput-long vX,vY,filed_id    |                                                      |

### 静态字段读写操作

前缀是s的sput-type和sget-type指令用于静态字段的读写操作

| 指令                        | 说明 |
| --------------------------- | ---- |
| sget-byte vX,vY,filed_id    |      |
| sput-byte vX,vY,filed_id    |      |
| sget-boolean vX,vY,filed_id |      |
| sput-boolean vX,vY,filed_id |      |
| sget-long vX,vY,filed_id    |      |
| sput-long vX,vY,filed_id    |      |

## 方法调用指令

Davilk中的方法指令和JVM的中指令大部分非常类似.目前共有五条指令集:

| 指令                                        | 说明                                                         |
| ------------------------------------------- | ------------------------------------------------------------ |
| `invoke-direct{parameters},methodtocall`    | 调用实例的直接方法,即private修饰的方法.此时需要注意{}中的第一个元素代表的是当前实例对象,即this,后面接下来的才是真正的参数.比如指令invoke-virtual {v3,v1,v4},Test2.method5:(II)V中,v3表示Test2当前实例对象,而v1,v4才是方法参数 |
| `invoke-static{parameters},methodtocall`    | 调用实例的静态方法,此时{}中的都是方法参数                    |
| `invoke-super{parameters},methodtocall`     | 调用父类方法                                                 |
| `invoke-virtual{parameters},methodtocall`   | 调用实例的虚方法,即public和protected修饰修饰的方法           |
| `invoke-interface{parameters},methodtocall` | 调用接口方法                                                 |

这五种指令是基本指令,除此之外,你也会遇到invoke-direct/range,invoke-static/range,invoke-super/range,invoke-virtual/range,invoke-interface/range指令,该类型指令和以上指令唯一的区别就是后者可以设置方法参数可以使用的寄存器的范围,在参数多于四个时候使用.

> 再此强调一遍对于非静态方法而言{}的结构是{当前实例对象,参数1,参数2,...参数n},而对于静态方法而言则是{参数1,参数2,...参数n}

需要注意,如果要获取方法执行有返回值,需要通过上面说道的move-result指令获取执行结果.

## 方法返回指令

在java中,很多情况下我们需要通过Return返回方法的执行结果,在Davilk中同样提供的return指令来返回运行结果:

| 指令              | 说明                       |
| ----------------- | -------------------------- |
| return-void       | 什么也不返回               |
| return vAA        | 返回一个32位非对象类型的值 |
| return-wide vAA   | 返回一个64位非对象类型的值 |
| return-object vAA | 反会一个对象类型的引用     |

## 同步指令

同步一段指令序列通常是由java中的synchronized语句块表示,则JVM中是通过monitorenter和monitorexit的指令来支持synchronized关键字的语义的,而在Davilk中同样提供了两条类似的指令来支持synchronized语义:

| 指令              | 说明                 |
| ----------------- | -------------------- |
| monitor-enter vAA | 为指定对象获取锁操作 |
| monitor-exit vAA  | 为指定对象释放锁操作 |

## 异常指令

很久以前,VM也是用过jsr和ret指令来实现异常的,但是现在的JVM中已经抛出原先的做法,转而采用异常表来实现异常.而Davilk仍然使用指令来实现:

| 指令      | 说明                          |
| --------- | ----------------------------- |
| throw vAA | 抛出vAA寄存器中指定类型的异常 |

## 跳转指令

跳转指令用于从当前地址条状到指定的偏移处,在if,switch分支中使用的居多.Davilk中提供了goto,packed-switch,if-test指令用于实现跳转操作

| 指令                          | 操作                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| `goto +AA`                    | 无条件跳转到指定偏移处(AA即偏移量)                           |
| `packed-switch vAA,+BBBBBBBB` | 分支跳转指令.vAA寄存器中的值是switch分支中需要判断的,BBBBBBBB则是偏移表(packed-switch-payload)中的索引值, |
| `spare-switch vAA,+BBBBBBBB`  | 分支跳转指令,和packed-switch类似,只不过BBBBBBBB偏移表(spare-switch-payload)中的索引值 |
| `if-test vA,vB,+CCCC`         | 条件跳转指令,用于比较vA和vB寄存器中的值,如果条件满足则跳转到指定偏移处(CCCC即偏移量),test代表比较规则,可以是eq.lt等. |

在条件比较中,if-test中的test表示比较规则.该指令用的非常多,因此我们简单的坐下说明:

| 指令                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| `if-eq vA,vB,target` | vA,vB寄存器中的相等,等价于java中的if(a==b),比如if-eq v3,v10,002c表示如果条件成立,则跳转到current position+002c处.其余的类似 |
| `if-ne vA,vB,target` | 等价与java中的if(a!=b)                                       |
| `if-lt vA,vB,target` | vA寄存器中的值小于vB,等价于java中的if(a`<`b)                 |
| `if-gt vA,vB,target` | 等价于java中的if(a`>`b)                                      |
| `if-ge vA,vB,target` | 等价于java中的if(a`>=`b)                                     |
| `if-le vA,vB,target` | 等价于java中的if(a`<=`b)                                     |

除了以上指令之外,Davilk还提供可一个零值条件指令,该指令用于和0比较,可以理解为将上面指令中的vB寄存器的值固定为0.

| 指令              | 说明                             |
| ----------------- | -------------------------------- |
| if-eqz vAA,target | 等价于java中的if(a==0)或者if(!a) |
| if-nez vAA,target | 等价于java中的if(a!=0)或者if(a)  |
| if-ltz vAA,target | 等价于java中的if(a`<`0)          |
| if-gtz vAA,target | 等价于java中的if(a`>`0)          |
| if-lez vAA,target | 等价于java中的if(a`<=`0)         |
| if-gtz vAA,target | 等价于java中的if(a`>=`0)         |

附:
上面我们说道两张偏移表packed-switch-payload和spare-switch-payload,两者唯一的区别就是表中的值是否有序,后面我们会在下文中进行详细的说明.

## 数据转换指令

数据类型转换对任何java开发者都是非常熟悉的,用于实现两种不同数据类型的相互转换.其基本指令格式是:unop vA,vB,表示对vB寄存器的中值进行操作,并将结果保存在vA寄存器中.

| 指令         | 说明                 |
| ------------ | -------------------- |
| int-to-long  | 整形转为长整型       |
| float-to-int | 单精度浮点型转为整形 |
| int-to-byte  | 整形转为字节类型     |
| neg-int      | 求补指令,对整数求补  |
| not-int      | 求反指令,对整数求反  |

到现在为止,我们对Davilk中的指令做了简单的说明.Davilk的指令在很大程度上结合了x86指令和JVM的指令结构和语意,因此总体来说Davilk中的指令还是非常容易学习.更多更详细的指令参考请参考:[Davilk指令集大全](https://link.jianshu.com/?t=http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html)

------

# 详解smali文件

上面我们介绍了Davilk的相关指令,下面我们则来认识一下smali文件.尽管我们使用java来写Android应用,但是Davilk并不直接加载.class文件,而是通过dx工具将.class文件优化成.dex文件,然后交由Davilk加载.这样说来,我们无法通过分析.class来直接分析apk文件,而是需要借助工具baksmali.jar反编译dex文件来获得对应smali文件,smali文件可以认为是Davilk的字节码文件,但是并两者并不完全等同.

通过baksmali.jar反编译出来每个.smali,都对应与java中的一个类,每个smali文件都是Davilk指令组成的,并遵循一定的结构.smali存在很多的关键词用于描述对应的java文件,所有的关键字都以"."开头,常用的关键词如下:

| 关键词               | 说明                       |
| -------------------- | -------------------------- |
| .filed               | 定义字段                   |
| .method...end method | 定义方法                   |
| .annotation          | 定义注解                   |
| .implements          | 定义接口指令               |
| .local               | 指定了使用的局部变量的个数 |
| .registers           | 指定使用本地寄存器的个数   |
| .prologue            | 表示方法中代码的开始处     |
| .line                | 表示java源文件中指定行     |
| .paramter            | 指定了方法的参数           |

在这里很多人对.local和.register感到困惑,如果你也是请重新看上面的有关寄存器的点.

下面我们就简单的说明一下smali文件的结构:

1. 文件头描述

------

smali文件的前三行描述了当前类的信息:

```
.class <访问权限修饰符> [非权限修饰符] <类名>
.super <父类名>
.source <源文件名称>
```

<>中的内容表示必不可缺的,[]表示的是可选择的.
访问权限修饰符即所谓的public,protected,private即default.而非权限修饰符则指的是final,abstract.
举例说明:

```
.class public final Lcom/sbbic/demo/Device;
.super Ljava/lang/Object;
.source "Device.java"
```

1. 文件正文

------

在文件头之后便是文件的正文,即类的主体部分,包括类实现的接口描述,注解描述,字段描述和方法描述四部分.下面我们就分别看看字段和方法的结构.(别忘了我们在Davilk中说过的方法和字段的表示)

### 接口描述

如果该类实现了某个接口,则会通过.implements定义,其格式如下:

```
#interfaces
.implements <接口名称>
```

举例说明:

```
# interfaces
.implements Landroid/view/View$OnClickListener;
```

smali为其添加了#Interface注释

### 注解描述

如果一个类中使用注解,会用.annotation定义:其格式如下:

```
#annotations
.annotation [注解的属性] <注解类名>
    [注解字段=值]
    ...
.end
```

### 字段描述

smali中使用.field描述字段,我们知道java中分为静态字段(类属性)和普通字段(实例属性),它们在smali中的表示如下:

**1. 普通字段:**

```
#instance fields
.field <访问权限修饰符> [非权限修饰符] <字段名>:<字段类型>
```

访问权限修饰符相比各位已经非常熟了,而此处非权限修饰符则可是final,volidate,transient.
举例说明:

```
# instance fields
.field private TAG:Ljava/lang/String;
```

**2. 静态字段**
静态字段知识在普通字段的的定义中添加了static,其格式如下:

```
#static fields
.field <访问权限> static [修饰词] <字段名>:<字段类型>
```

举例说明:

```
# static fields
.field private static final pi:F = 3.14f
```

需要注意:smali文件还为静态字段,普通字段分别添加#static field和#instan filed注释.

### 方法描述

smali中使用.method描述方法.具体定义格式如下:

**1. 直接方法**
直接方法即所谓的direct methods,还记的Davilk中方法调用指令invoke-direct么?忘记的童鞋自行翻看,这里就不做说明了.

```
#direct methods
.method <访问权限修饰符> [非访问权限修饰符] <方法原型>
      <.locals>
      [.parameter]
      [.prologue]
      [.line]
      <代码逻辑>
.end
```

重点解释一下parameter:
parameter的个数和方法参数的数量相对应,即有几个参数便有几个`.parameter`,默认从1开始,即p1,p2,p2....
熟悉java的童鞋一定会记得该类型的方法有个默认的参数指向当前对象,在smali中,方法的默认对象参数用p0表示.

举例说明:

```
# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    .line 8
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 10
    const-string v0, "MainActivity"

    iput-object v0, p0, Lcom/social_touch/demo/MainActivity;->TAG:Ljava/lang/String;

    .line 13
    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/social_touch/demo/MainActivity;->running:Z

    return-void
.end method
```

需要注意smali为其添加了#direct method注释

**2. 虚方法**
虚方法的定义会和直接方法唯一的不同就是注释不同:#virtual methods,其格式如下:

```
#virtual methods
.method <访问权限> [修饰关键词] <方法原想>
      <.locals>
      [.parameter1]
      [.parameter2]
      [.prologue]
      [.line]
      <代码逻辑>
.end
```

1. 内部类的smali文件结构

------

内部类的smali文件稍有不同,具体表现在内部类对应的smali文件的的文件名为[外部类名称$内部类名称.smali]更详细的说明见下文.

1. 实例演示

------

smali文件的结构也是非常清晰明了的,熟悉之后读起来也是非常不错的.下面我们来看个简单的smali文件.为了方便理解,我们首先贴一段java代码:

```
public class MainActivity extends Activity implements View.OnClickListener {

    private String TAG = "MainActivity";
    private static final float pi = (float) 3.14;

    public volatile boolean running = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    public void onClick(View view) {
        int result = add(4, 5);
        System.out.println(result);

        result = sub(9, 3);

        if (result > 4) {
            log(result);
        }
    }

    public int add(int x, int y) {
        return x + y;
    }

    public synchronized int sub(int x, int y) {
        return x + y;
    }

    public static void log(int result) {
        Log.d("MainActivity", "the result:" + result);
    }


}
```

解析来我们来看该段代码反编译出来的smali,在代码中

```
#文件头描述
.class public Lcom/social_touch/demo/MainActivity;
.super Landroid/app/Activity;#指定MainActivity的父类
.source "MainActivity.java"#源文件名称

#表明实现了View.OnClickListener接口
# interfaces
.implements Landroid/view/View$OnClickListener;

#定义float静态字段pi
# static fields
.field private static final pi:F = 3.14f

#定义了String类型字段TAG
# instance fields
.field private TAG:Ljava/lang/String;

#定义了boolean类型的字段running
.field public volatile running:Z

#构造方法,如果你还纳闷这个方法是怎么出来的化,就去看看jvm的基础知识吧
# direct methods
.method public constructor <init>()V
    .locals 1#表示函数中使用了一个局部变量

    .prologue#表示方法中代码正式开始
    .line 8#表示对应与java源文件的低8行
    #调用Activity中的init()方法
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 10
    const-string v0, "MainActivity"

    iput-object v0, p0, Lcom/social_touch/demo/MainActivity;->TAG:Ljava/lang/String;

    .line 13
    const/4 v0, 0x0

    iput-boolean v0, p0, Lcom/social_touch/demo/MainActivity;->running:Z

    return-void
.end method

#静态方法log()
.method public static log(I)V
    .locals 3
    .parameter "result"#表示result参数

    .prologue
    .line 42
    #v0寄存器中赋值为"MainActivity"
    const-string v0, "MainActivity"
    #创建StringBuilder对象,并将其引用赋值给v1寄存器
    new-instance v1, Ljava/lang/StringBuilder;
    
    #调用StringBuilder中的构造方法
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V
    
    #v2寄存器中赋值为ther result:
    const-string v2, "the result:"
   
    #{v1,v2}大括号中v1寄存器中存储的是StringBuilder对象的引用.
    #调用StringBuilder中的append(String str)方法,v2寄存器则是参数寄存器.
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
   
    #获取上一个方法的执行结果,此时v1中存储的是append()方法执行后的结果,此处之所以仍然返回v1的    #原因在与append()方法返回的就是自身的引用
    move-result-object v1
    
    #继续调用append方法(),p0表示第一个参数寄存器,即上面提到的result参数
    invoke-virtual {v1, p0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
    
    #同上
    move-result-object v1
   
    #调用StringBuilder对象的toString()方法
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    
    #获取上一个方法执行结果,toString()方法返回了一个新的String对象,因此v1中此时存储了String对象的引用
    move-result-object v1
    
    #调用Log类中的静态方法e().因为e()是静态方法,因此{v0,v1}中的成了参数寄存器
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 43
    #调用返回指令,此处没有返回任何值
    return-void
.end method


# virtual methods
.method public add(II)I
    .locals 1
    .parameter "x"#第一个参数
    .parameter "y"#第二个参数

    .prologue
    .line 34
    
    #调用add-int指令求和之后将结果赋值给v0寄存器
    add-int v0, p1, p2
   
    #返回v0寄存器中的值
    return v0
.end method


.method public onClick(Landroid/view/View;)V
    .locals 4
    .parameter "view" #参数view

    .prologue
    const/4 v3, 0x4 #v3寄存器中赋值为4

    .line 23#java源文件中的第23行
    const/4 v1, 0x5#v1寄存器中赋值为5
   
    #调用add()方法
    invoke-virtual {p0, v3, v1}, Lcom/social_touch/demo/MainActivity;->add(II)I
   
    #从v0寄存器中获取add方法的执行结果
    move-result v0

    .line 24#java源文件中的24行
    .local v0, result:I
    
    #v1寄存器中赋值为PrintStream对象的引用out
    sget-object v1, Ljava/lang/System;->out:Ljava/io/PrintStream;
    
    #执行out对象的println()方法
    invoke-virtual {v1, v0}, Ljava/io/PrintStream;->println(I)V

    .line 26
    
    const/16 v1, 0x9#v1寄存器中赋值为9
    const/4 v2, 0x3#v2寄存器中赋值为3
    
    #调用sub()方法,{p0,v1,v2},p0指的是this,即当前对象,v1,v2则是参数
    invoke-virtual {p0, v1, v2}, Lcom/social_touch/demo/MainActivity;->sub(II)I
    #从v0寄存器中获取sub()方法的执行结果
    move-result v0

    .line 28
    if-le v0, v3, :cond_0#如果v0寄存器的值小于v3寄存器中的值,则跳转到cond_0处继续执行

    .line 29
    
    #调用静态方法log()
    invoke-static {v0}, Lcom/social_touch/demo/MainActivity;->log(I)V

    .line 31
    :cond_0
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 1
    .parameter "savedInstanceState" #参数savedInstancestate

    .prologue
    .line 17
   
    #调用父类方法onCreate()
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    .line 18
    
    const v0, 0x7f04001a#v0寄存器赋值为0x7f04001a
   
    #调用方法setContentView()
    invoke-virtual {p0, v0}, Lcom/social_touch/demo/MainActivity;->setContentView(I)V

    .line 19
    return-void
.end method

#declared-synchronized表示该方法是同步方法
.method public declared-synchronized sub(II)I
    .locals 1
    .parameter "x"
    .parameter "y"

    .prologue
    .line 38
    
    monitor-enter p0#为该方法添加锁对象p0
     add-int v0, p1, p2
    #释放锁对象
    monitor-exit p0
  
    return v0
.end method
```

------

# 结束语

仍然感觉有很多点没写明白,后面再做补充吧.

[原文](https://www.jianshu.com/p/80d22f66e042)