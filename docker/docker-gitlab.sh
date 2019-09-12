#!/bin/sh
# sudo docker stop gitlab && 
# sudo docker rm gitlab
sudo docker run      -d \
                 -p 2222:22 \
                 -p 8888:80 \
                 -p 8443:443 \
                 -v /etc/localtime:/etc/localtime:ro \
                 -v /home/guo/ENV/gitlab/conf/gitlab:/etc/gitlab \
                 -v /home/guo/ENV/gitlab/logs/gitlab:/var/log/gitlab \
                 -v /home/guo/ENV/gitlab/data/gitlab/data:/var/opt/gitlab \
                 -h gitlab \
                 --name gitlab \
                 gitlab/gitlab-ce:latest
