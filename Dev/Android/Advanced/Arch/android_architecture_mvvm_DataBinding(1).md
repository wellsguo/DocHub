
## I. DataBinding 技术能解决什么问题？

DataBinding技术的出现，肯定是为了解决我们在开发中的一些痛点问题。所以，了解DataBinding要解决的问题，能够使我们更深刻地理解DataBinding技术的设计实现。

从开发角度看，简言之，DataBinding主要解决了两个问题：  
- (1). 需要多次使用 findViewById，损害了应用性能且令人厌烦  
- (2). 更新 UI 数据需切换至 UI 线程，将数据分解映射到各个 view 比较麻烦

应该说，针对上述问题，都有第三方解决方案。第一个问题可以使用 [Jake Wharton]() 的 **ButterKnife** ；对于第二个问题，谷歌提供了 **Loop-Handler** 方案，你还可以使用 **RxJava**，**EventBus** 等方案，但它们只是解决了线程切换的问题，却没有解决将数据分解映射到各个 **view** 的问题，这正是 DataBinding 的魅力所在！同时，DataBinding 的线程切换也是透明的，这是指，当你的 Activity 需要展示新的数据时，你可以在后台线程中获取数据，然后直接交给 DataBinding 就可以了，完全不需要关心线程切换的问题。


## II. DataBinding如何解决这些问题？

### 总体思路

DataBinding 解决这些问题的思路非常简单。就是针对每个 Activity 的布局，在编译阶段，生成一个 **ViewDataBinding** 类的对象，该对象持有 Activity 要展示的数据和布局中的各个 view 的引用（这里已经解决了令人厌烦的 findViewById 问题）。同时该对象还有如下可喜的功能：

- 将数据分解到各个view
- 在UI线程上更新数据
- 监控数据的变化，实时更新

有了这些功能，你会感觉到，你要展示的数据已经和展示它的布局紧紧绑定在了一起，这就是该技术叫做 DataBinding 的原因。

### 实现细节

下面，我们深入 DataBinding 的内部，看看它是如何实现以上所说的功能的。

##### 示范项目基本情况

- 项目名称为 DataBindingTest 
- 项目包名  com.like4hub.www.databindingtest 
- 项目只有一个 **Activity** (MainActivity -> activity_main.xml) Res(两张图片)  
  ![avatar_pure.jpg](https://upload-images.jianshu.io/upload_images/1371984-ddb23b8e6b20b185.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/200/format/webp)
  ![avatar_sexy.jpg](https://upload-images.jianshu.io/upload_images/1371984-c502cb8666c42467.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/200/format/webp)
- 项目数据模型 (**User**)
```java
package com.like4hub.www.databindingtest;
public class User {    
    private String firstName ;  
    private String lastName ;   
    private String avatar ;    
    public User(String avatar, String firstName, String lastName) {  
        this.avatar = avatar;       
        this.firstName = firstName;    
        this.lastName = lastName;   
    }   
    
    public String getAvatar() { return avatar; }   
    public void setAvatar(String avatar) { this.avatar = avatar; }    
    
    public String getFirstName() { return firstName; }  
    public void setFirstName(String firstName) { this.firstName =firstName;    }  
    
    public String getLastName() { return lastName; }  
    public void setLastName(String lastName) { this.lastName = lastName; }
}
```

有了以上的准备工作，我们可以开始了。

### 应用

#### 定义布局文件

```xml
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <data>
        <variable name="user" 
                  type="com.like4hub.www.databindingtest.User"/>
    </data>
    <LinearLayout 
              android:layout_width="match_parent" 
              android:layout_height="match_parent" 
              android:orientation="vertical" 
              android:paddingBottom="16dp" 
              android:paddingLeft="16dp" 
              android:paddingRight="16dp" 
              android:paddingTop="16dp">
        <TextView 
              android:id="@+id/firstname" 
              android:layout_width="wrap_content" 
              android:layout_height="wrap_content" 
              android:text="@{user.firstName}" />
        <TextView 
              android:id="@+id/lastname" 
              android:layout_width="wrap_content" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:text="@{user.lastName}" />
        <ImageView 
              android:layout_width="match_parent" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:src="@{@drawable/avatar_pure}" />
        <Button 
              android:id="@+id/button" 
              android:layout_width="match_parent" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:background="@color/orange" 
              android:text="Test" />
    </LinearLayout>
</layout>
```
> 在使用 DataBinding 需要遵照一定的模板去写布局文件

```xml
<!-- 模板文件 -->
<layout xmlns:android="http://schemas.android.com/apk/res/android">
    <data>
        <!--此处定义该布局要用到的数据的名称及类型-->
    </data>
    <!--此处按照常规方式定义要使用的布局，
        其中可以使用binding表达式代表属性值，
        所谓binding表达式，指形如"@{user.firstName}"的表达式-->
</layout>
```

#### Activity onCreate() 渲染 UI 和更新数据

```java
protected void onCreate(Bundle savedInstanceState) {    
        super.onCreate(savedInstanceState);    

    ActivityMainBinding binding =  DataBindingUtil.setContentView(this,R.layout.activity_main);  
    User user = new User(null, "万","人迷" );    
    binding.setUser(user);
}
```

#### 结果

<img src="https://upload-images.jianshu.io/upload_images/1371984-be91b1d1f934612b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/423/format/webp" width="400px" height="auto"/>



## III. DataBinding 究竟在背后做了什么？

### 3.1 对布局文件进行预处理

##### 首先是布局文件进行预处理

> 预处理后，原布局文件会变成这个样子

```xml
<LinearLayout 
       android:layout_width="match_parent" 
       android:layout_height="match_parent" 
       android:orientation="vertical" 
       android:paddingBottom="16dp"
       android:paddingLeft="16dp" 
       android:paddingRight="16dp" 
       android:paddingTop="16dp" 
       android:tag="layout/activity_main_0" 
       xmlns:android="http://schemas.android.com/apk/res/android">
    <TextView 
              android:id="@+id/firstname"
              android:layout_width="wrap_content"
              android:layout_height="wrap_content" 
              android:tag="binding_1" />
    <TextView 
              android:id="@+id/lastname" 
              android:layout_width="wrap_content" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:tag="binding_2" />
    <ImageView 
              android:layout_width="match_parent" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:tag="binding_3" />
    <Button 
              android:id="@+id/button" 
              android:layout_width="match_parent" 
              android:layout_height="wrap_content" 
              android:layout_marginTop="16dp" 
              android:background="@color/orange" 
              android:text="Test" />
</LinearLayout>
```
我们看到，根元素 LinearLayout 和那些在属性中使用了 binding 表达式的 view 都被设置了 **`Tag`** ，而原有的 `<layout>`、`<data>` 以及里面的 `<variable>`，还有各个 `view` 中的`binding 表达式` 都不见了！！

**DataBinding将它们藏在哪儿了呢？**

答案是：  
DataBinding 把最初布局文件中的 `<data>` 以及各个 `view` 中的 `binding 表达式` 内容抽取出来，生成了一个名为 **`activtiy_main-layout.xml`** 文件.
>activtiy_main-layout.xml

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Layout layout="activity_main" modulePackage="com.like4hub.www.databindingtest">
    <Variables declared="true" type="com.like4hub.www.databindingtest.User" name="user"></Variables>
    <Targets>
        <Target tag="layout/activity_main_0" view="LinearLayout"></Target>
        <Target id="@+id/firstname" tag="binding_1" view="TextView">
            <Expression text="user.firstName" attribute="android:text"/>
        </Target>
        <Target id="@+id/lastname" tag="binding_2" view="TextView">
            <Expression text="user.lastName" attribute="android:text"/>
        </Target>
        <Target tag="binding_3" view="ImageView">
            <Expression text="@drawable/avatar_pure" attribute="android:src"/>
        </Target>
    </Targets>
</Layout>
```

通过给原有布局文件中的 `view` 设置 `Tag` 和在生成的文件中使用 `Tag`，使得抽取出来的内容能够与其原先所在的位置关联起来。如下图所示：


![映射图.png](https://upload-images.jianshu.io/upload_images/1371984-dea0499aac246b02.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

这里有几点需要注意：

> 1、LinearLayout 设置的 Tag 是以 `layout` 开头的，表示它是根布局。  
> 2、最初布局文件 `<data>` 标签中的内容几乎原封不动的挪到了新生成的文件中。  


### 3.2 生成 ActivityMainBinding 与 BR 类

现在，DataBinding 将会依据上面两个 xml 文件（即activtiy_main.xml和activtiy_main-layout.xml）生成两个类:

#### (1) ActivityMainBinding

> 它继承自 ViewDataBinding，里面包含如下 fields

```java
// views
public final android.widget.Button button;
public final android.widget.TextView firstname;
public final android.widget.TextView lastname;
private final android.widget.LinearLayout mboundView0;
private final android.widget.ImageView mboundView3;
// variables
private com.like4hub.www.databindingtest.User mUser;
```

观察这些fields，我们可以发现：

- **对应每个 variable 标签**，ActivityMainBinding都有一个相应的变量，在本例中就是上面的mUser变量。
- **对应每一个有 id 的 View**，都会有一个以其 id 为名的 public final 变量，其类型正是该 View 的类型(如button，firstname)。
- **对应每一个没有 id 但是处理中添加了 Tag 的 View**，都会有一个 private final 的变量与其对应，名字没有什么特殊的含义(如mboundView0, mboundView3)。

#### (2) BR

```java
package com.like4hub.www.databindingtest;
public class BR {     
    public static final int _all = 0;     
    public static final int user = 1;
}
```

其中的 `_all` 变量是默认生成的，`user` 变量是对应 ActivityMainBinding 类中的 `mUser` 变量的。

举例来讲，假如我们有一个 ActivityMainBinding 类的实例对象 `amb` ，我们可以调用`amb.setVariable(BR.user, userInstance)`，该调用将会把 `userInstance` 赋值给 `amb` 的 `mUser` 变量。下面是 setVariable 方法的代码：

```java
public boolean setVariable(int variableId, Object variable) {    
       switch(variableId) {     
              case BR.user :  
                     setUser((com.like4hub.www.databindingtest.User)variable);
                     return true;
       }   
       return false;
}
```

那么，DataBinding 是否仅仅只给 `<data>` 标签中的每一个 `variable` 生成对应的 BR 常量，答案是：**NO**。

如果你在 `User` 类中的 `getAvatar` 方法上添加 `@Bindable`注解，并且让 `User` 类继承 `BaserObservable` 那么，DataBinding 生成的 BR 类中将会是这样：

```java
public class BR {        
    public static final int _all = 0;    
    public static final int avatar = 1;      
    public static final int user = 2;
}
```

实际上，BR 中的常量是一种标识符，它对应一个会发生变化的数据，当数据改变后，你可以用该标识符通知 DataBinding，很快，DataBinding 就会用新的数据去更新 UI。

那么，**DataBinding如何知道哪些数据会变化呢？**

目前，我们可以确定，`<data>` 中的每一个 `variable` 是会变化的，所以 DataBinding 会为它们生成 BR 标识符。用 `@Bindable` 注解的类中的 `getXXX` 方法（该类父类为 `BaseObservable` 或者实现 `Observable` 接口）对应一个会变化的数据，DataBinding 也会为它们生成 BR 标识符。实际上，还有第三种，暂且按下不表。

### 3.3 生成 ActivityMainBinding 实例并绑定

在这一步中，主要有三个过程：

- 第一步: **Inflate 处理后的布局文件**. 由于现在 activity_main.xml 文件与普通的 layout 文件一样。现在 **DataBindingUtil** 将会 Inflate activity_main.xml 文件，得到一个 ViewGroup 变量 root 。

- 第二步: **生成 ActivityMainBinding 实例对象**. DataBindingUtil 会将这个变量 root 传递给 ActivityMainBinding 的构造方法，生成一个 ActivityMainBinding 的实例，就是我们在 onCreate 方法中获取的 binding 对象。下面看看 ActivityMainBinding 的构造过程，它的构造方法签名如下：  
```java
public ActivityMainBinding(android.databinding.DataBindingComponent bindingComponent, View root)
```  
其中第二个参数就是刚刚生成的 ViewGroup root。你可能想知道第一个参数bindingComponent哪来的，简单一句话，是从 DataBindingUtil 的 getDefaultComponent 调用中得来的。如果你之前学习过 DataBinding，并且使用过 BindingAdapter 的话，你应该会比较熟悉它，这里不展开讲。  
好，让我们继续构造我们的ActivityMainBinding对象。  
在构造方法中，ActivityMainBinding 会首先遍历 root，根据各个 View 的 Tag 或者 id，初始化自己的fields ，就是下面这些：  
```java
public final android.widget.Button button;
public final android.widget.TextView firstname;
public final android.widget.TextView lastname;
private final android.widget.LinearLayout mboundView0;
private final android.widget.ImageView mboundView3;
```  
至此，Tag们的历史使命完成了，ActivityMainBinding 将会把之前加到各个 View 上的 Tags 清空。  
最后，构造方法调用invalidateAll引发数据绑定。

- 第三步: **数据绑定**  
在这一步中，ActivityMainBinding 将会计算各个 view 上的 binding 表达式，然后赋值给 view 相应的属性。绑定的主要代码如下（省略部分细节）：  
```java
@Override
protected void executeBindings() {   
       java.lang.String firstNameUser = null;  
       java.lang.String lastNameUser = null;   

       com.like4hub.www.databindingtest.User user = mUser;  

       if (user != null) {          
              // read user.firstName       
              firstNameUser = user.getFirstName();         
              // read user.lastName           
              lastNameUser = user.getLastName();    
       }  

       TextViewBindingAdapter.setText(this.firstname, firstNameUser);        
       TextViewBindingAdapter.setText(this.lastname, lastNameUser);   

       ImageViewBindingAdapter.setImageDrawable(this.mboundView3, 
       getDrawableFromResource(R.drawable.avatar_pure));   
}
```

##### 数据绑定过程分析   

- 首先，针对两个 binding 表达式  `user.firstname` 和 `user.lastname`   
ActivityMainBinding 生成了两个临时变量，即：
```java
java.lang.String firstNameUser = null;
java.lang.String lastNameUser = null;
```
从中我们可以看出这两个变量的命名的规律。这两个变量就代表了两个 binding 表达式的值，为它们赋值的过程实际上就是 binding 表达式求值的过程。  
ActivityMainBinding 通过调用 `mUser` 的 getFirstName 和 getLastName 方法为上面两个变量赋值。  

  请思考,ActivityMainBinding 是怎么知道调用 mUser 的 getXXX 方法为 binding 表达式求值的？  
  - 这个问题可以分成两步：
  
    首先，在构建 ActivityMainBinding 类时，会对 activtiy_main-layout.xml 中的数据进行分析，我们再次贴出该文件的内容，以便继续：  
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Layout layout="activity_main" modulePackage="com.like4hub.www.databindingtest">
    <Variables declared="true" type="com.like4hub.www.databindingtest.User" name="user"></Variables>
    <Targets>
        <Target tag="layout/activity_main_0" view="LinearLayout"></Target>
        <Target id="@+id/firstname" tag="binding_1" view="TextView">
            <Expression text="user.firstName" attribute="android:text"/>
        </Target>
        <Target id="@+id/lastname" tag="binding_2" view="TextView">
            <Expression text="user.lastName" attribute="android:text"/>
        </Target>
        <Target tag="binding_3" view="ImageView">
            <Expression text="@drawable/avatar_pure" attribute="android:src"/>
        </Target>
    </Targets>
</Layout>
```
DataBinding发现，有一个variable名为user，所以它为ActivityMainBinding生成了一个mUser变量，DataBinding 进一步检查该文件发现，两个 binding 表达式 user.firstName 和 user.lastName 圆点前面的字符串也是 user，由此知道，这两个表达式的值来自mUser。

   接着，DataBinding再次进行分析，两个binding表达式圆点后的字符串分别是firstName和lastName，所以DataBinding决定调用mUser的getFirstName和getLastName方法。
请注意，让User类中包含这两个方法是我们开发者的责任。
求出值之后就是设置了，比较简单。

   在这里我们可以清楚地看到，binding 表达式 user.firstName 和 user.lastName 并不是对应着 User类中的两个 fields，它们实际对应的是 User 类的两个 get 方法。
   
   至此，你可以大胆猜测一下，如果我们给User类添加一个如下方法：
```java
public String getAlias(){
return "Alias";
}
```
但是我们并不给它添加一个String 类型的alias field，我们是否可以在binding表达式中这样写：`@{user.alias}`。  

    答案是：**YES YOU CAN！**

    进一步你可以理解，上文中，我们为什么要将@Bindable注解加到一个get方法上面而不是一个field上面了。
    
- 最后，由于 ImagView中 的 binding 表达式本身就是一个值，我们不需要再求值了，直接赋值就是。

## IV. 小结
本文这样做，仅仅是为了说明，DataBinding 为 View 添加 tag 的规则是该 View 的属性中有没有使用binding 表达式。


好了，至此，我们分析DataBinding工作的核心原理，还有三个内容没有涉及，
 - 一个是数据更新（仅略提了一下），
 - 另一个是BindingAdapter（其实在executeBindings方法中已经看到它们的身影了），
 - 最后一个是事件监听绑定（这个很简单）。
 
其实，掌握了这些核心原理，剩下的内容你可以很轻松地掌握.
