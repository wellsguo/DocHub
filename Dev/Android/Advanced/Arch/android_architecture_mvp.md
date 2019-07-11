作者：diygreen  
链接：https://www.jianshu.com/p/9a6845b26856#  
來源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。  

## 前言    
2014年年底偶然得知在Android开发中出现了MVP这种模式，当时觉得这东西挺好，正好赶上公司要做一个新的小项目，于是尝试了一下。仿照网上的Demo分出View、Model、Presenter层，抽取View接口，看起来像那么回事的用MVP完成了整个项目。因为项目简单，期间也没有遇到什么坑，但是总觉得还有那些地方不对。当时网上一些关于Android MVP的介绍都有点浅尝辄止，一个登录或者根据地区查询天气等的小Demo，没有实际在项目中应用的示例，所以在用MVP做完一个小项目之后还是不敢在主项目中轻易尝试。首先，主项目比较混乱，改动起来工作量很大，而工期经常较紧，时间不允许；其次，知道自身对MVP理解还不够，怕掉坑里去；最后，也是最重要的一点，当时的项目不是按功能模块划分的包结构，如果改为MVP那是真的就回不到过去了。好了，废话不多说，今天主要是想分享一下，本人对MVP的浅见，以及如何使用MVP模式搭建一个项目框架。纯属一家之言，不足之处，请见谅。

## 一、什么是 MVP

### 1.1. MVP 的定义

MVP，全称 Model-View-Presenter 

要说MVP那就不得不说一说它的前辈——MVC。

MVC（Model-View-Controller，模型-视图-控制器）模式是80年代Smalltalk-80出现的一种软件设计模式，后来得到了广泛的应用，其主要目的在于促进应用中模型，视图，控制器间的关注的清晰分离。MVP（Model-View-Presenter，模型-视图-表示器）模式则是由IBM开发出来的一个针对C++和Java的编程模型，大概出现于2000年，是MVC模式的一个变种，主要用来隔离UI、UI逻辑和业务逻辑、数据。也就是说，MVP 是从经典的模式MVC演变而来，它们的基本思想有相通的地方：Controller/Presenter负责逻辑的处理，Model提供数据，View负责显示。

**说明：**按照View和Presenter之间的交互方式以及View本身的职责范围，Martin Folwer将MVP可分为PV（Passive View）和SoC（Supervising Controller）两种模式。

+ Passive View  
顾名思义，PV（Passive View）是一个被动的View，针对包含其中的UI元素（比如控件）的操作不是由View自身来操作，而交给Presenter来操控。

+ Supervising Controller  
在SoC（Supervising Controller）模式下，为了降低Presenter的复杂度，将诸如数据绑定和格式化这样简单的UI处理逻辑逻辑转移到View中，这些处理逻辑会体现在View实现的接口中。

### 1.2. 发展历程

任何一种思想的产生都有其特定的背景，在软件开发中也是如此。在软件复杂度增长，需求不断变更的客观条件下，为了更好的解决这些问题，出现了各种软件架构思想、编程思想以及设计模式。（因为人的能力并没有“跟上”机器，所以才会出现各种模式、方法、工具等等来补足人的不足，以最大地透支机器性能。--Indream Luo）

相信做过客户端（PC、Android、iOS等）或者前端开发的童鞋都听过MVC、MVP、MVVM这些名词（就算不了解也大致知道有这个东西吧），这些都是为了解决拥有图像界面的程序开发复杂性而产生的模式。这里说的是模式，当然有各种各样的框架方便开发者在项目中应用这种模式，这不是本文重点。

有前辈（Indream Luo）说过，架构是对客观不足的妥协，规范是对主观不足的妥协。对此我深表赞同，先不管这些，我们来看看GUI是怎么和MVX扯上关系的。

先搞清楚一个顺序，是GUI应用程序的出现导致了MVC的产生。GUI应用程序提供给用户可视化的操作界面，这个界面提供给用户数据和信息。在PC上用户与界面的交互主要依赖（键盘，鼠标等。这些操作会执行一些应用逻辑，应用逻辑（application logic）可能会触发一定的业务逻辑（business logic）使应用程序数据的发生变更，数据的变更自然需要用户界面的同步变更以提供最准确的信息。在开发这类应用程序时，为更好的管理应用程序的复杂性，基于职责分离（Speration of Duties）的思想都会对应用程序进行分层。在开发GUI应用程序的时候，会把管理用户界面的层次称为View，应用程序的数据为Model（注意这里的Model指的是Domain Model，这个应用程序对需要解决的问题的数据抽象，不包含应用的状态，可以简单理解为对象）。Model提供数据操作的接口，执行相应的业务逻辑。有了View和Model的分层，那么问题就来了：View如何同步Model的变更，View和Model之间如何粘合在一起。（所谓的MVX中的X都可以归纳为对这个问题不同的处理方式）（引自：戴嘉华）。

#### MVC 的产生
早在上个世纪70年代，美国的施乐公司（Xerox）的工程师研发了Smalltalk编程语言，并且开始用它编写图形界面的应用程序。而在Smalltalk-80这个版本的时候，一位叫Trygve Reenskaug的工程师设计了MVC图形应用程序的架构模式，极大地降低了图形应用程序的管理难度。而在四人帮（GoF）的设计模式当中并没有把MVC当做是设计模式，而仅仅是把它看成解决问题的一些类的集合。Smalltalk-80 MVC和GoF描述的MVC是最经典的MVC模式。

看到这服务端的童鞋有话要说：我们也用MVC，你看Structs、SpringMVC这些都是经典的MVC框架。那服务端的MVC和GUI开发中的MVC有何不同之处了，请看下面的分析。

#### MVC Model 2的出现
在Web服务端开发的时候也会接触到MVC模式，而这种MVC模式不能严格称为MVC模式。经典的MVC模式只是解决客户端图形界面应用程序的问题，而对服务端无效。服务端的MVC模式又自己特定的名字：MVC Model 2，或者叫JSP Model 2，或者直接就是Model 2 。

好吧，说了等于没说，总之一句话，我们今天所说的MVX都有一个前提，那就是得有GUI，得是来解决GUI应用程序开发中遇到的问题的。所以，我们只要关心最经典的MVC就可以了，想了解更多的请自行Google。

#### MVP 的产生
MVP模式是MVC模式的改良。在上个世纪90年代，IBM旗下的子公司Taligent在用C/C++开发一个叫CommonPoint的图形界面应用系统的时候提出来的。

#### MVVM 的产生
MVVM模式最早是微软公司提出，并且了大量使用在.NET的WPF和Sliverlight中。2005年微软工程师John Gossman在自己的博客上首次公布了MVVM模式。

### 1.3. 为什么需要 MVP

（以下内容参考自：MVP在Android平台上的应用，原文作者konmik，译者MiJack）

#### 理由1：尽量简单

如果你还有读过这篇文章，请阅读它：[Kiss原则（Keep It Stupid Simple）](https://link.jianshu.com/?t=https://people.apache.org/~fhanik/kiss.html)

大部分的安卓应用只使用View-Model结构程序员现在更多的是和复杂的View打交道而不是解决业务逻辑。当你在应用中只使用Model-View时，到最后，你会发现“所有的事物都被连接到一起”。




![只使用 Model-View ](https://upload-images.jianshu.io/upload_images/1233754-5f7d98f12dc2496d.png!web?imageMogr2/auto-orient/strip%7CimageView2/2/w/513/format/webp) 

如果这张图看上去还不是很复杂，那么请你想象一下以下情况：每一个View在任意一个时刻都有可能出现或者消失。不要忘记View的保存和恢复，在临时的view上挂载一个后台任务。“所有的事物都被连接到一起”的替代品是一个**万能对象(god object)**。

![god object](https://upload-images.jianshu.io/upload_images/1233754-41f3e3d839c950fc.png!web?imageMogr2/auto-orient/strip%7CimageView2/2/w/550/format/webp)  

god object 是十分复杂的，他的每一个部分都不能重复利用，无法轻易的测试、或者调试和重构。




![使用 MVP](https://upload-images.jianshu.io/upload_images/1233754-eb5b4bc4fbf757be.png!web?imageMogr2/auto-orient/strip%7CimageView2/2/w/550/format/webp)  

复杂的任务被分成细小的任务，并且很容易解决。越小的东西，bug越少，越容易debug，更好测试。在MVP模式下的View层将会变得简单，所以即便是他请求数据的时候也不需要回调函数。View逻辑变成十分直接。

##### 理由2：后台任务
当你编写一个Actviity、Fragment、自定义View的时候，你会把所有的和后台任务相关的方法写在一个静态类或者外部类中。这样，你的Task不再和Activity联系在一起，这既不会导致内存泄露，也不依赖于Activity的重建。这里有若干种方法处理后台任务，但是它们的可靠性都不及MVP。

### 1.4. 为什么 MVP 是可行的？

（以下内容参考自：MVP在Android平台上的应用，原文作者konmik，译者MiJack）

这里有一张表格，用于展示在configuration改变、Activity 重启、Out-Of-Memory时，不同的应用部分会发生什么？

![](https://upload-images.jianshu.io/upload_images/1233754-c600eb346b750910.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/686/format/webp)  

+ 情景 1: 当用户切换屏幕、更改语言设置或者链接外部的模拟器时，往往意味着设置改变。 相关更多请阅读[这里](https://link.jianshu.com/?t=http://developer.android.com/reference/android/R.attr.html#configChanges)。
+ 情景 2: Activity的重启发生在当用户在开发者选项中选中了“Don’t keep activities”（“中文下为 不保留活动”）的复选框，然后另一个Activity在最顶上的时候。
+ 情景 3: 进程的重启发生在应用运行在后台，但是这个时候内存不够的情况下。总结现在你可以发现，一个调用了setRetainInstance(true)的Fragment也不奏效，我们还是需要保存/恢复fragment的状态，所以为简化问题，我们暂不考虑上述情况的Fragment。Occam’s razor

![](https://upload-images.jianshu.io/upload_images/1233754-2c5bd50ac1579043.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/689/format/webp)  

现在，看上去更舒服了，我们只需要写两段代码为了恢复应用： 

+  保存/恢复 for Activity, View, Fragment, DialogFragment;
+  重启后台请求由于进程重启
第一个部分,用Android的API可以实现。第二个部分，就是Presenter的作用了。Presenter将会记住有哪些请求需要执行，当进程在执行过程中重启时，Presenter将会出现执行它们。  

### 1.5. MVP 的优缺点
任何事务都存在两面性，MVP当然也不列外，我们来看看MVP的优缺点。

**优点：**
1. 降低耦合度，实现了Model和View真正的完全分离，可以修改View而不影响Modle  
2. 模块职责划分明显，层次清晰（下面会介绍Bob大叔的Clean Architecture）  
3. 隐藏数据
4. Presenter可以复用，一个Presenter可以用于多个View，而不需要更改Presenter的逻辑（当然是在View的改动不影响业务逻辑的前提下）
5. 利于测试驱动开发。以前的Android开发是难以进行单元测试的（虽然很多Android开发者都没有写过测试用例，但是随着项目变得越来越复杂，没有测试是很难保证软件质量的；而且近几年来Android上的测试框架已经有了长足的发展——开始写测试用例吧），在使用MVP的项目中Presenter对View是通过接口进行，在对Presenter进行不依赖UI环境的单元测试的时候。可以通过Mock一个View对象，这个对象只需要实现了View的接口即可。然后依赖注入到Presenter中，单元测试的时候就可以完整的测试Presenter应用逻辑的正确性。
6. View可以进行组件化。在MVP当中，View不依赖Model。这样就可以让View从特定的业务场景中脱离出来，可以说View可以做到对业务完全无知。它只需要提供一系列接口提供给上层操作。这样就可以做到高度可复用的View组件。
7. 代码灵活性

**缺点：**
1. Presenter中除了应用逻辑以外，还有大量的View->Model，Model->View的手动同步逻辑，造成Presenter比较笨重，维护起来会比较困难。
2. 由于对视图的渲染放在了Presenter中，所以视图和Presenter的交互会过于频繁。
3. 如果Presenter过多地渲染了视图，往往会使得它与特定的视图的联系过于紧密。一旦视图需要变更，那么Presenter也需要变更了。
4.  额外的代码复杂度及学习成本。

### 1.6. 小结
在MVP模式里通常包含4个要素：  
(1) View :负责绘制UI元素、与用户进行交互(在Android中体现为Activity);  
(2) View interface :需要View实现的接口，View通过View interface与Presenter进行交互，降低耦合，方便进行单元测试;  
(3) Model :负责存储、检索、操纵数据(有时也实现一个Model interface用来降低耦合);  
(4) Presenter :作为View与Model交互的中间纽带，处理与用户交互的负责逻辑。

## 二、MVX 剖析

### 2.1. M（Model）模型
表示数据模型和业务逻辑(business logic)。模型并不总是DataSet，DataTable之类的东西，它代表着一类组件(components)或类(class)，这些组件或类可以向外部提供数据，同时也能从外部获取数据并将这些数据存储在某个地方。简单的理解，可以把模型想象成“外观类(facade class)”。译注：这里的外观是指“外观模式”中所说的外观。外观的一般作用是为一个复杂的子系统提供高层次的简单易用的访问接口，可以参看下面的图来理解它的原理：model层主要负责：· 从网络，数据库，文件，传感器，第三方等数据源读写数据。· 对外部的数据类型进行解析转换为APP内部数据交由上层处理。· 对数据的临时存储,管理，协调上层数据请求。

### 2.2 V（View）视图
将数据呈现给用户。一般的视图都只是包含用户界面(UI)，而不包含界面逻辑。比如，Asp.net中包含控件的页面(page)就是一个视图。视图可以从模型中读取数据，但是不能修改或更新模型。view 层主要负责：· 提供UI交互· 在presenter的控制下修改UI。· 将业务事件交由presenter处理。注意: View层不存储数据，不与Model层交互。在Android中View层一般是Activity、Fragment、View（控件）、ViewGroup（布局等）等。

### 2.3. X（C-Controller、P-Presenter、VM-ViewModel）控制器
View捕获到用户交互操作后会直接转发给Controller，后者完成相应的UI逻辑。如果需要涉及业务功能的调用，Controller会直接调用Model。在完成UI处理之后，Controller会根据需要控制原View或者创建新的View对用户交互操作予以响应。层现器：作为View与Model交互的中间纽带，处理与用户交互的负责逻辑。Presenter包含了根据用户在视图中的行为去更新模型的逻辑。视图仅仅只是将用户的行为告知Presenter，而Presenter负责从视图中取得数据然后发送给模型。视图模型：binder 所在之处，是 View 的抽象，对外暴露出公共属性和命令，它是View的抽象，负责View与Model之间信息转换，将View的Command传送到Model。ViewModel的含义就是 "Model of View"，视图的模型。它的含义包含了领域模型（Domain Model）和视图的状态（State）。可以简单把ViewModel理解为页面上所显示内容的数据抽象，和Domain Model不一样，ViewModel更适合用来描述View。2.4. 小结MVC模式、MVP模式和MVVM模式都作为用来分离UI层与业务层的一种开发模式。这些模式之间的差异可以归纳为对这个问题处理的方式的不同。

## 三、MVX 与三层架构

相信不少童鞋和我有过同样的疑惑：MVX分为了M-V-X三层，那这到底和软件的三层架构有何关系呢？我们带着问题继续往下阅读。

### 3.1. 什么是三层架构
三层架构是一个分层式的软件体系架构设计，它可适用于任何一个项目。通常意义上的三层架构就是将整个业务应用划分为：界面层（User Interface layer）、业务逻辑层（Business Logic Layer）、数据访问层（Data access layer）。区分层次的目的即为了“高内聚低耦合”的思想。在软件体系架构设计中，分层式结构是最常见，也是最重要的一种结构。微软推荐的分层式结构一般分为三层，从下至上分别为：数据访问层、业务逻辑层（又或称为领域层）、表示层。（参考自：百度百科）

**常见的架构有**：· 分层架构（如：三层架构）\ 事件驱动架构 \ 微内核架构 \ 微服务架构 \ 基于空间的架构  

**推荐阅读:**《软件架构模式》

### 3.2. 三层架构和 MVX 的关系
首先，我想说三层架构（分层架构）和 MVX 没有什么关系，它们不在同一个层次上（三层是一种架构思想，更多的是和事件驱动架构、微内核架构等放在一起讨论，而我更喜欢把 MVX 做为模式来对待）。

三层是从整个应用程序架构的角度来分为DAL(数据访问层)、BLL(业务逻辑层)、WEB层（界面层）各司其职，意在职责分离；三层是为了解决整个应用程序中各个业务操作过程中不同阶段的代码封装的问题，为了使程序员更加专注的处理某阶段的业务逻辑；并且三层只是多层架构中的一种情况，完全可以根据需要分为多层。

MVC 主要是为了解决应用程序用户界面的样式替换问题，把展示数据的 HTML 页面尽可能的和业务代码分离。MVC把纯净的界面展示逻辑（用户界面）独立到一些文件中（Views），把一些和用户交互的程序逻辑（Controller）单独放在一些文件中，在 Views 和 Controller 中传递数据使用一些专门封装数据的实体对象，这些对象，统称为Models。而在其后出现的 MVP 以及 MVVM 与 MVC 的作用类似，MVX 主要的区别在于如何解决 M 与 V 之间的连接与更新。

总之一句话，MVX 是一种模式，Spring MVC 以及 ASP.NET MVC 等是一个基于MVC模式的开发框架，三层架构是一种架构。

其次，它们都有一个表现层，但是这两者的展现层并不是一样的。可以这样看待 MVX 与三层架构中的表现层的关系，MVX 中的 V 和 X 都属于三层架构中的表现层，可以看下图的示意。

最后，虽然都有提到 Model，但是在 MVX 中没有把业务的逻辑访问看成两个层，这是采用三层架构或 MVX 搭建程序最主要的区别。在三层架构中Model 的概念与 MVX 中 Model 的概念是不一样的，“三层”中典型的Model 层是以实体类构成的，而MVC里，则是由业务逻辑与访问数据组成的。

也就是说，MVX 与三层架构说的根本不是一回事。在所谓的“三层”中，它要求你将BLL层独立出来，它只是告诉你表示层和业务逻辑层之间的静态关系。而 MVX 则告诉你在这个具体的地方如何处理其动态驱动流程，尽管 MVC 仍然粗糙（甚至 MVP、MVVM也是粗糙的），但是已经比所谓三层更细致一些了（三层是架构好吗...）。


![MVP和三层架构示意图](https://upload-images.jianshu.io/upload_images/1233754-c8f4880e03752932.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/820/format/webp)

## 四、Android 上 MVP 的几种实现

絮絮叨叨说了一大堆，终于干货要来了。正所谓：Talk is cheap,show me the code.下面会给出示例代码，请继续阅读。在 Android 开发中讨论 MVP、MVVM 最终都离不了 [Uncle Bob](https://link.jianshu.com/?t=http://blog.8thlight.com/uncle-bob/archive.html) 的 [The Clean Architecture](https://link.jianshu.com/?t=http://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html)。（请自行阅读，相信阅读原文会有更大的收获）

下面，我会尝试一一细数 Android 上常见的 MVP 实现方式（说明：并没有什么排序规则，只谈大家的实现思路，展示的顺序只是为了方便大家的理解和阅读）。

### 4.1. 存取用户信息的 MVP 小 Demo
这其实是我最先接触 MVP 时看到的示例，代码很少，但是把 MVP 的分层展示的挺清晰。   
原文：[MVP模式在Android开发中的应用](https://link.jianshu.com/?t=http://blog.csdn.net/vector_yi/article/details/24719873?utm_source=tuicool&utm_medium=referral)   
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/VectorYi/MVPSample)    

![登录Demo 界面](https://upload-images.jianshu.io/upload_images/1233754-974f0f167c5d84e6.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/290/format/webp)

![项目结构示例](https://upload-images.jianshu.io/upload_images/1233754-9db597002e7a8b95.jpeg?imageMogr2/auto-orient/strip%7CimageView2/2/w/248/format/webp)

### 4.2. 天气查询的 MVP 小 Demo
现在的 Andorid 开发怎么能够离开网络，来一个有网络的示例。该天气查询 Demo，是通过访问 Web 服务获取地区的天气信息（返回为JSON），然后在 Activity 中用 TextView 展示出来。  
原文：[Android中的MVP](https://link.jianshu.com/?t=http://rocko.xyz/2015/02/06/Android%e4%b8%ad%e7%9a%84MVP/)   
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/zhengxiaopeng/Rocko-Android-Demos/tree/master/architecture/android-mvp)

![包结构](https://upload-images.jianshu.io/upload_images/1233754-088b6cad3381f6e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/364/format/webp)

![项目效果预览](https://upload-images.jianshu.io/upload_images/1233754-f6b8ca2a6d3ff647.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/387/format/webp)

### 4.3. 使用 Activity/Fragment 作为 Presenter 的探索
上面的示例 View 都是 Activity 来承担的，Presenter 是一个普通的类，前面讨论过 Android 在不同场景下会进入不同的生命周期，这将可能导致 Presenter 也随着其生命周期需要做出响应。从这个角度考虑，有不少开发者提出了 MVP 实现的其他思路，接下来我们要探讨的就是使用 Activity/Fragment 作为 Presenter 的一些实现方案。

#### 4.3.1 一种实现MVP模式的新思路
其中有使用 Activity 和 Fragment 作为 Presenters 和使用 Adapter作为 Presenter的探讨，思路挺有意思，可以去看看。  
原文：[android-mvp-an-alternate-approach](https://upload-images.jianshu.io/upload_images/1233754-f6b8ca2a6d3ff647.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/387/format/webp)  
译文：[一种在android中实现MVP模式的新思路 ](https://link.jianshu.com/?t=https://github.com/bboyfeiyu/android-tech-frontier/tree/master/androidweekly/%E4%B8%80%E7%A7%8D%E5%9C%A8android%E4%B8%AD%E5%AE%9E%E7%8E%B0MVP%E6%A8%A1%E5%BC%8F%E7%9A%84%E6%96%B0%E6%80%9D%E8%B7%AF)   
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/wongcain/MVP-Simple-Demo)    

#### 4.3.2. TheMVP 介绍
TheMVP使用Activity作为Presenter层来处理代码逻辑，通过让Activity包含一个ViewDelegate对象来间接操作View层对外提供的方法，从而做到完全解耦视图层。  
原文：[用MVP架构开发Android应用](https://link.jianshu.com/?t=http://www.kymjs.com/code/2015/11/09/01/)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/kymjs/TheMVP)  




![TheMVP原理示意](https://upload-images.jianshu.io/upload_images/1233754-3e36db8569ba33bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/668/format/webp)





![TheMVP项目结构](https://upload-images.jianshu.io/upload_images/1233754-3e079631d1911c05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

#### 4.3.3 MVPro 介绍
MVPro的实现很简单，思想和上面两篇文章（[一种在android中实现MVP模式的新思路](https://link.jianshu.com/?t=https://github.com/bboyfeiyu/android-tech-frontier/tree/master/androidweekly/%E4%B8%80%E7%A7%8D%E5%9C%A8android%E4%B8%AD%E5%AE%9E%E7%8E%B0MVP%E6%A8%A1%E5%BC%8F%E7%9A%84%E6%96%B0%E6%80%9D%E8%B7%AF)和[用MVP架构开发Android应用](https://link.jianshu.com/?t=http://kymjs.com/code/2015/11/09/01/)）介绍的一样，都是将Activity和Fragment作为Presenter。Presenter即我们的Activity或者Fragment, View呢？说白了就是我们从Activity和Fragment中提取出来的和View操作相关的代码。   
原文：[Android MVP框架MVPro的使用和源码分析](https://link.jianshu.com/?t=http://blog.csdn.net/qibin0506/article/details/49992897)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/qibin0506/MVPro)  




![MVPro原理示意](https://upload-images.jianshu.io/upload_images/1233754-75eee2b3600f5850.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/688/format/webp)
### 4.4. Nucleus 框架
该框架还是值得一看的，作者 Konstantin Mikheev 对于 MVP 的理解挺有见地。

Nucleus is a simple Android library, which utilizes the Model-View-Presenter pattern to properly connect background tasks with visual parts of an application.  
原文：[Introduction to Model View Presenter on Android](https://link.jianshu.com/?t=https://github.com/konmik/konmik.github.io/wiki/Introduction-to-Model-View-Presenter-on-Android)  
译文：[介绍ModelViewPresenter在Android中的应用](https://link.jianshu.com/?t=http://www.it165.net/pro/html/201505/41758.html)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/konmik/nucleus)  

### 4.5. Beam 框架
该框架的作者对 MVP 的理解的特点如下：
>Activity会在很多情况下被系统重启：  
当用户旋转屏幕  
在后台时内存不足  
改变语言设置  
attache 一个外部显示器等。  


>正确的方式应该是：  
Presenter与Activity的绑定关系应由静态类管理。而不是由Activity管理。当Activity意外重启时Presenter不应重启。Activity重启时，Presenter与Activity重新绑定，根据数据恢复Activity状态。  
而当Activity真正销毁时。对应Presenter才应该跟随销毁。
  
这也是对 Presenter 管理的一个思路，可以参考。

原文：[Android应用中MVP最佳实践](https://www.jianshu.com/p/ed2aa9546c2c)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/Jude95/Beam) 

![Beam MVP](https://upload-images.jianshu.io/upload_images/1233754-7aad1f680d09cf82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

### 4.6. Mosby 框架
>我给这篇关于Android库的博客起的名字灵感来源于《老爸老妈浪漫史》中的建筑设计师Ted Mosby。这个Mosby库可以帮助大家在Android上通过Model-View-Presenter模式做出一个完善稳健、可重复使用的软件，还可以借助ViewState轻松实现屏幕翻转。

这又是一种解决Activity/Fragment生命周期在屏幕翻转等场景下对Presenter的处理的思路。  

原文：[Ted Mosby – Software Architect](https://link.jianshu.com/?t=http://hannesdorfmann.com/android/mosby)  
译文：[MVP框架 – Ted Mosby的软件架构](https://link.jianshu.com/?t=http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2015/0528/2945.html)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/sockeqwe/mosby)  

![获得ViewState支持的Activity的生命周期图解](https://upload-images.jianshu.io/upload_images/1233754-774bc3c30225dd60.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/720/format/webp)

![获得ViewState支持的Fragment的生命周期图解](https://upload-images.jianshu.io/upload_images/1233754-ba76071058ed2577.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/720/format/webp)

### 4.7. Loader 的使用
>就像刚才说的一样，关键问题就是在哪里存储Presenter以及什么时候销毁它们。而我们刚刚就看到了Loader的强大之处：由安卓系统框架提供，有单独生命周期，会被自动回收且不必在后台运行。  
>
>所以思考一下需求以及Loader的功能，我们可以让Loader作为Presenter的提供者，而不需要担心手机状态改变。  
>
>将同步的Loader作为存放Presenter的缓存。  
>
>这里的重点就在于同步使用Loader时，我们可以知道在生命周期的哪个阶段Presenter被创建了并且可以工作了。甚至是在Activity/Fragment可见之前。

使用Loader，思路很有新意，关键确实解决了问题，更关键的是使用的是 Android Framework 提供的功能。

原文：[Presenter surviving orientation changes with Loaders](https://link.jianshu.com/?t=https://medium.com/@czyrux/presenter-surviving-orientation-changes-with-loaders-6da6d86ffbbf#.3t97rb4t2)  
译文：[通过Loader延长Presenter生命周期](https://link.jianshu.com/?t=http://blog.chengdazhi.com/index.php/131)  
源码：[GitHub 地址](https://link.jianshu.com/?t=http://blog.chengdazhi.com/index.php/131)  

![MVP diagram](https://upload-images.jianshu.io/upload_images/1233754-fc687b2d4a4ddbb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/461/format/webp)

### 4.8. Google 官方推荐
大 Boss 总是最后出场，对于 Android 上 MVP 的实现，Google 给也出了一些建议和实例，赶紧看看去吧。  
原文：[Android Architecture Blueprints (beta)](https://link.jianshu.com/?t=https://github.com/googlesamples/android-architecture?utm_source=tuicool&utm_medium=referral)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/googlesamples/android-architecture?utm_source=tuicool&utm_medium=referral)    

![Google MVP 示例](https://upload-images.jianshu.io/upload_images/1233754-416515467a488229.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/350/format/webp)  

### 4.9. MVP 实现的完整开源项目

##### 4.9.1. Philm
ChrisBannes的开源项目Philm，其整体架构是一套MVP的实现。这里有一篇分析该项目的文章，可以直接去读源码，也可以先看看 lightSky 是怎么分析的。

Philm 分析：[开源项目Philm的MVP架构分析](https://link.jianshu.com/?t=http://www.lightskystreet.com/2015/02/10/philm_mvp/)  
源码：[GitHub 地址](https://link.jianshu.com/?t=https://github.com/chrisbanes/philm)

![Philm 的总体设计](https://upload-images.jianshu.io/upload_images/1233754-69e10d681e615d2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/787/format/webp)

![Philm 的类关系图](https://upload-images.jianshu.io/upload_images/1233754-90bedb5bd3f1cbb8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

![Philm 的基本调用流程图](https://upload-images.jianshu.io/upload_images/1233754-40ff18fcd402c76a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/888/format/webp)

#### 4.9.2. 使用 Beam 开发的 APP
[SearchPictureTool](https://link.jianshu.com/?t=https://github.com/wenhuaijun/SearchPictureTool) 搜图神器  
[Fishing](https://link.jianshu.com/?t=https://github.com/wenhuaijun/SearchPictureTool) 空钩钓鱼   
>Beam 前面已有介绍，感兴趣的童鞋可以看看上面两个项目。

#### 4.9.3. 干货集中营客户端
[干货集中营](https://link.jianshu.com/?t=http://gank.io/)有不少的开源实现都是 MVP 模式的（下面的 App 是官网上列出来的，具体是否都采用了 MVP 本人没有一一查阅）。  
[妹纸.gank.io](https://link.jianshu.com/?t=https://github.com/drakeet/Meizhi)  
[馒头先生](https://link.jianshu.com/?t=https://github.com/oxoooo/mr-mantou-android)  
[GankApp](https://link.jianshu.com/?t=https://github.com/oxoooo/mr-mantou-android)  
[GanK](https://link.jianshu.com/?t=https://github.com/dongjunkun/GanK)  
[Gank4Android](https://link.jianshu.com/?t=https://github.com/zzhoujay/Gank4Android)  
[GankDaily](https://link.jianshu.com/?t=https://github.com/maoruibin/GankDaily) 

### 4.10. 小结
上述众多解决方案都集中在 Presenter 实现的问题上，这主要是由于 Activity、Fragment 的复杂性导致的，它们有众多生命周期，它们无所不能，是否把它们仅仅视作 View 成了争论的焦点。个人认为从编码的难易程度和编码的习惯来说，我赞成把 Activity、Fragment 作为 View 即可，我们可以考虑其他方式来保证Presenter的生命周期和防止 Presenter 引起内存泄漏。其中使用 Loader 的方案就非常优雅，下面在本人的示例项目中也会采用这种方式。  

## 5. 最佳实践
好了终于要点讲自己的东西了，有点小激动。下面这些仅表示个人观点，非一定之规，各位看官按需取用，有说的不对的，敬请谅解。关于命名规范可以参考我的另一篇文章“[Android 编码规范](https://www.jianshu.com/p/0a984f999592#)”。老规矩先上图：

![MVPBestPractice 思维导图](https://upload-images.jianshu.io/upload_images/1233754-8bd547cf074d0860.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

在参考了 [kenjuwagatsuma](https://link.jianshu.com/?t=https://medium.com/@kenjuwagatsuma) 的 [MVP Architecture in Android Development](https://link.jianshu.com/?t=https://medium.com/@kenjuwagatsuma/mvp-architecture-in-android-development-3d63cc32707a#.9fyw4pjdg) 和 [Saúl Molinero](https://link.jianshu.com/?t=http://saulmm.github.io/) 的 [A useful stack on android #1, architecture](https://link.jianshu.com/?t=http://saulmm.github.io/2015/02/02/A-useful-stack-on-android-1,-architecture/) 之后，我决定采用如下的分层方案来构建这个演示Demo，如下：

![分层架构方案](https://upload-images.jianshu.io/upload_images/1233754-1d232d0114a5c19e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/908/format/webp)

总体架构可以被分成四个部分 ：  
**Presentation：**负责展示图形界面，并填充数据，该层囊括了 View 和 Presenter （上图所示的Model我理解为 ViewModel -- 为 View 提供数据的 Model，或称之为 VO -- View Object）。  
**Domain：**负责实现app的业务逻辑，该层中由普通的Java对象组成，一般包括 Usecases 和 Business Logic。  
**Data：**负责提供数据，这里采用了 Repository 模式，Repository 是仓库管理员，Domain 需要什么东西只需告诉仓库管理员，由仓库管理员把东西拿给它，并不需要知道东西实际放在哪。Android 开发中常见的数据来源有，RestAPI、SQLite数据库、本地缓存等。  
**Library：**负责提供各种工具和管理第三方库，现在的开发一般离不开第三方库（当然可以自己实现，但是不要重复造轮子不是吗？），这里建议在统一的地方管理（那就是建一个单独的 module），尽量保证和 Presentation 层分开。  


![AndroidStudio 中构建项目](https://upload-images.jianshu.io/upload_images/1233754-d744f35227a3cab9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/670/format/webp)

### 5.1. 关于包结构划分

一个项目是否好扩展，灵活性是否够高，包结构的划分方式占了很大比重。很多项目里面喜欢采用按照特性分包（就是Activity、Service等都分别放到一个包下），在模块较少、页面不多的时候这没有任何问题；但是对于模块较多，团队合作开发的项目中，这样做会很不方便。所以，我的建议是按照模块划分包结构。其实这里主要是针对 Presentation 层了，这个演示 Demo 我打算分为四个模块：登录，首页，查询天气和我的（这里仅仅是为了演示需要，具体如何划分模块还得根据具体的项目，具体情况具体分析了）。划分好包之后如下图所示：

![包结构划分](https://upload-images.jianshu.io/upload_images/1233754-a7259b477e304440.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/930/format/webp)

### 5.2. 关于res拆分
功能越来越多，项目越做越大，导致资源文件越来越多，虽然通过命名可以对其有效归类（如：通过添加模块名前缀），但文件多了终究不方便。得益于 Gradle，我们也可以对 res 目录进行拆分，先来看看拆分后的效果：

![按模块拆分 res 目录](https://upload-images.jianshu.io/upload_images/1233754-bed38e679fd920f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/846/format/webp)

注意：resource 目录的命名纯粹是个人的命名偏好，该目录的作用是用来存放那些不需要分模块放置的资源。

#### 5.2.1. res 目录的拆分步骤

> **首先**打开 module 的 build.gradle 文件

![res 拆分 Step1](https://upload-images.jianshu.io/upload_images/1233754-3456f3b1b4ce69f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/306/format/webp)

> **其次**定位到 defaultConfig {} 与 buildTypes {} 之间

![res 拆分 Step2.png](https://upload-images.jianshu.io/upload_images/1233754-226ed3830ecf60b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/712/format/webp)


> **接着**在第二步定位处编辑输入 sourceSets {} 内容，具体内容如下：

```
sourceSets {
    main {
        manifest.srcFile 'src/main/AndroidManifest.xml'
        java.srcDirs = ['src/main/java','.apt_generated']
        aidl.srcDirs = ['src/main/aidl','.apt_generated']
        assets.srcDirs = ['src/main/assets']
        res.srcDirs =
        [
                'src/main/res/home',
                'src/main/res/login',
                'src/main/res/mine',
                'src/main/res/weather',
                'src/main/res/resource',
                'src/main/res/'

        ]
    }
}
```

> **最后**在 res 目录下按照 sourceSets 中的配置建立相应的文件夹，将原来 res 下的所有文件（夹）都移动到 resource 目录下，并在各模块中建立 layout 等文件夹，并移入相应资源， Sync Project 即可。

### 5.3. 怎么写 Model

这里的 Model 其实贯穿了我们项目中的三个层，Presentation、Domain 和 Data。暂且称之为 Model 吧，这也我将提供 Repository 功能的层称之为 Data Layer 的缘故（有些称这一层为 Model Layer）。

**首先**，谈谈我对于 Model 是怎么理解的。应用都离不开数据，而这些数据来源有很多，如网络、SQLite、文件等等。一个应用对于数据的操作无非就是：获取数据、编辑（修改）数据、提交数据、展示数据这么几类。从分层的思想和 JavaEE 开发中积累的经验来看，我觉得 Model 中的类需要分类。从功能上来划分，可以分出这么几类：  
  + **VO（View Object）**：视图对象，用于展示层，它的作用是把某个指定页面（或组件）的所有数据封装起来。  
  + **DTO（Data Transfer Object）**：数据传输对象，这个概念来源于 JavaEE 的设计模式，原来的目的是为了 EJB 的分布式应用提供粗粒度的数据实体，以减少分布式调用的次数，从而提高分布式调用的性能和降低网络负载，但在这里，我泛指用于展示层与服务层之间的数据传输对象。
  + **DO（Domain Object）**：领域对象，就是从现实世界中抽象出来的有形或无形的业务实体。  
  + **PO（Persistent Object）**：持久化对象，它跟持久层（通常是关系型数据库）的数据结构形成一一对应的映射关系，如果持久层是关系型数据库，那么，数据表中的每个字段（或若干个）就对应 PO 的一个（或若干个）属性。  

  >> **注意**：关于vo、dto、do、po可以参考这篇文章-“[领域驱动设计系列文章——浅析VO、DTO、DO、PO的概念、区别和用处](http://www.cnblogs.com/qixuejia/p/4390086.html)”

当然这些不一定都存在，这里只是列举一下，可以有这么多分类，当然列举的也不全。

**其次**，要搞清楚 Domain 层和 Data 层分别是用来做什么的，然后才知道哪些 Model 该往 Data 层中写，哪些该往 Domain 层中写。
Data 层负责提供数据。
Data 层不会知道任何关于 Domain 和 Presentation 的数据。它可以用来实现和数据源（数据库，REST API或者其他源）的连接或者接口。这个层面同时也实现了整个app所需要的实体类。
Domain 层相对于 Presentation 层完全独立，它会实现应用的业务逻辑，并提供 Usecases。
Presentation 从 Domain 层获取到的数据，我的理解就是 VO 了，VO 应该可以直接使用。

  >> **注意**：这里说的直接使用是指不需要经过各种转换，各种判断了，如 Activity 中某个控件的显示隐藏是根据 VO 中的 visibility 字段来决定，那么这个最好将 visibility 作为 int 型，而且，取值为VISIBLE/INVISIBLE/GONE，或者至少是 boolean 型的。


>> **注意**：这里所谓的业务逻辑可能会于 Presenter 的功能概念上有点混淆。打个比方，假如 usecase 接收到的是一个 json 串，里面包含电影的列表，那么把这个 json 串转换成 json 以及包装成一个 ArrayList，这个应当是由 usecase 来完成。而假如 ArrayList 的 size 为0，即列表为空，需要显示缺省图，这个判断和控制应当是由 Presenter 完成的。（上述观点参考自：[Saúl Molinero](http://saulmm.github.io/)）


**最后**，就是关于 Data 层，采用的 Repository 模式，建议抽象出接口来，Domain 层需要感知数据是从哪里取出来的。

### 5.4. 怎么写 View

先区分一下Android View、View、界面的区别  
+ **Android View**： 指的是继承自android.view.View的Android组件。  
+ **View**：接口和实现类，接口部分用于由 Presenter 向 View 实现类通信，可以在 Android 组件中实现它。一般最好直接使用 Activity，Fragment 或自定义 View。  
+ **界面**：界面是面向用户的概念。比如要在手机上进行界面间切换时，我们在代码中可以通过多种方式实现，如 Activity 到 Activity 或一个 Activity 内部的 Fragment/View 进行切换。所以这个概念基于用户的视觉，包括了所有 View 中能看到的东西。  

> 那么该怎么写 View 呢？

在 MVP 中 View 是很薄的一层，里面不应该有业务逻辑，所以一般只提供一些 getter 和 setter 方法，供 Presenter 操作。关于 View，我有如下建议：  
+ i. 简单的页面中直接使用 Activity/Fragment 作为 View 的实现类，然后抽取相应的接口
+ ii. 在一些有 Tab 的页面中，可以使用 Activity + Fragment ( + ViewPager) 的方式来实现，至于 ViewPager，视具体情况而定，当然也可以直接 Activity + ViewPager 或者其他的组合方式
+ iii. 在一些包含很多控件的复杂页面中，那么建议将界面拆分，抽取自定义 View，也就是一个 Activity/Fragment 包含多个 View（实现多个 View 接口）

### 5.5. 怎么写 Presenter
Presenter 是 Android MVP 实现中争论的焦点，上篇中介绍了多种“MVP 框架”，其实都是围绕着**Presenter应该怎么写**。有一篇专门介绍如何设计 Presenter 的文章（[Modeling my presentation layer](http://panavtec.me/modeling-presentation-layer)），个人感觉写得不错，这里借鉴了里面不少的观点，感兴趣的童鞋可以去看看。下面进入正题。

> 为什么写 Presenter 会这么纠结，我认为主要有以下几个问题：

+ 1. 我们将 Activity/Fragment 视为 View，那么 View 层的编写是简单了，但是这有一个问题，当手机的状态发生改变时（比如旋转手机）我们应该如何处理Presenter对象，那也就是说 Presenter 也存在生命周期，并且还要“手动维护”（别急，这是引起来的，下面会细说）
+ 2. Presenter 中应该没有 Android Framework 的代码，也就是不需要导 Framework 中的包，那么问题来了，页面跳转，显示对话框这些情况在 Presenter 中该如何完成
+ 3. 上面说 View 的时候提到复杂的页面建议通过抽取自定义 View 的方式，将页面拆分，那么这个时候要怎么建立对应的 Presenter 呢
+ 4. View 接口是可以有多个实现的，那我们的 Presenter 该怎么写呢

好，现在我将针对上面这些问题一一给出建议。

#### 5.5.1. 关于 Presenter 生命周期的问题

先看图（更详细讲解可以看看这篇文章[Presenter surviving orientation changes with Loaders](https://medium.com/@czyrux/presenter-surviving-orientation-changes-with-loaders-6da6d86ffbbf)）   

![Presenter生命周期](http://upload-images.jianshu.io/upload_images/1233754-a9a829de0250462f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如上图所示，方案1和方案2都不够优雅（这也是很多“MVP 框架”采用的实现方案），而且并不完善，只适用于一些场景。而方案3，让人耳目一新，看了之后不禁想说 Loader 就是为 Presenter 准备的啊。这里我们抓住几个关键点就好了：
* Loader 是 **Android 框架**中提供的
* Loader 在手机状态改变时是**不会被销毁**的
* Loader 的生命周期是是由**系统控制**的，会在Activity/Fragment不再被使用后**由系统回收**
* Loader 与 Activity/Fragment 的生命周期绑定，所以**事件会自己分发**
* 每一个 Activity/Fragment 持有**自己的 Loader 对象**的引用
* 具体怎么用，在 [Antonio Gutierrez](https://medium.com/@czyrux) 的文章已经阐述的很明白，我就不再赘述了

>> 好吧，我有一点要补充，上面说的方案1和方案2不是说就没有用了，还是视具体情况而定，如果没有那么多复杂的场景，那么用更简单的方案也未尝不可。能解决问题就好，不要拘泥于这些条条框框...（话说，咱这不是为了追求完美吗，哈哈）

#### 5.5.2. 关于页面跳转和显示Dialog

首先说说页面跳转，前一阵子忙着重构公司的项目，发现项目中很多地方使用 startActivity() 和使用 Intent 的 putExtra() 显得很乱；更重要的是从 Intent 中取数据的时候需要格外小心——类型要对应，key 要写对，不然轻则取不到数据，重则 Crash。还有一点，就是当前 Activity/Fragment 必须要知道目标 Activity 的类名，这里耦合的很严重，有没有。当时就在想这是不是应该封装一下啊，或者有更好的解决方案。于是，先在网上搜了一下，知乎上有类似的提问，有人建议写一个 Activity Router（Activity 路由表）。嗯，正好和我的思路类似，那就开干。

我的思路很简单，在 util 包中定义一个 NavigationManager 类，在该类中按照模块使用注释先分好区块（为什么要分区块，去看看我的 “[Android 编码规范](http://www.jianshu.com/p/0a984f999592#)”）。然后为每个模块中的 Activity 该如何跳转，定义一个静态方法。

如果不需要传递数据的，那就很简单了，只要传入调用者的 Context，直接 new 出 Intent，调用该 Context 的 startActivity() 方法即可。代码如下：  
![导航管理类-跳转系统页面](http://upload-images.jianshu.io/upload_images/1233754-1729b46c1b2709d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)   
![导航管理类-跳转不需要传递数据的页面](http://upload-images.jianshu.io/upload_images/1233754-e958031db7c46841.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  
http://upload-images.jianshu.io/upload_images/1233754-a9a829de0250462f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240
如果需要传递数据呢？刚才说了，使用 Bundle 或者 putExtra() 这种方式很不优雅，而且容易出错（那好，你个给优雅的来看看，哈哈）。确实，我没想到比较优雅的方案，在这里我提供一个粗糙的方案，仅供大家参考一下，如有你有更好的，那麻烦也和我分享下。

我的方案是这样的，使用序列化对象来传递数据（建议使用 Parcelable，不要偷懒去用 Serializable，这个你懂的）。为需要传递数据的 Activity 新建一个实现了 Parcelable 接口的类，将要传递的字段都定义在该类中。其他页面需要跳转到该 Activity，那么就需要提供这个对象。在目标 Activity 中获取到该对象后，那就方便了，不需要去找对应的 key 来取数据了，反正只要对象中有的，你就能直接使用。

> 注意：这里我建议将序列化对象中的所有成员变量都定义为 public 的，一来，可以减少代码量，主要是为了减少方法数（虽说现在对于方法数超 64K 有比较成熟的 dex 分包方案，但是尽量不超不是更好）；二来，通过对象的 public 属性直接读写比使用 getter/setter 速度要快（听说的，没有验证过）。

> 注意：这里建议在全局常量类（没有，那就定义一个，下面会介绍）中定义一个唯一的 INTENT_EXTRA_KEY，往 Bundle 中存和取得时候都用它，也不用去为命名 key 费神（命名从来不简单，不是吗），取的时候也不用思考是用什么 key 存的，简单又可以避免犯错。

具体如下图所示：  
![导航管理类-跳转需要传递数据的页面](http://upload-images.jianshu.io/upload_images/1233754-8e7e60b8e75c0696.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)    
![导航管理类-传递数据](http://upload-images.jianshu.io/upload_images/1233754-cf4de86178b55378.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  
![导航管理类-获取传递的数据](http://upload-images.jianshu.io/upload_images/1233754-6cae34270d70ff30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  

导航管理类代码如下：

```java
//==========逻辑方法==========
public static <T> T getParcelableExtra(Activity activity) {
    Parcelable parcelable = activity.getIntent().getParcelableExtra(NavigateManager.PARCELABLE_EXTRA_KEY);
    activity = null;
    return (T)parcelable;
}

private static void overlay(Context context, Class<? extends Activity> targetClazz, int flags, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    setFlags(intent, flags);
    putParcelableExtra(intent, parcelable);
    context.startActivity(intent);
    context = null;
}

private static void overlay(Context context, Class<? extends Activity> targetClazz, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    putParcelableExtra(intent, parcelable);
    context.startActivity(intent);
    context = null;
}

private static void overlay(Context context, Class<? extends Activity> targetClazz, Serializable serializable) {
    Intent intent = new Intent(context, targetClazz);
    putSerializableExtra(intent, serializable);
    context.startActivity(intent);
    context = null;
}

private static void overlay(Context context, Class<? extends Activity> targetClazz) {
    Intent intent = new Intent(context, targetClazz);
    context.startActivity(intent);
    context = null;
}

private static void forward(Context context, Class<? extends Activity> targetClazz, int flags, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    setFlags(intent, flags);
    intent.putExtra(PARCELABLE_EXTRA_KEY, parcelable);
    context.startActivity(intent);
    if (isActivity(context)) return;
    ((Activity)context).finish();
    context = null;
}

private static void forward(Context context, Class<? extends Activity> targetClazz, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    putParcelableExtra(intent, parcelable);
    context.startActivity(intent);
    if (isActivity(context)) return;
    ((Activity)context).finish();
    context = null;
}

private static void forward(Context context, Class<? extends Activity> targetClazz, Serializable serializable) {
    Intent intent = new Intent(context, targetClazz);
    putSerializableExtra(intent, serializable);
    context.startActivity(intent);
    if (isActivity(context)) return;
    ((Activity)context).finish();
    context = null;
}

private static void forward(Context context, Class<? extends Activity> targetClazz) {
    Intent intent = new Intent(context, targetClazz);
    context.startActivity(intent);
    if (isActivity(context)) return;
    ((Activity)context).finish();
    context = null;
}

private static void startForResult(Context context, Class<? extends Activity> targetClazz, int flags) {
    Intent intent = new Intent(context, targetClazz);
    if (isActivity(context)) return;
    ((Activity)context).startActivityForResult(intent, flags);
    context = null;
}

private static void startForResult(Context context, Class<? extends Activity> targetClazz, int flags, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    if (isActivity(context)) return;
    putParcelableExtra(intent, parcelable);
    ((Activity)context).startActivityForResult(intent, flags);
    context = null;
}

private static void setResult(Context context, Class<? extends Activity> targetClazz, int flags, Parcelable parcelable) {
    Intent intent = new Intent(context, targetClazz);
    setFlags(intent, flags);
    putParcelableExtra(intent, parcelable);
    if (isActivity(context)) return;
    ((Activity)context).setResult(flags, intent);
    ((Activity)context).finish();
}

private static boolean isActivity(Context context) {
    if (!(context instanceof Activity)) return true;
    return false;
}

private static void setFlags(Intent intent, int flags) {
    if (flags < 0) return;
    intent.setFlags(flags);
}

private static void putParcelableExtra(Intent intent, Parcelable parcelable) {
    if (parcelable == null) return;
    intent.putExtra(PARCELABLE_EXTRA_KEY, parcelable);
}

private static void putSerializableExtra(Intent intent, Serializable serializable) {
    if (serializable == null) return;
    intent.putExtra(PARCELABLE_EXTRA_KEY, serializable);
}
```

传递数据用的序列化对象，如下：
```
public class DishesStockVO implements Parcelable {

    public boolean isShowMask; 
    public int pageNum; 

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeByte(isShowMask ? (byte) 1 : (byte) 0);
        dest.writeInt(this.pageNum);
    }

    public DishesStockVO() {
    }

    protected DishesStockVO(Parcel in) {
        this.isShowMask = in.readByte() != 0;
        this.pageNum = in.readInt();
    }

    public static final Creator<DishesStockVO> CREATOR = new Creator<DishesStockVO>() {
        public DishesStockVO createFromParcel(Parcel source) {
            return new DishesStockVO(source);
        }

        public DishesStockVO[] newArray(int size) {
            return new DishesStockVO[size];
        }
    };

    @Override
    public String toString() {
        return "DishesStockVO{" +
                "isShowMask=" + isShowMask +
                ", pageNum=" + pageNum +
                '}';
    }
}
```

好像，还没入正题。这里再多说一句，beautifulSoup 写了一篇文章，说的就是 Android 路由表框架的，可以去看看——“[Android路由框架设计与实现](https://link.jianshu.com/?t=http://sixwolf.net/blog/2016/03/23/Android%E8%B7%AF%E7%94%B1%E6%A1%86%E6%9E%B6%E8%AE%BE%E8%AE%A1/)”。  

好了，回到主题，在 Presenter 中该如何处理页面跳转的问题。在这里我建议简单处理，在 View Interface 中定义好接口（方法），在 View 的实现类中去处理（本来就是它的责任，不是吗？）。在 View 的实现类中，使用 NavigationManager 工具类跳转，达到解耦的目的。如下图所示：






![对页面跳转的处理](https://upload-images.jianshu.io/upload_images/1233754-4b4d20c19806c2ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/625/format/webp)

> 显示对话框  

我在这里采用和页面跳转的处理类似的方案，这也是 View 的责任，所以让 View 自己去完成。这里建议每个模块都定义一个相应的 XxxDialogManager 类，来管理该模块所有的弹窗，当然对于弹窗本来就不多的，那就直接在 util 包中定义一个 DialogManager 类就好了。如下图：






![对显示对话框的处理](https://upload-images.jianshu.io/upload_images/1233754-c7c9c01904953f63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/625/format/webp)

#### 5.5.3. 一个页面多个View的问题

对于复杂页面，一般建议拆成多个自定义 View，那么这就引出一个问题，这时候是用一个 Presenter 好，还是定义多个 Presenter 好呢？我的建议是，每个 View Interface 对应一个 Presenter，如下图所示：

![一个页面多个 View 处理](https://upload-images.jianshu.io/upload_images/1233754-ad86e58ffd1491ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/646/format/webp)

#### 5.5.4. 一个View有两个实现类的问题

有些时候会遇到这样的问题，只是展示上有差别，两个页面上所有的操作都是一样的，这就意味着 View Interface 是一样的，只是有两个实现类。  

这个问题该怎么处理，或许可以继续使用同样的Presenter并在另一个Android组件中实现View接口。不过这个界面似乎有更多的功能，那要不要把这些新功能加进这个Presenter呢？这个视情况而定，有多种方案：一是将Presenter整合负责不同操作，二是写两个Presenter分别负责操作和展示，三是写一个Presenter包含所有操作（在两个View相似时）。记住没有完美的解决方案，编程的过程就是让步的过程。（参考自：[Christian Panadero PaNaVTEC](https://link.jianshu.com/?t=https://github.com/PaNaVTEC) 的 [Modeling my presentation layer](https://link.jianshu.com/?t=http://panavtec.me/modeling-presentation-layer)）
如下图所示：

![一个 View 多个实现类处理](https://upload-images.jianshu.io/upload_images/1233754-f9733464ef609ad7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

### 5.6. 关于 RestAPI
一般项目当中会用到很多和服务器端通信用的接口，这里建议在每个模块中都建立一个 api 包，在该包下来统一处理该模块下所有的 RestAPI。
如下图所示：

![统一管理 RestAPI](https://upload-images.jianshu.io/upload_images/1233754-29f62cd38726a5aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/300/format/webp)

对于网络请求之类需要异步处理的情况，一般都需要传入一个回调接口，来获取异步处理的结果。对于这种情况，我建议参考 onClick(View v) {} 的写法。那就是为每一个请求编一个号（使用 int 值），我称之为 taskId，可以将该编号定义在各个模块的常量类中。然后在回调接口的实现类中，可以在回调方法中根据 taskId 来统一处理（一般是在这里分发下去，分别调用不同的方法）。
如下图所示：

![定义 taskId](https://upload-images.jianshu.io/upload_images/1233754-5f8af53e854065e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/604/format/webp)

![异步任务回调处理](https://upload-images.jianshu.io/upload_images/1233754-3a726be101359b93.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/625/format/webp)

### 5.6. 关于项目中的常量管理

Android 中不推荐使用枚举，推荐使用常量，我想说说项目当中我一般是怎么管理常量的。  
灵感来自 R.java 类，这是由项目构建工具自动生成并维护的，可以进去看看，里面是一堆的静态内部类，如下图：

![Android 中的 R 文件](https://upload-images.jianshu.io/upload_images/1233754-0c1f241d7b1c69ea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/779/format/webp)

看到这，可能大家都猜到了，那就是定义一个类来管理全局的常量数据，我一般喜欢命名为 C.java。这里有一点要注意，我们的项目是按模块划分的包，所以会有一些是该模块单独使用的常量，那么这些最好不要写到全局常量类中，否则会导致 C 类膨胀，不利于管理，最好是将这些常量定义到各个模块下面。如下图所示：

![全局常量 C 类](https://upload-images.jianshu.io/upload_images/1233754-9c04ce9fc34f257d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/753/format/webp)

### 5.7. 关于第三方库

Android 开发中不可避免要导入很多第三方库，这里我想谈谈我对第三方库的一些看法。关于第三方库的推荐我就不做介绍了，很多专门说这方面的文章。

#### 5.7.1. 挑选第三方库的一些建议

+ 项目中确实需要（这不是废话吗？用不着，我要它干嘛？呵呵，建议不要为了解决一个小小的问题导入一个大而全的库）
+ 使用的人要多（大家都在用的一般更新会比较快，出现问题解决方案也多）
+ 效率和体量的权衡（如果效率没有太大影响的情况下，我一般建议选择体量小点的，如，Gson vs Jackson，Gson 胜出；还是 65K 的问题）

#### 5.7.2. 使用第三方库尽量二次封装

> 为什么要二次封装？

为了方便更换，说得稍微专业点为了降低耦合。  
有很多原因可能需要你替换项目中的第三方库，这时候如果你是经过二次封装的，那么很简单，只需要在封装类中修改一下就可以了，完全不需要去全局检索代码。  
我就遇到过几个替换第三方库的事情：

+ 替换项目中的统计埋点工具
+ 替换网络框架
+ 替换日志工具

> 那该怎么封装呢？

一般的，如果是一些第三方的工具类，都会提供一些静态方法，那么这个就简单了，直接写一个工具类，提供类似的静态方法即可（就是用静态工厂模式）。
如下代码所示，这是对系统 Log 的简单封装：

```java
/**
 * Description: 企业中通用的Log管理
 * 开发阶段LOGLEVEL = 6
 * 发布阶段LOGLEVEL = -1
 */

public class Logger {

    private static int LOGLEVEL = 6;
    private static int VERBOSE = 1;
    private static int DEBUG = 2;
    private static int INFO = 3;
    private static int WARN = 4;
    private static int ERROR = 5;
    
    public static void setDevelopMode(boolean flag) {
        if(flag) {
            LOGLEVEL = 6;
        } else {
            LOGLEVEL = -1;
        }
    }
    
    public static void v(String tag, String msg) {
        if(LOGLEVEL > VERBOSE && !TextUtils.isEmpty(msg)) {
            Log.v(tag, msg);
        }
    }
    
    public static void d(String tag, String msg) {
        if(LOGLEVEL > DEBUG && !TextUtils.isEmpty(msg)) {
            Log.d(tag, msg);
        }
    }
    
    public static void i(String tag, String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
            Log.i(tag, msg);
        }
    }
    
    public static void w(String tag, String msg) {
        if(LOGLEVEL > WARN && !TextUtils.isEmpty(msg)) {
            Log.w(tag, msg);
        }
    }
    
    public static void e(String tag, String msg) {
        if(LOGLEVEL > ERROR && !TextUtils.isEmpty(msg)) {
            Log.e(tag, msg);
        }
    }
    
}
```

现在如果想替换为 [orhanobut](https://link.jianshu.com/?t=https://github.com/orhanobut) 的 [Logger](https://link.jianshu.com/?t=https://github.com/orhanobut/logger)，那很简单，代码如下：


```java   
/**
 * Description: 通用的Log管理工具类
 * 开发阶段LOGLEVEL = 6
 * 发布阶段LOGLEVEL = -1
 */

public class Logger {

    public static String mTag = "MVPBestPractice";
    private static int LOGLEVEL = 6;
    private static int VERBOSE = 1;
    private static int DEBUG = 2;
    private static int INFO = 3;
    private static int WARN = 4;
    private static int ERROR = 5;

    static {
        com.orhanobut.logger.Logger
                .init(mTag)                     // default PRETTYLOGGER or use just init()
                .setMethodCount(3)              // default 2
                .hideThreadInfo()               // default shown
                .setLogLevel(LogLevel.FULL);    // default LogLevel.FULL
    }
    
    public static void setDevelopMode(boolean flag) {
        if(flag) {
            LOGLEVEL = 6;
            com.orhanobut.logger.Logger.init().setLogLevel(LogLevel.FULL);
        } else {
            LOGLEVEL = -1;
            com.orhanobut.logger.Logger.init().setLogLevel(LogLevel.NONE);
        }
    }
    
    public static void v(@NonNull String tag, String msg) {
        if(LOGLEVEL > VERBOSE && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.v(tag, msg);
            com.orhanobut.logger.Logger.t(tag).v(msg);
        }
    }

    public static void d(@NonNull String tag, String msg) {
        if(LOGLEVEL > DEBUG && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.d(tag, msg);
            com.orhanobut.logger.Logger.t(tag).d(msg);
        }
    }
    
    public static void i(@NonNull String tag, String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.t(tag).i(msg);
        }
    }
    
    public static void w(@NonNull String tag, String msg) {
        if(LOGLEVEL > WARN && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.w(tag, msg);
            com.orhanobut.logger.Logger.t(tag).w(msg);
        }
    }
    
    public static void e(@NonNull String tag, String msg) {
        if(LOGLEVEL > ERROR && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.e(tag, msg);
            com.orhanobut.logger.Logger.t(tag).e(msg);
        }
    }

    public static void e(@NonNull String tag, Exception e) {
        tag = checkTag(tag);
        if(LOGLEVEL > ERROR) {
//          Log.e(tag, e==null ? "未知错误" : e.getMessage());
            com.orhanobut.logger.Logger.t(tag).e(e == null ? "未知错误" : e.getMessage());
        }
    }

    public static void v(String msg) {
        if(LOGLEVEL > VERBOSE && !TextUtils.isEmpty(msg)) {
//          Log.v(mTag, msg);
            com.orhanobut.logger.Logger.v(msg);
        }
    }

    public static void d(String msg) {
        if(LOGLEVEL > DEBUG && !TextUtils.isEmpty(msg)) {
//          Log.d(mTag, msg);
            com.orhanobut.logger.Logger.d(msg);
        }
    }

    public static void i(String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
//          Log.i(mTag, msg);
            com.orhanobut.logger.Logger.i(msg);
        }
    }

    public static void w(String msg) {
        if(LOGLEVEL > WARN && !TextUtils.isEmpty(msg)) {
//          Log.w(mTag, msg);
            com.orhanobut.logger.Logger.v(msg);
        }
    }

    public static void e(String msg) {
        if(LOGLEVEL > ERROR && !TextUtils.isEmpty(msg)) {
//          Log.e(mTag, msg);
            com.orhanobut.logger.Logger.e(msg);
        }
    }

    public static void e(Exception e) {
        if(LOGLEVEL > ERROR) {
//          Log.e(mTag, e==null ? "未知错误" : e.getMessage());
            com.orhanobut.logger.Logger.e(e == null ? "未知错误" : e.getMessage());
        }
    }

    public static void wtf(@NonNull String tag, String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.t(tag).wtf(msg);
        }
    }

    public static void json(@NonNull String tag, String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.t(tag).json(msg);
        }
    }

    public static void xml(@NonNull String tag, String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
            tag = checkTag(tag);
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.t(tag).xml(msg);
        }
    }

    public static void wtf(String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.wtf(msg);
        }
    }

    public static void json(String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.json(msg);
        }
    }

    public static void xml(String msg) {
        if(LOGLEVEL > INFO && !TextUtils.isEmpty(msg)) {
//          Log.i(tag, msg);
            com.orhanobut.logger.Logger.xml(msg);
        }
    }

    private static String checkTag(String tag) {
        if (TextUtils.isEmpty(tag)) {
            tag = mTag;
        }
        return tag;
    }
```

这里是最简单的一些替换，如果是替换网络框架，图片加载框架之类的，可能要多费点心思去封装一下，这里可以参考“门面模式”。（在这里就不展开来讲如何对第三库进行二次封装了，以后有时间专门写个帖子）

#### 5.7.3. 建立单独的 Module 管理所有的第三库

原因前面已经说过了，而且操作也很简单。网上有不少拆分 Gradle 文件的方法，讲的都很不错。那我们就先从最简单的做起，赶快行动起来，把项目中用到的第三方库都集中到 Library Module 中来吧。

### 5.8. MVP vs MVVM

关于 MVP 和 MVVM 我只想说一句，它们并不是相斥的。具体它们是怎么不相斥的，[markzhai](https://link.jianshu.com/?t=http://blog.zhaiyifan.cn/) 的这篇文章“[MVPVM in Action, 谁告诉你MVP和MVVM是互斥的](https://link.jianshu.com/?t=http://blog.zhaiyifan.cn/2016/03/16/android-new-project-from-0-p3/)”说得很详细。

### 5.9. Code

抱歉，要食言了，AndroidStudio 出了点问题，代码还没写完，代码估计要这周末才能同步到 [GitHub](https://link.jianshu.com/?t=https://github.com/DIY-green/MVPBestPractice) 上了，目前只上传了一个空框架。

### 5.10. 小结

历时三天的 MVP 总结，总算要告一段落了。前期断断续续地花了将近一周左右零散的时间去调研 MVP，直到正式开始码字的时候才发现准备的还不够。看了很多文章，有观点一致的，也有观点很不一致的。最关键的是，自己对于 MVP 还没有比较深刻的认知，所以在各种观点中取舍花了很长时间。  

这算得上是我第一次真正意义上的写技术性的文章，说来惭愧，工作这么长时间了，现在才开始动笔。

总体来说，写得并不尽如人意，套一句老话——革命尚未成功，同志仍需努力。这算是一次尝试，希望以后会越写越顺畅。在这里给各位坚持看到此处的看官们问好了，祝大家一同进步。（欢迎大家围观我的 [GitHub](https://link.jianshu.com/?t=https://github.com/DIY-green)，周末更新，会渐渐提交更多有用的代码的）

## 6. 进阶与不足

鉴于本人能力有限，还有很多想写的和该写的内容没有写出来，很多地方表达的也不是很清晰。下面说一说我觉得还有哪些不足和下一步要进阶的方向。

说好的“show me the code”，代码呢？（再次抱歉了）  
上篇当中关于各种 Presenter 方案只是做了简单的罗列，并没有仔细分析各个方案的优点和不足   
没有形成自己的框架（呵呵，好高骛远了，但是梦想还是要有的...）  
没有单元测试（项目代码都还没有呢，提倡 TDD 不是，呵呵）  
很多细节没有介绍清楚（如关于Model、Domain、Entity 等概念不是很清晰)  
很多引用的观点没有指明出处（如有侵权，马上删除  
......

最后想说一句，没有完美的架构，没有完美的框架，赶紧编码吧！


## 参考：
https://segmentfault.com/a/1190000003871577 
http://www.open-open.com/lib/view/open1450008180500.html  
http://www.myexception.cn/android/2004698.html  
http://gold.xitu.io/entry/56cbf38771cfe40054eb3a34  
http://kb.cnblogs.com/page/531834/  
http://blog.zhaiyifan.cn/2016/03/16/android-new-project-from-0-p3/  
http://www.open-open.com/lib/view/open1446377609317.html  
http://my.oschina.net/mengshuai/blog/541314?fromerr=3J2TdbiW  
http://gold.xitu.io/entry/56fcf1f75bbb50004d872e74  
https://github.com/googlesamples/android-architecture/tree/todo-mvp-loaders/todoapp  
http://blog.zhaiyifan.cn/2016/03/16/android-new-project-from-0-p3/  
http://android.jobbole.com/82375/  
http://blog.csdn.net/weizhiai12/article/details/47904135  
http://android.jobbole.com/82051/  
http://android.jobbole.com/81153/  
http://blog.chengdazhi.com/index.php/115  
http://blog.chengdazhi.com/index.php/131  
http://www.codeceo.com/article/android-mvp-practice.html  
http://www.wtoutiao.com/p/h01nn2.html  
http://blog.jobbole.com/71209/  
http://www.cnblogs.com/tianzhijiexian/p/4393722.html  
https://github.com/xitu/gold-miner/blob/master/TODO/things-i-wish-i-knew-before-i-wrote-my-first-android-app.md  
http://gold.xitu.io/entry/56cd79c12e958a69f944984c  
http://blog.yongfengzhang.com/cn/blog/write-code-that-is-easy-to-delete-not-easy-to/  
http://kb.cnblogs.com/page/533808/  







