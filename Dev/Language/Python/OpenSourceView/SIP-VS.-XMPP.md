## 一、前言

XMPP和SIP都是应用层协议,主要用于互联网上发送语音和即时通讯. SIP在[RFC 3621]()中定义,XMPP 在 [RFC 3920]() 中定义,

XMPP 是从**即时通讯**中演变而来, SIP 是从**VOIP**中演变而来,XMPP 为了会话协商添加了一个扩展叫做 **Jingle**,SIP 为了即时通讯业务添加了一个扩展叫做 **SIMPLE**.




### SIP (Session Initiation Protocol)

SIP 是一个应用层协议,是用在类似 VOIP 这样的场合,用来*建立,修改,中止会话*, 同时在多人会议中他也能在已有会话中加入新的会话. 

基本上 SIP 是 VOIP 中的信令协议,它处理呼叫建立,呼叫转移和产生 CDR(Call Detail Record, 供通话计费用).

##### SIMPLE

由 IETF 制定的 SIMPLE（SIP for Instant Messaging and Presence Leveraging Extensions）协议簇对 SIP 协议进行了扩展，以使其支持 IM 服务。
 
SIMPLE 增加了 MESSAGE、SUBSCRIBE 和 NOTIFY 方法，它们的作用分别如下：

- **MESSAGE**：用来发送一次性的短消息，即寻呼机模式的IM。

- **SUBSCRIBE**：用于申请者向服务器申请获得用户的呈现信息（Presence Information，通常指IM客户端在线状态信息）。

- **NOTIFY**：用于传输呈现信息。

### XMPP (Extensible Messaging Presence Protocol)

XMPP 是一个为即时通讯和请求响应业务服务的 XML 协议.

最早由 Jabber 开源社区在 1999 年开发,2002 年 XMPP 工作组为了更适合即时通讯对 Jabber 进行了扩展. 

#### Jingle 

Jingle 是 XMPP 的扩展协议。通过 Jingle 可以实现点对点（P2P）的多媒体交互会话控制，如：语音交互（VOIP），Jingle 由 Google 和 XMPP 基金会设计。

 

## 二、SIP VS. XMPP

其实我们不能简单地拿 SIP 和 XMPP 做比对, 就像我们不能直接比较比较苹果和橘子. SIP主要是为了会话协商, XMPP 主要是为了结构化数据交换,只不过随着各自对 Simple 和 Jingle 的引入,他们有了一些相似.

#### [1] SIP 提供连接的建立、修改和终止，而 XMPP 在客户端内部提供流管道，交换结构化数据。

也就是说：SIP的重点是终端之间连接的建立和维护，连接以后的数据和信息传送他不关注；而XMPP重点是考虑终端内部的数据交换，连接建立是基本的功能，而不是重点。所以，XMPP对应用的支持和扩展性的考虑很充分,比SIP天生要好.

#### [2] SIP 的信令和消息传送是基于文本的，不太好解析,或者说解析起来缺少规律性,在新增数据消息体的时候缺少继承性,需要开发新的代码来封装和解析,原有代码的继承性比较差。而 XMPP 采用 XML，是一种结构化的消息结构，能够方便地表达层次化的内容，以及内容之间的内在逻辑。这种XML结构对应用的扩展和内容的解析带来极大的方便，大量软件代码可以复用。

#### [3] SIP 信令由 header 和 body 两部分组成，也就是说，SIP 报文格式的 header 已经包含了部分内容,类似于HTTP,与具体的上层应用直接关联，而不是通用的报文格式；而 XMPP 所有信息都是采用 XML 在流管道之间透明传送。

SIP的连接建立通道与数据传送通道是各自独立的，连接建立在 SIP client 与 Server 之间，而数据传送通道是在 Client--Client 之间直接进行的。这个对视频、语音和文件传送业务很合适，但是不适合其他形式的应用。

XMPP 的控制和数据通道是一体的，Clent 只与 Server 建立连接，而 Client 与 Client 之间是没有之间连接的。Client 之间传送的通道是：```Client1---〉Server1---〉Server2---〉Client2```。这种方式看起来扩展性差，server 压力很大，但是能够实现很好的业务功能，比如留言、广播、群聊、状态更新、Blog、微博、数据共享等等。

这种C-S模型，很多业务的控制在 Server 上完成，新功能的增加在 server 上实现，在 server 上定义新的 XML 对象和逻辑，客户端只要负责 XML 数据流的解析和呈现就可以了, 所以，终端实现简单

#### [4] SIP 可以使用 UDP,TCP,TLS 进行传送,而 XMPP 仅仅使用 TCP 和 TLS 进行发送.

#### [5] SIP是双向对称，客户端和服务器都可以主动发起连接请求并响应，这种对称连接的方式在穿越 NAT 和 Firewall 的时候很麻烦，无法保证穿越 NAT。而 XMPP 是单向的连接，只有 Client 可以向 Server 发起连接请求，Server 不会向 Client 发起连接。这样便于 NAT 和 Firewall 的穿越。

 

参考文档:http://www.differencebetween.com/difference-between-sip-and-xmpp-jabber/

SIP和XMPP都是应用层的协议，主要用来在互联网上发送语音和即时通信IM。RFC 3521定义了SIP，RFC3920定义了XMPP。XMPP来自即时通信系统，而SIP类似语音和视频通信。XMPP增加了Jingle扩展协议来支持面向连接的业务，如语音和视频；而SIP增加了SIMPLE协议来支持即时通信业务。






