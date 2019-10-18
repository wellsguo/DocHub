

## 环境
- CenOS 6.5
- Nginx-Master：10.10.10.128
- Nginx-Backup：10.10.10.129
- Tomcat1：10.10.10.130
- Tomcat2：10.10.10.131
- VIP：10.10.10.100

## 一 环境基础配置
1. 更换国内yum源
2. 关闭防火墙、SELinux
3. 时间同步

## 二 安装 Web 服务

### 1 查看是否安装JDK
```
[root@Tomcat1 ~]# java -version
java version "1.8.0_171"
Java(TM) SE Runtime Environment (build 1.8.0_171-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.171-b11, mixed mode)
```
### 2 安装JDK
1. 官网下载二进制包

2. 解压到/usr/local/java
```
tar zxvf jdk-8u171-linux-x64.tar.gz -C /usr/local/java/
```

3. 修改环境变量/etc/profile
```
JAVA_HOME=/usr/local/java
PATH=$JAVA_HOME/bin:$PATH
CLASSPATH=$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/tools.jar
export PATH JAVA_HOME CLASSPATH
```

4. 使环境变量生效
```
source /etc/profile
```

### 3 下载Tomcat源码包
```
wget -O /opt/apache-tomcat-9.0.7.tar.gz http://mirrors.hust.edu.cn/apache/tomcat/tomcat-9/v9.0.7/bin/apache-tomcat-9.0.7.tar.gz
```
### 4 解压到/usr/local/tomcat
```
tar zxvf /opt/apache-tomcat-9.0.7.tar.gz -C /usr/local/
```
### 5 修改Tomcat的主页
```
rm -rf /usr/local/apache-tomcat-9.0.7/webapps/ROOT/*
echo "Tomcat1" >/usr/local/apache-tomcat-9.0.7/webapps/ROOT/index.html  #Tomcat1
echo "Tomcat2" >/usr/local/apache-tomcat-9.0.7/webapps/ROOT/index.html  #Tomcat2
```

### 6 测试Tomcat能否正常启动
```
[root@Tomcat1 bin]# ./usr/local/apache-tomcat-9.0.7/bin
/startup.sh 
Using CATALINA_BASE:  /usr/local/apache-tomcat-9.0.7
Using CATALINA_HOME:  /usr/local/apache-tomcat-9.0.7
Using CATALINA_TMPDIR: /usr/local/apache-tomcat-9.0.7/temp
Using JRE_HOME:        /usr/local/java
Using CLASSPATH:      /usr/local/apache-tomcat-9.0.7/bin/bootstrap.jar:/usr/local/apache-tomcat-9.0.7/bin/tomcat-juli.jar
Tomcat started.

curl 10.10.10.130:8080  #返回Tomcat1
curl 10.10.10.131:8080  #返回Tomcat2
```

至此web端配置完成。

## 二 Nginx 反向代理安装

### 1 安装依赖软件
```
yum install -y gcc gcc-c++
yum install -y pcre pcre-devel openssl openssl-devel zlib zlib-devel
```
### 2 官网下载源码包

### 3 解压源码包
```
tar zxvf nginx-1.14.0.tar.gz -C /tmp/
```

### 4 编译安装
```
useradd -s /bin/false -M nginx
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx-1.14.0/ --with-http_v2_module --with-http_ssl_module --with-http_sub_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre
make && make install
```

### 5 配置反向代理 /usr/local/nginx/conf/nginx.conf
```conf
worker_processes  1;
pid        /usr/local/nginx/logs/nginx.pid;
worker_rlimit_nofile 51200;
events {
  use epoll;
  worker_connections  51200;
}
http {
  include      mime.types;
  default_type  application/octet-stream;
  server_names_hash_bucket_size 128;
  client_header_buffer_size 32k;
  large_client_header_buffers 4 32k;
  client_max_body_size 8m;
  sendfile        on;
  tcp_nopush      on;
  keepalive_timeout  65;
  tcp_nodelay on;
  gzip on;
  gzip_min_length 1k;
  gzip_buffers 4 16k;
  gzip_http_version 1.0;
  gzip_comp_level 2;
  gzip_types    test/plain application/x-javascript test/css application/xml;
  gzip_vary on;

  upstream backend {
        server 10.10.10.130:8080;
        server 10.10.10.131:8080;

  }
  server {
      listen      80;
      server_name  10.10.10.128;  #Nginx2改为：10.10.10.129
      location / { 
          root  /var/www/html;
          index  index.php index.html index.htm;
          proxy_pass http://backend;
      }
  }
}
```

先测试再启动：

```
[root@Nginx1 ~]# /usr/local/nginx-1.14.0/sbin/nginx -t
nginx: the configuration file /usr/local/nginx-1.14.0//conf/nginx.conf syntax is ok
nginx: configuration file /usr/local/nginx-1.14.0//conf/nginx.conf test is successful
[root@Nginx1 ~]# /usr/local/nginx-1.14.0/sbin/nginx
[root@Nginx1 ~]# lsof -i:80
COMMAND  PID  USER  FD  TYPE DEVICE SIZE/OFF NODE NAME
nginx  4896  root    6u  IPv4  18439      0t0  TCP *:http (LISTEN)
nginx  4897 nginx    6u  IPv4  18439      0t0  TCP *:http (LISTEN)
```
```
curl 10.10.10.128  #轮询返回Tomcat1 Tomcat2
```

Nginx2同样的搭建。

至此Nginx反向代理搭建完成。

## 三 使用 Keepalived 实现高可用

### 1 安装：
    yum install keepalived -y
### 2 修改配置文件/etc/keepalived/keepalived.conf

**MASTER 端：**
```
! Configuration File for keepalived
vrrp_script check_nginx {
        script "/etc/keepalived/check_nginx.sh"
        interval 2
        weight 2
}
global_defs {
  notification_email {
    acassen@firewall.loc
    failover@firewall.loc
    sysadmin@firewall.loc
  }
  notification_email_from Alexandre.Cassen@firewall.loc
  smtp_server 192.168.200.1
  smtp_connect_timeout 30
  router_id LVS_DEVEL1
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        10.10.10.100/24 dev eth0
  }
 track_script {
        check_nginx
  }
}
```

**BACKUP端：**

修改：

```
router_id LVS_DEVEL2
state BACKUP
priority 90
```

检测Nginx脚本：

```
#!/bin/bash
nginxpid=`ps -C nginx --no-header | wc -l`
if [ $nginxpid -eq 0 ];then
        /etc/init.d/keepalived stop
fi
chmod +x /etc/keepalived/check_nginx.sh
```

重启Keepalived服务

```
service keepalived restart
```

## 四 检验服务的高可用

- Nginx1 执行
```
killall nginx
```
发现 web 访问依然正常

- Tomcat1 执行
```
/usr/local/apache-tomcat-9.0.7/bin/shutdown.sh
```
发现 web 访问依然正常

高可用的环境搭建完毕。