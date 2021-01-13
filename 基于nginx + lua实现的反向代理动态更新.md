## [基于nginx + lua实现的反向代理动态更新](https://www.cnblogs.com/shihuc/p/8044753.html) 

基于nginx和lua脚本，也就是在openresty的环境下，实现动态的反向代理逻辑，有一个开关控制。开关控制反向代理工作在nginx原生的upstream的模式，还是工作在lua控制的动态代理模式。 动态代理的服务器，通过http请求实现灵活的操作，向`lua_shared_dict`定义的全局变量里面写入或者删除动态代理的服务器信息。

环境信息如下：

```
1 [root@bogon sbin]# ./nginx -V
2 nginx version: openresty/1.11.2.2
3 built by gcc 4.8.5 20150623 (Red Hat 4.8.5-11) (GCC) 
4 built with OpenSSL 1.0.1e-fips 11 Feb 2013
5 TLS SNI support enabled
6 configure arguments: --prefix=/usr/local/openresty/nginx --with-cc-opt=-O2 --add-module=../ngx_devel_kit-0.3.0 --add-module=../echo-nginx-module-0.60 --add-module=../xss-nginx-module-0.05 --add-module=../ngx_coolkit-0.2rc3 --add-module=../set-misc-nginx-module-0.31 --add-module=../form-input-nginx-module-0.12 --add-module=../encrypted-session-nginx-module-0.06 --add-module=../srcache-nginx-module-0.31 --add-module=../ngx_lua-0.10.7 --add-module=../ngx_lua_upstream-0.06 --add-module=../headers-more-nginx-module-0.32 --add-module=../array-var-nginx-module-0.05 --add-module=../memc-nginx-module-0.17 --add-module=../redis2-nginx-module-0.13 --add-module=../redis-nginx-module-0.3.7 --add-module=../rds-json-nginx-module-0.14 --add-module=../rds-csv-nginx-module-0.07 --with-ld-opt=-Wl,-rpath,/usr/local/openresty/luajit/lib --add-module=/opt/nginx-rtmp-module-master --with-http_ssl_module 
```

先设计一下功能模块，在nginx.conf文件里面，有如下几个location：

```lua
# 业务逻辑的入口
location / {
    ...
}

# 动态反向代理开关控制入口
location /config {
    ...
}

# 添加反向代理的服务器信息进入lua_shared_dict定义的全局表单
location /add_ups { 
	...
}

# 从lua_shared_dict定义的全局表单里面删除掉不再参与反向代理的服务器信息
location /stop_ups {
	...
}

# 查看当前lua_shared_dict定义的全局表单里面有那些服务器信息
location /check_ups {
	...
}

```

为了验证这个设计，我在本地开发机器上，将同一个RDConsumer应用部署在3个不同的端口下，对应于nginx里面的upstream块：

```json
upstream robot_ups {
    server 10.90.9.20:8090;
    server 10.90.9.20:8081;
    server 10.90.9.20:9080;
}
```

在这里，**强调一下，这里，我们验证的动态反向代理，是轮询的方式**，当然，根据需要可以设计成符合各自业务的逻辑。

 

## 详细介绍

###  nginx.conf

```
#user  nobody;
worker_processes  4;

error_log  logs/error.log;
error_log  logs/error.log  notice;
error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
    use   epoll;
}

http {
    lua_shared_dict dyn_ups_zone 10m;

    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;
 
    upstream robot_ups {
        server 10.90.9.20:8090;
        server 10.90.9.20:8081;
        server 10.90.9.20:9080;
    }

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;
        
        location / {
            set_by_lua_file $cur_ups /opt/shihuc/luahome/ablb/bussups.lua
            proxy_next_upstream off;  
            proxy_set_header Host $host:$server_port;
            proxy_set_header Remote_Addr $remote_addr;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://$cur_ups;  
        } 

        location /config {
            default_type  text/plain;
            content_by_lua_block {
                local foo = ngx.req.get_uri_args()["foo"]
                if foo == nil then
                    ngx.say("usage: /config?foo=off, or /config?foo=on")
                    return;
                end
                ngx.log(ngx.INFO, "config ab deploy feature: ", foo);
                ngx.say("config ab deploy feature: ", foo);
                    
                ngx.shared.dyn_ups_zone:set("robotfoo", foo);
            }
        }

        location /stop_ups {
            default_type  text/plain;
            content_by_lua_file /opt/shihuc/luahome/ablb/stopups.lua;
        }

        location /add_ups {
            default_type  text/plain;
            content_by_lua_block {
                local add_s = ngx.req.get_uri_args()["ups"]  
                if add_s == nil then 
                    ngx.say("usage: /add_ups?ups=x.x.x.x")  
                    return "no add_s"
                end
                ngx.log(ngx.INFO, "add upstream server: ", add_s);
                local dynupszone = ngx.shared.dyn_ups_zone;
                local ups = dynupszone:get("robotups");
                if ups == nil then
                   ngx.say("first init global dict dyn_ups_zone");
                   ups = add_s
                else
                   local unders = "-";
                   ups = ups..unders
                   ups = ups..add_s
                end
                local succ, err, forcible = dynupszone:set("robotups", ups);
                ngx.say("succ: ",succ, ", err: ", err, ", forcible: ", forcible);
                ngx.say(dynupszone.get(dynupszone, "robotups"))
            }
        }
        
        location /check_ups {
            default_type  text/plain;
            content_by_lua_block {
                local dynupszone = ngx.shared.dyn_ups_zone;
                local ups = dynupszone:get("robotups");
                ngx.say(ups);
            }
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```



 

2. 调用add_ups url向全局缓存lua_shared_dict dyn_ups_zone 10m填写数据。

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202146074-1914941131.jpg)

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202231574-317847794.jpg)

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202240402-1535061211.jpg)

对应的后台日志如下：

```
2017/12/14 18:46:47 [info] 4347#0: *1 [lua] content_by_lua(nginx.conf:133):7: add upstream server: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "GET /add_ups?ups=10.90.9.20:8081 HTTP/1.1", host: "10.90.7.10"
2017/12/14 18:48:35 [info] 4347#0: *3 [lua] content_by_lua(nginx.conf:133):7: add upstream server: 10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "GET /add_ups?ups=10.90.9.20:8090 HTTP/1.1", host: "10.90.7.10"
2017/12/14 18:49:05 [info] 4347#0: *3 [lua] content_by_lua(nginx.conf:133):7: add upstream server: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "GET /add_ups?ups=10.90.9.20:9080 HTTP/1.1", host: "10.90.7.10"
```

 

3. config配置灰度启用

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202333980-944643214.jpg)

日志请参考：

```
2017/12/14 18:58:05 [info] 4347#0: *7 [lua] content_by_lua(nginx.conf:103):7: config ab deploy feature: on, client: 10.90.9.20, server: localhost, request: "GET /config?foo=on HTTP/1.1", host: "10.90.7.10"
```

 

4. 在不做灰度停用机器的时候，看看请求如何调度。这里，我的测试应用在本地部署了3个，端口区分。在10.90.7.10这个nginx上做反向代理，轮询分发请求。我执行了4次请求，通过restlet client （chrome的一个http模拟插件），nginx的后台日志如下：



```
2017/12/14 19:01:18 [info] 4347#0: *9 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:18 [info] 4347#0: *9 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:18 [info] 4347#0: *9 [lua] bussups.lua:29: cnt: nil, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:18 [info] 4347#0: *9 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:18 [info] 4347#0: *9 [lua] bussups.lua:50: idx: 3, exc: 3 ,current ups: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:19 [info] 4347#0: *9 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:19 [info] 4347#0: *9 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:19 [info] 4347#0: *9 [lua] bussups.lua:29: cnt: 1, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:19 [info] 4347#0: *9 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:19 [info] 4347#0: *9 [lua] bussups.lua:50: idx: 1, exc: 3 ,current ups: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:21 [info] 4347#0: *9 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:21 [info] 4347#0: *9 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:21 [info] 4347#0: *9 [lua] bussups.lua:29: cnt: 2, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:21 [info] 4347#0: *9 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:21 [info] 4347#0: *9 [lua] bussups.lua:50: idx: 2, exc: 3 ,current ups: 10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:22 [info] 4347#0: *9 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:22 [info] 4347#0: *9 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:22 [info] 4347#0: *9 [lua] bussups.lua:29: cnt: 3, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:22 [info] 4347#0: *9 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:8090-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:01:22 [info] 4347#0: *9 [lua] bussups.lua:50: idx: 3, exc: 3 ,current ups: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```



从日志看，轮询是没有问题的。轮询的依据，是在nginx的全局变量dyn_ups_zone里面定义了一个cnt的变量，记录请求次数。请求数与当前反向代理里面的机器数量求模。用余数作为lua列表的下标，求出服务器IP端口信息。作为反向代理的机器。
这里要注意的是：
**a. lua数组或者列表下标不是从0开始，而是1.**
**b. lua数组的下标，可以是不同数据类型的值，不像java等高级语言，是数字下标。**

 

5. 停用一台服务器，通过stop_ups调用。然后查看反向代理跳转是否生效。

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202550277-211053338.jpg)

发现stop操作，有点问题，请看下图，原来3个应用，停了中间一个，最后的ups列表中怎么只有一个应用服务器信息了？先看看stopups.lua的脚本吧：



```lua
#!/usr/bin/env lua

function split(s, delim)
    if type(delim) ~= "string" or string.len(delim) <= 0 then
        return
    end

    local start = 1
    local t = {}
    while true do
        local pos = string.find (s, delim, start, true) -- plain find
        if not pos then
          break
        end

        table.insert (t, string.sub (s, start, pos - 1))
        start = pos + string.len (delim)
    end
    table.insert (t, string.sub (s, start))

    return t
end

local stop_s = ngx.req.get_uri_args()["ups"];
if stop_s == nil then
   ngx.say("usage: /stop_ups?ups=x.x.x.x");
   return "no stop_s"
end
ngx.say("stop upstream server: ", stop_s);
local dynupszone = ngx.shared.dyn_ups_zone;
local ups = dynupszone:get("robotups");
if ups == nil then
   ngx.say("currently, there is no server ip to stop...");
   return;
end
local table_ups = split(ups, "-");
ngx.say(table_ups);
local delid=0;
for k,v in ipairs(table_ups) do
   ngx.say("key: ",k,", value: ", v);
   if v == stop_s then
      delid = k;
   end
end
table_ups[delid] = nil;
ngx.say(table_ups);
local new_ups = table.concat(table_ups,"-");
ngx.say("new ups: ", new_ups);
dynupszone:set("robotups",new_ups);
```



分析一下，发现，table数据table_ups里面设置nil的值，其实也是可以的。但是，在做table.concat的时候，会将第一个nil作为数据拼接的结束标识了，于是nil后面的数据不被计入。调整一下统计余下应用服务器信息的算法。调整后如下（local table_ups = split(ups, "-");代码之前的不变）：


```
local table_ups = split(ups, "-");
ngx.say(table_ups);
local new_table_ups = {}
for k,v in ipairs(table_ups) do
   ngx.say("key: ",k,", value: ", v);
   if v ~= stop_s then
      table.insert(new_table_ups, v);
   end
end
ngx.say(new_table_ups);
local new_ups = table.concat(new_table_ups,"-");
ngx.say("new ups: ", new_ups);
dynupszone:set("robotups",new_ups);
```



重复前面的操作，再进行stop_ups，就得到合理的结果，如图:

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202707699-690354821.jpg)

在模拟发送请求4次，看看日志：



```
2017/12/14 19:18:38 [info] 4747#0: *6 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:38 [info] 4747#0: *6 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:38 [info] 4747#0: *6 [lua] bussups.lua:29: cnt: nil, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:38 [info] 4747#0: *6 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:38 [info] 4747#0: *6 [lua] bussups.lua:50: idx: 2, exc: 2 ,current ups: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:39 [info] 4747#0: *6 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:39 [info] 4747#0: *6 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:39 [info] 4747#0: *6 [lua] bussups.lua:29: cnt: 1, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:39 [info] 4747#0: *6 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:39 [info] 4747#0: *6 [lua] bussups.lua:50: idx: 1, exc: 2 ,current ups: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:29: cnt: 2, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:50: idx: 2, exc: 2 ,current ups: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:29: cnt: 3, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:18:40 [info] 4747#0: *6 [lua] bussups.lua:50: idx: 1, exc: 2 ,current ups: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```



从日志看，现在ups的服务器只有2个了，刚才stop掉的一个，不再了。执行4次请求，分别在余下的2个服务器之间轮询。合乎逻辑设计。

 

6. 关闭灰度发布的开发，执行config?foo=off。参考题config_off,nginx的后台日志如下：

![img](https://images2017.cnblogs.com/blog/844237/201712/844237-20171215202808261-1984947101.jpg)

```
2017/12/14 19:21:47 [info] 4747#0: *11 [lua] content_by_lua(nginx.conf:103):7: config ab deploy feature: off, client: 10.90.9.20, server: localhost, request: "GET /config?foo=off HTTP/1.1", host: "10.90.7.10"
```

 

7. 在关闭灰度开关的情况下，看看反向代理的逻辑。主要看看后台日志：

第1次请求：

```
2017/12/14 19:23:46 [info] 4747#0: *13 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:23:46 [info] 4747#0: *13 [lua] bussups.lua:28: foo: off, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:23:46 [info] 4747#0: *13 [lua] bussups.lua:29: cnt: 4, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:23:46 [info] 4747#0: *13 [lua] bussups.lua:56: use default upstream, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```

从部署的3台应用服务器上来看，这次调度到8089端口的应用了。

 

第2次请求：

```
2017/12/14 19:27:32 [info] 4747#0: *15 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:27:32 [info] 4747#0: *15 [lua] bussups.lua:28: foo: off, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:27:32 [info] 4747#0: *15 [lua] bussups.lua:29: cnt: 5, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:27:32 [info] 4747#0: *15 [lua] bussups.lua:56: use default upstream, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```

从部署的3台应用服务器上来看，这次调度到8081端口的应用了。

 

第3次请求：

```
2017/12/14 19:29:31 [info] 4747#0: *17 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:29:31 [info] 4747#0: *17 [lua] bussups.lua:28: foo: off, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:29:31 [info] 4747#0: *17 [lua] bussups.lua:29: cnt: 6, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:29:31 [info] 4747#0: *17 [lua] bussups.lua:56: use default upstream, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```

从部署的3台应用服务器上来看，这次调度到9080端口的应用了。

 

基于上面3次foo=off的模拟调用来看，程序运行于upstream模块的轮询模式。这个时候全局变量ups里面只有2个服务器应用。

 

8. 将刚才灰度停用的服务器8090加回来，再次启用foo=on，动态轮询验证。


```log
2017/12/14 19:32:19 [info] 4747#0: *19 [lua] content_by_lua(nginx.conf:133):7: add upstream server: 10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "GET /add_ups?ups=10.90.9.20:8090 HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:01 [info] 4747#0: *23 [lua] content_by_lua(nginx.conf:103):7: config ab deploy feature: on, client: 10.90.9.20, server: localhost, request: "GET /config?foo=on HTTP/1.1", host: "10.90.7.10"


2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:29: cnt: 7, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:50: idx: 1, exc: 3 ,current ups: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:29: cnt: 8, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:20 [info] 4747#0: *23 [lua] bussups.lua:50: idx: 2, exc: 3 ,current ups: 10.90.9.20:9080, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:21 [info] 4747#0: *23 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:21 [info] 4747#0: *23 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:21 [info] 4747#0: *23 [lua] bussups.lua:29: cnt: 9, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:21 [info] 4747#0: *23 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:21 [info] 4747#0: *23 [lua] bussups.lua:50: idx: 3, exc: 3 ,current ups: 10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:22 [info] 4747#0: *23 [lua] bussups.lua:27: ups: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:22 [info] 4747#0: *23 [lua] bussups.lua:28: foo: on, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:22 [info] 4747#0: *23 [lua] bussups.lua:29: cnt: 10, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:22 [info] 4747#0: *23 [lua] bussups.lua:39: ups list: 10.90.9.20:8081-10.90.9.20:9080-10.90.9.20:8090, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
2017/12/14 19:34:22 [info] 4747#0: *23 [lua] bussups.lua:50: idx: 1, exc: 3 ,current ups: 10.90.9.20:8081, client: 10.90.9.20, server: localhost, request: "POST /RDConsumer/httpclient/conrst HTTP/1.1", host: "10.90.7.10"
```


从nginx日志以及应用程序的后台日志看，灰度的负载均衡方向代理逻辑，依然正常。

 

到此，整个验证完美收官！下面，附上，nginx.conf配置中涉及到的几个lua的脚本文件：

bussups.lua:


```lua
#!/usr/bin/env lua

function split(s, delim)
    if type(delim) ~= "string" or string.len(delim) <= 0 then
        return
    end

    local start = 1
    local t = {}
    while true do
        local pos = string.find (s, delim, start, true) -- plain find
        if not pos then
          break
        end

        table.insert (t, string.sub (s, start, pos - 1))
        start = pos + string.len (delim)
    end
    table.insert (t, string.sub (s, start))

    return t
end

local ups = ngx.shared.dyn_ups_zone:get("robotups");
local foo = ngx.shared.dyn_ups_zone:get("robotfoo");
local cnt = ngx.shared.dyn_ups_zone:get("robotcnt");
ngx.log(ngx.INFO, "ups: ", ups);
ngx.log(ngx.INFO, "foo: ", foo);
ngx.log(ngx.INFO, "cnt: ", cnt);

if cnt == nil then
   cnt = 0;
end
ngx.shared.dyn_ups_zone:set("robotcnt", cnt+1);

if foo == "on" then
   if ups ~= nil then
      --ngx.log(ngx.info, "get robotups server list: ", ups)
      ngx.log(ngx.INFO, "ups list: ", ups);
      local table_ups = split(ups, "-");
      local exc = 0;
      for k,v in ipairs(table_ups) do
          exc = exc + 1;
      end
      local idx = cnt % exc;
      if idx == 0 then  --lua array index from 1, not from 0
         idx = exc;
      end
      local cur_ups = table_ups[idx];
      ngx.log(ngx.INFO, "idx: ", idx, ", exc: ", exc,  " ,current ups: ", cur_ups);
      return cur_ups
   end
   ngx.log(ngx.INFO, "ab lb configuration error, use default upstream");
   return "robot_ups";
else
   ngx.log(ngx.INFO, "use default upstream");
   return "robot_ups";
end
```

 stopups.lua:

```lua
#!/usr/bin/env lua

function split(s, delim)
    if type(delim) ~= "string" or string.len(delim) <= 0 then
        return
    end

    local start = 1
    local t = {}
    while true do
        local pos = string.find (s, delim, start, true) -- plain find
        if not pos then
          break
        end

        table.insert (t, string.sub (s, start, pos - 1))
        start = pos + string.len (delim)
    end
    table.insert (t, string.sub (s, start))

    return t
end

local stop_s = ngx.req.get_uri_args()["ups"];
if stop_s == nil then
   ngx.say("usage: /stop_ups?ups=x.x.x.x");
   return "no stop_s"
end
ngx.say("stop upstream server: ", stop_s);
local dynupszone = ngx.shared.dyn_ups_zone;
local ups = dynupszone:get("robotups");
if ups == nil then 
   ngx.say("currently, there is no server ip to stop...");
   return;
end
local table_ups = split(ups, "-");
ngx.say(table_ups);
local new_table_ups = {}
for k,v in ipairs(table_ups) do
   ngx.say("key: ",k,", value: ", v);
   if v ~= stop_s then
      table.insert(new_table_ups, v);
   end
end
ngx.say(new_table_ups);
local new_ups = table.concat(new_table_ups,"-");
ngx.say("new ups: ", new_ups);
dynupszone:set("robotups",new_ups);
```




nginx功能强大，配合上lua脚本，在ngx_lua模块的存在下，功能就更加强大。感兴趣的话，可以加我关注哟，我们一起探讨！