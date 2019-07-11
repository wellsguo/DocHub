# Android 图片库比较
作者：Rtia  
链接：https://www.jianshu.com/p/44a4ee648ab4  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。 

  | Imageloader | Picasso | Glide | Fresco
 -- | --| -- | --| --
 author | nostra13 | Square | Sam sjudd | Facebook
 startup | 2011/09 | 2013/02 | 2012/12 | 2015/03

## 基本概念
在正式对比前，先了解几个图片缓存通用的概念

  NOTION | DESC.
  --|--
**RequestManager**|请求生成和管理模块
**Engine**|引擎部分，负责创建任务（获取数据），并调度执行
**GetDataInterface**|数据获取接口，负责从各个数据源获取数据。比如 MemoryCache 从内存缓存获取数据、DiskCache 从本地缓存获取数据，下载器从网络获取数据等
**Displayer**|资源（图片）显示器，用于显示或操作资源。 比如 ImageView，这几个图片缓存都不仅仅支持 ImageView，同时支持其他 View 以及虚拟的 Displayer 概念
**Processor**| 资源（图片）处理器， 负责处理资源，比如旋转、压缩、截取等

以上概念的称呼在不同图片缓存中可能不同，比如 Displayer 在 ImageLoader 中叫做 ImageAware，在 Picasso 和 Glide 中叫做 Target。

## 共同优点
1. 使用简单  
  都可以通过一句代码可实现图片获取和显示。
2. 可配置度高，自适应程度高  
  图片缓存的下载器（重试机制）、解码器、显示器、处理器、内存缓存、本地缓存、线程池、缓存算法等大都可轻松配置。  
  自适应程度高，根据系统性能初始化缓存配置、系统信息变更后动态调整策略。  
  比如根据 CPU 核数确定最大并发数，根据可用内存确定内存缓存大小，网络状态变化时调整最大并发数等。
3. 多级缓存  
  都至少有两级缓存、提高图片加载速度。
4. 支持多种数据源  
  支持多种数据源，网络、本地、资源、Assets 等
5. 支持多种 Displayer  
  不仅仅支持 ImageView，同时支持其他 View 以及虚拟的 Displayer 概念。   
  其他小的共同点包括支持动画、支持 transform 处理、获取 EXIF 信息等。

## Imageloader
![ImageLoader](https://upload-images.jianshu.io/upload_images/9028834-cc780c4cd84b1c01.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/580/format/webp)

上面是 ImageLoader 的总体设计图。整个库分为 ImageLoaderEngine，Cache 及 ImageDownloader，ImageDecoder，BitmapDisplayer，BitmapProcessor 五大模块，其中 Cache 分为 MemoryCache 和 DiskCache 两部分。

简单的讲就是 ImageLoader 收到加载及显示图片的任务，并将它交给 ImageLoaderEngine，ImageLoaderEngine 分发任务到具体线程池去执行，任务通过 Cache 及 ImageDownloader 获取图片，中间可能经过 BitmapProcessor 和 ImageDecoder 处理，最终转换为Bitmap 交给 BitmapDisplayer 在 ImageAware 中显示。


