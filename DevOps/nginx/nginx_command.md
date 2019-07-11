## nginx 命令


### 启动
```
nginx -c /path/to/nginx.conf  
```

### 重启
```
nginx -s reload                 # 修改配置后重新加载生效  
nginx -s reopen                 # 重新打开日志文件   
nginx -t -c /path/to/nginx.conf # 测试nginx配置文件是否正确  
```
### 平滑重启
```
kill -HUP 主进程号
```

### 关闭
```
nginx -s stop  # 快速停止nginx  
nginx -s quit  # 完整有序的停止nginx  
```

### 其他停止方式  
```
ps -ef | grep nginx  
kill -QUIT 主进程号     # 从容停止Nginx  
kill -TERM 主进程号     # 快速停止Nginx  
pkill -9 nginx          # 强制停止Nginx  
```

