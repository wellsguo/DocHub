## 1 目录 
- a、基础调优
- b、JVM 优化
- c、高级调优

## 2 基础调优 

### 2.1 tomcat 的各版本的优化参数有点不一样

可在启动 tomcat 之后访问 ***`http://<ip>:<port>/docs/config`*** 查看说明

### 2.2 配置管理员账户

编辑 `<tomcat>/bin/conf/tomcat-users.xml` 文件，在里面添加下面信息：

```xml
<role rolename="manager"/>
<role rolename="manager-gui"/>
<role rolename="admin"/>
<role rolename="admin-gui"/>
<user username="tomcat" password="tomcat" roles="admin-gui,admin,manager-gui,manager"/>
```
  
### 2.3 配置

先登录上面配置的管理员账号进入 `Server Status` 界面

![服务状态管理界面.png](https://upload-images.jianshu.io/upload_images/5131080-4978b0fb74d20776.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

可以看到 **`ajp-nio-8009`** 和 **`http-nio-8081`** ，由于我是用的最新的tomcat9做的演示，所以我们看到的 IO 类型直接就是非阻塞的同步 IO（nio），Tomcat6/7/8默认的都是阻塞式的同步IO（bio），因为 nio 效果要远大于 bio，所以我们要改为 nio，之所以之前默认为 bio，是为了兼容 `jdk1.4` 以下版本。

#### 2.3.1 修改 bio 为 nio

修改 ***`/conf/server.xml`*** 的 **Connector** 

```xml
<Connector 
  port="8080" 
  protocol="HTTP/1.1" 
  connectionTimeout="20000" 
  redirectPort="8443" 
/>
```

变为

```xml
<Connector 
  port="8080" 
  protocol="org.apache.coyote.http11.Http11NioProtocol" 
  connectionTimeout="20000" 
  redirectPort="8443" 
/>
<!-- 或者 protocol="org.apache.coyote.http11.Http11Nio2Protocol" -->
<!-- 或者 protocol="org.apache.coyote.http11.Http11AprProtocol" -->
```

注意：Tomcat 8 设置 nio2 更好（如果这个用不了，就用nio）， Tomcat 6、7 设置 nio 更好。 nio2 也就是非阻塞的异步IO，性能比nio更好一点，APR(ApachePortable Runtime/Apache可移植运行时)，是 Apache HTTP 服务器的支持库。你可以简单地理解为:Tomcat 将以 JNI 的形式调用 Apache HTTP 服务器的核心动态链接库来处理文件读取或网络传输操作，从而大大地提高 Tomcat 对静态文件的处理性能。

#### 2.3.2 enableLookups

禁用DNS查询

#### 2.3.3 acceptorThreadCount

用于接收连接的线程的数量，默认值是1。一般这个指需要改动的时候是因为该服务器是一个多核CPU，如果是多核 CPU 一般配置为 2

#### 2.3.4 acceptCount

指定当所有可以使用的处理请求的线程数都被使用时，可以放到处理队列中的请求数，超过这个数的请求将不予处理，默认设置 100

```xml
<Connector 
  port="8080" 
  protocol="org.apache.coyote.http11.Http11NioProtocol" 
  enableLookups="false"
  acceptCount="100"
  acceptorThreadCount="2" 
  connectionTimeout="20000" 
  redirectPort="8443" 
/>
```
#### 2.3.5 Tomcat 缓存优化

- compression 打开压缩功能
- compressionMinSize 启用压缩的输出内容大小，这里面默认为2KB
- compressableMimeType 压缩类型
- connectionTimeout 定义建立客户连接超时的时间.如果为-1,表示不限制建立客户连接的时间

```xml
compression="on"
compressionMinSize="2048"
compressableMimeType="text/html,text/xml,text/javascript,text/css,text/plain"
connectionTimeout="20000"
```
#### 2.3.6 配置最大线程数量（maxThreads，默认200）

由该连接器创建的处理请求线程的最大数目，也就是可以处理的同时请求的最大数目。如果未配置默认值为200。如果一个执行器与此连接器关联，则忽略此属性，因为该属性将被忽略，所以该连接器将使用执行器而不是一个内部线程池来执行任务。**maxThreads是一个重要的配置属性**，maxThreads 配置的合理直接影响了 Tomcat 的相关性能，所以这里我们重点讨论下。

maxThreads 并不是配置的越大越好，事实上你即使配置成 999999 也是没有用的，因为这个最大值是受操作系统及相关硬件所制约的，并且最大值并不一定是最优值，所以我们追寻的应该是最优值而不是最大值。

#### 2.3.7 禁用 AJP（如果你服务器没有使用 Apache）

AJP 是为了配合 Apache 处理静态文件服务器，进行服务器间文件传输的协议，用不上的话就注销它，后面我会讲述 Tomcat 配合 Nginx 处理静态文件（动静分离和负载均衡）
把下面这一行注释掉，默认 Tomcat 是开启的。

```xml
<!-- <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" /> -->
```
禁用之后我们可以看一下服务状态页面：

![图三.png](https://upload-images.jianshu.io/upload_images/5131080-8ed1455665a8f150.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

发现AJP协议已经没有了，nio转换为nio2了

### 2.3.8 整合

```xml
<Connector 
  protocol="HTTP/1.1"
  maxHttpHeaderSize="8192"
  maxThreads="1000" //最大线程数，默认200
  minSpareThreads="100" //Tomcat初始化时创建的socket线程数，线程的最小运行数目，这些始终保持运行，如果未指定，默认值为10
  maxSpareThreads="1000"//Tomcat连接器的最大空闲socket线程数
  minProcessors="100"//服务器创建时的最小处理线程数
  maxProcessors="1000"//服务器同时最大处理线程数
  enableLookups="false"//关闭DNS反向查询，若设为true,则支持域名解析，可把ip地址解析为主机名
  compression="on"//打开压缩功能
  compressionMinSize="2048"
  compressableMimeType="text/html,text/xml,text/javascript,text/css,text/plain"
  connectionTimeout="20000"//代表连接超时时间，单位为毫秒，默认值为60000。通常情况下设置为30000
  URIEncoding="utf-8"//URL统一编码
  acceptCount="1000"//监听端口队列最大数，满了之后客户请求会被拒绝（不能小于maxSpareThreads），如果未指定，默认值为100
  redirectPort="8443"//在需要基于安全通道的场合，把客户请求转发到基于SSL的redirectPort端口
  disableUploadTimeout="true"/>//这个标志允许servlet[Container](http://lib.csdn.net/base/4)在一个servlet执行的时候，使用一个不同的，更长的连接超时。最终的结果是给servlet更长的时间以便完成其执行，或者在数据上载的时候更长的超时时间。如果没有指定，默认为false
```

```xml
<Connector 
  executor=" tomcatThreadPool" //开启线程池 
  port="8080" 
  protocol="org.apache.coyote.http11.Http11AprProtocol" //开启Apr协议，需要安装Apr支持 
  maxHttpHeaderSize="8192" 
  maxThreads="1000" 
  processorCache="1000" 
  acceptCount="1000" 
  minSpareThreads="100" 
  acceptorThreadCount="8" 
  URIEncoding="UTF-8" 
  enableLookups="false" //关闭反向查询 
  redirectPort="8443" 
  connectionTimeout="120000" 
  keepAliveTimeout="120000" 
  maxKeepAliveRequests="65535" 
  disableUploadTimeout="true" 
  compression="on" //开启静态文件压缩 
  compressionMinSize="4096" //开启静态文件压缩 
  noCompressionUserAgents="gozilla, traviata" //开启静态文件压缩 
  compressableMimeType="text/html,text/xml,text/javascript,text/css,text/plain,application/json,application/x-javascript " //开启静态文件压缩 
/>
```

#### 2.3.9 Web 应用管理

用管理员账号进入web应用管理界面，在这个里面可以对tomcat中部署的应用的启动状态做修改，把不需要的应用可以暂时关闭，同时也可以对session缓存时间进行配置

## 3 JVM 优化

修改 ***`/bin/catalina.bat`*** 文件，如：

![jvm优化参数.png](https://upload-images.jianshu.io/upload_images/5131080-a1ca929fb4a94520.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

- 如果服务器只运行一个 Tomcat

  - 机子内存如果是 8G，一般 PermSize 配置是主要保证系统能稳定起来就行(如果是Linux系统，等号后的值要用引号引起来)  
```bat
set JAVA_OPTS=-Dfile.encoding=UTF-8 -server -Xms6144m -Xmx6144m -XX:NewSize=1024m -XX:MaxNewSize=2048m -XX:PermSize=512m -XX:MaxPermSize=512m -XX:MaxTenuringThreshold=10 -XX:NewRatio=2 -XX:+DisableExplicitGC
```

  - 机子内存如果是 16G，一般 PermSize 配置是主要保证系统能稳定起来就行：  
```bat
set JAVA_OPTS=-Dfile.encoding=UTF-8 -server -Xms13312m -Xmx13312m -XX:NewSize=3072m -XX:MaxNewSize=4096m -XX:PermSize=512m -XX:MaxPermSize=512m -XX:MaxTenuringThreshold=10 -XX:NewRatio=2 -XX:+DisableExplicitGC
```

  - 机子内存如果是 32G，一般 PermSize 配置是主要保证系统能稳定起来就行：  
```bat
set JAVA_OPTS=-Dfile.encoding=UTF-8 -server -Xms29696m -Xmx29696m -XX:NewSize=6144m -XX:MaxNewSize=9216m -XX:PermSize=1024m -XX:MaxPermSize=1024m -XX:MaxTenuringThreshold=10 -XX:NewRatio=2 -XX:+DisableExplicitGC
```

- 如果是开发机  
```bat
set JAVA_OPTS=-Xms550m -Xmx1250m -XX:PermSize=550m -XX:MaxPermSize=1250m
```

参数说明：
- -Dfile.encoding：默认文件编码
- -server：表示这是应用于服务器的配置，JVM 内部会有特殊处理的
- -Xmx1024m：设置JVM最大可用内存为1024MB
- -Xms1024m：设置JVM最小内存为1024m。此值可以设置与-Xmx相同，以避免每次垃圾回收完成后JVM重新分配内存。
- -XX:NewSize：设置年轻代大小
- -XX:MaxNewSize：设置最大的年轻代大小
- -XX:PermSize：设置永久代大小
- -XX:MaxPermSize：设置最大永久代大小
- -XX:NewRatio=4：设置年轻代（包括 Eden 和两个 Survivor 区）与终身代的比值（除去永久代）。设置为 4，则年轻代与终身代所占比值为 1：4，年轻代占整个堆栈的 1/5
- -XX:MaxTenuringThreshold=10：设置垃圾最大年龄，默认为：15。如果设置为 0 的话，则年轻代对象不经过 Survivor 区，直接进入年老代。对于年老代比较多的应用，可以提高效率。如果将此值设置为一个较大值，则年轻代对象会在 Survivor 区进行多次复制，这样可以增加对象再年轻代的存活时间，增加在年轻代即被回收的概论。
- -XX:+DisableExplicitGC：这个将会忽略手动调用 GC 的代码使得 System.gc() 的调用就会变成一个空调用，完全不会触发任何 GC

## 4 高级调优
以上内容足以应付绝大多数情景，熟悉以上内容，你也就步入了服务器优化的大门了，且水平会远强于其他菜鸟，但要进一步提升，则需继续学习以下内容

- 4.1、Tomcat 配合 Nginx做负载均衡
- 4.2、Tomcat 配合 Nginx做动静分离
- 4.3、Tomcat 配合 Nginx 和 Redis 做 tomcat 集群和 session 共享
- 4.4、Jmeter 做压力测试

作者：笑才  
链接：https://www.jianshu.com/p/4024bddc0550  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。