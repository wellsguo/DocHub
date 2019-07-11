## 1. 前言

是不是想马上就有个聊天工具来聊一下天，没问题，这节课，我们就帮助您实现这个梦想。现在你要做的就是，看一个身边的美女，然后想他是我的，然后就努力吧。

哈哈，上面的话摘自“书中只有颜如玉，书中只有黄金屋”。

## 2. openfire 的安装

即时通讯程序的三大要素：服务器、客户端和协议，我们这一节课就来讲讲服务器的安装。前面的一章已经告诉了大家我们将使用openfire，那么怎么让openfire运行起来呢？

### （1）、windows 上安装 openfire

安装openfire有两个方法，我们这里只讲一种，另一种是通过源代码编译安装：

A、下载openfire的可执行文件，如果你在window上，请下载exe。如果你在mac上，就下载openfire_3_10_2.dmg。

访问http://www.igniterealtime.org/downloads/index.jsp，选择windows平台，下载openfire_3_10_2.exe，这个版本包含jre，也就是说，你如果没有java运行环境，那么这个包可以帮助你安装一下java。

openfire官网

B、下载完成后，点击openfire.exe文件。有一部电影叫《一路向西》，你也可以一路什么都不管，就直接安装openfire就可以了。

C、安装后，假设你安装在C:\Program Files\openfire这个目录下，那么在bin目录下有一个openfire.exe程序，直接打开，然后点击start，程序就启动了。

###（2）linux上安装openfire
首先要确保必须安装了java，怎么在linux上安装java，可以在网上找一找，我们这里提供了centos的安装java的脚本，如果已经安装了java，就不用安装了。Java 1.6以上的版本都可以，下面是安装1.6的举例：

```
#! /bin/sh

os_type=`uname`

if [ "$os_type" != "Linux" ];then
  echo "the script for linux only!"
  exit 1
fi

isMysqlInstalled=`yum list installed java* | grep java* | wc -l`
if [ "$isMysqlInstalled" = 1 ]; then
    echo "the java had been installed"
    exit 1
fi

echo 'the java 6  is installing '
yum -y install java-1.6.0-open*
echo 'the java 6 is installed  '

isMysqlInstalled=`yum list installed java* | grep java* | wc -l`
if [ "$isMysqlInstalled" = 1 ]; then
    echo "the java 6  is installed successily"
fi
```

安装java后，可以执行java –version，参看java版本，如下：

```
[root@localhost local]# java -version
java version "1.6.0_23"
Java(TM) SE Runtime Environment (build 1.6.0_23-b05)
Java HotSpot(TM) 64-Bit Server VM (build 19.0-b09, mixed mode)
```

安装成功java后，我们需要下载openfire，如下：

```
[root@localhost local]# 
wget http://download.igniterealtime.org/openfire/openfire_3_10_2.tar.gz
```

注意，我们下载的是linux版本。

然后解压openfire_3_10_2.tar.gz，如下：

```
[root@localhost local]# 
tar -zxvf openfire_3_10_2.tar.gz
```

然后进入目录：

```
[root@localhost local]# 
cd openfire/bin
./openfire start
```

这样openfire就启动成功了。你可以通过 http://127.0.0.1:9090 地址访问试一试。

## 3. 配置 openfire 服务器

安装并启动openfire后，就需要配置openfire服务器了。openfire提供了一个控制台，其实就是jsp网站，我们可以通过这个网站来配置openfire服务器。

在输入网址： http://127.0.0.1:9090 进行openfire的第一次配置之前，一定记得启动您的mysql服务，因为openfire需要用到数据库，我们的课程中使用mysql作为存储数据库。

具体的配置可以参看《openfire视频教程之openfire的配置》。

## 4. spark 客户端的安装

Openfire配置较为复杂，可以通过视频了解配置过程。当openfire配置成功后，就可以用Spark连接openfire了。

Spark是openfire开源组织提供的一个开源客户端，他是纯java编写的。如果想研究spark源码，那么我们举双手支持，因为这份源码对理解java网络编程，其实是很有帮助的。我们后期的课程，如果有精力，会给大家讲讲spark的实现。

大家可以在http://www.igniterealtime.org/downloads/index.jsp#spark下载spark的安装文件，它同时支持window平台和linux平台。目前spark的最新版本是spark 2.7.2 。

安装也很简单，一路向西，就安装成功了。

### （1） 安装后的界面的登录界面

![](http://myopenfire.com/attached/image/20151103/20151103211714_819.jpg)  
###### spark登录界面

### （2）设置服务器地址和连接端口

如果你的openfire在本地启动，那么ip地址为127.0.0.1 。

Openfire默认的端口号为5222

![](http://myopenfire.com/attached/image/20151103/20151103211749_939.jpg)  
###### spark服务器端口


如果您不想在本地安装openfire，那么可以使用我们的公用openfire服务器，主机地址是myopenfire.com，将主机地址改为myopenfire.com，你就可以连接服务器了。

如果你没有账号，你可以通过spark中的注册功能来注册一个账号。如下图，你找到了吗？

![](http://myopenfire.com/attached/image/20151103/20151103211831_24.jpg)  
###### spark注册界面

### （3）输入用户名和密码进行登录

注意，这里的用户名和密码应该现在openfire的控制台里面先新建一个用户。spark登录界面

Ok，如果你还没有明白，那么自己尝试一次吧，最好自己安装一下服务器，windows上还是linux上，都可以安装。

Jack老师语录：“编程像做爱一样，不尝试一次，您永远不知道其中的滋味。所以还是亲手做一次吧。”

如果你还是明白，可以看一下，我们精心制作的openfire入门视频。还没有明白，就问问老师吧。老师会免费为您进行大于1小时的答疑。

## 5. 在线openfire服务器

为了让大家节省搭建openfire服务器的过程，我们提供了一个在线的openfire服务器，大家可以在服务器地址输入框中输入 myopenfire.com ,即可通过spark连接上我们的openfire服务器了。如果没有账号，也可以通过spark进行注册哦。

如果你想和某个人聊天，你必须知道他们的账号才可以发起聊天，如果只是为了试验，你可以注册2个账号，然后分别登陆2个账号，进行测试。

## 6. 小结

本节我们讲解了怎么运行openfire，同时讲了windows和linux上怎么运行。一般我们开发在windows上，生产环境在linux上，所以现在你应该同时学会了这两种方法了。

另外，为了方便一些同学，我们也搭建了一个在线的openfire服务器，域名是myopenfire.com，大家也可以直接连接这台服务器，进行测试。

感谢大家，我们下节课再见。