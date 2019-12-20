```shell
chmod 777 /home/nexus-data
```



```shell
ubuntu@ubuntu-VirtualBox:~/Development/nexus3$ sudo docker run -d -p 8081:8081 --name nexus -v /home/ubuntu/Development/nexus3/nexus-data:/nexus-data  sonatype/nexus3
51695688160feb6e286e3943e1866ced757276c44c2ab1910323629735205e34

```



```shell
ubuntu@ubuntu-VirtualBox:~/Development/nexus3$ sudo docker ps -a
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS                 PORTS                                                               NAMES
51695688160f        sonatype/nexus3           "sh -c ${SONATYPE_DI…"   23 seconds ago      Up 22 seconds          0.0.0.0:8081->8081/tcp                                              nexus
33983644aa1a        jenkins:latest            "/bin/tini -- /usr/l…"   6 weeks ago         Up 6 weeks             0.0.0.0:50000->50000/tcp, 0.0.0.0:9090->8080/tcp                    jenkins
f4eadd6f6951        gitlab/gitlab-ce:latest   "/assets/wrapper"        6 weeks ago         Up 6 weeks (healthy)   0.0.0.0:2222->22/tcp, 0.0.0.0:8080->80/tcp, 0.0.0.0:8443->443/tcp   gitlab
```



```shell
ubuntu@ubuntu-VirtualBox:~/Development/nexus3$ cd nexus-data/
ubuntu@ubuntu-VirtualBox:~/Development/nexus3/nexus-data$ ls
admin.password  blobs  cache  db  elasticsearch  etc  generated-bundles  instances  javaprefs  karaf.pid  keystores  lock  log  orient  port  restore-from-backup  tmp
ubuntu@ubuntu-VirtualBox:~/Development/nexus3/nexus-data$ cat admin.password
c7f56eba-bbb9-4f12-af17-ea4852d6de75ubuntu@ubuntu-VirtualBox:~/Development/nexus3/nexus-data$
```



nexus@kys

