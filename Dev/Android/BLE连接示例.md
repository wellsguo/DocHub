[详解 BLE 连接建立过程](https://blog.csdn.net/iini01/article/details/80147232)

- 同一款手机，为什么跟某些设备可以连接成功，而跟另外一些设备又连接不成功？

- 同一个设备，为什么跟某些手机可以建立连接，而跟另外一些手机又无法建立连接？

- 同一个手机，同一个设备，为什么他们两者有时候连起来很快，有时候连起来又很慢？

- Master 是什么？Slave 又是什么？

- 什么又是 Connection event 和 Slave latency ？

希望这篇文章能帮助你回答上述问题。

## BLE 连接示例

假设我们有一台 `手机A`（以安卓手机为例），一个 `设备B`（设备名称：Nordic_HRM），如下所示，我们可以通过安卓设置菜单里面的蓝牙界面，让两者连接起来。

1. 打开安卓设置菜单

2. 选择“蓝牙”条目

3. 打开蓝牙

4. 等待系统搜索结果，不出意外的话，设备“Nordic_HRM”会出现在结果列表中

5. 点击“Nordic_HRM”，手机将与此设备建立连接

   

![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002027071-1762450998.png)



上述即为大家直观感受到的 `连接`。那么 `手机` 要与 `设备Nordic_HRM` 建立连接，具体包含哪些流程？他们为什么可以连接成功？下面给大家一一道来。

## 广播（advertising）

在手机跟设备 B 建立连接之前，`设备B` 需要先进行广播，即设备 B（Advertiser）不断发送如下广播信号，`t` 为广播间隔。每发送一次广播包，我们称其为一次 `广播事件（advertising event）`，因此 `t`也称为广播事件间隔。虽然图中广播事件是用一根线来表示的，但实际上广播事件是有一个持续时间的，蓝牙芯片只有在广播事件期间才打开射频模块，这个时候功耗比较高，其余时间蓝牙芯片都处于 `idle` 状态，因此平均功耗非常低，以 `Nordic nRF52810` 为例，每 `1秒` 钟发一次广播，平均功耗不到 `11uA`。



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002154131-174494960.png)

> Advertiser 广播示意图



上面只是一个概略图，按照蓝牙 spec，实际上每一个广播事件包含三个广播包，即分别在 `37/38/39` 三个通道上同时广播相同的信息，即真正的广播事件是下面这个样子的。



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002230342-2145438133.png)

> Advertiser 广播示意图



`设备 B` 不断发送广播信号给 `手机（Observer）`，如果手机不开启扫描窗口，手机是收不到设备 B 的广播的，如下图所示，不仅手机要开启射频接收窗口，而且只有手机的射频接收窗口跟广播发送的发射窗口匹配成功，手机才能收到设备 B 的广播信号。由于这种匹配成功是一个概率事件，因此 `手机扫到设备 B 也是一个概率事件`，也就是说，手机有时会很快扫到设备 B，比如只需要一个广播事件，手机有时又会很慢才能扫到设备 B，比如需要 10 个广播事件甚至更多。



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002311031-42119225.png)

> 广播匹配示意图

## 建立连接（connection）

根据蓝牙 spec 规定，Advertiser 发送完一个广播包之后 150us（T_IFS），Advertiser 必须开启一段时间的射频 `Rx 窗口`，以接收来自 Observer 的数据包。Observer 就可以在这段时间里给 Advertiser 发送连接请求。如下图所示，手机在第三个广播事件的时候扫到了设备 B，并发出了连接请求 conn_req。



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002402732-1616456526.png)

> Observer 与 Advertiser 建立连接示意图



上图的交互流程比较粗略，为此我们引入下图，以详细描述连接建立过程。



![图 5：连接建立过程](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002512648-481754524.png)

> Observer 与 Advertiser 建立连接示意图



> 注：图中 `M` 代表手机，`S` 代表设备 B，`M->S` 表示手机将数据包发给设备 B，即手机开启 `Tx` 窗口，设备 B 开启 `Rx` 窗口；`S->M` 正好相反，表示设备 B 将数据包发给手机，即设备 B 开启 `Tx` 窗口，手机开启 `Rx` 窗口。

如图所示，手机在收到 A1 广播包 ADV_IND 后，以此为初始锚点（这个锚点不是连接的锚点），`T_IFS` 后给 Advertiser 发送一个 `connection request 命令`，即 A2 数据包，告诉 Advertiser 我将要过来连你，请做好准备。Advertiser 根据 connect_req 命令信息做好接收准备，connect_req 包含如下关键信息：

- Transmit window offset

- Transmit window size


![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002642874-286768904.png)

> connect_req 数据包完整定义



connect_req 其实是在告诉 Advertiser，手机将在 `Transmit Window` 期间发送第一个`同步包（P1）`给你，请在这段时间里把你的射频接收窗口打开。设备 B 收到 P1 后，`T_IFS` 时间后将给手机回复`数据包 P2`。一旦手机收到数据包 P2，连接即可认为建立成功。后续手机将以 P1 为锚点（原点），`Connection Interval `为周期，周期性地给设备 B 发送 Packet，Packet 除了充当数据传送功能，它还有如下两个非常重要的功能：

- 同步手机和设备的时钟，也就是说，设备每收到手机发来的一个包，都会把自己的时序原点重新设置，以跟手机同步。

- 告诉设备你现在可以传数据给我了。连接成功后，BLE 通信将变成主从模式，因此把连接发起者（手机）称为 `Master` 或者 `Central`，把被连接者（之前的 Advertiser）称为 `Slave` 或者 `Peripheral`。BLE 通信之所以为主从模式，是因为 Slave 不能“随性”给 Master 发信息，它只有等到 Master 给它发了一个 packet 后，然后才能把自己的数据回传给 Master。

## 连接失败

有如下几种典型的连接失败情况：

- 如果 Slave 在 transmit window 期间没有收到 Master 发过来的 P1，那么连接将会失败。此时应该排查 Master 那边的问题，看看 Master 为什么没有在约定的时间把 P1 发出来。
- 如果 Master 在 transmit window 期间把 P1 发出来了，也就是说 Master 按照 connect_req 约定的时序把 P1 发出来了，但 Slave 没有把 P2 回过去，那么连接也会失败。此时应该排查 Slave 这边的问题，看一看 Slave 为什么没有把 P2 回过去。
- 如果 Master 把 P1 发出来了，Slave 也把 P2 回过去了，此时主机还是报连接失败，这种情况有可能是 Master 软件有问题，需要仔细排查 Master 的软件。
- 还有一种比较常见的连接失败情况：空中射频干扰太大。此时应该找一个干净的环境，比如屏蔽室，排除干扰后再去测试连接是否正常。

## Connection events

连接成功后，Master 和 Slave 在每一个 `connection interval` 开始的时候，都必须交互一次，即 Master 给 Slave 发一个包，Slave 再给 Master 发一个包，整个交互过程称为一个 `connection event`。蓝牙芯片只有在 `connection event` 期间才把射频模块打开，此时功耗比较高，其余时间蓝牙芯片都是处于 idle 状态的，因此蓝牙芯片平均功耗就非常低。以 Nordic nRF52810 为例，每 1 秒钟 Master 和 Slave 通信 1 次，平均功耗约为 6 微安左右。Master 不可能时时刻刻都有数据发给 Slave，所以 Master 大部分时候都是发的空包（empty packet）给 Slave。同样 Slave 也不是时时刻刻都有数据给 Master，因此 Slave 回复给 Master 的包大部分时候也是空包。另外在一个 connection event 期间，Master 也可以发多个包给 Slave，以提高吞吐率。综上所述，连接成功后的通信时序图应该如下所示：



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002708393-419602791.png)

> 连接成功后的通信时序图（每个 connection event 只发一个包）



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002818335-1761917951.png)

> 连接成功后的通信时序图（ connection event 可能发多个包）



![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430002837207-145463955.png)

> connection event 细节图

## Slave latency

在 `connection event 细节图` 中出现了 `Slave latency`（Slave latency = 2），那么什么叫 `Slave latency`？

如前所述，在每一个 connection interval 开始的时候，Master 和 Slave 必须交互一次，哪怕两者之间交互的是 empty packet（空包），但如果 Slave 定义了 Slave latency，比如 Slave latency = 9，此时 Slave 可以每 9 个 connection interval 才回复一次 Master，也就是说 Slave 可以在前面 8 个 connection interval 期间一直睡眠，直到第 9 个 connection interval 到来之后，才回复一个 packet 给 Master，这样将大大节省 Slave 的功耗，提高电池续航时间。当然如果 Slave 有数据需要上报给 Master，它也可以不等到第 9 个 connection interval 才上报，直接像正常情况进行传输即可，这样既节省了功耗，又提高了数据传输的实时性。

## GAP 层角色总结

对上面提到的手机和设备 B，在 BLE 通信过程中，随着时间的推移，他们的状态在发生变化，两者的关系也在发生变化，为此蓝牙 spec 根据不同的时间段或者状态给手机和设备 B 取不同的名字，即 GAP 层定义了如下角色：

- Advertiser。 发出广播的设备

- Observer 或者 scanner。可以扫描广播的设备

- Initiator。能发起连接的设备

- Master 或者 Central。连接成功后的主设备，即主动发起 packet 的设备

- Slave 或者 Peripheral。连接成功后的从设备，即被动回传 packet 的设备



以时间为线索把 Observer，Initiator 和 Central 串起来了，其实这三个角色是相互独立的，也就是说一个设备可以只支持 Observer 角色，而不支持 Initiator 和 Central 角色。同样， 也把 Advertiser 和 Peripheral 串起来了，其实 Advertiser 和 Peripheral 也是相互独立的，即一个设备可以只作为 Advertiser 角色，而不支持 Peripheral 角色。


![](https://images2018.cnblogs.com/blog/1366713/201804/1366713-20180430003005175-1508520545.png)

>  GAP 层角色

```
版权声明：本文为CSDN博主「iini」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/iini01/article/details/80147232
```
