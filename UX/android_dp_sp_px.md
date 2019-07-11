![](https://upload-images.jianshu.io/upload_images/2684179-5f31c83fb448db90.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)


### 前言： 

众所周知，Android厂商非常多，各种尺寸的android手机、平板层出不穷。导致了Android生态环境的碎片化现象越来越严重。Google公司为了解决分辨率过多的问题，在Android的开发文档中定义了px、dp、sp，方便开发者适配不同分辨率的Android设备。对于初级程序员来说理解掌握适配的一些基础知识是必须的。



###### Android 开发使用尺寸单位

密度 | lpdi | mdpi | hdpi | xhdpi | xxhdpi | xxxhdpi 
-- | -- | -- | -- | -- | -- | -- 
标注  | | 44dp|  44dp | 44 dp | 44 dp | 
像素  | | 44px | 66 px | 88 px | 132 px |
倍率| @0.75| @1x|@1.5x|@2x|@3x|@4x

- `dp`：android 开发使用的单位，其实相当于一种比例换算单位，它可以保证控件在不同密度的屏幕上按照这个比例单位换算显示相同的效果。  
- `sp`：android 开发使用的文字单位，和dp差不多，也是为了保证文字在不同密度的屏幕上显示相同的效果，同时可以保证系统字体大小的变化而变化。

> 对于 Android 工程师，只需要记住两点：一是对于字体的大小使用 `sp` 作为尺寸单位；而是对于其他非字体的如图片、按钮、图标等使用 `dp` 作为尺寸单位。  
> 对于 UI 设计师而言，在对 UI 进行标注时，需要将 `px` 转换成 `dp`，`sp`  
> 后面的已经不重要了^v^



### 基础概念

类型 | 描述
-- | -- 
px |  其实就是像素单位，比如我们通常说的手机分辨列表800*400都是px的单位   
sp | 同dp相似，还会根据用户的字体大小偏好来缩放 
dp | 虚拟像素，在不同的像素密度的设备上会自动适配 
dpi| 同dp

> 概念理得不够，如 dp dpi ppi sp px pt... 

### 举个栗子 : px VS. dp 
pixel，即像素，1px代表屏幕上的一个物理的像素点。但px单位不被建议使用。因为同样像素大小的图片在不同手机显示的实际大小可能不同。要用到px的情况是需要画1像素表格线或阴影线的时候，如果用其他单位画则会显得模糊。

要理解dp，首先要先引入dpi这个概念，dpi全称是dots per inch，对角线每英寸的像素点的个数，所以，它的计算公式如下：

![](http://7d9qiv.com2.z0.glb.qiniucdn.com/data/file/5/3/5/400535.jpg)

```Latex
dpi = \dfrac{\sqrt{height^2 + width^2}}{size}
```
> 此处似乎用错了概念吧，是不是应该是 ppi 啊？？

比如 height 和 width 即为长宽的像素，平方和即为对角线的像素个数，size即我们常说的5寸手机、4寸手机中的5和4，即对角线的长度。   
所以，一样是5寸的手机，分辨率越高，dpi越高。分辨率相同，屏幕对角线英寸数越小，dpi越高。

而dp也叫dip，是device independent pixels。设备不依赖像素的一个单位。在不同的像素密度的设备上会自动适配，比如:
```
在320x480分辨率，像素密度为160,1dp=1px 
在480x800分辨率，像素密度为240,1dp=1.5px 
计算公式：px = dp * (dpi/160)
```

我们做个简单的Sample验证一下，如下,一个布局代码
```xml
    <Button
        android:layout_width="150px"
        android:layout_height="wrap_content"
        android:text="Test px" />
    <Button
        android:layout_width="150dp"
        android:layout_height="wrap_content"
        android:text="Test dp" />
```

 3.7 in（480\*800） | 5.1 in（480\*800）
  -- | -- 
  ![](https://img-blog.csdn.net/20170829162412459?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZG9ua29yXw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast) | ![](https://img-blog.csdn.net/20170829162422477?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZG9ua29yXw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


>> 由此可以看出使用px作为单位的，在不同的设备中会显示不同的效果。使用dp作为单位的，会根据不同的设备进行转化，适配不同机型。所以建议在长度宽度的数值使用dp作为单位。

### 再举个栗子 : dp VS. sp 
既然我们在上面说了，dp可以自动适配设备机型，那在字体里是否也同样可行？我们再做个简单的Sample验证一下，如下,一个布局代码
```xml
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Test dp"
        android:textSize="20dp" />
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Test sp"
        android:textSize="20sp" />
```
 3.7 in（480\*800） | 3.7 in（480\*800）修改系统字体大小
  -- | -- 
  ![](https://img-blog.csdn.net/20170829163733646?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZG9ua29yXw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast) | ![](https://img-blog.csdn.net/20170829164600424?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZG9ua29yXw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)


>> 由此可以看出使用sp作为字体大小单位,会随着系统的字体大小改变，而dp作为单位则不会。所以建议在字体大小的数值要使用sp作为单位

### 拓展 
提供一个工具类：dp与px值转换

```java
public class DensityUtil {

    /**
     * 根据手机的分辨率从 dp 的单位 转成为 px(像素)
     */
    public static int dp2px(Context context, float dpValue) {
        final float scale = context.getResources().getDisplayMetrics().density;
        return (int) (dpValue * scale + 0.5f);
    }

    /**
     * 根据手机的分辨率从 px(像素) 的单位 转成为 dp
     */
    public static int px2dp(Context context, float pxValue) {
        final float scale = context.getResources().getDisplayMetrics().density;
        return (int) (pxValue / scale + 0.5f);
    }
}
```

--------------------- 
作者：Donkor-   
来源：CSDN   
原文：https://blog.csdn.net/donkor_/article/details/77680042   
版权声明：本文为博主原创文章，转载请附上博文链接！

----

## dp、sp、px傻傻分不清楚[完整]


做移动设计的同学，不管是原生 app 或者 web app，应该对字体字号都是很头痛的问题。根本原因是，我们用唯一分辨率的电脑，设计各个不同尺寸大小分辨率的设备，那简直要疯掉了。

但不要着急，我们先来理解一下一些名词：
我们一般会碰到的度量单位主要有：**dpi、ppi、dp、sp、px、pt、in**。其中，**px** 应该各位最熟悉的单位，也是我们主要使用的photoshop 或者 axure 等工具用的度量单位，而它在移动端时，的确已经“过时”了。但不要着急把它丢掉，因为它是接下来非常重要的换算单位（所有手机参数还是用px在表达）。

**dpi** 和 **ppi** 这两个是密度单位，不是度量单位，而这两个恰恰是我们换算中重要的分母。简单理解一下：

- ppi (pixels per inch)：图像分辨率 （在图像中，每英寸所包含的像素数目）
- dpi (dots per inch)： 打印分辨率 （每英寸所能打印的点数，即打印精度）

dpi主要应用于输出，重点是打印设备上。

![](https://pic4.zhimg.com/80/9ae594fa58c25f4a2e4fd267b0f62d13_hd.jpg)

我们在移动应用中提到 ppi 和 dpi 其实都一样（概念不同，但对设计来讲没有特别需要深入了解），所以我们先忽略掉dpi。而ppi的运算方式是：
```
PPI = √（长度像素数² + 宽度像素数²） / 屏幕对角线英寸数
```

> 举个简单的栗子，iphone5 的ppi是多少？  
> ppi=√（1136px² + 640px²）/4 in=326ppi（视网膜Retina屏）.  
> 这样大家就能够明白ppi和px的关系。

这里还提到in（英寸）这个词，这个非常重要，因为现实中我们经常提到4英寸手机或者5.5英寸大屏手机，而这个尺寸是用户真正感受到的物理大小，所有提到不同尺寸的屏幕不仅仅是分辨率或者像素，而更多的是英寸。

###### 好，现在关键的来了，dp、sp、pt，是我们设计中的关键。

**dp：**Density-independent pixels，以160PPI屏幕为标准，则1dp=1px，dp和px的换算公式 ：
```
dp*ppi/160 = px。
```

> 比如1dp x 320ppi/160 = 2px。

**sp：**Scale-independent pixels，它是安卓的字体单位，以160PPI屏幕为标准，当字体大小为 100%时， 1sp=1px。
sp 与 px 的换算公式：
```
sp*ppi/160 = px
```
是不是看起来dp和sp一样，在 **Android 设计原则中**，有提到这两个单位，他<u>建议文字的尺寸一律用 **sp** 单位，非文字的尺寸一律使用 **dp** 单位</u>。

> 例如textSize="16sp"、layout_width="60dp"。

为什么要把sp和dp代替px？最简单的原因是他们不会因为ppi的变化而变化，在相同物理尺寸和不同ppi下，他们呈现的高度大小是相同。也就是说更接近物理呈现，而px则不行。

但问题来了，ps或者axure里面没有sp或者dp这个选项啊，怎么办？看到网上有人说用 **pt** 去替换 **px**（pt是物理高度，1in=72pt）。补充一下自己推算的pt转换px的公式，不一定对，可以参考：例如9pt，再96dpi下，那么就是9 * 1/72 * 96 =12px。而在72ppi下，9pt=9px。

###### 我再来做个小小的实验：
1、先了解清楚你笔记本的ppi，比如我的macbook air是11.6英寸，1366 x 768分辨率，那么它的ppi就是135ppi。

2、然后新建一个页面，输入的ppi值就是你电脑的ppi值。我们先来看看不同ppi值在电脑上呈现的字体大小是怎么样的：

![](https://pic4.zhimg.com/80/50bb033af88558f43d43c389c3cd230f_hd.jpg)

我用的都是arial 14点（注：专家指正这里不是px而是pt，点）的字体，但在320ppi、160ppi、135ppi（我自己的）以及标准72ppi下的大小，截然不同。

好，我们再来看看，在电脑上直接截图web页之后对比的效果：

![](https://pic4.zhimg.com/80/22ec6d543857b6d59fcec223494e80b7_hd.jpg)

你会惊讶的发现，只有72ppi是正常的，其他字体都不对了，因为原本的web设计是不用考虑dp、sp或者ppi的，它是直接px作为物理单位的，而点在72ppi下（1pt x 1/72 x 72dpi=1px）是正常显示的。所以我们以前做web的时候根本不用担心自己的设计在别人电脑上看起来会很大或很小。当然其实像firefox是用96dpi，也就是9pt=12px。

但我再截一下用iphone访问web之后的图：

![](https://pic1.zhimg.com/80/8b701dab66c088d89ab848510322b104_hd.jpg)


好吧，这时候，你就发现72ppi是见鬼了，因为这个字体在手机上看到完全地小了，所以做移动设计不要傻乎乎地还用72ppi了，不然你很难判断效果。（当然你也可以借助我之前提到的同屏工具来映像到移动设备上查看效果，但这个其实会很麻烦很麻烦很麻烦...）

但是到底是选160ppi还是135ppi呢？如果选了135ppi那在别人的电脑上会怎么样呢？是不是又要重新调？其实不用，我借用另外一台Retina的macbook pro做了相同的测试，你会发现，其实和屏幕ppi无关，和你在ps里设定的分辨率有关。

![](https://pic1.zhimg.com/80/cb6066e540b447e4b38cefb5584735f8_hd.jpg)

[补充，有位专家指出我的不对，就是在点和px上我搞错了，我又尝试了一下，如果是px的话，不同ppi下字体大小是不变的，而点（pt）的话会有变化。

并且如果是用pt来代替px的话，为了整除方便，那么ppi一定要设置成72的倍数，比如144ppi，上图里面160ppi则会除不尽，所以上图其实160ppi的字体还是和截图字体有些许差异。]

然后有专家提出，iOS下是用pt作为字体单位，而Android是以sp作为字体单位，而且web app还是以px作为字体单位。怎么样让设计和输出单位是一致的？我之前给出的解决方案并不十分严谨易懂，所以我重新编辑了一下。

为了求证移动字号的问题，跑了一圈同事，最后只能暂时得出一些“不一定正确”的结论：

1、字号行业标准几乎没有，不像web一样，宋体12px、14px这样很清楚。我唯一找到的只有Android的设计建议：

![](https://pic4.zhimg.com/80/27b359f4addebd9e7d3298ed1ba5fd97_hd.jpg)

图中原作者还换算了一下在240ppi下对应的px值。

而我问了一圈同事，基本上现在设定字号都是凭感觉做事的。当然你也可以参考Android这个标准。

2、如何在电脑上快速预览高清内容是否排版合理，我想到最简单的一点就是缩放psd，缩放的比例很关键，要达到物理尺寸，首先你得知道你电脑的分辨率，我的分辨率是135ppi，如果要看分辨率是326的iphone上的效果，就缩小到135/326≈41.4%，你就会发现物理尺寸非常接近。可以看看一些排版上的问题。当然你也可以装一些工具来达到更好的效果。

3、怎么和开发沟通你的字体大小？我也没有特别好的办法，就简单分成3块来说：

iOS，你设计的时候字体记得用“点”，然后ps设定分辨率用标准的72ppi即可，因为据同事说，这样下的pt值是准确的，或者说iOS自动会转换这个值。具体也需要大家操作了才知道。而这个分辨率下1pt=1px，我简单换算了一下sp->px->pt的尺寸：

```
12sp=24.45px=24.45pt；
14sp=28.52px=28.52pt；
18sp=36.67px=36.67pt；
22sp=44.88px=44.88pt；
```

但这个小数点实在难受，所以四舍五入取整数，并且为了保证可以整除，那么可以是24pt、28pt、36pt、44pt。

Android，你就用标准sp就好了，当然其他图片等尺寸你可以用dp来表述。
Web app，这个我也找不到答案，因为Web app还会涉及到响应式设计，而且前端会用em去表示字体比例。所以同样，如果你用72ppi分辨率做的话，直接可以把对应的字号告诉开发就好了，当然最好你所用到的字号是倍数关系，最小倍数是0.25，这样用em去做比例的时候会更容易些。比如12px、16px、24px、32px这样。
有关字体字号的研究已经有同事在做，以后有结论了再和大家分享。

[以上都是本人自己瞎弄的，如果正确纯属偶然，所以请那些“傻逼”闭嘴，我欢迎专业上的讨论和交流，但不喜欢人品低下地谩骂。]()

## 更多

https://blog.csdn.net/liangfeng093/article/details/81236255  
https://www.jianshu.com/p/ee3b2b75b180  
https://www.ui.cn/detail/79573.html  

