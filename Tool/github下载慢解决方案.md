## github下载慢，轻松提速教程



### 获取 github 的IP地址
访问 [网站](https://www.ipaddress.com/) 依次获取以下三个网址的 IP

- github.com
- github.global.ssl.fastly.net
- codeload.github.com




```
# 这是我获取的IP
192.30.253.113  github.com
151.101.25.194 github.global.ssl.fastly.net
192.30.253.121 codeload.github.com
```

### hosts 文件添加 IP 映射

```
192.30.253.113  github.com
151.101.25.194 github.global.ssl.fastly.net
192.30.253.121 codeload.github.com
```


## Windows 系统
hosts 文件路径

> C:\Windows\System32\drivers\etc\hosts 

添加上面查询到的 IP 到 hosts 文件中

### 刷新DNS

```
ipconfig /flushdns
```

恭喜完成！！！

## Linux 系统

### 1. 编辑 hosts 文件

```
sudo vim /etc/hosts

```

插入 ip 映射保存退出

### 2.重启网络服务

```
sudo /etc/init.d/networking restart1
```
恭喜完成！！！
