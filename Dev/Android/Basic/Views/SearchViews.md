
#### [MaterialDesignDemo](https://github.com/GitLqr/MaterialDesignDemo)[[1]](https://www.jianshu.com/p/7c1e78e91506) 
![](https://upload-images.jianshu.io/upload_images/4050443-f5a2893cfbdb56ac.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/329/format/webp)


## 如何修改已有控件的显示效果和功能

### 修改控件的显示布局

最简单的当然是通过 style 样式来改变控件的显示效果。如果不能则需要考虑通过代码的方式来实现，
如果控件 ***通过xml布局文件*** 来实现的，那么可以通过 `SearchView.findViewById()` 的方式得到其中的部分或所有的控件；如果是通过 ***代码动态添加*** 的话，那么可以通过 ***反射的方式*** 得到我们需要的控件，进而对控件进行样式设置。
## 使用场景

SearchView 可以单独使用也可配合 menu + toolbar 一起使用。

## 常规使用

### 快速入门


###### menu.xml
``` xml
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:app="http://schemas.android.com/apk/res-auto"
      xmlns:tools="http://schemas.android.com/tools">
    <item
        android:id="@+id/menu_search"
        android:orderInCategory="100"
        android:title="搜索"
        app:actionViewClass="android.support.v7.widget.SearchView"
        app:showAsAction="always"
        />
    ...
</menu>
```

###### Activity / Fragment
```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.search_view, menu);
    MenuItem searchItem = menu.findItem(R.id.menu_search);
    //通过MenuItem得到SearchView
    mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
    ...
    return super.onCreateOptionsMenu(menu);
}
```

### SearchView 设置

#### 默认展开搜索框

- 左侧有放大镜(在搜索框中), 右侧有叉叉, 可以关闭搜索框
```java
mSearchView.setIconified(false);
```



- 左侧有放大镜(在搜索框外),右侧无叉叉,有输入内容后有叉叉, 不能关闭搜索框
```java
mSearchView.setIconifiedByDefault(false);
```


- 左侧有无放大镜(在搜索框中), 右侧无叉叉,有输入内容后有叉叉,不能关闭搜索框
```java
mSearchView.onActionViewExpanded();
```

mSearchView.setIconified(false); | mSearchView.setIconifiedByDefault(false);| mSearchView.onActionViewExpanded();
-- | -- | -- 
![](https://upload-images.jianshu.io/upload_images/4050443-f147d75f2c1f2fca.gif?imageMogr2/auto-orient/strip\|imageView2/2/w/329/format/webp) | ![](https://upload-images.jianshu.io/upload_images/4050443-37322f765d8d61d8.gif?imageMogr2/auto-orient/strip\|imageView2/2/w/329/format/webp)  | ![](https://upload-images.jianshu.io/upload_images/4050443-f91bf4253eb0d7d3.gif?imageMogr2/auto-orient/strip\|imageView2/2/w/329/format/webp) 

#### 其它设置

```java
//设置最大宽度
mSearchView.setMaxWidth(500);
//设置是否显示搜索框展开时的提交按钮
mSearchView.setSubmitButtonEnabled(true);
//设置输入框提示语
mSearchView.setQueryHint("hint");
```

#### 监听事件设置

## 仿旧版网易云音乐搜索框

### code

https://github.com/GitLqr/MaterialDesignDemo

### 1. 设置Toolbar

#### 1）创建该界面的布局activity_search_view2.xml

指定Toolbar的高度、NaviagtionIcon、标题、字体等

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              xmlns:app="http://schemas.android.com/apk/res-auto"
              android:layout_width="match_parent"
              android:layout_height="match_parent"
              android:orientation="vertical">

    <android.support.v7.widget.Toolbar
        android:id="@+id/toolbar"
        style="@style/Toolbar.MyStyle"
        android:layout_width="match_parent"
        android:layout_height="?attr/actionBarSize"
        android:background="?attr/colorPrimary"
        app:navigationIcon="@mipmap/lg"
        app:popupTheme="@style/ThemeOverlay.AppCompat.Light"
        app:title="本地音乐"
        app:titleTextAppearance="@style/Toolbar.TitleText"
        app:titleTextColor="@android:color/white"/>
</LinearLayout>
```

其中`style`指向的 `Toolbar.MyStyle`是设置标题与NavigationIcon的距离，`titleTextAppearance`指向的`Toolbar.TitleText` 是设置标题文字大小。

在style.xml中创建Toolbar的自定义样式

```xml
<!--标题与NavigationIcon的距离-->
<style name="Toolbar.MyStyle" parent="Base.Widget.AppCompat.Toolbar">
    <item name="contentInsetStart">0dp</item>
    <item name="contentInsetStartWithNavigation">0dp</item>
</style>

<!--Toolbar标题文字大小-->
<style name="Toolbar.TitleText" parent="TextAppearance.Widget.AppCompat.Toolbar.Title">
    <item name="android:textSize">15sp</item>
</style>
```

如果不设置的话，效果不好，NavigationIcon和Toolbar的标题之前的间距看起来很大.
 before | after
 -- | -- 
![](https://upload-images.jianshu.io/upload_images/4050443-cdd823965e2b0ab7.png?imageMogr2/auto-orient/strip\|imageView2/2/w/333/format/webp) | ![](https://upload-images.jianshu.io/upload_images/4050443-c5f76be76773f95c.png?imageMogr2/auto-orient/strip\|imageView2/2/w/334/format/webp)

#### 2）设置去除ActionBar的主题

在Style.xml中创建无ActionBar的主题，并设置主题背景色

```xml
<style name="AppTheme.NoActionBar2" parent="AppTheme">
    <item name="colorPrimary">#D33A31</item>
    <item name="colorPrimaryDark">#D33A31</item>
    <item name="windowActionBar">false</item>
    <item name="windowNoTitle">true</item>
    <!--设置menu中item的图标颜色-->
    <item name="android:textColorSecondary">#ffffff</item>
</style>
```

不设置textColorSecondary的话，默认menu的item图标是黑色，下面看下设置前后的差别：



为Activity设置主题

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
          package="com.lqr.materialdesigndemo">

    <application
        ...
        android:theme="@style/AppTheme">
        ...

        <activity
            android:name=".SearchViewActivity2"
            android:screenOrientation="portrait"
            android:theme="@style/AppTheme.NoActionBar2"/>
    </application>
</manifest>
```

#### 3）在Activity中设置Toolbar的代码如下：

```java
public class SearchViewActivity2 extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_view2);
        // 使用Toolbar代替actionbar
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
    }
    ...
}
```

### 2. 设置Menu

#### 1）创建菜单布局search_view.xml

跟之前的代码相比，只是多加了几个item而已。

```xml
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
      xmlns:app="http://schemas.android.com/apk/res-auto"
      xmlns:tools="http://schemas.android.com/tools">
    <item
        android:id="@+id/menu_search"
        android:orderInCategory="100"
        android:title="搜索"
        app:actionViewClass="android.support.v7.widget.SearchView"
        app:showAsAction="always"
        />
    <item
        android:id="@+id/scan_local_music"
        android:icon="@mipmap/lv"
        android:orderInCategory="100"
        android:title="扫描本地音乐"
        app:showAsAction="never"
        />
    <item
        android:id="@+id/select_sort_way"
        android:icon="@mipmap/lt"
        android:orderInCategory="100"
        android:title="选择排序方式"
        app:showAsAction="never"
        />
    <item
        android:id="@+id/get_cover_lyrics"
        android:icon="@mipmap/lq"
        android:orderInCategory="100"
        android:title="获取封面歌词"
        app:showAsAction="never"
        />
    <item
        android:id="@+id/imporve_tone_quality"
        android:icon="@mipmap/lw"
        android:orderInCategory="100"
        android:title="升级音质"
        app:showAsAction="never"
        />
</menu>
```

#### 2）在Activity中设置Menu的代码如下：

```java
public class SearchViewActivity2 extends AppCompatActivity {

    private SearchView mSearchView;
    ...
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.search_view, menu);
        MenuItem searchItem = menu.findItem(R.id.menu_search);

        //通过MenuItem得到SearchView
        mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
        return super.onCreateOptionsMenu(menu);
    }

    // 让菜单同时显示图标和文字
    @Override
    public boolean onMenuOpened(int featureId, Menu menu) {
        if (menu != null) {
            if (menu.getClass().getSimpleName().equalsIgnoreCase("MenuBuilder")) {
                try {
                    Method method = menu.getClass().getDeclaredMethod("setOptionalIconsVisible", Boolean.TYPE);
                    method.setAccessible(true);
                    method.invoke(menu, true);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
        return super.onMenuOpened(featureId, menu);
    }
}
```
到这里，除了搜索框（SearchView）以外，整个布局的效果大体上都实现了：

![](https://upload-images.jianshu.io/upload_images/4050443-5d7b43fcf641fc7e.gif?imageMogr2/auto-orient/strip|imageView2/2/w/329/format/webp)


### 3. 定制SearchView样式
接下来要实现的样式自定义有：

![](https://upload-images.jianshu.io/upload_images/4050443-cb6a9fbb3a17c242.png?imageMogr2/auto-orient/strip|imageView2/2/w/332/format/webp)

重点来了，我们先来分析一下。SearchView本身不向外提供 “关闭搜索框” 和 “设置搜索框左边的搜索图标” 等方法，所以需要通过其他的方式来实现样式自定义。

**思路** 

如果SearchView的布局结构是 ***通过xml布局文件*** 来实现的，那么可以通过 `SearchView.findViewById()` 的方式得到其中的部分或所有的控件；如果是通过 ***代码动态添加*** 的话，那么可以通过反射的方式得到我们需要的控件，进而对控件进行样式设置。

**结论**  

实现证明，SearchView 的布局结构就是使用xml布局文件实现的，该xml文件名为 `abc_search_view.xml`，且基本上每个控件都有id，这样就可以拿到需要的控件来实现样式自定义了。

#### 1）点击返回按钮，退出搜索框（若搜索框显示的话）
SearchView 本身没有提供关闭搜索框的方法（反正我是没找到啊~~），不过SearchView中正好有一个onCloseClicked()方法是用来关闭搜索框，我们可以通过反射来调用该方法，先来理解下该方法都做了什么，onCloseClicked()的代码如下：

```java
void onCloseClicked() {
    Editable text = this.mSearchSrcTextView.getText();
    
    if(TextUtils.isEmpty(text)) {//否则关闭搜索框
        if(this.mIconifiedByDefault && (this.mOnCloseListener == null || !this.mOnCloseListener.onClose())) {
            this.clearFocus();
            this.updateViewsVisibility(true);
        }
    } 
    else {//如果搜索框中有文字，则清除其中的文字
        this.mSearchSrcTextView.setText("");
        this.mSearchSrcTextView.requestFocus();
        this.setImeVisibility(true);
    }
}
```

这里要考虑到，当搜索框显示时，按下Toolbar的返回按钮关闭搜索框，否则就关闭当前界面。因为搜索框也有id，所以我们可以通过id可以得到搜索框控件，用来判断当前搜索框的显隐状态。结合SearchView内部的onCloseClicked()方法，最后Toolbar返回按钮的点击事件代码可以这么写：

```java
public class SearchViewActivity2 extends AppCompatActivity {

    private SearchView mSearchView;
    private SearchView.SearchAutoComplete mSearchAutoComplete;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_view2);
        ...
        //Toolbar返回按钮的点击事件
        toolbar.setNavigationOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mSearchAutoComplete.isShown()) {
                    try {
                        //如果搜索框中有文字，则会先清空文字，但网易云音乐是在点击返回键时直接关闭搜索框
                        mSearchAutoComplete.setText("");
                        Method method = mSearchView.getClass().getDeclaredMethod("onCloseClicked");
                        method.setAccessible(true);
                        method.invoke(mSearchView);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } else {
                    finish();
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.search_view, menu);
        MenuItem searchItem = menu.findItem(R.id.menu_search);

        //通过MenuItem得到SearchView
        mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
        //通过id得到搜索框控件
        mSearchAutoComplete = (SearchView.SearchAutoComplete) mSearchView.findViewById(R.id.search_src_text);

        return super.onCreateOptionsMenu(menu);
    }

    ...
}
```

![](https://upload-images.jianshu.io/upload_images/4050443-afa0372f65f7ec71.gif?imageMogr2/auto-orient/strip|imageView2/2/w/329/format/webp)

#### 2）隐藏搜索框左边的搜索图标

**搜索框中左边的搜索图标不是一个控件，所以没办法通过id得到，但好在可以通过设置style的方式来修改SearchView所有的图标**。方法也很简单，只需创建一个style（这里取名Widget.SearchView）继承自Widget.AppCompat.SearchView，然后替换需要修改的属性即可。先看下Widget.AppCompat.SearchView的父级Base.Widget.AppCompat.SearchView吧：

![](https://upload-images.jianshu.io/upload_images/4050443-2e39a00c66724194.png?imageMogr2/auto-orient/strip|imageView2/2/w/890/format/webp)

可以看到，这个父级style提供了SearchView中几乎所有的Icon属性，这意味着在图标定制上可以有很大拓展性。其中，layout是指定SearchView的布局，原始布局就是abc_search_view.xml，我们一般不会去动这个属性。
这里我们只需要去掉搜索框左边的图标（即：searchHintIcon），直接设置为@null就好了，如下修改style文件中的Widget.SearchView主题：

```xml
<!--没有ActionBar主题，自定义SearchView样式-->
<style name="AppTheme.NoActionBar2" parent="AppTheme">
    ...
    <!--引入SearchView的自定义样式-->
    <item name="searchViewStyle">@style/Widget.SearchView</item>
</style>

<style name="Widget.SearchView" parent="Widget.AppCompat.SearchView">
    <!--修改搜索框提示文字-->
    <item name="defaultQueryHint">搜索本地歌曲</item>
    <!--修改打开搜索框的搜索按钮的图标-->
    <item name="searchIcon">@mipmap/m5</item>
    <!--修改搜索框左边的搜索按钮图标-->
    <item name="searchHintIcon">@null</item>
</style>
```

![](https://upload-images.jianshu.io/upload_images/4050443-2dd965405732b61a.png?imageMogr2/auto-orient/strip|imageView2/2/w/333/format/webp)

#### 3）设置搜索框的提示文字

##### 修改提示文字内容

修改搜索框提示文字的方式有两种:
- 一种就是修改 SearchView 的 style，如上一步中，修改 `Widget.AppCompat.SearchView` 的 `defaultQueryHint` 属性；
- 另一种方式是调用 SearchView 的 setQueryHint() 来修改。 

这两种方式都可以，如果同时用这两种方式来设置搜索框的提示语，则最终的提示内容将以代码设置方式为主。

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.search_view, menu);
    MenuItem searchItem = menu.findItem(R.id.menu_search);

    //通过MenuItem得到SearchView
    mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
    mSearchAutoComplete = (SearchView.SearchAutoComplete) mSearchView.findViewById(R.id.search_src_text);

    //通过代码方式修改提示文字内容
    mSearchView.setQueryHint("搜索本地歌曲by code");

｝
```

![](https://upload-images.jianshu.io/upload_images/4050443-193f901a04bf2891.png?imageMogr2/auto-orient/strip|imageView2/2/w/333/format/webp)

#####  修改提示文字样式

SearchView 也没有提供任何直接修改搜索框提示文字样式的方法，但既然我们可以通过id得到搜索框控件，那设置提示文字的样式便不是什么问题了，代码如下：

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.search_view, menu);
    MenuItem searchItem = menu.findItem(R.id.menu_search);

    //通过MenuItem得到SearchView
    mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
    mSearchAutoComplete = (SearchView.SearchAutoComplete) mSearchView.findViewById(R.id.search_src_text);
    mSearchView.setQueryHint("搜索本地歌曲by code");

    //设置输入框提示文字样式
    mSearchAutoComplete.setHintTextColor(getResources().getColor(android.R.color.darker_gray));
    mSearchAutoComplete.setTextColor(getResources().getColor(android.R.color.background_light));
    mSearchAutoComplete.setTextSize(14);

    return super.onCreateOptionsMenu(menu);
}
```

![](https://upload-images.jianshu.io/upload_images/4050443-42dedb27a6c82b30.png?imageMogr2/auto-orient/strip|imageView2/2/w/333/format/webp)

#### 4）根据搜索框中有无文字，来显隐搜索框右边的叉叉


这个有点像searchView.onActionViewExpanded()的效果，唯一的区别就是搜索框不能是默认展开的，这要怎么办呢？通过观察onActionViewExpanded()的源码，可以发现该方法中调用了setIconified(false)！！！再联想到setIconified(false)本身就有让搜索框默认展开的效果，这是不是意味着，只要让onActionViewExpanded()的setIconified(false)改为setIconified(true)就好了呢？答案是是的。而且不需要重写SearchView，因为onActionViewExpanded()和setIconified(true)是可以搭配使用的，只要依次调用这两个方法就可以实现这种效果了，代码如下：

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.search_view, menu);
    MenuItem searchItem = menu.findItem(R.id.menu_search);

    //通过MenuItem得到SearchView
    mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
    mSearchAutoComplete = (SearchView.SearchAutoComplete) mSearchView.findViewById(R.id.search_src_text);
    mSearchView.setQueryHint("搜索本地歌曲by code");

    //设置输入框提示文字样式
    mSearchAutoComplete.setHintTextColor(getResources().getColor(android.R.color.darker_gray));
    mSearchAutoComplete.setTextColor(getResources().getColor(android.R.color.background_light));
    mSearchAutoComplete.setTextSize(14);

    //设置搜索框有字时显示叉叉，无字时隐藏叉叉
    mSearchView.onActionViewExpanded();
    mSearchView.setIconified(true);

    //修改搜索框控件间的间隔（这样只是为了在细节上更加接近网易云音乐的搜索框）
    LinearLayout search_edit_frame = (LinearLayout) mSearchView.findViewById(R.id.search_edit_frame);
    ViewGroup.MarginLayoutParams params = (ViewGroup.MarginLayoutParams) search_edit_frame.getLayoutParams();
    params.leftMargin = 0;
    params.rightMargin = 0;
    search_edit_frame.setLayoutParams(params);
    return super.onCreateOptionsMenu(menu);
}
```

![](https://upload-images.jianshu.io/upload_images/4050443-3477a6515519ade1.gif?imageMogr2/auto-orient/strip|imageView2/2/w/329/format/webp)

### 4. 实现搜索提示功能

上面我们已经学习了SearchView的UI定制，下面将通过SearchView自身或结合ListView的方式（RecyclerView应该也一样吧，还没试过）直接学习SearchView搜索提示功能的实现，继续完善 “仿网易云音乐本地音乐搜索” 效果。

#### 1）弹出式搜索提示
SearchView本身的搜索框就是AutoCompleteTextView的一个子类，有图有真相。



AutoCompleteTextView是可以通过设置适配器来实现文本补全提示功能的，所以，SearchView中的搜索框一样也可以，不过SearchView提供了setSuggestionsAdapter()方法可以直接为搜索框设置适配器，需要注意的是，这个适配器必须跟数据库的Cursor对象一起使用，例如：

```java
mSearchView.setSuggestionsAdapter(new SimpleCursorAdapter(SearchViewActivity2.this, R.layout.item_layout, cursor, new String[]{"name"}, new int[]{R.id.text1}));
```

一般开发中遇到的需求是一边输入关键字一边显示搜索结果，所以需要监听搜索框的文字输入，一旦文字变化就查询数据库，更新搜索结果，所以代码可以这么写：

```java
// 监听搜索框文字变化
mSearchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
    @Override
    public boolean onQueryTextSubmit(String s) {
        return false;
    }

    @Override
    public boolean onQueryTextChange(String s) {
        Cursor cursor = TextUtils.isEmpty(s) ? null : queryData(s);
        // 不要频繁创建适配器，如果适配器已经存在，则只需要更新适配器中的cursor对象即可。
        if (mSearchView.getSuggestionsAdapter() == null) {
            mSearchView.setSuggestionsAdapter(new SimpleCursorAdapter(SearchViewActivity2.this, R.layout.item_layout, cursor, new String[]{"name"}, new int[]{R.id.text1}));
        } else {
            mSearchView.getSuggestionsAdapter().changeCursor(cursor);
        }

        return false;
    }
});
```

对于SimpleCursorAdapter的使用，不熟悉的自己百度学习吧，下面看效果：


可以发现，当输入第一个文字"a"时，没有什么反应，当输入第二个文字"a"时，弹出了一个列表弹窗，这是由于AutoCompleteTextView本身默认触发查询动作的条件就是该控件中的文字至少要2个以上，如果我们想修改成只要有一个文字就触发查询的话，则可以这么做：

- 拿到SearchView中搜索框控件
- 调用setThreshold()设置触发查询的字数

直接上代码：

```java
@Override
public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.search_view, menu);
    MenuItem searchItem = menu.findItem(R.id.menu_search);

    //通过MenuItem得到SearchView
    mSearchView = (SearchView) MenuItemCompat.getActionView(searchItem);
    mSearchAutoComplete = (SearchView.SearchAutoComplete) mSearchView.findViewById(R.id.search_src_text);
    ...
    //设置触发查询的最少字符数（默认2个字符才会触发查询）
    mSearchAutoComplete.setThreshold(1);
｝
```

再看下效果：


好了，弹出式搜索功能做完了，下面贴出条目布局item_layout.xml和queryData()方法的代码实现：

① item_layout.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:layout_width="match_parent"
              android:layout_height="match_parent"
              android:orientation="vertical">
    
    <TextView
        android:id="@+id/text1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="center_vertical"
        android:minHeight="?android:attr/listPreferredItemHeightSmall"
        android:paddingLeft="10dp"
        android:paddingRight="10dp"
        android:textAppearance="?android:attr/textAppearanceListItemSmall"
        android:textColor="@android:color/black"/>
</LinearLayout>
```

② queryData()
只是简单的创建一个数据库（music.db），库中有一张tb_music表，表中有_id和name两个字段，然后填充数据，查询数据，相对比较简单，这里就不做过多解释了。

```java
private Cursor queryData(String key) {
    SQLiteDatabase db = SQLiteDatabase.openOrCreateDatabase(getFilesDir() + "music.db", null);
    Cursor cursor = null;
    try {
        String querySql = "select * from tb_music where name like '%" + key + "%'";
        cursor = db.rawQuery(querySql, null);
    } catch (Exception e) {
        e.printStackTrace();
        String createSql = "create table tb_music (_id integer primary key autoincrement,name varchar(100))";
        db.execSQL(createSql);

        String insertSql = "insert into tb_music values (null,?)";
        for (int i = 0; i < Cheeses.sCheeseStrings.length; i++) {
            db.execSQL(insertSql, new String[]{Cheeses.sCheeseStrings[i]});
        }

        String querySql = "select * from tb_music where name like '%" + key + "%'";
        cursor = db.rawQuery(querySql, null);
    }
    return cursor;
}
```

#### 2）结合ListView实现搜索提示

虽然上面已经实现了搜索提示的功能，但网易云音乐本地搜索出来的结果并不是弹出式的，而是在SearchView下方以列表的方式呈现，要做到这样的效果，就必需让SearchView结合ListView一起使用。其实这并不难，因为AutoCompleteTextView设置的适配器跟ListView要设置的适配器是一样的，直接将上边的适配器设置给ListView即可。

```java
// 监听搜索框文字变化
mSearchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
    @Override
    public boolean onQueryTextSubmit(String s) {
        return false;
    }

    @Override
    public boolean onQueryTextChange(String s) {
        Cursor cursor = TextUtils.isEmpty(s) ? null : queryData(s);
        // 设置或更新ListView的适配器
        setAdapter(cursor);
        return false;
    }
});

private void setAdapter(Cursor cursor) {
    if (mLv.getAdapter() == null) {
        SimpleCursorAdapter adapter = new SimpleCursorAdapter(SearchViewActivity2.this, R.layout.item_layout, cursor, new String[]{"name"}, new int[]{R.id.text1});
        mLv.setAdapter(adapter);
    } else {
        ((SimpleCursorAdapter) mLv.getAdapter()).changeCursor(cursor);
    }
}
```
这样就完成了，虽然样式上是丑了点，但，那又怎样，呵呵~





