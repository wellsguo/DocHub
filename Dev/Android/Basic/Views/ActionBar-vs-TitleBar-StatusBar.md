

## XxxBar

作者：K.I.O   
来源：CSDN   
原文：https://blog.csdn.net/sinat_29675423/article/details/86254222   
版权声明：本文为博主原创文章，转载请附上博文链接！

![actionbar-vs-titlebar-vs-toolbar](https://img-blog.csdnimg.cn/20190110201704714.png)

## StatusBar
即状态栏，它处于屏幕的最顶部，正常情况下它是显示的，它和TitleBar和ActionBar、ToolBar之间没有直接的关系。
可设置隐藏、颜色，获取高度等。

## TitleBar
即标题栏,它紧挨状态栏的下面，正常情况下它的布局和主题样式都是使用系统定义好的，且默认情况下只显示图标和文本。

## ActionBar
ActionBar 是android 3.0的推出的，当时Google 想要逐渐改善过去 android 纷乱的界面设计，希望让终端使用者尽可能在 android 手机有个一致的操作体验。
可设置标题、图标、样式、按钮、menu等。

Action bar被包含在所有的使用Theme.Hole主题的Activity（或者是这些Activity的子类）中。

开发API11以下的程序，首先必须在AndroidManifest.xml中指定Application或Activity的theme是Theme.Holo或其子类，否则将无法使用ActionBar。

### 删除actionbar
- 方法一  
如果不想用ActionBar，那么只要在theme主题后面" .NoActionBar", 就可以了。

- 方法二  
在onCreate方法中添加一句代码: requestWindowFeature(Window.FEATURE_NO_TITLE);   
不过这句代码一定要添加到setContentView(R.layout.activity_main); 之前

- 方法三  
用getActionBar()/getSupportActionBar()得到ActionBar对象，用对象调用hide()方法；  
注意配置清单文件中**最低版本改为11**以上；
```java
public class MainActivity extends Activity {
    ActionBar  actionBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
 
        setContentView(R.layout.activity_main);
        actionBar=getActionBar();
        actionBar.hide();
    }
}
```


## ToolBar
Toolbar 是**android 5.0**的推出的，放在了v7包中作为控件，它是为了**取代actionbar而产生**的.由于ActionBar在各个安卓版本和定制Rom中的效果表现不一，导致严重的碎片化问题，ToolBar应运而生。  
优点：自定义视图的操作更加简单，状态栏的颜色可以调（Android 4.4以上）。
```java
Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
setSupportActionBar(toolbar); // Toolbar即能取代原本的 actionbar
```


### ToolBar详解
- http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2014/1118/2006.html
- https://blog.csdn.net/u012207345/article/details/73065453




