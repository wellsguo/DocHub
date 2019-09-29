
## Flutter混合开发：Android接入Flutter

`Flutter`  `混合开发`

### 前言

Flutter Google 推出已经已经一年多了，单个 Flutter 项目的开发流程已经很成熟了。对与个人开发者来说使用 Flutter 开发一个跨平台的 App 挺有意思。但是对于现有的项目改造来说还是不建议，Flutter 中的控件还没有完全能满足我们的要求，我们需要解决这个问题会消耗我们大量的研发资源。

虽然 Flutter 无法接入我们的项目，但是我们可以尝试者去模仿 Flutter 在项目中的使用场景。下边我讲讲我在 Android 和 Flutter 的混合开发实践的躺坑之旅。

### 官方指导

[Add Flutter to existing apps](https://github.com/flutter/flutter/wiki/Add-Flutter-to-existing-apps)

### 实践

#### 创建Flutter模块

如果你存在一个 Android app 的路径是 some/path/MyApp ，你希望创建你的 Flutter 项目作为子模块：

```bash
1 $ cd some/path/
2 $ flutter create my_flutter # 是创建纯 Flutter 项目的命令
3 $ flutter create -t module my_flutter
```

你能得到一个创建好的 some/path/my_flutter 的 Flutter 项目，它包含了一部分Dart 的代码。其中有一个 .android/ 的隐藏的子文件夹，它包装了Android库中的模块项目。

#### 使主 app 依赖 Flutter 模块  

在主 App 的 setting.gradle 文件中包含 Flutter 模块作为子模块。

```groovy
1 // MyApp/settings.gradle
2 include ':app'                                     // assumed existing content
3 setBinding(new Binding([gradle: this]))                                 // new
4 evaluate(new File(                                                      // new
5   settingsDir.parentFile,                                               // new
6   'my_flutter/.android/include_flutter.groovy'                          // new
7 ))
```

这个绑定和脚本评估允许 Flutter 模块可以包含自己（作为:flutter），在你自己的 setting.gradle 文件中， 任何 Flutter 插件可以作为模块使用（作为 :package_info , :video_player 等）。

在你的 app 采用 implementation 方式依赖 Flutter 模块：

```groovy
1 // MyApp/app/build.gradle
2 :
3 dependencies {
4   implementation project(':flutter')
5   :
6 }
```

#### 在你的 Java 代码中使用 Flutter 模块

使用 Flutter 模块的 Java 接口 ***Flutter.createView*** ，可以在你的 app 中添加 FlutterView 。

- addView

```java
1 // MyApp/app/src/main/java/some/package/MainActivity.java
2 public class MainActivity extends AppCompatActivity {
3     @Override
4     protected void onCreate(Bundle savedInstanceState) {
5         super.onCreate(savedInstanceState);
6         setContentView(R.layout.activity_main);
7         FrameLayout frameLayout = findViewById(R.id.flutter_root);
8         View flutterView = Flutter.createView(MainActivity.this, getLifecycle(), "route1");
9         FrameLayout.LayoutParams layout = new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT);
10        frameLayout.addView(flutterView, layout);
11     }
12 }
```


- setContentView

```java
1 // MyApp/app/src/main/java/some/package/MainActivity.java
2 public class MainActivity extends AppCompatActivity {
3     @Override
4     protected void onCreate(Bundle savedInstanceState) {
5         View flutterView = Flutter.createView(MainActivity.this, getLifecycle(), "route1");
6         FrameLayout.LayoutParams layout = new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT);
7         setContentView(flutterView, layout);
8     }
9 }
```

#### fragment

也可以创建一个负责管理自己生命周期的 FlutterFragment。

```java
1 //io.flutter.facade.Flutter.java
2 public static FlutterFragment createFragment(String initialRoute) {
3     final FlutterFragment fragment = new FlutterFragment();
4     final Bundle args = new Bundle();
5     args.putString(FlutterFragment.ARG_ROUTE, initialRoute);
6     fragment.setArguments(args);
7     return fragment;
8 }
9 //io.flutter.facade.FlutterFragment.java
10 public class FlutterFragment extends Fragment {
11     public static final String ARG_ROUTE = "route";
12     private String mRoute = "/";
13 
14     @Override
15     public void onCreate(Bundle savedInstanceState) {
16         super.onCreate(savedInstanceState);
17         if (getArguments() != null) {
18             mRoute = getArguments().getString(ARG_ROUTE);
19         }
20     }
21 
22     @Override
23     public void onInflate(Context context, AttributeSet attrs, Bundle savedInstanceState) {
24         super.onInflate(context, attrs, savedInstanceState);
25     }
26 
27     @Override
28     public FlutterView onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
29         return Flutter.createView(getActivity(), getLifecycle(), mRoute);
30     }
31 }
```


### dart代码交互

上面我们使用了 ***route1*** 字符串告诉 Flutter 模块中的 Dart 代码展示那个 widget 。在 Flutter 模块项目的模板文件 lib/main.dart 中的可以使用 `window.defaultRouteName` 作为提供路由选择的字符串，通过 runApp 决定创建那个 widget 。

```Dart
1 import 'dart:ui';
2 import 'package:flutter/material.dart';
3 
4 void main() => runApp(_widgetForRoute(window.defaultRouteName));
5 
6 Widget _widgetForRoute(String route) {
7   switch (route) {
8     case 'route1':
9       return SomeWidget(...);
10     case 'route2':
11       return SomeOtherWidget(...);
12     default:
13       return Center(
14         child: Text('Unknown route: $route', textDirection: TextDirection.ltr),
15       );
16   }
17 }
```

### 构建和运行你的 app

一般在使用 Android Studio 中，你可以构建和运行 Myapp ，完全和在添加 Flutter 模块依赖项之前相同。也可以同样的进行代码的编辑、调试和分析。


### 报错和解决

整个接入的过程一般是不会有问题的，但是呢？我们不按照官方提供的文档上自己一顿操作可能会产生其他的问题。

#### 关联项目报错

```
AILURE: Build failed with an exception.

* Where:
Settings file '/Users/tanzx/AndroidStudioWorkSapce/GitHub/MyApp/settings.gradle' line: 6

* What went wrong:
A problem occurred evaluating settings 'MyApp'.
> /Users/tanzx/AndroidStudioWorkSapce/GitHub/MyApp/my_flutter/.android/include_flutter.groovy (/Users/tanzx/AndroidStudioWorkSapce/GitHub/MyApp/my_flutter/.android/include_flutter.groovy)

* Try:
Run with --stacktrace option to get the stack trace. Run with --info or --debug option to get more log output. Run with --scan to get full insights.

* Get more help at https://help.gradle.org

BUILD FAILED in 0s
```

##### 报错原因：

将创建的 Flutter 模块放在了 MyApp 文件夹的内部，地址搞错。

##### 解决方法：

- 将 Flutter 放在 MyApp 的外层；
- 将 setting.gradle 配置文件中的， 'my_flutter/.android/include_flutter.groovy' 改为 'MyApp/my_flutter/.android/include_flutter.groovy' ；

### 更多

- [闲鱼Flutter混合工程持续集成的最佳实践](https://yq.aliyun.com/articles/618599?spm=a2c4e.11153959.0.0.4f29616b9f6OWs)
- [头条团队方案](https://mp.weixin.qq.com/s/wdbVVzZJFseX2GmEbuAdfA)
- [Flutter与Android混合开发及Platform Channel的使用](https://www.jianshu.com/p/1317aed6cd8c)
