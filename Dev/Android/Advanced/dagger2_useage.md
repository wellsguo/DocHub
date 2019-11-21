## 命名规约

**@Provides**方法用 provide 前缀命名  
**@Module** 用 Module 后缀命名  
**@Component** 以 Component 作为后缀

简单的说，就是一个工厂模式，由 Dagger 负责创建工厂，帮忙生产 instance。遵从 Java 规范`JSR 330`，可以使用这些注解。现在不研究 Dagger2 是如何根据注解去生成工厂的，先来看看工厂是什么东西，理解为什么可以实现了 DI(Dependency Injection)，如何创建 IoC(Inverse of Control)容器。

## Dagger2 是通过依赖注入完成类的初始化

这个过程需要三部分：

**[#]()1 依赖提供方（生产者）**  
**[#]()2 依赖注入容器（桥梁）**  
**[#]()3 依赖需求方（消费者）**

## Dagger2 是怎么选择依赖提供的呢?

规则是这样的：

- 步骤 1：查找 Module 中是否存在创建该类的方法
- 步骤 2：若存在创建类方法，查看该方法是否存在参数
  - 步骤 2.1：若存在参数，则按从步骤 1 开始依次初始化每个参数
  - 步骤 2.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
- 步骤 3：若不存在创建类方法，则查找 Inject 注解的构造函数，看构造函数是否存在参数
  - 步骤 3.1：若存在参数，则从步骤 1 开始依次初始化每个参数
  - 步骤 3.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束

在使用 `@Component` 的时候必须要提供 `scope` 范围，标准范围是 `@Singleton`  
`@Component` 在使用 `@Module` 的时候必须匹配相同的 `scope`  
能使用 `Singleton` 的时候，要注意标注，否则默认多例

```java
@ActivityScope
@Component(modules = UserModule.class, dependencies = AppComponent.class)
public interface UserComponent {
    void inject(UserActivity activity);
    @Component.Builder
    interface Builder {
        @BindsInstance
        UserComponent.Builder view(UserContract.View view);
        UserComponent.Builder appComponent(AppComponent appComponent);
        UserComponent build();
    }
}
```

> 在上面的示例中，注解 @Component 实现 Dagger 的中的桥接功能，其中 modules = {...} 引入依赖的的源，而`inject(UserActivity activity)`则引入了使用依赖源的目标。

## 总结

### @Inject

主要有两个作用

**[#]()1 作为依赖注提供方：**

使用 `@Inject` 注解构造方法。
注解类的构造函数，让 `Dagger2` 帮我们实例化该类，并注入。

**[#]()2 作为依赖需求方:**

使用 `@Inject` 注解成员。  

如果一个成员变量被 `@Inject` 注解修饰，并且成员类的构造函数也被 `@Inject` 注解，那么 `dagger2` 帮我们实例化该成员类，并注入。  

通常在需要依赖的地方使用这个注解。换句话说，你用它告诉 `Dagger` 这个类或者字段需要依赖注入。这样，`Dagger` 就会构造一个这个类的实例并满足他们的依赖。  

使用 `@Inject` 可以让 `IoC` 容器负责生成 `instance`，如果没有这个注解，`dagger` 将不认识，当做普通类，无法代理

### @Module

**[#]()1 @Module 注解类，负责管理依赖。**

Module 其实是一个简单工厂模式，Module 里面的方法都是创建相应类实例的方法。

**[#]()2 通过@Module 获得第三方类库的对象。**

**[#]()3 @Module 是一个依赖提供方的合集。**

```java
@Module
public class AModule {

    @Provides
    public Gson provideGson(){
        return new Gson();
    }

}
```

### @Provides

**[#]()1 注解@Module 类中的方法。**

在 modules 中，我们定义的方法是用这个注解，以此来告诉 Dagger 我们想要构造对象并提供这些依赖。

### @Component

**[#]()1 @Component 一般用来注解接口。**

**[#]()2 负责在@Inject 和@Module 之间建立连接。**

也可以说是@Inject 和@Module 的桥梁，它的主要作用就是连接这两个部分。

**[#]()3 实例化@Inject 注解的类时，遇到没有构造函数的类依赖，则该依赖由@Module 修饰的类提供。**

**[#]()4 依赖注入容器只是一个接口 interface。**

> Component 需要引用到目标类的实例，Component 会查找目标类中用 Inject 注解标注的属性，查找到相应的属性后会接着查找该属性对应的用 Inject 标注的构造函数（这时候就发生联系了），剩下的工作就是初始化该属性的实例并把实例进行赋值。因此我们也可以给 Component 叫另外一个名字注入器（Injector）

> Component 注解的类,再编译之后,会生产一个以 Dagger+类名的一个类,如下面的 MainComponent 会生成类 DaggerMainComponent(补充一点,Kotlinkapt 编译生成类的位置:\build\generated\source\kapt\debug),我们需要在目标类 MainActivity 中加入下面代码

```java
DaggerMainComponent.builder()
    .build()
    .inject(this)
```

DaggerMainComponent 使用了建造者设计模式,inject 方法是我们 MainComponent 中定义的,这样目标类就和 Component 建立了联系.Component 会去遍历使用@Inject 注解的常量,然后去查找对应的类是否有@Inject 注解的构造方法,如果没有就会报异常.

```java
@Component {modules = {HeaterModule.class, PumperModule.class}}
public interface MachineComponent {
    void inject(CoffeeMachine machine);
}
```

dagger 中 Component 就是最顶级的入口，dagger 为之生成了工厂类 `DaggerMachineComponent`，目标是构建 `CoffeeMachine`， 在 `CoffeeMachine` 中使用了 `@Injection`，那么依赖要由工厂类来提供。工厂类是根据 modules 的参数来找依赖绑定的。

本例中，指向了 `HeaterModule`, `PumperModule`，意思是 `CoffeeMachine` 的依赖要从这些 `module` 里找。

## 工厂名称生成规则

- 如果 Component 是接口, 则生成 `Dagger+接口名`

- 如果 Component 是内部接口，比如本例，则生成 `Dagger+类名+ _+ 接口名`

### @Scope

Scopes 可是非常的有用，Dagger2 可以通过自定义注解限定注解作用域。后面会演示一个例子，这是一个非常强大的特点，因为就如前面说的一样，没 必要让每个对象都去了解如何管理他们的实例。在 scope 的例子中，我们用自定义的 `@PerActivity` 注解一个类，所以这个对象存活时间就和 activity 的一样。简单来说就是我们可以定义所有范围的粒度(@PerFragment, @PerUser, 等等)。

### Qualifier

当类的类型不足以鉴别一个依赖的时候，我们就可以使用这个注解标示。例如：在 Android 中，我们会需要不同类型的 context，所以我们就可以定义 qualifier 注解“@ForApplication”和“@ForActivity”，这样当注入一个 context 的时候，我们就可以告诉 Dagger 我们想要哪种类型的 context。

## DEMO

```java
  /**
   * View 层，负责界面的展示
   */
  public class TestActivity extends AppCompatActivity implements IView{
    // 当一个成员变量被@Inject 注解修饰，并且它的类型构造函数也被@Inject 注解修饰,
    // dagger2 就会自动实例化该成员类型，并注入到该成员变量
    @Inject
    TestPresent mPresent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test);
        DaggerTestComponent.builder().testModule(new TestModule(this)).build().inject(this);
        // @Component 负责连接起 @Inject 和 @Module 注解
        mPresent.updateUI();
    }

    @Override
    public void updateUI(String text) {
        ((TextView)findViewById(R.id.textview)).setText(text);
    }
  }
```

```java
  /**
   * Present 类，调用 Model 层的业务方法，更新 View 层的界面展示
   */
  public class TestPresent {
    IView mView;

    // Dagger2 遇到 @Inject 标记的成员属性，就会去查看该成员类的构造函数，
    // 如果构造函数也被 @Inject 标记,则会自动初始化，完成依赖注入。
    @Inject
    TestModel mModel;

    //TestPresent 的构造函数也被 @Inject 注解修饰
    @Inject
    public TestPresent(IView view){
        this.mView=view;
    }

    public void updateUI(){
        mView.updateUI(mModel.getText());
    }
  }
```

```java
  /**
   * Model 类，实现具体的业务逻辑
   */
  public class TestModel {
    //构造函数用 @Inject 修饰
    @Inject
    public TestModel(){
    }

    public String getText(){
        return "Dagger2 应用实践...";
    }
  }
```

```java
  /**
   * Module 类提供那些没有构造函数的类的依赖，如第三方类库，系统类，接口类
   */
  @Module
  public class TestModule {
    private IView mView;

    public TestModule(IView iView){
        this.mView=iView;
    }

    //@Provides 注解的方法，提供 IView 类的依赖。
    @Provides
    public IView provideIView(){
        return this.mView;
    }
  }
```

```java
  /**
   * Component 必须是一个接口类或者抽象
   */
  @Component(modules = TestModule.class)
  public interface TestComponent {
    void inject(TestActivity testActivity);
  }
```
