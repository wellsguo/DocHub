## 常见的安全问题

1. 数据库安全
2. 注入安全
3. 跨域安全
4. 用户登录弱口令和密码明文
5. 、、





## WEB 开发常见的几大安全问题

1. 涉及到私密信息使用 POST 请求，因为信息放在请求体中，不会像 GET 请求暴露在 URL 上。

2. HTTPS。传输层保护不足，在身份验证过程中没有使用 SSL/TLS，因此暴露传输数据和 SESSIONID。HTTP 协议传输的数据都是未加密的，也就是明文的，因此使用 HTTP 协议传输隐私信息非常不安全。 HTTPS 协议是由 SSL + HTTP 协议构建的可进行加密传输、身份认证的网络协议，比 HTTP 协议更安全。

3. 防 SQL 注入。把参数放在元组里，避免拼接 SQL 语句。

4. 用户密码须加密存储，设计一个完善能防范各种类型攻击的用户认证系统。

5. 防止 CSRF (Cross Site Request Forgery)，即跨站请求伪造，是一种常见的 Web 攻击，它利用用户一登录的身份，在用户毫不知情的情况下，以用户的名义完成非法操作。请求时附带验证信息，比如验证码或者 token.

6. 预防 XSS（Cross-Site Scripting），跨站脚本攻击，因为缩写和 CSS 重复，所以只能叫 XSS。跨站脚本攻击是指通过存在安全漏洞的 Web 网站注册永不的浏览器内运行非法的 HTML 标签或 javascript 进行的一种攻击。- HttpOnly Cookie. 这是预防 XSS 攻击窃取用户 Cookie 最有效的防御手段。Web 应用程序在设置 Cookie 时，将其属性设置为 HttpOnly，就可以避免改网页的 cookie 被客户端恶意 javascript 窃取，保护用户的 Cookie 信息。

7. 点击劫持，点击劫持是一种视觉欺骗的攻击手段。攻击者将需要攻击的网站通过 iframe 嵌套的方式嵌入自己的网页中，并将 firem 设置为透明，在页面中透出一个按钮诱导用户点击。

8. URL 跳转漏洞，借助未验证的 URL 跳转，将应用程序引导到不安全的第三方区域，从而导致的安全漏洞。

9. OS 命令注入攻击，OS 命令注入攻击和 SQL 注入差不多，只不过 SQL 注入针对的是数据库，而 OS 命令注入是针对操作系统的。OS 命令注入攻击指通过 Web 应用，执行非法的操作系统命令达到攻击的目的。只要在能调用 Shell 函数的地方就有存在被攻击的风险。倘若调用 Shell 时存在疏漏，就可以执行插入的非法命令。

10. DOS 攻击，Denial of Service，拒绝服务，即无法及时接收并处理外界合法请求。

11. Session 劫持，基于 Session 的攻击方法有很多种。大部分的手段都是首先通过捕获合法的用户的 Session，然后冒充该用户来访问系统。也就是说，攻击者至少必须要获取到一个有效的 session 标识符，用于接下来的身份验证。

12. 文件上传漏洞，允许上传任意文件会让攻击者注入危险内容或恶意代码，并在服务器上运行。

    解决方法：

    - 检查服务器是否判断了上传文件类型及后缀
    - 对上传文件的目录设置不可执行

13. 没有限制 URL 访问，系统已经对 URL 的访问做了限制，但这种限制却实际并没有生效。攻击中很容易伪造请求直接访问未被授权的页面。

14. 越权访问，用户对系统某个模块或功能内有权限，通过拼接 URL 或 Cookie 欺骗来访问该模块或功能。如 java 中通过 cookie.setHttpOnly(true)

15. 泄漏配置信息，服务器返回的提示或错误信息中出现服务器版本信息泄漏、程序出错泄漏物理路劲、程序出错返回 SQL 语句、过于详细的用户验证返回信息。

16. 不安全的加密存储，常见的问题是不安全的密钥生成和存储。

17. 重复提交数据，程序员在代码中没有对重复提交请求做限制，导致数据重复。

