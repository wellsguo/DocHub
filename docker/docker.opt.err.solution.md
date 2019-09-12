## docker 删除镜像时报错解决办法

### [报错信息](https://www.cnblogs.com/wholj/p/10329201.html)

```shell
root@kvm ~]# docker rmi 4950a54ede5a
Error response from daemon: conflict: unable to delete 4950a54ede5a (must be forced) - image is being used by stopped container 834789a17497
```
### 报错原因
`image is being used by stopped container 834789a17497`，即要删除的该镜像,被容器 `834789a17497` 所引用了。

### 解决办法

- 执行 `docker ps -a` 查看所有容器记录（包括未运行的容器），并查看那些容器是使用了这个要删除的镜像：

- 执行命令 `docker rm <container_ID>` 删除这两个容器

```shell
[root@kvm ~]# docker rm 834789a17497
834789a17497
[root@kvm ~]# docker rm 63b699a2cbb6
63b699a2cbb6
```

- 执行命令 `docker rmi <image_ID>` 删除镜像

```shell
[root@kvm ~]# docker rmi 4950a54ede5a
Untagged: www.wholj.com:7.5
Deleted: sha256:4950a54ede5a5c0da704c6f74e6bcc43d440e83260b0752a926325035435a7dc
Deleted: sha256:788edba9eaa8ade63d8ba9d5747281c5da2b34b12a6c80f4dffd8ad9e05f68c1
```

---

### [报错信息](http://www.ibloger.net/article/3217.html)

```
Error response from daemon: conflict: unable to delete 6ec9a5a0fc9f (cannot be forced) - image has dependent child images
```

### 报错原因
原因是有另外的 image FROM 了这个 image，

### 解决办法
可使用下面的命令列出所有在指定 image 之后创建的 image 的父 image

```shell
docker image inspect --format='{{.RepoTags}} {{.Id}} {{.Parent}}' $(docker image ls -q --filter since=xxxxxx)
```
其中 xxxxxx 是报错 image 的 id，在文章开头的例子中就是 6ec9a5a0fc9f。从列表中查找到之后就可以核对并删除这些 image。

#### 1、查看我的镜像列表

```Bash
➜  ~ docker images -a
REPOSITORY                       TAG                 IMAGE ID            CREATED             SIZE
<none>                           <none>              b707620d204c        8 hours ago         179MB
tingfeng/dockerfile_build_demo   latest              6586e000b464        8 hours ago         179MB
<none>                           <none>              54f305491871        10 hours ago        122MB
<none>                           <none>              97ea9f11c94f        10 hours ago        81.2MB
tingfeng/commit_test             latest              58fac7144497        31 hours ago        234MB
tomcat                           latest              61205f6444f9        2 weeks ago         467MB
ubuntu                           latest              113a43faa138        2 weeks ago         81.2MB
nginx                            latest              cd5239a0906a        2 weeks ago         109MB
hello-world                      latest              e38bc07ac18e        2 months ago        1.85kB
```

#### 2、删除none的镜像（删不掉）

```Bash
➜  ~ docker rmi b707620d204c
Error response from daemon: conflict: unable to delete b707620d204c (cannot be forced) - image has dependent child images
➜  ~ docker rmi 97ea9f11c94f
Error response from daemon: conflict: unable to delete 97ea9f11c94f (cannot be forced) - image has dependent child images
➜  ~ docker rmi -f 54f305491871
Error response from daemon: conflict: unable to delete 54f305491871 (cannot be forced) - image has dependent child images
```

#### 3、查找出所有在指定 image 之后创建的 image 的父 image，本示例看得出是同一个依赖镜像 tingfeng/dockerfile_build_demo

```Bash
➜  ~ docker image inspect --format='{{.RepoTags}} {{.Id}} {{.Parent}}' $(docker image ls -q --filter since=b707620d204c)
[tingfeng/dockerfile_build_demo:latest] sha256:6586e000b464654f420b0aa9cf6c3c61cc29edfbbe7cc5cb5d6e0fe037efaf87 sha256:b707620d204ca475f13394b14614e1f2fde986931c925cd8cc8e8bb3de7debe3

➜  ~ docker image inspect --format='{{.RepoTags}} {{.Id}} {{.Parent}}' $(docker image ls -q --filter since=54f305491871)
[tingfeng/dockerfile_build_demo:latest] sha256:6586e000b464654f420b0aa9cf6c3c61cc29edfbbe7cc5cb5d6e0fe037efaf87 sha256:b707620d204ca475f13394b14614e1f2fde986931c925cd8cc8e8bb3de7debe3

➜  ~ docker image inspect --format='{{.RepoTags}} {{.Id}} {{.Parent}}' $(docker image ls -q --filter since=97ea9f11c94f)
[tingfeng/dockerfile_build_demo:latest] sha256:6586e000b464654f420b0aa9cf6c3c61cc29edfbbe7cc5cb5d6e0fe037efaf87 sha256:b707620d204ca475f13394b14614e1f2fde986931c925cd8cc8e8bb3de7debe3
```
#### 4、删除关联的依赖镜像，关联的none镜像也会被删除

```Bash
➜  ~ docker rmi 6586e000b464
Untagged: tingfeng/dockerfile_build_demo:latest
Deleted: sha256:6586e000b464654f420b0aa9cf6c3c61cc29edfbbe7cc5cb5d6e0fe037efaf87
Deleted: sha256:b707620d204ca475f13394b14614e1f2fde986931c925cd8cc8e8bb3de7debe3
Deleted: sha256:c241c7f781a3176d395b38a7e96eb2e0b7e031e622ad9d14eaa9098de1a063d1
Deleted: sha256:54f305491871f5609295cd6c59f304401761c7fa96bdda8a74968358c54ba402
Deleted: sha256:be4d80c4407bde1fe700983ad805a0237a148d7af04e8bf2197fc040ae654acb
Deleted: sha256:97ea9f11c94fb8f76288361e37f884d639c6ea918bc6142feee2409e7ff43791
```
#### 5、再次查看镜像列表

```Bash
➜  ~ docker images -a
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
tingfeng/commit_test   latest              58fac7144497        31 hours ago        234MB
tomcat                 latest              61205f6444f9        2 weeks ago         467MB
ubuntu                 latest              113a43faa138        2 weeks ago         81.2MB
nginx                  latest              cd5239a0906a        2 weeks ago         109MB
hello-world            latest              e38bc07ac18e        2 months ago        1.85kB
```

#### 其他操作

```Bash
# 停止所有容器
➜  ~ docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker stop

# 删除所有容器
➜  ~ docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker rm

# 删除所有none容器
➜  ~ docker images|grep none|awk '{print $3 }'|xargs docker rmi
```