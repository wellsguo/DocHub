## Android StatusBar设置 [LINK](https://blog.csdn.net/u011486491/article/details/81869780)

自 4.4 版本（API 19）以后，Android 系统开始支持状态栏的定制，并被纳入 Android 设计规范当中。

### 1. statusBar 的颜色设置


#### 1.1 通过 theme 实质对应的颜色

```xml
<!-- 设置status的颜色 -->
<item name="android:statusBarColor">@android:color/transparent</item>
<!-- true: status栏的图标和文字为黑色；
     false: status栏的图标和文字为白色  -->
<item name="android:windowLightStatusBar">true</item>
<!-- true: status栏会有一层阴影；
     false: status栏没有阴影;当该项为true时，则name="android:windowLightStatusBar"设置无效，永远为白色 -->
<item name="android:windowTranslucentStatus">false</item>
```

#### 1.2 通过代码设置 statusBar 颜色

```java
// 设置颜色
getWindow().setStatusBarColor(Color.TRANSPARENT);
// 设置文字是否黑色
View decorView = getWindow().getDecorView();
int option = View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
decorView.setSystemUiVisibility(option);
```

### 2. statusBar 的显示与隐藏

```java
View decorView = getWindow().getDecorView(); 
int option = View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN; decorView.setSystemUiVisibility(option);
```

### 3. 其他

decorView.setSystemUiVisibility(option)涉及到的设置：

- SYSTEM_UI_FLAG_LOW_PROFILE  
设置状态栏和导航栏中的图标变小，变模糊或者弱化其效果。这个标志一般用于游戏，电子书，视频，或者不需要去分散用户注意力的应用软件。

- SYSTEM_UI_FLAG_HIDE_NAVIGATION  
隐藏导航栏，点击屏幕任意区域，导航栏将重新出现，并且不会自动消失。

- SYSTEM_UI_FLAG_FULLSCREEN  
隐藏状态栏，点击屏幕区域不会出现，需要从状态栏位置下拉才会出现。

- SYSTEM_UI_FLAG_LAYOUT_STABLE  
稳定布局，主要是在全屏和非全屏切换时，布局不要有大的变化。一般和View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN、View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION搭配使用。同时，android:fitsSystemWindows要设置为true。

- SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION  
将布局内容拓展到导航栏的后面。

- SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN  
将布局内容拓展到状态的后面。

- SYSTEM_UI_FLAG_IMMERSIVE  
使状态栏和导航栏真正的进入沉浸模式,即全屏模式，如果没有设置这个标志，设置全屏时，我们点击屏幕的任意位置，就会恢复为正常模式。所以，View.SYSTEM_UI_FLAG_IMMERSIVE都是配合View.SYSTEM_UI_FLAG_FULLSCREEN和View.SYSTEM_UI_FLAG_HIDE_NAVIGATION一起使用的。

- SYSTEM_UI_FLAG_IMMERSIVE_STICKY  
它的效果跟View.SYSTEM_UI_FLAG_IMMERSIVE一样。但是，它在全屏模式下，用户上下拉状态栏或者导航栏时，这些系统栏只是以半透明的状态显示出来，并且在一定时间后会自动消息。

## 终于搞懂令人迷惑的 StatusBar 了 [LINK](https://blog.csdn.net/coderder/article/details/78294777)


随着Android版本的迭代，开发者对状态栏等控件有了更多的控制， google 一直在尝试引入新的Api来满足开发者的需求，但 Api 却一直不够完美，接口添加了很多，却都不够简单或者说完美，算上第三方厂商的特色行为，怎一个“乱”字了得。

### 1 效果
当前主流（2017）Android app StatusBar 效果有以下几种：


- Material Design 风格，状态栏颜色比 toolbar 颜色略深。google 全家桶主要采用这个方式。
- 与 DrawerLayout 结合使用，抽屉划出后，状态栏添加一个半透明蒙层，抽屉位于蒙层和原状态栏之间。 google 全家桶采用。
- 与 toolbar 同色，大部分国内 app 使用。
- 大黑边 国内少部分 app，5.0以下大部分app都是这个效果。
- 隐藏状态栏，导航栏，滑动时出现。欢迎，登录，全屏视频播放等界面使用。
- 渐变效果，少部分app使用
- 状态栏字体默认为白色，部分 app 修改为黑色
- 图片延伸到状态栏
  
### 2. 相关 API

与状态栏相关的 Api 主要有以下几个：

#### 2.1. 远古时期 API1

```java
// 全屏布局且隐藏状态栏：
//4.4 上，顶部下滑，出现半透明状态栏，过一会儿状态栏消失
//4.1 上，顶部下滑，没反应
getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
 
// 全屏布局，不隐藏状态栏（可能已失效）：
//实测 Support libaray 26.1.0 下（使用 support 库中的主题和 AppCompatActivity）,未见状态栏。
getWindow().addFlags(WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN 
| WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);
```

#### 2.2. Android 3.0
在Android3.0中，View添加了一个重要的方法：View.setSystemUiVisibility(int)，用于控制一些窗口装饰元素的显示，并添加了

- View.STATUS_BAR_VISIBLE
- View.STATUS_BAR_HIDDEN ：实测statusbar不会消失，仅隐藏statusbar 部分内容

两个 Flag 用于控制 Status Bar 的显示与隐藏。

> 一般是这么用的

```java
View decorView = getWindow().getDecorView();
int uiOptions =  View.STATUS_BAR_VISIBLE;
decorView.setSystemUiVisibility(uiOptions);
```

#### 2.3. Android 4.0

- View.STATUS_BAR_VISIBLE 改为 View.SYSTEM_UI_FLAG_VISIBLE，
- View.STATUS_BAR_HIDDEN 更名为 View.SYSTEM_UI_FLAG_LOW_PROFILE,该 flag 同时影响 StatusBar 和 NavigationBar ,但并不会使得 SystemUI 消失，而只会使得背景很浅，并且去掉 SystemUI 的一些图标或文字。
- 添加了一个flag:SYSTEM_UI_FLAG_HIDE_NAVIGATION,会隐藏NavigationBar,但是由于NavigationBar是非常重要的，因此只要有用户交互（例如点击一个 button），系统就会清除这个flag使NavigationBar就会再次出现。

#### 2.4. Android 4.1

- View.SYSTEM_UI_FLAG_FULLSCREEN: 这个标志与WindowManager.LayoutParams.FLAG_FULLSCREEN作用相同(全屏布局且隐藏状态栏)
  - 4.1 上顶部下滑没反应
  - 4.4 上顶部下滑从新出现状态栏，且挤压 Activity 的布局。
- View.SYSTEM_UI_FLAG_LAYOUT_STABLE: 与其它flag配合使用，防止系统栏隐藏时内容区域发生变化。
- View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN: Activity全屏显示，但状态栏不会被隐藏覆盖，状态栏依然可见，Activity顶端布局部分会被状态遮住
- View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION: 使内容布局到NavigationBar之下。

#### 2.5. Android 4.4

- View.SYSTEM_UI_FLAG_IMMERSIVE
- View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
  - View.SYSTEM_UI_FLAG_IMMERSIVE 和 SYSTEM_UI_FLAG_HIDE_NAVIGATION 搭配使用，使用 SYSTEM_UI_FLAG_HIDE_NAVIGATION 后，导航栏消失，当用户交互时（例如点击一个 button），导航栏又会出现，添加 View.SYSTEM_UI_FLAG_IMMERSIVE 后，交互时导航栏不会出现，但是会底部滑动导航栏仍会出现。
  - View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY 和 View.SYSTEM_UI_FLAG_FULLSCREEN 配合使用：状态栏半透明，顶部向下滑动出现，过一段时间消失。
  - View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY 和 SYSTEM_UI_FLAG_HIDE_NAVIGATION 配合使用：导航栏半透明，交互时，导航栏不出现，底部向上滑动出现，过一段时间消失。
- FLAG_TRANSLUCENT_STATUS  
当使用这个flag时SYSTEM_UI_FLAG_LAYOUT_STABLE和SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN会被自动添加,同时，设置FLAG_TRANSLUCENT_STATUS也会影响到StatusBar的背景色，但并没有固定的表现：
  - 对于7.0以上的机型，设置此flage会使得StatusBar半透明
  - 对于6.0以上的机型，设置此flage会使得StatusBar完全透明
  - 对于5.x的机型，大部分是使背景色半透明，小米和魅族以及其它少数机型会全透明
  - 对于4.4的机型，小米和魅族是透明色，而其它系统上就只是黑色到透明色的渐变。
  - google 你到底要闹哪样？

- FLAG_TRANSLUCENT_NAVIGATION  
当使用这这个个flag时SYSTEM_UI_FLAG_LAYOUT_STABLE和SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION会被自动添加。同时，设置FLAG_TRANSLUCENT_STATUS也会影响到 NavigationBar 的背景色,效果与 FLAG_TRANSLUCENT_STATUS 相同

#### 2.6. Android 5.0
- 主题里通过 colorPrimaryDark 来指定 StatusBar 背景色
- 可以调用 window.setStatusBarColor(@ColorInt int color) 来修改状态栏颜色,但是让这个方法生效有一个前提条件：你必须给window添加FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS并且取消FLAG_TRANSLUCENT_STATUS

#### 2.7 Android 6.0

在 Android6 以后，我们只要给 SystemUI 加上 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR 这个flag，就可以让字体和图标变为黑色。

#### 2.8、fitSystemWindows

在布局内容延伸到状态栏和导航栏时，我们可以给 View 设置 fitSystemWindows 属性，它是一个 boolean 值，可以在xml里直接设置android:fitsSystemWindows="true",也可以通过View#setFitsSystemWindows(boolean fitSystemWindows)在java代码中设置。设置后，空调会调整自己的 padding 用于避开系统控件。

> 工作原理

Android系统组件例如状态栏、NavBar、键盘所占据的空间称为界面的WindowInsets,Android系统会在特定的时机从根View派发WindowInsets(深度优先)。一旦有一个View 的 fitSystemWindows 设置为 true，它就会根据WindowInsets来调整自己的 padding,并消耗WindowInsets，不在向下分发 WindowInsets,那么WindowInsets的派发过程就结束了。

**需要注意的是:**

- fitSystemWindows 设置为 true,会让 View 原本的 padding 失效。
- 可以覆写 View 的 onApplyWindowInsets(WindowInsets insets) 方法来自己处理 WindowInsets。
- dispatchApplyWindowInsets 方法可以继续传递 WindowInsets.

### 3 实现

#### 3.1. Material Design 风格

采用这个效果的应用主要是 Material Design 设计风格的 App，表现形式为：

- Android 5.0+,状态栏颜色略深与 toolbar,颜色值可以来这里找
- Android 5.0以下，状态栏变现为大黑边

> 实现这样的风格很简单

如果状态栏颜色不变，可以直接在主题（5.0 style）中定义：

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <!-- 默认使用 colorPrimaryDark 做状态栏颜色 -->
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
         <!-- 如果使用了下面两个属性，状态栏颜色变为android:statusBarColor，colorPrimaryDark 被覆盖 -->
        <item name="android:windowDrawsSystemBarBackgrounds">true</item>
        <item name="android:statusBarColor">@android:color/transparent</item>
    </style>
</resources>
```

**需要注意的是：**

`<item name="android:windowDrawsSystemBarBackgrounds">true</item>`
和
`<item name="android:windowTranslucentStatus">true</item>`
不能同时设置为 true，否则设置的颜色失效。

如果状态栏颜色在运行过程中需要变化：

```java
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
    window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
    window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
    window.setStatusBarColor(color); 
}
```

#### 3.2. Toolbar 同色

效果和 Material Design 风格类似，设置方法和 Material Design 风格相同。

#### 3.3. 侧边栏

效果：

- 5.0+：抽屉划出后，状态栏添加一个半透明蒙层，抽屉位于蒙层和原状态栏之间。
- 5.0-：状态栏为大黑边，不参与交互。

曾经，想做个 material design 风格的侧边栏效果，那是相当的复杂，可以看看[这篇](http://www.jianshu.com/p/aca4fd6743b1)文章，现在（support 库最新版本 26.1.0）,给 DrawerLayout 设置 fitSystemWindows 为 true，系统就帮你把所有的事办好了，当然包括了老版本的兼容（google 大法好）。

#### 3.4. 渐变效果

效果：

- 5.0+：渐变
- 5.0-：大黑边

> 实现

##### (1) 状态栏设置为透明

v21 的style

```java
<item name="android:windowDrawsSystemBarBackgrounds">true</item>
<item name="android:statusBarColor">@android:color/transparent</item>
```

或者

```java
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
    getWindow().clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
    getWindow().addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
    getWindow().setStatusBarColor(getResources().getColor(android.R.color.transparent));
}
```

##### (2) 设置从状态栏开始布局

```java
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
    View decorView = getWindow().getDecorView();
    int uiOptions = View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN;
    decorView.setSystemUiVisibility(uiOptions);
 }
```

##### (3) 修改布局
不同版本设置不同的布局（代码，xml 均可）  

- 5.0+：在布局顶部加上有渐变效果背景的 View，渐变效果可以使用 shape 实现。
- 5.0-：正常布局。

#### 3.5. 隐藏状态栏，导航栏，滑动时出现

欢迎，登录，全屏视频播放等界面可能会使用这样的效果。

> 常见的效果有：

- 视频全屏播放

  - 4.4+：全屏布局，状态栏，导航栏消失，一般交互时不出现，滑动顶部或底部时出现，过一段时间消失。
```java
getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
```

  - 4.0+：这个版本就不要指望隐藏导航栏了（这个版本一交互，导航栏必然要出现），状态栏消失，顶部滑动导航栏不出现。
```java
getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
```

- 全屏欢迎页面

  - 4.4+：全屏布局，状态栏，导航栏消失，一般交互时不出现，滑动顶部或底部时出现且状态栏导航栏均为半透明，过一段时间消失。
```java
getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
```
  - 4.0+：导航栏，状态栏消失。欢迎页没有交互，导航栏不会因为交互出现。
```java
getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_HIDE_NAVIGATION);
```

- 类似qq的登录页面

  - 4.4+：全屏布局，状态栏消失，滑动顶部时出现，过一段时间消失。
```java
getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
```
  - 4.0+：状态栏消失，顶部滑动导航栏不出现。
```java
getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
```

#### 3.6. 状态栏字体修改为黑色

一般这么干的都是将状态栏设计为浅色的。因为仅 6.0+ 和 小米 魅族支持修改状态栏颜色。5.0 版本会因为浅色状态栏看不清状态栏信息。最好还是让设计改设计稿吧！非要这么做的话，就只有为 5.0 单独设计了，适配 5.0-， 5.0+， 6.0+，这酸爽。

#### 3.7. 图片延伸到状态栏

同渐变效果，仅最后一步将添加渐变 view 改为 添加 ImageView 即可。

**注意**   
github 有一些很火热的库，使用了 FLAG_TRANSLUCENT_STATUS 特性，将状态栏适配到了 4.4，上文已指出 FLAG_TRANSLUCENT_STATUS 在不同平台显示效果存在差异，不能保证较为一致的视觉效果，所以状态栏要玩出花样最合适的版本是 5.0+， 5.0- 统一大黑边就可以了。

#### 参考资料

- [Android 沉浸状态栏](http://www.jianshu.com/p/aca4fd6743b1)
- [Android沉浸式状态栏必知必会](http://blog.cgsdream.org/2017/03/16/android-translcent-statusbar/)
- [Material Design 之 侧边栏与 Status Bar 不得不说的故事](http://www.jianshu.com/p/ab937c80ed6e)