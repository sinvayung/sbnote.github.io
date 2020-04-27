---
title: Git
description: Git
---

## Git

读写配置

```shell
# 查看系统config
git config --system --list
　　
# 查看当前用户（global）配置
git config --global  --list

# 查看当前仓库配置信息
git config --local  --list

# 设置提交用户的用户名和email（全局）
git config --global user.name "myname"
git config --global user.email  "test@gmail.com"

# 设置提交用户的用户名和email（单独为当前仓库设置）
git config user.name "myname"
git config user.email  "test@gmail.com"
```



```shell
$ git push origin master
To https://github.com/sbnote/sbnote.github.io.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/sbnote/sbnote.github.io.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

原因：这个问题是因为远程库与本地库不一致造成的

解决：

```sh
git pull --rebase origin master
```

这条指令的意思是把远程库中的更新合并到本地库中，–rebase的作用是取消掉本地库中刚刚的commit，并把他们接到更新后的版本库之中。

git pull --rebase origin master意为先取消commit记录，并且把它们临时 保存为补丁(patch)(这些补丁放到".git/rebase"目录中)，之后同步远程库到本地，最后合并补丁到本地库之中。