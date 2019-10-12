*[原文链接](https://blog.csdn.net/j20lin/article/details/80319835)*

## 前言
Web的架构经过多年的发展已经非常成熟了，我们常用的SSM，SSH等等，架构都非常标准。个人认为，Web服务逻辑比较清晰，目的明确，流程也相对固定，从服务器收到请求开始，经过一系列的的拦截器，过滤器->被转发到控制器手中->控制器再调用服务->服务再调用DAO获取想要的数据->最后把数据返回给web层。哪怕中间增加一些东西，如缓存什么的。他的模型依然是以用户请求的线程为生命周期，经过一个个切面(层)的结构，感觉类似于流水线的结构吧。 

<!-- <img src="https://img-blog.csdn.net/20160920115503322" alt="这里写图片描述" width="200px" height="auto" />  -->

而Android App则有所不同，他没有像用户请求这样一个统一的出发点，最接近的可能是来自于UI的事件，然而远不仅仅于此。根据app不同的需求，其结构也会千差万别，所以很难有较为统一的架构。但是客户端类app确实是较为常见的App类型，其结构还是有迹可循的。

## 常见的架构

### 一.MVC 

mvc现在是用的人最多，同时也是Android官方的设计模式，可以说Android App原本就是MVC的，View对应布局文件xml，Controller对应Activity，Model对应数据模型。 

<!-- 这里写图片描述  -->

这类App一般会定义一个BaseActivity，BaseActivity内部实现了网络的异步请求，本地数据的存储加，数据库访问载等复用性较强的逻辑。逻辑控制则在对应的Activity中实现。 

***MVC的缺点:***  
Activity过于臃肿，往往一个Activity几百上千行代码。View层的XML控制力其实非常弱，众多的View处理还是要放在Activity进行，这样的话，Activity就既包含了View又包含了Controller，耦合高，不利于测试扩展，可读性也变差。

### 二. MVVM 

用过VS开发过.net的人肯定知道MVVM的强大之处，仅需要点点鼠标，数据库里的信息和View的控件显示就被简单的绑定了。 

<!-- 这里写图片描述 -->

而Android的数据绑定个人认为还是不够成熟的，用法长这样 `android:text=”@{user.username}”/>` 
在xml里面配置数据模型。一是控制力不够，二是部分逻辑需要放到数据Model里处理。

### 三. MVP 

最近在Android上应用比较火的模式。相较于MVC，MVP将Activity中的业务逻辑抽取出来，将Activity，Fragment等作为View层，专职与界面交互。而Presenter则负责数据Model的填充和View层的显示。View不直接与Model交互，解耦了Actiity。 

<!-- 这里写图片描述  -->

这样可以做到逻辑和界面交互的完全分离，方便测试，界面升级等。代码的可读性也大大增加。

### 个人的设计

对于我自己，在我自己架构项目的时候确实遇到了一些困难，也有选择障碍，经过一番思考。我有了自己的见解，总体还是偏向于MVP，但又有些不同。可能是MVP+MVVM(伪)吧。

首先是包结构 

<!-- ![这里写图片描述](https://img-blog.csdn.net/20160920133658367)  -->

#### 1.View 层 

view层按照Android组件的分类，可以使用接口通信，也可以使用类似EventBus的事件框架进行通信 
Action包就是事件实体，这里使用的是我自己实现的事件框架。 
这里写图片描述

#### 2.Model 层 

model层包含数据模型，实体类，以及dao，http等数据获取得代码。回掉的话可以使用接口，也可以使用事件框架。另外缓存也放在这里。 
这里写图片描述

#### 3.Presenter 

包含Base(自己实现的Presenter框架，其实就是将Activity抽取了一层)，Service包是Android组件Service 
Impl是业务的实现，下面一堆I开头的是业务接口。 
这里写图片描述 
这里讲一下Base，Base相当于控制器，拿登陆来举例，一个登陆操作可能涉及多个界面，多个业务逻辑单元。比如登陆，首先是请求网络的逻辑，除此之外，登陆成功后，需要对会话,用户基础信息等进行持久化；还有控制器需要控制各个界面的刷新。这些都是在控制器Base中完成的，他是一组逻辑的控制单元，负责一个典型的业务，比如说登陆。

#### 业务逻辑

下面的重点是业务接口，例如登陆ILogin，如果自己实现，你需要写一大堆的东西，***网络请求，异步处理，Handler，异常处理，JSON解析，显示***，洋洋洒洒至少上百行了。如果你的项目需要快速上线怎么办？同时你又想保持项目的逻辑结构，以后做更细致的改进，这时候就体现了接口的重要性。这里安利我一个比较快速的实现 *[链接](http://blog.csdn.net/ganyao939543405/article/details/52389852)* 也是我实现的一个小框架。 


用起来画风是这样的。

```java
public class LoginPresenter extends Presenter implements ActivityOnCreatedListener,ICallBack<User,Throwable>{
 
    private ILogin ILogin;
 
    @Override
    protected void onContextChanged(ContextChangeEvent event) {
 
    }
 
    @Override
    public void OnPresentInited(Context context) {
        ILogin = HttpProxyFactory.With(ILogin.class).setCallBack(this).setViewContent(getActivityRaw()).establish();
        getActivityInter().setOnCreateListener(this);
    }
 
    @Override
    public void ActivityOnCreated(Bundle savedInstanceState, final Activity activity) {
        getActivityInter().getView(R.id.btn_login)
                          .setOnClickListener(new View.OnClickListener() {
                              @Override
                              public void onClick(View v) {
                                  LoginActivity ac = (LoginActivity) activity;
                                  ac.progressDialog.show();
                                  getActivityInter().getView(R.id.btn_login).setClickable(false);
                                  EditText name = getActivityInter().getView(R.id.login_name);
                                  EditText pass = getActivityInter().getView(R.id.login_pass);
                                  ILogin.login(name.getText().toString(),pass.getText().toString());
                              }
                          });
    }
 
 
    @Override
    public void onSuccess(User user) {
        Log.e("gy",user.toString());
        getActivityRaw().finish();
        navTo(HomeActivity.class);
    }
 
    @Override
    public void onFailed(Throwable throwable) {
        ILoginCallBack callBack = (ILoginCallBack) getContext();
        callBack.onLogFailed(throwable.getMessage());
    }
}
```

你可以发现ILogin = HttpProxyFactory.With(ILogin.class).setCallBack(this).setViewContent(getActivityRaw()).establish(); 
这么简单，你的ILogin业务接口就被框架实现了，简单的说就是用了动态代理，框架根据你在接口上绑定的注解信息，帮你动态代理处一个业务实现对象。帮你包办了网络请求，异步处理，异步回掉，异常处理，JSON解析，显示等一大堆操作。 
如何绑定你的需求？

ILogin接口张这样的

```java
public interface ILogin {
    @HttpSrcMethod(url = "/store/login",session = Global.SKEY_UNLOGIN,filters = ResultFilter.class)
    public User login(@Param("tel")String name,@Param("password")String passwd);
}
```

返回值模型Model User比较简单，我们换一个比较典型的

```java
@JsonOrm
public class ResultArea implements IHandler{
 
    @JsonString("name")
    private String name;
    @JsonString("id")
    private String id;
    @BindListView(CityPickerActivity.ListViewId)
    @JsonSet(name = "areas",clazz = Area.class)
    private List<Area> child;
 
    public String getName() {
        return name;
    }
 
    public void setName(String name) {
        this.name = name;
    }
 
    public String getId() {
        return id;
    }
 
    public void setId(String id) {
        this.id = id;
    }
 
    public List<Area> getChild() {
        return child;
    }
 
    public void setChild(List<Area> child) {
        this.child = child;
    }
 
    @Override
    public void handler() throws Exception {
        if (child == null)
            child = new ArrayList<>();
        child.add(0,new Area(name,id));
    }
}
```
注解几乎映射了你所有的业务接口协议，包括请求参数，URL，头，返回值的json映射，对应View层的视图显示等等。

使用这种临时解决方案之后，后期如有需求，自己再选用其它框架，或者自己实现业务接口即可，根本不需要动其他模块，从而保证了可扩展性。