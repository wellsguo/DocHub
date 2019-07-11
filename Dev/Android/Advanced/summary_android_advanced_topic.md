# Android 高级技术篇

* 热修复、热更新  
* 模块化
* 组件化
* 插件化


## （一）概述

### 热修复、热更新

强调的是修改线上版本的bug，用技术去实现不更新整个 apk 的条件下，修改掉bug。

涉及到类的加载。比如可以 new 一个 **BaseDexClassLoader** 动态的去加载修复 apk 的 dex 文件，再合并到正在运行 **PathClassLoader** 中(这只是其中一种思路)目前主流的热修复框架阿里AndFix、Sophix，微信Tinker，饿了么Amigo，美团Robust，他们的区别就不多说了，网上很多对比。其中收费的阿里的Sophix目前是做的最好的，免费的Amigo最好用吧。


### 增量更新

比如说王者荣耀，不可能每次更新就去下几百M，通过生成差分包的供下载，再合并达到更新的方式(主要是生成差分包和合并的工作--不太熟悉)。

### 插件化

通过hook，动态代理等方式，启动另一个apk中的activity，或使用另一个apk的资源。主流的有360的DroidPlugin，Small，DynamicAPK(携程)。推荐360的DroidPlugin。

强调的是想把需要实现的模块或功能当做一个独立的模块提取出来

涉及动态代理，ClassLoader，以及另一个apk资源的加载
