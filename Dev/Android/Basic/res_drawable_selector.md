# selector

作者：MrSeaSky   
来源：CSDN   
原文：https://blog.csdn.net/qq_20451879/article/details/80340823   
版权声明：本文为博主原创文章，转载请附上博文链接！


## 效果展示

![](https://img-blog.csdn.net/20180611194652803?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIwNDUxODc5/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

## 两种创建方式

- （1） 以Xml方式写出状态选择器，然后将我们写好的 selector 状态器存在放 `res/ drawable` 或 `res/color` 文件夹下(较为常用)
- （2） 在代码中动态创建 selector，实现不如前者简单，但胜在灵活，一般用在选择器状态改变频繁的情况下

### 注意

- 设置 bankground的时候，我们的 selector 状态选择器存放在 `res/drawable`  下！！！
- 设置 TextColor 属性的时候，我们的 selector 状态选择器存放在 `res/color`  下！！！

## 状态设置类型

### 常用类型

```java
//设置是否按压状态，一般在true时设置该属性，表示已按压状态，默认为false
android:state_pressed
//设置是否选中状态，true表示已选中，false表示未选中
android:state_selected
//设置是否勾选状态，主要用于CheckBox和RadioButton，true表示已被勾选，false表示未被勾选
android:state_checked
//设置勾选是否可用状态，类似state_enabled，只是state_enabled会影响触摸或点击事件，state_checkable影响勾选事件
android:state_checkable
//设置是否获得焦点状态，true表示获得焦点，默认为false，表示未获得焦点
android:state_focused
//设置触摸或点击事件是否可用状态，一般只在false时设置该属性，表示不可用状态
android:state_enabled
```

### 较少使用类型
```java
//设置当前窗口是否获得焦点状态，true表示获得焦点,false 表示未获得焦点，例如拉下通知栏或弹出对话框时， 当前界面就会失去焦点；另外，ListView的ListItem获得焦点时也会触发true状态，可以理解为当前窗口就是ListItem本身
android:state_window_focused       
//设置是否被激活状态，true表示被激活，false表示未激活，API Level 11及以上才支持，可通过代码调用控件的
android:state_activated             
//方法设置是否激活该控件
setActivated(boolean)
//设置是否鼠标在上面滑动的状态**，true表示鼠标在上面滑动，默认为false，API Level 14及以上才支持
//补充：selector标签下有两个比较有用的属性要说一下，添加了下面两个属性之后，则会在状态改变时出现淡入淡出效果，
//但必须在API Level 11及以上才支持
android:state_hovered     
//状态改变时，旧状态消失时的淡出时间，以毫秒为单位
android:exitFadeDuration      
//状态改变时，新状态展示时的淡入时间，以毫秒为单位
android:enterFadeDuration    
```

## 常用类型示例

### 样式一：点击改变字体颜色 - android:state_pressed（按压状态）

###### selector状态选择器(bg_btn_one (存放 res - color）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:color="@color/colorPrimary" android:state_pressed="true"/>
    <item android:color="@color/colorAccent" />
</selector>
```

###### 应用

```xml
<Button
    android:textColor="@color/bg_btn_one"
    android:layout_width="match_parent"
    android:layout_height="45dp"
    android:text="样式一：点击改变字体颜色"
    android:gravity="center"
    />
```

### 样式二：点击改变背景颜色

###### selector状态选择器(bg_btn_two (存放 res - drawable）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/colorAccent" android:state_pressed="true"/>
    <item android:drawable="@color/colorPrimary" />
</selector>
```

###### 应用

```xml
<Button
    android:background="@drawable/bg_btn_two"
    android:layout_width="match_parent"
    android:layout_height="45dp"
    android:text="样式二：点击改变背景颜色"
    android:gravity="center"
    />
```

### 样式三：改变背景色同时改变字体色

###### selector状态选择器(bg_btn_one (存放 res - color）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:color="@color/colorPrimary" android:state_pressed="true"/>
    <item android:color="@color/colorAccent" />
</selector>
```

###### selector状态选择器(bg_btn_two (存放 res - drawable）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/colorAccent" android:state_pressed="true"/>
    <item android:drawable="@color/colorPrimary" />
</selector>
```


###### 应用

```xml
<Button
    android:background="@drawable/bg_btn_two"
    android:textColor="@color/bg_btn_one"
    android:layout_width="match_parent"
    android:layout_height="45dp"
    android:text="样式三：改变背景色同时改变字体色"
    android:gravity="center"
    />
```


### 样式四： android:state_checked (勾选状态)

###### selector状态选择器(bg_check_three(存放 res - drawable）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/colorPrimary" android:state_checked="true"/>
    <item android:drawable="@color/colorAccent" />
</selector>
``` 

###### 应用

```xml
  <CheckBox
        android:layout_marginTop="20dp"
        android:id="@+id/btn"
        android:background="@drawable/bg_check_three"
        android:layout_width="match_parent"
        android:layout_height="45dp"
        android:text="Checked：点击后背景状态长存"
        android:gravity="center"
        />
```

### 样式五：android:state_focused （焦点状态）

###### selector状态选择器(bg_check_three(存放 res - color）)

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:color="@color/colorPrimary" android:state_focused="true"/>
    <item android:color="@color/colorAccent" />
</selector>
```

###### 应用
```xml
<EditText
    android:textColor="@color/bg_edittext_one"
    android:layout_width="match_parent"
    android:layout_height="45dp"
    android:text="焦点样式：改变背景色同时改变字体色"
    android:gravity="center"
    />
```

## Selector状态选择器 - SelectorUtil

```java
/**
 * 动态设置 点击事件 selector 的工具类  可以从本地添加  也可以从网络添加
 * Created by suwenlai on 16-12-26.
 */
public class SelectorUtil {

    /**
     * 从 drawable 获取图片 id 给 Imageview 添加 selector
     * @param context 调用方法的 Activity
     * @param idNormal 默认图片的 id
     * @param idPress  点击图片的 id
     * @param iv   点击的 view
     */
    public static void addSelectorFromDrawable(Context context , int idNormal, int idPress,ImageView iv){

        StateListDrawable drawable = new StateListDrawable();
        Drawable normal = context.getResources().getDrawable(idNormal);
        Drawable press = context.getResources().getDrawable(idPress);
        drawable.addState(new int[]{android.R.attr.state_pressed},press);
        drawable.addState(new int[]{-android.R.attr.state_pressed},normal);
        iv.setBackgroundDrawable(drawable);
    }

    /**
     * 从 drawable 获取图片 id 给 Button 添加 selector
     * @param context 调用方法的 Activity
     * @param idNormal 默认图片的 id
     * @param idPress  点击图片的 id
     * @param button   点击的 view
     */

    public static void addSelectorFromDrawable(Context context , int idNormal, int idPress,Button button){

        StateListDrawable drawable = new StateListDrawable();
        Drawable normal = context.getResources().getDrawable(idNormal);
        Drawable press = context.getResources().getDrawable(idPress);
        drawable.addState(new int[]{android.R.attr.state_pressed},press);
        drawable.addState(new int[]{-android.R.attr.state_pressed},normal);
        button.setBackgroundDrawable(drawable);
    }

    /**
     * 从网络获取图片 给 ImageView 设置 selector
     *  @param clazz 调用方法的类
     * @param normalUrl 获取默认图片的链接
     * @param pressUrl 获取点击图片的链接
     * @param imageView 点击的 view
     */
    public static void addSeletorFromNet(final Class clazz, final String normalUrl, final String pressUrl, final ImageView imageView){
        new AsyncTask<Void,Void,Drawable>(){

            @Override
            protected Drawable doInBackground(Void... params) {
                StateListDrawable drawable = new StateListDrawable();
                Drawable normal = loadImageFromNet(clazz,normalUrl);
                Drawable press = loadImageFromNet(clazz, pressUrl);
                drawable.addState(new int[]{android.R.attr.state_pressed},press);
                drawable.addState(new int[]{-android.R.attr.state_pressed},normal);
                return drawable;
            }

            @Override
            protected void onPostExecute(Drawable drawable) {
                super.onPostExecute(drawable);
                imageView.setBackgroundDrawable(drawable);
            }
        }.execute();

    }

    /**
     *
     * 从网络获取图片 给 Button 设置 selector
     * @param clazz 调用方法的类
     * @param normalUrl 获取默认图片的链接
     * @param pressUrl 获取点击图片的链接
     * @param button 点击的 view
     */
    public static void addSeletorFromNet(final Class clazz, final String normalUrl, final String pressUrl, final Button button){
        new AsyncTask<Void,Void,Drawable>(){

            @Override
            protected Drawable doInBackground(Void... params) {
                StateListDrawable drawable = new StateListDrawable();
                Drawable normal = loadImageFromNet(clazz,normalUrl);
                Drawable press = loadImageFromNet(clazz, pressUrl);
                drawable.addState(new int[]{android.R.attr.state_pressed},press);
                drawable.addState(new int[]{-android.R.attr.state_pressed},normal);
                return drawable;
            }

            @Override
            protected void onPostExecute(Drawable drawable) {
                super.onPostExecute(drawable);
                button.setBackgroundDrawable(drawable);
            }
        }.execute();

    }

    /**
     * 从网络获取图片
     * @param clazz 调用方法的类
     * @param netUrl 获取图片的链接
     * @return  返回一个 drawable 类型的图片
     */
    private static Drawable loadImageFromNet(Class clazz, String netUrl) {
        Drawable drawable =null;
        try {
            drawable = Drawable.createFromStream(new URL(netUrl).openStream(), "netUrl.jpg");
        } catch (IOException e) {
            MyLog.e(clazz.getName(),e.getMessage());
        }

        return drawable;
    }
}
```

## 最佳实践

>作者：南岸青栀   
来源：CSDN   
原文：https://blog.csdn.net/jiankeufo/article/details/73845750   
版权声明：本文为博主原创文章，转载请附上博文链接！


我们做按钮的时候经常需要用两个图片来实现按钮点击和普通状态的样式，这就需要提供两种图片，而且每个分辨率下还有多套图片，大大增加了apk的大小。

![](http://images0.cnblogs.com/blog2015/651487/201505/150940374709184.png)

我们希望让这两张图片合二为一，而且还能实现两种或者多种状态，怎么做呢？我们首先建立一个圆形的selector，正常情况下是完全透明的，按下后透明度变小。

### 第一种方法（强烈推荐）

#### 原理
selector做遮罩，原图做background。



###### normal_bg_selector.xml


```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:state_pressed="true">
        <shape android:shape="oval">
            <solid android:color="#21000000" />
        </shape>
    </item>

    <item>
        <shape android:shape="oval">
            <solid android:color="#00000000" />
        </shape>
    </item>
</selector>
```
然后只需要问美工拿一张图片就好了，比如这张：

![](http://images0.cnblogs.com/blog2015/651487/201505/150944289238341.png)

关键的一步来了，现在我们需要把selector文件当作遮罩，然后用上面的蓝色icon作为bg，放到一个ImageButton中：

```xml
<ImageButton
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@drawable/normal_bg_selector"
        android:background="@drawable/blue_btn_icon"
        />
```
最后只需要调整下padding就好了，如果你需要矩形的图片，就按照上面的方法建立一个矩形的遮罩即可。如果你们公司用的圆角矩形，直接问设计师要个圆角的标准就行，再建立一个selector文件吧。下面是最简单的原型和矩形的遮罩文件：

###### normal_oval_mask_selector.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:state_pressed="true">
        <shape android:shape="oval">
            <solid android:color="#21000000" />
        </shape>
    </item>

    <item>
        <shape android:shape="oval">
            <solid android:color="#00000000" />
        </shape>
    </item>
</selector>
```

###### normal_rectangle_mask_selector.xml


```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <item android:state_pressed="true">
        <shape android:shape="rectangle">
            <solid android:color="#21000000" />
        </shape>
    </item>

    <item>
        <shape android:shape="rectangle">
            <solid android:color="#00000000" />
        </shape>
    </item>
</selector>
```
 

### 第二种方法（不推荐）

当然我们还有另一种方法来实现这个效果，用的是 `layer-list`。先放一个 selector 做的遮罩，然后在遮罩下面叠加一个 button 的 icon。这样就做好 button 按下后的样式。

###### blue_btn_selector_layerlist.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">    
    <item android:drawable="@drawable/blue_btn_icon" />    
    <item android:drawable="@drawable/blue_btn_mask_shape" />    
</layer-list> 
```

现在我们有了按钮普通的样式和按钮按下的样式，之后就可以建立一个selector：

###### blue_button_bg_selector.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item
        android:state_pressed="true"
        android:drawable="@drawable/blue_btn_selector_layerlist" />

    <item
        android:drawable="@drawable/blue_btn_icon" />
</selector>
```
最后就只需要在 button 的 background 设置这个 blue_button_bg_selector.xml 就行了。

**第二种方法明显就比较繁琐，需要多建立一个文件，没有模块化**。



