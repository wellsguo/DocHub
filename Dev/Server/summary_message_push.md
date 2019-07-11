
## [消息推送概述](https://www.cnblogs.com/xueshui20/p/4151405.html)

消息推送，就是在互联网上通过定期传送用户需要的信息来减少信息过载的一项新技术。推送技术通过自动传送信息给用户，来减少用于网络上搜索的时间。它根据用户的兴趣来搜索、过滤信息，并将其定期推给用户，帮助用户高效率地发掘有价值的信息

当我们开发需要和服务器交互的移动应用时，基本上都需要和服务器进行交互，包括上传数据到服务器，同时从服务器上获取数据。

一般情况下，客户端与服务器之间通讯客户端是主动的，但这就存在一个问题就是一旦服务器数据有更新或者服务器要下发通知给客户端只能等客户端连接的时候才能实现。这种方式使消息失去了实时性。

如何使客户端能够实时的收到服务器的消息和通知，总体来说有两种方式，第一种是客户端使用 **Pull** （拉）的方式，就是隔一段时间就去服务器上获取一下信息，看是否有更新的信息出现。第二种就是 服务器使用Push（推送）的方式，当服务器端有新信息了，则把最新的信息 **Push** 到客户端上。这样，客户端就能自动的接收到消息。 

虽然 Pull 和 Push 两种方式都能实现获取服务器端更新信息的功能，但是明显来说 Push 方式比 Pull 方式更优越。因为 Pull 方式更费客户端的网络流量，更主要的是费电量，还需要我们的程序不停地去监测服务端的变化。 


## [几种常见的解决方案实现原理](https://www.cnblogs.com/xueshui20/p/4151405.html)

1. 轮询(Pull)方式  
客户端定时向服务器发送询问消息，一旦服务器有变化则立即同步消息。

2. SMS(Push)方式  
通过拦截SMS消息并且解析消息内容来了解服务器的命令，但这种方式一般用户在经济上很难承受。

3. 持久连接(Push)方式  
客户端和服务器之间建立长久连接，这样就可以实现消息的及时行和实时性。


## [消息推送解决方案概述](https://www.cnblogs.com/xueshui20/p/4151405.html)

###  1. GOOGLE 提供的 Message Service

#### + C2DM
在Android手机平台上，Google 提供了 C2DM（Cloudto Device Messaging）服务。Android Cloud to Device Messaging (C2DM)是一个用来帮助开发者从服务器向 Android 应用程序发送数据的服务。该服务提供了一个简单的、轻量级的机制，允许服务器可以通知移动应用程序直接与服务器进行通信，以便于从服务器获取应用程序更新和用户数据。

该方案存在的主要问题是 C2DM 需要依赖于 Google 官方提供的 C2DM 服务器，由于国内的网络环境，这个服务经常不可用。

#### + GCM
Android 自带的推送 GCM 可以帮助开发人员给他们的 Android 应用程序发送数据。它是一个轻量级的消息，告诉 Android 应用程序有新的数据要从服务器获取，或者它可能是一个消息，其中包含了 **4KB** 的payload data（像即时通讯这类应用程序可以直接使用该 payload 消息）。GCM 服务处理排队的消息，并把消息传递到目标设备上运行的 Android 应用程序。[更多>>](https://www.cnblogs.com/Joanna-Yan/p/6241354.html)

优/缺点| 描述
--| --
优点 | Google提供的服务、原生、简单，无需实现和部署服务端。
缺点 | 1. 要求 Android 2.2 以上，对于不少 2.2 以前的系统没法推送；<br>2. 国内服务不稳定。而且不少国内的终端厂商纷纷把 Google 的服务去掉，替换上自己的。<br>3. 需要用户绑定 Google 账号，但不少国内用户没有 Google 账号。 


### 2. [MQTT]() 协议实现Android推送

采用MQTT协议实现Android推送功能也是一种解决方案。MQTT是一个轻量级的消息发布/订阅协议，它是实现基于手机客户端的消息推送服务器的理想解决方案。

wmqtt.jar 是IBM提供的MQTT协议的实现。我们可以从[这里](https://github.com/tokudu/AndroidPushNotificationsDemo)下载该项目的实例代码，并且可以找到一个采用 PHP 写的[服务器端实现](https://github.com/tokudu/PhpMQTTClient)。

优/缺点| 描述
--| --
优点| 协议简洁、小巧、可扩展性强、省流量、省电，目前已经应用到企业领域<br>[参考](http://mqtt.org/software)，且已有 C++ 版的服务端组件 rsmb。
缺点|不够成熟、实现较复杂、服务端组件 rsmb 不开源，部署硬件成本较高

#### + RSMB 实现推送功能

Really Small Message Broker (RSMB) ，是一个简单的 MQTT 代理，同样由 IBM 提供，其查看[地址](http://www.alphaworks.ibm.com/tech/rsmb)。缺省打开1883端口，应用程序当中，它负责接收来自服务器的消息并将其转发给指定的移动设备。[SAM](http://pecl.php.net/package/sam/download/0.2.0) 是一个针对 MQTT 写的 PHP 库。



### 3. XMPP 协议实现 Android 推送

Google 官方的 C2DM 服务器底层也是采用 XMPP 协议进行的封装。XMPP(可扩展通讯和表示协议)是基于可扩展标记语言（XML）的协议，它用于即时消息（IM）以及在线探测。这个协议可能最终允许因特网用户向因特网上的其他任何人发送即时消息。GTalk、QQ、IM等都用这个协议.

优/缺点| 描述
--| --
优点| 协议成熟、强大、可扩展性强、目前主要应用于许多聊天系统中<br>已有开源的 Java 版的开发实例 [androidpn](http://sourceforge.net/projects/androidpn/)。
缺点|协议较复杂、冗余（基于XML）、费流量、费电，部署硬件成本高。

#### + **androidpn（Android Push Notification）** 

基于 **XMPP** 开源组件的一套整合方案，服务端基于 Openfire、客户端基于Smack.

1. androidpn 服务端重启后客户端不会重连，这个非常悲剧，导致时间过长时，就再也收不到推送的信息了；
2. 由于服务器不保存消息，造成了如果客户端当前离线就收不到消息
3. androidpn 发送完消息就不管了，所以没有消息回执报表之类，造成没法做应用后续的数据分析用户体验的改善，这对于企业级的应用是个致命伤。
4. 性能上也不够稳定。

如果我们要使用androidpn，则还需要做大量的工作，需要理解 XMPP 协议、理解 Androidpn 的实现机制，需要调试内部存在的BUG。


### 4. 使用第三方平台

目前国内、国外有一些推送平台可供使用，但是涉及到收费问题、保密问题、服务质量问题、扩展问题等等，又不得不是我们望而却步。

首先看一张国内Top500 Android应用中它们用到的第三方推送以及所占数量：

<img src="https://images2015.cnblogs.com/blog/746143/201701/746143-20170101184008351-2030327868.png" width="400px" height="auto" />


### 5. HTTP 轮循方式

定时向HTTP服务端接口（Web Service API）获取最新消息。

优/缺点| 描述
--| --
优点|实现简单、可控性强，部署硬件成本低
缺点|实时性差，浪费资源

## 消息推送完美方案

综合以上论述，在建立Android消息推送方面可谓方案多多，但每一款方案都有其优缺点。但无论如何，还是自己搭建一个推送平台是上策。因为你有、他有不如自己有。

举个例子，在搭建自有推送平台上建议使用《某某Android消息推送组件》。该组不仅可以拿来即用，并且还可以提供源码以便扩展，实现自己的特殊需求。

### A、推送原理

Android消息推送组件基于XMPP协议实现Android推送。XMPP（可扩展通讯和表示协议）是基于可扩展标记语言（XML）的协议，它用于即时消息（IM）以及在线探测。这个协议可能最终允许因特网用户向因特网上的其他任何人发送即时消息。

Android消息推送组件实现原理见下图：

![图1-消息推送原理图](http://s7.51cto.com/wyfs02/M00/23/15/wKioL1Mw8-Xw8-JxAABPp3oFFg8892.jpg)

Android 消息推送组件由服务器部分和客户端部分组成。每一部分都由 XMPP 协议组件和外部接口组件构成。XMPP 协议组件负责服务器和 Android 客户端间的连接管理、消息通讯，外部接口组件负责接收应用系统、客户端应用的命令，向应用系统发送接收到的通知消息。

Android 消息组件提供基于 Tomcat 的服务器应用和 Android 开发jar包。其中基于 Tomcat 的服务器应用直接在 Tomcat 上部署即可，Android开发jar包引入Android项目即可。

### B 集成方式

#### 1）服务器部署

Android 消息组件 Tomcat 的服务器应用直接部署在 Tomcat 中，端口号任意设定。

#### 2）客户端 jar 包引用

在 Android 项目中建立 libs 目录，然后将提供的 Android 开发 jar 包复制到该目录即可。

[图2-jar包引入图]()

#### 3）Android 项目 AndroidManifest.xml 文件修改

在该文件中增加以下权限：
 
```xml
<uses-permission android:name="android.permission.READ_PHONE_STATE" /> 
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" /> 
<uses-permission android:name="android.permission.INTERNET" /> 
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" /> 
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" /> 
<uses-permission android:name="android.permission.VIBRATE" /> 
```

在该文件中注册服务：
 
```xml
<service android:enabled="true" 
    android:name="com.bjjrs.server.NotificationService" 
    android:label="NotificationService"> 
    <intent-filter> 
        <action android:name="com.bjjrs.server.NotificationService" /> 
     </intent-filter> 
</service> 
```

至此，Android消息组件集成工作完成。

### C、接口方式

#### 1）服务器端接口采用基于http协议的访问方式，采用http协议从服务器中获取各种信息，实现通知消息的推送。

如使用以下方式和参数就可以实现各种用户消息的查询：

http://localhost:8080/user.do?action=getAllUser&isOnline=&userID=&userType=&deptID=&deptName=&realName=

使用如下方式就可以实现各种消息的推送：

http://localhost:8080/notification.do?action=pushNoti&userNames=&title=&content=

#### 2）Android客户端接口采用广播机制。

消息接收：当XMPP协议组件接收到推送消息时，将按照一定格式广播该消息，通知客户端其他应用接收并处理该消息。

消息发送：客户端应用需要向服务器或者其他客户端发送即时消息时，只需按一定格式广播该消息，XMPP组件就会自动接收该消息并发送到指定的其他客户端。

### D、优势特点

*1.* 系统集成简单，无需复杂的设置。

*2.* Android客户端应用和Android消息推送组件完全分离，通过接口相互调用，实现模块应用最优化。

*3.* 客户端通讯机制采用广播方式，给客户端应用带来极大的灵活性和可扩展性，可以自由处理接收到的推送消息。

*4.* Android消息推送组件在服务器端具备消息存储、消息重发、消息路由等功能，在客户端部分具备断线重连、、收到确认、阅读确认、消息发送、命令执行等功能，确保消息能够推送到客户端，同时也保证客户端能够收到、阅读消息。

### E、 应用范围

Android消息推送组件可在以下场景中使用：

*1.* 用于消息推送。如：通知下达、应急指挥等。

*2.* 用户及时消息交互。如在线聊天、工作情况交互等。

*3.* 用于远程控制。如控制远程客户端的状态、数据上报等。




