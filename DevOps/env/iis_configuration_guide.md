
[C# 创建、部署和调用WebService的简单示例](https://www.cnblogs.com/Brambling/p/6815565.html)



```
“/”应用程序中的服务器错误。
访问被拒绝。
说明: 访问服务此请求所需的资源时出错。您可能没有查看所请求的资源的权限。 

错误消息 401.3: 您无权使用您提供的凭据查看此目录或页(由于访问控制列表而导致访问被拒绝)。请让 Web 服务器的管理员授予您访问“F:\web\wwwroot\landu.cn\index.aspx”的权限。

版本信息: Microsoft .NET Framework 版本:2.0.50727.5466; ASP.NET 版本:2.0.50727.5456

```
> 出现这个错误是因为IIS设置中身份验证出现问题。[解决方法如下](http://kevintseng.blog.hexun.com/84848538_d.html)

身份验证：
启用“ASP.NET”模拟（已通过身份验证的标识）

```
HTTP 错误 500.24 - Internal Server Error
检测到在集成的托管管道模式下不适用的 ASP.NET 设置。
```

[解决](https://blog.csdn.net/wrs120/article/details/71081149)  