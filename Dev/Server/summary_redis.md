## Redis 安装

Redis 是一个 key-value 存储系统。和 Memcached 类似，它支持存储的 value 类型相对更多，包括 string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和 hash（哈希类型）。这些数据类型都支持 push/pop、add/remove 及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。在此基础上，redis 支持各种不同方式的排序。与 memcached 一样，为了保证效率，**数据都是缓存在内存中**。区别的是**redis 会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件**，并且在此基础上实现了 master-slave(主从)同步。

Redis 是一个高性能的 key-value 数据库。 redis 的出现，很大程度补偿了 memcached 这类 key/value 存储的不足，在部 分场合可以对关系数据库起到很好的补充作用。它提供了 Java，C/C++，C#，PHP，JavaScript，Perl，Object-C，Python，Ruby，Erlang 等客户端，使用很方便。 [1]

**Redis 支持主从同步**。数据可以从主服务器向任意数量的从服务器上同步，从服务器可以是关联其他从服务器的主服务器。这使得 Redis 可执行单层树复制。存盘可以有意无意的对数据进行写操作。由于完全实现了发布/订阅机制，使得从数据库在任何地方同步树时，可订阅一个频道并接收主服务器完整的消息发布记录。同步对读取操作的可扩展性和数据冗余很有帮助。

### Ubuntu 安装

> 下载 & 解压  
> sudo wget http://download.redis.io/releases/redis-3.2.6.tar.gz  
> sudo tar -zxvf redis-3.2.6.tar.gz

> 安装  
> sudo make
> sudo make install

> 配置  
> redis-server /etc/redis/redis.conf # 可修改配置  
> redis-cli -p 6379

### windows 安装

> http://www.cnblogs.com/jaign/articles/7920588.html  
> 下载安装: https://github.com/MicrosoftArchive/redis/releases  
> 
安装完毕后，需要先做一些设定工作，以便服务启动后能正常运行。使用文本编辑器，这里使用Notepad++，打开Redis服务配置文件。  
注意：不要找错了，通常为**redis.windows-service.conf**，而不是redis.windows.conf。后者是以非系统服务方式启动程序使用的配置文件。


### Redis 配置

1. 配置端口号  
port 6379

2. 配置远程访问    
bind 192.168.80.103

3. 配置快照  
save 900 1
save 300 10
save 60 10000

4. 配置密码  
requirepass foobared

5. 后台运行  
默认情况，Redis 不是在后台运行，需要把 redis 放在后台运行  
vim /usr/local/redis/etc/redis.conf  
将 daemonize 的值改为yes  

6. 使用config set 命令来修改配置
127.0.0.1:6379> config set loglevel 'notice'

### Redis 启动/停止/重启 

> /etc/init.d/redis-server start[stop/restart]    


> redis-cli -h 127.0.0.1 -p 6379 shutdown



