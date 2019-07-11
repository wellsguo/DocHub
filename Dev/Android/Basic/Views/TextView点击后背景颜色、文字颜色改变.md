## [TextView点击后背景颜色、文字颜色改变](https://blog.csdn.net/u013278940/article/details/51152655)  

TextView本没有点击效果，故为实现点击后文字颜色改变和背景改变，需要写selector进行点击时颜色的替换。效果图如下：

- 未点击时：字颜色为黑色，背景为系统默认颜色。
- 点击时：字体颜色为绿色，背景色为粉色。

未点击时 | 点击时
-- | --
![](https://img-blog.csdn.net/20160414163926189?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)| ![](https://img-blog.csdn.net/20160414163932895?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

### 布局文件

res/layout/activity_main.xml

```xml
<TextView
        android:layout_width="fill_parent"
        android:layout_height="60dp"
        android:paddingLeft="25dp"
        android:gravity="center_vertical"
        android:text="@string/hello_world" 
        android:textSize="25dp"
        android:textColor="@color/textcolor_selector"
        android:background="@drawable/background_selector"
        android:clickable="true"
        android:focusable="true"/>
```

### 文字颜色

res/color/textcolor_selector.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_focused="true" android:color="@color/green"></item>
    <item android:state_checked="true" android:color="@color/green"></item>
    <item android:state_pressed="true" android:color="@color/green"></item>
    <item android:color="@color/black"/>
</selector>
```

### 背景颜色

res/drawable/background_selector.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android" >
    <item android:state_focused="true" android:drawable="@color/pink"></item>
    <item android:state_checked="true" android:drawable="@color/pink"></item>
    <item android:state_pressed="true" android:drawable="@color/pink"></item>
</selector>
```

### 涉及颜色值

res/values/color.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="white">#ffffffff</color>
    <color name="black">#ff000000</color>
    <color name="pink">#ffffcbd7</color>
    <color name="green">#ffbae4b6</color>
</resources> 
```



