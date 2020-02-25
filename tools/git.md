#### 读写配置

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

