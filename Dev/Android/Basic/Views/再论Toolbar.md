# Toolbar [LINK](https://www.jianshu.com/p/05ef48b777cc)

## 1. 功能分区

<img src="https://upload-images.jianshu.io/upload_images/2477378-c2e81b1df5da058c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/809/format/webp" width="400px" height="auto"/>

Toolbar首先是一个ViewGroup，它是用来做APP的标题栏，其中包括5个部分，分别是  
- a navigation button
- a branded logo image
- a title and subtitle
- one or more custom views
- action menu( an action menu)

## 2. 应用

### 2.1 基础配置

```xml
<android.support.v7.widget.Toolbar
    android:id="@+id/toolbar"
    android:layout_width="match_parent"
    android:layout_height="?attr/actionBarSize"
    android:background="@color/colorPrimary"
    app:logo="@mipmap/ic_launcher"
    app:title="标题"
    app:titleTextColor="#fff"
    app:subtitle="副标题"
    app:subtitleTextColor="#fff"
    app:navigationIcon="@drawable/ic_menu"
    android:theme="@style/Base.Theme.AppCompat.Light"
    app:popupTheme="@style/toolBar_pop_item"
    >
```

这里的属性设置了**导航按钮**、**logo**和**主标题副标题**，属性名称很清楚不多讲，action menu 的设置需要通过代码，自定义 View 放到后面来讲。

```java
mToolbar=findViewById(R.id.toolbar);
//利用Toolbar代替ActionBar
setSupportActionBar(mToolbar);
//设置导航Button点击事件
mToolbar.setNavigationOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        Toast.makeText(MainActivity.this,"点击导航栏",Toast.LENGTH_SHORT).show();
    }
});
```

### 2.2 设置 action menu

```java
//设置移除图片  如果不设置会默认使用系统灰色的图标
mToolbar.setOverflowIcon(getResources().getDrawable(R.drawable.icon_action));
//填充menu
mToolbar.inflateMenu(R.menu.toolbar_menu);
//设置点击事件
mToolbar.setOnMenuItemClickListener(new Toolbar.OnMenuItemClickListener() {
    @Override
    public boolean onMenuItemClick(MenuItem item) {
        switch (item.getItemId()){
            case R.id.action_settings:
                Toast.makeText(MainActivity.this,"action_settings",Toast.LENGTH_SHORT).show();

                break;
            case R.id.action_share:
                Toast.makeText(MainActivity.this,"action_share",Toast.LENGTH_SHORT).show();

                break;
            case R.id.action_search:
                Toast.makeText(MainActivity.this,"action_search",Toast.LENGTH_SHORT).show();

                break;
                default:
                    break;
        }
        return false;
    }
});
```

##### 2.2.1 重写 onCreateOptionsMenu

你发现设置了这一对之后，action menu 依然没有显示出来，因为你还没有重写 **onCreateOptionsMenu**，让 action menu 显示出来。

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.toolbar_menu,menu);
    return true;
}
```
加上这个重写方法以后，action menu就会显示，如同上面的介绍图一样，这个时候有朋友就可能问了，为啥action menu在标题栏上显示这么多图标

<img src="https://upload-images.jianshu.io/upload_images/2477378-720388fff2aa01f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/266/format/webp" width="200px" height="auto"/>

##### R.menu.toolbar_menu
```xml
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    tools:context=".MainActivity">
    <item
        android:id="@+id/action_settings"
        android:orderInCategory="100"
        android:title="测试1"
        android:icon="@drawable/icon_search"
        app:showAsAction="ifRoom"/>
    <item
        android:id="@+id/action_share"
        android:orderInCategory="100"
        android:title="测试2"
        android:icon="@drawable/icon_notify"
        app:showAsAction="ifRoom"/>
    <item
        android:id="@+id/action_search"
        android:orderInCategory="100"
        android:title="设置"
        app:showAsAction="never"/>
    <item
        android:id="@+id/action_search2"
        android:orderInCategory="100"
        android:title="关于"
        app:showAsAction="never"/>
</menu>
```

###### app:showAsAction 属性的作用是来控制 item 在标题栏上展示的形式，一般多取三个值：always、ifRoom以及never。

- lways:总是展示在标题栏上；
- ifRoom如果标题栏上有位置就展示出来；
- never：永不展示标题栏。

##### 溢出图标
点击溢出图标，系统默认的弹出样式是这样的

<img src="https://upload-images.jianshu.io/upload_images/2477378-c695e34e084109fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/781/format/webp" width="400px" height="auto"/>

可以通过

```xml
<android.support.v7.widget.Toolbar
        android:id="@+id/toolbar"
        android:layout_width="match_parent"
        android:layout_height="?attr/actionBarSize"
        android:background="@color/colorPrimary"
        app:logo="@mipmap/ic_launcher"
        app:title="标题"
        app:titleTextColor="#fff"
        app:subtitle="副标题"
        app:subtitleTextColor="#fff"
        app:navigationIcon="@drawable/ic_menu"
        android:theme="@style/Base.Theme.AppCompat.Light"
        app:popupTheme="@style/toolBar_pop_item"
        >
```

app:popupTheme 属性来控制的，在 style 文件里可以设置风格、字体颜色大小等等属性。简单看一下  

###### toolBar_pop_item

```xml
<style name="toolBar_pop_item" parent="Base.Theme.AppCompat.Light">
        <item name="android:textColor">@color/colorAccent</item>
</style>
```

<img src="https://upload-images.jianshu.io/upload_images/2477378-e4f4ca50fa54ed9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/784/format/webp" width="400px" height="auto"/>

## 3. 标题居中问题和自定义 Toolbar

关于标题居中问题，我看很多小伙伴们都提出过，其实解决起来非常的简单，就是利用自定义View。之前文中提到过Toolbar是一个ViewGroup，如果需要添加自定义View，只需要在Toolbar里面增加其子ViewGroup或者子View。

```xml
<android.support.v7.widget.Toolbar
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@color/colorPrimary"
        >

        <RelativeLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:layout_marginLeft="10dp"
            android:layout_marginRight="10dp"
            android:gravity="center_vertical"

            >
            <ImageView
                android:id="@+id/iv_back"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:src="@drawable/ic_back"
                android:layout_centerVertical="true"
                />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:textColor="#fff"
                android:text="标题"
                android:textSize="18sp"
                android:layout_centerHorizontal="true"
                />

               <EditText
                   android:visibility="gone"
                   android:layout_width="match_parent"
                   android:layout_height="wrap_content"
                   android:layout_marginLeft="50dp"
                   android:layout_marginRight="50dp"
                   android:layout_centerHorizontal="true"
                   android:background="@drawable/search_bg"
                   android:drawableLeft="@drawable/icon_search"
                   android:padding="5dp"
                   android:textColorHint="#fff"
                   android:hint="请输入搜索内容"
                   android:gravity="center"
                   android:cursorVisible="false"
                   />
        </RelativeLayout>
    </android.support.v7.widget.Toolbar>
```

通过这种自定义View方式就可以解决标题居中的问题，看一下效果

<img src="https://upload-images.jianshu.io/upload_images/2477378-2b5e2c232a8cd10d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/779/format/webp" width="400px" height="auto"/>

**注意：**这里返回键不要通过Toolbar的导航Button设置，这样会影响标题居中的效果，直接在自定义View里面设置就行了。

有些App用搜索框，其实也是利用自定义View来实现，实现起来也很简单，搜索框在中间跟标题重叠，通过设置可见性来调控，简单看一下效果

<img src="https://upload-images.jianshu.io/upload_images/2477378-5ad1d78e322af8ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/783/format/webp" width="400px" height="auto"/>

## 4 为什么推荐使用 Toolbar

写到这里，肯定会有小伙伴问了，这里使用Toolbar有什么用，我自己写一个 RelativeLayout 或者其他什么布局都能实现，为啥非要用Toolbar呢？

这里说一下，使用Toolbar比起传统的自定义布局的好处。  
- 第一、不需要考虑标题栏和系统状态栏匹配的问题，你自己写还得匹配系统状态栏；
- 第二、就是 Toolbar 可以更好的和其他的MD设计风格的控件组合应用，快速做出比较炫的效果，比如 Toolbar+NestScrollView, Toolbar+DrawerLayout + NavigationView等等；







