### 修改/配置环境变量
---
1. 修改或配置当前用户的环境变量
```bash
vim ~/.bashrc  
export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib  
source ~/.bashrc
```  

2. 修改或配置系统的环境变量
```bash 
sudo vim /etc/profile   
export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib  
source /etc/profile
```

1. 临时修改环境变量
>export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib
