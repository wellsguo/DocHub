
## [LinearLayout 分割线](https://blog.csdn.net/bingshushu/article/details/51444206)

- divider
```xml
android:divider = ""
```
divider 可以是图片文件，也可以是 xml 绘制的 shape。  
使用shape的时候一定要添加`<size>` ，一定要添加 `color`，即使是透明也要写上。  
例如：
```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/black" />
    <size android:height="1px" />
</shape>
```

- showDividers
```xml
android:showDividers = "middle|end|beginning|none"
```
  - middle 在每一项中间添加分割线
  - end 在整体的最后一项添加分割线
  - beginning 在整体的最上方添加分割线
  - none 无

添加上这两个属性就可以实现图中效果。 




#### Android 3.0+
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:divider="@drawable/divider"
    android:showDividers="middle"></LinearLayout>
```

#### Android 3.0- 兼容性处理
```xml
<android.support.v7.widget.LinearLayoutCompat xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    app:divider="@drawable/divider"
    app:showDividers="middle"></android.support.v7.widget.LinearLayoutCompat>
```
### 野路子 (一)
在每一项中间添加一个View，设置view的宽高，和背景。(不推荐，浪费资源)

### 野路子 (二)
给每一项添加带有下划线的背景。(不推荐，麻烦)
