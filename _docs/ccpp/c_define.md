---
title: C语言高级宏技巧
description: C语言高级宏技巧
---

## C语言高级宏技巧

**特殊符号#、##**

**（1）#**

　**When you put a # before an argument in a preprocessor macro, the preprocessor turns that argument into a character array.**

　**在一个宏中的参数前面使用一个#,预处理器会把这个参数转换为一个字符数组**　

　**简化理解：#是“字符串化”的意思，出现在宏定义中的#是把跟在后面的参数转换成一个字符串**

```
#define ERROR_LOG(module)   fprintf(stderr,"error: "#module"\n") //注意2个引号
```

**ERROR_LOG("add"); 转换为 fprintf(stderr,"error: "add"\n");**

**ERROR_LOG(devied =0); 转换为 fprintf(stderr,"error: devied=0\n");**

**（2）##**

　　**“##”是一种分隔连接方式，它的作用是先分隔，然后进行强制连接。**

　　在普通的宏定义中，预处理器一般把空格解释成分段标志，对于每一段和前面比较，相同的就被替换。但是这样做的结果是，被替换段之间存在一些空格。如果我们不希望出现这些空格，就可以通过添加一些##来替代空格。

```
1 #define TYPE1(type,name)   type name_##type##_type
2 #define TYPE2(type,name)   type name##_##type##_type
```

**TYPE1(int, c); 转换为：int 　name_int_type ; (因为##号将后面分为 name_ 、type 、 _type三组，替换后强制连接)**
**TYPE2(int, d);转换为： int 　d_int_type ; (因为##号将后面分为 name、_、type 、_type四组，替换后强制连接)**



**宏定义 do{ }while(0)**

有几个作用：

**（1）空的宏定义避免warning:**
　　 #define foo() do{}while(0)
　　**（2）存在一个独立的block，可以用来进行变量定义，进行比较复杂的实现。**
　　**（3）如果出现在判断语句过后的宏，这样可以保证作为一个整体来是实现：**
　　　　 #define foo(x) \
　　　　　　　 action1(); \
　　　　　　 　action2();
　　　　在以下情况下：
　　　　if(NULL == pPointer)
　　　　　　 foo();
　　　　就会出现action1和action2不会同时被执行的情况，而这显然不是程序设计的目的。如果在do{} while(0)就可以保证作为一个整体。
　　（4）以上的第3种情况用单独的{}也可以实现，但是为什么一定要一个do{}while(0)呢，看以下代码：
　　　　　　#define switch(x,y) {int tmp; tmp="x";x=y;y=tmp;}
　　　　　　if(x>y)
　　　　　　　　switch(x,y);
　　　　　　else //error, parse error before else
　　　　　　otheraction();
　　　　**在把宏引入代码中，会多出一个分号，从而会报错。这对这一点，可以将if和else语句用{}括起来，可以避免分号错误。**
　　使用do{….}while(0) 把它包裹起来，成为一个独立的语法单元，从而不会与上下文发生混淆。同时因为绝大多数的编译器都能够识别do{…}while(0)这种无用的循环并进行优化，所以使用这种方法也不会导致程序的性能降低。

\-------------------------

### 消除多余的分号－Semicolon Swallowing

通常情况下，为了使函数模样的宏在表面上看起来像一个通常的C语言调用一样，通常情况下我们在宏的后面加上一个分号，比如下面的带参宏：

```
MY_MACRO(x);
```

但是如果是下面的情况：

```
#define MY_MACRO(x) {/
/* line 1 *//
/* line 2 *//
/* line 3 */ }

//...

if (condition())
MY_MACRO(a);
else
{...}
```

这样会由于多出的那个分号产生编译错误。为了避免这种情况出现同时保持MY_MACRO(x);的这种写法，我们需要把宏定义为这种形式：

```
#define MY_MACRO(x) do {
/* line 1 *//
/* line 2 *//
/* line 3 */ } while(0)
```

这样只要保证总是使用分号，就不会有任何问题。

### Duplication of Side Effects

这里的Side Effect是指宏在展开的时候对其参数可能进行多次Evaluation（也就是取值），但是如果这个宏参数是一个函数，那么就有可能被调用多次从而达到不一致的结果，甚至会发生更严重的错误。比如：

```
#define min(X,Y) ((X) > (Y) ? (Y) : (X))

//...

c = min(a,foo(b));
```

这时foo()函数就被调用了两次。为了解决这个潜在的问题，我们应当这样写min(X,Y)这个宏：

```
#define min(X,Y) ({/
typeof (X) x_ = (X);/
typeof (Y) y_ = (Y);/
(x_ < y_) ? x_ : y_; })
```

({...})的作用是将内部的几条语句中最后一条的值返回，它也允许在内部声明变量（因为它通过大括号组成了一个局部Scope）。

（c语言关键字typeof介绍：

### 使用`typeof`的声明示例

下面是两个等效声明，用于声明`int`类型的变量`a`。

```
typeof(int) a; /* Specifies variable a which is of the type int */ 
typeof('b') a; /* The same. typeof argument is an expression consisting of 
                    character constant which has the type int */

(
```

typeof(int) a;
typeof(a) b;

printf("%d\n",sizeof(b));// 4

)

以下示例用于声明指针和数组。为了进行对比，还给出了不带`typeof`的等效声明。

```
typeof(int *) p1, p2; /* Declares two int pointers p1, p2 */
int *p1, *p2;

typeof(int) * p3, p4;/* Declares int pointer p3 and int p4 */
int * p3, p4;

typeof(int [10]) a1, a2;/* Declares two arrays of integers */

int a1[10], a2[10];
```

如果将`typeof`用于表达式，则该表达式不会执行。只会得到该表达式的类型。以下示例声明了int类型的`var`变量，因为表达式`foo()`是`int`类型的。由于表达式不会被执行，所以不会调用`foo`函数。

```
extern int foo();
typeof(foo()) var;
```

### 使用`typeof`的声明限制

请注意，`typeof`构造中的类型名不能包含存储类说明符，如`extern`或`static`。不过允许包含类型限定符，如`const`或`volatile`。例如，下列代码是无效的，因为它在`typeof`构造中声明了`extern`：

```
typeof(extern int) a;
```

下列代码使用外部链接来声明标识符`b`是有效的，表示一个`int`类型的对象。下一个声明也是有效的，它声明了一个使用`const`限定符的`char`类型指针，表示指针`p`不能被修改。

```
extern typeof(int) b;
typeof(char * const) p = "a";
```

### 在宏声明中使用`typeof`

`typeof`构造的主要应用是用在宏定义中。可以使用`typeof`关键字来引用宏参数的类型。


**在宏声明中使用typeof**
typeof构造的主要应用是用在宏定义中。可以使用typeof关键字来引用宏参数的类型。因此，在没有将类型名明确指定为宏实参的情况下，构造带有所需类型的对象是可能的。
下面是一个交换两个变量的值的宏定义：
\#define SWAP(a,b) {\
typeof(a) _t=a;\
a=b;\
b=_t;}
这个宏可以交换所有基本数据类型的变量(整数，字符，结构等）

在linux内核中的应用：



```
/* linux-2.6.38.8/include/linux/kernel.h */

#define min(x, y) ({                \
    typeof(x) _min1 = (x);            \
    typeof(y) _min2 = (y);            \
    (void) (&_min1 == &_min2);        \
    _min1 < _min2 ? _min1 : _min2; })

#define max(x, y) ({                \
    typeof(x) _max1 = (x);            \
    typeof(y) _max2 = (y);            \
    (void) (&_max1 == &_max2);        \
    _max1 > _max2 ? _max1 : _max2; })
```



通过typeof获得x和y的数据类型，然后定义两个临时变量，并把x和y的值分别赋给这两个临时变量，最后进行比较。

另外，宏定义中(void)(&_min1 == &_min2)语句的作用是用来警告x和y不能属于不同的数据类型。

这句的作用是比较两个操作数的类型是否相同，防止不同类型的数据进行比较。
若不相同，则会在编译时给出警告：comparison of distinct pointer types lacks a cast。

两个指针类型不同是不能进行相互比较的。

为什么要将结果转成void？看：<http://bbs.csdn.net/topics/390898979>

答：比较两个地址后扔掉比较结果的意义。 否则有些编译器会有warning。

还有container_of，看以前的：<http://www.cnblogs.com/youxin/p/3348227.html>