## 参考链接
[1] https://www.cnblogs.com/lin3615/p/5653234.html   
[2] https://blog.csdn.net/wunianjiumeng/article/details/79642643  
[3] https://blog.csdn.net/guangmingsky/article/details/78581651  

## 前言 
套用古龙武侠小说套路来说，代理服务技术是一门很古老的技术，是在互联网早期出现就使用的技术。一般实现代理技术的方式就是在服务器上安装代理服务软件，让其成为一个代理服务器，从而实现代理技术。常用的代理技术分为`正向代理`、`反向代理`和`透明代理`。本文就是针对这三种代理来讲解一些基本原理和具体的适用范围，便于大家更深入理解代理服务技术[[1]](https://www.cnblogs.com/lin3615/p/5653234.html)。

## 一、正向代理(Forward Proxy) 

一般情况下，如果没有特别说明，代理技术默认说的是正向代理技术。关于正向代理的概念如下：  

**正向代理**(forward)是一个位于客户端`用户A`和原始服务器(origin server)`服务器B`之间的服务器代理`服务器Z`，为了从原始服务器取得内容，`用户A`向代理`服务器Z`发送一个请求并指定目标(`服务器B`)，然后代理`服务器Z`向`服务器B`转交请求并将获得的内容返回给客户端。客户端必须要进行一些特别的设置才能使用正向代理。如下图1.1

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708140606796-900029688.jpg)  
**图 1.1**

从上面的概念中，我们看出，文中所谓的**正向代理就是代理服务器替代访问方`用户A`去访问目标服务器`服务器B`
这就是正向代理的意义所在**。而为什么要用代理服务器去代替访问方`用户A`去访问`服务器B`呢？这就要从代理服务器使用的意义说起。

###### 使用正向代理服务器作用主要有以下几点：

##### 1、访问本无法访问的服务器B

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708140714874-248025558.jpg)   
**图 1.2**

我们抛除复杂的网络路由情节来看图1.2，假设图中路由器从左到右命名为R1,R2假设最初`用户A`要访问`服务器B`需要经过R1和R2路由器这样一个路由节点，如果路由器R1或者路由器R2发生故障，那么就无法访问`服务器B`了。但是如果`用户A`让代理`服务器Z`去代替自己访问`服务器B`，由于代理`服务器Z`没有在路由器R1或R2节点中，而是通过其它的路由节点访问`服务器B`，那么`用户A`就可以得到`服务器B`的数据了。现实中的例子就是“FQ”。不过自从VPN技术被广泛应用外，“FQ”不但使用了传统的正向代理技术，有的还使用了VPN技术。

##### 2、加速访问服务器B
这种说法目前不像以前那么流行了，主要是带宽流量的飞速发展。早期的正向代理中，很多人使用正向代理就是提速。还是如图1.2
假设`用户A`到`服务器B`，经过R1路由器和R2路由器，而R1到R2路由器的链路是一个低带宽链路。而`用户A`到代理`服务器Z`，从代理`服务器Z`到`服务器B`都是高带宽链路。那么很显然就可以加速访问`服务器B`了。

##### 3、Cache作用
Cache（缓存）技术和代理服务技术是紧密联系的（不光是正向代理，反向代理也使用了Cache（缓存）技术。还如上图所示，如果在`用户A`访问`服务器B`某数据J之前，已经有人通过代理`服务器Z`访问过`服务器B`上得数据J，那么代理`服务器Z`会把数据J保存一段时间，如果有人正好取该数据J，那么代理`服务器Z`不再访问`服务器B`，而把缓存的数据J直接发给`用户A`。这一技术在Cache中术语就叫Cache命中。如果有更多的像`用户A`的用户来访问代理`服务器Z`，那么这些用户都可以直接从代理`服务器Z`中取得数据J，而不用千里迢迢的去`服务器B`下载数据了。

##### 4、客户端访问授权
这方面的内容现今使用的还是比较多的，例如一些公司采用ISA SERVER做为正向代理服务器来授权用户是否有权限访问互联网，挼下图1.3

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708140858983-1802960832.jpg)  
**图 1.3**

图1.3防火墙作为网关，用来过滤外网对其的访问。假设`用户A`和`用户B`都设置了代理服务器，`用户A`允许访问互联网，而`用户B`不允许访问互联网（这个在代理`服务器Z`上做限制）这样`用户A`因为授权，可以通过代理服务器访问到`服务器B`，而`用户B`因为没有被代理`服务器Z`授权，所以访问`服务器B`时，数据包会被直接丢弃。

##### 5、隐藏访问者的行踪
如下图1.4 我们可以看出`服务器B`并不知道访问自己的实际是`用户A`，因为代理`服务器Z`代替`用户A`去直接与`服务器B`进行交互。如果代理`服务器Z`被`用户A`完全控制（或不完全控制），会惯以“肉鸡”术语称呼。

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708141008233-1501364711.jpg)  
**图 1.4 **

我们总结一下 正向代理是一个位于客户端和原始服务器(origin server)之间的服务器，为了从原始服务器取得内容，客户端向代理发送一个请求并指定目标(原始服务器)，然后代理向原始服务器转交请求并将获得的内容返回给客户端。客户端必须设置正向代理服务器，当然前提是要知道正向代理服务器的IP地址，还有代理程序的端口。

## 二、反向代理（reverse proxy）

反向代理正好与正向代理相反，对于客户端而言代理服务器就像是原始服务器，并且客户端不需要进行任何特别的设置。客户端向反向代理的命名空间(name-space)中的内容发送普通请求，接着反向代理将判断向何处(原始服务器)转交请求，并将获得的内容返回给客户端。
使用反向代理服务器的作用如下：

##### 1、  保护和隐藏原始资源服务器

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708141141139-1712830564.jpg)  
**图 2.1**

`用户A`始终认为它访问的是原始`服务器B`而不是代理`服务器Z`，但实用际上反向代理服务器接受`用户A`的应答，从原始资源`服务器B`中取得`用户A`的需求资源，然后发送给`用户A`。由于防火墙的作用，只允许代理`服务器Z`访问原始资源`服务器B`。尽管在这个虚拟的环境下，防火墙和反向代理的共同作用保护了原始资源`服务器B`，但`用户A`并不知情。

##### 2、  负载均衡

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708141233749-566667619.jpg)  
**图 2.2**

当反向代理服务器不止一个的时候，我们甚至可以把它们做成集群，当更多的用户访问资源`服务器B`的时候，让不同的代理`服务器Z`（x）去应答不同的用户，然后发送不同用户需要的资源。

##### 3、  CACHE
当然反向代理服务器像正向代理服务器一样拥有CACHE的作用，它可以缓存原始资源`服务器B`的资源，而不是每次都要向原始资源`服务器B`请求数据，特别是一些静态的数据，比如图片和文件，如果这些反向代理服务器能够做到和用户X来自同一个网络，那么用户X访问反向代理服务器X，就会得到很高质量的速度。这正是CDN技术的核心。如下图2.3

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708141326249-830450274.jpg)   
**图 2.3**
 
我们并不是讲解CDN，所以去掉了CDN最关键的核心技术智能DNS。只是展示CDN技术实际上利用的正是反向代理原理这块。反向代理结论与正向代理正好相反，对于客户端而言它就像是原始服务器，并且客户端不需要进行任何特别的设置。客户端向反向代理的命名空间(name-space)中的内容发送普通请求，接着反向代理将判断向何处(原始服务器)转交请求，并将获得的内容返回给客户端，就像这些内容原本就是它自己的一样。基本上，网上做正反向代理的程序很多，能做正向代理的软件大部分也可以做反向代理。开源软件中最流行的就是squid，既可以做正向代理，也有很多人用来做反向代理的前端服务器。另外MS ISA也可以用来在WINDOWS平台下做正向代理。反向代理中最主要的实践就是WEB服务，近些年来最火的就是Nginx了。网上有人说NGINX不能做正向代理，其实是不对的。NGINX也可以做正向代理，不过用的人比较少了。

## 三、透明代理
如果把正向代理、反向代理和透明代理按照人类血缘关系来划分的话。那么正向代理和透明代理是很明显堂亲关系，而正向代理和反向代理就是表亲关系了。透明代理的意思是客户端根本不需要知道有代理服务器的存在，它改编你的request fields（报文），并会传送真实IP。注意，加密的透明代理则是属于匿名代理，意思是不用设置使用代理了。透明代理实践的例子就是时下很多公司使用的行为管理软件。如下图3.1

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708141416030-876700397.jpg)  
**图3.1**

`用户A`和`用户B`并不知道行为管理设备充当透明代理行为，当`用户A`或`用户B`向服务器A或`服务器B`提交请求的时候，透明代理设备根据自身策略拦截并修改`用户A`或B的报文，并作为实际的请求方，向服务器A或B发送请求，当接收信息回传，透明代理再根据自身的设置把允许的报文发回至`用户A`或B，如上图，如果透明代理设置不允许访问`服务器B`，那么`用户A`或者`用户B`就不会得到`服务器B`的数据。

## 大型网站的负载均衡器、db proxy和db

本文主要分析网站后台架构中的负载均衡器，企业常用的`硬件负载均衡器`、`软件负载均衡器`、`数据库代理服务器`和`数据库`。

### 1.1 负载均衡

在大型网站部署中，负载均衡至少有三层部署。第一层为web server或者缓存代理之上的负载均衡，第二层为数据库之上的负载均衡，第三层为存储设备之上的负载均衡。

在第一层部署中，最常使用的是硬件负载均衡器有F5 BIG-IP、Citrix NetScaler、Radware、Cisco CSS、Foundry等产品。这些产品价格不菲，高达几十万人民币。在中国大陆，采用F5Network公司的BIG-IP负载均衡交换机的网站有新浪网、雅虎、百度、搜狐、凤凰网、央视国际、中华英才网、猫扑、畅游等。之前淘宝采用 NetScaler作为其硬件负载均衡器。后来用软件负载均衡器LVS和HAproxy混合使用来代替硬件负载均衡器。硬件负载均衡器可以提供[OSI](https://www.cnblogs.com/Robin-YB/p/6668762.html)参考模型的第四/七层进行负载均衡。在第七层实现负载均衡的原理是，通过检查流经的HTTP报头，根据报头内的信息来执行负载均衡任务。在第四层(网络层)实现负载均衡的DR模式的原理是，通过更改请求包的目的MAC地址来进行负载均衡。

<table  cellspacing="0" cellpadding="0">
<tbody>
<tr>
<td valign="bottom">
<p align="center">OSI七层网络模型</p>
</td>
<td valign="bottom">
<p align="center">TCP/IP四层概念模型 &nbsp;</p>
</td>
<td valign="bottom">
<p align="center">对应网络协议</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>应用层（Application）</p>
</td>
<td rowspan="3">
<p>应用层</p>
</td>
<td valign="bottom">
<p>HTTP、TFTP,&nbsp;FTP, NFS, WAIS、SMTP</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>表示层（Presentation）</p>
</td>
<td valign="bottom">
<p>Telnet, Rlogin, SNMP, Gopher</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>会话层（Session）</p>
</td>
<td valign="bottom">
<p>SMTP, DNS</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>传输层（Transport）</p>
</td>
<td>
<p>传输层</p>
</td>
<td valign="bottom">
<p>TCP, UDP</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>网络层（Network）</p>
</td>
<td>
<p>网络层</p>
</td>
<td valign="bottom">
<p>IP, ICMP, ARP, RARP, AKP, UUCP</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>数据链路层（Data Link）</p>
</td>
<td rowspan="2">
<p>数据链路层</p>
</td>
<td valign="bottom">
<p>FDDI, Ethernet, Arpanet, PDN, SLIP, PPP</p>
</td>
</tr>
<tr>
<td valign="bottom">
<p>物理层（Physical）</p>
</td>
<td valign="bottom">
<p>IEEE 802.1A, IEEE 802.2到IEEE 802.11</p>
</td>
</tr>
</tbody>
</table>

- 在第一层部署中，最常用的软件负载均衡器为LVS(LinuxVirtual Server)和HAproxy。其中LVS采用基于IP负载均衡技术和基于内容请求分发技术。最常用的LVS负载均衡技术为DR负载均衡。
- 在第二层部署中，最常用的为MySQL-proxy(后端部署必须为MySQL数据库)，该代理服务器可以监测、分析或改变客户端的通信。最常用途为负载均衡，读写分离等。
- 在第三层部署中，最常用的存储设备都要做RAID[[2]](https://blog.csdn.net/wunianjiumeng/article/details/79642643)[[3]](https://blog.csdn.net/guangmingsky/article/details/78581651)，其中RAID0便为最基本的存储层的负载均衡。RAID0通过分带技术，将数据分割，然后并行的读写于各个磁盘上。这样实现底层存储一级的负载均衡。

 

### 1.2 LVS软件负载均衡器
LVS(Linux Virtual Server)是由章文嵩博士主导开发的一款开源软件，可以实现Linux平台下的基于网络层的负载均衡软件。典型的基本架构图如图6-2-1所示。


![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143529467-1138147090.gif)  
**图 6-2-1**

如图6-2-1所示，LVS集群采用基于**IP负载均衡技术**和**基于内容请求分发技术**。当客户端有请求时，首先将请求包传送到Load Balance，然后Load Balance从后面的Real Servers中按照一定的算法策略选取一台Real Server，比如Real Server1，然后把请求包发送给Real Server1进行处理。对所有用户而言，面向用户的服务器端IP地址，只有一台，称之为Virtual IP Address。

#### 1.2.1 LVS集群中实现的三种IP负载均衡技术
VS/NAT、 VS/TUN 和VS/DR技术是LVS集群中实现的三种IP负载均衡技术。

##### 1.2.1.1 VS/NAT技术
VS/NAT(Virtual Server via Network Address Translation)技术，主要通过网络地址转换，将一组服务器构成一个高性能的、高可用的虚拟服务器。NAT的工作原理是当内部网络中的主机要访问Internet或被Internet访问时，就需要采用网络地址转换NAT,将内部地址转化为Internet上可用的外部地址。NAT的工作原理是报文头(目标地址、源地址和端口等)被正确改写后，客户端相信他们连接到了一个IP地址，而不同的IP地址服务器组也认为他们与客户直接相连的。由此，可以用NAT方法将不同IP地址的并行网络服务变成一个IP地址上的虚拟服务。VS/NAT的体系结构如图6-2-1-1所示。

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143616358-732172719.gif)  
**图 6-2-1-1**

客户端访问服务器的请求包和响应包变化情况如下所示：

访问Web服务的报文可能有以下的源地址和目标地址：

| SOURCE | DEST |
| -- | -- |
| 202.100.1.2:3456 |202.103.106.5:80 |

调度器从调度列表中选出一台服务器，例如是172.16.0.3:8000。该报文会被改写为如下地址，并将它发送给选出的服务器。

| SOURCE | DEST |
| -- | -- |
| 202.100.1.2:3456 | 172.16.0.3:8000 |

从服务器返回到调度器的响应报文如下：

| SOURCE | DEST |
| -- | -- |
| 172.16.0.3:8000 | 202.100.1.2:3456 |


响应报文的源地址会被改写为虚拟服务的地址，再将报文发送给客户：

| SOURCE | DEST |
| -- | -- |
| 202.103.106.5:80 | 202.100.1.2:3456 |


这样，客户认为是从202.103.106.5:80服务得到正确的响应，而不会知道该请求是服务器172.16.0.2还是服务器172.16.0.3处理的。

##### 1.2.1.2 VS/TUN技术
VS/TUN 的工作原理：它的连接调度和管理与VS/NAT中的一样，只是它的报文转发方法不同。调度器根据各个服务器的负载情况，动态地选择一台服务器，将请求报文封装在另一个IP报文中，再将封装后的IP报文转发给选出的服务器；服务器收到报文后，先将报文解封获得原来目标地址为VIP的报文，服务器发现VIP地址被配置在本地的IP隧道设备上，所以就处理这个请求，然后根据路由表将响应报文直接返回给客户。如图6-2-1-2所示。


![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143712421-1612642711.gif)  
**图 6-2-1-2**

##### 1.2.1.3 VS/DR技术

在VS/DR中，调度器根据各个服务器的负载情况，动态地选择一台服务器，不修改也不封装IP报文，而是将数据帧的MAC地址改为选出服务器的MAC地址，再将修改后的数据帧在与服务器组的局域网上发送。因为数据帧的MAC地址是选出的服务器，所以服务器肯定可以收到这个数据帧，从中可以获得该IP报文。当服务器发现报文的目标地址VIP是在本地的网络设备上，服务器处理这个报文，然后根据路由表将响应报文直接返回给客户。如图6-2-1-3所示。

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143747436-1475305364.gif)
**图 6-2-1-3**

##### 1.2.1.4 LVS的调度算法

前面几节，介绍了LVS的三种基于IP的负载均衡技术，下面简单介绍一下调度算法。调度算法的目的是解决如何合理有效的从LVS后端的RealServers中，选择一个RealServer来对请求包进行处理。在整个LVS项目中，共给出八种调度算法，主要有：

- (1)轮询调度。主要指按顺序从RealServers中选择一台RealServers。
- (2) 加权轮叫调度。给Real Servers设置一定权值，进行调度。
- (3)最小连接调度。按照RealServers的连接情况进行调度。
- (4)加权最小连接。根据设置的权值和现有的连接数进行调度。
- (5)基于局部性的最小连接。主要用于增大Cache命中。
- (6)代复制的基于局部性的最小连接。
- (7)目标地址散列调度。
- (8)源地址散列调度。

在上述八种调度算法中，最常用的调度算法是轮询调度。

### 1.3 db proxy

在大型互联网站的数据库部署中，部署最多的数据库为MySQL。随着MySQL中Innodb存储引擎对事物的支持，MySQL在互联网公司部署中，应用量越来越多。典型应用MySQL的公司有Google、Baidu、Taobao等大型互联网公司。MySQL的优势在于其高扩展性和价格优势等。实际上，MySQL可以免费应用于企业级的部署中。

在MySQL复制方式部署中，有两种部署方式：同步复制和异步复制。同步复制采用NDB 存储引擎，异步复制需要使用mysql-proxy结合master-slave实现。

异步复制主要为了解决读写分离的问题。因为用户对网站的访问有读操作多，写操作少的特点。甚至像taobao.com这样的网站读写比例高达10:1，所以采用MySQL-Proxy结合主从异步复制实现读写分离是非常重要的增快访问速度的方法。这样如果有更高的用户访问需求，通过增加slave机器，不会对现有系统提供的服务产生影响而实现很好的、很灵活的业务扩展。

#### 1.3.1 mysql-proxy

mysql-proxy是一个MySQL的代理服务器，用户的请求先发向mysql-proxy，然后mysql-proxy对用户的数据包进行分析，从下一层的mysql 数据库中选择一台数据库，将用户的请求包交给mysql处理。

首先 MySQL Proxy 以服务器的身份接受客户端的请求，根据相应配置对这些请求进行分析处理，然后以客户端的身份转发给相应的后端数据库服务器，再接受服务器的信息，然后返回给客户端。所以MySQL Proxy需要同时实现客户端和服务器的协议。由于要对客户端发送过来的SQL语句进行分析，还需要包含一个SQL解析器。MySQL Proxy通过使用lua脚本，来实现复杂的连接控制和过滤，从而实现读写分离和负载平衡。所以部署MySQL-Proxy需要安装运行Lua语言的环境。典型的MySQL-Proxy应用为实现读写分离，如图6-3-1所示。

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143835046-1752907974.gif)  
**图 6-3-1**

#### 1.3.2 MySQL主从复制(Master-Slave Replication)

MySQL主从复制(Master-Slave Replication)是通过设置在Master MySQL上的binlog(使其处于打开状态)，Slave MySQL上通过一个I/O线程从Master MySQL上读取binlog，然后传输到Slave MySQL的中继日志中，然后Slave MySQL的SQL线程从中继日志中读取中继日志，然后应用到Slave MySQL的数据库中。这样实现了数据库的复制功能。原理如图6-3-2所示：


![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143907639-1935270682.gif)  
**图 6-3-2**

MySQL主从复制的作用如下：
- (1)    可以作为一种备份机制。  
- (2)    可以用来做读写分离。

#### 1.3.3 MySQL主从复制结合MySQL Proxy实现读写分离

通过使用MySQL-Proxy来作为代理服务器，配置MySQL Proxy，将所有的写操作分流到 Master MySQL 上，所有的读操作分流到 Slave MySQLs。
这样就实现了读写分离。如果有新的访问需求，只需添加slave MySQL机器来解决问题。所以这样的结构扩展能力非常好。如图6-3-3所示。

![](https://images2015.cnblogs.com/blog/533862/201607/533862-20160708143942296-936787237.gif)  
**图 6-3-3**

### 1.4 本文小结
本文主要论述了负载均衡在大型网站后台架构中的应用。主要分析了应用层的软件负载均衡器LVS的三种负载均衡算法，简单介绍了LVS的八种调度算法。详细分析了MySQL的主从复制和读写分离的实现机制。给出了高可用网站后台的部署中解决负载均衡的方案。


