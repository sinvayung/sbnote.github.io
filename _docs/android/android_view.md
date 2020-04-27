---
title: Android自定义View全解
description: Android自定义View全解
---

# Android自定义View全解

# 目录

![image-20190212134418595](assets/android_view/image-20190212134418595.png)

# 1. 自定义View基础

## 1.1 分类

自定义View的实现方式有以下几种

| 类型              | 定义                                                         |
| ----------------- | ------------------------------------------------------------ |
| 自定义组合控件    | 多个控件组合成为一个新的控件，方便多处复用                   |
| 继承系统View控件  | 继承自TextView等系统控件，在系统控件的基础功能上进行扩展     |
| 继承View          | 不复用系统控件逻辑，继承View进行功能定义                     |
| 继承系统ViewGroup | 继承自LinearLayout等系统控件，在系统控件的基础功能上进行扩展 |
| 继承ViewViewGroup | 不复用系统控件逻辑，继承ViewGroup进行功能定义                |

## 1.2 View绘制流程

View的绘制基本由measure()、layout()、draw()这个三个函数完成

| 函数      | 作用                         | 相关方法                                     |
| --------- | ---------------------------- | -------------------------------------------- |
| measure() | 测量View的宽高               | measure(),setMeasuredDimension(),onMeasure() |
| layout()  | 计算当前View以及子View的位置 | layout(),onLayout(),setFrame()               |
| draw()    | 视图的绘制工作               | draw(),onDraw()                              |

# 1.3 坐标系

在Android坐标系中，以屏幕左上角作为原点，这个原点向右是X轴的正轴，向下是Y轴正轴。如下所示：

![image-20190212134501403](assets/android_view/image-20190212134501403.png)

Android坐标系.png

除了Android坐标系，还存在View坐标系，View坐标系内部关系如图所示。

![image-20190212134531559](assets/android_view/image-20190212134531559.png)

视图坐标系.png

### View获取自身高度

由上图可算出View的高度：

- width = getRight() - getLeft();
- height = getBottom() - getTop();

View的源码当中提供了getWidth()和getHeight()方法用来获取View的宽度和高度，其内部方法和上文所示是相同的，我们可以直接调用来获取View得宽高。

### View自身的坐标

通过如下方法可以获取View到其父控件的距离。

- getTop()；获取View到其父布局顶边的距离。
- getLeft()；获取View到其父布局左边的距离。
- getBottom()；获取View到其父布局底边的距离。
- getRight()；获取View到其父布局右边的距离。

## 1.4 构造函数

无论是我们继承系统View还是直接继承View，都需要对构造函数进行重写，构造函数有多个，至少要重写其中一个才行。如我们新建`TestView`，

```
public class TestView extends View {
    /**
     * 在java代码里new的时候会用到
     * @param context
     */
    public TestView(Context context) {
        super(context);
    }

    /**
     * 在xml布局文件中使用时自动调用
     * @param context
     */
    public TestView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
    }

    /**
     * 不会自动调用，如果有默认style时，在第二个构造函数中调用
     * @param context
     * @param attrs
     * @param defStyleAttr
     */
    public TestView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }


    /**
     * 只有在API版本>21时才会用到
     * 不会自动调用，如果有默认style时，在第二个构造函数中调用
     * @param context
     * @param attrs
     * @param defStyleAttr
     * @param defStyleRes
     */
    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    public TestView(Context context, @Nullable AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
    }
}
```

## 1.5 自定义属性

Android系统的控件以android开头的都是系统自带的属性。为了方便配置自定义View的属性，我们也可以自定义属性值。
Android自定义属性可分为以下几步:

1. 自定义一个View
2. 编写values/attrs.xml，在其中编写styleable和item等标签元素
3. 在布局文件中View使用自定义的属性（注意namespace）
4. 在View的构造方法中通过TypedArray获取

## 实例说明

- 自定义属性的声明文件

```
    <?xml version="1.0" encoding="utf-8"?>
    <resources>
        <declare-styleable name="test">
            <attr name="text" format="string" />
            <attr name="testAttr" format="integer" />
        </declare-styleable>
    </resources>
```

- 自定义View类

```
public class MyTextView extends View {
    private static final String TAG = MyTextView.class.getSimpleName();

    //在View的构造方法中通过TypedArray获取
    public MyTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
        TypedArray ta = context.obtainStyledAttributes(attrs, R.styleable.test);
        String text = ta.getString(R.styleable.test_testAttr);
        int textAttr = ta.getInteger(R.styleable.test_text, -1);
        Log.e(TAG, "text = " + text + " , textAttr = " + textAttr);
        ta.recycle();
    }
}
```

- 布局文件中使用

```
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:app="http://schemas.android.com/apk/res/com.example.test"
    android:layout_width="match_parent"
    android:layout_height="match_parent" >

    <com.example.test.MyTextView
        android:layout_width="100dp"
        android:layout_height="200dp"
        app:testAttr="520"
        app:text="helloworld" />

</RelativeLayout>
```

## 属性值的类型format

(1). reference：参考某一资源ID

- 属性定义：

```
<declare-styleable name = "名称">
     <attr name = "background" format = "reference" />
</declare-styleable>
```

- 属性使用：

```
<ImageView android:background = "@drawable/图片ID"/>
```

(2). color：颜色值

- 属性定义：

```
<attr name = "textColor" format = "color" />
```

- 属性使用：

```
<TextView android:textColor = "#00FF00" />
```

(3). boolean：布尔值

- 属性定义：

```
<attr name = "focusable" format = "boolean" />
```

- 属性使用：

```
<Button android:focusable = "true"/>
```

(4). dimension：尺寸值

- 属性定义：

```
<attr name = "layout_width" format = "dimension" />
```

- 属性使用：

```
<Button android:layout_width = "42dip"/>
```

(5). float：浮点值

- 属性定义：

```
<attr name = "fromAlpha" format = "float" />
```

- 属性使用：

```
<alpha android:fromAlpha = "1.0"/>
```

(6). integer：整型值

- 属性定义：

```
<attr name = "framesCount" format="integer" />
```

- 属性使用：

```
<animated-rotate android:framesCount = "12"/>
```

(7). string：字符串

- 属性定义：

```
<attr name = "text" format = "string" />
```

- 属性使用：

```
<TextView android:text = "我是文本"/>
```

(8). fraction：百分数

- 属性定义：

```
<attr name = "pivotX" format = "fraction" />
```

- 属性使用：

```
<rotate android:pivotX = "200%"/>
```

(9). enum：枚举值

- 属性定义：

```
<declare-styleable name="名称">
    <attr name="orientation">
        <enum name="horizontal" value="0" />
        <enum name="vertical" value="1" />
    </attr>
</declare-styleable>
```

- 属性使用：

```
<LinearLayout  
    android:orientation = "vertical">
</LinearLayout>
```

注意：枚举类型的属性在使用的过程中只能同时使用其中一个，不能 android:orientation = “horizontal｜vertical"

(10). flag：位或运算

- 属性定义：

```
<declare-styleable name="名称">
    <attr name="gravity">
            <flag name="top" value="0x01" />
            <flag name="bottom" value="0x02" />
            <flag name="left" value="0x04" />
            <flag name="right" value="0x08" />
            <flag name="center_vertical" value="0x16" />
            ...
    </attr>
</declare-styleable>
```

- 属性使用：

```
<TextView android:gravity="bottom|left"/>
```

注意：位运算类型的属性在使用的过程中可以使用多个值

(11). 混合类型：属性定义时可以指定多种类型值

- 属性定义：

```
<declare-styleable name = "名称">
     <attr name = "background" format = "reference|color" />
</declare-styleable>
```

- 属性使用：

```
<ImageView
android:background = "@drawable/图片ID" />
或者：
<ImageView
android:background = "#00FF00" />
```

# 2. View绘制流程

> 这一章节偏向于解释View绘制的源码实现，可以更好地帮助我们掌握整个绘制过程。

View的绘制基本由measure()、layout()、draw()这个三个函数完成

| 函数      | 作用                         | 相关方法                                     |
| --------- | ---------------------------- | -------------------------------------------- |
| measure() | 测量View的宽高               | measure(),setMeasuredDimension(),onMeasure() |
| layout()  | 计算当前View以及子View的位置 | layout(),onLayout(),setFrame()               |
| draw()    | 视图的绘制工作               | draw(),onDraw()                              |

## 2.1 Measure()

### MeasureSpec

`MeasureSpec`是View的内部类，它封装了一个View的尺寸，在`onMeasure()`当中会根据这个`MeasureSpec`的值来确定View的宽高。

`MeasureSpec`的值保存在一个int值当中。一个int值有32位，前两位表示`模式mode`后30位表示`大小size`。即`MeasureSpec` = `mode` + `size`。

在`MeasureSpec`当中一共存在三种`mode`：`UNSPECIFIED`、`EXACTLY` 和
`AT_MOST`。

对于View来说，`MeasureSpec`的mode和Size有如下意义

| 模式        | 意义                                                         | 对应             |
| ----------- | ------------------------------------------------------------ | ---------------- |
| EXACTLY     | 精准模式，View需要一个精确值，这个值即为MeasureSpec当中的Size | match_parent     |
| AT_MOST     | 最大模式，View的尺寸有一个最大值，View不可以超过MeasureSpec当中的Size值 | wrap_content     |
| UNSPECIFIED | 无限制，View对尺寸没有任何限制，View设置为多大就应当为多大   | 一般系统内部使用 |

> 使用方式

```
    // 获取测量模式（Mode）
    int specMode = MeasureSpec.getMode(measureSpec)

    // 获取测量大小（Size）
    int specSize = MeasureSpec.getSize(measureSpec)

    // 通过Mode 和 Size 生成新的SpecMode
    int measureSpec=MeasureSpec.makeMeasureSpec(size, mode);
```

在View当中，`MeasureSpace`的测量代码如下：

```
public static int getChildMeasureSpec(int spec, int padding, int childDimension) {
        int specMode = MeasureSpec.getMode(spec);
        int specSize = MeasureSpec.getSize(spec);

        int size = Math.max(0, specSize - padding);

        int resultSize = 0;
        int resultMode = 0;

        switch (specMode) {
        //当父View要求一个精确值时，为子View赋值
        case MeasureSpec.EXACTLY:
            //如果子view有自己的尺寸，则使用自己的尺寸
            if (childDimension >= 0) {
                resultSize = childDimension;
                resultMode = MeasureSpec.EXACTLY;
                //当子View是match_parent,将父View的大小赋值给子View
            } else if (childDimension == LayoutParams.MATCH_PARENT) {
                resultSize = size;
                resultMode = MeasureSpec.EXACTLY;
                //如果子View是wrap_content，设置子View的最大尺寸为父View
            } else if (childDimension == LayoutParams.WRAP_CONTENT) {
                resultSize = size;
                resultMode = MeasureSpec.AT_MOST;
            }
            break;

        // 父布局给子View了一个最大界限
        case MeasureSpec.AT_MOST:
            if (childDimension >= 0) {
                //如果子view有自己的尺寸，则使用自己的尺寸
                resultSize = childDimension;
                resultMode = MeasureSpec.EXACTLY;
            } else if (childDimension == LayoutParams.MATCH_PARENT) {
                // 父View的尺寸为子View的最大尺寸
                resultSize = size;
                resultMode = MeasureSpec.AT_MOST;
            } else if (childDimension == LayoutParams.WRAP_CONTENT) {
                //父View的尺寸为子View的最大尺寸
                resultSize = size;
                resultMode = MeasureSpec.AT_MOST;
            }
            break;

        // 父布局对子View没有做任何限制
        case MeasureSpec.UNSPECIFIED:
            if (childDimension >= 0) {
            //如果子view有自己的尺寸，则使用自己的尺寸
                resultSize = childDimension;
                resultMode = MeasureSpec.EXACTLY;
            } else if (childDimension == LayoutParams.MATCH_PARENT) {
                //因父布局没有对子View做出限制，当子View为MATCH_PARENT时则大小为0
                resultSize = View.sUseZeroUnspecifiedMeasureSpec ? 0 : size;
                resultMode = MeasureSpec.UNSPECIFIED;
            } else if (childDimension == LayoutParams.WRAP_CONTENT) {
                //因父布局没有对子View做出限制，当子View为WRAP_CONTENT时则大小为0
                resultSize = View.sUseZeroUnspecifiedMeasureSpec ? 0 : size;
                resultMode = MeasureSpec.UNSPECIFIED;
            }
            break;
        }
    
        return MeasureSpec.makeMeasureSpec(resultSize, resultMode);
    }
```

> 这里需要注意，这段代码只是在为子View设置`MeasureSpec`参数而不是实际的设置子View的大小。子View的最终大小需要在View中具体设置。

从源码可以看出来，子View的测量模式是由自身LayoutParam和父View的MeasureSpec来决定的。

| 父View mode | 子View                                                       |
| ----------- | ------------------------------------------------------------ |
| UNSPECIFIED | 父布局没有做出限制，子View有自己的尺寸，则使用，如果没有则为0 |
| EXACTLY     | 父布局采用精准模式，有确切的大小，如果有大小则直接使用，如果子View没有大小，子View不得超出父view的大小范围 |
| AT_MOST     | 父布局采用最大模式，存在确切的大小，如果有大小则直接使用，如果子View没有大小，子View不得超出父view的大小范围 |

在测量子View大小时：

| 父View mode | 子View                                                       |
| ----------- | ------------------------------------------------------------ |
| UNSPECIFIED | 父布局没有做出限制，子View有自己的尺寸，则使用，如果没有则为0 |
| EXACTLY     | 父布局采用精准模式，有确切的大小，如果有大小则直接使用，如果子View没有大小，子View不得超出父view的大小范围 |
| AT_MOST     | 父布局采用最大模式，存在确切的大小，如果有大小则直接使用，如果子View没有大小，子View不得超出父view的大小范围 |

### onMeasure()

整个测量过程的入口位于`View`的`measure`方法当中，该方法做了一些参数的初始化之后调用了`onMeasure`方法，这里我们主要分析`onMeasure`。

`onMeasure`方法的源码如下：

```
protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {

        setMeasuredDimension(getDefaultSize(getSuggestedMinimumWidth(), widthMeasureSpec),
                getDefaultSize(getSuggestedMinimumHeight(), heightMeasureSpec));
    }
```

很简单这里只有一行代码，涉及到了三个方法我们挨个分析。

- **setMeasuredDimension(int measuredWidth, int measuredHeight)** ：该方法用来设置View的宽高，在我们自定义View时也会经常用到。
- **getDefaultSize(int size, int measureSpec)**：该方法用来获取View默认的宽高，结合源码来看。

```
/**
*   有两个参数size和measureSpec
*   1、size表示View的默认大小，它的值是通过`getSuggestedMinimumWidth()方法来获取的，之后我们再分析。
*   2、measureSpec则是我们之前分析的MeasureSpec，里面存储了View的测量值以及测量模式
*/
public static int getDefaultSize(int size, int measureSpec) {
        int result = size;
        int specMode = MeasureSpec.getMode(measureSpec);
        int specSize = MeasureSpec.getSize(measureSpec);

        //从这里我们看出，对于AT_MOST和EXACTLY在View当中的处理是完全相同的。所以在我们自定义View时要对这两种模式做出处理。
        switch (specMode) {
        case MeasureSpec.UNSPECIFIED:
            result = size;
            break;
        case MeasureSpec.AT_MOST:
        case MeasureSpec.EXACTLY:
            result = specSize;
            break;
        }
        return result;
    }
```

- **getSuggestedMinimumWidth()**：getHeight和该方法原理是一样的，这里只分析这一个。

```
//当View没有设置背景时，默认大小就是mMinWidth，这个值对应Android:minWidth属性，如果没有设置时默认为0.
//如果有设置背景，则默认大小为mMinWidth和mBackground.getMinimumWidth()当中的较大值。
protected int getSuggestedMinimumWidth() {
        return (mBackground == null) ? mMinWidth : max(mMinWidth, mBackground.getMinimumWidth());
    }
```

------

`ViewGroup`的测量过程与View有一点点区别，其本身是继承自`View`，它没有对`View`的`measure`方法以及`onMeasure`方法进行重写。

为什么没有重写`onMeasure`呢？ViewGroup除了要测量自身宽高外还需要测量各个子`View`的大小，而不同的布局测量方式也都不同（可参考`LinearLayout`以及`FrameLayout`），所以没有办法统一设置。因此它提供了测量子`View`的方法`measureChildren()`以及`measureChild()`帮助我们对子View进行测量。

`measureChildren()`以及`measureChild()`的源码这里不再分析，大致流程就是遍历所有的子View，然后调用`View`的`measure()`方法，让子`View`测量自身大小。具体测量流程上面也以及介绍过了

------

`measure`过程会因为布局的不同或者需求的不同而呈现不同的形式，使用时还是要根据业务场景来具体分析，如果想再深入研究可以看一下`LinearLayout`的`onMeasure`方法。

## 2.2 Layout()

> 要计算位置首先要对Android坐标系有所了解，前面的内容我们也有介绍过。

`layout()`过程，对于`View`来说用来计算`View`的位置参数,对于`ViewGroup`来说，除了要测量自身位置，还需要测量子`View`的位置。

`layout()`方法是整个Layout()流程的入口，看一下这部分源码

```
/**
*  这里的四个参数l、t、r、b分别代表View的左、上、右、下四个边界相对于其父View的距离。
*
*/
public void layout(int l, int t, int r, int b) {
        if ((mPrivateFlags3 & PFLAG3_MEASURE_NEEDED_BEFORE_LAYOUT) != 0) {
            onMeasure(mOldWidthMeasureSpec, mOldHeightMeasureSpec);
            mPrivateFlags3 &= ~PFLAG3_MEASURE_NEEDED_BEFORE_LAYOUT;
        }

        int oldL = mLeft;
        int oldT = mTop;
        int oldB = mBottom;
        int oldR = mRight;

        //这里通过setFrame或setOpticalFrame方法确定View在父容器当中的位置。
        boolean changed = isLayoutModeOptical(mParent) ?
                setOpticalFrame(l, t, r, b) : setFrame(l, t, r, b);

        //调用onLayout方法。onLayout方法是一个空实现，不同的布局会有不同的实现。
        if (changed || (mPrivateFlags & PFLAG_LAYOUT_REQUIRED) == PFLAG_LAYOUT_REQUIRED) {
            onLayout(changed, l, t, r, b);

        }

    }
```

从源码我们知道，在`layout()`方法中已经通过`setOpticalFrame(l, t, r, b)`或 `setFrame(l, t, r, b)`方法对View自身的位置进行了设置，所以`onLayout(changed, l, t, r, b)`方法主要是`ViewGroup`对子View的位置进行计算。

> 有兴趣的可以看一下`LinearLayout`的`onLayout`源码，可以帮助加深理解。

## 2.3 Draw()

draw流程也就是的View绘制到屏幕上的过程，整个流程的入口在`View`的`draw()`方法之中，而源码注释也写的很明白，整个过程可以分为6个步骤。

1. 如果需要，绘制背景。
2. 有过有必要，保存当前canvas。
3. 绘制View的内容。
4. 绘制子View。
5. 如果有必要，绘制边缘、阴影等效果。
6. 绘制装饰，如滚动条等等。

通过各个步骤的源码再做分析：

```
    public void draw(Canvas canvas) {

       
        int saveCount;
        // 1. 如果需要，绘制背景
        if (!dirtyOpaque) {
            drawBackground(canvas);
        }

        // 2. 有过有必要，保存当前canvas。
        final int viewFlags = mViewFlags;
      
        if (!verticalEdges && !horizontalEdges) {
            // 3. 绘制View的内容。
            if (!dirtyOpaque) onDraw(canvas);

            // 4. 绘制子View。
            dispatchDraw(canvas);

            drawAutofilledHighlight(canvas);

            // Overlay is part of the content and draws beneath Foreground
            if (mOverlay != null && !mOverlay.isEmpty()) {
                mOverlay.getOverlayView().dispatchDraw(canvas);
            }

            // 6. 绘制装饰，如滚动条等等。
            onDrawForeground(canvas);

            // we're done...
            return;
        }
    }
    
    /**
    *  1.绘制View背景
    */
    private void drawBackground(Canvas canvas) {
        //获取背景
        final Drawable background = mBackground;
        if (background == null) {
            return;
        }

        setBackgroundBounds();

        //获取便宜值scrollX和scrollY，如果scrollX和scrollY都不等于0，则会在平移后的canvas上面绘制背景。
        final int scrollX = mScrollX;
        final int scrollY = mScrollY;
        if ((scrollX | scrollY) == 0) {
            background.draw(canvas);
        } else {
            canvas.translate(scrollX, scrollY);
            background.draw(canvas);
            canvas.translate(-scrollX, -scrollY);
        }
    }
    
    /**
    * 3.绘制View的内容,该方法是一个空的实现，在各个业务当中自行处理。
    */
    protected void onDraw(Canvas canvas) {
    }
    
    /**
    * 4. 绘制子View。该方法在View当中是一个空的实现，在各个业务当中自行处理。
    *  在ViewGroup当中对dispatchDraw方法做了实现，主要是遍历子View，并调用子类的draw方法，一般我们不需要自己重写该方法。
    */
    protected void dispatchDraw(Canvas canvas) {

    }
        
```

# 3. 自定义组合控件

自定义组合控件就是将多个控件组合成为一个新的控件，主要解决多次重复使用同一类型的布局。如我们顶部的HeaderView以及dailog等，我们都可以把他们组合成一个新的控件。

我们通过一个自定义HeaderView实例来了解自定义组合控件的用法。

**1. 编写布局文件**

```
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:id="@+id/header_root_layout"
    android:layout_height="45dp"
    android:background="#827192">

    <ImageView
        android:id="@+id/header_left_img"
        android:layout_width="45dp"
        android:layout_height="45dp"
        android:layout_alignParentLeft="true"
        android:paddingLeft="12dp"
        android:paddingRight="12dp"
        android:src="@drawable/back"
        android:scaleType="fitCenter"/>

    <TextView
        android:id="@+id/header_center_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerInParent="true"
        android:lines="1"
        android:maxLines="11"
        android:ellipsize="end"
        android:text="title"
        android:textStyle="bold"
        android:textColor="#ffffff"/>
    
    <ImageView
        android:id="@+id/header_right_img"
        android:layout_width="45dp"
        android:layout_height="45dp"
        android:layout_alignParentRight="true"
        android:src="@drawable/add"
        android:scaleType="fitCenter"
        android:paddingRight="12dp"
        android:paddingLeft="12dp"/>

</RelativeLayout>
```

布局很简单，中间是title的文字，左边是返回按钮，右边是一个添加按钮。

**2. 实现构造方法**

```
//因为我们的布局采用RelativeLayout，所以这里继承RelativeLayout。
//关于各个构造方法的介绍可以参考前面的内容
public class YFHeaderView extends RelativeLayout {

    public YFHeaderView(Context context) {
        super(context);
    }

    public YFHeaderView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public YFHeaderView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

}
```

**3. 初始化UI**

```
    //初始化UI，可根据业务需求设置默认值。
    private void initView(Context context) {
        LayoutInflater.from(context).inflate(R.layout.view_header, this, true);
        img_left = (ImageView) findViewById(R.id.header_left_img);
        img_right = (ImageView) findViewById(R.id.header_right_img);
        text_center = (TextView) findViewById(R.id.header_center_text);
        layout_root = (RelativeLayout) findViewById(R.id.header_root_layout);
        layout_root.setBackgroundColor(Color.BLACK);
        text_center.setTextColor(Color.WHITE);

    }
    
```

**4. 提供对外的方法**

可以根据业务需求对外暴露一些方法。

```
    //设置标题文字的方法
    private void setTitle(String title) {
        if (!TextUtils.isEmpty(title)) {
            text_center.setText(title);
        }
    }
    //对左边按钮设置事件的方法
    private void setLeftListener(OnClickListener onClickListener) {
        img_left.setOnClickListener(onClickListener);
    }

    //对右边按钮设置事件的方法
    private void setRightListener(OnClickListener onClickListener) {
        img_right.setOnClickListener(onClickListener);
    }
```

**5. 在布局当中引用该控件**

```
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <com.example.yf.view.YFHeaderView
        android:layout_width="match_parent"
        android:layout_height="45dp">

    </com.example.yf.view.YFHeaderView>

</LinearLayout>
```

到这里基本的功能已经有了。除了这些基础功能外，我们还可以做一些功能扩展，比如可以在布局时设置我的View显示的元素，因为可能有些需求并不需要右边的按钮。这时候就需要用到自定义属性来解决了。

前面已经简单介绍过自定义属性的相关知识，我们之间看代码

**1.首先在values目录下创建attrs.xml**

内容如下：

```
<resources>

    <declare-styleable name="HeaderBar">
        <attr name="title_text_clolor" format="color"></attr>
        <attr name="title_text" format="string"></attr>
        <attr name="show_views">
            <flag name="left_text" value="0x01" />
            <flag name="left_img" value="0x02" />
            <flag name="right_text" value="0x04" />
            <flag name="right_img" value="0x08" />
            <flag name="center_text" value="0x10" />
            <flag name="center_img" value="0x20" />
        </attr>
    </declare-styleable>
</resources>
```

这里我们定义了三个属性，文字内容、颜色以及要显示的元素。

**2.在java代码中进行设置**

```
    private void initAttrs(Context context, AttributeSet attrs) {
        TypedArray mTypedArray = context.obtainStyledAttributes(attrs, R.styleable.HeaderBar);
        //获取title_text属性
        String title = mTypedArray.getString(R.styleable.HeaderBar_title_text);
        if (!TextUtils.isEmpty(title)) {
            text_center.setText(title);
        }
        //获取show_views属性，如果没有设置时默认为0x26
        showView = mTypedArray.getInt(R.styleable.HeaderBar_show_views, 0x26);
        text_center.setTextColor(mTypedArray.getColor(R.styleable.HeaderBar_title_text_clolor, Color.WHITE));
        mTypedArray.recycle();
        showView(showView);

    }
    
    private void showView(int showView) {
        //将showView转换为二进制数，根据不同位置上的值设置对应View的显示或者隐藏。
        Long data = Long.valueOf(Integer.toBinaryString(showView));
        element = String.format("%06d", data);
        for (int i = 0; i < element.length(); i++) {
            if(i == 0) ;
            if(i == 1) text_center.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 2) img_right.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 3) ;
            if(i == 4) img_left.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 5) ;
        }

    }
```

**3.在布局文件中进行设置**

```
    <com.example.yf.view.YFHeaderView
        android:layout_width="match_parent"
        android:layout_height="45dp"
        app:title_text="标题"
        app:show_views="center_text|left_img|right_img">

    </com.example.yf.view.YFHeaderView>
```

OK，到这里整个View基本定义完成。整个YFHeaderView的代码如下

```
public class YFHeaderView extends RelativeLayout {

    private ImageView img_left;
    private TextView text_center;
    private ImageView img_right;
    private RelativeLayout layout_root;
    private Context context;
    String element;

    private int showView;

    public YFHeaderView(Context context) {
        super(context);
        this.context = context;
        initView(context);
    }

    public YFHeaderView(Context context, AttributeSet attrs) {
        super(context, attrs);
        this.context = context;
        initView(context);
        initAttrs(context, attrs);
    }

    public YFHeaderView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        this.context = context;
        initView(context);
        initAttrs(context, attrs);
    }

    private void initAttrs(Context context, AttributeSet attrs) {
        TypedArray mTypedArray = context.obtainStyledAttributes(attrs, R.styleable.HeaderBar);
        String title = mTypedArray.getString(R.styleable.HeaderBar_title_text);
        if (!TextUtils.isEmpty(title)) {
            text_center.setText(title);
        }
        showView = mTypedArray.getInt(R.styleable.HeaderBar_show_views, 0x26);
        text_center.setTextColor(mTypedArray.getColor(R.styleable.HeaderBar_title_text_clolor, Color.WHITE));
        mTypedArray.recycle();
        showView(showView);

    }

    private void showView(int showView) {
        Long data = Long.valueOf(Integer.toBinaryString(showView));
        element = String.format("%06d", data);
        for (int i = 0; i < element.length(); i++) {
            if(i == 0) ;
            if(i == 1) text_center.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 2) img_right.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 3) ;
            if(i == 4) img_left.setVisibility(element.substring(i,i+1).equals("1")? View.VISIBLE:View.GONE);
            if(i == 5) ;
        }

    }

    private void initView(final Context context) {
        LayoutInflater.from(context).inflate(R.layout.view_header, this, true);
        img_left = (ImageView) findViewById(R.id.header_left_img);
        img_right = (ImageView) findViewById(R.id.header_right_img);
        text_center = (TextView) findViewById(R.id.header_center_text);
        layout_root = (RelativeLayout) findViewById(R.id.header_root_layout);
        layout_root.setBackgroundColor(Color.BLACK);
        text_center.setTextColor(Color.WHITE);

        img_left.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(context, element + "", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void setTitle(String title) {
        if (!TextUtils.isEmpty(title)) {
            text_center.setText(title);
        }
    }


    private void setLeftListener(OnClickListener onClickListener) {
        img_left.setOnClickListener(onClickListener);
    }

    private void setRightListener(OnClickListener onClickListener) {
        img_right.setOnClickListener(onClickListener);
    }

}
```

# 4. 继承系统控件

继承系统的控件可以分为继承View子类（如TextVIew等）和继承ViewGroup子类(如LinearLayout等)，根据业务需求的不同，实现的方式也会有比较大的差异。这里介绍一个比较简单的，继承自View的实现方式。

业务需求：为文字设置背景，并在布局中间添加一条横线。

因为这种实现方式会复用系统的逻辑，大多数情况下我们希望复用系统的`onMeaseur`和`onLayout`流程，所以我们只需要重写`onDraw`方法 。实现非常简单，话不多说，直接上代码。

```
public class LineTextView extends TextView {

    //定义画笔，用来绘制中心曲线
    private Paint mPaint;
    
    /**
     * 创建构造方法
     * @param context
     */
    public LineTextView(Context context) {
        super(context);
        init();
    }

    public LineTextView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public LineTextView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        mPaint = new Paint();
        mPaint.setColor(Color.BLACK);
    }

    //重写draw方法，绘制我们需要的中间线以及背景
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        int width = getWidth();
        int height = getHeight();
        mPaint.setColor(Color.BLUE);
        //绘制方形背景
        RectF rectF = new RectF(0,0,width,height);
        canvas.drawRect(rectF,mPaint);
        mPaint.setColor(Color.BLACK);
        //绘制中心曲线，起点坐标（0,height/2），终点坐标（width,height/2）
        canvas.drawLine(0,height/2,width,height/2,mPaint);
    }
}
```

> 对于View的绘制还需要对`Paint()`、`canvas`以及`Path`的使用有所了解，不清楚的可以稍微了解一下。

这里的实现比较简单，因为具体实现会与业务环境密切相关，这里只是做一个参考。

# 5. 直接继承View

直接继承View会比上一种实现方复杂一些，这种方法的使用情景下，完全不需要复用系统控件的逻辑，除了要重写`onDraw`外还需要对`onMeasure`方法进行重写。

我们用自定义View来绘制一个正方形。

- **首先定义构造方法，以及做一些初始化操作**

```
ublic class RectView extends View{
    //定义画笔
    private Paint mPaint = new Paint();

    /**
     * 实现构造方法
     * @param context
     */
    public RectView(Context context) {
        super(context);
        init();
    }

    public RectView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public RectView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        mPaint.setColor(Color.BLUE);

    }

}
```

- **重写draw方法，绘制正方形，注意对padding属性进行设置**

```
/**
     * 重写draw方法
     * @param canvas
     */
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        //获取各个编剧的padding值
        int paddingLeft = getPaddingLeft();
        int paddingRight = getPaddingRight();
        int paddingTop = getPaddingTop();
        int paddingBottom = getPaddingBottom();
        //获取绘制的View的宽度
        int width = getWidth()-paddingLeft-paddingRight;
        //获取绘制的View的高度
        int height = getHeight()-paddingTop-paddingBottom;
        //绘制View，左上角坐标（0+paddingLeft,0+paddingTop），右下角坐标（width+paddingLeft,height+paddingTop）
        canvas.drawRect(0+paddingLeft,0+paddingTop,width+paddingLeft,height+paddingTop,mPaint);
    }
```

之前我们讲到过View的`measure`过程，再看一下源码对这一步的处理

```
    public static int getDefaultSize(int size, int measureSpec) {
        int result = size;
        int specMode = MeasureSpec.getMode(measureSpec);
        int specSize = MeasureSpec.getSize(measureSpec);

        switch (specMode) {
        case MeasureSpec.UNSPECIFIED:
            result = size;
            break;
        case MeasureSpec.AT_MOST:
        case MeasureSpec.EXACTLY:
            result = specSize;
            break;
        }
        return result;
    }
```

在View的源码当中并没有对`AT_MOST`和`EXACTLY`两个模式做出区分，也就是说View在`wrap_content`和`match_parent`两个模式下是完全相同的，都会是`match_parent`，显然这与我们平时用的View不同，所以我们要重写`onMeasure`方法。

- **重写onMeasure方法**

```
    /**
     * 重写onMeasure方法
     *
     * @param widthMeasureSpec
     * @param heightMeasureSpec
     */
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        int widthSize = MeasureSpec.getSize(widthMeasureSpec);
        int widthMode = MeasureSpec.getMode(widthMeasureSpec);
        int heightSize = MeasureSpec.getSize(heightMeasureSpec);
        int heightMode = MeasureSpec.getMode(heightMeasureSpec);

        //处理wrap_contentde情况
        if (widthMode == MeasureSpec.AT_MOST && heightMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(300, 300);
        } else if (widthMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(300, heightSize);
        } else if (heightMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(widthSize, 300);
        }
    }
```

整个自定义View的代码如下:

```
public class RectView extends View {
    //定义画笔
    private Paint mPaint = new Paint();

    /**
     * 实现构造方法
     *
     * @param context
     */
    public RectView(Context context) {
        super(context);
        init();
    }

    public RectView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public RectView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        mPaint.setColor(Color.BLUE);

    }

    /**
     * 重写onMeasure方法
     *
     * @param widthMeasureSpec
     * @param heightMeasureSpec
     */
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        int widthSize = MeasureSpec.getSize(widthMeasureSpec);
        int widthMode = MeasureSpec.getMode(widthMeasureSpec);
        int heightSize = MeasureSpec.getSize(heightMeasureSpec);
        int heightMode = MeasureSpec.getMode(heightMeasureSpec);

        if (widthMode == MeasureSpec.AT_MOST && heightMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(300, 300);
        } else if (widthMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(300, heightSize);
        } else if (heightMode == MeasureSpec.AT_MOST) {
            setMeasuredDimension(widthSize, 300);
        }
    }

    /**
     * 重写draw方法
     *
     * @param canvas
     */
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        //获取各个编剧的padding值
        int paddingLeft = getPaddingLeft();
        int paddingRight = getPaddingRight();
        int paddingTop = getPaddingTop();
        int paddingBottom = getPaddingBottom();
        //获取绘制的View的宽度
        int width = getWidth() - paddingLeft - paddingRight;
        //获取绘制的View的高度
        int height = getHeight() - paddingTop - paddingBottom;
        //绘制View，左上角坐标（0+paddingLeft,0+paddingTop），右下角坐标（width+paddingLeft,height+paddingTop）
        canvas.drawRect(0 + paddingLeft, 0 + paddingTop, width + paddingLeft, height + paddingTop, mPaint);
    }
}
```

整个过程大致如下，直接继承View时需要有几点注意：

> 1、在onDraw当中对padding属性进行处理。
> 2、在onMeasure过程中对wrap_content属性进行处理。
> 3、至少要有一个构造方法。

# 6. 继承ViewGroup

自定义ViewGroup的过程相对复杂一些，因为除了要对自身的大小和位置进行测量之外，还需要对子View的测量参数负责。

## 需求实例

实现一个类似于Viewpager的可左右滑动的布局。

代码比较多，我们结合注释分析。

```
public class HorizontaiView extends ViewGroup {

    private int lastX;
    private int lastY;

    private int currentIndex = 0;
    private int childWidth = 0;
    private Scroller scroller;
    private VelocityTracker tracker;

    
    /**
     * 1.创建View类，实现构造函数
     * 实现构造方法
     * @param context
     */
    public HorizontaiView(Context context) {
        super(context);
        init(context);
    }

    public HorizontaiView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(context);
    }

    public HorizontaiView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init(context);
    }

    private void init(Context context) {
        scroller = new Scroller(context);
        tracker = VelocityTracker.obtain();
    }

    /**
     * 2、根据自定义View的绘制流程，重写`onMeasure`方法，注意对wrap_content的处理
     * 重写onMeasure方法
     * @param widthMeasureSpec
     * @param heightMeasureSpec
     */
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        //获取宽高的测量模式以及测量值
        int widthMode = MeasureSpec.getMode(widthMeasureSpec);
        int widthSize = MeasureSpec.getSize(widthMeasureSpec);
        int heightMode = MeasureSpec.getMode(heightMeasureSpec);
        int heightSize = MeasureSpec.getSize(heightMeasureSpec);
        //测量所有子View
        measureChildren(widthMeasureSpec, heightMeasureSpec);
        //如果没有子View，则View大小为0，0
        if (getChildCount() == 0) {
            setMeasuredDimension(0, 0);
        } else if (widthMode == MeasureSpec.AT_MOST && heightMode == MeasureSpec.AT_MOST) {
            View childOne = getChildAt(0);
            int childWidth = childOne.getMeasuredWidth();
            int childHeight = childOne.getMeasuredHeight();
            //View的宽度=单个子View宽度*子View个数，View的高度=子View高度
            setMeasuredDimension(getChildCount() * childWidth, childHeight);
        } else if (widthMode == MeasureSpec.AT_MOST) {
            View childOne = getChildAt(0);
            int childWidth = childOne.getMeasuredWidth();
            //View的宽度=单个子View宽度*子View个数，View的高度=xml当中设置的高度
            setMeasuredDimension(getChildCount() * childWidth, heightSize);
        } else if (heightMode == MeasureSpec.AT_MOST) {
            View childOne = getChildAt(0);
            int childHeight = childOne.getMeasuredHeight();
            //View的宽度=xml当中设置的宽度，View的高度=子View高度
            setMeasuredDimension(widthSize, childHeight);
        }
    }

    /**
     * 3、接下来重写`onLayout`方法，对各个子View设置位置。
     * 设置子View位置
     * @param changed
     * @param l
     * @param t
     * @param r
     * @param b
     */
    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        int childCount = getChildCount();
        int left = 0;
        View child;
        for (int i = 0; i < childCount; i++) {
            child = getChildAt(i);
            if (child.getVisibility() != View.GONE) {
                childWidth = child.getMeasuredWidth();
                child.layout(left, 0, left + childWidth, child.getMeasuredHeight());
                left += childWidth;
            }
        }
    }
}
```

到这里我们的View布局就已经基本结束了。但是要实现`Viewpager`的效果，还需要添加对事件的处理。事件的处理流程之前我们有分析过，在制作自定义View的时候也是会经常用到的，不了解的可以参考之前的文章[Android Touch事件分发超详细解析](https://www.jianshu.com/p/bc4c9e5f4b1c)。

```
    /**
     * 4、因为我们定义的是ViewGroup，从onInterceptTouchEvent开始。
     * 重写onInterceptTouchEvent,对横向滑动事件进行拦截
     * @param event
     * @return
     */
    @Override
    public boolean onInterceptTouchEvent(MotionEvent event) {
        boolean intercrpt = false;
        //记录当前点击的坐标
        int x = (int) event.getX();
        int y = (int) event.getY();
        switch (event.getAction()) {
            case MotionEvent.ACTION_MOVE:
                int deltaX = x - lastX;
                int delatY = y - lastY;
                //当X轴移动的绝对值大于Y轴移动的绝对值时，表示用户进行了横向滑动，对事件进行拦截
                if (Math.abs(deltaX) > Math.abs(delatY)) {
                    intercrpt = true;
                }
                break;
        }
        lastX = x;
        lastY = y;
        //intercrpt = true表示对事件进行拦截
        return intercrpt;
    }
    
    /**
     * 5、当ViewGroup拦截下用户的横向滑动事件以后，后续的Touch事件将交付给`onTouchEvent`进行处理。
     * 重写onTouchEvent方法
     * @param event
     * @return
     */
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        tracker.addMovement(event);
        //获取事件坐标(x,y)
        int x = (int) event.getX();
        int y = (int) event.getY();
        switch (event.getAction()) {
            case MotionEvent.ACTION_MOVE:
                int deltaX = x - lastX;
                int delatY = y - lastY;
                //scrollBy方法将对我们当前View的位置进行偏移
                scrollBy(-deltaX, 0);
                break;
            //当产生ACTION_UP事件时，也就是我们抬起手指
            case MotionEvent.ACTION_UP:
                //getScrollX()为在X轴方向发生的便宜，childWidth * currentIndex表示当前View在滑动开始之前的X坐标
                //distance存储的就是此次滑动的距离
                int distance = getScrollX() - childWidth * currentIndex;
                //当本次滑动距离>View宽度的1/2时，切换View
                if (Math.abs(distance) > childWidth / 2) {
                    if (distance > 0) {
                        currentIndex++;
                    } else {
                        currentIndex--;
                    }
                } else {
                    //获取X轴加速度，units为单位，默认为像素，这里为每秒1000个像素点
                    tracker.computeCurrentVelocity(1000);
                    float xV = tracker.getXVelocity();
                    //当X轴加速度>50时，也就是产生了快速滑动，也会切换View
                    if (Math.abs(xV) > 50) {
                        if (xV < 0) {
                            currentIndex++;
                        } else {
                            currentIndex--;
                        }
                    }
                }
                //对currentIndex做出限制其范围为【0，getChildCount() - 1】
                currentIndex = currentIndex < 0 ? 0 : currentIndex > getChildCount() - 1 ? getChildCount() - 1 : currentIndex;
                //滑动到下一个View
                smoothScrollTo(currentIndex * childWidth, 0);
                tracker.clear();
                break;
        }
        lastX = x;
        lastY = y;
        return true;
    }


    private void smoothScrollTo(int destX, int destY) {
        //startScroll方法将产生一系列偏移量，从（getScrollX(), getScrollY()），destX - getScrollX()和destY - getScrollY()为移动的距离
        scroller.startScroll(getScrollX(), getScrollY(), destX - getScrollX(), destY - getScrollY(), 1000);
        //invalidate方法会重绘View，也就是调用View的onDraw方法，而onDraw又会调用computeScroll()方法
        invalidate();
    }

    //重写computeScroll方法
    @Override
    public void computeScroll() {
        super.computeScroll();
        //当scroller.computeScrollOffset()=true时表示滑动没有结束
        if (scroller.computeScrollOffset()) {
            //调用scrollTo方法进行滑动，滑动到scroller当中计算到的滑动位置
            scrollTo(scroller.getCurrX(), scroller.getCurrY());
            //没有滑动结束，继续刷新View
            postInvalidate();
        }
    }
```

这部分代码比较多，为了方便阅读，在代码当中进行了注释。
之后就是在XML代码当中引入自定义View

```
<com.example.yf.view.HorizontaiView
        android:id="@+id/test_layout"
        android:layout_width="match_parent"
        android:layout_height="400dp">
        <ListView
            android:id="@+id/list1"
            android:layout_width="match_parent"
            android:layout_height="match_parent">

        </ListView>

        <ListView
            android:id="@+id/list2"
            android:layout_width="match_parent"
            android:layout_height="match_parent">

        </ListView>

        <ListView
            android:id="@+id/list3"
            android:layout_width="match_parent"
            android:layout_height="match_parent">

        </ListView>

    </com.example.yf.view.HorizontaiView>
```

好了，可以运行看一下效果了。

# 总结

本篇文章对常用的自定义View的方式进行了总结，并简单分析了View的绘制流程。对各种实现方式写了简单的实现。

[原文](https://www.jianshu.com/p/705a6cb6bfee)

