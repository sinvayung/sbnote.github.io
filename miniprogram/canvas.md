### 1. 微信小程序API 绘图介绍（如何在Canvas上画图）

```xml
<canvas canvas-id="myCanvas" style="border: 1px solid;"/>
```

- `fillRect(x, y, width, height)`方法画一个矩形

```javascript
const ctx = wx.createCanvasContext('myCanvas', this)
ctx.setFillStyle('red')
ctx.fillRect(20, 10, 200, 100);  # (x, y, width, height)
ctx.draw()
```



### 2. 微信小程序API coordinates（Canvas 坐标系）

### 3. 微信小程序API gradient（如何绘制渐变效果）

- `createLinearGradient(x, y, x1, y1)`- 创建一个线性的渐变
- `createCircularGradient(x, y, r)`- 创建一个从圆心开始的渐变

```javascript
const ctx = wx.createCanvasContext('myCanvas', this)

// Create linear gradient
const grd = ctx.createLinearGradient(0, 0, 200, 0)  //(x, y, x1, y1)
grd.addColorStop(0, 'red')
grd.addColorStop(1, 'white')

// Fill with gradient
ctx.setFillStyle(grd)
ctx.fillRect(20, 10, 200, 100)
ctx.draw()
```



### 4. 微信小程序API color（绘图颜色）

- RGB 颜色：如`'rgb(255, 0, 0)'`
- RGBA 颜色：如`'rgba(255, 0, 0, 0.3)'`
- 16 进制颜色：如`'#FF0000'`
- 预定义的颜色：如`'red'`



### 5. 微信小程序API wx.createCanvasContext(canvasId)（绘图上下文）

```javascript
wx.createCanvasContext(canvasId)
```

### 6. 微信小程序API 创建并返回上下文 wx.createContext (不推荐使用)

### 7. 微信小程序API 绘图·绘制画布 drawCanvas (不推荐使用)

### 8. 微信小程序API 绘图·导出图片canvasToTempFilePath(OBJECT)

```javascript
wx.canvasToTempFilePath(OBJECT)
```

```javascript
wx.canvasToTempFilePath({
  canvasId: 'myCanvas',
  x: 50,  // 画布x轴起点（默认0）
  y: 50,  // 画布y轴起点（默认0）
  width: 200, // 画布宽度（默认为canvas宽度-x）
  height: 100,  //画布高度（默认为canvas高度-y）	
  destWidth: 200,  // 输出图片宽度（默认为width）
  height: 100,  // 输出图片高度（默认为height）
  fileType: 'png',  // 目标文件的类型，只支持 'jpg' 或 'png'。默认为 'png'
  quality: 1,  // 图片的质量，取值范围为 (0, 1]，
  success: function (res) {
    console.log(res.tempFilePath)
  },
  fail: function (res) {
    console.log('fail.')
  }
})
```

> 注意，不能与draw()方法在同一个方法体中使用，需在回调中使用，如draw(false, function(){...})或setTimeout(function(){...}, 500)



### 9. 微信小程序API 绘图·设置填充样式setFillStyle

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setFillStyle('red')
ctx.fillRect(10, 10, 150, 75)  // 涂个面积
ctx.draw()
```



### 10. 微信小程序API 绘图setStrokeStyle（设置线条样式）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setStrokeStyle('red')
ctx.strokeRect(10, 10, 150, 75)  // 画个框，内为空白
ctx.draw()
```



### 11. 微信小程序API 绘图setShadow（设置阴影样式）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setFillStyle('red')
ctx.setShadow(5, 5, 10, 'blue')  //(offsetX, offsetY, blur, color)
ctx.fillRect(20, 10, 200, 100)
ctx.draw()
```

| 参数    | 类型                                                         | 范围  | 定义                                  |
| ------- | ------------------------------------------------------------ | ----- | ------------------------------------- |
| offsetX | Number                                                       |       | 阴影相对于形状在水平方向的偏移，默认0 |
| offsetY | Number                                                       |       | 阴影相对于形状在竖直方向的偏移，默认0 |
| blur    | Number                                                       | 0~100 | 阴影的模糊级别，数值越大越模糊        |
| color   | [Color](https://www.w3cschool.cn/weixinapp/weixinapp-api-canvas-color.html) |       | 阴影的颜色，默认`black`               |



### 12. 微信小程序API 绘图createLinearGradient（创建线性渐变）

```javascript
const ctx = wx.createCanvasContext('myCanvas')

// Create linear gradient
const grd = ctx.createLinearGradient(0, 0, 200, 0)  //(x, y, x1, y1)
grd.addColorStop(0, 'red')
grd.addColorStop(1, 'white')

// Fill with gradient
ctx.setFillStyle(grd)
ctx.fillRect(10, 10, 150, 80)
ctx.draw()
```

> `addColorStop()`来指定渐变点，至少要两个



### 13. 微信小程序API 绘图createCircularGradient（创建圆形渐变）

```javascript
const ctx = wx.createCanvasContext('myCanvas')

// Create circular gradient
const grd = ctx.createCircularGradient(75, 50, 50)  // (x, y, r)
grd.addColorStop(0, 'red')
grd.addColorStop(1, 'white')

// Fill with gradient
ctx.setFillStyle(grd)
ctx.fillRect(10, 10, 150, 80)
ctx.draw()
```

> (x, y)为圆心，r为半径



### 14. 微信小程序API绘图addColorStop（创建颜色渐变点）

```javascript
const ctx = wx.crateCanvasContext('myCanvas')

// Create circular gradient
const grd = ctx.createCircularGradient(30, 10, 120, 10)
grd.addColorStop(0, 'red')
grd.addColorStop(0.16, 'orange')
grd.addColorStop(0.33, 'yellow')
grd.addColorStop(0.5, 'green')
grd.addColorStop(0.66, 'cyan')
grd.addColorStop(0.83, 'blue')
grd.addColorStop(1, 'purple')

// Fill with gradient
ctx.setFillStyle(grd)
ctx.fillRect(10, 10, 150, 80)
ctx.draw()
```

> addColorStop()`来指定渐变点，至少要两个; 
>
> 第一个参数， 表示渐变点在起点和终点中的位置， 范围[0~1]



### 15. 微信小程序API 绘图setLineWidth（设置线条宽度）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.beginPath()
ctx.setLineWidth(5)  //设置线条宽度
ctx.moveTo(50, 50)  //(x0, y0)
ctx.lineTo(200, 50)  //(x1, y1
ctx.lineTo(200, 100)  //(x2, y2))
ctx.stroke()

ctx.beginPath()
ctx.setLineWidth(10)  //设置线条宽度
ctx.moveTo(50, 50)  //(x0, y0)
ctx.lineTo(50, 100)  //(x1, y1))
ctx.stroke()
ctx.draw()
```



### 16. 微信小程序API 绘图setLineCap（设置线条端点样式）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.beginPath()
ctx.setLineWidth(20)
ctx.moveTo(50, 50)  //(x0, y0)
ctx.lineTo(200, 50)  //(x1, y1
ctx.stroke()

ctx.beginPath()
ctx.setLineCap('butt')  //设置线条端点样式
ctx.setLineWidth(20)
ctx.moveTo(50, 50)  //(x0, y0)
ctx.lineTo(50, 100)  //(x1, y1))
ctx.stroke()
ctx.draw()
```

lineCap三种取值：

- butt，顶撞？
- round， 圆形端点
- square， 方形端点



### 17. 微信小程序API 绘图setLineJoin（设置线条交点样式）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.beginPath()
ctx.setLineJoin('bevel')  //设置线条交点样式
ctx.setLineWidth(10)
ctx.moveTo(50, 10)
ctx.lineTo(140, 50)
ctx.lineTo(50, 90)
ctx.stroke()
ctx.draw()
```

LineJoin三种取值：

- bevel， 斜角？
- round，圆角
- miter，斜接 



### 18. 微信小程序API 绘图setMiterLimit（设置最大倾斜）

设置最大斜接长度，斜接长度指的是在两条线交汇处内角和外角之间的距离。 当`setLineJoin()`为 miter 时才有效。超过最大倾斜长度的，连接处将以 lineJoin 为 bevel 来显示

```javascript
ctx.setLineJoin('miter')
ctx.setMiterLimit(1)
```



### 19. 微信小程序API 绘图rect创建矩形

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.rect(10, 10, 150, 75)  // 创建矩形
ctx.setFillStyle('red')
ctx.fill()
ctx.draw()
```

> 用`fill()`或者`stroke()`方法将矩形真正的画到 canvas 中。



### 20. 微信小程序API 绘图fillRect（填充矩形）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setFillStyle('red')
ctx.fillRect(10, 10, 150, 75)  // 填充矩形
ctx.draw()
```



### 21. 微信小程序API 绘图strokeRect（画一个矩形，非填充）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setStrokeStyle('red')
ctx.strokeRect(10, 10, 150, 75)  // 画一个矩形
ctx.draw()
```



### 22. 微信小程序API 绘图clearRect（在给定的矩形区域内，清除画布上的像素）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.setFillStyle('red')
ctx.fillRect(0, 0, 150, 200)
ctx.setFillStyle('blue')
ctx.fillRect(150, 0, 150, 200)
ctx.clearRect(10, 10, 150, 75)  //(x, y, width, height)
ctx.draw()
```



### 23. 微信小程序API 绘图fill（对当前路径进行填充）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.moveTo(10, 10)
ctx.lineTo(100, 10)
ctx.lineTo(100, 100)
ctx.fill()  // 对当前路径进行填充
ctx.draw()
```

```javascript
const ctx = wx.createCanvasContext('myCanvas')
// begin path
ctx.rect(10, 10, 100, 30)
ctx.setFillStyle('yellow')
ctx.fill()

// begin another path
ctx.beginPath()
ctx.rect(10, 40, 100, 30)

// only fill this rect, not in current path
ctx.setFillStyle('blue')
ctx.fillRect(10, 70, 100, 30)

ctx.rect(10, 100, 100, 30)

// it will fill current path
ctx.setFillStyle('red')
ctx.fill() //填充，但不包含fillRect部分
ctx.draw()
```

> 如果当前路径没有闭合，`fill()`方法会将起点和终点进行连接，然后填充，详情见例一。

> `fill()`填充的的路径是从`beginPath()`开始计算，但是不会将`fillRect()`包含进去，详情见例二。



### 24. 微信小程序API 绘图stroke（对当前路径进行描边）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.moveTo(10, 10)
ctx.lineTo(100, 10)
ctx.lineTo(100, 100)
ctx.stroke()
ctx.draw()
```

```javascript
const ctx = wx.createCanvasContext('myCanvas')
// begin path
ctx.rect(10, 10, 100, 30)
ctx.setStrokeStyle('yellow')
ctx.stroke()

// begin another path
ctx.beginPath()
ctx.rect(10, 40, 100, 30)

// only stoke this rect, not in current path
ctx.setStrokeStyle('blue')
ctx.strokeRect(10, 70, 100, 30)

ctx.rect(10, 100, 100, 30)

// it will stroke current path
ctx.setStrokeStyle('red')
ctx.stroke()
ctx.draw()
```

> 画出当前路径的边框。默认颜色色为黑色。
>
> **Tip**:`stroke()`描绘的的路径是从`beginPath()`开始计算，但是不会将`strokeRect()`包含进去，详情见例二。



### 25. 微信小程序API 绘图beginPath（开始一个路径）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
// begin path
ctx.rect(10, 10, 100, 30)
ctx.setFillStyle('yellow')
ctx.fill()

// begin another path
ctx.beginPath()  //开始一个路径
ctx.rect(10, 40, 100, 30)

// only fill this rect, not in current path
ctx.setFillStyle('blue')
ctx.fillRect(10, 70, 100, 30)

ctx.rect(10, 100, 100, 30)

// it will fill current path
ctx.setFillStyle('red')
ctx.fill()
ctx.draw()
```

> 开始创建一个路径，需要调用fill或者stroke才会使用路径进行填充或描边。
>
> **Tip**: 在最开始的时候相当于调用了一次`beginPath()`。
>
> **Tip**: 同一个路径内的多次`setFillStyle()`、`setStrokeStyle()`、`setLineWidth()`等设置，以最后一次设置为准



### 26. 微信小程序API 绘图closePath（关闭一个路径）

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.moveTo(10, 10)
ctx.lineTo(100, 10)
ctx.lineTo(100, 100)
ctx.closePath()  //关闭一个路径
ctx.stroke()
ctx.draw()
```

```javascript
const ctx = wx.createCanvasContext('myCanvas')
// begin path
ctx.rect(10, 10, 100, 30)
ctx.closePath()

// begin another path
ctx.beginPath()
ctx.rect(10, 40, 100, 30)

// only fill this rect, not in current path
ctx.setFillStyle('blue')
ctx.fillRect(10, 70, 100, 30)

ctx.rect(10, 100, 100, 30)

// it will fill current path
ctx.setFillStyle('red')
ctx.fill()
ctx.draw()
```

> Tip**: 关闭路径会连接起点和终点。
>
> **Tip**: 如果关闭路径后没有调用`fill()`或者`stroke()`并开启了新的路径，那之前的路径将不会被渲染。



### 27. 微信小程序使用moveTo把路径移动到画布中的指定点，不创建线条

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.moveTo(10, 10)  //移动到画布中的指定点
ctx.lineTo(100, 10)

ctx.moveTo(10, 50)
ctx.lineTo(100, 50)
ctx.stroke()
ctx.draw()
```



### 28. 微信小程序中使用lineTo方法增加一个新点

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.moveTo(10, 10)
ctx.rect(10, 10, 100, 50) 
ctx.lineTo(110, 60)  // 增加一个新点
ctx.stroke()
ctx.draw()
```



### 29. 使用arc()方法在微信小程序canvas中画弧线

```javascript
const ctx = wx.createCanvasContext('myCanvas')
// Draw arc
ctx.beginPath()
ctx.arc(100, 75, 50, 0, 1.5 * Math.PI)
ctx.setStrokeStyle('#333333')
ctx.stroke()
ctx.draw()
```

| 参数             | 类型    | 说明                                                         |
| ---------------- | ------- | ------------------------------------------------------------ |
| x                | Number  | 圆的x坐标                                                    |
| y                | Number  | 圆的y坐标                                                    |
| r                | Number  | 圆的半径                                                     |
| sAngle           | Number  | 起始弧度，单位弧度（在3点钟方向）                            |
| eAngle           | Number  | 终止弧度                                                     |
| counterclockwise | Boolean | 可选。指定弧度的方向是逆时针还是顺时针。默认是false，即顺时针。 |

> **Tip**: 创建一个圆可以用`arc()`方法指定起始弧度为0，终止弧度为`2 * Math.PI`。
>
> **Tip**: 用`stroke()`或者`fill()`方法来在 canvas 中画弧线。



### 30. 在微信小程序绘图API中创建二次方贝塞尔曲线

```javascript
const ctx = wx.createCanvasContext('myCanvas')

// Draw points
ctx.beginPath()
ctx.arc(20, 20, 2, 0, 2 * Math.PI)
ctx.setFillStyle('red')
ctx.fill()

ctx.beginPath()
ctx.arc(200, 20, 2, 0, 2 * Math.PI)
ctx.setFillStyle('lightgreen')
ctx.fill()

ctx.beginPath()
ctx.arc(20, 100, 2, 0, 2 * Math.PI)
ctx.setFillStyle('blue')
ctx.fill()

ctx.setFillStyle('black')
ctx.setFontSize(12)

// Draw guides
ctx.beginPath()
ctx.moveTo(20, 20)
ctx.lineTo(20, 100)
ctx.lineTo(200, 20)
ctx.setStrokeStyle('#AAAAAA')
ctx.stroke()

// Draw quadratic curve
ctx.beginPath()
ctx.moveTo(20, 20)
ctx.quadraticCurveTo(20, 100, 200, 20)  // 创建二次方贝塞尔曲线
ctx.setStrokeStyle('black')
ctx.stroke()

ctx.draw()
```

> **Tip**: 曲线的起始点为路径中前一个点。

| 参数 | 类型   | 说明                |
| ---- | ------ | ------------------- |
| cpx  | Number | 贝塞尔控制点的x坐标 |
| cpy  | Number | 贝塞尔控制点的y坐标 |
| x    | Number | 结束点的x坐标       |
| y    | Number | 结束点的y坐标       |

针对 `moveTo(20, 20)` `quadraticCurveTo(20, 100, 200, 20)`的三个关键坐标如下：

- 红色：起始点(20, 20)
- 蓝色：控制点(20, 100)
- 绿色：终止点(200, 20)



### 31. 在微信小程序API绘图中创建三次方贝塞尔曲线路径

```javascript
const ctx = wx.createCanvasContext('myCanvas')

// Draw points
ctx.beginPath()
ctx.arc(20, 20, 2, 0, 2 * Math.PI)
ctx.setFillStyle('red')
ctx.fill()

ctx.beginPath()
ctx.arc(200, 20, 2, 0, 2 * Math.PI)
ctx.setFillStyle('lightgreen')
ctx.fill()

ctx.beginPath()
ctx.arc(20, 100, 2, 0, 2 * Math.PI)
ctx.arc(200, 100, 2, 0, 2 * Math.PI)
ctx.setFillStyle('blue')
ctx.fill()

ctx.setFillStyle('black')
ctx.setFontSize(12)

// Draw guides
ctx.beginPath()
ctx.moveTo(20, 20)
ctx.lineTo(20, 100)
ctx.lineTo(150, 75)

ctx.moveTo(200, 20)
ctx.lineTo(200, 100)
ctx.lineTo(70, 75)
ctx.setStrokeStyle('#AAAAAA')
ctx.stroke()

// Draw quadratic curve
ctx.beginPath()
ctx.moveTo(20, 20)
ctx.bezierCurveTo(20, 100, 200, 100, 200, 20)  //创建三次方贝塞尔曲线路径
ctx.setStrokeStyle('black')
ctx.stroke()

ctx.draw()
```

> **Tip**: 曲线的起始点为路径中前一个点。

| 参数 | 类型   | 说明                        |
| ---- | ------ | --------------------------- |
| cp1x | Number | 第一个贝塞尔控制点的 x 坐标 |
| cp1y | Number | 第一个贝塞尔控制点的 y 坐标 |
| cp2x | Number | 第二个贝塞尔控制点的 x 坐标 |
| cp2y | Number | 第二个贝塞尔控制点的 y 坐标 |
| x    | Number | 结束点的 x 坐标             |
| y    | Number | 结束点的 y 坐标             |

针对 `moveTo(20, 20)` `bezierCurveTo(20, 100, 200, 100, 200, 20)` 的三个关键坐标如下：

- 红色：起始点(20, 20)
- 蓝色：两个控制点(20, 100) (200, 100)
- 绿色：终止点(200, 20)



### 32. 在微信小程序中调用scale方法对横纵坐标进行缩放

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.strokeRect(10, 10, 25, 15)
ctx.scale(2, 2)  //(scaleWidth, scaleHeight)
ctx.strokeRect(10, 10, 25, 15)  //2倍
ctx.scale(2, 2)
ctx.strokeRect(10, 10, 25, 15)  //4倍

ctx.draw()
```

> 在调用`scale`方法后，之后创建的路径其横纵坐标会被缩放。多次调用`scale`，倍数会相乘。



### 33. 微信小程序API 绘图对坐标轴进行顺时针旋转

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.strokeRect(100, 10, 150, 100)
ctx.rotate(20 * Math.PI / 180)  // 旋转20度
ctx.strokeRect(100, 10, 150, 100)
ctx.rotate(20 * Math.PI / 180)
ctx.strokeRect(100, 10, 150, 100)

ctx.draw()
```

> 以原点为中心，原点可以用 [translate](https://www.w3cschool.cn/weixinapp/weixinapp-api-canvas-translate.html)方法修改。顺时针旋转当前坐标轴。多次调用`rotate`，旋转的角度会叠加。

| 参数   | 类型   | 说明                                                         |
| ------ | ------ | ------------------------------------------------------------ |
| rotate | Number | 旋转角度，以弧度计(degrees * Math.PI/180；degrees范围为0~360) |



### 34. 微信小程序canvas中使用translate对坐标原点进行缩放

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.strokeRect(10, 10, 150, 100)
ctx.translate(20, 20)  //(offsetX, offsetY)
ctx.strokeRect(10, 10, 150, 100)
ctx.translate(20, 20)
ctx.strokeRect(10, 10, 150, 100)

ctx.draw()
```



### 35. 微信小程序API 绘图setFontSize（设置字号）

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.setFontSize(20)
ctx.fillText('20', 20, 20)

ctx.draw()
```



### 36. 微信小程序绘图API中使用fillText在画布上绘制被填充的文本

```javascript
ctx.fillText('20', 20, 20)  // (text, x, y)
```



### 37. 微信小程序API·setTextAlign（用于设置文字的对齐）

```javascript
    const ctx = wx.createCanvasContext('myCanvas')

    ctx.setStrokeStyle('red')
    ctx.moveTo(150, 20)
    ctx.lineTo(150, 170)
    ctx.stroke()

    ctx.setFontSize(15)
    ctx.setTextAlign('left')
    ctx.fillText('textAlign=left', 150, 60)

    ctx.setTextAlign('center')
    ctx.fillText('textAlign=center', 150, 80)

    ctx.setTextAlign('right')
    ctx.fillText('textAlign=right', 150, 100)

    ctx.draw()
```



### 38. 微信小程序API·setTextBaseline（设置文字水平对齐）

```javascript
    const ctx = wx.createCanvasContext('myCanvas')
    ctx.setStrokeStyle('red')
    ctx.moveTo(5, 75)
    ctx.lineTo(295, 75)
    ctx.stroke()

    ctx.setFontSize(20)

    ctx.setTextBaseline('top')
    ctx.fillText('top', 5, 75)

    ctx.setTextBaseline('middle')
    ctx.fillText('middle', 50, 75)

    ctx.setTextBaseline('bottom')
    ctx.fillText('bottom', 120, 75)

    ctx.setTextBaseline('normal')
    ctx.fillText('normal', 200, 75)

    ctx.draw()
```



### 39. 微信小程序API中，使用drawImage完成绘制图像，图像保持原始尺寸

```javascript
const ctx = wx.createCanvasContext('myCanvas')

wx.chooseImage({
  success: function(res){
    ctx.drawImage(res.tempFilePaths[0], 0, 0, 150, 100)
    ctx.draw()
  }
})
```

| imageResource | String | 所要绘制的图片资源 |
| ------------- | ------ | ------------------ |
| x             | Number | 图像左上角的x坐标  |
| y             | Number | 图像左上角的y坐标  |
| width         | Number | 图像宽度           |
| height        | Number | 图像高度           |



### 40. 微信小程序API 绘图中使用setGlobalAlpha设置全局画笔透明度

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.setFillStyle('red')
ctx.fillRect(10, 10, 150, 100)
ctx.setGlobalAlpha(0.2)  //透明度，0 表示完全透明，1 表示完全不透明
ctx.setFillStyle('blue')
ctx.fillRect(50, 50, 150, 100)
ctx.setFillStyle('yellow')
ctx.fillRect(100, 100, 150, 100)

ctx.draw()
```



### 41. 微信小程序save/restore（保存和恢复绘图上下文）

```javascript
const ctx = wx.createCanvasContext('myCanvas')

// save the default fill style
ctx.save()  //保存当前的绘图上下文
ctx.setFillStyle('red')
ctx.fillRect(10, 10, 150, 100)

// restore to the previous saved state
ctx.restore()  //恢复之前保存的绘图上下文
ctx.fillRect(50, 50, 150, 100)

ctx.draw()
```



### 42. 微信小程序API 绘图·draw（进行绘图）

```javascript
const ctx = wx.createCanvasContext('myCanvas')

ctx.setFillStyle('red')
ctx.fillRect(10, 10, 150, 100)
ctx.draw()
ctx.fillRect(50, 50, 150, 100)
ctx.draw(true)
```

| 参数     | 类型     | 说明                                                         | 最低版本                                                     |
| -------- | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| reserve  | Boolean  | 非必填。本次绘制是否接着上一次绘制，即reserve参数为false，则在本次调用drawCanvas绘制之前native层应先清空画布再继续绘制；若reserver参数为true，则保留当前画布上的内容，本次调用drawCanvas绘制的内容覆盖在上面，默认 false |                                                              |
| callback | Function | 绘制完成后回调                                               | [1.7.0](https://www.w3cschool.cn/weixinapp/compatibility.html) |



### 43. 微信小程序API 绘图·getActions(不推荐使用)

### 44. 微信小程序API 绘图·clearActions (不推荐使用)

### 45. 微信小程序API 绘图·measureText

测量文本尺寸信息，目前仅返回文本宽度。同步接口。

```javascript
const ctx = wx.createCanvasContext('myCanvas')
ctx.font = 'italic bold 20px cursive'
const metrics = ctx.measureText('Hello World')
console.log(metrics.width)
```



### 46. 微信小程序API 绘图·globalCompositeOperation

该属性是设置要在绘制新形状时应用的合成操作的类型。

```javascript
canvasContext.globalCompositeOperation = type
```

type 支持的操作有：

| 平台 |                             操作                             |
| :--: | :----------------------------------------------------------: |
| 安卓 | xor, source-over, source-atop, destination-out, lighter, overlay, darken, lighten, hard-light |
| iOS  | xor, source-over, source-atop, destination-over, destination-out, lighter, multiply, overlay, darken, lighten, color-dodge, color-burn, hard-light, soft-light, difference, exclusion, saturation, luminosity |



### 47. 微信小程序API 绘图·arcTo

根据控制点和半径绘制圆弧路径。

```javascript
canvasContext.arcTo(x1, y1, x2, y2, radius)  //	radius为圆弧的半径
```



### 48. 微信小程序API 绘图·strokeText

给定的 (x, y) 位置绘制文本描边的方法

```javascript
canvasContext.strokeText(text, x, y, maxWidth)
```

|  属性值  |  类型  |           说明           |
| :------: | :----: | :----------------------: |
|   text   | String |       要绘制的文本       |
|    x     | Number |  文本起始点的 x 轴坐标   |
|    y     | Number |  文本起始点的 y 轴坐标   |
| maxWidth | Number | 需要绘制的最大宽度，可选 |



### 49. 微信小程序API 绘图·lineDashOffset

设置虚线偏移量的属性

```javascript
canvasContext.lineDashOffset = value
```

Value偏移量，初始值为 0



### 50. 微信小程序API 绘图·createPattern

对指定的图像创建模式的方法，可在指定的方向上重复元图像

```javascript
canvasContext.createPattern(image, repetition)
```

|   属性值   |  类型  |                             说明                             |
| :--------: | :----: | :----------------------------------------------------------: |
|   image    | String |            重复的图像源，仅支持包内路径和临时路径            |
| repetition | String | 指定如何重复图像，有效值有: repeat, repeat-x, repeat-y, no-repeat |

```javascript
const ctx = wx.createCanvasContext('myCanvas')
const pattern = ctx.createPattern('/path/to/image', 'repeat-x')
ctx.fillStyle = pattern
ctx.fillRect(0, 0, 300, 150)
ctx.draw()
```

