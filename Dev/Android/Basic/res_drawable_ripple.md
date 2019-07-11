# [控件点击出现波纹效果](https://blog.csdn.net/qq137464739/article/details/78721311)

## android 5.0 +

> 波纹效果，因为只有 android5.0 以上才有效果，所以需要在res下新建 drawable-v21 文件夹

1. 新建 ripple_bg.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<ripple xmlns:android="http://schemas.android.com/apk/res/android"
        android:color="#cfd8dc">  <!-- 波纹的颜色 -->
    <item android:drawable="@drawable/bg_rectangle"/> <!-- 背景色 -->
</ripple>
```

2. 背景 bg_rectangle.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#FFFFFF" />
    <!--shape的很多属性随意设置-->
    <!--<corners android:radius="5dp"/> -->
</shape>
```

3. 调用

```xml
<RelativeLayout
    android:layout_width="match_parent"
    android:background="@drawable/ripple_bg"
    android:layout_height="50dp">

</RelativeLayout>
```

## < android 5.0

> 如果要适配 5.0 以下，还需要在 drawable 文件下建一个同样的 ripple.xml 文件名跑在 5.0 以下机器才不会报错

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <shape android:shape="rectangle">
            <solid android:color="#cfd8dc"/>
        </shape>
    </item>
    <item android:drawable="@color/white" />  <!-- 颜色属性随意 -->
</selector>
```

## ImageView ripple 效果

1. 在 drawable 下新建 scan_image.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<bitmap xmlns:android="http://schemas.android.com/apk/res/android"
        android:src="@mipmap/ic_scan_new" 
        android:tint="#ea0e24"  
        android:tintMode="multiply"> 
</bitmap>
```

2. 创建 selector (scan_selector_bg.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/scan_image" android:state_pressed="true"/>
    <item android:drawable="@mipmap/ic_scan_new"/>
</selector>
```

3. 调用

```xml
<ImageView
    android:src="@drawable/scan_selector_bg"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"/>
```

这样的 ImageView 就自带 selector 效果了，点击的时候就会变色。

## 更多

- https://www.cnblogs.com/taixiang/p/9095464.html
  ![](https://user-gold-cdn.xitu.io/2018/4/8/162a4159ab455fef?w=480&h=384&f=gif&s=1796359)

- https://blog.csdn.net/u014372299/article/details/84238709
  ![](https://img-blog.csdnimg.cn/20181119141105501.gif)