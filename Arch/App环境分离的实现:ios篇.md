# [App环境分离的实现:iOS篇](https://keeganlee.me/post/architecture/20160329/)

- *[App环境分离的实现:Android篇]()* 
- *[App环境分离的实现:iOS篇]()*



说到App环境分离在iOS的实现，我曾在iOS技术群里问过：如何实现在同一台手机能同时安装同个应用的测试和生产版本？应用名称要有区分，图标也要有所区别。不要手动修改Bundle id和应用名称，也不要手动替换图标，更不要维护两个项目。如何才能简单地实现？

结果发现很多人都不知道该怎么实现。其实，实现方案很简单，只要建立多个Target即可。当然，有些细节问题要注意，不然会出错。接下来，看如何一步步地实现环境分离。

## 复制Target

关于Xcode中Target的概念，文档中有这么一段说明：


> A target specifies a product to build and contains the instructions for building the product from a set of files in a project or workspace. A target defines a single product; it organizes the inputs into the build system—the source files and instructions for processing those source files—required to build that product. Projects can contain one or more targets, each of which produces one product.


即是说，每个Target代表一个编译的产品。每个Target，可以有不同的编译源文件和资源文件。那么，实现环境分离的方案，就是分别建立测试环境和生产环境的两个Target。默认的Target作为生产环境的Target，在此基础上复制多一个Target作为测试环境的Target。

如下图，选择默认的Target，从右键菜单中选择Duplicate，就可以复制出一个新的Target了。


新Target默认名称为productname copy。复制完成后，不只是TARGETS列表中多出了名为productname copy的新Target，同时也会为该新Target生成名为productname copy的新的scheme，以及在项目的根目录下生成productname copy-Info.plist文件。

## 更名Target

不喜欢productname copy这样的名字，productnameBeta这样的名字才是测试版本该有的名字。那么，需要改名的地方有三处：target名称、scheme名称、plist文件名称。

修改target名称很简单，只要在TARGETS列表中选中后，再点击一下即可编辑修改名称。修改scheme则可以在Xcode左上角的Run\Stop按钮右边的scheme列表菜单中选择Manage Schemes，打开弹出框，如下图，则可将productname copy修改为productnameBeta


plist文件则修改为productnameBeta-Info.plist，同时，我还将其移到与默认的Info.plist文件在同个目录下。不只是在同一个分组下，也是在同一个物理目录下。改完plist文件后，还需要修改productnameBeta的Target的Info.plist File设置，该属性设置了相应Target绑定的plist文件是哪个。该属性值本来为productname copy-Info.plist，现需要更改为productname/productnameBeta-Info.plist。

## 修改配置

接下来，就要修改Target的配置，实现真正的环境分离了。默认的productname的Target，作为生产版本，基本不需要改动，需要改的是作为测试版的productnameBeta。

首先，修改productnameBeta的Bundle id，在原有的基础上添加后缀“.beta”，以实现能和生产版同时安装在同一台设备上。

接着，修改Bundle display name，可在原有名称的基础上添加后缀“Beta”，以实现和生产版应用名称上的区分。

然后，需要更换图标了。默认会使用AppIcon这一项Assets，但AppIcon是给生产版设置的图标，既然测试版要使用不同图标，那就需要新建一套新的App Icon，如下图：


新建的App Icon将其命名为AppIcon-Beta，放置测试版的图标。并将productnameBeta的App Icons Source指定为新建的AppIcon-Beta。至此，图标也与生产版的有所区别了。

## 判别Target

那么，设置了不同Target后，代码上可能需要根据不同Target做不同处理，因此，需要在代码上能判断当前编译的是哪个Target。这可以通过预编译宏来区分。例如，我们在productnameBeta的Build Settings中，将Preprocessor Macros属性值设置为BETA，也就是为productnameBeta定义了一个预编译宏，宏名称为BETA。


然后，在代码中可以通过如下预编译指令判断当前是在哪个Target下：

```
#ifdef BETA
    // 测试版需要执行的代码
#else
    // 默认生产版需要执行的代码
#endif
```

## 写在最后

通过多个Target可以实现环境的分离，本文的实现很简单。而关于Target的用法也不只限于此，若想了解Target更多高级用法，可查询相关资料，在此就不展开了。
