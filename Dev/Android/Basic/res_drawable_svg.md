## 相关背景
### Why SVG

可缩放矢量图形（英语：Scalable Vector Graphics，SVG）是一种基于可扩展标记语言（XML），用于描述二维矢量图形的图形格式。SVG由W3C制定，是一个开放标准。——摘自维基百科

`.svg`格式相对于`.jpg`、`.png`甚至`.webp`具有较多优势，我认为核心有两点：


- 省时间。图像与分辨率无关，收放自如，适配安卓机坑爹的分辨率真是一劳永逸；

- 省空间。体积小，一般复杂图像也能在数KB搞定，图标更不在话下。

### VectorDrawable
`VectorDrawable` 是 Google从Android 5.0 开始引入的一个新的 Drawable 子类，能够加载矢量图。到现在通过 support-library 已经至少能适配到 `Android 4.0`了（通过AppBrain统计的Android版本分布来看，Android 4.1以下（api\<15）几乎可以不考虑了）。Android 中的 VectorDrawable 只支持 SVG 的**部分属性**，相当于阉割版。

它虽然是个类，但是一般通过配置 xml 再设置到要使用的控件上。在 Android 工程中，在资源文件夹 `res/drawable/` 的目录下（没有则需新建），通过`<vector></vector>`标签描述，例如

###### svg_ic_arrow_right.xml

```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
        android:width="8dp"
        android:height="8dp"
        android:viewportHeight="24.0"
        android:viewportWidth="24.0">
    <path
        android:fillColor="#ffffff"
        android:pathData="M12,4l-1.41,1.41L16.17,11H4v2h12.17l-5.58,5.59L12,20l8,-8z"/>
</vector>
```

#### 基本属性说明



- width, height：图片的宽高。可手动修改到需要尺寸；

- viewportHeight, viewportWidth：对应将上面 height width 等分的份数。以 svg_ic_arrow_right.xml 举例，可以想象将长宽都为8dp的正方形均分为24x24的网格，在这个网格中就可以很方便地描述点的坐标，图像就是这些点连接起来构成的。

- fillColor：填充颜色。最好直接在这里写明色值 #xxxxxxxx，而**不要用 `@color/some_color` **的形式，避免某些5.0以下机型可能会报错。

- pathData：在2中描述的网格中作画的路径。具体语法不是本文的重点，故不展开。

这段代码描述出来的是一个白色箭头，可以从Android Studio的preview功能栏里预览到它的样子：





> vector preview

<img src="https://upload-images.jianshu.io/upload_images/2913031-3c87ae40b9ee0e51.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/959/format/webp" width="600px" height="auto" />


## 获取矢量图

### 方式一：iconfont


<img src="https://upload-images.jianshu.io/upload_images/2913031-a955de416b8908e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/957/format/webp" width="600px" height="auto" />

可以对图标属性进行编辑，如色值和大小（单位dp），然后点按钮“SVG下载”。下载成功后在下载目录找到一个 `.svg` 格式的文件，我的是：





<img src="https://upload-images.jianshu.io/upload_images/2913031-0ded4452ebcbe2eb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/76/format/webp" width="60px" height="auto" />


这个文件可以用浏览器打开->查看网页源码，或者用NotePad++等编辑器打开看到里面的内容，格式化后是这样：

```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg t="1490517024583" class="icon" style="" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1010" xmlns:xlink="http://www.w3.org/1999/xlink" width="16" height="16">
    <defs>
        <style type="text/css"></style>
    </defs>
    <path d="M288.86749 12.482601C272.260723-4.160867 245.369563-4.160867 228.720647 12.482601 212.15603 29.126068 212.15603 56.438425 228.720647 73.081892L704.289552 511.786622 228.720647 950.918109C212.15603 967.561574 212.15603 994.447175 228.720647 1011.517401 245.369563 1028.160866 272.260723 1028.160866 288.86749 1011.517401L794.952385 544.646802C803.803707 535.684935 807.597131 523.735776 807.007043 511.786622 807.597131 500.264224 803.803707 488.315065 794.952385 479.353198L288.86749 12.482601Z" p-id="1011"></path>
</svg>
```

问题是，文件里好多标签Android是不认识的。不过没关系，有三种解决办法：

  - (1) 大招。先放大招，大招之下，后两种可以自动忽略。经大神[@天之界线2010](https://www.jianshu.com/u/denPHP)在评论区力荐的 [svgtoandroid](https://github.com/misakuo/svgtoandroid) 插件，用过之后果然神清气爽。安装：`File -> Setting -> Plugins -> Browser repositories -> 搜“svg2VectorDrawable” -> 安装并重启Android Studio`，再次进来后顶部工具栏会多一个图标：  
<img src="https://upload-images.jianshu.io/upload_images/2913031-3a123eaa9d0a631d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/130/format/webp" width="100px" height="auto" />  
点击图标弹出对话框：  
<img src="https://upload-images.jianshu.io/upload_images/2913031-cf7218bb5aec9e03.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/596/format/webp" width="600px" height="auto" />  
勾选Batch选项，将对被选中文件夹中的.svg文件进行批量转换。nodpi会自动添加到没有后缀的drawable文件夹中。   
网上下载的svg资源往往一步到位，有个这个插件将会事半功倍。导入第一个svg文件时就命名成我们想要的名字，如果不满意再导入时无需再关注命名，将后面导入的pathData覆盖第一个观察效果，直到满意后删除不需要的文件。


   - (2) 手动。新建一个<vector></vector>标签的xml文件，通过观察文件内容，很容易获取到关键信息。width height自然对应<vector/>中宽高，viewBox后两位数字是分别对应<vector/>中的viewportWidth和viewportHeight，往下<path/>中的d的数据的对应<vector/>中<path/>中的pathData。fillColor自己手动设置。
   
   - (3) 自动。Android Studio大发神威的时候到了。  
<img src="https://upload-images.jianshu.io/upload_images/2913031-78db817e07dc6af7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/638/format/webp" width="600px" height="auto" />  
鼠标选中drawable文件夹，右键， New， Vector Asset， Local file，然后出现：  
<img src="https://upload-images.jianshu.io/upload_images/2913031-dec7f6b85ac61946.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/716/format/webp" width="600px" height="auto" />  
先选本地文件（还能支持PSD，强吧），再到磁盘中找到之前下载的.svg矢量图。导入后可以为文件重命名（建议用svg\_或者有区别于其它格式的前缀），默认导入宽高均为24dp，选中Override框则读取文件本来宽高，其它配置视需求而定。点击Next到下一页最后点Finish就导入了。自动导入需要格式化一下就是前面svg_ic_arrow_right.xml的样子了。  
海搜比较耗时间，线条粗细啦，位置没居中啦，大小不搭配啦，关键是这些问题都是导入项目或者运行到手机后才能发现（非强迫症当我没说）。
iconfont还有诸多成套的图标库，优点是风格大小一致，或者多彩图标。

### 方式二：Android Studio 的 Material Icon 入口
鼠标选中drawable文件夹，右键， New， Vector Asset，然后出现：




<img src="https://upload-images.jianshu.io/upload_images/2913031-51b7e24cdb5f1271.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/716/format/webp" width="600px" height="auto" />


点击机器人进入搜索筛选：



<img src="https://upload-images.jianshu.io/upload_images/2913031-0e25d9d42da7bc1d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/737/format/webp" width="600px" height="auto" />




左侧的搜索和分类可以快速索引。这里应该都是由谷歌官方制作的MD标准图标，建议先到这里搜索，如果没有再到网上搜索。

### 方式三：用软件或工具导出
对本人来说，方式一基本可以搞定一个App了。但如果以上两种方式均不能满足你的需求，下面祭出求矢量图三式：

- 求美工。有好吃的出好吃的，有美色的出美色（诶？），据说PS+AI就能分分钟导出SVG（我试了怎么不行呢，姿势不对？）。

- 求自己。自学作画技能，到这种[在线制作SVG的网站](https://svg-edit.github.io/svgedit/releases/svg-edit-2.8.1/svg-editor.html)自己画去（不开玩笑，技多不压身啊）。

- 求 **Vector Magic**。这是一个黑科技软件，可以读取.png或.jpg的路径，进而转化为SVG，用过一次，还原度还不错（支持正版，请不要点击任何带“破解”关键字的链接[正经脸]）。


## 项目应用

### 应用准备

#### (1) 项目的 `build.gradle` 配置有

```groovy
android{
  ...
  defaultConfig {
    ...
    vectorDrawables.useSupportLibrary = true
   }
  ...
}
dependencies {
  ...
  compile "com.android.support:appcompat-v7:21+" // 至少Api21
  ...
}
```
#### (2) 项目的 Activity 中都包含（通用做法是在BaseActivity中加）

```java
static {
  AppCompatDelegate.setCompatVectorFromResourcesEnabled(true);
}
```

### AppCompatImageView

这是继承自 ImageView 用于 5.0 以下加载矢量图的控件，只需要替换 src 为 `srcCompat` 属性，其它没什么不同。例如：

```xml
<android.support.v7.widget.AppCompatImageView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    app:srcCompat="@drawable/svg_ic_arrow_right"/>
```


- 如果你的 Activity 直接或间接继承自 AppCompatActivity，当前视图中的 ImageView 在编译过程中会被自动转为 AppCompatImageView（support包中所有含有AppCompat前缀的控件均受相同处理），因而在Activity 中通过 findViewById()的实例用 ImageView 或 AppCompatActivity 接收是没有区别的。



- 用以上条件的 Activity 中装载的 Fragment，或者通过动态注入（如Dialog的contentView）的ImageView，均将被自动转为AppCompatActivity。

- 从xml文件中初始化ImageView并加载矢量图，必须使用AppCompatImageView的srcCompat属性。

- ImageView的染色属性tint同样适合矢量图。

### TextView
在我的经验中，TextView可以用到矢量图的场景是最多的，主要是设置CompoundDrawable。例如：

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:drawableRight="@drawable/svg_ic_arrow_right"
    android:drawablePadding="4dp"
    android:text="drawable right"/>
```    

这样设置后，没有任何不适，编译器也不报错，可能你自己运行也没问题。但是！这才是深坑啊。5.0以下某些机型可能会崩溃的。

AppCompatTextView是没有对CompoundDrawable进行适配的，所以需要自己动手才能丰衣足食。简单原理是，判断系统版本如果小于5.0，就用ContextCompat.getDrawable获取到Drawable实例，再setCompoundDrawablesWithIntrinsicBounds。

这个部分本人已经做好并开源了，地址：[VectorCompatTextView](https://github.com/woxingxiao/VectorCompatTextView)，轻松compile到项目中使用。还特意添加了一个实用功能——`tint`染色——可以选择是否让图标与文字颜色一样，这样就不必关心xml里的`fillColor`属性了。用例：

```xml
<com.xw.repo.VectorCompatTextView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:background="@color/color_gray_light"
    android:gravity="center_vertical"
    android:padding="16dp"
    android:text="Next"
    android:textSize="16sp"
    app:drawableRightCompat="@drawable/svg_ic_arrow_right"
    app:tintDrawableInTextColor="true"/>
```

> 效果

<img src="https://upload-images.jianshu.io/upload_images/2913031-30464f5e2ba0fc79.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/512/format/webp" width="400px" height="auto" />






### MenuItem
MenuItem就是在res/menu/目录下通过xml配置的菜单，适用于NavigationView的menu属性和Activity中onCreateOptionsMenu()注入的选项菜单。

前一阵做了一个小应用叫“简影讯”，发现MenuItem是可以完美支持矢量图的，而且也可以自动跟随文字颜色改变颜色。且看证明：




<img src="https://upload-images.jianshu.io/upload_images/2913031-53a81f375a62a483.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/773/format/webp" width="600px" height="auto" />







> 自适应颜色

<img src="https://upload-images.jianshu.io/upload_images/2913031-883d7d3775fb985a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/900/format/webp" width="600px" height="auto" />

简影讯（[GracefulMovies](https://github.com/woxingxiao/GracefulMovies)），是一枚基于Retrofit+RxJava+MVP+Colorful多彩主题框架开发的高颜值影讯app。简约，优雅，精彩，即看即走。欢迎在应用宝或360手机助手下载围观。
该项目除ic_launcher外，所有的图标都是矢量图。
“是时候全面使用矢量图了。”

### VectorDrawable 转 Bitmap
自定义View中也可以自由使用矢量图。
首先需要将VectorDrawable 转为 Bitmap，看码：

```java
public Bitmap getBitmapFromVectorDrawable(Context context, int drawableId) {
        Drawable drawable = ContextCompat.getDrawable(context, drawableId);
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
            drawable = (DrawableCompat.wrap(drawable)).mutate();
        }

        Bitmap bitmap = Bitmap.createBitmap(drawable.getIntrinsicWidth(), drawable.getIntrinsicHeight(),
                Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight());
        drawable.draw(canvas);

        return bitmap;
    }
```
执行以上方法获得一个Bitmap的实例（设为mVectorBitmap），然后再在ondraw()里根据你的需求画出bitmap：

```
@Override
 protected void onDraw(Canvas canvas) {
    super.onDraw(canvas);
     ///
     canvas.drawBitmap(mVectorBitmap, left, top, paint);
     ///
}
```

## 后记
矢量图的优点一大把，但也不是万能的。矢量图特别适合 `icon图标` 的应用场景，但是不能用于比如加载相册时，设置的 `placeholder` 或者 `error` 这类需要频繁切换回收的应用场景，否则会造成非常明显的卡顿，因为矢量图是不被硬件加速支持的。

Android 5.0 推出已经有些年份了，也不知道 Android 开发圈对矢量图的使用情况，但知道比如微信这些大厂早已全面推广使用。然而在本人周边似乎自己算先驱了，所以才有了把过程中的一些经验总结分享出来的想法。
毕竟本人才疏学浅，难免有纰漏之处，请大神轻拍砖，并不吝赐教。若对后来学习者有帮助，那花这一天码的字自然也超值了，希望共勉。


## 出处
作者：woxingxiao  
链接：https://www.jianshu.com/p/0555b8c1d26a  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

----

 

[放荡不羁SVG讲解与实战——Android高级UI](https://juejin.im/post/5ca9f65e6fb9a05e472b9cab?utm_source=gold_browser_extension)

<img src="https://user-gold-cdn.xitu.io/2019/4/7/169f7ea756869a23?imageslim" width="300px" height="auto" />
<img src="https://user-gold-cdn.xitu.io/2019/4/7/169f7ea756c73955?imageslim" width="300px" height="auto" />

## 出处

作者：猛猛的小盆友  
链接：https://juejin.im/post/5ca9f65e6fb9a05e472b9cab  
来源：掘金  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。 