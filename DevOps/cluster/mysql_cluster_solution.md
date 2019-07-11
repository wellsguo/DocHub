本篇文章紀錄安裝 Percona XtraDB Cluster (簡稱 PXC) 及搭配 HAProxy 做分散流量系統，其實在業界已經很常看到 HAProxy + MySQL Cluster Database 解決方案，HAProxy 幫您解決負載平衡，並且偵測系統是否存活，管理者也就不用擔心 MySQL 服務是否會掛掉。本篇會著重於 HAProxy 設定部份，並且紀錄每一步安裝步驟。之前本作者寫過一篇 Galera Cluster for MySQL Multi-master Replication，也可以參考。今天測試系統都會以 CentOS 為主，各位讀者可以直接開 Amazone EC2 來測試，測試完成再關閉即可。

## 安裝 Percona XtraDB Cluster
我們會使用官方 Percona 及 EPEL repositories 進行軟體安裝，底下是 Yum 安裝步驟

```shell
$ yum -y install Percona-XtraDB-Cluster-server Percona-XtraDB-Cluster-client Percona-Server-shared-compat percona-xtrabackup
```

如果系統已經有安裝過 MariaDB + Galera，請務必先移除套件

完成安裝 PXC 套件後，接著設定 my.cnf 設定檔

```conf
[mysqld]
server_id=1
wsrep_provider=/usr/lib64/libgalera_smm.so
wsrep_cluster_address="gcomm://"
wsrep_sst_auth=username:password
wsrep_provider_options="gcache.size=4G"
wsrep_cluster_name=Percona
wsrep_sst_method=xtrabackup
wsrep_node_name=db_01
wsrep_slave_threads=4
log_slave_updates
innodb_locks_unsafe_for_binlog=1
innodb_autoinc_lock_mode=2
```

再開啟第 2 台或第 3 台 PXC 服務的時候，務必確認第 1 台已經正確開啟成功。上面設定檔是針對第 1 台做設定，之後新增 Node，請務必修改 `wsrep_cluster_address` 填上你想要 Join 的 *Cluster Server IP Address*，另外每台的 `server_id` 及 `wsrep_node_name` 也會不同，請務必注意

##### 第 2 台設定值

```
server_id=2
wsrep_cluster_address=gcomm://192.168.1.100 # replace this with the IP of your first node
wsrep_node_name=db_02
```

##### 第 3 台設定值

```
server_id=2
wsrep_cluster_address=gcomm://192.168.1.100 # replace this with the IP of your first node
wsrep_node_name=db_03
```

根據 State Snapshot Transfer (簡稱 SST)，我們使用 Xtrabackup，當新的 Node 連上時，就會開始複製資料到新的 Node 上，成功複製完成，可以看到底下 Log 訊息

```
140117 11:56:05 [Note] WSREP: Flow-control interval: [28, 28]
140117 11:56:05 [Note] WSREP: Shifting OPEN -> PRIMARY (TO: 678691)
140117 11:56:05 [Note] WSREP: State transfer required:
        Group state: 28e87291-da41-11e2-0800-34a03cad54a7:678691
        Local state: 28e87291-da41-11e2-0800-34a03cad54a7:678684
140117 11:56:05 [Note] WSREP: New cluster view: global state: 28e87291-da41-11e2-0800-34a03cad54a7:678691, view# 33: Primary, number of nodes: 3, my index: 1, protocol version 2
140117 11:56:05 [Warning] WSREP: Gap in state sequence. Need state transfer.
140117 11:56:07 [Note] WSREP: Running: 'wsrep_sst_xtrabackup --role 'joiner' --address '122.146.119.102' --auth 'username:password' --datadir '/var/lib/mysql/' --defaults-file '/etc/my.cnf' --parent '965''
WSREP_SST: [INFO] Streaming with tar (20140117 11:56:07.517)
WSREP_SST: [INFO] Using socat as streamer (20140117 11:56:07.519)
WSREP_SST: [INFO] Evaluating socat -u TCP-LISTEN:4444,reuseaddr stdio | tar xfi - --recursive-unlink -h; RC=( ${PIPESTATUS[@]} ) (20140117 11:56:07.531)
140117 11:56:07 [Note] WSREP: Prepared SST request: xtrabackup|122.146.119.102:4444/xtrabackup_sst
140117 11:56:07 [Note] WSREP: wsrep_notify_cmd is not defined, skipping notification.
140117 11:56:07 [Note] WSREP: Assign initial position for certification: 678691, protocol version: 2
140117 11:56:07 [Note] WSREP: Prepared IST receiver, listening at: tcp://122.146.119.102:4568
140117 11:56:07 [Note] WSREP: Node 1 (db_01) requested state transfer from '*any*'. Selected 0 (db_02)(SYNCED) as donor.
140117 11:56:07 [Note] WSREP: Shifting PRIMARY -> JOINER (TO: 678692)
140117 11:57:36 [Note] WSREP: Synchronized with group, ready for connections
140117 11:57:36 [Note] WSREP: wsrep_notify_cmd is not defined, skipping notification.
140117 11:57:36 [Note] WSREP: 1 (db_02): State transfer from 0 (db_01) complete.
140117 11:57:36 [Note] WSREP: Member 1 (db_02) synced with group.
```

最後我們可以透過 MySQL Status 來看看是否有建立成功

```
mysql> show global status like 'wsrep_cluster_size';
+--------------------+-------+
| Variable_name      | Value |
+--------------------+-------+
| wsrep_cluster_size | 3     |
+--------------------+-------+
1 row in set (0.00 sec)
```

看到 wsrep_cluster_size 出現正確的 Server 數量，就代表設定成功。

## 設定 HAProxy 負載平衡

上述完成了 3 台 Cluster 設定，接著所有的 Application 服務都需要直接跟此 Cluster 溝通，為了完成此需求，我們必須將 HAProxy 安裝在其中一台伺服器來做負載平衡，今天會介紹兩種設定方式，第一種是採用 round robin 方式，意思就是說所有的 Application 都可以連上並且寫入資料到三台機器，這狀況其實沒有錯誤，但是如果同時寫入三台機器，難免會出現 optimistic locking 而產生 rollback，如果可以確定不會產生 conflict，其實這方案是不錯的。第2種設定方式就是只寫入單一 Node，但是可以讀取三台機器，也就是 insert, update 都是在同一台 Node 完成，所以 Application 不用擔心會產生 rollback 情形。第1種設定在大部份的狀況底下都是可以運作很好的，所以其實也不用擔心。

底下是 /etc/haproxy/haproxy.cfg 設定

```
frontend stats-front
bind *:8080
mode http
default_backend stats-back

frontend pxc-front
bind *:3307
mode tcp
default_backend pxc-back

frontend pxc-onenode-front
bind *:3308
mode tcp
default_backend pxc-onenode-back

backend stats-back
mode http
balance roundrobin
stats uri /haproxy/stats
stats auth username:password

backend pxc-back
mode tcp
balance leastconn
option httpchk
server c1 192.168.1.100:3306 check port 9200 inter 12000 rise 3 fall 3
server c2 192.168.1.101:3306 check port 9200 inter 12000 rise 3 fall 3
server c3 192.168.1.102:3306 check port 9200 inter 12000 rise 3 fall 3

backend pxc-onenode-back
mode tcp
balance leastconn
option httpchk
server c1 192.168.1.100:3306 check port 9200 inter 12000 rise 3 fall 3
server c2 192.168.1.101:3306 check port 9200 inter 12000 rise 3 fall 3 backup
server c3 192.168.1.102:3306 check port 9200 inter 12000 rise 3 fall 3 backup
```

從上述設定，可以看到我們定義了 3 個 frontend-backend，其中 stats-front 是 HAProxy Status Page，另外兩組則是針對 PXC 設定。看到此設定，可以知道系統會 Listen 3307 及 3308 兩個 port，其中 3308 會讓 App 使用一台 PXC Node 而已，此設定可以避免因為 optimistic locking 而產生 rollbacks，如果 Node 掛點，則會啟動其他 Node。然而如果是連接 3307 port，系統會直接對3台 node 寫入或讀取，我們使用 leastconn 取代 round robin，這代表著 HAProxy 會偵測所有機器，並且取得現在連線數目最少的 Node 來給下一個連線。最後 stats-front 是顯示 HAProxy 偵測及連線狀態，請務必設定帳號密碼。

完成設定，如何偵測 MySQL Server 是否存活，靠著就是 9200 port，透過 Http check 方式，讓 HAProxy 知道 PXC 狀態，安裝完 PXC 後，可以發現多了 clustercheck 指令，我們必須先給 clustercheckuser 使用者帳號密碼

```
# Grant privileges required:
$ GRANT PROCESS ON *.* TO 'clustercheckuser'@'localhost' IDENTIFIED BY 'clustercheckpassword!';
```

此 clustercheck 指令會在 Local 執行 SHOW STATUS LIKE 'wsrep_local_state' MySQL 指令，回傳值為 200 或 503，指令確定成功執行，最後步驟就是透過 xinetd 產生 9200 port 的服務。底下先安裝 xinetd 服務

```
$ yum -y install xinetd
```

產生 mysqlchk 設定

```
# default: on
# description: mysqlchk
service mysqlchk
{
# this is a config for xinetd, place it in /etc/xinetd.d/
    disable = no
    flags = REUSE
    socket_type = stream
    port = 9200
    wait = no
    user = nobody
    server = /usr/bin/clustercheck
    log_on_failure += USERID
    only_from = 0.0.0.0/0
    # recommended to put the IPs that need
    # to connect exclusively (security purposes)
    per_source = UNLIMITED
}
```

上面步驟全部成功，請打開 URL 輸入 HAProxy Status 頁面，看到底下狀態，就是代表設定成功

![](http://www.flickr.com/photos/appleboy/12029396533/)

