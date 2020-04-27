---
title: Android应用劫持的攻与防
description: Android应用劫持的攻与防
---

## Android应用劫持的攻与防

### Root的危害

- Android通过用户隔离来保障每个应用的安全
- Root后，你的App就可以被其他App访问：内存被篡改、行为被监控、……

### 什么是App劫持?

- App劫持：App的执行流程被重定向
- 通常通过“注入+Hook”来实现

### App劫持过程

- Step1: 逆向分析App的逻辑
- Step2: 注入模块到App进程中
  - Ptrace
  - Dlopen
- Step3: Hook
  - Java Hook
  - Native(so) Hook

### 注入Hook过程

![img](assets/hacker_yyjc/ba54a5e1-ff8b-4c95-9e52-ff9a09afeb37.jpg)

### Hook类型

- Java Hook
  - Static Field Hook：静态成员hook
  - Method Hook：函数hook
- Native So Hook
  - GOT Hook：全局偏移表hook
  - SYM Hook：符号表hook
  - Inline Hook：函数内联hook

### Java静态成员Hook

[https://www.rsaconference.com/writable/presentations/file_upload/man-w07-*app*-*android*.pdf](https://www.rsaconference.com/writable/presentations/file_upload/man-w07-_app_-_android_.pdf)