# gradle task总结

![96](https://upload.jianshu.io/users/upload_avatars/2608779/4c1bd87d-f1f2-4d7a-9447-aa6a12f969a8.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96)

 

[juexingzhe](https://www.jianshu.com/u/ea71bb3770b4)

 

关注

2017.11.12 20:03* 字数 1351 阅读 843评论 0喜欢 4

今天我们来总结下Gradle 中task的相关知识点，gradle中的project和task真的是太太太重要了。在Gradle中可以有很多的Project，Project就是抽出来的一个个独立的模块，所有的Project组成了整个Gradle的构建。一个Project可以包含很多的Task，Task就是一个操作，比如上传jar到maven，复制一份文件，输出lint报告等等。打个不是很恰当的比喻，Project可以看做Java中的类，task就是这个类里面的一个个方法。

今天概念性的东西会比较多，主要从下面几个方面：

> 1 Task的创建
> 2 Task的常用属性
> 3 Task的执行分析

### 1.Task的创建

常用的task创建方式有4种，下面我们分别来看一下：

##### 1.1第一种创建方式

第一种就是通过task的原型
`Task task(String name) throws InvalidUserDataException;`
用法如下，创建了一个名字是`createTask1Name`的task，返回类型是Task的createTask1，这样我们就可以在脚本中对这个task进行其他操作。

```
def Task createTask1 = task(createTask1Name)
createTask1.doLast{
    println '第一种创建方法'
}
```

怎么运行上面这个task就很简单了：

```
$ gradle createTask1
:createTask1Name
第一种创建方法

BUILD SUCCESSFUL

Total time: 0.834 secs
```

##### 1.2第二种创建方式

第二种方法就是通过name和对该任务的配置Map来创建任务，原型就是：

```
Task task(Map<String, ?> args, String name) throws InvalidUserDataException;
```

用法如下：

```
def Task createTask2 = task(description: '任务创建方式2', createTask2)
createTask2.doLast{
    println '第二种创建方法'
}
```

运行效果：

```
$ gradle createTask2
:createTask2
第二种创建方法

BUILD SUCCESSFUL

Total time: 0.872 secs
```

我们看一下这个task的信息,可以看出description属性生效了，同理也可以配置task的其他属性。

```
$ gradle help --task createTask2
:help
Detailed task information for createTask2

Path
     :createTask2

Type
     Task (org.gradle.api.Task)

Description
     任务创建方式2

Group
     -

BUILD SUCCESSFUL

Total time: 0.811 secs
```

常用的配置属性有下面这些：

> 1 type:基于一个存在的task来创建，和继承差不多意思
> 2 description:配置任务的描述
> 3 group:用于配置任务的分组
> 4 dependsOn:配置任务的依赖
> 5 action:添加action

##### 1.3第三种创建方式

第三种创建的原型：

```
Task task(String name, Closure configureClosure);
```

用法如下,有的小伙伴就有意见了，这个和上面的原型不一样。

```
task createTask3 {
    description '任务创建方式3'
    group 'testTaskCreate'
    doLast{
        println '第三种创建方法'
    }
}
```

我做一下解释哈，其中闭包Closure如果是最后一个参数可以移到外面，方法的参数可以不用加括号，这个都是Groovy的语法糖。如果你高兴也可以这样写：

```
task(createTask3) {
    description '任务创建方式3'
    group 'testTaskCreate'
    doLast{
        println '第三种创建方法'
    }
}
```

也可以这样写：

```
task(createTask3,  {
    description '任务创建方式3'
    group 'testTaskCreate'
    doLast{
        println '第三种创建方法'
    }
})
```

运行方式：

```
gradle createTask3
:createTask3
第三种创建方法

BUILD SUCCESSFUL

Total time: 0.889 secs
```

##### 1.4第四种创建方式

第四种就是通过`TaskContainer`来创建，简单看下对`TaskContainer`的解释,`TaskContainer`其实就是用来管理task集合的，可以在project中通过getTask()方法来拿到这个实例，或者直接通过tasks来或者这个实例。

```
/**
 * <p>A {@code TaskContainer} is responsible for managing a set of {@link Task} instances.</p>
 *
 * <p>You can obtain a {@code TaskContainer} instance by calling {@link org.gradle.api.Project#getTasks()}, or using the
 * {@code tasks} property in your build script.</p>
 */
public interface TaskContainer extends TaskCollection<Task>, PolymorphicDomainObjectContainer<Task> 
Task create(String name, Closure configureClosure) throws InvalidUserDataException;
```

用法如下,这个也是把闭包挪到外面了，见上面语法糖。

```
tasks.create('createTask4'){
    description '任务创建方式4'
    group 'testTaskCreate'
    doLast{
        println '第四种创建方法'
    }
}
```

运行效果：

```
$ gradle createTask4
:createTask4
第四种创建方法

BUILD SUCCESSFUL

Total time: 0.825 secs
```

一般在Android中构建用第三种简化方式会比较多一点。

那么在project中怎么访问这个任务？
主要有两种方式，第一种方式就是先定义：

```
def Task myTask = task groupTask
myTask.group = BasePlugin.BUILD_GROUP
myTask.description = '这是一个构建的引导任务'

myTask.doLast {
    println "group: $group, description:$description"
}
```

另外一种方式就是通过`TaskContainer`来获取：

```
def Task myTask = task groupTask
tasks['groupTask'].doLast {
    println "group: $group, description:$description"
}
```

### 2.Task的常用属性

部分常用属性在前面已经有用到过了，`dependsOn`就是`taskProperty`这个依赖另外的task；`group`就是分组；`description`就是这个task的描述。

```
task helloTask{
    println 'hello'
}

task worldTask{
    println 'world!'
}

def Task myTask = task taskProperty{
    dependsOn helloTask, worldTask
    println 'in myTask'
}
myTask.group = BasePlugin.BUILD_GROUP
myTask.description = '测试常用属性'
```

我们看下执行结果,首先先执行依赖的Task：

```
$ gradle taskProperty
hello
world!
in myTask
:helloTask UP-TO-DATE
:worldTask UP-TO-DATE
:taskProperty UP-TO-DATE

BUILD SUCCESSFUL
```

再看下这个Task的信息,可以看到上面设置的属性生效了：

```
$ gradle help --task taskProperty
hello
world!
in myTask
:help
Detailed task information for taskProperty

Path
     :taskProperty

Type
     Task (org.gradle.api.Task)

Description
     测试常用属性

Group
     build

BUILD SUCCESSFUL
```

另外一个和`dependsOn`类似的属性就是`mustRunAfter`,这个运行结果和上面是一样的，就不贴出来了，小伙伴们可以自行试一下。

```
myTask.mustRunAfter = [helloTask, worldTask]
```

还有一个属性`enabled`可以启用或者禁用任务，默认是true，表示启用。设置为false，则禁止该任务执行，输出会提示任务被跳过：

```
task helloTask{
    println 'hello'
}
helloTask.enabled = false

task worldTask{
    println 'world!'
}

def Task myTask = task taskProperty{
    dependsOn helloTask, worldTask
    println 'in myTask'
}
```

输出结果,可以看到helloTask 提示SKIPPED

```
$ gradle taskProperty
hello
world!
in myTask
:helloTask SKIPPED
:worldTask UP-TO-DATE
:taskProperty UP-TO-DATE

BUILD SUCCESSFUL
```

另外一个比较常用的属性是onlyIf，它可以接受一个闭包作为参数，如果闭包返回true则执行该任务，否则跳过。这个在Android里面可以用于多渠道打包：

```
final String BUILD_ALL = 'all'

task testOnlyIf{
    println '打包'
}

task build{
    dependsOn testOnlyIf
    group BasePlugin.BUILD_GROUP
    description '多渠道打包'
}

testOnlyIf.onlyIf{
    def execute = false
    if (project.hasProperty('build')) {
        Object buildApps = project.property('build')
        if (BUILD_ALL.equals(buildApps)) {
            execute = true
        }else{
            execute = false
        }
    }else{
        execute = false
    }
    execute
}
```

在执行的时候就可以传入`build`属性值来决定`testOnlyIf`这个打包任务是否执行,如果我传入**all**就会执行`testOnlyIf`

```
$ gradle -Pbuild=all build
打包
:testOnlyIf UP-TO-DATE
:build UP-TO-DATE

BUILD SUCCESSFUL
```

如果传入不是 **all** 就不会执行这个Task：

```
$ gradle -Pbuild=Notall build
打包
:testOnlyIf SKIPPED
:build UP-TO-DATE

BUILD SUCCESSFUL
```

还有几个常用的属性`doLast`，`doFirst`在下面的执行顺序中一起说。

### 3.Task的执行分析

首先有个概念，配置在`doFirst`中的操作会首先执行，而配置在`doLast`中的会最后执行，执行顺序是`doFirst`,`doSelf`,`doLast`。我们看个例子：

```
def Task myTask = task createCustomTask(type: CustomTask){
    doFirst{
        println 'myTask执行之前执行doFirst'
    }
    doLast {
        println 'myTask执行之后执行doLast'
    }
}

class CustomTask extends DefaultTask{
    @TaskAction
    def doSelf(){
        println 'myTask执行doSelf'
    }
}
```

输出结果可以看出任务执行顺序跟我们的预期一致，type其实就是类似于继承，我们这里自定义一个Task：CustomTask，通过注解标注这个Task的需要做的任务。

```
$ gradle createCustomTask
:createCustomTask
myTask执行之前执行doFirst
myTask执行doSelf
myTask执行之后执行doLast

BUILD SUCCESSFUL
```

### 4.总结

今天关于`Task`的分享就到这里了，Task是Gradle中比较重要的知识点，我这里只是一些常用知识点的总结，希望对小伙伴们有点帮助哈。

文中有部分例子参考了Android Gradle权威指南，在此表示感谢！

最后，感谢@右倾倾的理解和支持。

以上。

欢迎关注公众号：JueCode



https://www.jianshu.com/p/facbca0576a6