## Android 模块化开发

[1] [Android 模块化探索与实践](https://www.cnblogs.com/baronzhang/p/6861258.html)  
[2] [Android 模块化完整方案实现](https://blog.csdn.net/yalinfendou/article/details/78822749)  
[3] [关于Android模块化我有一些话不知当讲不当讲](https://www.jianshu.com/p/910911172243)  
[4] [Android组件化开发实践](https://www.jianshu.com/p/186fa07fc48a)



#### `Q1` 为什么要采用模块化的方法进行开发？

`A` 随着移动平台的不断发展，移动平台上的软件慢慢走向复杂化，体积也变得臃肿庞大；为了降低大型软件复杂性和耦合度，同时也为了适应模块重用、多团队并行开发测试等等需求，模块化在 Android 平台上变得势在必行。阿里 Android 团队在年初开源了他们的容器化框架 Atlas 就很大程度说明了当前 Android 平台开发大型商业项目所面临的问题。<sup>[[1]](https://www.cnblogs.com/baronzhang/p/6861258.html)</sup>

模块化的同时也带来相应的好处：
  - 多团队并行开发测试；
  - 模块间解耦、重用；
  - 可单独编译打包某一模块，提升开发效率。

#### `Q2` 如何实现模块间的跳转？
`A` 拆分业务代码时，自然会涉及到跨 Module 的 Activity 跳转，当单独编译时，自然是不能获取到其他模块的引用的。有几种方式可以实现跨模块的唤起 Activity：<sup>[[4]](https://www.jianshu.com/p/186fa07fc48a)</sup>

- **隐式启动**  
通过设置 intent-filter 实现，这需要在 manifest 中**插入大量代码**，同时也**降低了安全性**（其它 App 就可以通过这种方式随意启动）。

- **通过类名跳转**  
Android 业务组件化开发实践提出了一种通过类名跳转的方式，使用脚本生成 Rlist 类，比较方便快捷，但** Activity 间数据传递不方便**。

- **Scheme 跳转**  
Scheme 方式是建立映射表，集中处理 Activity，这种方式可以传递一定的数据。Activity 传递大量数据时可以通过 EventBus 来进行传递（其实即使通过 intent 显示启动，也不要把大量数据放置在 intent 中，intent 对数据大小有限制）。

在进行本次实践时找到 GitHub 上的一个 Router 项目，同时支持 HTTP 和程序内 Activity 跳转，而且通过注解的方式进行，使用非常方便。项目地址 [ActivityRouter](https://github.com/mzule/ActivityRouter) 。 ActivityRouter 的 readme 中有比较详细的 wiki。

---

`A2` 当一个大项目拆成若干小项目时候，调用方式也随之发生了少许改变。App 各模块间的数据通信有以下几种方式：<sup>[[3]](https://www.jianshu.com/p/910911172243)</sup>

- **页面跳转**：比如，在订单页面下单时候，需要判断用户是否登录，如果没有则需要跳到登录界面。
- **主动获取数据**：比如，在下单时候，用户已经登录，下单需要传递用户的基本信息。
- **被动获得数据**：比如，在切换用户的时候，有时候需要更新数据，如订单页面，需要把原先用户的购物车数据给清空。



#### `Q3` 如何解决资源冲突问题？
`A` 对于多个 Bussines Module 中资源名冲突的问题，可以通过在 build.gradle 定义前缀的方式解决：
```
defaultConfig {
   ...
   resourcePrefix "new_house_"
   ...
}
```
而对于 Module 中有些资源不想被外部访问的，我们可以创建 res/values/public.xml，添加到 public.xml 中的 resource 则可被外部访问，未添加的则视为私有：
```
<resources>
    <public name="new_house_settings" type="string"/>
</resources>
```

#### `Q4` 如何进行模块划分？模块划分粒度？

`A1` 以安居客为例<sup>[[1]](https://www.cnblogs.com/baronzhang/p/6861258.html)</sup>
![安居客模块化实例剖析](https://images2015.cnblogs.com/blog/639237/201705/639237-20170516142733947-1083157483.png)

整个项目分为三层，从下至上分别是：

 - **Basic Component Layer**: 基础组件层，顾名思义就是一些基础组件，包含了各种开源库以及和业务无关的各种自研工具库；
 - **Business Component Layer**: 业务组件层，这一层的所有组件都是业务相关的，例如上图中的支付组件 AnjukePay、数据模拟组件 DataSimulator 等等；
 - **Business Module Layer**: 业务 Module 层，在 Android Studio 中每块业务对应一个单独的 Module。例如安居客用户 App 我们就可以拆分成新房 Module、二手房 Module、IM Module 等等，每个单独的 Business Module 都必须准遵守我们自己的 MVP 架构。
 
我们在谈模块化的时候，其实就是将业务模块层的各个功能业务拆分层独立的业务模块。所以我们进行模块化的第一步就是业务模块划分，但是模块划分并没有一个业界通用的标准，因此划分的粒度需要根据项目情况进行合理把控，这就需要对业务和项目有较为透彻的理解。拿安居客来举例，我们会将项目划分为新房模块、二手房模块、IM 模块等等。

对于模块化项目，每个单独的 Business Module 都可以单独编译成 APK。在开发阶段需要单独打包编译，项目发布的时候又需要它作为项目的一个 Module 来整体编译打包。简单的说就是开发时是 Application，发布时是 Library。因此需要在 Business Module 的 build.gradle 中加入如下代码：
```
if(isBuildModule.toBoolean()){
    apply plugin: 'com.android.application'
}else{
    apply plugin: 'com.android.library'
}
```
> isBuildModule 在项目根目录的 gradle.properties 中定义:  ```isBuildModule=false```

同样 Manifest.xml 也需要有两套：
```
sourceSets {
   main {
       if (isBuildModule.toBoolean()) {
           manifest.srcFile 'src/main/debug/AndroidManifest.xml'
       } else {
           manifest.srcFile 'src/main/release/AndroidManifest.xml'
       }
   }
}
```

#### `Q5` 如何解决重复依赖问题？
`A` 模块化的过程中我们常常会遇到重复依赖的问题，如果是通过 aar 依赖， gradle 会自动帮我们找出新版本，而抛弃老版本的重复依赖。如果是以 project 的方式依赖，则在打包的时候会出现重复类。对于这种情况我们可以在 build.gradle 中将 compile 改为 provided，只在最终的项目中 compile 对应的 library ；

其实从前面的安居客模块化设计图上能看出来，我们的设计方案能一定程度上规避重复依赖的问题。比如我们所有的第三方库的依赖都会放到 OpenSoureLibraries 中，其他需要用到相关类库的项目，只需要依赖 OpenSoureLibraries 就好了。