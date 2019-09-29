
## [文章 1]()
### 1. 什么是include?
include就是在一个布局中，导入另一个布局


### 2. 为什么使用include?
相同的页面只需要写一次，在需要的地方include即可，提高了共通布局的复用性。


### 3. 怎么使用include？

#### 3.1 步骤
- 定义共通布局
- include共通布局

#### 3.2 Sample

##### 3.2.1 定义共通布局:include_layout.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical" android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/include_lay"
    android:clickable="true"
    android:focusable="true"
    >
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="这是文字"
        android:padding="16dp"
        android:background="@color/colorAccent"
        android:clickable="false"
        android:focusable="false"
        android:layout_marginBottom="10dp"
        />
</LinearLayout>
```

##### 3.2.2 在想要引入的布局中引入 activity_include.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical" 
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    >
    <include layout="@layout/include_layout"/>
</LinearLayout>
```



### 4 include之后，布局变成了什么样?

include布局伪代码

```xml
<LinearLayout>
    <include layout="@layout/include_layout"/>
</LinearLayout>
```

运行时，布局实际结构

```xml
<LinearLayout>
    <LinearLayout id="include_lay">
        <TextView/>
    </LinearLayout>
</LinearLayout>
```

#### 4.1 当我们 include 两个同样的布局时

如果想要获取 id 为 include_lay 的控件实际上为**第一**个 id 为 **include_lay** 的控件，

include的布局伪代码:

```xml
<LinearLayout>
    <include layout="@layout/include_layout"/>
   <include layout="@layout/include_layout"/>     
</LinearLayout>
```

运行时布局实际结构

```xml
<LinearLayout>
    <LinearLayout id="include_lay">
        <TextView/>
    </LinearLayout>
    <LinearLayout id="include_lay">
        <TextView/>
    </LinearLayout>
</LinearLayout>
```
看图说话：

![](https://img-blog.csdn.net/20180604163858578?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l6dGJ5ZGg=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

此时如果，通过 `findViewById(R.id.include_lay)` 获取控件并设置点击事件，则第一个点击时响应，第二个不响应


I think the top answer misses the most important point and might mislead people into thinking the `<include/>` tag creates a View that holds the include contents.

The key point is that include's id is passed to the root view of the include's layout file.

Meaning that this:

```xml
// activity_main.xml
<include layout="@layout/somelayout" android:id="@+id/someid"/>
```

```xml
// somelayout.xml
<?xml version="1.0" encoding="utf-8"?>
<ImageView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    />
```    
Becomes this:

```xml
// activity_main.xml
<ImageView
    android:id="@+id/someid"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    />
```
#### 4.2 当 include 两个相同的布局时，如果区别?

可以在include时指定一个新的id,用来区别。


##### 4.2.1 include之后，使用新的 id 区分

```xml
<LinearLayout>
    <include layout="@layout/include_layout"
        android:id="@+id/include_lay_1"/>
   <include layout="@layout/include_layout"
        android:id="@+id/include_lay_2"/>     
</LinearLayout>
```

##### 4.2.2 这时通过include时指定的id来获取View,就是对应的LinearLayout

```java
LinearLayout include1 = findViewById(R.id.include_lay_1);
LinearLayout include2 = findViewById(R.id.include_lay_2);
```

4.2.3 此时运行时布局实际结构？

```xml
<LinearLayout>
    <LinearLayout id="include_lay_1">
        <TextView   />
    </LinearLayout>
    <LinearLayout id="include_lay_2">
        <TextView />
    </LinearLayout>
</LinearLayout>
```

看图说话:

![](https://img-blog.csdn.net/20180604163912752?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l6dGJ5ZGg=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)


## [2]()

### block_header.xml
```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    	android:id="@+id/layout_header"
        android:layout_width="match_parent"
        android:layout_height="@dimen/title_bar_h"
        android:layout_alignParentTop="true"
        android:background="@color/app_main_color"
        android:paddingLeft="@dimen/bar_pd_left"
        android:paddingRight="@dimen/bar_pd_left"
        android:gravity="bottom" >
		<ImageButton
		    android:id="@+id/btn_back"
		    android:layout_width="wrap_content"
		    android:layout_height="wrap_content"
		    android:src="@drawable/back"
		    android:background="@drawable/grid_item_selector"
		    android:layout_alignParentLeft="true"
		    android:visibility="invisible" />
			
		<TextView android:id="@+id/label_title"
		    android:layout_width="wrap_content"
		    android:layout_height="wrap_content"
		    android:textSize="@dimen/title_size"
		    android:text="标题栏"
		    android:textColor="@color/white"
		    android:layout_centerHorizontal="true"
		    android:layout_alignBottom="@id/btn_back"
        	android:paddingBottom="@dimen/bar_pd_bottom"/>
		
		<ImageButton
		    android:id="@+id/btn_setting"
		    android:layout_width="wrap_content"
		    android:layout_height="wrap_content"
		    android:src="@drawable/setting"
		    android:background="@drawable/grid_item_selector"
		    android:layout_alignParentRight="true"
		    android:visibility="invisible" />
</RelativeLayout>
```

### activity_main.xml

```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity" >

    <include
        android:id="@+id/bolck_titlebar"
        layout="@layout/block_header" />
    
    <TextView
        android:id="@+id/text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/hello_world"
        android:layout_below="@id/bolck_titlebar" />
 
</RelativeLayout>
```

### inlcude 布局控件操作

#### 普通控件的使用

对控件的操作和直接在 activity_main 中布局的控件的操作一致，如设置标题栏的标题文字如下：

```java
TextView tvTitle = (TextView) findViewById(R.id.label_title);
tvTitle.setText(“title”);
```

#### 最外层的 layout 的使用

但要注意的是，如果要对 block_header.xml 中最外层的布局layout_header进行操作，

采用

```java
RelativeLayout layoutHeader = (RelativeLayout) findViewById(R.id.layout_header);
```

获得，获得到的对象为 **null**，这是由于 ***我们为include部分设置了id属性***。

- 如果我们没有设置id属性时，同样能够按照以上方式对其进行操作，如我们要设置背景色（没有对include设置id的做法）：

```java
RelativeLayout layoutHeader = (RelativeLayout) findViewById(R.id.layout_header);
layoutHeader.setBackgroundColor(Color.BLUE);
```

- 如果我们设置了id属性，一些网页介绍通过如下方式获得并对其操作（**错误做法**）：

```java
View layout = getLayoutInflater().inflate(R.layout.block_header, null); 
RelativeLayout layoutHeader= (RelativeLayout)layout.findViewById(R.id.layout_header); 
layoutHeader.setBackgroundColor(Color.BLUE);
```

但通过实验，并不能达到我们想要的效果，虽然设置了背景色，但是在activity_main.xml中表现出来的还是没有设置之前的样子.不难解释，我们通过这种方式获得的对象只是block_header.xml中的layout，并不是我们include进activity_main.xml中的layout.

当我们在 activity_main.xml 设置了 include 的 id，block_header.xml 的最外层布局已被映射到 include 上，所以只需对 include 的视图进行操作，就相当于对 block_header.xml 最外层的布局进行操作.具体如下（对include设置了id的做法）：

```java
View layoutHeader = findViewById(R.id.bolck_titlebar);
layoutHeader.setBackgroundColor(Color.BLUE);
```

Specify the ID in the <include>
```xml
<include layout="@layout/test" android:id="@+id/test1" />
```

Then use two `findViewById` to access fields in the layout

```java
View test1View = findViewById(R.id.test1);
TextView test1TextView = (TextView) test1View.findViewById(R.id.text);
```

Using that approach, you can **access any field in any include you have**.