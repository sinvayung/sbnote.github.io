# 协程与任务

本节将简述用于协程与任务的高层级 API。

- [协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutines)
- [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#awaitables)
- [运行 asyncio 程序](https://docs.python.org/zh-cn/3/library/asyncio-task.html#running-an-asyncio-program)
- [创建任务](https://docs.python.org/zh-cn/3/library/asyncio-task.html#creating-tasks)
- [休眠](https://docs.python.org/zh-cn/3/library/asyncio-task.html#sleeping)
- [并发运行任务](https://docs.python.org/zh-cn/3/library/asyncio-task.html#running-tasks-concurrently)
- [屏蔽取消操作](https://docs.python.org/zh-cn/3/library/asyncio-task.html#shielding-from-cancellation)
- [超时](https://docs.python.org/zh-cn/3/library/asyncio-task.html#timeouts)
- [简单等待](https://docs.python.org/zh-cn/3/library/asyncio-task.html#waiting-primitives)
- [来自其他线程的日程安排](https://docs.python.org/zh-cn/3/library/asyncio-task.html#scheduling-from-other-threads)
- [内省](https://docs.python.org/zh-cn/3/library/asyncio-task.html#introspection)
- [Task 对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#task-object)
- [基于生成器的协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#generator-based-coroutines)



## [协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id2)

协程通过 async/await 语法进行声明，是编写异步应用的推荐方式。例如，以下代码段 (需要 Python 3.7+) 打印 "hello"，等待 1 秒，然后打印 "world":

\>>>

```
>>> import asyncio

>>> async def main():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')

>>> asyncio.run(main())
hello
world
```

注意：简单地调用一个协程并不会将其加入执行日程:

\>>>

```
>>> main()
<coroutine object main at 0x1053bb7c8>
```

要真正运行一个协程，asyncio 提供了三种主要机制:

- [`asyncio.run()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.run) 函数用来运行最高层级的入口点 "main()" 函数 (参见上面的示例。)

- 等待一个协程。以下代码段会在等待 1 秒后打印 "hello"，然后 *再次* 等待 2 秒后打印 "world":

  ```
  import asyncio
  import time
  
  async def say_after(delay, what):
      await asyncio.sleep(delay)
      print(what)
  
  async def main():
      print(f"started at {time.strftime('%X')}")
  
      await say_after(1, 'hello')
      await say_after(2, 'world')
  
      print(f"finished at {time.strftime('%X')}")
  
  asyncio.run(main())
  ```

  预期的输出:

  ```
  started at 17:13:52
  hello
  world
  finished at 17:13:55
  ```

- [`asyncio.create_task()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.create_task) 函数用来并发运行作为 asyncio [`任务`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 的多个协程。

  让我们修改以上示例，*并发* 运行两个 `say_after` 协程:

  ```
  async def main():
      task1 = asyncio.create_task(
          say_after(1, 'hello'))
  
      task2 = asyncio.create_task(
          say_after(2, 'world'))
  
      print(f"started at {time.strftime('%X')}")
  
      # Wait until both tasks are completed (should take
      # around 2 seconds.)
      await task1
      await task2
  
      print(f"finished at {time.strftime('%X')}")
  ```

  注意，预期的输出显示代码段的运行时间比之前快了 1 秒:

  ```
  started at 17:14:32
  hello
  world
  finished at 17:14:34
  ```



## [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id3)

如果一个对象可以在 [`await`](https://docs.python.org/zh-cn/3/reference/expressions.html#await) 语句中使用，那么它就是 **可等待** 对象。许多 asyncio API 都被设计为接受可等待对象。

*可等待* 对象有三种主要类型: **协程**, **任务** 和 **Future**.

协程

Python 协程属于 *可等待* 对象，因此可以在其他协程中被等待:

```
import asyncio

async def nested():
    return 42

async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    nested()

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".

asyncio.run(main())
```

重要

 

在本文档中 "协程" 可用来表示两个紧密关联的概念:

- *协程函数*: 定义形式为 [`async def`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#async-def) 的函数;
- *协程对象*: 调用 *协程函数* 所返回的对象。

asyncio 也支持旧式的 [基于生成器的](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-generator-based-coro) 协程。

任务

*任务* 被用来设置日程以便 *并发* 执行协程。

当一个协程通过 [`asyncio.create_task()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.create_task) 等函数被打包为一个 *任务*，该协程将自动排入日程准备立即运行:

```
import asyncio

async def nested():
    return 42

async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```

Future 对象

[`Future`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future) 是一种特殊的 **低层级** 可等待对象，表示一个异步操作的 **最终结果**。

当一个 Future 对象 *被等待*，这意味着协程将保持等待直到该 Future 对象在其他地方操作完毕。

在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码。

通常情况下 **没有必要** 在应用层级的代码中创建 Future 对象。

Future 对象有时会由库和某些 asyncio API 暴露给用户，用作可等待对象:

```
async def main():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
```

一个很好的返回对象的低层级函数的示例是 [`loop.run_in_executor()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)。

## [运行 asyncio 程序](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id4)

- `asyncio.``run`(*coro*, ***, *debug=False*)

  此函数运行传入的协程，负责管理 asyncio 事件循环并 *完结异步生成器*。当有其他 asyncio 事件循环在同一线程中运行时，此函数不能被调用。如果 *debug* 为 `True`，事件循环将以调试模式运行。此函数总是会创建一个新的事件循环并在结束时关闭之。它应当被用作 asyncio 程序的主入口点，理想情况下应当只被调用一次。*3.7 新版功能:* **重要:** 此函数是在 Python 3.7 中加入 asyncio 模块，处于 [暂定基准状态](https://docs.python.org/zh-cn/3/glossary.html#term-provisional-api)。

## [创建任务](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id5)

- `asyncio.``create_task`(*coro*)

  将 *coro* [协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine) 打包为一个 [`Task`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 排入日程准备执行。返回 Task 对象。该任务会在 [`get_running_loop()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.get_running_loop) 返回的循环中执行，如果当前线程没有在运行的循环则会引发 [`RuntimeError`](https://docs.python.org/zh-cn/3/library/exceptions.html#RuntimeError)。此函数 **在 Python 3.7 中被加入**。在 Python 3.7 之前，可以改用低层级的 [`asyncio.ensure_future()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.ensure_future) 函数。`async def coro():     ...  # In Python 3.7+ task = asyncio.create_task(coro()) ...  # This works in all Python versions but is less readable task = asyncio.ensure_future(coro()) ... `*3.7 新版功能.*

## [休眠](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id6)

- *coroutine* `asyncio.``sleep`(*delay*, *result=None*, ***, *loop=None*)

  阻塞 *delay* 指定的秒数。如果指定了 *result*，则当协程完成时将其返回给调用者。`sleep()` 总是会挂起当前任务，以允许其他任务运行。*loop* 参数已弃用，计划在 Python 3.10 中移除。以下协程示例运行 5 秒，每秒显示一次当前日期:`import asyncio import datetime  async def display_date():     loop = asyncio.get_running_loop()     end_time = loop.time() + 5.0     while True:         print(datetime.datetime.now())         if (loop.time() + 1.0) >= end_time:             break         await asyncio.sleep(1)  asyncio.run(display_date()) `

## [并发运行任务](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id7)

- *awaitable* `asyncio.``gather`(**aws*, *loop=None*, *return_exceptions=False*)

  *并发* 运行 *aws* 序列中的 [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-awaitables)。如果 *aws* 中的某个可等待对象为协程，它将自动作为一个任务加入日程。如果所有可等待对象都成功完成，结果将是一个由所有返回值聚合而成的列表。结果值的顺序与 *aws* 中可等待对象的顺序一致。如果 *return_exceptions* 为 `False` (默认)，所引发的首个异常会立即传播给等待 `gather()` 的任务。*aws* 序列中的其他可等待对象 **不会被取消** 并将继续运行。如果 *return_exceptions* 为 `True`，异常会和成功的结果一样处理，并聚合至结果列表。如果 `gather()` *被取消*，所有被提交 (尚未完成) 的可等待对象也会 *被取消*。如果 *aws* 序列中的任一 Task 或 Future 对象 *被取消*，它将被当作引发了 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 一样处理 -- 在此情况下 `gather()` 调用 **不会** 被取消。这是为了防止一个已提交的 Task/Future 被取消导致其他 Tasks/Future 也被取消。示例:`import asyncio  async def factorial(name, number):     f = 1     for i in range(2, number + 1):         print(f"Task {name}: Compute factorial({i})...")         await asyncio.sleep(1)         f *= i     print(f"Task {name}: factorial({number}) = {f}")  async def main():     # Schedule three calls *concurrently*:     await asyncio.gather(         factorial("A", 2),         factorial("B", 3),         factorial("C", 4),     )  asyncio.run(main())  # Expected output: # #     Task A: Compute factorial(2)... #     Task B: Compute factorial(2)... #     Task C: Compute factorial(2)... #     Task A: factorial(2) = 2 #     Task B: Compute factorial(3)... #     Task C: Compute factorial(3)... #     Task B: factorial(3) = 6 #     Task C: Compute factorial(4)... #     Task C: factorial(4) = 24 `*在 3.7 版更改:* 如果 *gather* 本身被取消，则无论 *return_exceptions* 取值为何，消息都会被传播。

## [屏蔽取消操作](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id8)

- *awaitable* `asyncio.``shield`(*aw*, ***, *loop=None*)

  保护一个 [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-awaitables) 防止其被 [`取消`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel)。如果 *aw* 是一个协程，它将自动作为任务加入日程。以下语句:`res = await shield(something()) `相当于:`res = await something() `*不同之处* 在于如果包含它的协程被取消，在 `something()` 中运行的任务不会被取消。从 `something()` 的角度看来，取消操作并没有发生。然而其调用者已被取消，因此 "await" 表达式仍然会引发 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError)。如果通过其他方式取消 `something()` (例如在其内部操作) 则 `shield()` 也会取消。如果希望完全忽略取消操作 (不推荐) 则 `shield()` 函数需要配合一个 try/except 代码段，如下所示:`try:     res = await shield(something()) except CancelledError:     res = None `

## [超时](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id9)

- *coroutine* `asyncio.``wait_for`(*aw*, *timeout*, ***, *loop=None*)

  等待 *aw* [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-awaitables) 完成，指定 timeout 秒数后超时。如果 *aw* 是一个协程，它将自动作为任务加入日程。*timeout* 可以为 `None`，也可以为 float 或 int 型数值表示的等待秒数。如果 *timeout* 为 `None`，则等待直到完成。如果发生超时，任务将取消并引发 [`asyncio.TimeoutError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.TimeoutError).要避免任务 [`取消`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel)，可以加上 [`shield()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.shield)。函数将等待直到目标对象确实被取消，所以总等待时间可能超过 *timeout* 指定的秒数。如果等待被取消，则 *aw* 指定的对象也会被取消。*loop* 参数已弃用，计划在 Python 3.10 中移除。示例:`async def eternity():     # Sleep for one hour     await asyncio.sleep(3600)     print('yay!')  async def main():     # Wait for at most 1 second     try:         await asyncio.wait_for(eternity(), timeout=1.0)     except asyncio.TimeoutError:         print('timeout!')  asyncio.run(main())  # Expected output: # #     timeout! `*在 3.7 版更改:* 当 *aw* 因超时被取消，`wait_for` 会等待 *aw* 被取消。之前版本则将立即引发 [`asyncio.TimeoutError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.TimeoutError)。

## [简单等待](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id10)

- *coroutine* `asyncio.``wait`(*aws*, ***, *loop=None*, *timeout=None*, *return_when=ALL_COMPLETED*)

  并发运行 *aws* 指定的 [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-awaitables) 并阻塞线程直到满足 *return_when* 指定的条件。如果 *aws* 中的某个可等待对象为协程，它将自动作为任务加入日程。直接向 `wait()` 传入协程对象已弃用，因为这会导致 [令人迷惑的行为](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-example-wait-coroutine)。返回两个 Task/Future 集合: `(done, pending)`。用法:`done, pending = await asyncio.wait(aws) `*loop* 参数已弃用，计划在 Python 3.10 中移除。如指定 *timeout* (float 或 int 类型) 则它将被用于控制返回之前等待的最长秒数。请注意此函数不会引发 [`asyncio.TimeoutError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.TimeoutError)。当超时发生时，未完成的 Future 或 Task 将在指定秒数后被返回。*return_when* 指定此函数应在何时返回。它必须为以下常数之一:常数描述`FIRST_COMPLETED`函数将在任意可等待对象结束或取消时返回。`FIRST_EXCEPTION`函数将在任意可等待对象因引发异常而结束时返回。当没有引发任何异常时它就相当于 `ALL_COMPLETED`。`ALL_COMPLETED`函数将在所有可等待对象结束或取消时返回。与 [`wait_for()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.wait_for) 不同，`wait()` 在超时发生时不会取消可等待对象。注解 `wait()` 会自动将协程作为任务加入日程，以后将以 `(done, pending)` 集合形式返回显式创建的任务对象。因此以下代码并不会有预期的行为:`async def foo():     return 42  coro = foo() done, pending = await asyncio.wait({coro})  if coro in done:     # This branch will never be run! `以上代码段的修正方法如下:`async def foo():     return 42  task = asyncio.create_task(foo()) done, pending = await asyncio.wait({task})  if task in done:     # Everything will work as expected now. `直接向 `wait()` 传入协程对象的方式已弃用。

- `asyncio.``as_completed`(*aws*, ***, *loop=None*, *timeout=None*)

   并发地运行 *aws* 集合中的 [可等待对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio-awaitables)。返回一个 [`Future`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future) 对象的迭代器。返回的每个 Future 对象代表来自剩余可等待对象集合的最早结果。如果在所有 Future 对象完成前发生超时则将引发 [`asyncio.TimeoutError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.TimeoutError)。示例:`for f in as_completed(aws):     earliest_result = await f     # ... `

## [来自其他线程的日程安排](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id11)

- `asyncio.``run_coroutine_threadsafe`(*coro*, *loop*)

  向指定事件循环提交一个协程。线程安全。返回一个 [`concurrent.futures.Future`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.Future) 以等待来自其他 OS 线程的结果。此函数应该从另一个 OS 线程中调用，而非事件循环运行所在线程。示例:`# Create a coroutine coro = asyncio.sleep(1, result=3)  # Submit the coroutine to a given loop future = asyncio.run_coroutine_threadsafe(coro, loop)  # Wait for the result with an optional timeout argument assert future.result(timeout) == 3 `如果在协程内产生了异常，将会通知返回的 Future 对象。它也可被用来取消事件循环中的任务:`try:     result = future.result(timeout) except asyncio.TimeoutError:     print('The coroutine took too long, cancelling the task...')     future.cancel() except Exception as exc:     print(f'The coroutine raised an exception: {exc!r}') else:     print(f'The coroutine returned: {result!r}') `查看 [并发和多线程](https://docs.python.org/zh-cn/3/library/asyncio-dev.html#asyncio-multithreading) 章节的文档。不同与其他 asyncio 函数，此函数要求显式地传入 *loop* 参数。*3.5.1 新版功能.*

## [内省](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id12)

- `asyncio.``current_task`(*loop=None*)

  返回当前运行的 [`Task`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 实例，如果没有正在运行的任务则返回 `None`。如果 *loop* 为 `None` 则会使用 [`get_running_loop()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.get_running_loop) 获取当前事件循环。*3.7 新版功能.*

- `asyncio.``all_tasks`(*loop=None*)

  返回事件循环所运行的未完成的 [`Task`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 对象的集合。如果 *loop* 为 `None`，则会使用 [`get_running_loop()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.get_running_loop) 获取当前事件循环。*3.7 新版功能.*

## [Task 对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id13)

- *class* `asyncio.``Task`(*coro*, ***, *loop=None*)

  一个与 [`Future 类似`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future) 的对象，可运行 Python [协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine)。非线程安全。Task 对象被用来在事件循环中运行协程。如果一个协程在等待一个 Future 对象，Task 对象会挂起该协程的执行并等待该 Future 对象完成。当该 Future 对象 *完成*，被打包的协程将恢复执行。事件循环使用协同日程调度: 一个事件循环每次运行一个 Task 对象。而一个 Task 对象会等待一个 Future 对象完成，该事件循环会运行其他 Task、回调或执行 IO 操作。使用高层级的 [`asyncio.create_task()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.create_task) 函数来创建 Task 对象，也可用低层级的 [`loop.create_task()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.loop.create_task) 或 [`ensure_future()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.ensure_future) 函数。不建议手动实例化 Task 对象。要取消一个正在运行的 Task 对象可使用 [`cancel()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel) 方法。调用此方法将使该 Task 对象抛出一个 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常给打包的协程。如果取消期间一个协程正在等待一个 Future 对象，该 Future 对象也将被取消。[`cancelled()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancelled) 可被用来检测 Task 对象是否被取消。如果打包的协程没有抑制 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常并且确实被取消，该方法将返回 `True`。[`asyncio.Task`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task) 从 [`Future`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future) 继承了其除 [`Future.set_result()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future.set_result) 和 [`Future.set_exception()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future.set_exception) 以外的所有 API。Task 对象支持 [`contextvars`](https://docs.python.org/zh-cn/3/library/contextvars.html#module-contextvars) 模块。当一个 Task 对象被创建，它将复制当前上下文，然后在复制的上下文中运行其协程。*在 3.7 版更改:* 加入对 [`contextvars`](https://docs.python.org/zh-cn/3/library/contextvars.html#module-contextvars) 模块的支持。`cancel`()请求取消 Task 对象。这将安排在下一轮事件循环中抛出一个 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常给被封包的协程。协程在之后有机会进行清理甚至使用 [`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) ... ... `except CancelledError` ... [`finally`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#finally) 代码块抑制异常来拒绝请求。不同于 [`Future.cancel()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future.cancel)，[`Task.cancel()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel) 不保证 Task 会被取消，虽然抑制完全取消并不常见，也很不鼓励这样做。以下示例演示了协程是如何侦听取消请求的:`async def cancel_me():     print('cancel_me(): before sleep')      try:         # Wait for 1 hour         await asyncio.sleep(3600)     except asyncio.CancelledError:         print('cancel_me(): cancel sleep')         raise     finally:         print('cancel_me(): after sleep')  async def main():     # Create a "cancel_me" Task     task = asyncio.create_task(cancel_me())      # Wait for 1 second     await asyncio.sleep(1)      task.cancel()     try:         await task     except asyncio.CancelledError:         print("main(): cancel_me is cancelled now")  asyncio.run(main())  # Expected output: # #     cancel_me(): before sleep #     cancel_me(): cancel sleep #     cancel_me(): after sleep #     main(): cancel_me is cancelled now ``cancelled`()如果 Task 对象 *被取消* 则返回 `True`。当使用 [`cancel()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.cancel) 发出取消请求时 Task 会被 *取消*，其封包的协程将传播被抛入的 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常。`done`()如果 Task 对象 *已完成* 则返回 `True`。当 Task 所封包的协程返回一个值、引发一个异常或 Task 本身被取消时，则会被认为 *已完成*。`result`()返回 Task 的结果。如果 Task 对象 *已完成*，其封包的协程的结果会被返回 (或者当协程引发异常时，该异常会被重新引发。)如果 Task 对象 *被取消*，此方法会引发一个 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常。如果 Task 对象的结果还不可用，此方法会引发一个 [`InvalidStateError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.InvalidStateError) 异常。`exception`()返回 Task 对象的异常。如果所封包的协程引发了一个异常，该异常将被返回。如果所封包的协程正常返回则该方法将返回 `None`。如果 Task 对象 *被取消*，此方法会引发一个 [`CancelledError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.CancelledError) 异常。如果 Task 对象尚未 *完成*，此方法将引发一个 [`InvalidStateError`](https://docs.python.org/zh-cn/3/library/asyncio-exceptions.html#asyncio.InvalidStateError) 异常。`add_done_callback`(*callback*, ***, *context=None*)添加一个回调，将在 Task 对象 *完成* 时被运行。此方法应该仅在低层级的基于回调的代码中使用。要了解更多细节请查看 [`Future.add_done_callback()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future.add_done_callback) 的文档。`remove_done_callback`(*callback*)从回调列表中移除 *callback* 指定的回调。此方法应该仅在低层级的基于回调的代码中使用。要了解更多细节请查看 [`Future.remove_done_callback()`](https://docs.python.org/zh-cn/3/library/asyncio-future.html#asyncio.Future.remove_done_callback) 的文档。`get_stack`(***, *limit=None*)返回此 Task 对象的栈框架列表。如果所封包的协程未完成，这将返回其挂起所在的栈。如果协程已成功完成或被取消，这将返回一个空列表。如果协程被一个异常终止，这将返回回溯框架列表。框架总是从按从旧到新排序。每个被挂起的协程只返回一个栈框架。可选的 *limit* 参数指定返回框架的数量上限；默认返回所有框架。返回列表的顺序要看是返回一个栈还是一个回溯：栈返回最新的框架，回溯返回最旧的框架。(这与 traceback 模块的行为保持一致。)`print_stack`(***, *limit=None*, *file=None*)打印此 Task 对象的栈或回溯。此方法产生的输出类似于 traceback 模块通过 [`get_stack()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.get_stack) 所获取的框架。*limit* 参数会直接传递给 [`get_stack()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.Task.get_stack)。*file* 参数是输出所写入的 I/O 流；默认情况下输出会写入 [`sys.stderr`](https://docs.python.org/zh-cn/3/library/sys.html#sys.stderr)。*classmethod* `all_tasks`(*loop=None*)返回一个事件循环中所有任务的集合。默认情况下将返回当前事件循环中所有任务。如果 *loop* 为 `None`，则会使用 [`get_event_loop()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.get_event_loop) 函数来获取当前事件循环。此方法 **已弃用** 并将在 Python 3.9 中移除。请改用 [`asyncio.all_tasks()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.all_tasks) 函数。*classmethod* `current_task`(*loop=None*)返回当前运行任务或 `None`。如果 *loop* 为 `None`，则会使用 [`get_event_loop()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.get_event_loop) 函数来获取当前事件循环。此方法 **已弃用** 并将在 Python 3.9 中移除。请改用 [`asyncio.current_task()`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.current_task) 函数。



## [基于生成器的协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#id14)

注解

 

对基于生成器的协程的支持 **已弃用** 并计划在 Python 3.10 中移除。

基于生成器的协程是 async/await 语法的前身。它们是使用 `yield from` 语句创建的 Python 生成器，可以等待 Future 和其他协程。

基于生成器的协程应该使用 [`@asyncio.coroutine`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.coroutine) 装饰，虽然这并非强制。

- `@``asyncio.``coroutine`

  用来标记基于生成器的协程的装饰器。此装饰器使得旧式的基于生成器的协程能与 async/await 代码相兼容:`@asyncio.coroutine def old_style_coroutine():     yield from asyncio.sleep(1)  async def main():     await old_style_coroutine() `此装饰器 **已弃用** 并计划觉得 Python 3.10 中移除。此装饰器不应该被用于 [`async def`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#async-def) 协程。

- `asyncio.``iscoroutine`(*obj*)

  如果 *obj* 是一个 [协程对象](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine) 则返回 `True`。此方法不同于 [`inspect.iscoroutine()`](https://docs.python.org/zh-cn/3/library/inspect.html#inspect.iscoroutine) 因为它对基于生成器的协程返回 `True`。

- `asyncio.``iscoroutinefunction`(*func*)

  如果 *func* 是一个 [协程函数](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine) 则返回 `True`。此方法不同于 [`inspect.iscoroutinefunction()`](https://docs.python.org/zh-cn/3/library/inspect.html#inspect.iscoroutinefunction) 因为它对以 [`@coroutine`](https://docs.python.org/zh-cn/3/library/asyncio-task.html#asyncio.coroutine) 装饰的基于生成器的协程函数返回 `True`。



https://docs.python.org/zh-cn/3/library/asyncio-task.html