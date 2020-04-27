# 为您的Flutter应用程序添加交互

**你将会学到:**

- 如何响应点击(tap).
- 如何创建自定义widget.
- stateless（无状态）和 stateful（有状态）widgets的区别.

如何修改你的应用程序，使其对用户动作做出反应？在本教程中，您将为widget添加交互。 具体来说，您将通过创建一个管理两个无状态widget的自定义有状态的widget来使图标可以点击。

### 内容

- [Stateful 和 stateless widgets](https://flutterchina.club/tutorials/interactive/#stateful-stateless)
- 创建一个stateful widget
  - [第1步: 决定哪个widget管理widget的状态(state)](https://flutterchina.club/tutorials/interactive/#step-1)
  - [第2步: 创建StatefulWidget子类](https://flutterchina.club/tutorials/interactive/#step-2)
  - [第3步: 创建State子类](https://flutterchina.club/tutorials/interactive/#step-3)
  - [第4步: 将stateful widget 插入到 widget 树](https://flutterchina.club/tutorials/interactive/#step-4)
  - [遇到问题?](https://flutterchina.club/tutorials/interactive/#problems)
- 管理状态
  - [widget管理自己的state](https://flutterchina.club/tutorials/interactive/#self-managed)
  - [父组件管理state](https://flutterchina.club/tutorials/interactive/#parent-managed)
  - [混合管理state](https://flutterchina.club/tutorials/interactive/#mix-and-match)
- 其它交互式widgets
  - [标砖widgets](https://flutterchina.club/tutorials/interactive/#standard-widgets)
  - [Material Components](https://flutterchina.club/tutorials/interactive/#material-components)
- [资源](https://flutterchina.club/tutorials/interactive/#resources)

## 准备

如果您已经根据[在Flutter中构建布局](https://flutterchina.club/tutorials/layout/)一节的构建好了布局，请跳过本块。

- 确保您已经[配置](https://flutterchina.club/get-started/install/)好了Flutter开发环境.
- [创建一个基础的Flutter app.](https://flutterchina.club/get-started/test-drive/#create-app)
- 用Github上的[`main.dart`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/lakes/main.dart) 替换本地工程 `lib/main.dart`
- 用Github上的[`pubspec.yaml`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/lakes/pubspec.yaml)替换本地工程`pubspec.yaml`
- 在你的工程中创建一个 `images` 文件夹, 并添加 [`lake.jpg`.](https://github.com/flutter/website/blob/master/_includes/code/layout/lakes/images/lake.jpg)

一旦你有一个连接和启用的设备，或者你已经启动了[iOS模拟器](https://flutterchina.club/setup-macos/#set-up-the-ios-simulator)（Flutter安装一节介绍过），就会很容易开始！ </aside>

[在Flutter中构建布局](https://flutter.io/tutorials/layout/)一节展示了如何构建下面截图所示的布局。

![The starting Lakes app that we will modify](https://flutterchina.club/tutorials/interactive/images/lakes.jpg)

当应用第一次启动时，这颗星形图标是实心红色，表明这个湖以前已经被收藏了。星号旁边的数字表示41个人对此湖感兴趣。 完成本教程后，点击星形图标将取消收藏状态，然后用轮廓线的星形图标代替实心的，并减少计数。再次点击会重新收藏，并增加计数。

![the custom widget you'll create](https://flutterchina.club/tutorials/interactive/images/favorited-not-favorited.png)

为了实现这个，您将创建一个包含星号和计数的自定义widget，它们都是widget。 因为点击星形图标会更改这两个widget的状态，所以同一个widget应该同时管理这两个widget。



## Stateful（有状态） 和 stateless（无状态） widgets

**什么是重点?**

- 有些widgets是有状态的, 有些是无状态的
- 如果用户与widget交互，widget会发生变化，那么它就是有状态的.
- widget的状态（state）是一些可以更改的值, 如一个slider滑动条的当前值或checkbox是否被选中.
- widget的状态保存在一个State对象中, 它和widget的布局显示分离。
- 当widget状态改变时, State 对象调用`setState()`, 告诉框架去重绘widget.

*stateless* widget 没有内部状态. [Icon](https://docs.flutter.io/flutter/widgets/Icon-class.html)、 [IconButton](https://docs.flutter.io/flutter/material/IconButton-class.html), 和[Text](https://docs.flutter.io/flutter/widgets/Text-class.html) 都是无状态widget, 他们都是 [StatelessWidget](https://docs.flutter.io/flutter/widgets/StatelessWidget-class.html)的子类。

*stateful* widget 是动态的. 用户可以和其交互 (例如输入一个表单、 或者移动一个slider滑块),或者可以随时间改变 (也许是数据改变导致的UI更新). [Checkbox](https://docs.flutter.io/flutter/material/Checkbox-class.html), [Radio](https://docs.flutter.io/flutter/material/Radio-class.html), [Slider](https://docs.flutter.io/flutter/material/Slider-class.html), [InkWell](https://docs.flutter.io/flutter/material/InkWell-class.html), [Form](https://docs.flutter.io/flutter/widgets/Form-class.html), and [TextField](https://docs.flutter.io/flutter/material/TextField-class.html) 都是 stateful widgets, 他们都是 [StatefulWidget](https://docs.flutter.io/flutter/widgets/StatefulWidget-class.html)的子类。



## 创建一个有状态的widget

**重点：**

- 要创建一个自定义有状态widget，需创建两个类：StatefulWidget和State
- 状态对象包含widget的状态和build() 方法。
- 当widget的状态改变时，状态对象调用`setState()`，告诉框架重绘widget

在本节中，您将创建一个自定义有状态的widget。 您将使用一个自定义有状态widget来替换两个无状态widget - 红色实心星形图标和其旁边的数字计数 - 该widget用两个子widget管理一行：IconButton和Text。

实现一个自定义的有状态widget需要创建两个类:

- 定义一个widget类，继承自StatefulWidget.
- 包含该widget状态并定义该widget `build()`方法的类，它继承自State.

本节展示如何为Lakes应用程序构建一个名为FavoriteWidget的StatefulWidget。第一步是选择如何管理FavoriteWidget的状态。



### Step 1: 决定哪个对象管理widget的状态

Widget的状态可以通过多种方式进行管理，但在我们的示例中，widget本身（FavoriteWidget）将管理自己的状态。 在这个例子中，切换星形图标是一个独立的操作，不会影响父窗口widget或其他用户界面，因此该widget可以在内部处理它自己的状态。

在[管理状态](https://flutterchina.club/tutorials/interactive/#managing-state)中了解更多关于widget和状态的分离以及如何管理状态的信息。



### Step 2: 创建StatefulWidget子类

FavoriteWidget类管理自己的状态，因此它重写`createState()`来创建状态对象。 框架会在构建widget时调用`createState()`。在这个例子中，`createState()`创建_FavoriteWidgetState的实例，您将在下一步中实现该实例。

```dart
class FavoriteWidget extends StatefulWidget {
  @override
  _FavoriteWidgetState createState() => new _FavoriteWidgetState();
}
```

**注意:** 以下划线（_）开头的成员或类是私有的。有关更多信息，请参阅[Dart语言参考](https://www.dartlang.org/guides/language/language-tour)中的[库和可见性](https://www.dartlang.org/guides/language/language-tour#libraries-and-visibility)部分 。



### Step 3: 创建State子类

自定义State类存储可变信息 - 可以在widget的生命周期内改变逻辑和内部状态。 当应用第一次启动时，用户界面显示一个红色实心的星星形图标，表明该湖已经被收藏，并有41个“喜欢”。状态对象存储这些信息在`_isFavorited`和`_favoriteCount`变量。

状态对象也定义了`build`方法。此`build`方法创建一个包含红色IconButton和Text的行。 该widget使用[IconButton](https://docs.flutter.io/flutter/material/IconButton-class.html)（而不是Icon）， 因为它具有一个onPressed属性，该属性定义了处理点击的回调方法。IconButton也有一个icon的属性，持有Icon。

按下IconButton时会调用`_toggleFavorite()`方法，然后它会调用`setState()`。 调用`setState()`是至关重要的，因为这告诉框架，widget的状态已经改变，应该重绘。 `_toggleFavorite`在: 1）实心的星形图标和数字“41” 和 2）虚心的星形图标和数字“40”之间切换UI。

```dart
class _FavoriteWidgetState extends State<FavoriteWidget> {
  bool _isFavorited = true;
  int _favoriteCount = 41;

  void _toggleFavorite() {
    setState(() {
      // If the lake is currently favorited, unfavorite it.
      if (_isFavorited) {
        _favoriteCount -= 1;
        _isFavorited = false;
        // Otherwise, favorite it.
      } else {
        _favoriteCount += 1;
        _isFavorited = true;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return new Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        new Container(
          padding: new EdgeInsets.all(0.0),
          child: new IconButton(
            icon: (_isFavorited
                ? new Icon(Icons.star)
                : new Icon(Icons.star_border)),
            color: Colors.red[500],
            onPressed: _toggleFavorite,
          ),
        ),
        new SizedBox(
          width: 18.0,
          child: new Container(
            child: new Text('$_favoriteCount'),
          ),
        ),
      ],
    );
  }
}
```

**提示:** 当文本在40和41之间变化时，将文本放在SizedBox中并设置其宽度可防止出现明显的“跳跃” ，因为这些值具有不同的宽度。



### Step 4: 将有stateful widget插入widget树中

将您自定义stateful widget在build方法中添加到widget树中。首先，找到创建图标和文本的代码，并删除它：

```dart
// ...
new Icon(
  Icons.star,
  color: Colors.red[500],
),
new Text('41')
// ...
```

在相同的位置创建stateful widget：

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Widget titleSection = new Container(
      // ...
      child: new Row(
        children: [
          new Expanded(
            child: new Column(
              // ...
          ),
          new FavoriteWidget(),
        ],
      ),
    );

    return new MaterialApp(
      // ...
    );
  }
}
```


好了! 当您热重载应用程序后，星形图标就会响应点击了.

### 遇到问题?

如果您的代码无法运行，请在IDE中查找可能的错误。[调试Flutter应用程序](https://flutterchina.club/debugging/)可能会有所帮助。如果仍然无法找到问题，请根据GitHub上的示例检查代码。

- [`lib/main.dart`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/lakes-interactive/main.dart)
- [`pubspec.yaml`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/lakes-interactive/pubspec.yaml)—此文件没有变化
- [`lakes.jpg`](https://github.com/flutter/website/blob/master/_includes/code/layout/lakes-interactive/images/lake.jpg)—此文件没有变化

------

本页面的其余部分介绍了可以管理widget状态的几种方式，并列出了其他可用的可交互的widget。



## 管理状态

**重点是什么?**

- 有多种方法可以管理状态.
- 选择使用何种管理方法
- 如果不是很清楚时, 那就在父widget中管理状态吧.

谁管理着stateful widget的状态？widget本身？父widget？都会？另一个对象？答案是……这取决于实际情况。 有几种有效的方法可以给你的widget添加互动。作为小部件设计师。以下是管理状态的最常见的方法：

- [widget管理自己的state](https://flutterchina.club/tutorials/interactive/#self-managed)
- [父widget管理 widget状态](https://flutterchina.club/tutorials/interactive/#parent-managed)
- [混搭管理（父widget和widget自身都管理状态））](https://flutterchina.club/tutorials/interactive/#mix-and-match)

如何决定使用哪种管理方法？以下原则可以帮助您决定：

- 如果状态是用户数据，如复选框的选中状态、滑块的位置，则该状态最好由父widget管理
- 如果所讨论的状态是有关界面外观效果的，例如动画，那么状态最好由widget本身来管理.

如果有疑问，首选是在父widget中管理状态

我们将通过创建三个简单示例来举例说明管理状态的不同方式：TapboxA、TapboxB和TapboxC。 这些例子功能是相似的 - 每创建一个容器，当点击时，在绿色或灰色框之间切换。 `_active`确定颜色：绿色为true,灰色为false。

![a large green box with the text, 'Active'](https://flutterchina.club/tutorials/interactive/images/tapbox-active-state.png)      ![a large grey box with the text, 'Inactive'](https://flutterchina.club/tutorials/interactive/images/tapbox-inactive-state.png)

这些示例使用[GestureDetector](https://docs.flutter.io/flutter/widgets/GestureDetector-class.html)捕获Container上的用户动作。



### widget管理自己的状态

有时，widget在内部管理其状态是最好的。例如， 当[ListView](https://docs.flutter.io/flutter/widgets/ListView-class.html)的内容超过渲染框时， ListView自动滚动。大多数使用ListView的开发人员不想管理ListView的滚动行为，因此ListView本身管理其滚动偏移量。

_TapboxAState 类:

- 管理TapboxA的状态.
- 定义`_active`：确定盒子的当前颜色的布尔值.
- 定义`_handleTap()`函数，该函数在点击该盒子时更新`_active`,并调用`setState()`更新UI.
- 实现widget的所有交互式行为.

```dart
// TapboxA 管理自身状态.

//------------------------- TapboxA ----------------------------------

class TapboxA extends StatefulWidget {
  TapboxA({Key key}) : super(key: key);

  @override
  _TapboxAState createState() => new _TapboxAState();
}

class _TapboxAState extends State<TapboxA> {
  bool _active = false;

  void _handleTap() {
    setState(() {
      _active = !_active;
    });
  }

  Widget build(BuildContext context) {
    return new GestureDetector(
      onTap: _handleTap,
      child: new Container(
        child: new Center(
          child: new Text(
            _active ? 'Active' : 'Inactive',
            style: new TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
        width: 200.0,
        height: 200.0,
        decoration: new BoxDecoration(
          color: _active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
      ),
    );
  }
}

//------------------------- MyApp ----------------------------------

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Flutter Demo',
      home: new Scaffold(
        appBar: new AppBar(
          title: new Text('Flutter Demo'),
        ),
        body: new Center(
          child: new TapboxA(),
        ),
      ),
    );
  }
}
```

**Dart code:** [`lib/main.dart`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/tapbox-a/main.dart)

------



### 父widget管理widget的state

对于父widget来说，管理状态并告诉其子widget何时更新通常是最有意义的。 例如，[IconButton](https://docs.flutter.io/flutter/material/IconButton-class.html)允许您将图标视为可点按的按钮。 IconButton是一个无状态的小部件，因为我们认为父widget需要知道该按钮是否被点击来采取相应的处理。

在以下示例中，TapboxB通过回调将其状态导出到其父项。由于TapboxB不管理任何状态，因此它的父类为StatelessWidget。

ParentWidgetState 类:

- 为TapboxB 管理`_active`状态.
- 实现`_handleTapboxChanged()`，当盒子被点击时调用的方法.
- 当状态改变时，调用`setState()`更新UI.

TapboxB 类:

- 继承`StatelessWidget`类，因为所有状态都由其父widget处理.
- 当检测到点击时，它会通知父widget.

```dart
// ParentWidget 为 TapboxB 管理状态.

//------------------------ ParentWidget --------------------------------

class ParentWidget extends StatefulWidget {
  @override
  _ParentWidgetState createState() => new _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  bool _active = false;

  void _handleTapboxChanged(bool newValue) {
    setState(() {
      _active = newValue;
    });
  }

  @override
  Widget build(BuildContext context) {
    return new Container(
      child: new TapboxB(
        active: _active,
        onChanged: _handleTapboxChanged,
      ),
    );
  }
}

//------------------------- TapboxB ----------------------------------

class TapboxB extends StatelessWidget {
  TapboxB({Key key, this.active: false, @required this.onChanged})
      : super(key: key);

  final bool active;
  final ValueChanged<bool> onChanged;

  void _handleTap() {
    onChanged(!active);
  }

  Widget build(BuildContext context) {
    return new GestureDetector(
      onTap: _handleTap,
      child: new Container(
        child: new Center(
          child: new Text(
            active ? 'Active' : 'Inactive',
            style: new TextStyle(fontSize: 32.0, color: Colors.white),
          ),
        ),
        width: 200.0,
        height: 200.0,
        decoration: new BoxDecoration(
          color: active ? Colors.lightGreen[700] : Colors.grey[600],
        ),
      ),
    );
  }
}
```

**Dart code:** [`lib/main.dart`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/tapbox-b/main.dart)

**提示:** 在创建API时，请考虑使用@required为代码所依赖的任何参数使用注解。 要使用@required注解，请导入[foundation library](https://docs.flutter.io/flutter/foundation/foundation-library.html)（该库重新导出Dart的[meta.dart](https://pub.dartlang.org/packages/meta)）

```
 'package: flutter/foundation.dart';
 
```

------



### 混合管理

对于一些widget来说，混搭管理的方法最有意义的。在这种情况下，有状态widget管理一些状态，并且父widget管理其他状态。

在TapboxC示例中，点击时，盒子的周围会出现一个深绿色的边框。点击时，边框消失，盒子的颜色改变。 TapboxC将其`_active`状态导出到其父widget中，但在内部管理其`_highlight`状态。这个例子有两个状态对象`_ParentWidgetState`和`_TapboxCState`。

_ParentWidgetState 对象:

- 管理`_active` 状态.
- 实现 `_handleTapboxChanged()`, 当盒子被点击时调用.
- 当点击盒子并且`_active`状态改变时调用`setState()`更新UI

_TapboxCState 对象:

- 管理`_highlight` state.
- `GestureDetector`监听所有tap事件。当用户点下时，它添加高亮（深绿色边框）；当用户释放时，会移除高亮。
- 当按下、抬起、或者取消点击时更新`_highlight`状态，调用`setState()`更新UI。
- 当点击时，将状态的改变传递给父widget.

```dart
//---------------------------- ParentWidget ----------------------------

class ParentWidget extends StatefulWidget {
  @override
  _ParentWidgetState createState() => new _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  bool _active = false;

  void _handleTapboxChanged(bool newValue) {
    setState(() {
      _active = newValue;
    });
  }

  @override
  Widget build(BuildContext context) {
    return new Container(
      child: new TapboxC(
        active: _active,
        onChanged: _handleTapboxChanged,
      ),
    );
  }
}

//----------------------------- TapboxC ------------------------------

class TapboxC extends StatefulWidget {
  TapboxC({Key key, this.active: false, @required this.onChanged})
      : super(key: key);

  final bool active;
  final ValueChanged<bool> onChanged;

  _TapboxCState createState() => new _TapboxCState();
}

class _TapboxCState extends State<TapboxC> {
  bool _highlight = false;

  void _handleTapDown(TapDownDetails details) {
    setState(() {
      _highlight = true;
    });
  }

  void _handleTapUp(TapUpDetails details) {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTapCancel() {
    setState(() {
      _highlight = false;
    });
  }

  void _handleTap() {
    widget.onChanged(!widget.active);
  }

  Widget build(BuildContext context) {
    // This example adds a green border on tap down.
    // On tap up, the square changes to the opposite state.
    return new GestureDetector(
      onTapDown: _handleTapDown, // Handle the tap events in the order that
      onTapUp: _handleTapUp, // they occur: down, up, tap, cancel
      onTap: _handleTap,
      onTapCancel: _handleTapCancel,
      child: new Container(
        child: new Center(
          child: new Text(widget.active ? 'Active' : 'Inactive',
              style: new TextStyle(fontSize: 32.0, color: Colors.white)),
        ),
        width: 200.0,
        height: 200.0,
        decoration: new BoxDecoration(
          color:
              widget.active ? Colors.lightGreen[700] : Colors.grey[600],
          border: _highlight
              ? new Border.all(
                  color: Colors.teal[700],
                  width: 10.0,
                )
              : null,
        ),
      ),
    );
  }
}
```

另一种实现可能会将高亮状态导出到父widget，同时保持`_active`状态为内部，但如果您要求某人使用该TapBox，他们可能会抱怨说没有多大意义。 开发人员只会关心该框是否处于活动状态。开发人员可能不在乎高亮显示是如何管理的，并且倾向于让TapBox处理这些细节。

**Dart code:** [`lib/main.dart`](https://raw.githubusercontent.com/flutter/website/master/_includes/code/layout/tapbox-c/main.dart)

------



## 其他交互式widgets

Flutter提供各种按钮和类似的交互式widget。这些widget中的大多数实现了[Material Design 指南](https://material.io/guidelines/)， 它们定义了一组具有质感的UI组件。

如果你愿意，你可以使用[GestureDetector](https://docs.flutter.io/flutter/widgets/GestureDetector-class.html)来给任何自定义widget添加交互性。 您可以在[管理状态](https://flutterchina.club/tutorials/interactive/#managing-state)和[Flutter Gallery](https://github.com/flutter/flutter/tree/master/examples/flutter_gallery)中找到GestureDetector的示例。

**注意:** Futter还提供了一组名为[Cupertino](https://docs.flutter.io/flutter/cupertino/cupertino-library.html)的iOS风格的小部件 。

When you need interactivity, it’s easiest to use one of the prefabricated widgets. Here’s a partial list: 当你需要交互性时，最容易的是使用预制的widget。这是预置widget部分列表:

### 标准 widgets:

- [Form](https://docs.flutter.io/flutter/widgets/Form-class.html)
- [FormField](https://docs.flutter.io/flutter/widgets/FormField-class.html)

### Material Components:

- [Checkbox](https://docs.flutter.io/flutter/material/Checkbox-class.html)
- [DropdownButton](https://docs.flutter.io/flutter/material/DropdownButton-class.html)
- [FlatButton](https://docs.flutter.io/flutter/material/FlatButton-class.html)
- [FloatingActionButton](https://docs.flutter.io/flutter/material/FloatingActionButton-class.html)
- [IconButton](https://docs.flutter.io/flutter/material/IconButton-class.html)
- [Radio](https://docs.flutter.io/flutter/material/Radio-class.html)
- [RaisedButton](https://docs.flutter.io/flutter/material/RaisedButton-class.html)
- [Slider](https://docs.flutter.io/flutter/material/Slider-class.html)
- [Switch](https://docs.flutter.io/flutter/material/Switch-class.html)
- [TextField](https://docs.flutter.io/flutter/material/TextField-class.html)



## 资源

给您的应用添加交互时，以下资源可能会有所帮助

- [处理手势](https://flutter.io/widgets-intro/#handling-gestures), [Flutter Widget框架总览](https://flutter.io/widgets-intro/)的一节
  如何创建一个按钮并使其响应用户动作.
- [Flutter中的手势](https://flutter.io/gestures/)
  Flutter手势机制的描述
- [Flutter API 文档](https://docs.flutter.io/)
  所有Flutter库的参考文档.
- [Flutter Gallery](https://github.com/flutter/flutter/tree/master/examples/flutter_gallery)
  一个Demo应用程序，展示了许多Material Components和其他Flutter功能
- [Flutter的分层设计 (video)](https://www.youtube.com/watch?v=dkyY9WCGMi0)
  此视频包含有关有状态和无状态widget的信息。由Google工程师Ian Hickson讲解。

[原文](https://flutterchina.club/tutorials/interactive/)