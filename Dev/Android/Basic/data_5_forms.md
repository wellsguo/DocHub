# Android 数据


## 五种数据
https://www.cnblogs.com/ITtangtang/p/3920916.html 
http://www.cnblogs.com/hanyonglu/archive/2012/03/01/2374894.html 

| 数据源 |   特性 |
| -- | -- |
| 网络请求数据 | 最常用数据获取方式，实时性好，但请求耗时 |
| 文件存取 | 1. FileInputStream openFileInput(String name); <br> 2.  FileOutputStream(String name , int mode) <br> 3. Environment.getExternalStorageDirectory() <br> **Cache**: [Acache](https://github.com/yangfuhai/ASimpleCache/tree/master/AsimpleCacheDemo/ASimpleCache/org/afinal/simplecache) / [RxCache](https://github.com/LtLei/RxCache) |
| sqlite | 轻量级嵌入式数据库引擎，支持 SQL , 只利用很少内存就有很好性能   |
| [SharedPreferences](./SharedPreference.md) | 1. 保存少量的数据，且格式简单：字符串型、数值类型，及其set。<br>2. 多用来存储应用程序的各种配置信息<br>3. 保存基于XML文件存储的key-value键值对数据。<br>- 通常用来存储一些简单的配置信息(如是否打开音效、是否使用震动效果、小游戏的玩家积分等，解锁口令密码)。 |
| ContentProvider |  跨应用数据操作 |

## 网络数据缓存

请求网络数据是在安卓开发中使用最频繁的一个功能，网络请求的体验决定了用户对整个APP的感觉，因此合理地使用缓存对网络请求的数据进行处理极为重要。合理的进行缓存和网络请求，可以为APP带来更优秀的体验。图片的缓存有Picasso、Glide、Fresco等非常著名的框架，它们极为成熟并且使用广泛，程序员应该做的是使用轮子而非重复造轮子。但对于网络数据的缓存，大多都是自用自封装，每个人都需要进行繁琐的编码工作。RxCache就对网络缓存进行了封装，并采用RxJava模式，可以与其他RxJava的代码无缝对接，使用极为方便。

RxCache使用 **LruCache** 和 **DiskLruCache** 对网络请求数据进行二级缓存，主要适配于接口 API 返回数据，不用于图片等的缓存。可以设置缓存模式、缓存大小，设置数据过期时间，并提供了根据 key 删除缓存和清空所有缓存的功能。提供了 **Gson** 方式和 **Serialize** 方式进行数据存储转换与还原。

## 二级缓存

所谓二级缓存实际上并不复杂，当 Android 端需要获得数据时比如获取网络中的图片，我们首先从内存中查找（按键查找），内存中没有的再从磁盘文件或sqlite中去查找，若磁盘中也没有才通过网络获取；当获得来自网络的数据，就以key-value对的方式先缓存到内存（一级缓存），同时缓存到文件或sqlite中（二级缓存）。

**注意：**内存缓存会造成堆内存泄露，所有一级缓存通常要严格控制缓存的大小，一般控制在**系统内存的1/4**。

理解了二级缓存大家可能会有个问题网络中的数据是变化的，数据一旦放入缓存中，再取该数据就是从缓存中获得，这样岂不是不能体现数据的变化？我们在缓存数据时会设置有效时间，比如说30分钟，若超过这个时间数据就失效并释放空间，然后重新请求网络中的数据。有的童鞋就问30分钟内咋办？那好吧，我也没招了，只有下拉刷新了， 实际上这不是问题。

> 以 Acache 为例

###### 设置缓存数据 
```java
// 将数据同时上存入一级缓存（内存Map）和二级缓存（文件）中
acache.put(key,data,time);
acache.put(key,data);  
```