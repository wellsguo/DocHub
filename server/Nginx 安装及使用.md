# Nginx 安装篇

## 1. Ubuntu 安装 Nginx

```sh
sudo apt-get install nginx
```


## 2. 启动 Nginx

```shell
/etc/init.d nginx start
```

or

```shell
service nginx start
```

or

```shell
systemctl nginx start
```



> - `/etc/init.d` 是 `sysVinit` 服务的启动方式，对于一些古老的系统或者服务使用这个。
> - `service` 也是 `sysVinit`，比 `/etc/init.d`先进一点，底层还是调用/etc/init.d
> -  ` systemctl` 是 `systemD` 命令的主要方式, 尽管一些老的系统或者命令不支持 `systemctl`， 但是`systemctl` 最后会逐渐的替代其他的命令方式的， 能用这个就优先用这个,是最时尚/方便的



# Nginx 路径篇



 **主程序**

/usr/sbin/nginx：



**存放配置文件**

/etc/nginx



**存放静态文件**

/usr/share/nginx



**存放日志**

/var/log/nginx

## Linux 小技巧

- 查找Nginx启动文件路径

```shell
find / -name nginx.conf
```



- 查询nginx进程

```shell
ps -ef | grep nginx
```



- 重启nginx

```shell
sudo nginx -s reload
```



# 配置篇



> **推荐配置**
>
> 配置文件位置：`/etc/nginx/conf.d/***.conf`
> 静态网页位置：` /var/www/ `
> html 中加载的 `js` 之类的文件夹和 `index.html` 在一个文件夹中



## **配置案例** 1

> 设置静态文件的路径

```shell
server {
  listen 80;
  server_name # 你的网站IP 或 ****.com;
  
  location /www1
  {
      alias /var/www/****;
      index index.html index.php index.htm;
  }
  
  location /www2
  {
      alias /var/www/****;
      index index.html index.php index.htm;
  }
  
  location  ~ .*\.(jpg|jpeg|gif|png|ico|css|js|pdf|txt|webp)$
  {
      root /var/www/;
      proxy_temp_path /var/www/;
  }
}  
```



> **alias vs root** 
>
> - root和alias是系统文件路径的设置。 
> - root用来设置根目录，而alias用来重置当前文件的目录。
>
> ```shell
> location /img/ {
>     alias /var/www/image/;
> }
> # 若按照上述配置的话，则访问/img/目录里面的文件时，ningx会自动去/var/www/image/目录找文件
> 
> location /img/ {
>     root /var/www/image;
> }
> # 若按照这种配置的话，则访问/img/目录下的文件时，nginx会去/var/www/image/img/目录下找文件。
> ```



## 配置案例 2

> **反向代理**
> 客户端（浏览器）不直接访问目标服务器，而是通过代理服务器进行访问，可以不暴露目标服务器实际IP。

```shell
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  102400;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name www.simonjia.top ;#服务器域名
	      #rewrite ^(.*) https://$server_name$1 permanent; #这句是代表 把http的域名请求转成https
        #charset koi8-r;
		    error_log   /logs/nginx-error.log info;
        access_log  /logs/host.access.log  main;
        location / {
            #root   /usr/tools/nignx/nginx-1.9.9/web;
			      alias /usr/workspace/pc;
            #index  index.html index.htm;
	          #proxy_pass  http://www.simonjia.top; #因为这里还是80端口，所以保持http就可以
			      proxy_pass http://127.0.0.1:8001/;#代理的实际端口，在本地8001
			      proxy_set_header Host $host;# 代理请求信息，转换为实际域名地址
		        proxy_set_header X-real-ip $remote_addr;
		        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		        proxy_connect_timeout 15s;
        }
	      #8080管理后台
        location /admin/ {
		        alias /usr/workspace/shiroSSO;
		        proxy_pass http://127.0.0.1:8080/admin/;
            proxy_set_header X-real-ip $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_connect_timeout 15s;
        }
		    # 配置静态资源 解决js css文件无法加载无法访问的问题，注意末尾不能有 /
			  # 正则匹配css文件，防止css：404
			  # 多个项目css文件，可以根据项目路径进行匹配
        location ~ .*(/admin).*\.(js|css|jpg|jpeg|gif|png|ico|pdf|txt)$ {
             proxy_pass http://127.0.0.1:8080; #匹配实际端口地址（不需要加入项目名）
			  }
			
		    location ~ .*\.(js|css|jpg|jpeg|gif|png|ico|pdf|txt)$ {
		         proxy_pass http://127.0.0.1:8001;
		    }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
 
    }

 

    # HTTPS server 这里是配置ssl证书，需添加对应ssl模块
    #
    server {
        listen       443 ssl;
        server_name  www.simonjia.top;

        ssl_certificate      /usr/tools/nignx/ssl/xx.crt; #添加ssl证书
        ssl_certificate_key  /usr/tools/nignx/ssl/xx.key;

        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;

        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers  on;

        location / {
            root   html;
            index  index.html index.htm;
      	    # proxy_pass   https://www.simonjia.top;
        }
        
		    # 8080管理后台
        location /admin/ {
		         alias /usr/workspace/shiroSSO;
             proxy_pass http://127.0.0.1:8080/admin/;
             proxy_set_header X-real-ip $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_connect_timeout 5s;
        }
		    
		    # 配置静态资源 解决js css文件无法加载无法访问的问题，注意末尾不能有 /
        location ~ .*\.(js|css|jpg|jpeg|gif|png|ico|pdf|txt)$ {
             proxy_pass http://127.0.0.1:8080;
        }
    }

}
```



## 配置案例 3



```shell
    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;
        #access_log  logs/host.access.log  main;


        location / {
            proxy_pass http://lxstest;
            root   html;
            index  index.html index.htm;
        }

        upstream lxstest {
             server localhost:7070;
             server localhost:7071;
             server localhost:7072;

        }
```



### Nginx upstream 的 5 种权重分配方式



原文地址:https://blog.csdn.net/wh2691259/article/details/52300423



####  1. 轮询(默认)

每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除。



####  2. weight

指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。

```java
upstream backend { 
    server 192.168.0.14 weight=10; 
    server 192.168.0.15 weight=10; 
} 
```

#### 3. ip_hash

每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，可以解决session的问题。

```java
upstream backend { 
    ip_hash; 
    server   172.16.125.76:8066 weight=10;  
    server   172.16.125.76:8077 down;  
    server   172.16.0.18:8066 max_fails=3 fail_timeout=30s;  
    server   172.16.0.18:8077 backup;  
} 
```

根据服务器的本身的性能差别及职能，可以设置不同的参数控制。

- down 表示负载过重或者不参与负载
- weight 权重过大代表承担的负载就越大
- backup 其它服务器时或down时才会请求backup服务器
- max_fails 失败超过指定次数会暂停或请求转往其它服务器
- fail_timeout 失败超过指定次数后暂停时间



#### 4. fair（第三方）

按后端服务器的响应时间来分配请求，响应时间短的优先分配



#### 5. url_hash（第三方）

按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，后端服务器为缓存时比较有效

 