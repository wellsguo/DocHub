## 物联网中的无线通信技术主要有哪些？

### 概述

无线技术正在迅速发展，并在人们的生活中发挥越来越大的作用。而随着无线应用的增长，各种技术和设备也会越来越多，也越来越依赖于无线通信技术。本文盘点下物联网中无线通信主要的技术。

### 无线通信技术分类

#### I 美国通信委员会(FCC)分类

2015年，美国通信委员会 (FCC, Federal Communications Commission) 技术咨询委员会 (TAC，Technological Advisory Council) 网络安全工作组在一份白皮书中提到了将物联网通信技术分成了以下四类：

- Mobile/WAN，Wide Area Network - 移动广域网络，覆盖范围大

- WAN，Wide Area Network - 广域网，覆盖范围大，非移动技术

- LAN，Local Area Network - 局域网，覆盖范围相对较小，如住宅、建筑或园区

- PAN，Personal Area Network - 个域网，覆盖范围从几厘米到几米不等

##### 主要的无线技术及分类如下表所示：
![](http://www.iotworld.com.cn/FileUpLoadSavePath/2017-11/cf87287f7e4eb8ee.jpg)

#### FCC TAC 通信技术分类

不知为何，FCC TAC将Sigfox归入了LAN，而LoRaWAN归入了WAN。Sigfox与LoRaWAN都同属于LPWAN领域中的窄带技术，都是可以广域覆盖。Weightless SIG在LPWAN领域中主推的将会是Weightless-P。NB-IoT也没有列入其中。新的技术在不断出现，也在不断地重塑物联网市场的格局。

#### KEYSIGHT分类

在KEYSIGHT的一份PPT中《Low Power Wide Area Networks,NB-IoT and the Internet of Things》，将IoT无线技术做了比较详细的划分，如下图所示：

![](http://www.iotworld.com.cn/FileUpLoadSavePath/2017-11/ed55f61bb25a7391.jpg)

###### 相关术语如下：

　　NFC，Near Field Communication - 近场通信

　　WPAN， Wireless Personal Area Network - 无线个域网

　　WHAN，Wireless Home Area - 无线家用网络

　　WFAN，Wireless Field (or Factory) Area - 无线现场(或工厂)域网络

　　WLAN，Wireless Local Area - 无线局域网

　　WNAN，Wireless Neighbourhood Area - 无线邻域网

　　WWAN，Wireless Wide Area - 无线广域网

　　LPWAN，Low Power Wide Area Network - 低功耗广域网

　　KEYSIGHT按照10cm、5km、100km通信范围或距离，将无线通信技术分成了三大类。
  
  ##### 近距离和远距离

从上面的分类可以看出无线通信技术基本都还是以覆盖范围或通信的距离来分类的。小编稍加整理，将通信技术分成近距离和远距离通信技术两大类，如下图所示：

![](http://www.iotworld.com.cn/FileUpLoadSavePath/2017-11/0b3e710383c54e12.jpg)

窄带广域是这两年发展最为迅速的领域，NB-IoT和LoRa在中国的网络化建设正如火如荼地进行。近距离的无线通信技术相对成熟，产业链比较完善。

### II 国际电机电子工程学会(IEEE)

国际电机电子工程学会定义了一些标准，如关于局域网和城域网的IEEE 802系列标准，也成为了一些物联网技术的基础。这些主要的标准有：

　　IEEE 802.11 Wireless LAN (WLAN) & Mesh (Wi-Fi certification)

　　IEEE 802.15 Wireless PAN

　　IEEE 802.15.1 Bluetooth certification

　　IEEE 802.15.3 High-Rate wireless PAN (e.g., UWB, etc.)

　　IEEE 802.15.4 Low-Rate wireless PAN (e.g., ZigBee, WirelessHART, MiWi, etc.)

　　IEEE 802.15.6 Body area network

![](http://www.iotworld.com.cn/FileUpLoadSavePath/2017-11/5552ee202d8e844e.jpg)

##### IEEE标准

　　IEEE 802.11 定义了用于在900MHz、2.4GHz、3.6GHz、5GHz和60GHz频段实现无线局域网(WLAN)计算机通信的一组媒体访问控制(MAC)和物理层(PHY)规范，也是现在无线局域网通用的标准。

　　IEEE 802.15 规定了无线个人区域网络(WPAN)标准，有10个主要的领域。

　　IEEE 802.11ah ，又称为&rdquo;Wi-Fi HaLow&ldquo;，是定义在900MHz免授权频段的WLAN网络。相比2.4GHz和5GHz的Wi-Fi，功耗更低，距离更远。11ah可用于包括大规模传感器网络的各种应用。

　　IEEE 802.15.4c ，中国的WPAN，增加了新的RF频谱规格：314-316 MHz, 430-434 MHz, 779-787 MHz

　　IEEE 802.11p ，这个通信协议主要用在车用电子的无线通信上。是在IEEE 802.11基础上的扩充延伸，主要面向智能运输系统(Intelligent Transportation Systems，ITS)的相关应用。

　　IEEE 802.15.4 是低速率无线个域网(LR-WPAN)的技术标准。 它是ZigBee、ISA100.11a，WirelessHART、MiWi和Thread等技术的基础，这些技术都通过开发在IEEE 802.15.4中未定义的上层进一步扩展了标准。 另外，它可以与6LoWPAN一起使用来定义上层。

## 结束语

对技术的分类不一而论，简单易于接受的是从通信距离或范围的角度分。有些无线通信技术又都是相对而存在的，如广域宽带和广域窄带、高速率和低速率，这些都是适应不同的应用需求而存在的。在选择物联网技术时，不仅仅考虑到距离，还有频段、功耗、数据速率、安全以及网络部署等因素。

## MORE
protocol | desc.
--|--
Zigbee|低速、中距、自组网、低功耗。
Bluetooth|中速、近距、点对点或自组网、低功耗。
WiFi|高速、星型、功耗高、距离中。
NFC|属于RFID技术，距离近。

