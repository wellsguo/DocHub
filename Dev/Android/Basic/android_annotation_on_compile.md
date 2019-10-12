# Android编译时注解

之前写了注解基础和运行时注解这篇文章，里面使用运行时注解来模仿ButterKnife绑定控件ID的功能，运行时注解主要是运行时使用反射来找到注解进行一些操作；反射存在一定的性能问题，而且一般使用了注解的框架都是使用编译时注解

仔细看了一下这篇文章，Android 如何编写基于编译时注解的项目，自己尝试写了代码理解了一番，感觉还是比较有意思的；

## 实现原理

1. 注解处理器（Annotation Processor）：用来在编译时扫描和处理注解，我们需要实现自己的注解处理器，去处理我们自己的注解，一般就是去生成我们需要的代码文件；

2. 我们实现的注解处理器会被打包成jar在编译的过程中调用，为了让java编译器识别出这个自定义的注解处理器，我们需要注册一下

需要使用到注解处理的插件，因为Android Studio原本是不支持注解处理器的
整个流程大概就是，我们先`创建注解`，`创建注解处理器`，然后代码中`使用注解`；在编译的时候注解处理插件会使用我们的注解处理器去处理注解，生成相应的代码；

## 具体实现

### 创建注解
还是以实现一个ViewById注解为例，在项目中新创建一个Java Library，模块名为annotation用来保存所有注解，然后创建一个编译时注解

```java
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.CLASS)
public @interface ViewById {
    int value() default -1;
}
```

### 注解处理器的创建和注册

注解处理器是必须放在一个Java Library中，所以创建一个annotator模块，用来实现注解处理器，这里通过创建类IocProcessor继承AbstractProcessor重写其中方法来实现一个注解处理器

```java
@AutoService(Processor.class)
public class IocProcessor extends AbstractProcessor {
...
```

注册有比较简单的方法，只需要给IocProcessor加一个AutoService注解就可以实现注册，这个注解需要依赖一个库

```groovy
implementation 'com.google.auto.service:auto-service:1.0-rc4'
implementation project(':annotation')
```

重写init方法，获取一些有用的变量

```java
    /**
     * 生成代码用的
     */
    private Filer mFileUtils;

    /**
     * 跟元素相关的辅助类，帮助我们去获取一些元素相关的信息
     * - VariableElement  一般代表成员变量
     * - ExecutableElement  一般代表类中的方法
     * - TypeElement  一般代表代表类
     * - PackageElement  一般代表Package
     */
    private Elements mElementUtils;
    
    @Override
    public synchronized void init(ProcessingEnvironment processingEnv) {
        super.init(processingEnv);
        mFileUtils = processingEnv.getFiler();
        mElementUtils = processingEnv.getElementUtils();
    }
```

重写getSupportedAnnotationTypes方法，支持自己的注解

```java
    /**
     * 添加需要支持的注解
     *
     * @return
     */
    @Override
    public Set<String> getSupportedAnnotationTypes() {
        Set<String> annotationTypes = new LinkedHashSet<String>();
        //添加需要支持的注解
        annotationTypes.add(ViewById.class.getCanonicalName());
        return annotationTypes;
    }
```
这个固定写法是设置支持的版本

```java
    @Override
    public SourceVersion getSupportedSourceVersion() {
        return SourceVersion.latestSupported();
    }
```

然后是最重要的process方法，这个方法就是开始处理注解，这里是先保存获取到的被注解的元素，以外部类为单元，用ProxyInfo对象去保存一个类里面的所有被注解的元素；用mProxyMap去保存所有的ProxyInfo；然后再一个个拿出来，使用了ProxyInfo对象去实现生成代码

```java
        mProxyMap.clear();
        //获取被注解的元素
        Set<? extends Element> elements = roundEnvironment.getElementsAnnotatedWith(ViewById.class);
        for (Element element : elements) {
            //检查element类型
            if (!checkAnnotationValid(element, ViewById.class)) {
                return false;
            }
            //获取到这个成员变量
            VariableElement variableElement = (VariableElement) element;
            //获取到这个变量的外部类，所在的类
            TypeElement typeElement = (TypeElement) variableElement.getEnclosingElement();
            //获取外部类的类名
            String qualifiedName = typeElement.getQualifiedName().toString();
            //一个类里面的注解都在一个ProxyInfo中处理
            ProxyInfo proxyInfo = mProxyMap.get(qualifiedName);
            if (proxyInfo == null) {
                proxyInfo = new ProxyInfo(mElementUtils, typeElement);
                mProxyMap.put(qualifiedName, proxyInfo);
            }
            //把这个注解保存到proxyInfo里面，用于实现功能
            ViewById annotation = variableElement.getAnnotation(ViewById.class);
            int id = annotation.value();
            proxyInfo.injectVariables.put(id, variableElement);
        }


        //生成类
        for (String key : mProxyMap.keySet()) {
            ProxyInfo proxyInfo = mProxyMap.get(key);
            try {
                //创建一个新的源文件，并返回一个对象以允许写入它
                JavaFileObject jfo = mFileUtils.createSourceFile(
                        proxyInfo.getProxyClassFullName(),
                        proxyInfo.getTypeElement());
                Writer writer = jfo.openWriter();
                writer.write(proxyInfo.generateJavaCode());
                writer.flush();
                writer.close();
            } catch (IOException e) {
                error(proxyInfo.getTypeElement(),
                        "Unable to write injector for type %s: %s",
                        proxyInfo.getTypeElement(), e.getMessage());
            }
        }
        return true;
```
到这里其实都很好理解，拿到了注解的这个元素（对象），就知道它的一切信息，就可以去生成相应的代码，主要在于生成代码，是在上面代码中的这个地方实现的

```java
//创建一个新的源文件，并返回一个对象以允许写入它
JavaFileObject jfo = mFileUtils.createSourceFile(
        proxyInfo.getProxyClassFullName(),
        proxyInfo.getTypeElement());
Writer writer = jfo.openWriter();
writer.write(proxyInfo.generateJavaCode());
writer.flush();
writer.close(); 
```

这里去创建Java对象，写入代码，其中创建新的源文件需要传入两个参数，一个是保存的文件的全路径，你想保存在哪里就哪里随便写，我是保存在被注解的这个变量所在类的同一个包下，另一个参数是传入一个基本元素，但是说实话，这个基本元素我在网上查了很久，不知道这个东西有什么用，删了也没问题，直接删了好了；

代码是通过proxyInfo.generateJavaCode()来获取的相应生成的代码去生成对象的，是具体生成代码的方法

```java
    /**
     * 生成代码
     *
     * @return
     */
    public String generateJavaCode() {
        StringBuilder builder = new StringBuilder();
        builder.append("// Generated code. Do not modify!\n");
        builder.append("package ").append(packageName).append(";\n\n");
        builder.append("import com.dhht.annotation.*;\n");
        builder.append("import com.dhht.annotation.R;\n");
        builder.append("import com.dhht.annotationlibrary.*;\n");
        builder.append('\n');

        builder.append("public class ").append(proxyClassName).append(" implements " + ProxyInfo.PROXY + "<" + typeElement.getQualifiedName() + ">");
        builder.append(" {\n");

        generateMethods(builder);
        builder.append('\n');

        builder.append("}\n");
        return builder.toString();
    }
```

就是使用字符串组建一下代码，字符串拼接倒是非常简单，这里也没有展示完全，可以看看拼接出来的代码，我稍微优化了一下格式；这里有专门生成代码的库可以使用，比字符串拼接好用，叫**Javapoet**

```java
package com.dhht.annotation.activity;

import com.dhht.annotation.*;
import com.dhht.annotation.R;
import com.dhht.annotationlibrary.*;

public class MainActivity$$ViewInject implements ViewInject<com.dhht.annotation.activity.MainActivity> {
    @Override
    public void inject(com.dhht.annotation.activity.MainActivity host, Object source) {
        if (source instanceof android.app.Activity) {
            host.txtView = (android.widget.TextView) (((android.app.Activity) source).findViewById(R.id.txtView));
        } else {
            host.txtView = (android.widget.TextView) (((android.view.View) source).findViewById(R.id.txtView));
        }
    }
}
```

可以调用生成的这个类的inject()方法，为传入的host对象的.txtView控件进行初始化，这里只是在MainActivity里面用了，如果在其他类里面则会生成很多个这样的文件，而且当这个类不是Activity的时候需要传入这个控件的根布局进去；

### 调用生成的代码
里面还有一些检查参数是不是公共的呀，注解的对象属性是否正确呀，具体的代码生成可以下载源码看看，都是比较简单的；现在注解器处理器算是写完了，需要在我们的项目中使用，我们也新建一个Android Library，annotationlibrary专门用于提供API，这样注解的实现完全和我们的项目分开;

```groovy
//这个依赖是用于对外暴露注解的
api project(':annotation')
```

需要实现的功能很简单，就是调用生成的代码，首先不同的类里面的注解生成的代码类是不一样的，而且生成的代码是编译的时候才生成的，肯定只能使用反射来获取这个生成的类，所以肯定需要传入使用注解的这个类，然后根据我们的命名规则获取到；

```java
    /**
     * 根据使用注解的类和约定的命名规则，反射获取注解生成的类
     *
     * @param object
     * @return
     */
    private static ViewInject findProxyActivity(Object object) {
        try {
            Class clazz = object.getClass();
            Class injectorClazz = Class.forName(clazz.getName() + SUFFIX);
            return (ViewInject) injectorClazz.newInstance();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        throw new RuntimeException(String.format("can not find %s , something when compiler.", object.getClass().getSimpleName() + SUFFIX));
    }
```
再说我们这个绑定控件，从生成的代码来看，需要一个Activity或者一个View来调用findViewById方法，所以使用注解的不是Activity的类，在需要加一个Object参数，传入View进来；

```java
public interface ViewInject<T> {
    /**
     * 提供给生成的代码去绑定id用的
     *
     * @param t
     * @param source
     */
    void inject(T t, Object source);
}
```

然后考虑到Activity就不用传另一个参数了，所以新建两个方法完事儿

```java
    public static void injectView(Activity activity) {
        ViewInject proxyActivity = findProxyActivity(activity);
        proxyActivity.inject(activity, activity);
    }

    public static void injectView(Object object, View view) {
        ViewInject proxyActivity = findProxyActivity(object);
        proxyActivity.inject(object, view);
    }
```
然后在项目中依赖一下，并且使用之前说的注解插件

```groovy
implementation project(':annotationlibrary')
annotationProcessor project(':annotator')
```

然后就可以在项目中使用注解了

```java
    @ViewById
    TextView txtView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ViewInjector.injectView(this);
        txtView.setOnClickListener(v -> Toast.makeText(MainActivity.this, "醉了", Toast.LENGTH_SHORT).show());
    }
```
使用了lambda 表达式简单了不少，在模块的build.gradle的android节点下面添加支持

```groovy
compileOptions {
    sourceCompatibility = '1.8'
    targetCompatibility = '1.8'
}
```

就完成了，整体还是比较好理解的，关键在于得下载代码自己试试

项目地址：https://github.com/tyhjh/Annotation