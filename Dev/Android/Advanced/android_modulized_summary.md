## Android 模块化（一）：概述

### 1. 为什么要模块化？

- **逻辑结构清晰**  
各个模块的代码实现分离，不会搅在一起。在代码 review 或者二次开发的时候一目了然，不会满世界去找代码。
- **便于协同开发**  
协同开发时更灵活，不用再等同组其他同事的模块开发完成后才能运行 app，自己负责的模块稍加修改就可以当做主 app 直接跑起来。
- **便于维护**  
每个模块的代码、布局文件、资源文件可以随时从项目中通过 gradle 配置去除掉。



### 2. 模块化要解决的问题

- 模块间页面跳转（路由）；

- 模块间事件通信；

- 模块间服务调用；

- 模块的独立运行；

- 模块间页面跳转路由拦截（登录）

- 其他注意事项；


### 3. 模块化分

![](https://img-blog.csdn.net/20171208150423643?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvaHVhbmd4aWFvZ3VvMQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

- app 模块  
 主模块。按需配置模块，同时进行一些初始化工作。

- lib_base  
 router 管理，和放置一些各个模块公用的封装类。
  - 关于 base 模块，大家也可以继续拆分一些细的模块，比如把router 独立处理，但是不建议拆分太多，因为 base 模块是会变动较大，就是在版本的迭代过程中，不断变化的，被拆分较多的话开发起来不是很方便。
  - 因为有依赖的传递的关系，base 是项目中依赖较多模块，当设计到底层较多模块修改，那么就需要一层一层的在传递上去。 
  - base 模块应该是与业务无关的模块。
  - 建议，base 模块负责管理 Router，同时提供一些基础的东西，比如 BaseActivit，Util 资源等。假如自家有 sdk，网络库依赖等，也将其放入在 base 模块中。

- lib_icon  
 放置图片、assets、xml 等公用资源文件

- 其他  
  - module_home 首页  
  - module_caht 微聊
  - module_recom 推荐
  - module_me 我的

