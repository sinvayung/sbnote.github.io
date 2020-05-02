---
title: CC++交叉编译的问题
description: CC++交叉编译的问题
---

CC++交叉编译的问题



foo.h, foo.c, main.cpp

或

foo.h, foo.cpp, main.c

时，编译会报错：

 

```
jni/main.cpp:16: error: undefined reference to 'abc(int, int)'
collect2.exe: error: ld returned 1 exit status
```

解决方法：foo.h文件应该这样写：

 

```
#ifndef FOO_H_
#define FOO_H_

#ifdef __cplusplus
    extern "C" {
#endif

int abc(int a, int b) ;

#ifdef __cplusplus
}
#endif /* __cplusplus */


#endif /* FOO_H_ */
```