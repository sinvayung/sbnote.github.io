

| Shell脚本语法                                                |                    |                                                              |
| ------------------------------------------------------------ | ------------------ | ------------------------------------------------------------ |
| [上一页](http://docs.linuxtone.org/ebooks/C&CPP/c/ch31s04.html) | 第 31 章 Shell脚本 | [下一页](http://docs.linuxtone.org/ebooks/C&CPP/c/ch31s06.html) |

## Shell脚本语法

### 条件测试：test [

命令`test`或`[`可以测试一个条件是否成立，如果测试结果为真，则该命令的Exit Status为0，如果测试结果为假，则命令的Exit Status为1（注意与C语言的逻辑表示正好相反）。例如测试两个数的大小关系：

```
$ VAR=2
$ test $VAR -gt 1
$ echo $?
0
$ test $VAR -gt 3
$ echo $?
1
$ [ $VAR -gt 3 ]
$ echo $?
1
```

*虽然看起来很奇怪，但左方括号[确实是一个命令的名字，传给命令的各参数之间应该用空格隔开*，比如，`$VAR`、`-gt`、`3`、`]`是`[`命令的四个参数，它们之间必须用空格隔开。命令`test`或`[`的参数形式是相同的，只不过`test`命令不需要`]`参数。以`[`命令为例，常见的测试命令如下表所示：



**表 31.2. 测试命令**

| `[ -d DIR ]`             | 如果`DIR`存在并且是一个目录则为真                            |
| ------------------------ | ------------------------------------------------------------ |
| `[ -f FILE ]`            | 如果`FILE`存在且是一个普通文件则为真                         |
| `[ -z STRING ]`          | 如果`STRING`的长度为零则为真                                 |
| `[ -n STRING ]`          | 如果`STRING`的长度非零则为真                                 |
| `[ STRING1 = STRING2 ]`  | 如果两个字符串相同则为真                                     |
| `[ STRING1 != STRING2 ]` | 如果字符串不相同则为真                                       |
| `[ ARG1 OP ARG2 ]`       | `ARG1`和`ARG2`应该是整数或者取值为整数的变量，`OP`是`-eq`（等于）`-ne`（不等于）`-lt`（小于）`-le`（小于等于）`-gt`（大于）`-ge`（大于等于）之中的一个 |

和C语言类似，测试条件之间还可以做与、或、非逻辑运算：



**表 31.3. 带与、或、非的测试命令**

| `[ ! EXPR ]`         | `EXPR`可以是上表中的任意一种测试条件，!表示逻辑反            |
| -------------------- | ------------------------------------------------------------ |
| `[ EXPR1 -a EXPR2 ]` | `EXPR1`和`EXPR2`可以是上表中的任意一种测试条件，`-a`表示逻辑与 |
| `[ EXPR1 -o EXPR2 ]` | `EXPR1`和`EXPR2`可以是上表中的任意一种测试条件，`-o`表示逻辑或 |

例如：

```
$ VAR=abc
$ [ -d Desktop -a $VAR = 'abc' ]
$ echo $?
0
```

注意，如果上例中的`$VAR`变量事先没有定义，则被Shell展开为空字符串，会造成测试条件的语法错误（展开为`[ -d Desktop -a = 'abc' ]`），作为一种好的Shell编程习惯，应该总是把变量取值放在双引号之中（展开为`[ -d Desktop -a "" = 'abc' ]`）：

```
$ unset VAR
$ [ -d Desktop -a $VAR = 'abc' ]
bash: [: too many arguments
$ [ -d Desktop -a "$VAR" = 'abc' ]
$ echo $?
1
```

### if/then/elif/else/fi

和C语言类似，在Shell中用`if`、`then`、`elif`、`else`、`fi`这几条命令实现分支控制。这种流程控制语句本质上也是由若干条Shell命令组成的，例如先前讲过的

```
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
```

其实是三条命令，`if [ -f ~/.bashrc ]`是第一条，`then . ~/.bashrc`是第二条，`fi`是第三条。如果两条命令写在同一行则需要用;号隔开，一行只写一条命令就不需要写;号了，另外，`then`后面有换行，但这条命令没写完，Shell会自动续行，把下一行接在`then`后面当作一条命令处理。和`[`命令一样，要注意命令和各参数之间必须用空格隔开。`if`命令的参数组成一条子命令，如果该子命令的Exit Status为0（表示真），则执行`then`后面的子命令，如果Exit Status非0（表示假），则执行`elif`、`else`或者`fi`后面的子命令。`if`后面的子命令通常是测试命令，但也可以是其它命令。Shell脚本没有{}括号，所以用`fi`表示`if`语句块的结束。见下例：

```
#! /bin/sh

if [ -f /bin/bash ]
then echo "/bin/bash is a file"
else echo "/bin/bash is NOT a file"
fi
if :; then echo "always true"; fi
```

`:`是一个特殊的命令，称为空命令，该命令不做任何事，但Exit Status总是真。此外，也可以执行`/bin/true`或`/bin/false`得到真或假的Exit Status。再看一个例子：

```
#! /bin/sh

echo "Is it morning? Please answer yes or no."
read YES_OR_NO
if [ "$YES_OR_NO" = "yes" ]; then
  echo "Good morning!"
elif [ "$YES_OR_NO" = "no" ]; then
  echo "Good afternoon!"
else
  echo "Sorry, $YES_OR_NO not recognized. Enter yes or no."
  exit 1
fi
exit 0
```

上例中的`read`命令的作用是等待用户输入一行字符串，将该字符串存到一个Shell变量中。

此外，Shell还提供了&&和||语法，和C语言类似，具有Short-circuit特性，很多Shell脚本喜欢写成这样：

```
test "$(whoami)" != 'root' &amp;&amp; (echo you are using a non-privileged account; exit 1)
```

&&相当于“if...then...”，而||相当于“if not...then...”。&&和||用于连接两个命令，而上面讲的`-a`和`-o`仅用于在测试表达式中连接两个测试条件，要注意它们的区别，例如，

```
test "$VAR" -gt 1 -a "$VAR" -lt 3
```

和以下写法是等价的

```
test "$VAR" -gt 1 &amp;&amp; test "$VAR" -lt 3
```

### case/esac

`case`命令可类比C语言的`switch`/`case`语句，`esac`表示`case`语句块的结束。C语言的`case`只能匹配整型或字符型常量表达式，而Shell脚本的`case`可以匹配字符串和Wildcard，每个匹配分支可以有若干条命令，末尾必须以;;结束，执行时找到第一个匹配的分支并执行相应的命令，然后直接跳到`esac`之后，不需要像C语言一样用`break`跳出。

```
#! /bin/sh

echo "Is it morning? Please answer yes or no."
read YES_OR_NO
case "$YES_OR_NO" in
yes|y|Yes|YES)
  echo "Good Morning!";;
[nN]*)
  echo "Good Afternoon!";;
*)
  echo "Sorry, $YES_OR_NO not recognized. Enter yes or no."
  exit 1;;
esac
exit 0
```

使用`case`语句的例子可以在系统服务的脚本目录`/etc/init.d`中找到。这个目录下的脚本大多具有这种形式（以`/etc/apache2`为例）：

```
case $1 in
	start)
		...
	;;
	stop)
		...
	;;
	reload | force-reload)
		...
	;;
	restart)
	...
	*)
		log_success_msg "Usage: /etc/init.d/apache2 {start|stop|restart|reload|force-reload|start-htcacheclean|stop-htcacheclean}"
		exit 1
	;;
esac
```

启动`apache2`服务的命令是

```
$ sudo /etc/init.d/apache2 start
```

`$1`是一个特殊变量，在执行脚本时自动取值为第一个命令行参数，也就是`start`，所以进入`start)`分支执行相关的命令。同理，命令行参数指定为`stop`、`reload`或`restart`可以进入其它分支执行停止服务、重新加载配置文件或重新启动服务的相关命令。

### for/do/done

Shell脚本的`for`循环结构和C语言很不一样，它类似于某些编程语言的`foreach`循环。例如：

```
#! /bin/sh

for FRUIT in apple banana pear; do
  echo "I like $FRUIT"
done
```

`FRUIT`是一个循环变量，第一次循环`$FRUIT`的取值是`apple`，第二次取值是`banana`，第三次取值是`pear`。再比如，要将当前目录下的`chap0`、`chap1`、`chap2`等文件名改为`chap0~`、`chap1~`、`chap2~`等（按惯例，末尾有~字符的文件名表示临时文件），这个命令可以这样写：

```
$ for FILENAME in chap?; do mv $FILENAME $FILENAME~; done
```

也可以这样写：

```
$ for FILENAME in `ls chap?`; do mv $FILENAME $FILENAME~; done
```

### while/do/done

`while`的用法和C语言类似。比如一个验证密码的脚本：

```
#! /bin/sh

echo "Enter password:"
read TRY
while [ "$TRY" != "secret" ]; do
  echo "Sorry, try again"
  read TRY
done
```

下面的例子通过算术运算控制循环的次数：

```
#! /bin/sh

COUNTER=1
while [ "$COUNTER" -lt 10 ]; do
  echo "Here we go again"
  COUNTER=$(($COUNTER+1))
done
```

Shell还有until循环，类似C语言的do...while循环。本章从略。

#### 习题

1、把上面验证密码的程序修改一下，如果用户输错五次密码就报错退出。

### 位置参数和特殊变量

有很多特殊变量是被Shell自动赋值的，我们已经遇到了`$?`和`$1`，现在总结一下：



**表 31.4. 常用的位置参数和特殊变量**

| `$0`          | 相当于C语言`main`函数的`argv[0]`                             |
| ------------- | ------------------------------------------------------------ |
| `$1`、`$2`... | 这些称为位置参数（Positional Parameter），相当于C语言`main`函数的`argv[1]`、`argv[2]`... |
| `$#`          | 相当于C语言`main`函数的`argc - 1`，注意这里的`#`后面不表示注释 |
| `$@`          | 表示参数列表`"$1" "$2" ...`，例如可以用在`for`循环中的`in`后面。 |
| `$?`          | 上一条命令的Exit Status                                      |
| `$$`          | 当前Shell的进程号                                            |

位置参数可以用`shift`命令左移。比如`shift 3`表示原来的`$4`现在变成`$1`，原来的`$5`现在变成`$2`等等，原来的`$1`、`$2`、`$3`丢弃，`$0`不移动。不带参数的`shift`命令相当于`shift 1`。例如：

```
#! /bin/sh

echo "The program $0 is now running"
echo "The first parameter is $1"
echo "The second parameter is $2"
echo "The parameter list is $@"
shift
echo "The first parameter is $1"
echo "The second parameter is $2"
echo "The parameter list is $@"
```

### 函数

和C语言类似，Shell中也有函数的概念，但是函数定义中没有返回值也没有参数列表。例如：

```
#! /bin/sh

foo(){ echo "Function foo is called";}
echo "-=start=-"
foo
echo "-=end=-"
```

注意函数体的左花括号{和后面的命令之间必须有空格或换行，如果将最后一条命令和右花括号`}`写在同一行，命令末尾必须有;号。

在定义`foo()`函数时并不执行函数体中的命令，就像定义变量一样，只是给`foo`这个名字一个定义，到后面调用`foo`函数的时候（注意Shell中的函数调用不写括号）才执行函数体中的命令。Shell脚本中的函数必须先定义后调用，一般把函数定义都写在脚本的前面，把函数调用和其它命令写在脚本的最后（类似C语言中的`main`函数，这才是整个脚本实际开始执行命令的地方）。

Shell函数没有参数列表并不表示不能传参数，事实上，函数就像是迷你脚本，调用函数时可以传任意个参数，在函数内同样是用`$0`、`$1`、`$2`等变量来提取参数，函数中的位置参数相当于函数的局部变量，改变这些变量并不会影响函数外面的`$0`、`$1`、`$2`等变量。函数中可以用`return`命令返回，如果`return`后面跟一个数字则表示函数的Exit Status。

下面这个脚本可以一次创建多个目录，各目录名通过命令行参数传入，脚本逐个测试各目录是否存在，如果目录不存在，首先打印信息然后试着创建该目录。

```
#! /bin/sh

is_directory()
{
  DIR_NAME=$1
  if [ ! -d $DIR_NAME ]; then
    return 1
  else
    return 0
  fi
}

for DIR in "$@"; do
  if is_directory "$DIR"
  then :
  else
    echo "$DIR doesn't exist. Creating it now..."
    mkdir $DIR > /dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "Cannot create directory $DIR"
      exit 1
    fi
  fi
done
```

注意`is_directory()`返回0表示真返回1表示假。



http://docs.linuxtone.org/ebooks/C&CPP/c/ch31s05.html