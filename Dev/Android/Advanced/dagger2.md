## Dagger2 入门

### 0. 写在最前面
<font color=#D2691E>`作用`</font> 解决 Android 或 Java 中依赖注入的一个类库（DI类库）.  

<font color=#D2691E>`依赖注入`</font> 就是目标类（需要进行依赖初始化的类）中所依赖的其他的类的初始化过程，不是通过手动编码的方式创建，而是通过技术手段把其他类的已经初始化好的实例自动注入到目标类中。从 UML 关系角度我们将依赖的目标类称为 Client，被依赖的类称为 Supplier，全文都用 Client 和 Supplier 来进行说明。  


- 常规的对象间依赖解决方法
```java
 class Normal {
       B b = new B(...);
       C c = new C();
       D d = new D(new E());
       F f = new F(.....);
 }
```
上面的代码完全没任何问题，但是总感觉创建对象的这些代码基本都是重复的体力劳动，那为何不想个办法，把这些重复的体力劳动用一种自动化的、更省力的方法解决掉，这样就可以让开发的效率提高，可以把精力集中在重要的业务上了。


- 注解方式依赖解决方法
```java
class Client {
     @inject
     Supplier supplier;
}
```
```java
class Supplier {
    @inject
    Supplier(){ ... }
}
```
注解( Annotation )来标注目标类中所依赖的其他类，同样用注解来标注所依赖的其他类的构造函数，那注解的名字就叫 Inject。

### 1. dagger2 注解
Inject / Component / Module / Provides

#### 1.1 Inject
在上面的代码中已经出现过`@inject`，分别出现在依赖的目标类 Client (客户方) 和被依赖类 Supplier (供给方)中。仅仅在两个类中进行简单的声明是不足以实现依赖的自动注入。并不能像 Spring 那样直接用一个 @Autoware 注解，便可以从容器中查找相对应的对应，同时完成依赖注入。但是 Dagger 中提供了一个 Component 来弥补 Client 和 Supplier 之间的鸿沟，起到了一个桥接关联的作用。

#### 1.2 Component
`@Component` 也是一个注解类，一个类要想成为 Component 组件，必须用 `@Component` 注解来标注该类，并且规定该类必须是接口或抽象类。

Component 又是如何是实现 Client 和 Supplier 构造函数之间的桥接工作呢？  
首先 Component 查找 Client 类中用 @Inject 注解标注的属性，获取到相应的属性后，接着查找该属性对应的 Supplier 类，然后在该 Supplier 类中用 @Inject 标注的构造函数（此时就发生联系了），剩下的工作就是初始化该属性的实例并为实例进行赋值。因此根据其工作模式也可以将 Component 叫作 Injector （注入器）。

```java
@Component(dependencies = AppComponent.class)
public interface BookComponent {
    BookDetailActivity inject(BookDetailActivity activity); // BookDetailActivity 即为 Client
    ...
    BookDetailDiscussionFragment inject(BookDetailDiscussionFragment fragment);
}
```

`小结`

1. 用 Inject 注解标注 Client 类中属性
2. 用 Inject 注解标注 Client 属性所对应的 Supplier 类的构造方法  
3. 若当前 Supplier 类还依赖于其它的 Supplier 类，则重复上面2个步骤  
4. 调用 Component（注入器）的 injectXXX(Object) 方法开始注入（ injectXXX 方法名字是官方推荐的）

#### 1.3 Module
到目前为止依赖注入是不是就可以完全实现了呢？当然不是。开发中经常会用到第三方库，往往第三方库又不能修改(其实也是可以修改的，但最好不要改)，所以根本不可能把 Inject 注解加入这些类中，这时 Inject 就无能为力了。

不能直接修改那就封装吧。因此，另一种做法是封装第三方库，封装的代码怎么管理呢，总不能让这些封装的代码散落在项目中的任何地方，总得有个好的管理机制，此时 Module 就应运而生了。可以把封装第三方库的代码放入 Module 中，如下：
```java
@Module
public class ModuleClass{
      // A 是第三方类库中的一个类
      @Provides
      A provideA(){
          return A();
      }
}
```   
Module 其实是一个简单工厂模式， Module 里面的方法基本都是创建类实例的方法。接下来问题来了，因为 Component 是注入器（Injector），我们怎么能让 Component 与 Module 有联系呢？

```java
@Module
public class BookApiModule {

    @Provides
    public OkHttpClient provideOkHttpClient() {

        LoggingInterceptor logging = new LoggingInterceptor(new Logger());
        logging.setLevel(LoggingInterceptor.Level.BODY);

        OkHttpClient.Builder builder = new OkHttpClient.Builder().connectTimeout(10, TimeUnit.SECONDS)
                .connectTimeout(20 * 1000, TimeUnit.MILLISECONDS)
                .readTimeout(20 * 1000, TimeUnit.MILLISECONDS)
                .retryOnConnectionFailure(true) // 失败重发
                .addInterceptor(new HeaderInterceptor())
                .addInterceptor(logging);
        return builder.build();
    }

    @Provides
    protected BookApi provideBookService(OkHttpClient okHttpClient) {
        return BookApi.getInstance(okHttpClient);
    }
}
```

```java
@Module
public class AppModule {
    private Context context;

    public AppModule(Context context) {
        this.context = context;
    }

    @Provides
    public Context provideContext() {
        return context;
    }
}
```


##### Component 新职责
Component 是注入器，它一端连接 Client 类，另一端连接 Supplier 实例，它把 Supplier 实例注入到 Client 类中。上文中的 Module 是一个提供类实例的类，所以 Module 应该是属于 Component 的实例端的。 因此， Component 的新职责就是管理好 Module，Component 中的 modules 属性可以把 Module 加入 Component，modules 可以加入多个 Module。
```java
@Component(modules = {AppModule.class, BookApiModule.class})
public interface AppComponent {

    Context getContext();

    BookApi getReaderApi();

}
```

#### 1.4 Provides

Module 中的创建类实例方法用 Provides 进行标注，Component 在搜索到 Client 类中用 Inject 注解标注的属性后，Component 就会去 Module 中去查找用 Provides 标注的对应的创建类实例方法，这样就可以解决第三方类库用 dagger2 实现依赖注入了。

#### 1.5 Summary
Inject，Component，Module，Provides 是 dagger2 中的最基础最核心的知识点。奠定了 dagger2 的整个依赖注入框架。

- Inject 主要是用在自己编写的代码中，用来标注目标类的依赖和依赖的构造函数
- Module 和 Provides 是为解决第三方类库而生的。Module 是一个简单工厂模式，Module 可以包含创建类实例的方法，这些方法用 Provides 来标注
- Component 它是一个桥梁，一端是 Client 类，另一端是 Supplier 类的实例，它也是注入器（Injector）负责把 Supplier 类的实例注入到 Client 类中，同时它也管理 Module。

## Dagger2 进阶
Qualifier（限定符）、Singleton（单例）、Scope（作用域）、Component 的组织方式。

### 1. Qualifier
创建类实例有两个维度可以创建。一是，通过用 Inject 注解标注的构造函数来创建（简称 Inject 维度）。二是，通过工厂模式的 Module 来创建（简称 Module 维度）。
这两个维度是有优先级之分的，Component 会首先从 Module 维度中查找类实例，若找到就用 Module 维度创建类实例，并停止查找 Inject 维度。否则从 Inject 维度查找类实例。所以创建类实例级别 Module 维度要高于 Inject 维度。

现在有个问题，基于同一个维度条件下，若一个类的实例可以通过多种方法来创建，那 Component 应该选择哪种方法来创建该类的实例呢？如下，基于Inject维度：
```java
public class Supplier {
    @Inject Supplier() {}
    @Inject Supplier(...) {}
}
```

```java
public class Client {
    @Inject
    Supplier supplier;
}
```

此时出现了```依赖注入迷失```, 可以通过 Qualifier 注解解决。 如下： 

```java
// 自定义一个 ThemeNight 的注解
@Qualifier
public @interface ThemeNight {
}
```

```java
// 自定义一个 ThemeDay 的注解
@Qualifier
public @interface ThemeDay {
}
```

```java
public class Supplier {
    @Inject
    @ThemeDay
    Supplier() {}
    
    @Inject 
    @ThemeNight
    Supplier(...) {}
}
```

```java
public class Client {
    @Inject
    @ThemeNight
    Supplier supplier;
}
```

### 2.  Component 组织方式

#### 2.1 App 该如何划分 Component
假如一个 App 中只有一个 Component，那这个 Component 是很难维护的，不仅代码体积庞大，并且后期的变化也会很大。就是因为 Component 的职责太多了导致的。所以有必要把这个庞大的 Component 进行划分，划分为粒度更小的 Component。划分的规则如下：

- a. 要有一个全局的 Component (Application Component), 负责管理整个 App 的全局类实例（整个 App 都要用到的实例，这些类基本上都是单例的，后面会用此词代替）
- b. 每个页面对应一个 Component，比如一个 Activity 页面定义一个 Component，一个 Fragment 定义一个 Component。当然这不是必须的，有些页面之间的依赖的类是一样的，可以共用一个 Component。

第一个规则应该很好理解，具体说下第二个规则，为什么以页面为粒度来划分 Component？

- 一个 App 是由很多个页面组成的，从组成 App 的角度来看一个页面就是一个完整的最小粒度了。
- 一个页面的实现其实是要依赖各种类的，可以理解成一个页面把各种依赖的类组织起来共同实现一个大的功能，每个页面都组织着自己的需要依赖的类，一个页面就是一堆类的组织者。
- 划分粒度不能太小了。假如使用 MVP 架构搭建 App，划分粒度是基于每个页面的 M、V、P 各自定义 Component 的，那 Component 的粒度就太小了，定义这么多的 Component，管理、维护就很非常困难。  

所以以**页面**划分 Component 在管理、维护上面相对来说更合理。

#### 2.2 Singleton 没有创建单例的能力
为什么要谈到创建单例呢？因为上面谈到一个 App 要有一个全局的 Component（ApplicationComponent），ApplicationComponent负责管理整个 App 用到的全局类实例，那不可否认的是这些全局类实例应该都是单例的，那我们怎么才能创建单例？

> 上一节提到过 Module 的作用，Module 和 Provides 是为解决第三方类库而生的，Module 是一个简单工厂模式, Module 可以包含创建类实例的方法。

现在 Modlule 可以创建所有类的实例。同时

> Component 会首先从 Module 维度中查找类实例，若找到就用 Module 维度创建类实例，并停止查找 Inject 维度。否则从 Inject 维度查找类实例。所以创建类实例级别 Module 维度要高于 Inject 维度。

所以基于以上两点，我们就可以创建单例。

- a. 在 Module 中定义创建全局类实例的方法
- b. ApplicationComponent 管理 Module
- c. 保证 ApplicationComponent 只有一个实例（在 App 的 Application 中实例化 ApplicationComponent）

dagger2 中正真创建单例的方法就是上面的步骤，全局类实例的生命周期也和Application一样了，很关键的一点就是保证 ApplicationComponent 是只初始化一次。那估计有朋友就会问 Singleton 那岂不是多余的？答案当然是 no no no。Singleton 有以下作用：

- 更好地管理 ApplicationComponent 和 Module 之间的关系，保证 ApplicationComponent 和 Module 是匹配的。若 ApplicationComponent 和 Module 的 Scope 是不一样的，则在编译时报错。
- 代码可读性，让程序猿更好的了解 Module 中创建的类实例是单例。

#### 2.3 组织 Component
我们已经把一个 App 按照上面的规则划分为不同的 Component，全局类实例也创建了单例模式。问题来了其他的 Component 想要把全局的类实例注入到目标类中该怎么办呢？这就涉及到类实例共享的问题了，因为 Component 有管理创建类实例的能力。因此只要能很好的组织 Component 之间的关系，问题就好办了。具体的组织方式分为以下3种：

- a. 依赖方式  
一个 Component 是依赖于一个或多个 Component，Component 中的 dependencies 属性就是依赖方式的具体实现

- b. 包含方式   
一个 Component 是包含一个或多个 Component 的，被包含的 Component 还可以继续包含其他的 Component。这种方式特别像 Activity 与 Fragment 的关系。SubComponent 就是包含方式的具体实现。

- c. 继承方式  
官网没有提到该方式，具体没有提到的原因我觉得应该是，该方式不是解决类实例共享的问题，而是从更好的管理、维护 Component 的角度，把一些 Component 共有的方法抽象到一个父类中，然后子 Component 继承。

### 3. Scope
Scope 真正用处就在于 Component 的组织。

- 更好的管理 Component 之间的组织方式，不管是依赖方式还是包含方式，都有必要用自定义的 Scope 注解标注这些 Component，这些注解最好不要一样了，不一样是为了能更好的体现出 Component 之间的组织方式。还有编译器检查有依赖关系或包含关系的 Component，若发现有 Component 没有用自定义 Scope 注解标注，则会报错。
- 更好的管理 Component 与 Module 之间的匹配关系，编译器会检查 Component 管理的 Modules，若发现标注 Component 的自定义 Scope 注解与 Modules 中的标注创建类实例方法的注解不一样，就会报错。
- 可读性提高，如用 Singleton 标注全局类，这样让程序猿立马就能明白这类是全局单例类。


## Dagger2 终结
依赖注入具体步骤：
```
步骤1：查找Module中是否存在创建该类的方法。
步骤2：若存在创建类方法，查看该方法是否存在参数
    步骤2.1：若存在参数，则按从**步骤1**开始依次初始化每个参数
    步骤2.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
步骤3：若不存在创建类方法，则查找Inject注解的构造函数，看构造函数是否存在参数
    步骤3.1：若存在参数，则从 ** 步骤1 ** 开始依次初始化每个参数
    步骤3.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
```

注意：
- 一个 App 必须要有一个 Component（名字可以是 ApplicationComponent）用来管理 App 的整个全局类实例
- 多个页面可以共享一个 Component
- 不是说 Component 就一定要对应一个或多个 Module， Component 也可以不包含 Module
- 自定义 Scope 注解最好使用上，虽然不使用也是可以让项目运行起来的，但是加上好处多多。

Show me the [code](https://github.com/niuxiaowei/Dagger2Sample).   
reference  
- [https://www.jianshu.com/p/cd2c1c9f68d4](https://www.jianshu.com/p/cd2c1c9f68d4)
- [https://www.jianshu.com/p/22c397354997](https://www.jianshu.com/p/22c397354997)




