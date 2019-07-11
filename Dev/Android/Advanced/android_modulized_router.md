## Android 模块化（三）：路由

[ARouter，要做到组件之间自由并且可控的跳转，需要做到下面几点](https://www.jianshu.com/p/aa17cf4b2dca)：  
- 路由跳转需要支持传递基本类型和自定义类型（例如Object）  
- 路由的跳转需要和组件的生命周期一致，即只有加载的组件才可以跳转，卸载后的组件是不可达的  
- 最好生成路由表，组件对外提供的路由可以轻松查阅到  


### 1. ARouter 配置

- 组件化框架的公用模块添加依赖库
```
compile 'com.alibaba:arouter-api:1.3.0'
```

- 在跳转的目标组件的 build.gradle 中，增加以下配置
```
android {
    defaultConfig {
    ...
    javaCompileOptions {
        annotationProcessorOptions {
        arguments = [ moduleName : project.getName() ]
        }
    }
    }
}
dependencies {
    annotationProcessor 'com.alibaba:arouter-compiler:1.1.4'
    ...
}
```
在组件化框架中，如果要从 *A 模块* 跳转到 *B 模块*，所以需要在*B 模块/build.gradle* 中增加上述配置。



### 2. 在目标页面增加相应的注解

> 以“分享图书” 页面为例

```java
@Route(path = "/share/shareBook")
public class ShareActivity extends AppCompatActivity {
    ...
}
```

在进入这个页面，需要传入两个参数，一个是 String 类型的 bookName，一个是自定义类型 Author 的 author。

```java
@Autowired
String bookName;
@Autowired
Author author;
```


### 3. 如何传递自定义类型

由于自定义类型 Author 需要跨组件传递，我们知道，[JIMU](https://link.jianshu.com/?t=https%3A%2F%2Fgithub.com%2Fmqzhangw%2FJIMU) 的核心之处就是在组件之间见了一堵墙，在编译期代码和资源都是完全隔离的，所以 Author 必须定义在 share 组件向外提供的服务中。所以我们在 component 中，定义Author类：

```java
public class Author {
    private String name;
    private int age;
    private String county;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
    public String getCounty() {
        return county;
    }
    public void setCounty(String county) {
        this.county = county;
    }
}
```

现在就解决了Author的可见性问题，但是为了能在路由中传递，按照ARouter的要求，还需要自己实现SerializationService：

```java
@Route(path = "/service/json")
public class JsonServiceImpl implements SerializationService {
    
    @Override
    public void init(Context context) {}
    
    @Override
    public <t> T json2Object(String text, Class<t> clazz) {
        return JSON.parseObject(text, clazz);
    }
    
    @Override
    public String object2Json(Object instance) {
        return JSON.toJSONString(instance);
    }
    
    @Override
    public <t> T parseObject(String input, Type clazz) {
        return JSON.parseObject(input, clazz);
    }
}
```

这里笔者就遇到了一个坑，本来我把这个类定义在 readercomponent 中，结果运行之后会报空指针异常。只有我把类移到 sharecomponent 之后，异常才消失。暂时没找到原因，但是定义在这里，假如要跳转到 readercomponent 怎么办呢？

### 4. 发起跳转

在组件化框架 demo 中，发起跳转是 readercomponent 中的 ReaderFragment 中，demo 中列出了两个示例：

#### 4.1 普通跳转

```java
private void goToShareActivityNormal() {
    Author author = new Author();
    author.setName("Margaret Mitchell");
    author.setCounty("USA");
    ARouter.getInstance().build("/share/shareBook")
            .withString("bookName", "Gone with the Wind")
            .withObject("author", author)
            .navigation();
}
```

#### 4.2 startActivityForResult

```java
private void goToShareActivityForResult() {
    Author author = new Author();
    author.setName("Margaret Mitchell");
    author.setCounty("USA");
    ARouter.getInstance().build("/share/shareMagazine")
            .withString("bookName", "Gone with the Wind")
            .withObject("author", author)
            .navigation(getActivity(), REQUEST_CODE);
}
```

### 5. 控制生命周期

经过上面的操作，已经可以完成UI跳转了。但是如果运行demo就可以发现，此时即使卸载了分享组件，分享书的页面还是可以进入的，说明生命周期没有同步。在JIMU自带的方案中是不存在这个问题的，因为跳转的逻辑已经与组件化生命周期绑定在一起。

这里就用到ARouter自带的拦截器功能，每个组件都需要定义一个拦截器，当组件卸载之后需要拦截住该组件的跳转入口。

下面是分享组件拦截器的示例代码：

```java
@Interceptor(priority = 1, name = "分享组件拦截器")
public class ShareInterceptor implements IInterceptor {
    public static boolean isRegister;
    Context mContext;
    @Override
    public void process(Postcard postcard, InterceptorCallback callback) {
        if (isRegister) {
            callback.onContinue(postcard);
        } else if ("/share/shareBook".equals(postcard.getPath())
                || "/share/shareMagazine".equals(postcard.getPath())) {
            MainLooper.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(mContext, "分享组件已经卸载", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
    @Override
    public void init(Context context) {
        mContext = context;
    }
}
```

这里通过一个isRegister开关来控制拦截器是否生效，为了保证生命周期一致性，在ShareApplike中增加赋值逻辑：

```java
public class ShareApplike implements IApplicationLike {
    @Override
    public void onCreate() {
        ShareInterceptor.isRegister = true;
    }
    @Override
    public void onStop() {
        ShareInterceptor.isRegister = false;
    }
}
```

但是这里也遇到了两个小坑，不知道是否是ARouter使用不当：  
- (1) 添加或者修改拦截器之后，必须卸载重装app才能生效，不论是clean还是rebuild都是不生效的  
- (2) 拦截器中需要硬编码该组件的所有路由，例如/share/shareBook等，一旦路由发生了改变，一定要记得修改这个地方

### 6. 路由表生成

这个 ARouter 暂时没有提供，JIMU 自带的方案增加了这个功能，当组件 build 生成之后，在根目录生成 UIRouterTable 文件夹，里面会列出每个组件向外提供的路由表以及具体参数

```
auto generated, do not change !!!! 

HOST : share

分享杂志页面
/shareMagazine
author:com.luojilab.componentservice.share.bean.Author
bookName:String

分享书籍页面
/shareBook
author:com.luojilab.componentservice.share.bean.Author
bookName:String
```

这点对于组件的协同开发是比较重要的，毕竟跳转之前翻阅别人的代码是件比较费事的工作


