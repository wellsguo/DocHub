## 一、Docker 安装 GitLab

### 1. 下载镜像

```bash
gitlab/gitlab-ce:latest            # 当前gitlab最新版本为10.0.4
```

### 2. 在服务器上创建目录

```bash
mkdir -p /home/work/ins/conf
mkdir -p /home/work/ins/logs
mkdir -p /home/work/ins/data/gitlab
```

### 3. 将 gitlab-rails.tar.gz 包解压放在 `/home/work/ins/data/gitlab` 目录下  

> 为了汉化，如果不汉化可以忽略这一步

### 4. 创建容器启动脚本
```shell
sudo docker stop gitlab && sudo docker rm gitlab
sudo docker run -d \
        -p 2222:22 \
        -p 8888:80 \
        -p 8443:443 \
        -v /etc/localtime:/etc/localtime:ro \
        -v /home/work/ins/conf/gitlab:/etc/gitlab \
        -v /home/work/ins/logs/gitlab:/var/log/gitlab \
        -v /home/work/ins/data/gitlab/data:/var/opt/gitlab \
        -v /home/work/ins/data/gitlab/gitlab-rails:/opt/gitlab/embedded/service/gitlab-rails \
        -h gitlab \
        --name gitlab \
        gitlab/gitlab-ce:latest
```

### 5.登录验证

登录

登录地址：http://server:8888

输入分配的个人帐号和密码

## 二、管理员用户登录基本操作教程

### 1. 创建普通用户

![wpsB8A1.tmp](http://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120203209-325849472.jpg)

填写正确的邮箱，用户通过邮箱可以重置密码（邮箱中的链接需要该IP端口）

### 2. 创建空项目

![wpsB8A2.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120204693-21424732.jpg)

### 3. 指定一个开发人员权限用户和一个访客权限用户

![wpsB8A3.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120205990-55109058.jpg)

![wpsB8B3.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120206896-1943764755.jpg)

## 三、开发人员基本操作

### 1. 以开发人员帐号密码在客户端 clone 项目

![wpsB8B4.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120207787-1971299956.jpg)

### 2. 添加文件并 push 到项目中

![wpsB8B5.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120212381-1306511292.jpg)

推送失败，原因是主分支是默认被保护的，只有项目创建者或者是主程序员权限的用户才能推送，那就以root用户先push上去吧。

![wpsB8B6.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120215006-160209836.jpg)

![wpsB8B7.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120224021-661476600.jpg)

果然没有报错并提交到服务器了。

### 3. 开发人员创建dev分支并切换到dev分支

![wpsB8B8.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120225396-2105200224.jpg)

### 4. 开发人员在 dev 分支 coding 代码合并 master 分支后以 root 用户提交到项目中

![wpsB8B9.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120226334-151196640.jpg)

![wpsB8BA.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120227099-1042903460.jpg)

![wpsB8CB.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120227818-163300518.jpg)

### 5. 开发人员创建 dev1 分支，并将分支以开发用户提交到项目中

![wpsB8CC.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120228881-171035472.jpg)

![wpsB8CD.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120229631-1973399909.jpg)

![wpsB8CE.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120230381-1577890118.jpg)

查看分支：git branch

创建分支：git branch <name>

切换本地分支：git checkout <name>

切换远程分支：git checkout -b <localname> origin/<name>

创建+切换分支：git checkout -b <name>

合并某分支到当前分支：git merge <name>

删除本地分支：git branch -d <name>

删除远程分支：git push origin :<name>

## 四、访客的权限验证

### 1. clone 代码到本地，切换分支查看代码

![wpsB8CF.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120231271-1061333702.jpg)

### 2. 编写代码并提交

![wpsB8D0.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120232568-504541557.jpg)

![wpsB8D1.tmp](https://images2017.cnblogs.com/blog/1059167/201710/1059167-20171020120233849-77743608.jpg)

提示push失败，没有权限
