# [Android DataBinding库(MVVM设计模式)](https://www.cnblogs.com/ldq2016/p/6698181.html)

说到 DataBinding，就有必要先提起 **MVVM** 设计模式。

Model–View–ViewModel(MVVM) 是一个软件架构设计模式，相比 MVVM，大家对 MVC 或 MVP 可能会更加熟悉。

- MVC：（VIew-Model-Controller）

  早期将 View、Model、Controller 代码块进行划分，使得程序大部分分离，降低耦合。


- MVP：（VIew-Model-Presenter）

  由于 MVC 中 View 和 Model 之间的依赖太强，导致 Activity 中的代码过于臃肿。为了他们可以绝对独立的存在，慢慢演化出了 MVP。在 MVP 中 View 并不直接使用 Model，它们之间的通信是通过 Presenter (MVC中的Controller) 来进行的。

- MVVM：（Model–View–ViewModel）

  MVVM 可以算是 MVP的升级版，将 Presenter 改名为 ViewModel。关键在于 View和Model的双向绑定，当 View 有用户输入后，ViewModel 通知 Model 更新数据，同理 Model 数据更新后，ViewModel 通知 View 更新。

 

## Data Binding

 

在Google I/O 2015上，伴随着 Android M 预览版发布了 Data Binding [兼容函数库](https://developer.android.com/tools/data-binding/guide.html).
不知道要扯什么了，还是直接上代码，来看看 Data Binding 的魅力吧。

 



 

### 配置 gradle  

在对应的 Module 的 build.gradle 中添加：

 
```groovy
android {
    ....
    dataBinding {
        enabled =true
    }
}
```



 

### 创建对象

 

创建一个 User类：

```java
 public class User {
  private String firstName;
  private String lastName;

  public User(String firstName, String lastName) {
      this.firstName = firstName;
      this.lastName = lastName;
  }

  public String getFirstName() {
      return this.firstName;
  }

  public String getLastName() {
      return this.lastName;
  }

  public void setLastName(String lastName) {
      this.lastName = lastName;
  }

  public void setFirstName(String firstName) {
      this.firstName = firstName;
  }
}```



 

### 布局

 

在 activity_main.xml 中布局：

```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
  <data>
      <import type="com.example.gavin.databindingtest.User"/>
      <variable
          name="user"
          type="User" />
  </data>
  <LinearLayout
      android:layout_width="match_parent"
      android:layout_height="match_parent"
      android:orientation="vertical"
      android:gravity="center"
      >
      <TextView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text="@{user.firstName}"
          android:textSize="20sp" />
      <Button
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text="@{user.lastName}"
          android:textSize="25sp" />
  </LinearLayout>
</layout>
```

 



 

这里跟平时的布局有点不同，最外层是 layout，里面分别是 data 以及我们的布局。

 

data：声明了需要用到的 user对象，type 用于指定路径。

 

可以在 TextView 中的看到 android:text="@{user.firstName}"， 这是什么鬼，没见过这么写的！！！（不急，继续往下看）

 

### 绑定数据

 

看看下面的 MainActivity：

```java
public class MainActivity extends AppCompatActivity {
  private ActivityMainBinding binding;
  @Override
  protected void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
      User user = new User("Micheal", "Jack");
      binding.setUser(user);
  }
}
```



 

问我 ActivityMainBinding 哪来的？我怎么知道...

运行下看看效果吧：

![](https://upload-images.jianshu.io/upload_images/1638147-0e962174d9fd8f74.png?imageMogr2/auto-orient/strip%7CimageView2/2) 

ActivityMainBinding 是根据布局文件的名字生成的，在后面加了 Binding。

 



 



 

有点懵逼了，就绑定了下而已，这些数据是怎么显示到界面上的。

 



 

## 他是怎么工作的？

 

原来 Data Binding 在程序代码正在编译的时候，找到所有它需要的信息。然后通过语法来解析这些表达式，最后生成一个类。

 

通过反编译我们可以看到(反编译可以[参考这里](http://blog.csdn.net/vipzjyno1/article/details/21039349))

![](https://upload-images.jianshu.io/upload_images/1638147-ffd1bcc515796270.png?imageMogr2/auto-orient/strip%7CimageView2/2)
 

Data Binding 为我们生成了 databinding 包，以及 ActivityMainBinding 类：

 



 

看看我们在 onCreate 中最后调用的 binding.setUser(user)，在 ActivityMainBinding 中可以看到这个方法：

![](https://upload-images.jianshu.io/upload_images/1638147-f0366fe8eb4431f6.png?imageMogr2/auto-orient/strip%7CimageView2/2)



 

我想就是这个 super.requestRebind() 对数据进行了绑定，至于里面怎么实现的，有待进一步研究。

 

## 更多用法

 

上面只是用一个简单的例子，展示了 Data Binding 的用法，如果想在实际项目中使用，可不是上面这例子可以搞定的。下面就来说说 Data Bindig 的更多用法。

 

### 消除空指针顾虑

 

自动生成的 DataBinding 代码会检查 null，避免出现 NullPointerException。

 

例如在表达式中 `@{user.phone}` 如果 u`ser == null` 那么会为 `user.phone` 设置 `默认值null` 而不会导致程序崩溃（基本类型将赋予默认值如 int 为 0，引用类型都会赋值 null）。

 

### 自定义 DataBinding 名

 

如果不喜欢自动生成的 Data Binding 名，我们可以自己来定义：

 
```xml
<data class="MainBinding">
    ....
</data>
``` 

class对应 的就是生成的 Data Binding名。

 

### 导包

 

跟 Java 中的用法相似，布局文件中支持 import 的使用，原来的代码是这样：

 
```xml
<data>
    <variable name="user" type="com.example.gavin.databindingtest.User" />
</data>
``` 

- 使用 import 后可以写成这样：

 
```xml
<data>
    <import type="com.example.gavin.databindingtest.User"/>
    <variable
        name="user"
        type="User" />
</data>
 ```

#### 遇到 `相同的类名` 的时候：

 

```xml
<data>
  <import type="com.example.gavin.databindingtest.User" alias="User"/>
  <import type="com.example.gavin.mc.User" alias="mcUser"/>
  <variable name="user" type="User"/>
  <variable name="mcUser" type="mcUser"/>
</data>
```

 

使用 `alias `设置别名，这样 user 对应的就是 com.example.gavin.databindingtest.User，mcUser 就对应com.example.gavin.mc.User，然后：
 
```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@{user.firstName}"/>
```

当需要用到一些包时，在 Java 中可以自动导包，不过在布局文件中就没有这么方便了。需要使用 import 导入这些包，才能使用。如需要用到 View 的时候：

 
```xml
<data>
    <import type="android.view.View"/></data>
    ...
    <TextView
    ...
    android:visibility="@{user.isStudent ? View.VISIBLE : View.GONE}"
/>
```

> 注意：只要是在 Java 中需要导入包的类，这边都需要导入，如：Map、ArrayList 等，不过 java.lang 包里的类是可以不用导包的。

 

### 表达式

 

在布局中，不仅可以使用：

 
```xml
android:text="@{user.lastName}"
 
```

还可以使用表达式如：

 

#### 三元运算：

 

在 User 中添加 boolean 类型的 isStudent 属性，用来判断是否为学生：

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text='@{user.isStudent? "Student": "Other"}'
    android:textSize="30sp"/>
```



 

> 注意：需要用到双引号的时候，外层的双引号改成单引号。还可以这样用：

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="学生"
    android:visibility="@{user.isStudent ? View.VISIBLE : View.GONE}"
    android:textSize="30sp"/>
```



 

这里用到的 View 需要在 data 中声明：

 
```
<data>
    <import type="android.view.View"/>
</data>
``` 

> 注意：android:visibility="@{user.isStudent ? View.VISIBLE : View.GONE}"，可能会被标记成红色，不用管它编译会通过的。

 

#### ??

 

除了常用的操作法，另外还提供了一个 null 的合并运算符号 ??，这是一个三目运算符的简便写法。

```java
contact.lastName ?? contact.name
 
```

相当于：

 
```java
contact.lastName != null ? contact.lastName : contact.name
``` 

- 所支持的操作符如下：
  - 数学运算符 + - / * %
  - 字符串拼接 +
  - 逻辑运算 && ||
  - 二进制运算 & | ^
  - 一元运算符 + - ! ~
  - 位运算符 >> >>> <<
  - 比较运算符 == > < >= <=
  - instanceof
  - Grouping ()
  - 文字 - character, String, numeric, null
  - 类型转换 cast
  - 方法调用 methods call
  - 字段使用 field access
  - 数组使用 [] Arrary access
  - 三元运算符 ? :

 

### 显示图片

 

除了文字的设置，网络图片的显示也是我们常用的。来看看 Data Binding 是怎么实现图片的加载的。

 

首先要提到 BindingAdapter 注解，这里创建了一个类，里面有显示图片的方法：

```java
public class ImageUtil {
  /**
   * 使用ImageLoader显示图片
   * @param imageView
   * @param url
   */
  @BindingAdapter({"bind:image"})
  public static void imageLoader(ImageView imageView, String url) {
      ImageLoader.getInstance().displayImage(url, imageView);
  }
}
```


（这方法必须是public static的，否则会报错）

 

这里只用了 bind 声明了一个 image 自定义属性，等下在布局中会用到。

 

这个类中只有一个静态方法 imageLoader，里面有两参数，一个是需要设置图片的 view，另一个是对应的 Url，这里使用了 ImageLoader 库加载图片。

 

看看它的布局是什么样的吧：

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:app="http://schemas.android.com/apk/res-auto">

  <data >
      <variable
          name="imageUrl"
          type="String"/>
  </data>

  <LinearLayout

      android:layout_width="match_parent"
      android:layout_height="match_parent"
      android:orientation="vertical"
      android:gravity="center"
      >
      <ImageView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          app:image = "@{imageUrl}"/>
  </LinearLayout>
</layout>
```



 

最后在 MainActivity 中绑定下数据就可以了：

 
```java
binding.setImageUrl("http://115.159.198.162:3000/posts/57355a92d9ca741017a28375/1467250338739.jpg");
 ```

哇靠！！！就这样？我都没看出来它是怎么设置这些图片的。

 

不管了，先看看效果。（其中的原理以后慢慢唠，这里就负责说明怎么使用，这篇已经够长了，不想再写了）

 


看个美女压压惊

![](https://upload-images.jianshu.io/upload_images/1638147-42b66d69c5af3ecc.png?imageMogr2/auto-orient/strip%7CimageView2/2)

> 使用 BindingAdapter 的时候，我这还出现了这样的提示，不过不影响运行。不知道你们会不会...
>
>![](https://upload-images.jianshu.io/upload_images/1638147-97e2b40db38de27d.png?imageMogr2/auto-orient/strip%7CimageView2/2)
>
> ##已解决##
>
> 感谢 颜路 同学指出 `@BindingAdapter({"bind:image"}) ` 改成 `@BindingAdapter({"image"})` 就不会有警告了。

 

### 点击事件

 

在 MainActivity 中声明方法：

 
```java
//参数View必须有，必须是public
//参数View不能改成对应的控件，只能是View，否则编译不通过
public void onClick(View view) {
    Toast.makeText(this,"点击事件", Toast.LENGTH_LONG).show();
}
``` 

布局中：

```java
<data>
    ...
      <variable
      name="mainActivity"
      type="com.example.gavin.databindingtest.MainActivity"/>
  </data>
  ....
      <Button
          ...
          android:onClick="@{mainActivity.onClick}"
          />
```



 

最后记得在 MainActivity 中调用：

```java
binding.setMainActivity(this);
```

发现：布局文件中，variable 中的 name，在 binding 中都会生成一个对应的 set 方法，如：setMainActivity。有 set 方法，那就应该有 get 方法，试试 getMainActivity，还真有。

 

运行下看看效果：

 
![](https://upload-images.jianshu.io/upload_images/1638147-64b01e08adae35d9.gif?imageMogr2/auto-orient/strip)


 

当然如果你不想把点击事件写在 MainActivity 中，你把它单独写在一个类里面：

 
```java
public class MyHandler {
    public void onClick(View view) {
        Toast.makeText(view.getContext(), "点击事件", Toast.LENGTH_LONG).show();
    }
}
```

```xml
  <data>
    ...
      <variable
      name="handle"
      type="com.example.gavin.databindingtest.MyHandler"/>
  </data>
  ....
      <Button
          ...
          android:onClick="@{handle.onClick}"
          />
  </data>
```

 

在 MainActivity 调用：

 
```java
binding.setHandle(new MyHandler());
```

### 调用Activity中变量

 

上面看到它调用 MainActivity中的onClick方法，那么可以调用 MainActivity 中的属性吗？

 

在 MainActivity 中定义 mName：

 
```java
public static String mName = "MM";
``` 

布局中：

 

```xml
  <data>
      ...
      <variable
          name="mainActivity"
          type="com.example.gavin.databindingtest.MainActivity"/>
  </data>
      <Button
          ...
          android:text="@{mainActivity.mName}"
          />
```

 

> 注意：这个变量必须是 public static。

 

### 数据改变时更新UI

 

当数据发生变化时，我们可以这样更新UI：

```java
  private ActivityMainBinding binding;
  private User user;
  @Override
  protected void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
      user = new User("Micheal", "Jack");
      binding.setUser(user);
      binding.setHandle(new MyHandler());
      delay();
  }
  /**
   * 两秒后改变firstName
   */
  private void delay() {
      new Handler().postDelayed(new Runnable() {
          @Override
          public void run() {
              user.setFirstName("Com");
              binding.setUser(user);
          }
      }, 2000);
  }
```




 

看看调用的这个 setUser 是什么：

 

![](https://upload-images.jianshu.io/upload_images/1638147-ff43d8156f8baa78.png?imageMogr2/auto-orient/strip%7CimageView2/2)

 

从反编译的代码中可以看出，setUser 方法中重新绑定了数据。

 

看下效果：

 
![](https://upload-images.jianshu.io/upload_images/1638147-f85afcbd74ac53d4.gif?imageMogr2/auto-orient/strip)


 

### BaseObservable

 

使用上面的代码实现了UI的更新你就满足了？其实官方为我们提供了更加简便的方式，使 User继承BaseObservable，代码如下：

```
public class User extends BaseObservable {
  private String firstName;
  private String lastName;

  public User(String firstName, String lastName) {
      this.firstName = firstName;
      this.lastName = lastName;
  }
  @Bindable
  public String getFirstName() {
      return this.firstName;
  }
  @Bindable
  public String getLastName() {
      return this.lastName;
  }

  public void setLastName(String lastName) {
      this.lastName = lastName;
      notifyPropertyChanged(BR.lastName);
  }

  public void setFirstName(String firstName) {
      this.firstName = firstName;
      notifyPropertyChanged(BR.firstName);
  }
}
```



 

只要 user 发生变化，就能达到改变 UI 的效果。在 MainActivity 中只要调用以下代码：

 
```java
user.setFirstName("Com");
```

有了 BaseObservable 就够了？不不不，我比较懒，不想写那么多 @Bindable 和 notifyPropertyChanged。万一里面有几十个属性，那不写哭起来？而且还有可能写丢了。

 

Data Binding 的开发者贴心得为我们准备了一系列的 ObservableField，包括： ObservableBoolean, ObservableByte, ObservableChar, ObservableShort, ObservableInt, ObservableLong, ObservableFloat,ObservableDouble 以及 ObservableParcelable （原文蓝字部分都是超链接，感兴趣的朋友可以通过原文查看，我这里就不贴出来了，下文若有蓝色字体视为同等情况）看看它们的用法。

 

### ObservableField 的使用

 

1. 创建User2  
```java
public class User2 {
  public final ObservableField<String> firstName = new ObservableField<>();
  public final ObservableField<String> lastName = new ObservableField<>();
  public final ObservableInt age = new ObservableInt();
  public final ObservableBoolean isStudent = new ObservableBoolean();
}
```  
这类里面 没有Get/Set。

2. 布局文件
```xml
<TextView
    ...
    android:text="@{user2.firstName}" />
<TextView
    ...
    android:text="@{user2.lastName}" />
<TextView
    ...
    android:text="@{String.valueOf(user2.age)}" />
 ```

3. MainActivity中：
```java
mUser2 = new User2();
binding.setUser2(mUser2);
mUser2.firstName.set("Mr");
mUser2.lastName.set("Bean");
mUser2.age.set(20);
mUser2.isStudent.set(false);
```

这里 new 了一个 User2 对象后，直接就绑定了。之后只要 mUser2 中的数据发生变化，UI也会随之更新。

除了这几个 Map 跟 List 也是必不可少的，Data Binding 为我们提供了 ObservableArrayMap 和 ObservableArrayList。

 

### ObservableArrayMap 的使用

 
```java
ObservableArrayMap<String, Object> user = new ObservableArrayMap<>();
user.put("firstName", "Google");
user.put("lastName", "Inc.");
user.put("age", 17);
 ```

```xml
<data>
  <import type="android.databinding.ObservableMap"/>
  <variable name="user" type="ObservableMap<String, Object>"/>
</data>
…
<TextView
    android:text='@{user["lastName"]}'
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"/>
<TextView
    android:text='@{String.valueOf(1 + (Integer)user["age"])}'
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"/>
 ```

 

### ObservableArrayList 的使用

 

 
```java
ObservableArrayList<Object> user = new ObservableArrayList<>();
user.add("Google");
user.add("Inc.");
user.add(17);
```

```xml
<data>
  <import type="android.databinding.ObservableList"/>
  <import type="com.example.my.app.Fields"/>
  <variable name="user" type="ObservableList<Object>"/>
</data>
…
<TextView
 android:text='@{user[Fields.LAST_NAME]}'
 android:layout_width="wrap_content"
 android:layout_height="wrap_content"/>
<TextView
 android:text='@{String.valueOf(1 + (Integer)user[Fields.AGE])}'
 android:layout_width="wrap_content"
 android:layout_height="wrap_content"/>
 ```

> 在布局中使用到 ObservableBoolean 类型时，编译无法通过：
```xml
android:text='@{user2.isStudent?"学生":"非学生"}'
 ```
>【目前已知】
>
> 将中文改成英文是可以通过编译的，像下面这样：
>
```xml
android:text='@{user2.isStudent?"Student":"Not Student"}'
 ```
>
> 为何使用中文不可以？原因未明。（感谢指教）
>
> 感谢吕檀溪同学的解决方案： 这是java环境的问题，在系统环境变量中增加一个变量，变量名为: JAVA_TOOL_OPTIONS， 变量值为：-Dfile.encoding=UTF-8，保存。要重启一次电脑，中文就解决了，但是在某些地方，编译的时候控制台会出现部分乱


 

## 在RecyclerView或ListView中使用

 

前面说了那么多基础的用法，可还是不能达到我们的需求。几乎在每个app中都有列表的存在，RecyclerView 或 ListView，从上面所说的似乎还看不出 Data Binding 在 RecyclerView 或 ListView 中是否也能起作用。（用屁股想也知道，Google的开发团对怎么可能会犯这么低级的错误）。下面以 RecyclerView 为例子：

 

-  直接看 Item 的布局（user_item.xml）：
```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">
  <data>
      <variable
          name="user2"
          type="com.example.gavin.databindingtest.User2" />
  </data>
  <LinearLayout
      android:layout_width="match_parent"
      android:layout_height="wrap_content"
      android:padding="10dp"
      android:orientation="horizontal">
      <TextView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text="@{user2.firstName}"/>
      <TextView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text="·"/>
      <TextView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text="@{user2.lastName}"/>
      <View
          android:layout_width="0dp"
          android:layout_height="0dp"
          android:layout_weight="1"/>
      <TextView
          android:layout_width="wrap_content"
          android:layout_height="wrap_content"
          android:text='@{user2.age+""}'/>
  </LinearLayout>
</layout>
```


 

-  RecyclerView 的数据绑定是在 Adapter 中完成的，下面看看 Adapter，这里使用了一个 Adapter，如果你在使用的时候发现 RecyclerView 的动画没了，去[这里](https://realm.io/cn/news/data-binding-android-boyar-mount/)寻找答案.
```java
public class MyAdapter extends RecyclerView.Adapter<MyAdapter.MyHolder> {

  private List<User2> mData = new ArrayList<>();

  public MyAdapter(List<User2> data) {
      this.mData = data;
  }

  @Override
  public MyHolder onCreateViewHolder(ViewGroup parent, int viewType) {
      return MyHolder.create(LayoutInflater.from(parent.getContext()), parent);
  }

  @Override
  public void onBindViewHolder(MyHolder holder, int position) {
      holder.bindTo(mData.get(position));
  }

  @Override
  public int getItemCount() {
      if (mData == null)
          return 0;
      return mData.size();
  }

  static class MyHolder extends RecyclerView.ViewHolder {
      private UserItemBinding mBinding;

      static MyHolder create(LayoutInflater inflater, ViewGroup parent) {
          UserItemBinding binding = UserItemBinding.inflate(inflater, parent, false);
          return new MyHolder(binding);
      }

      private MyHolder(UserItemBinding binding) {
          super(binding.getRoot());
          this.mBinding = binding;
      }

      public void bindTo(User2 user) {
          mBinding.setUser2(user);
          mBinding.executePendingBindings();
      }

  }
}
```

- 最后在布局和 MainActivity 中的使用跟平时的用法一样。  
  - 布局中加入 RecyclerView：
```xml
<android.support.v7.widget.RecyclerView
    android:id="@+id/recycler_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent"/>
 ```
 
  - MainActivity 中：
```java
 List<User2> data = new ArrayList<>();
      for (int i = 0; i < 20; i++) {
          User2 user2 = new User2();
          user2.age.set(30);
          user2.firstName.set("Micheal " + i);
          user2.lastName.set("Jack " + i);
          data.add(user2);
      }
      RecyclerView recyclerView = (RecyclerView) findViewById(R.id.recycler_view);
      LinearLayoutManager layoutManager = new LinearLayoutManager(
              this, LinearLayoutManager.VERTICAL, false);
      recyclerView.setLayoutManager(layoutManager);
      recyclerView.setAdapter(new MyAdapter(data));
```

    这样就可以了。

     不过，在自动生成的 ActivityMainBinding 中，我们可以看到根据 RecyclerView 的 id，会自动生成一个 recyclerView。
  ![](https://upload-images.jianshu.io/upload_images/1638147-25cf2c6224318135.png?imageMogr2/auto-orient/strip%7CimageView2/2)

    所以在 MainActivity 中，我们可以不用 findViewById，直接使用 binding.recyclerView。
```java
LinearLayoutManager layoutManager = new LinearLayoutManager(
              this, LinearLayoutManager.VERTICAL, false);
binding.recyclerView.setLayoutManager(layoutManager);
binding.recyclerView.setAdapter(new MyAdapter(data));
```

来看看效果吧：

![](https://upload-images.jianshu.io/upload_images/1638147-ca6f78541abc5d99.png?imageMogr2/auto-orient/strip%7CimageView2/2)


 

## Tips

 

- `tip1` 若需要显示int类型，需要加上""，例如：
  user.age 为 int类型，需要这样用：  
```xml
<TextView   
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text='@{""+user.age}'/>
 ```  
或者
```xml
<TextView   
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@{String.valueOf(user.age)}"/>
 ```

- `tip2` 不建议新手使用，出现错误的时候根据提示，不容易找到出错位置。（是根本找不到...）
 

 

## 参考

 

- Google官方（权威，不过全英文。点击事件写的好像不对，后来去其他地方查的）  
https://developer.android.com/topic/libraries/data-binding/index.html#data_binding_layout_files

 

- Realm（十分全面）  
https://realm.io/cn/news/data-binding-android-boyar-mount

 

- CSDN-亓斌（有点像google文档的翻译版，整体结果相似）  
http://blog.csdn.net/qibin0506/article/details/47393725

 

- 阳春面的博客（好奇怪的名字）  
https://www.aswifter.com/2015/07/04/android-data-binding-1

 

## 源码地址
- https://github.com/Gavin-ZYX/DataBindingTest

