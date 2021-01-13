# [Ubuntu 16.04安装MySQL（5.7.18）](https://www.cnblogs.com/EasonJim/p/7147787.html)

## 须知

1、MySQL各类型版本的区别，参考：http://www.cnblogs.com/EasonJim/p/6274344.html

2、官方的下载地址一般指向最新的版本下载，如果要下载以前的版本，比如5.5.x的版本，有特殊入口，参考：http://www.cnblogs.com/EasonJim/p/7147134.html

3、随着时间的推移，教程上可能会失效，但是最标准和最新的教程官方是提供的，入口请参考：http://www.cnblogs.com/EasonJim/p/7147198.html

## 安装方式选择

0、前提，无论是哪种安装方式都必须对my.cnf文件有所了解，参考：http://www.cnblogs.com/EasonJim/p/7158466.html

1、在安装之前需要注意，前面有篇文章http://www.cnblogs.com/EasonJim/p/6275863.html是讲解Mac下安装MySQL的，里面采用的安装方式基于安装包pkg，有安装界面，安装好之后在系统设置和命令行上自动配置了环境变量等。

2、对于Mac下安装，我觉得越简单越好，能用就行了，毕竟在Mac下不可能作为服务器使用，至于开机启动和不启动也没关系，只要能做简单的测试即可。命令行这些也无关紧要。还有就是很多时候在开发时都是连接公司的服务器来进行的。

3、而对于在Linux下安装，如果为开发服务器，那么建议安装deb版本，也就是安装包的形式，或者是APT源进行安装，安装好之后自动配置了环境变量等。观点就是能用就行，不需要太复杂的配置，比较很多时候在开发时都是连接公司的服务器来进行的。

4、如果对于服务器版本的Linux，建议是安装tar.gz压缩包版本的，这个安装全部都是手动配置，包括启动服务，环境变量等，因为可以给你一个很清晰的配置思路，至于安装了什么，配置了什么，这些都可以一步了然的排查出来。当然，在Linux下deb还是tar.gz各有各的好处，毕竟这些都可以根据需要进行版本选择。

5、通过安装tar.gz压缩包版本，也就是二进制包，能在同一台机器上安装多个MySQL。



## APT方式安装

说明：此种方式完全参考*[官方教程](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/)*。

注意：通过APT方式安装的版本都是现在最新的版本，现在我安装的是5.7.18。通过这种方式安装好之后开机自启动都已经配置好，和命令行上的环境变量，无需手动配置。

### 配置APT源

1.（可省略）下载官方提供的 `mysql-apt-config.deb` 包进行APT源设置。*[点我下载](https://dev.mysql.com/downloads/repo/apt/)*

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712005943462-259670188.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712005943462-259670188.png)

不过我感觉这个配置没什么作用，只不过可以配置可以安装什么类型版本的MySQL，和一些常用工具等，这些都可以自己手动通过 apt-get 的方式进行安装解决。

```
sudo dpkg -i mysql-apt-config_0.8.6-1_all.deb
```

运行之后会出现如下界面：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712010158462-1359480244.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712010158462-1359480244.png)

一般只需要默认，按方向键选择OK回车即可。

完成后运行更新命令：

```
sudo apt-get update
```

说明：官方说通过这个工具这样操作之后，安装MySQL时就是按照上面选择的来进行。

### 安装

```
sudo apt-get install mysql-server
```

此时如果提示依赖不足，如下所示：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013030915-745345968.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013030915-745345968.png)

那么需要运行下面命令解决依赖问题

```
sudo apt-get install -f
```

安装MySQL时会一并安装如下所示的软件：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013215134-1044405155.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013215134-1044405155.png)

完成后再次运行 `sudo apt-get install mysql-server`。如果没出现依赖问题，那么就不需要使用此命令。

### 安装过程

安装过程会提示输入数据库的登录名和密码，输入即可，如下所示：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013507306-405580830.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013507306-405580830.png)

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013535197-795103168.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712013535197-795103168.png)

### 安装后的操作

说明：通过这种方式安装好之后开机自启动都已经配置好，和命令行上的环境变量，无需手动配置。

安装好之后会创建如下目录：

数据库目录：/var/lib/mysql/ 

配置文件：/usr/share/mysql（命令及配置文件） ，/etc/mysql（如：my.cnf）

相关命令：/usr/bin(mysqladmin mysqldump等命令) 和/usr/sbin

启动脚本：/etc/init.d/mysql（启动脚本文件mysql的目录）

测试：

```
#服务启动后端口查询
sudo netstat -anp | grep mysql
```

```
#服务管理
#启动
sudo service mysql start
#停止
sudo service mysql stop
#服务状态
sudo service mysql status
```

```
#连接数据库
mysql -h 127.0.0.1 -P 3306 -uroot -p123456
#-h为远程IP，-P为端口号，-u为用户名，-p为密码
#测试SQL
show databases;
```

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712015529087-1235120750.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712015529087-1235120750.png)

测试一切正常。

### 卸载

```
#首先使用以下命令删除MySQL服务器：
sudo apt-get remove mysql-server
#然后，删除随MySQL服务器自动安装的任何其他软件：
sudo apt-get autoremove
#卸载其他组件：
sudo apt-get remove <<package-name>>
#查看从MySQL APT存储库安装的软件包列表：
dpkg -l | grep mysql | grep ii
```



## DEB 方式安装

说明：参考*[官方安装文档](https://dev.mysql.com/doc/refman/5.7/en/linux-installation-debian.html)*

### 下载

其实DEB Bundle类型就是离线deb安装包，把所有软件打包进去了。登录站点：https://dev.mysql.com/downloads/mysql/

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712020338509-661966154.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712020338509-661966154.png)

选择系统：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712043640197-1587635812.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712043640197-1587635812.png)

选择版本，在最下方选择16.04：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712020705040-1235878038.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712020705040-1235878038.png)

在列表上会有DEB Package的，这个其实就是deb文件，不过也是在线安装的形式，所以文件很小，不建议选择。

### 解压

```
tar xvf mysql-server_5.7.18-1ubuntu16.04_amd64.deb-bundle.tar 
```

解压出来的文件如下：

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712022147212-1730861027.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712022147212-1730861027.png)

### 安装

说明：以下命令是官网提供的

```
#libaio 如果系统中尚未存在库，则 可能需要安装该库：
sudo apt-get install libaio1
#使用以下命令预配置MySQL服务器软件包：
sudo dpkg-preconfigure mysql-community-server_*.deb
#提示：将被要求为root用户提供您的MySQL安装密码。
#对于MySQL服务器的基本安装，请安装数据库公用文件包，客户端包，客户端元包，服务器包和服务器元包（按此顺序）; 可以使用单个命令来执行此操作：
#注意：下面这条命令不能直接运行，应该拆开来按中括号里面以逗号分开的顺序进行安装，比如：
#sudo dpkg -i mysql-{common,community-client,client,community-server,server}_*.deb
sudo dpkg -i mysql-common_*.deb
sudo dpkg -i mysql-community-client_*.deb
sudo dpkg -i mysql-client_*.deb
sudo dpkg -i mysql-community-server_*.deb
sudo dpkg -i mysql-server_*.deb
#如果中途被dpkg警告未满足的依赖关系 ，可以使用apt-get来修复它们，然后再运行中断的命令 ：
sudo apt-get -f install
```

 安装完成后和第一种方式效果上是一致的。

## tar.gz方式安装

以下*[教程官网](https://dev.mysql.com/doc/refman/5.7/en/binary-installation.html)*已经提供

说明：这种方式是需要进行后期处理，比如开机启动服务，命令行环境变量，以及配置文件设置等。

### 下载

 站点：https://dev.mysql.com/downloads/mysql/

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712044213103-1528089607.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712044213103-1528089607.png)

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712044249681-851564642.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170712044249681-851564642.png)

### 解压

```
tar zxvf mysql-5.7.18-linux-glibc2.5-x86_64.tar.gz
sudo mv mysql-5.7.18-linux-glibc2.5-x86_64 /usr/local
sudo ln -s /usr/local/mysql-5.7.18-linux-glibc2.5-x86_64/ /usr/local/mysql
```

### 安装

由于MySQL运行需要libaio1库，所以需要运行以下命令进行安装：

```
sudo apt-get install libaio1
```

```
#添加用户组
sudo groupadd mysql
#添加用户，这个用户是不能登录的
sudo useradd -r -g mysql -s /bin/false mysql
#进入文件目录，mysql是链接
cd /usr/local/mysql
#新建文件夹
sudo mkdir mysql-files
#修改文件夹的权限
sudo chmod 750 mysql-files
sudo chown -R mysql .
sudo chgrp -R mysql .
#安装初始化，注意：此部最后一行会有一个初始化密码，用于root账号的首次登录
sudo bin/mysqld --initialize --user=mysql 
#生成证书
sudo bin/mysql_ssl_rsa_setup        
#把权限修改回来      
sudo chown -R root .
sudo chown -R mysql data mysql-files
```

### 启动

```
#启动在后台
sudo bin/mysqld_safe --user=mysql &
```

### 登录测试并修改root密码

```
/usr/local/mysql/bin/mysql -uroot -p
```

提示：密码在安装初始化时最后一行的信息，里面有括号和特殊字符。

```
#修改root密码，每一个分号直接回车
mysql> SET PASSWORD = PASSWORD('新密码');
mysql> ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
mysql> flush privileges;
#增加一个'root'@'%'账号实现远程登录
mysql> grant all privileges on *.* to 'root'@'%' identified by '新密码' with grant option;
```

### 配置服务自动启动

```
#复制服务文件到/etc/init.d
sudo cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql.server
```

### 安装sysv-rc-conf

```
sudo apt-get install sysv-rc-conf
```

### 启动sysv-rc-conf

```
sudo sysv-rc-conf
```

[![img](https://images2015.cnblogs.com/blog/417876/201707/417876-20170713030417775-1008544459.png)](https://images2015.cnblogs.com/blog/417876/201707/417876-20170713030417775-1008544459.png)

按空格键出现X，然后按Q退出。重启即可。

服务的相关操作命令：

```
#服务状态
sudo service mysql.server status
#服务启动
sudo service mysql.server start
#服务停止
sudo service mysql.server stop
```

### 配置环境变量

在～/.profile文件的最下方加入

```
export PATH=$PATH:/usr/local/mysql/bin
```

 

## 参考

http://www.cnblogs.com/oldfish/p/5039772.html（基于deb包的安装）

http://blog.csdn.net/lllliulin/article/details/51526569（基于APT源的安装）

http://www.2cto.com/database/201401/273423.html（基于APT源的安装）

https://my.oschina.net/ramboo/blog/725378（基于二进制包安装多个MySQL）

http://blog.csdn.net/carry9148/article/details/52624990（基于二进制包安装，有Shell脚本快速安装）

http://www.jianshu.com/p/b600c3b28bd9（基于二进制包安装）

http://www.jianshu.com/p/90b5a749b3b0（my.cnf）

http://www.fx114.net/qa-220-164752.aspx（my.cnf）

