```xml
<Switch
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_alignParentEnd="true"
    android:layout_centerVertical="true"
    android:switchMinWidth="20dp"
    android:thumb="@drawable/thumb"
    android:track="@drawable/track"/>
```

```java
 //点击监听
 mSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {

            if (isChecked) {
                //开
                isDefaultAddress = true;
            } else {
                //关
                isDefaultAddress = false;
            }

        }
    });
 //设置选中
mSwitch.setChecked(true);
```

### \# android:thumb="@drawable/thumb"

```xml
<?xml version="1.0" encoding="utf-8"?><!-- 按钮的选择器，可以设置按钮在不同状态下的时候，按钮不同    的颜色 -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/green_thumb" android:state_checked="true" />
    <item android:drawable="@drawable/gray_thumb" />
</selector>
```

### \# green_thumb.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
android:shape="rectangle" >

    <!-- 高度40 -->
    <size android:height="30dp" android:width="30dp"/>
    <!-- 圆角弧度 20 -->
    <corners android:radius="15dp"/>


    <!-- 变化率 -->
    <gradient
        android:endColor="#eeeeee"
        android:startColor="#eeeeee" />

    <stroke android:width="1dp"
        android:color="#33da33"/>
</shape>
```

### \# green_track.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" >
    <!-- 高度40 -->
    <size android:height="25dp"/>
    <!-- 圆角弧度 20 -->
    <corners android:radius="15dp"/>
    <!-- 变化率 -->
    <gradient
        android:endColor="#33da33"
        android:startColor="#33da33" />
</shape>
```

### \# android:track="@drawable/track"

```xml
<?xml version="1.0" encoding="utf-8"?><!-- 底层下滑条的样式选择器，可控制Switch在不同状态下，底下   下滑条的颜色 -->
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/green_track" android:state_checked="true" />
    <item android:drawable="@drawable/gray_track" />
</selector>
```

### \# track.xml

```xml
 <?xml version="1.0" encoding="utf-8"?>
 <shape xmlns:android="http://schemas.android.com/apk/res/android" >

    <!-- 高度40 -->
    <size android:height="25dp"/>
    <!-- 圆角弧度 20 -->
    <corners android:radius="15dp"/>
    <!-- 变化率 -->
    <gradient
        android:endColor="#33da33"
        android:startColor="#33da33" />
</shape>
```

### \# gray_track.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
android:shape="rectangle" >

    <!-- 高度30   此处设置宽度无效-->
    <size android:height="25dp"/>
    <!-- 圆角弧度 15 -->
    <corners android:radius="15dp"/>


    <!-- 变化率  定义从左到右的颜色不变 -->
    <gradient
        android:endColor="#FFFFFF"
        android:startColor="#FFFFFF" />
</shape>
```
作者：菜鸟考官  
链接：https://www.jianshu.com/p/ec9875fb1b84  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。  
