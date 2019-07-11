
## RecyclerView仿Gallery效果

### RecyclerView仿Gallery效果
> 
作者：android_hcf  
链接：https://www.jianshu.com/p/198748de8581  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。  

由于RecyclerView提供的LayoutManager有限，只能满足日常常见的一些效果，如果想达到一些想要的效果，则需要重写LayoutManager了。网上重写LayoutManger的例子非常多，例如 [你可能误会了！原来自定义LayoutManager可以这么简单](https://www.jianshu.com/p/715b59c46b74)。所以以下关于LayoutManger需要重写方法的细节我就不再这里一一赘述了。

<img src="https://upload-images.jianshu.io/upload_images/2223007-5bc45786becb4257.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/240/format/webp" width="200px" height="auto"/>


### ViewPager 实现 Gallery 效果
> 中间大图显示，两边小图展示

<img src="https://img-blog.csdn.net/20160827224815332?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center" width="200px" height="auto"/>

 - [CSDN](https://blog.csdn.net/xiangzhihong8/article/details/52337374) 
 - [Github](https://github.com/xiangzhihong/jingdongApp)


###  FancyCoverFlow
> 一个页面显示多张图片，中间大，两边小  

<img src="https://img-blog.csdn.net/20170427143816915?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcXFfMzgyNTA2ODI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast" width="200px" height="auto"/>


- [github](https://github.com/LittleLiByte/GlFancyCoverFlow)1
- [github](https://github.com/davidschreiber/FancyCoverFlow)2

### 旋转木马  
<img src="https://github.com/dalong982242260/CarrouselView/raw/master/screenshot/carouselview.gif" width="200px" height="auto"/>
  
[github](https://github.com/dalong982242260/CarrouselView)

<img src="https://github.com/dalong982242260/LoopRotarySwitch/raw/master/img/dalong2.gif" width="200px" height="auto"/>
  
[github](https://github.com/dalong982242260/LoopRotarySwitch)

## 图片 颜色
### 图片取色并让图片融入背景色 

<img src="https://upload-images.jianshu.io/upload_images/6912282-7ca5ddc262663eb7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp" width="200px" height="auto"/>


<img src="https://upload-images.jianshu.io/upload_images/6912282-7e2f55efcae3f39b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp" width="200px" height="auto"/>


[Github](https://github.com/DongDian455/MyDemoList.git)

### Android通过代码修改图片颜色

> 
作者：简简单单敲代码  
链接：https://www.jianshu.com/p/514fbcd7e98d  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。  

最近公司的详情页改版，有一个需求设计同学觉得挺好，需要我们实现出来。
具体的需求大概就是，toolbar 上面的图标，需要根据滑动的距离去改变颜色~

当然是难不倒我们伟大的工程师(码农)的，所以讨论需求两小时，开发五分钟实现了设计的需求。

> 先看效果图 

<img src="https://upload-images.jianshu.io/upload_images/1432234-94181658e1f7f22b.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/352/format/webp" width="200px" height="auto"/>


> 其实需求也就两点

1.灰色圆圈背景需要根据滑动距离变透明，其实改变它的alpha值就行了，这个容易。  
2.就是白色图标需要渐变成黑色，这个其实也不难。

#### 技术点

这个时候肯定需要去查阅下相关API文档了，发现原生确实就有 API 实现，相当的容易。
在官网中发现有这个 API，位于android.support.v4.graphics.drawable.DrawableCompat下：

中文意思差不多就是可以给指定的drawable着色。
有了这个 API 就好办了，我们去监听下面的控件滑动距离，根据距离去设置给图片着色。

#### 核心代码
```kotlin
fun tintDrawable(drawable: Drawable, colors: ColorStateList): Drawable {
    val wrappedDrawable = DrawableCompat.wrap(drawable)
    DrawableCompat.setTintList(wrappedDrawable, colors)
    return wrappedDrawable
}
```
> 在需要改变的地方调用这行代码即可

```java
 imageView.setImageDrawable(tintDrawable(imageView.drawable, ColorStateList.valueOf(Color.argb(alpha, red, green, blue))))
```

### SetColorFilter 改变图片颜色

> 
作者：DRPrincess   
来源：CSDN   
原文：https://blog.csdn.net/qq_32452623/article/details/79878132   
版权声明：本文为博主原创文章，转载请附上博文链接！  

有一个效果展示是这样的，选中某个车型时，显示选中的颜色，是主题色红色。
<img src="https://raw.githubusercontent.com/DRPrincess/BlogImages/master/qiniu/646D48768CC5BAB2662C9E295FE92C2E.jpg" width="200px" height="auto"/>


产品和UI宝宝决定要把主题色改成蓝色，于是选中效果要像下面这样：  
<img src="https://raw.githubusercontent.com/DRPrincess/BlogImages/master/qiniu/2D2974E3BFC803C9392EAF0415A66538.jpg" width="200px" height="auto"/>


原图，是这个样子的:  
<img src="https://raw.githubusercontent.com/DRPrincess/BlogImages/master/qiniu/e53dfe62f49a0ec9c0b712403b91c3b1.png" width="200px" height="auto"/>


#### 代码控制颜色显示：

```java
//定义选中的颜色
int checkColor = context.getResources().getColor(R.color.theme_red);

//当选中该项时，显示选中颜色，否则显示未选中颜色
viewHolder.icon.setColorFilter(selectPosition==position? checkColor :Color.TRANSPARENT);
```

更多关于 [PorterDuff.Mode](https://blog.csdn.net/IO_Field/article/details/78222527) | [more](https://www.jianshu.com/p/d11892bbe055)

<img src="https://upload-images.jianshu.io/upload_images/2041548-d964105abf4be5d9.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/312/format/webp" width="200px" height="auto"/>


##### 问题：



> 
作者：多啦欸A梦    
来源：CSDN   
原文：https://blog.csdn.net/jiangxiao_000/article/details/80585983   
版权声明：本文为博主原创文章，转载请附上博文链接！     

只有一套图标，图标本身的内容比较简单，但是在不同场景下需要显示不同的颜色，且只改变图标颜色，不改变透明度


> 解法

通过如下参数构造ColorMatrix，进而构造ColorMatrixColorFilter，然后调用ImageView.setColorFilter()方法调整图标颜色

```java
float[] m  = {
        0, 0, 0, 0, R,
        0, 0, 0, 0, G,
        0, 0, 0, 0, B,
        0, 0, 0, 1, 0,
};
```
涉及到的类和方法
```java
ImageView.setColorFilter(ColorFilter);
```

- ColorFilter
- ColorMatrix
- ColorMatrixColorFilter


#### XML(tint)
简单一行代码搞定，只需要在imageview中添加如下：
```xml
android:tint="#ff0000"
````
