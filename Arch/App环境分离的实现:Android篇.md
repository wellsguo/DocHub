# [App环境分离的实现:Android篇](https://keeganlee.me/post/architecture/20160329/)

- *[App环境分离的实现:Android篇]()* 
- *[App环境分离的实现:iOS篇]()*

我在App架构经验总结中有简单提到环境分离的实现方案，但没有深入讲实现细节。本系列则打算用两篇文章分别详细讲讲Android和iOS环境分离的具体实现，本篇则先讲Android的实现。

## 概念解析

本文的实现方案是基于Gradle的，因此，有几个概念需要先了解清楚。

### applicationId

没有Gradle之前，我们都知道，包名是Android程序的唯一标识，通过在AndroidManifest.xml文件中定义package属性。同时，这个包名也是引用资源的路径名，即R资源文件的包名。

引入Gradle之后，就多了一个applicationId的概念。官方解释是：**applicationId是程序的唯一标识，而package则用来引用R类以及解析相关的activity/service注册操作**。因此，可以设置多个不同的applicationId，对应多个不同版本的apk，而package则保持一致。新建的项目默认applicationId和package是一样的。

### Product Flavors

通过Product Flavors可以创建不同的产品渠道版本，网上流行的多渠道打包方案大部分都是通过添加多个渠道的Flavors来实现的。Flavors一般设置的属性如下图，当然，实际上不只是这些，例如manifestPlaceholders就不在此设置界面里。默认有defaultConfig这个Flavors。

### Build Types

Build Types则是构建类型。默认提供debug和release两种类型，如下图所示。主要提供是否可调试、是否混淆等构建打包时的相关配置。

### Build Variants

Product Flavors和Build Types的组合形成了多个Build Variant，例如，如果有两个Product Flavors版本：

```groovy
productFlavors {
    free { ... }
    enterprise { ... }
}
```

而Build Types也有两种类型：

```groovy
buildTypes {
    debug { ... }
    release { ... }
}
```

那么，组合出来的Build Variant就有四个版本了：

- freeDebug
- freeRelease
- enterpriseDebug
- enterpriseRelease

## 环境分离实现

相关概念都了解清楚了，那么，环境分离具体如何实现呢？其实，实现方案不止一个，这里，我提供两个方案，一个可以使用Product Flavors实现，一个可以使用Build Types来实现。

### 方案一

Product Flavors用来定义产品渠道，假如我们有两个环境：测试环境和生产环境。那么，定义两个Flavors分别对应测试环境和生产环境，并且applicationId不同，可以如下定义：

```groovy
productFlavors {
    beta { 
        applicationId 'com.domain.productname.beta'
    }
    production {
        applicationId 'com.domain.productname'
    }
}
```

这样，测试环境和生产环境实际上等于是已经分开的两个app了，已经可以在同一个设备里同时安装测试版本和生产版本了。但这样是不够的，两个app将会一模一样，很难区分。因此，我们也要修改两个环境版本的应用名称，同时还要使用不同的应用图标。怎么做呢？

在app模块，src目录下，新建一个与main目录同级的beta目录，beta目录的结构如下图：


新建的beta目录对应于productFlavors的beta版本，beta版本目录下的图片资源ic_launcher.png对应于beta版本的应用图标，这要与main目录的ic_launcher.png保持一致的位置和名称，只是图片不同。而beta版本的strings.xml则只需要包含一个属性，如下：

```xml
<resources>
    <string name="app_name">appNameBeta</string>
</resources>
```

至此，当运行beta版的Build Variant时，则会看到beta版的应用图标和应用名称也与生产版的不同了。

这里要说明一下原理。首先，productFlavors定义的每个渠道是会继承自defaultConfig的，就是说上面定义的beta和production都继承了defaultConfig。然后，productFlavors每个渠道里自定义的属性会覆盖defaultConfig相应的属性，beta和production定义了applicationId，则会覆盖了defaultConfig的applicationId。这里，因为production自定义的applicationId和defaultConfig的applicationId是一样的，所以其实也可以取消applicationId的自定义。

而对于源代码部分，当运行beta版的Build Variant时，默认会引用main目录的资源文件，而beta目录下的资源会覆盖main目录相应位置的资源，例如上面beta目录下的mipmap目录的ic_launcher.png就会覆盖main目录下相应位置的ic_launcher.png；同样的，beta下的strings.xml里定义的app_name就会覆盖main目录下的strings.xml定义的app_name。

但对于java类则不同，beta里定义的java类并不会覆盖main目录里相应的java类。事实上，两个目录的java类只能有一份，否则会出现类重复的错误。如果beta和production版本需要有同个页面不同的实现，例如有一个Activity需要不同的实现，那么，只能新建一个production版本目录，然后该Activity类在beta和production都有一份拷贝，代码实现可以不同，但main目录下则不能有该Activity类。

### 方案二

前面就已经说过，Build Types默认提供了debug和release两种类型，其实也可以分别对应于测试和生产环境。在Build Types的设置界面中，可以看到有个 **`Application Id Suffix`** 的设置选择，这个可以用来设置 **`applicationId`** 的后缀。这个后缀是相对于Flavors来说的，比如我们定义了一个如下的productFlavors：

```groovy
productFlavors {
    free { 
        applicationId 'com.domain.productname.free'
    }
    enterprise {
        applicationId 'com.domain.productname'
    }
}
```

而debug类型的Application Id Suffix设置为“.debug”，那么对应的

- freeDebug 版本的 applicationId 就是’com.domain.productname.free.debug’，而
- enterpriseDebug 版本的 applicationId 则是’com.domain.productname.debug’。

对于本方案二来说，并不需要再定义额外的productFlavors，使用默认的即可。那么，debug类型的Application Id Suffix可设置为”.debug”，release类型则无需设置。

接着，src目录下新建一个debug目录，和方案一的beta目录完全一样，只是目录名称不同。另外，如果两个版本需要有同个页面不同的实现，那么，也和方案一一样，需要新建个release目录，和production目录一样。

## 写在最后

如果只是从环境分离来说的话，我更倾向于方案二，因为系统默认就提供了debug和release两个版本，而对应的Build Variant也只有两个。如果采用方案一，那么将产生四个Build Variant，这显得有点多余。
