---
title: 【译】Android: 自定义View
description: 【译】Android: 自定义View
---

# 【译】Android: 自定义View



> [原文链接](https://link.jianshu.com/?t=https://medium.com/@romandanylyk96/android-draw-a-custom-view-ef79fe2ff54b#.hl4rzavps)
> 部分译文是按自己的理解翻译的，如有错漏，还请指正

### 简介

每天我们都会使用很多的应用程序，尽管他们有不同的约定，但大多数应用的设计是非常相似的。这就是为什么许多客户要求使用一些其他应用程序没有的设计，使得应用程序显得独特和不同。

如果功能布局要求非常定制化，已经不能由Android内置的View创建 —这时候就需要使用自定义View了。而这意味着在大多数情况下，我们将需要相当长的时间来完成它。但这并不意味着我们不应该这样做，因为实现它是非常令人兴奋和有趣的。

我最近面临了类似的情况：我的任务是使用`ViewPager`实现Android应用引导页。不同于iOS，Android并没有提供这样的View，所以我不得不编写一个自定义View来实现它。

我花了一些时间来实现它。幸运的是，时下很多开源项目都有类似可复用的View，这节省了我和其他开发者的时间。我决定基于这种View创建一个公共库。如果你有类似的功能需求并且缺乏时间实现它，可以在[github repo](https://link.jianshu.com/?t=https://github.com/romandanylyk/PageIndicatorView)发现它。



![img](assets/android_view_2/1000.jpeg)

Sample of using PageIndicatorView

### 绘制！

因为编写自定义View比起普通的View更耗时，你应该只在为了实现特定的功能但没有更简单的方法情况下使用自定义View，或者你希望通过自定义View解决以下问题：

1. 性能。如果你布局里面有很多View，你想通自定义View优化它，使其更轻量。
2. 视图层次结构复杂。
3. 一个完全自定义的View，需要手动绘制才能实现。

如果你还没有尝试过编写自定义View，这篇文章将教会你绘制扁平的自定义View的一些技巧。我将会告诉你整体的视图结构，如何实现具体的功能，不要重犯常见的错误，以及实现动画效果！

我们需要知道的第一件事 --View的生命周期。不知出于某种原因，谷歌并没有提供View生命周期的图表，由于开发者普遍对其有误解，导致了一些意想不到的错误和问题，所以我们要认清这过程。



![img](assets/android_view_2/692.jpeg)

view lifecycle

#### 构造函数

每个View的生命都是从构造函数开始。而且这是一个绘制初始化，进行各种计算，设定默认值或做任何我们需要的事情很好的地方。

但是，为了使我们的View更易于使用和配置，Android提供了很有用的`AttributeSet`接口。它很容易实现，而且绝对值得花时间去了解和实现它，因为它会帮助你（和你的团队）通过静态参数来设置View，对于以后新特性加入或者新屏幕拓展性支持也更好。

首先，创建一个新的文件`attrs.xml`。所有不同的自定义View属性都可以放在该文件中。正如你看到的这个例子，我们有一个PageIndicatorView和它的唯一属性piv_count。



![img](https://upload-images.jianshu.io/upload_images/1625938-ef7082a5d6a7f33a.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

Custom Attributes sample

紧接着在View的构造函数中，你需要获取这个属性并使用它，如下图所示。

```
public PageIndicatorView(Context context, AttributeSet attrs) {
    super(context, attrs);
    TypedArray typedArray = getContext().obtainStyledAttributes(attrs, R.styleable.PageIndicatorView);
    int count = typedArray.getInt(R.styleable.PageIndicatorView_piv_count,0);
    typedArray.recycle();
}
```

##### 注意：

- 在创建自定义属性使用一个简单的前缀，以避免与其它View类似的属性名称冲突。一般我们使用View名称缩写，就像例子中的piv_。
- 如果你使用的是Android Studio，一旦你使用完属性，lint会建议你调用`recycle()`方法 。The reason is just to get rid of inefficiently bound data that’s not gonna be used again。[译者注：翻译有点拗口，其实就是回收TypedArray，以便后面重用]

#### onAttachedToWindow

父View调用`addView(View)`后，这个View将被依附到一个窗口。在这个阶段，我们的View会知道它被包围的其他view。如果你的View和其他View在相同的`layout.xml`,这是通过id找到他们的好地方（你可以通过属性进行设置），同时可以保存为全局（如果需要）的引用。

#### onMeasure

这意味着我们的自定义View到了处理自己的大小的时候。这是非常重要的方法，因为在大多数情况下，你的View需要有特定的大小以适应你的布局。

当你重写此方法，需要记得的是，最终要设置`setMeasuredDimension(int width, int height)` 。



![img](assets/android_view_2/800.jpeg)

onMeasure

当处理自定义View的大小时候，使用者可能通过`layout.xml`或者动态设置了具体的大小。要正确地计算它，我们需要做几件事情。

1.计算你的View内容所需的大小（宽度和高度）。
2.获取你的View MeasureSpec大小和模式（宽度和高度）。

`protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) { int widthMode = MeasureSpec.getMode(widthMeasureSpec); int widthSize = MeasureSpec.getSize(widthMeasureSpec); int heightMode = MeasureSpec.getMode(heightMeasureSpec); int heightSize = MeasureSpec.getSize(heightMeasureSpec); }`
3.检查MeasureSpec 设置和调整View（宽度和高度）的尺寸模式。

```
int width; if (widthMode == MeasureSpec.EXACTLY) { width = widthSize; } else if (widthMode == MeasureSpec.AT_MOST) { width = Math.min(desiredWidth, widthSize); } else { width = desiredWidth; }
```

##### 注意：

看看MeasureSpec的值：

- MeasureSpec.EXACTLY 意味着硬编码大小值，所以你应该设置指定的宽度或高度。
- MeasureSpec.AT_MOST 用于表明你的View匹配父View的大小，
  所以它应该和他想要的大小一样大。
  [译者注：此时View尺寸只要不超过父View允许的最大尺寸即可]
- MeasureSpec.UNSPECIFIED 实际上是视图包装尺寸。因此，你可以使用上面计算所需的大小。

在通过`setMeasuredDimension`设置最终值之前，以防万一，可以检查这些值不为负数。这可以避免在布局预览时一些问题。

#### onLayout

此方法分配大小和位置给它的每一个子View。正因为如此，我们正在研究一个扁平的自定义视图（继承简单的View）不具有任何子View，那么就没有理由重写此方法。[译者注：实现可以参考[Custom Layouts on Android](https://link.jianshu.com/?t=http://lucasr.org/2014/05/12/custom-layouts-on-android/)]

#### onDraw

这就是发生魔法的地方。在这里，使用`Canvas`和`Paint`对象你将可以画任何你需要的东西。
一个`Canvas`实例从onDraw参数得来，它一般用于绘制不同形状，而`Paint`对象定义形状颜色。简单地说，`Canvas`用于绘制对象，而`Paint`用于造型。它们无处不在，无论绘制的是一个直线，圆或长方形。



![img](https://upload-images.jianshu.io/upload_images/1625938-b5fdb6243c71024e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

onDraw() — methods example

使自定义View，要始终牢记onDraw会花费大量的时间。当布局有一些变化，滚动、快速滑动都会导致重新绘制。所以这就是为什么Android Studio也建议：避免在onDraw中进行对象分配的操作，对象应该只创建一次并在将来重用。



![img](assets/android_view_2/700.jpeg)

onDraw() — Paint object recreation



![img](assets/android_view_2/700-0001426.jpeg)

onDraw() — Paint object reuse

##### 注意：

- 在执行绘制时始终牢记重用对象，而不创建新的。不要依赖于IDE高亮一个潜在的问题，而是自己有意识地去做这件事，因为在onDraw调用一个内部会创建对象的方法时，IDE无法识别它。
- 同时请不要硬编码View大小。其他开发者在使用时可以定义不同的大小，所以View大小应该取决于它有什么尺寸。

#### View 更新

从View的生命周期图可以得知，可以重绘View自身有两种方法。`invalidate()`和`requestLayout()`方法会帮助你在运行时动态改变View状态。但为什么需要两个方法？

- `invalidate()`用来简单重绘View。例如更新其文本，色彩或触摸交互性。View将只调用`onDraw()`方法再次更新其状态。
- `requestLayout()`方法，你可以看到其将会从`onMeasure()开始更新View。这意味着你的View更新后，它改变它的大小，你需要再次测量它，并依赖于新的大小来重新绘制。

#### 动画

在自定义View中，动画是一帧一帧的过程。这意味着，如果你想使一个圆半径从小变大，你将需要逐步增加半径并调用`invalidate()`来重绘它。

在自定义View动画中，ValueAnimator是你的好朋友。下面这个类将帮助你从任何值开始执行动画到最后，甚至支持`Interpolator`（如果需要）。

```
ValueAnimator animator = ValueAnimator.ofInt(0, 100);
animator.setDuration(1000);
animator.setInterpolator(new DecelerateInterpolator());
animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
  public void onAnimationUpdate(ValueAnimator animation) {
    int newRadius = (int) animation.getAnimatedValue();
  }
});
```

##### 注意：

当每一次新的动画值出来时，不要忘记调用`invalidate()`。



![img](assets/android_view_2/450.gif)

Sample of animation via ValueAnimator

希望这篇文章可以帮助你实现你的第一个自定义View，如果你想更多地了解它，可以看看这个[视频](https://link.jianshu.com/?t=https://www.youtube.com/watch?v=4NNmMO8Aykw&feature=youtu.be)。

[原文](https://www.jianshu.com/p/29bb35a4860e)

