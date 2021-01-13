## H5 和移动端 WebView 缓存机制解析与实战

原创 叶建升 [腾讯Bugly](javascript:void(0);) *2017-06-15*

![img](http://mmbiz.qpic.cn/mmbiz_png/tnZGrhTk4dfWKseqPuud1kuhicLwg6rlLLKuEXWxD3LY2ibl1b5Rg4PE9Nk4hHL1rQbthIFIuRvguTFeQyIajIUA/640?wx_fmt=png&tp=webp&wxfrom=5)

> 作者：叶建升
> 个人主页：http://www.linkedin.com/in/jiansheng-ye-b3319778/

## 导语

web缓存是web开发逃不开的一个话题，在减少网络带宽消耗、降低服务器压力和提高页面打开速度方面有广泛应用。本文从实际web应用项目中缓存相关问题出发，较为全面地分析了html5缓存机制的原理与应用以及移动端应用webView对html5缓存机制的支持方式，以供web开发的同学们参考。

## 正文

在web项目开发中，我们可能都曾碰到过这样一个棘手的问题：

**线上项目需要更新一个有问题的资源（可能是图片，js，css,json数据等）,这个资源已经发布了很长一段时间，为什么页面在浏览器里打开还是没有看到更新？**

有些web开发经验的同学应该马上会想到，可能是资源发布出了岔子导致没有实际发布成功，更大的可能是老的资源被缓存了。说到web缓存，首先我们要弄清它是什么。Web缓存可以理解为Web资源在Web服务器和客户端（浏览器）的副本，其作用体现在减少网络带宽消耗、降低服务器压力和减少网络延迟，加快页面打开速度等方面(笔者在香港求学期间看到港台地区将cache译为“快取”，除了读音相近，大概就是贴近这层含义)。他们通常还会告诉你：ctrl+F5强刷一下，但是**本文下面的内容将会说明为什么强制刷新在去除缓存上不总是能奏效的**，更何况对于线上项目而言，总不能让所有已经访问过的用户撸起袖子岔开两个手指都强制刷新一下吧？

同时，当前原生 + html5的混合模式移动应用(hybrid APP)因可大幅降低移动应用的开发成本，并且可在用户桌面形成独立入口以及有接近原生应用的体验而大行其道，APP内嵌h5应用的开发也是本人现在工作内容重要的一部分，**本文将从实际项目开发中遇到的问题出发，一窥html5和app内webview的缓存机制真容。**

## 一、协议缓存

回到开头的那个问题，更新了一张图片，发布之后反复重新进页面总是看不到更新，这是为什么呢？

这里我们假设已经排除了资源没有发布成功过的情况，那么第一步，我们可能会认为是http协议缓存（也称为浏览器缓存或者网页缓存）。

http协议缓存机制是指通过 HTTP 协议头里的 `Cache-Control（或 Expires）`和` Last-Modified（或 Etag）`等字段来控制文件缓存的机制。

- **Cache-Control** 用于控制文件在本地缓存有效时长。最常见的，比如服务器回包：Cache-Control:max-age=600 表示文件在本地应该缓存，且有效时长是600秒（从发出请求算起）。在接下来600秒内，如果有请求这个资源，浏览器不会发出 HTTP 请求，而是直接使用本地缓存的文件。
- **Last-Modified** 是标识文件在服务器上的最新更新时间。下次请求时，如果文件缓存过期，浏览器通过 If-Modified-Since 字段带上这个时间，发送给服务器，由服务器比较时间戳来判断文件是否有修改。如果没有修改，服务器返回304告诉浏览器继续使用缓存；如果有修改，则返回200，同时返回最新的文件。

Cache-Control 通常与 Last-Modified 一起使用。一个用于控制缓存有效时间，一个在缓存失效后，向服务查询是否有更新。

Cache-Control 还有一个同功能的字段：Expires。Expires 的值一个绝对的时间点，如：Expires: Thu, 10 Nov 2015 08:45:11 GMT，表示在这个时间点之前，缓存都是有效的。

Expires 是 HTTP1.0 标准中的字段，Cache-Control 是 HTTP1.1 标准中新加的字段，功能一样，都是控制缓存的有效时间。当这两个字段同时出现时，Cache-Control 是高优化级的。

Etag 也是和 Last-Modified 一样，对文件进行标识的字段。不同的是，Etag 的取值是一个对文件进行标识的特征字串。在向服务器查询文件是否有更新时，浏览器通过 If-None-Match 字段把特征字串发送给服务器，由服务器和文件最新特征字串进行匹配，来判断文件是否有更新。没有更新回包304，有更新回包200。Etag 和 Last-Modified 可根据需求使用一个或两个同时使用。两个同时使用时，只要满足基中一个条件，就认为文件没有更新。

![img](https://upload-images.jianshu.io/upload_images/6533092-e297e26bc999fe67.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/557/format/webp)

**一个比较形象的理解：**

> 翠花：狗蛋，你几岁了？
> 狗蛋：我18岁了。(200)
> 翠花记住了狗蛋18岁(200 from cache)

=================================

> 翠花：狗蛋 ，你几岁了？我猜你18岁。
> 狗蛋：靠，知道还问我!（304）

=================================

> 翠花：狗蛋 ，你几岁了？我猜你18岁。
> 狗蛋：翠花 ，我已经19岁了。（200）

**不过有两种情况比较特殊：**

1. **手动刷新页面**（F5)，浏览器会直接认为缓存已经过期（可能缓存还没有过期），在请求中加上字段：Cache-Control:max-age=0，发包向服务器查询是否有文件是否有更新。
2. **强制刷新页面**（Ctrl+F5)，浏览器会直接忽略本地的缓存（有缓存也会认为本地没有缓存），在请求中加上字段：Cache-Control:no-cache（或 Pragma:no-cache），发包向服务重新拉取文件。

当然，各个浏览器对于刷新和强制刷新的实现方式也有一些区别。

**那么，如果线上更新了web资源，如何能让尽快更新呢？（要知道像图片这样比较少更新的资源一般缓存时间都设置得比较长，比如game.gtimg.cn域名下是一天，有问题的图片在用户侧缓存这么长时间是不可接受的）**

**方法一 修改请求header头，比如php添加：**

```php
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
header("Cache-Control: no-cache, must-revalidate");
header("Pragma: no-cache");
```

**方法二 修改html的head块：**

```html
<META HTTP-EQUIV="pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
<META HTTP-EQUIV="expires" CONTENT="Wed, 26 Feb 1997 08:21:57 GMT">
<META HTTP-EQUIV="expires" CONTENT="0">
```

**方法三：添加随机参数：**

对于图片或者css，可使用如下方式：

```html
<img src="./data/avatar_mingpian_bak.jpg?rand=h9xqeI"  width="156" height="98">
```

对于js则可以直接使用时间戳：

```html
<script language="javascript" src="UILib/Common/Common.js?time=new Date()">
```

## 二、应用缓存

除了http协议缓存，HTML5 提供一种应用程序缓存机制，使得基于web的应用程序可以离线运行。为了能够让用户在离线状态下继续访问 Web 应用，开发者需要提供一个 cache manifest 文件。这个文件中列出了所有需要在离线状态下使用的资源，浏览器会把这些资源缓存到本地。例如以下页面：

```html
<!-- calender.html -->
<!DOCTYPE HTML>
<html manifest="calender.manifest">
<head>
   <title>calender</title>
   <script src="calender.js"></script>
   <link rel="stylesheet" href="calender.css">
</head>
<body>
   <p>The time is: <output id="calender"></output></p>
</body>
</html>
```

其对应的 calender.manifest代码

```javascript
CACHE MANIFEST
calender.html
calender.css
calender.js
```

**cache manifest 格式遵循以下原则：**

1. 首行必须是 CACHE MANIFEST。
2. 其后，每一行列出一个需要缓存的资源文件名。
3. 可根据需要列出在线访问的白名单。白名单中的所有资源不会被缓存，在使用时将直接在线访问。声明白名单使用 NETWORK：标识符。
4. 如果在白名单后还要补充需要缓存的资源，可以使用 CACHE：标识符。
5. 如果要声明某 URI 不能访问时的替补 URI，可以使用 FALLBACK：标识符。其后的每一行包含两个 URI，当第一个 URI 不可访问时，浏览器将尝试使用第二个 URI。
6. 注释要另起一行，以 # 号开头。

例如以下manifest文件：

```
CACHE MANIFEST
# 上一行是必须书写
images/sound-icon.png
images/background.png
NETWORK:
comm.cgi
# 下面是另一些需要缓存的资源，在这个示例中只有一个 css 文件。
CACHE:
style/default.css
FALLBACK:
/files/projects /projects
```

**那么，如果使用了应用缓存，应该如何去更新呢？有以下两种方式**

#### 1、自动更新

浏览器除了在第一次访问 Web 应用时缓存资源外，只会在 cache manifest 文件本身发生变化时更新缓存。而 cache manifest 中的资源文件发生变化并不会触发更新。

#### 2、手动更新

开发者也可以使用 window.applicationCache 的接口更新缓存。方法是检测 window.applicationCache.status 的值，如果是 UPDATEREADY，那么可以调用 window.applicationCache.update() 更新缓存。示范代码如下。

手动更新缓存代码：

```javascript
if(window.applicationCache.status== window.applicationCache.UPDATEREADY)
{
    window.applicationCache.update();
}
```

**然而，有时候虽然应用缓存刷新了，但是还是不能看到最新的：那么有可能是使用了本地存储。**常用的本地存储有DOM Storage和webSQL和indexDB三种，细节可以搜索这篇文章 《HTML5 Storage Wars - localStorage vs. IndexedDB vs. Web SQL》，这里就不展开了，**需要注意的是，若使用本地存储，想要清理缓存，除了清理本地存储文件外，还需要重启APP，以消除内存中的备份。**

至此，一个完成的流程图就出来了： 

![img](https://upload-images.jianshu.io/upload_images/6533092-62494b2818233471.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/605/format/webp)

## 三、移动端APP如何支持html5缓存机制？

笔者现在常会和移动端APP内嵌html5页面打交道，那么移动端hybrid方式开发的APP，如何支持以上的缓存方式呢？

需要了解这些，我们先了解下hybrid方式开发的APP怎么展示网页。简单得说就是使用了webView，那么什么是webView呢？WebView是手机中内置了一款高性能webkit 内核浏览器,在SDK 中封装的一个组件。 没有提供地址栏和导航栏，WebView只是单纯的展示一个网页界面。简单地可以理解为简略版的浏览器。

### 安卓端：

#### 1、网页缓存：

在data/应用package下生成database与cache两个文件夹，请求的Url记录是保存在webviewCache.db里，而url的内容是保存在webviewCache文件夹下。

**<1> 缓存构成**

```
/data/data/package_name/cache/
/data/data/package_name/database/webview.db
/data/data/package_name/database/webviewCache.db
```

**<2> 缓存模式**

- **LOAD_CACHE_ONLY**： 不使用网络，只读取本地缓存数据，
- **LOAD_DEFAULT**：根据cache-control决定是否从网络上取数据，
- **LOAD_CACHE_NORMAL**：API level 17中已经废弃, 从API level 11开始作用同- - LOAD_DEFAULT模式，
- **LOAD_NO_CACHE**: 不使用缓存，只从网络获取数据，
- **LOAD_CACHE_ELSE_NETWORK**，只要本地有，无论是否过期，或者no-cache，都使用缓存中的数据。

如果一个页面的cache-control为no-cache，在模式LOAD_DEFAULT下，无论如何都会从网络上取数据，如果没有网络，就会出现错误页面；在LOAD_CACHE_ELSE_NETWORK模式下，无论是否有网络，只要本地有缓存，都使用缓存。本地没有缓存时才从网络上获取。如果一个页面的cache-control为max-age=60，在两种模式下都使用本地缓存数据。

#### 2、应用缓存

根据setAppCachePath(String appCachePath)提供的路径，在H5使用缓存过程中生成的缓存文件。

无模式选择，通过setAppCacheEnabled(boolean flag)设置是否打开。默认关闭，即，H5的缓存无法使用。如果要手动清理缓存，需要找到调用setAppCachePath(String appCachePath)设置缓存的路径，把它下面的文件全部删除就OK了。

### iOS端：

iOS的UIWebView组件不支持html5应用程序缓存的方式，对于协议缓存，可以使用sdk中的NSURLCache类。NSURLRequest需要一个缓存参数来说明它请求的url何如缓存数据的，我们先看下它的CachePolicy类型。

1. NSURLRequestUseProtocolCachePolicy NSURLRequest 默认的cache policy，使用Protocol协议定义，注意这种情况下默认缓存时间是60s
2. NSURLRequestReloadIgnoringCacheData 忽略缓存直接从原始地址下载。
3. NSURLRequestReturnCacheDataElseLoad 只有在cache中不存在data时才从原始地址下载。
4. NSURLRequestReturnCacheDataDontLoad 只使用cache数据，如果不存在cache，请求失败；用于没有建立网络连接离线模式；
5. NSURLRequestReloadIgnoringLocalAndRemoteCacheData：忽略本地和远程的缓存数据，直接从原始地址下载，与NSURLRequestReloadIgnoringCacheData类似。
6. NSURLRequestReloadRevalidatingCacheData:验证本地数据与远程数据是否相同，如果不同则下载远程数据，否则使用本地数据。

处于数据安全性的考虑，iOS的应用拥有自己独立的目录，用来写入应用的数据或者首选项参数。应用安装后，会有对应的home目录，基于NSURLCache来实现数据的Cache，NSURLCache会存放在home内的子目录Library/ Caches下，以Bundle Identifier为文件夹名建立Cache的存放路径。在xcode下可以管理对应的文件，具体可以搜索阅读此文：《关于 iOS 删除缓存的那些事儿》

![img](data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg==)

## 四、总结

综上所述，html5缓存主要可以分为http协议缓存、应用缓存、DOM Storage、webSQL和indexedDB几种方式，针对不同的方式清理缓存的方式也不尽相同，上文中都有说明。同时，在移动端webView层，对html缓存机制做了支持（从笔者接触过的手游和相关APP来看，目前使用默认缓存机制的比较多），项目开发过程中缓存更新和清理方式也需要有针对性地选择使用。

#### 参考文献：

> 《HTML Living Standard》
> 《HTML5 Storage Wars - localStorage vs. IndexedDB vs. Web SQL》
> 《使用 HTML5 开发离线应用》
> 《Android WebView缓存机制总结》
> 《iOS: 聊聊 UIWebView 缓存》
> 《NSURLRequestCachePolicy—iOS缓存策略》
> 《H5 缓存机制浅析 - 移动端 Web 加载性能优化》
> 《关于 iOS 删除缓存的那些事儿》