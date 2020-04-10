 在ImageView显示图片时，有如下几种图片填充模式scaleType： matrix ，fitXY，fitStart, fitEnd, fitCenter, center, centerCrop, centerInside。

我感兴趣的是这几种图片填充模式是如何实现的，在这里我们以fitCenter为例，动手探索一下这种填充模式算法是如何实现的。通过思考算法，我也更深刻体会到了这几种填充模式应用场景。

只有当图片本身的大小不符合ImageView控件的大小时，才会发生填充的动作， fitCenter顾名思义是居中填充。我们不妨将ImageView看成一张画布，那么填充模式解决的问题其实就是**如何画图以及在哪里画图的问题**。

套用上面的话来说，fitCenter模式解决的就是：

1. 图片完整展现 （fit开头的模式都是保留完整的图片，不存在切割和局部展现问题）

2. 图片要居中绘制

绘制图片到画布时，重要的参考指标就是**图片的宽高比，以及画布的宽高比**，这两个参数的差值决定了以何种方式拉伸图片。可能你还是一头雾水，我们分两种情况来讨论。 

假设图片高h，宽w ， Imageview的高y，宽x ，比较两者高宽比。

>  $$\frac{y}{x}  –\frac{h} {w} > 0 $$

说明Imageview的高宽比大于图片的高宽比，如图所示：

![img](http://pic.yupoo.com/wangyuetingtao/CBmk4Pfx/dmp0z.png)

 左图实线标示的是图片Imageview的高和宽，右图是Imageview。 如果实现Image居中完全展示，需要计算画布的宽高和绘制点。

 显而易见，画布的宽度是w，高度h1 。

 画布的高宽比必须和Imageview的高宽比相同，即 y / x = h1 / w  , 计算出 h1 = (y * w) / x

 计算出画布的高度和宽度，那么图片的绘制点 p的坐标为 (0, (h1 – h) / 2)

> $$\frac{y}{x}  –\frac{h} {w} \le 0 $$

说明Imageview的高宽比小于图片的高宽比，如图所示：

![img](http://pic.yupoo.com/wangyuetingtao/CBmk0D4Z/aEuEA.png)

显而易见，画布的高度为h， 宽度为w1 ，依据 y / x = h / w1 , 计算出 w1 = (h * x) / y

图片的绘制点P 的坐标是 ((w1 – w) / 2 , 0)

 好了，算法分析完了，我们来动手实现fitCenter模式。为了方便观看，我们将图片背景绘制为黑色。

 核心算法：

```java
     /**
      * resize图片，以 fitcenter模式填充到指定宽高的 imageview中
      *
      * @param src
      *            原始图片
      * @param destWidth
      *            imageview 高度
      * @param destHeight
      *            imageview 宽度
      * @return
      */
     public Bitmap resizeBitmap(Bitmap src, int destWidth, int destHeight) {
           if (src == null || destWidth == 0 || destHeight == 0) {
               return null ;
          }

           // 图片宽度
           int w = src.getWidth();

           // 图片高度
           int h = src.getHeight();

           // Imageview 宽度
           int x = destWidth;
           
           // Imageview 高度
           int y = destHeight;
           // 高宽比之差
           int temp = (y / x) - (h / w);
           
           /**
            * 判断高宽比例，如果目标高宽比例大于原图，则原图宽度不变，高度按照比例(h1 = (y * w) / x)拉伸
            * 画布宽高(w,h1),原图绘制点在(0, (h1 -h)/2)
            */

           if (temp > 0) {
               // 计算画布高度
               int h1 = (y * w) / x;
               // 创建一个指定高宽的图片
              Bitmap newb = Bitmap. createBitmap(w, h1, Config.ARGB_8888);

               // 创建画布
              Canvas cv = new Canvas(newb);

              // 画布背景设置为黑色
              cv.drawColor(Color. BLACK);
               // 在 0，(h1-h)/2坐标开始画入 src
              cv.drawBitmap(src, 0, (h1 - h) / 2, null);
               // 保存
              cv.save(Canvas. ALL_SAVE_FLAG);
               // 存储
              cv.restore();
               return newb;
          } else {

               /**
                * 如果高宽比小于原图，则原图高度不变，宽度按照比例(w1 = (h * x) / y),画布宽高(w1, h),
                * 原图绘制点((w1 -w)/2 , 0)
                */

              // 计算画布高度
              int w1 = (h * x) / y;
               // 创建一个指定高宽的图片
              Bitmap newb = Bitmap. createBitmap(w1, h, Config.ARGB_8888);

               // 创建画布
              Canvas cv = new Canvas(newb);

               // 绘制一个黑色背景的图片
              cv.drawColor(Color. BLACK);

               // 在 0，(h1-h)/2坐标开始画入 src
              cv.drawBitmap(src, (w1 - w) / 2, 0, null);

               // 保存
              cv.save(Canvas. ALL_SAVE_FLAG);

               // 存储
              cv.restore();
              return newb;
          }

     }
```



 效果图：

![img](http://pic.yupoo.com/wangyuetingtao/CBmkp6A0/37fCw.png)





 CenterCrop模式解决的就是：

1. 图片要去两头，留中间

2. 图片要填充满控件

这个模式和fitCenter还有有很大的不同。借鉴上篇文章的思路，我们同样按照Image与ImageView的宽高比差值，分两种情况进行讨论。

 假设原始图片高h，宽w ， Imageview的高y，宽x ，比较两者高宽比。裁剪出的图称为Image1：

 1、 当 y / x – h / w > 0 时

  说明Imageview的高宽比大于图片的高宽比，如图所示：

![img](http://pic.yupoo.com/wangyuetingtao/CJUCPo9E/11QfGw.png)

  左图实线标示的是图片Image的高和宽，右图是Imageview。 我们需要从Image的中间按照比例y/x裁剪出一幅图Image1来，如图中虚线所示。 

  显而易见，Image1的宽度是w1，高度是h 。

  Image1的高宽比必须和Imageview的高宽比相同，即 y / x = h / w1  , 计算出 w1 = (h * x )/ y

  在FitCenter模式中，我们需要计算Image在画布上的绘制点。在CenterCrop模式中，都是裁剪操作，我们只需要计算在Image的什么地方进行裁剪。从图上可以看出，裁剪点P的坐标是（(w – w1) / 2, 0）。

 2、当 y / x – h / w <= 0时

  说明Imageview的高宽比小于图片的高宽比，如图所示：

![img](http://pic.yupoo.com/wangyuetingtao/CJUCOIVE/T81Dp.png)

  显而易见，Image1高度为h1， 宽度为w ，依据 y / x = h1 / w , 计算出 h1 = (w * y) / x

  裁剪点P 的坐标是 (0, (h – h1) / 2)

  好了，算法我们分析出来了。在Android中绘制图片的某一个部分使用到了函数 Bitmap.createBitmap(Bitmap source, int x, int y, int width, int height)

  source是原始图片，x指的是绘制的横坐标，y指的是绘制的纵坐标。width,height分别代表宽高。

 下面给出核心代码实现：

```java
/**
 * 以CenterCrop方式resize图片
 * @param src  原始图片
 * @param destWidth  目标图片宽度
 * @param destHeight 目标图片高度
 * @return
 */

public Bitmap resizeBitmapByCenterCrop(Bitmap src, int destWidth, int destHeight) {

    if (src == null || destWidth == 0 || destHeight == 0) {
        return null;
    }

    // 图片宽度
    int w = src.getWidth();

    // 图片高度
    int h = src.getHeight();

    // Imageview宽度
    int x = destWidth;

    // Imageview高度
    int y = destHeight;
    
    // 高宽比之差
    int temp = (y / x) - (h / w);

    /**
     * 判断高宽比例，如果目标高宽比例大于原图，则原图高度不变，宽度为(w1 = (h * x) / y)拉伸
     * 画布宽高(w1,h),在原图的((w - w1) / 2, 0)位置进行切割
     */
    if (temp > 0) {

        // 计算画布宽度

        int w1 = (h * x) / y;

        // 创建一个指定高宽的图片

        Bitmap newb = Bitmap.createBitmap(src, (w - w1) / 2, 0, w1, h);

        //原图回收
        src.recycle();

        return newb;

    } else {

        /**
         * 如果目标高宽比小于原图，则原图宽度不变，高度为(h1 = (y * w) / x),
         * 画布宽高(w, h1), 原图切割点(0, (h - h1) / 2)
         */

        // 计算画布高度
        int h1 = (y * w) / x;

        // 创建一个指定高宽的图片
        Bitmap newb = Bitmap.createBitmap(src, 0, (h - h1) / 2, w, h1);
        //原图回收
        src.recycle();
        return newb;
    }
}
```



  效果图：

![img](http://pic.yupoo.com/wangyuetingtao/CJUG02U8/103TnH.png)

