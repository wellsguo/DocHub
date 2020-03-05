# HTTP的POST提交的四种常见消息主体格式

[HTTP/1.1 协议](http://www.ietf.org/rfc/rfc2616.txt)规定的 HTTP 请求方法有 OPTIONS、GET、HEAD、POST、PUT、DELETE、TRACE、CONNECT 这几种。其中 POST 一般用来向服务端提交数据，本文主要讨论 POST 提交数据的几种方式。

我们知道，HTTP 协议是以 ASCII 码传输，建立在 TCP/IP 协议之上的应用层规范。规范把 HTTP 请求分为三个部分：状态行、请求头、消息主体。类似于下面这样：



```
<method> <request-URL> <version>
<headers>
<entity-body>
```



协议规定 POST 提交的数据必须放在消息主体（entity-body）中，但协议并没有规定数据必须使用什么编码方式。实际上，开发者完全可以自己决定消息主体的格式，只要最后发送的 HTTP 请求满足上面的格式就可以。

但是，数据发送出去，还要服务端解析成功才有意义。一般服务端语言如 php、python 等，以及它们的 framework，都内置了自动解析常见数据格式的功能。*<u>服务端通常是根据请求头（headers）中的` Content-Type` 字段来获知请求中的消息主体是用何种方式编码，再对主体进行解析</u>*。所以说到 POST 提交数据方案，包含了 Content-Type 和消息主体编码方式两部分。下面就正式开始介绍它们。

### application/x-www-form-urlencoded

这应该是最常见的 POST 提交数据的方式了。浏览器的原生 form 表单，如果不设置 enctype 属性，那么最终就会以 `application/x-www-form-urlencoded` 方式提交数据。请求类似于下面这样（无关的请求头在本文中都省略掉了）：

```
POST http://www.example.com HTTP /1.1
Content-Type: application/x-www-form-urlencoded;charset=utf8

title=test&sub%5B%5D=1&sub%5B%5D=2&sub%5B%5D=3
```

- 首先，`Content-Type` 被指定为 `application/x-www-form-urlencoded`；
- 其次，提交的数据按照 `key1=val1&key2=val2` 的方式进行编码，key 和 val 都进行了 `URL 转码`。大部分服务端语言都对这种方式有很好的支持。例如 PHP 中，`$_POST['title']` 可以获取到 title 的值，`$_POST['sub']` 可以得到 sub 数组。

很多时候，我们用 Ajax 提交数据时，也是使用这种方式。例如 [JQuery](http://jquery.com/) 和 [QWrap](http://www.qwrap.com/) 的 Ajax，Content-Type 默认值都是「application/x-www-form-urlencoded;charset=utf-8」。

### multipart/form-data

这又是一个常见的 POST 数据提交的方式。我们使用表单上传文件时，必须让 form 的 enctyped 等于这个值。直接来看一个请求示例：

```
POST http://www.example.com HTTP/1.1
Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryrGKCBY7qhFd3TrwA
------WebKitFormBoundaryrGKCBY7qhFd3TrwA 
Content-Disposition: form-data; name="text"
title
------WebKitFormBoundaryrGKCBY7qhFd3TrwA
Content-Disposition: form-data; name="file"; filename="chrome.png"
Content-Type: image/png
PNG ... content of chrome.png ...
------WebKitFormBoundaryrGKCBY7qhFd3TrwA--
```

这个例子稍微复杂点。首先生成了一个 `boundary` 用于分割不同的字段，为了避免与正文内容重复，boundary 很长很复杂。然后 `Content-Type` 里指明了数据是以 `mutipart/form-data` 来编码，本次请求的 `boundary` 是什么内容。消息主体里按照字段个数又分为多个结构类似的部分，每部分都是以 `–boundary` 开始，紧接着内容描述信息，然后是回车，最后是字段具体内容（文本或二进制）。如果传输的是文件，还要包含文件名和文件类型信息。消息主体最后以 `–boundary–` 标示结束。关于 `mutipart/form-data` 的详细定义，请前往 [rfc1867](http://www.ietf.org/rfc/rfc1867.txt) 查看。

这种方式一般用来上传文件，各大服务端语言对它也有着良好的支持。

上面提到的这两种 POST 数据的方式，都是浏览器原生支持的，而且现阶段原生 form 表单也[只支持这两种方式](http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4)。但是随着越来越多的 Web 站点，尤其是 WebApp，全部使用 Ajax 进行数据交互之后，我们完全可以定义新的数据提交方式，给开发带来更多便利。

### application/json

`application/json` 这个`Content-Type` 作为响应头大家肯定不陌生。实际上，现在越来越多的人把它作为请求头，用来告诉服务端消息主体是序列化后的 JSON 字符串。由于 JSON 规范的流行，除了低版本 IE 之外的各大浏览器都原生支持 JSON.stringify，服务端语言也都有处理 JSON 的函数，使用 JSON 不会遇上什么麻烦。

JSON 格式支持比键值对复杂得多的结构化数据，这一点也很有用。记得我几年前做一个项目时，需要提交的数据层次非常深，我就是把数据 JSON 序列化之后来提交的。不过当时我是把 JSON 字符串作为 val，仍然放在键值对里，以 x-www-form-urlencoded 方式提交。

Google 的 [AngularJS](http://angularjs.org/) 中的 Ajax 功能，默认就是提交 JSON 字符串。例如下面这段代码：

```javascript
var data = {'title':'test', 'sub': [1,2,3]};
$http.post(url, data).success(function(result) {
   ...
});
```

最终发送的请求是：

```
POST http://www.example.com HTTP/1.1
Content-Type: application/json;charset=utf-8

{"title":"test","sub":[1,2,3]}
```

这种方案，可以方便的提交复杂的结构化数据，特别适合 RESTful 的接口。各大抓包工具如 Chrome 自带的开发者工具、Firebug、Fiddler，都会以树形结构展示 JSON 数据，非常友好。但也有些服务端语言还没有支持这种方式，例如 php 就无法通过 $_POST 对象从上面的请求中获得内容。这时候，需要自己动手处理下：在请求头中 Content-Type 为 application/json 时，从 php://input 里获得原始输入流，再 json_decode 成对象。一些 php 框架已经开始这么做了。

当然 AngularJS 也可以配置为使用 x-www-form-urlencoded 方式提交数据。如有需要，可以参考[这篇文章](http://victorblog.com/2012/12/20/make-angularjs-http-service-behave-like-jquery-ajax/)。

### text/xml

我的博客之前[提到过 XML-RPC](http://www.imququ.com/post/64.html)（XML Remote Procedure Call）。它是一种使用 HTTP 作为传输协议，XML 作为编码方式的远程调用规范。典型的 XML-RPC 请求是这样的：

```
POST http://www.example.com HTTP/1.1
Content-Type: text/xml
<?xml version="1.0"?>
<methodCall>
    <methodName>examples.getStateName</methodName>
    <params>
        <param>
            <value><i4>41</i4></value>
        </param>
    </params>
</methodCall>
```

XML-RPC 协议简单、功能够用，各种语言的实现都有。它的使用也很广泛，如 WordPress 的 [XML-RPC Api](http://codex.wordpress.org/XML-RPC_WordPress_API)，搜索引擎的 [ping 服务](http://www.baidu.com/search/blogsearch_help.html#n7)等等。JavaScript 中，也有[现成的库](http://plugins.jquery.com/xmlrpc/)支持以这种方式进行数据交互，能很好的支持已有的 XML-RPC 服务。不过，我个人觉得 XML 结构还是过于臃肿，一般场景用 JSON 会更灵活方便。



-----

# HTTP_POST请求的数据格式

在HTTP的请求头中，可以使用Content-type来指定不同格式的请求信息。

### Content-type的类型

**常见的媒体格式类型：**

-   text/html ： HTML格式
-   text/plain ：纯文本格式   
-   text/xml ： XML格式
-   image/gif ：gif图片格式  
-   image/jpeg ：jpg图片格式 
-   image/png：png图片格式

**以applicaton开头的没提类型：**

- **application/json**  ： JSON数据格式
- application/xhtml+xml ：XHTML格式
- application/xml   ： XML数据格式
- application/atom+xml ：Atom XML聚合格式  
- application/pdf    ：pdf格式 
- application/javascript ：js格式
- application/msword ： Word文档格式
- application/octet-stream ： 二进制流数据（如常见的文件下载）
- **application/x-www-form-urlencoded** ：form表单默认的数据格式类型，form表单数据被编码为key/value格式发送到服务器。

**另外一种常见的媒体格式是上传文件之时使用的：**

- **multipart/form-data** ： 需要在表单中进行文件上传时，就需要使用该格式。

除了原生的content-type，开发人员也可以完全自定义数据提交格式！

**最常用的三种：**

1. application/x-www-form-urlencoded，form表单默认的数据格式，提交的数据按照 key1=val1&key2=val2 的方式进行编码，key 和 val 都进行了 URL 转码。大部分服务端语言都对这种方式有很好的支持。比如下面的http请求格式：

   ```
   # Request Headers
   POST /adduser HTTP/1.1
   Host: localhost:8030
   Connection: keep-alive
   Content-Length: 16
   Pragma: no-cache
   Cache-Control: no-cache
   Origin: chrome-extension://fdmmgilgnpjigdojojpjoooidkmcomcm
   User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
   Content-Type: application/x-www-form-urlencoded
   Accept: */*
   Accept-Encoding: gzip, deflate, br
   Accept-Language: zh-CN,zh;q=0.9
   
   # Form Data
   name=name&age=11
   ```

2. application/json，现在越来越多的人把它作为请求头，用来告诉服务端消息主体是序列化后的 JSON 字符串。服务端语言也有很多函数去解析JSON，使用JSON可以支持更加复杂的结构化数据。比如下面的http请求格式：

   ```
   # Request Headers
   POST /adduser HTTP/1.1
   Host: localhost:8030
   Connection: keep-alive
   Content-Length: 24
   Pragma: no-cache
   Cache-Control: no-cache
   Origin: chrome-extension://fdmmgilgnpjigdojojpjoooidkmcomcm
   User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
   Content-Type: application/json
   Accept: */*
   Accept-Encoding: gzip, deflate, br
   Accept-Language: zh-CN,zh;q=0.9
   
   # Request Payload
   {"name":"121","age":121}
   ```

3. multipart/form-data，对用于在表单中上传文件时，也可以上传普通数据，只需要让from的ectyle等于multipart/form-data就可以了。比如下面的http请求格式：

   ```
   # Request Header
   POST /adduser HTTP/1.1
   Host: localhost:8030
   Connection: keep-alive
   Content-Length: 232
   Pragma: no-cache
   Cache-Control: no-cache
   Origin: chrome-extension://fdmmgilgnpjigdojojpjoooidkmcomcm
   User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
   Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBRi81vNtMyBL97Rb
   Accept: */*
   Accept-Encoding: gzip, deflate, br
   Accept-Language: zh-CN,zh;q=0.9
   
   # Request Payload
   ------WebKitFormBoundaryBRi81vNtMyBL97Rb
   Content-Disposition: form-data; name="name"
   
   name1
   ------WebKitFormBoundaryBRi81vNtMyBL97Rb
   Content-Disposition: form-data; name="age"
   
   12
   ------WebKitFormBoundaryBRi81vNtMyBL97Rb--
   ```

   

   这种格式的数据会有一个边界线boundary（这里就是`------WebKitFormBoundaryBRi81vNtMyBL97Rb`）用于分割不同的字段，为了避免与正文内容重复，boundary很长很复杂。消息主体以boundary开始，紧接着就是内容描述信息，然后是回车，最后是字段具体的内容（文本或二进制）。如果传输的是文件，还要包含文件名和文件类型信息。消息主体以boundary结束。

### Request Headers部分各个字段的功能

通过上面的例子，我们可以看到在Request Headers里面以后很多字段，比如Content-type，Host这些，那么这些字段又有什么意思呢，下面通过表格来介绍一下：

| Header              | 解释                                                         | 示例                                                         |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Accept              | 指定客户端能够接收的内容类型                                 | Accept: text/plain, text/html,*/*                            |
| Accept-Charset      | 浏览器可以接受的字符编码集。                                 | Accept-Charset: iso-8859-5                                   |
| Accept-Encoding     | 指定浏览器可以支持的web服务器返回内容压缩编码类型。          | Accept-Encoding: compress, gzip                              |
| Accept-Language     | 浏览器可接受的语言                                           | Accept-Language: en,zh                                       |
| Accept-Ranges       | 可以请求网页实体的一个或者多个子范围字段                     | Accept-Ranges: bytes                                         |
| Authorization       | HTTP授权的授权证书                                           | Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==            |
| Cache-Control       | 指定请求和响应遵循的缓存机制                                 | Cache-Control: no-cache                                      |
| Connection          | 表示是否需要持久连接。（HTTP 1.1默认进行持久连接）           | Connection: keep-alive                                       |
| Cookie              | HTTP请求发送时，会把保存在该请求域名下的所有cookie值一起发送给web服务器。 | Cookie: $Version=1; Skin=new;                                |
| Content-Length      | 请求的内容长度                                               | Content-Length: 348                                          |
| Content-Type        | 请求的与实体对应的MIME信息                                   | Content-Type: application/x-www-form-urlencoded              |
| Date                | 请求发送的日期和时间                                         | Date: Tue, 15 Nov 2010 08:12:31 GMT                          |
| Expect              | 请求的特定的服务器行为                                       | Expect: 100-continue                                         |
| From                | 发出请求的用户的Email                                        | From: user@email.com                                         |
| Host                | 指定请求的服务器的域名和端口号                               | Host: www.zcmhi.com                                          |
| If-Match            | 只有请求内容与实体相匹配才有效                               | If-Match: “737060cd8c284d8af7ad3082f209582d”                 |
| If-Modified-Since   | 如果请求的部分在指定时间之后被修改则请求成功，未被修改则返回304代码 | If-Modified-Since: Sat, 29 Oct 2010 19:43:31 GMT             |
| If-None-Match       | 如果内容未改变返回304代码，参数为服务器先前发送的Etag，与服务器回应的Etag比较判断是否改变 | If-None-Match: “737060cd8c284d8af7ad3082f209582d”            |
| If-Range            | 如果实体未改变，服务器发送客户端丢失的部分，否则发送整个实体。参数也为Etag | If-Range: “737060cd8c284d8af7ad3082f209582d”                 |
| If-Unmodified-Since | 只在实体在指定时间之后未被修改才请求成功                     | If-Unmodified-Since: Sat, 29 Oct 2010 19:43:31 GMT           |
| Max-Forwards        | 限制信息通过代理和网关传送的时间                             | Max-Forwards: 10                                             |
| Pragma              | 用来包含实现特定的指令                                       | Pragma: no-cache                                             |
| Proxy-Authorization | 连接到代理的授权证书                                         | Proxy-Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==      |
| Range               | 只请求实体的一部分，指定范围                                 | Range: bytes=500-999                                         |
| Referer             | 先前网页的地址，当前请求网页紧随其后,即来路                  | Referer: [http://www.zcmhi.com/archives...](http://www.zcmhi.com/archives/71.html) |
| TE                  | 客户端愿意接受的传输编码，并通知服务器接受接受尾加头信息     | TE: trailers,deflate;q=0.5                                   |
| Upgrade             | 向服务器指定某种传输协议以便服务器进行转换（如果支持）       | Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11               |
| User-Agent          | User-Agent的内容包含发出请求的用户信息                       | User-Agent: Mozilla/5.0 (Linux; X11)                         |
| Via                 | 通知中间网关或代理服务器地址，通信协议                       | Via: 1.0 fred, 1.1 nowhere.com (Apache/1.1)                  |
| Warning             | 关于消息实体的警告信息                                       | Warn: 199 Miscellaneous warning                              |

**拓展知识：**

User-Agent里面包含了浏览器客户端的信息，比如：Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36

通过这个信息可以看到使用的是Chrome浏览器，内核是Apple的WebKit。

其实前世界上主要有来自四个不同机构的四种的Web浏览器内核。每一家机构都推出了至少一种使用自己的内核的浏览器产品。

这四家机构分别是Microsoft、Mozilla、Apple和Opera SAS，提供的内核则分别叫做Trident、Gecko、WebKit和Presto，推出的主打浏览器则分别叫做Internet Explorer、Firefox、Safari和Opera。我们最常使用的Chrome浏览器就是用的苹果公司的Webkit。国内的一些浏览器也是基于webkit内核的，其所谓的双核中的极速模式就是webkit内核，兼容模式就是ie的trident内核。

### Response Headers部分各个字段的功能

Request Headers是请求头，Response Headers是响应头，同样，它也包含了一些字段信息：

| Header             | 解释                                                         | 示例                                                         |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Accept-Ranges      | 表明服务器是否支持指定范围请求及哪种类型的分段请求           | Accept-Ranges: bytes                                         |
| Age                | 从原始服务器到代理缓存形成的估算时间（以秒计，非负）         | Age: 12                                                      |
| Allow              | 对某网络资源的有效的请求行为，不允许则返回405                | Allow: GET, HEAD                                             |
| Cache-Control      | 告诉所有的缓存机制是否可以缓存及哪种类型                     | Cache-Control: no-cache                                      |
| Content-Encoding   | web服务器支持的返回内容压缩编码类型。                        | Content-Encoding: gzip                                       |
| Content-Language   | 响应体的语言                                                 | Content-Language: en,zh                                      |
| Content-Length     | 响应体的长度                                                 | Content-Length: 348                                          |
| Content-Location   | 请求资源可替代的备用的另一地址                               | Content-Location: /index.htm                                 |
| Content-MD5        | 返回资源的MD5校验值                                          | Content-MD5: Q2hlY2sgSW50ZWdyaXR5IQ==                        |
| Content-Range      | 在整个返回体中本部分的字节位置                               | Content-Range: bytes 21010-47021/47022                       |
| Content-Type       | 返回内容的MIME类型                                           | Content-Type: text/html; charset=utf-8                       |
| Date               | 原始服务器消息发出的时间                                     | Date: Tue, 15 Nov 2010 08:12:31 GMT                          |
| ETag               | 请求变量的实体标签的当前值                                   | ETag: “737060cd8c284d8af7ad3082f209582d”                     |
| Expires            | 响应过期的日期和时间                                         | Expires: Thu, 01 Dec 2010 16:00:00 GMT                       |
| Last-Modified      | 请求资源的最后修改时间                                       | Last-Modified: Tue, 15 Nov 2010 12:45:26 GMT                 |
| Location           | 用来重定向接收方到非请求URL的位置来完成请求或标识新的资源    | Location: [http://www.zcmhi.com/archives...](http://www.zcmhi.com/archives/94.html) |
| Pragma             | 包括实现特定的指令，它可应用到响应链上的任何接收方           | Pragma: no-cache                                             |
| Proxy-Authenticate | 它指出认证方案和可应用到代理的该URL上的参数                  | Proxy-Authenticate: Basic                                    |
| refresh            | 应用于重定向或一个新的资源被创造，在5秒之后重定向（由网景提出，被大部分浏览器支持） | Refresh: 5; url=[http://www.zcmhi.com/archives...](http://www.zcmhi.com/archives/94.html) |
| Retry-After        | 如果实体暂时不可取，通知客户端在指定时间之后再次尝试         | Retry-After: 120                                             |
| Server             | web服务器软件名称                                            | Server: Apache/1.3.27 (Unix) (Red-Hat/Linux)                 |
| Set-Cookie         | 设置Http Cookie                                              | Set-Cookie: UserID=JohnDoe; Max-Age=3600; Version=1          |
| Trailer            | 指出头域在分块传输编码的尾部存在                             | Trailer: Max-Forwards                                        |
| Transfer-Encoding  | 文件传输编码                                                 | Transfer-Encoding:chunked                                    |
| Vary               | 告诉下游代理是使用缓存响应还是从原始服务器请求               | Vary: *                                                      |
| Via                | 告知代理客户端响应是通过哪里发送的                           | Via: 1.0 fred, 1.1 nowhere.com (Apache/1.1)                  |
| Warning            | 警告实体可能存在的问题                                       | Warning: 199 Miscellaneous warning                           |
| WWW-Authenticate   | 表明客户端请求实体应该使用的授权方案                         | WWW-Authenticate: Basic                                      |