#  getopt和getopt_long函数

2012年09月04日 17:44:21 [开水](https://me.csdn.net/Cashey1991) 阅读数：41134



平时在写程序时常常需要对命令行参数进行处理，当命令行参数个数较多时，如果按照顺序一个一个定义参数含义很容易造成混乱，而且如果程序只按顺序处理参数的话，一些“可选参数”的功能将很难实现。

**在Linux中，我们可以使用getopt、getopt_long、getopt_long_only来对这个问题进行处理。**



```cpp
       #include <unistd.h>



 



       int getopt(int argc, char * const argv[],



                  const char *optstring);



 



       extern char *optarg;



       extern int optind, opterr, optopt;



 



       #include <getopt.h>



 



       int getopt_long(int argc, char * const argv[],



                  const char *optstring,



                  const struct option *longopts, int *longindex);



 



       int getopt_long_only(int argc, char * const argv[],



                  const char *optstring,



                  const struct option *longopts, int *longindex);
```



**从最简单的getopt讲起，getopt函数的前两个参数，就是main函数的argc和argv，这两者直接传入即可，要考虑的就只剩下第三个参数。**

**optstring的格式举例说明比较方便，例如：**

​    char *optstring = "abcd:";

上面这个optstring在传入之后，getopt函数将依次检查命令行是否指定了 -a， -b， -c及 -d（这需要多次调用getopt函数，直到其返回-1），当检查到上面某一个参数被指定时，函数会返回被指定的参数名称（即该字母）

最后一个参数d后面带有冒号，: 表示参数d是可以指定值的，如 -d 100 或 -d user。

optind表示的是下一个将被处理到的参数在argv中的下标值。

如果指定opterr = 0的话，在getopt、getopt_long、getopt_long_only遇到错误将不会输出错误信息到标准输出流。



```cpp
#include <unistd.h>



#include <stdlib.h>



#include <stdio.h>



 



int main(int argc, char *argv[])



{



    int opt;



    char *optstring = "a:b:c:d";



 



    while ((opt = getopt(argc, argv, optstring)) != -1)



    {



        printf("opt = %c\n", opt);



        printf("optarg = %s\n", optarg);



        printf("optind = %d\n", optind);



        printf("argv[optind - 1] = %s\n\n",  argv[optind - 1]);



    }



 



    return 0;



}
```

编译上述程序并运行，有如下结果：





```cpp
cashey@ubuntu:~/Desktop/getopt$ ./test_getopt -a 100 -b 200 -c admin -d



opt = a



optarg = 100



optind = 3



argv[optind - 1] = 100



 



opt = b



optarg = 200



optind = 5



argv[optind - 1] = 200



 



opt = c



optarg = admin



optind = 7



argv[optind - 1] = admin



 



opt = d



optarg = (null)



optind = 8



argv[optind - 1] = -d
```





下面来讲getopt_long函数，getopt_long函数包含了getopt函数的功能，并且还可以指定“长参数”（或者说长选项），与getopt函数对比，getopt_long比其多了两个参数：

​       int getopt(int argc, char * const argv[],
​                  const char *optstring);

​       int getopt_long(int argc, char * const argv[],
​                  const char *optstring,
​                  const struct option *longopts, int *longindex);



在这里，longopts指向的是一个由option结构体组成的数组，那个数组的每个元素，指明了一个“长参数”（即形如--name的参数）名称和性质：

​           struct option {
​               const char *name;
​               int         has_arg;
​               int        *flag;
​               int         val;
​           };

​       name  是参数的名称

​       has_arg 指明是否带参数值，其数值可选：
​              no_argument (即 0) 表明这个长参数不带参数（即不带数值，如：--name）
​              required_argument (即 1) 表明这个长参数必须带参数（即必须带数值，如：--name Bob）
​            optional_argument（即2）表明这个长参数后面带的参数是可选的，（即--name和--name Bob均可）

​       flag   当这个指针为空的时候，函数直接将val的数值从getopt_long的返回值返回出去，当它非空时，val的值会被赋到flag指向的整型数中，而函数返回值为0

​       val    用于指定函数找到该选项时的返回值，或者当flag非空时指定flag指向的数据的值。

**另一个参数longindex，如果longindex非空，它指向的变量将记录当前找到参数符合longopts里的第几个元素的描述，即是longopts的下标值。**



```cpp
#include <unistd.h>



#include <stdlib.h>



#include <stdio.h>



#include <getopt.h>



 



int



main(int argc, char **argv)



{



   int opt;



   int digit_optind = 0;



   int option_index = 0;



   char *optstring = "a:b:c:d";



   static struct option long_options[] = {



       {"reqarg", required_argument, NULL, 'r'},



       {"noarg",  no_argument,       NULL, 'n'},



       {"optarg", optional_argument, NULL, 'o'},



       {0, 0, 0, 0}



   };



 



   while ( (opt = getopt_long(argc, argv, optstring, long_options, &option_index)) != -1)



   {



        printf("opt = %c\n", opt);



        printf("optarg = %s\n", optarg);



        printf("optind = %d\n", optind);



        printf("argv[optind - 1] = %s\n",  argv[optind - 1]);



        printf("option_index = %d\n", option_index);



   }



 



   return 0;



}
```



编译运行以上程序并运行，可以得到以下结果：





```ruby
cashey@ubuntu:~/Desktop/getopt$ ./test_getopt_long -a 100 --reqarg 100 --nonarg
opt = a
optarg = 100
optind = 3
argv[optind - 1] = 100
option_index = 0
opt = r
optarg = 100
optind = 5
argv[optind - 1] = 100
option_index = 0
./test_getopt_long: unrecognized option '--nonarg'
opt = ?
optarg = (null)
optind = 6
argv[optind - 1] = --nonarg
option_index = 0
```

当所给的参数存在问题时，opt（即函数返回值是'?'），如：





```ruby
cashey@ubuntu:~/Desktop/getopt$ ./test_getopt_long -a
./test_getopt_long: option requires an argument -- 'a'
opt = ?
optarg = (null)
optind = 2
argv[optind - 1] = -a
option_index = 0
cashey@ubuntu:~/Desktop/getopt$ ./test_getopt_long --reqarg
./test_getopt_long: option '--reqarg' requires an argument
opt = ?
optarg = (null)
optind = 2
argv[optind - 1] = --reqarg
```

最后说说getopt_long_only函数，它与getopt_long函数使用相同的参数表，在功能上基本一致，只是getopt_long只将--name当作长参数，但getopt_long_only会将--name和-name两种选项都当作长参数来匹配。在getopt_long在遇到-name时，会拆解成-n -a -m -e到optstring中进行匹配，而getopt_long_only只在-name不能在longopts中匹配时才将其拆解成**-n -a -m -e这样的参数到optstring中进行匹配。**