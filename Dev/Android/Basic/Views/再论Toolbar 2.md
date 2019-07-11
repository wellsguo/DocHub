# Toolbar + AppbarLayout [](https://blog.csdn.net/briblue/article/details/77075198)

Material Design 是个好东西，它的出现使得 Android 也能定制高颜值的界面，并且指导了如果实现复杂炫丽的交互效果，而 Android Surpport Desgin 这个支持包就是 Android 官方对 Material Design 的代码实现。

Android Support Desgin 这个包中提供了一系列的组件如：CoordinatorLayout、AppBarLayout、FloatingActionButton 等等。其中 CoordinatorLayout 是核心，它是包内其它组件能够正常工作的前提。

## 1. CoordinatorLayout、AppBarLayout、Toolbar 之间的关系

有同学可能不是太了解 CoordinatorLayout 这个类，其实没有太大的关系，下面我会简单介绍一下它的大致功能。
在 Android 为实现 Material Design 提供的支持包 android support design 中，CoordinatorLayout 毫无疑问是最核心的，它通过子 View 对象配置的 **Behavior**，实现了子 View 与 CoordinatorLayout、子 View 与子 View 之间一系列复杂的交互。
所以，CoordinatorLayout 编程的关键是它的子 View 们配置的 **Behavior**.

AppBarLayout 本身有默认的 Behavior,这使得它能够响应依赖对象的位置变化或者是 CoordinatorLayout 中产生的嵌套滑动事件，这从它的源码中可以看出来。

```java
@CoordinatorLayout.DefaultBehavior(AppBarLayout.Behavior.class)
    public class AppBarLayout extends LinearLayout {
}
```

AppBarLayout 对象默认配置了一个 Behavior。而正是这个 Behavior，它会响应外部的嵌套滑动事件，然后根据特定的规则去伸缩和滑动内部的子 View。本文的主要目的就是要讲解这些特定的规则及它们作用后的效果。

AppBarLayout 本身想提供一个 AppBar 的概念，所以严格地讲它本身与 Toolbar 没有直接的关系。**AppBarLayout 内部的子 View 不一定非要是 Toolbar,它可以是任何 View，比如，你可以放置进去一张图片、一个列表、一个 ViewPager 等等**。 

![](https://img-blog.csdn.net/20170811002255821?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYnJpYmx1ZQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

我们知道，Android 的历史进程中，大概有 TitleBar、ActionBar、Toolbar 的进化，这是 Android 设计语言的改良过程。而后来随着 Material Design 设计的出现,它又提供了 AppBar 的概念，而 AppBarLayout 则是 AppBar 在 Android 中的代码实现。 

![](https://img-blog.csdn.net/20170811001812658?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYnJpYmx1ZQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

AppBarLayout 虽然和 Toolbar 没有直接联系，但是当 Toolbar 内置在 AppbarLayout 中的时候，Toolbar 的效果增强了，这使得开发者非常愿意用 AppBarLayout 与 Toolbar 配合使用，这比单独使用 Toolbar 炫丽的多。所以，基本上有 AppBarLayout 的地方就有 Toolbar。通过 AppBarLayout 实现一个可伸缩折叠的 Toolbar 也是本文的目的。

> TIPS

当我们运用 support design 中的组件时，我们应该拥有下面几个最基本的意识：

1. CoordinatorLayout 是这个库的组织容器，一切基于 support design 扩展出来的特性都应该发生在 CoordinatorLayout 及它的子 View 体系中。

2. AppbarLayout 应该作为一个 CoordinatorLayout 的直接子 View，否则它与普通的 LinearLayout 无异。

3. AppbarLayout 的子 View 不仅仅是 Toolbar,它们可以是任何的 View，但通常和 Toolbar 配合使用。

## 2. AppBarLayout 基本使用方法
AppBarLayout 是 android support design 这个支持包中的类，前面说过它的一切效果都建立在 CoordinatorLayout 这个父类容器之上，AppBarLayout 要想正常发挥它的所有特性，那么它必须作为 CoordinatorLayout 的直接子类。

### 2.1 引入依赖
android support design 没有内置在 SDK 中，所以我们需要引入依赖。
```gradle
compile 'com.android.support:design:25.0.1'
```
### 2.2 与嵌套滑动组件配合
在 AppBarLayout 官方文档注释中有这么一段。

> AppBarLayout 需要和一个独立的兄弟 View 配合使用，这个兄弟 View 是一个嵌套滑动组件，只有这样 AppBarLayout 才能知道什么时候开始滑动。它们之间关系的绑定通过给嵌套滑动的组件设立特定的 Behavior,那就是 AppBarLayout.ScrollingViewBehavior。

然后，官方还给出了示例。

```xml
<android.support.design.widget.CoordinatorLayout
         xmlns:android="http://schemas.android.com/apk/res/android"
         xmlns:app="http://schemas.android.com/apk/res-auto"
         android:layout_width="match_parent"
         android:layout_height="match_parent">

     <android.support.v4.widget.NestedScrollView
             android:layout_width="match_parent"
             android:layout_height="match_parent"
             app:layout_behavior="@string/appbar_scrolling_view_behavior">

         <!-- Your scrolling content -->

     </android.support.v4.widget.NestedScrollView>

     <android.support.design.widget.AppBarLayout
             android:layout_height="wrap_content"
             android:layout_width="match_parent">

         <android.support.v7.widget.Toolbar
                 ...
                 app:layout_scrollFlags="scroll|enterAlways"/>

         <android.support.design.widget.TabLayout
                 ...
                 app:layout_scrollFlags="scroll|enterAlways"/>

     </android.support.design.widget.AppBarLayout>

 </android.support.design.widget.CoordinatorLayout>
 ```

上面布局文件中，NestedScrollView 就是那个配套的滑动组件，它需要和 AppBarLayout 进行绑定，所以它必须指定 Behavior。在 xml 中通过

```xml
app:layout_behavior="@string/appbar_scrolling_view_behavior"
```

多说两句，有同学可能会想一定要是 NestedScrollView 吗？

当然不是，在 CoordinatorLayout 中嵌套滑动的本质是一个 NestedScrollingChild 对象。

NestedScrollingChild 是一个接口，目前它的实现类有 4 个。 

所以除了使用 NestedScrollView,我们还经常使用 RecyclerView 和 SwipeRefreshLayout 作为配套的嵌套滑动组件，这是其它博文都没有提到的，希望大家注意。

可能大家注意到了上面示例中有 app:layout_scrollFlags 这样的属性，大家一定很好奇，它们是如何作用的。不要着急，下面就讲这一块的内容。


