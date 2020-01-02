这篇博客的作用是为了让小白朋友了解 andorid 蓝牙的一些基本概念,同时学习总结下目前我实际项目中用到的蓝牙库 BluetoothKit ,包括其优点 、基本使用，最后以库中的源码为基石深入探究这个优秀的蓝牙库的设计理念。

# 一 . 蓝牙基础知识

## 1.1 Ble 蓝牙的基本介绍

### 1.1.1 Ble 蓝牙介绍

Android 4.3（API Level 18）开始引入 Bluetooth Low Energy（BLE，**低功耗蓝牙**）的核心功能并提供了相应的 API， 应用程序通过这些 API 扫描蓝牙设备、查询 services、读写设备的 characteristics（属性特征）等操作。

Android BLE 使用的蓝牙协议是 GATT 协议，有关该协议的详细内容可以参见蓝牙官方文档或者这篇[博客](https://blog.csdn.net/u013378580/article/details/52891462)。以下我引用一张官网的图来大概说明 Android 开发中我们 用到的一些专业术语。（专业名词参考 1.2 节内容）

![蓝牙协议图.png](https:////upload-images.jianshu.io/upload_images/4948784-414eb976a894a071.png?imageMogr2/auto-orient/strip|imageView2/2/w/572/format/webp)

### 1.1.2 Android BLE 的相关系统 API

**Profile**

一个通用的规范，即 Ble 的蓝牙通讯协议，Ble 蓝牙的必须按照这个规范来收发数据。

**Service**

一个低功耗蓝牙设备可以定义许多 Service, Service 可以理解为**一个功能的集合**。设备中每一个不同的 Service 都有一个 128 bit 的 UUID 作为这个 Service 的独立标志。蓝牙核心规范制定了两种不同的 UUID，一种是基本的 UUID，一种是代替基本 UUID 的 16 位 UUID。所有的蓝牙技术联盟定义 UUID 共用了一个基本的 UUID(`0x0000xxxx-0000-1000-8000-00805F9B34FB`) ，为了进一步简化基本 UUID，每一个蓝牙技术联盟定义的属性有一个唯一的 16 位 UUID，以代替上面的基本 UUID 的‘x’部分。例如，心率测量特性使用 0X2A37 作为它的 16 位 UUID，因此它完整的 128 位 UUID 为` 0x00002A37-0000-1000-8000-00805F9B34FB`.

**BluetoothAdapter**

BluetoothAdapter 拥有**系统调用蓝牙基本的蓝牙操作**。例如，开启蓝牙`扫描` `连接`，使用已知的 MAC 地址 （BluetoothAdapter#getRemoteDevice）实例化一个 BluetoothDevice 用于连接蓝牙设备的操作等等。

**BluetoothDevice**

代表一个远程蓝牙设备。这个类可以让你连接所代表的蓝牙设备或者获取一些有关它的信息，例如它的名字，地址和绑定状态等等。

**RSSI**

Received Signal Strength Indication.用来标识搜索到的设备的信号强度值。

**BluetoothGatt**

这个类提供了 Bluetooth GATT 的基本功能。例如重新连接蓝牙设备，发现蓝牙设备的 Service 等等，是在一个中心设备（如手机）和外围设备（手环等 Ble 设备）之间建立的数据通道，通过调用 gatt 对象的一系列方法来操作蓝牙。

**UUID**

**一个 service 对应一个 UUID**

一蓝牙核心规范制定了两种不同的 UUID，一种是基本的 UUID，一种是代替基本 UUID 的 16 位 UUID。所有的蓝牙技术联盟定义 UUID 共用了一个基本的 UUID：0x0000xxxx-0000-1000-8000-00805F9B34FB

为了进一步简化基本 UUID，每一个蓝牙技术联盟定义的属性有一个唯一的 16 位 UUID，以代替上面的基本 UUID 的‘x’部分。例如，心率测量特性使用 0X2A37 作为它的 16 位 UUID，因此它完整的 128 位 UUID 为：0x00002A37-0000-1000-8000-00805F9B34FB

**BluetoothGattService**

一个低功耗蓝牙设备可以定义许多 Service, Service 可以理解为一个功能的集合。设备中每一个不同的 Service 都有一个 128 bit 的 UUID 作为这个 Service 的独立标志。
这一个类通过 BluetoothGatt#getService 获得，如果当前服务不可见那么将返回一个 null。这一个类对应上面说过的 Service。我们可以通过这个类的 getCharacteristic(UUID uuid) 进一步获取 Characteristic 实现蓝牙数据的双向传输。

**BluetoothGattCharacteristic**

在 Service 之下，又包括了许多的独立数据项，我们把这些**独立的数据项**称作 Characteristic。同样的，每一个 Characteristic 也有一个唯一的 UUID 作为标识符。在 Android 开发中，建立蓝牙连接后，我们说的通过蓝牙发送数据给外围设备就是往这些 Characteristic 中的 `Value` 字段写入数据；外围设备发送数据给手机就是监听这些 Charateristic 中的 `Value` 字段有没有变化，如果发生了变化，手机的 BLE API 就会收到一个监听的回调。

这个类对应上面提到的 Characteristic。通过这个类定义需要往外围设备写入的数据和读取外围设备发送过来的数据，这个类是中心设备和 BLE 设备之间数据通信的载体。

相当于一个数据类型，它包括一个 value 和 0~n 个 value 的描述（BluetoothGattDescriptor）

**BluetoothGattDescriptor**

描述符位于 Characteristic 之下,是对 Characteristic 的描述，包括范围、计量单位等

**Notification 和 Indication**

`Notification` 外围设备（硬件）设备给中心设备（手机）发送一个数据,无需接收方确认, 接收通知.

`Indication` 外围设备给中心设备（手机）发送一个数据,需要接收方确认。

二者关系类似于 TCP 协议和 UDP 协议，效率上来讲 Notification 比 Indication 要高。在蓝牙 API 中体现在 notify() 方法和 indicate()方法。

### 1.1.3 与传统蓝牙 ClassicBluetooth 的比较

#### 1.1.3.1 蓝牙模块分类

![蓝牙模块分类.png](https:////upload-images.jianshu.io/upload_images/4948784-6235457521a03817.png?imageMogr2/auto-orient/strip|imageView2/2/w/501/format/webp)

#### 1.1.3.2 BLE 和 CLASSIC 蓝牙的比较

**经典蓝牙模块（BT）**：泛指支持蓝牙协议在 4.0 以下的模块，一般用于数据量比较大的传输，如：语音、音乐、较高数据量传输等。经典蓝牙模块可再细分为：传统蓝牙模块和高速蓝牙模块。传统蓝牙模块在 2004 年推出，主要代表是支持蓝牙 2.1 协议的模块，在智能手机爆发的时期得到广泛支持。高速蓝牙模块在 2009 年推出，速率提高到约 24Mbps，是传统蓝牙模块的八倍，可以轻松用于录像机至高清电视、PC 至 PMP、UMPC 至打印机之间的资料传输。

**低功耗蓝牙模块（BLE）**：是指支持蓝牙协议 4.0 或更高的模块，也称为 BLE 模块（BluetoohLow EnergyModule），最大的特点是成本和功耗的降低，应用于实时性要求比较高，但是数据速率比较低的产品，如：遥控类的（鼠标、键盘）、传感设备的数据发送（心跳带、血压计、温度传感器）等。

---

接下来是第 2 个部分 ,实际工作中我们使用到的蓝牙库 BluetoothKit 的使用:

# 二 . 框架介绍

## 2.1 框架项目地址

https://github.com/dingjikerbo/BluetoothKit

## 2.2 框架优点

一、统一解决 Android 蓝牙通信过程中的兼容性问题

二、提供尽可能简单易用的接口，屏蔽蓝牙通信中的技术细节，只开放连接，读写，通知等语义。

三、实现串行化任务队列，统一处理蓝牙通信中的失败以及超时，支持可配置的容错处理

四、统一管理连接句柄，避免句柄泄露

五、方便监控各设备连接状态，在尽可能维持连接的情况下，将最不活跃的设备自动断开。

六、便于多进程 APP 架构下蓝牙连接的统一管理

七、支持拦截所有对蓝牙原生接口的调用

## 2.3 基本使用

### 2.3.1 添加依赖 

```groovy
compile 'com.inuker.bluetooth:library:1.4.0' 
```

或直接导入依赖 Liabrary 模块

### 2.3.2 在 app 模块的 Manifest 中添加蓝牙权限

```xml
<!--蓝牙相关权限-->
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### 2.3.3  扫描

```java
BluetoothClient mClient = new BluetoothClient(context);

SearchRequest request = new SearchRequest.Builder()
        .searchBluetoothLeDevice(3000, 3)   // 先扫BLE设备3次，每次3s
        .searchBluetoothClassicDevice(5000) // 再扫经典蓝牙5s,在实际工作中没用到经典蓝牙的扫描
        .searchBluetoothLeDevice(2000)      // 再扫BLE设备2s
        .build();

mClient.search(request, new SearchResponse() {

    @Override
    public void onSearchStarted() {//开始搜素

    }

    @Override
    public void onDeviceFounded(SearchResult device) {//找到设备 可通过manufacture过滤
        Beacon beacon = new Beacon(device.scanRecord);
        BluetoothLog.v(String.format("beacon for %s\n%s", device.getAddress(), beacon.toString()));
    }

    @Override
    public void onSearchStopped() {//搜索停止

    }

    @Override
    public void onSearchCanceled() {//搜索取消

    }

});
```

### 2.3.4  连接

- 连接配置

```java
BleConnectOptions options = new BleConnectOptions.Builder()
        .setConnectRetry(3)   // 连接如果失败重试3次
        .setConnectTimeout(30000)   // 连接超时30s
        .setServiceDiscoverRetry(3)  // 发现服务如果失败重试3次
        .setServiceDiscoverTimeout(20000)  // 发现服务超时20s
        .build();

mClient.connect(MAC, options, new BleConnectResponse() {
    @Override
    public void onResponse(int code, BleGattProfile data) {

    }
});
```



- 连接状态监听

```java
mClient.registerConnectStatusListener(MAC, mBleConnectStatusListener);

private final BleConnectStatusListener mBleConnectStatusListener = new BleConnectStatusListener() {

    @Override
    public void onConnectStatusChanged(String mac, int status) {
        if (status == STATUS_CONNECTED) {
    
        } else if (status == STATUS_DISCONNECTED) {
    
        }
    }

};

mClient.unregisterConnectStatusListener(MAC, mBleConnectStatusListener);
```



### 2.3.5  通讯

**读 Characteristic** 

```java
mClient.read(MAC, serviceUUID, characterUUID, new BleReadResponse() {

    @Override

    public void onResponse(int code, byte[] data) {

        if(code == REQUEST_SUCCESS) {

        }

    }

});
```

**写Characteristic**

要注意这里写的 byte[] **不能超过20字节**，如果超过了需要自己分成几次写。建议的办法是第一个 byte 放剩余要写的字节的长度。

```java
mClient.write(MAC, serviceUUID, characterUUID, bytes, new BleWriteResponse() {

    @Override
    public void onResponse(int code) {

        if(code == REQUEST_SUCCESS) {

        }
    }
});
```

这个写是带了 `WRITE_TYPE_NO_RESPONSE` 标志的，实践中发现比普通的 write 快 `2~3` 倍，建议用于固件升级。

```java
mClient.writeNoRsp(MAC, serviceUUID, characterUUID, bytes, new BleWriteResponse() {

    @Override
    public void onResponse(int code) {

        if(code == REQUEST_SUCCESS) {

        }
    }
});
```

**读 Descriptor**

```java
mClient.readDescriptor(MAC, serviceUUID, characterUUID, descriptorUUID, new BleReadResponse() {

    @Override
    public void onResponse(int code, byte[] data) {

    }

});
```

**写 Descriptor**

```java
mClient.writeDescriptor(MAC, serviceUUID, characterUUID, descriptorUUID, bytes, new BleWriteResponse() {

    @Override
    public void onResponse(int code) {

    }
});
```

**打开 Notify**

这里有两个回调，onNotify是接收通知的。

```java
mClient.notify(MAC, serviceUUID, characterUUID, new BleNotifyResponse() {

    @Override
    public void onNotify(UUID service, UUID character, byte[] value) {

    }

    @Override
    public void onResponse(int code) {
        if(code == REQUEST_SUCCESS) {

        }
    }

});
```

**关闭Notify**

```java
mClient.unnotify(MAC, serviceUUID, characterUUID, new BleUnnotifyResponse() {

    @Override
    public void onResponse(int code) {
        if(code == REQUEST_SUCCESS) {

        }
    }
});
```

**打开Indicate**

和Notify类似

```java
mClient.indicate(MAC, serviceUUID, characterUUID, new BleNotifyResponse() {

    @Override
    public void onNotify(UUID service, UUID character, byte[] value) {

    }

    @Override
    public void onResponse(int code) {
        if(code == REQUEST_SUCCESS) {

        }
    }
});
```

**关闭Indicate**

```java
mClient.unindicate(MAC, serviceUUID, characterUUID, new BleUnnotifyResponse() {

    @Override
    public void onResponse(int code) {
        if(code == REQUEST_SUCCESS) {

        }
    }
});
```

**读Rssi**

```java
mClient.readRssi(MAC, new BleReadRssiResponse() {

    @Override
    public void onResponse(int code, Integer rssi) {
        if(code == REQUEST_SUCCESS) {

        }

    }

});
```

### **2.3.6  断开**

```java
mClient.disconnect(MAC);
```

## 三、 蓝牙框架源码解析

接下来 , 我以蓝牙框架的**"连接"**功能为例来追踪下源码

```java
@Override
public void connect(String mac, BleConnectOptions options, BleConnectResponse response) {
    BluetoothLog.v(String.format("connect %s", mac));
    response = ProxyUtils.getUIProxy(response);
    mClient.connect(mac, options, response);
}
```

#### 3.1  BluetoothClientImpl 在这个实现里真正干了 BluetoothClient 的活

```java
@Override
public void connect(String mac, BleConnectOptions options, final BleConnectResponse response) {
  Bundle args = new Bundle();
  args.putString(EXTRA_MAC, mac);
  args.putParcelable(EXTRA_OPTIONS, options);
  safeCallBluetoothApi(CODE_CONNECT, args, new BluetoothResponse() {
    @Override
    protected void onAsyncResponse(int code, Bundle data) {
      checkRuntime(true);
      if (response != null) {
        data.setClassLoader(getClass().getClassLoader());
        BleGattProfile profile = data.getParcelable(EXTRA_GATT_PROFILE);
        response.onResponse(code, profile);
      }
    }
  });
}
```

其中有一个关键方法 safeCallBluetoothApi

```java
private void safeCallBluetoothApi(int code, Bundle args, final BluetoothResponse response) {
    checkRuntime(true);
    // BluetoothLog.v(String.format("safeCallBluetoothApi code = %d", code));
    try {
        IBluetoothService service = getBluetoothService();
        // BluetoothLog.v(String.format("IBluetoothService = %s", service));
        if (service != null) {
            args = (args != null ? args : new Bundle());
            service.callBluetoothApi(code, args, response);
        } else {
            response.onResponse(SERVICE_UNREADY, null);
        }
    } catch (Throwable e) {
        BluetoothLog.e(e);
    }
}
```

在这个方法里,首先拿到了蓝牙的 service(通过 bindservice 的方法),再调用了 callBluetoothApi 的方法
接下来我们来重点看下 BluetoothServiceImpl 中的 callBluetoothApi 方法 :

```java
@Override
public void callBluetoothApi(int code, Bundle args, final IResponse response) throws RemoteException {
    Message msg = mHandler.obtainMessage(code, new BleGeneralResponse() {

        @Override
        public void onResponse(int code, Bundle data) {
            if (response != null) {
                if (data == null) {
                    data = new Bundle();
                }
                try {
                    response.onResponse(code, data);
                } catch (Throwable e) {
                    BluetoothLog.e(e);
                }
            }
        }
    });

    args.setClassLoader(getClass().getClassLoader());
    msg.setData(args);
    msg.sendToTarget();
}
```

这里面用了 handler 发送消息,在 handleMessage 方法中处理消息 :

```java
@Override
public boolean handleMessage(Message msg) {
    Bundle args = msg.getData();
    String mac = args.getString(EXTRA_MAC);
    UUID service = (UUID) args.getSerializable(EXTRA_SERVICE_UUID);
    UUID character = (UUID) args.getSerializable(EXTRA_CHARACTER_UUID);
    UUID descriptor = (UUID) args.getSerializable(EXTRA_DESCRIPTOR_UUID);
    byte[] value = args.getByteArray(EXTRA_BYTE_VALUE);
    BleGeneralResponse response = (BleGeneralResponse) msg.obj;

    switch (msg.what) {
        case CODE_CONNECT:
            BleConnectOptions options = args.getParcelable(EXTRA_OPTIONS);
            BleConnectManager.connect(mac, options, response);
            break;

        case CODE_DISCONNECT:
            BleConnectManager.disconnect(mac);
            break;

        case CODE_READ:
            BleConnectManager.read(mac, service, character, response);
            break;

        case CODE_WRITE:
            BleConnectManager.write(mac, service, character, value, response);
            break;

        case CODE_WRITE_NORSP:
            BleConnectManager.writeNoRsp(mac, service, character, value, response);
            break;

        case CODE_READ_DESCRIPTOR:
            BleConnectManager.readDescriptor(mac, service, character, descriptor, response);
            break;

        case CODE_WRITE_DESCRIPTOR:
            BleConnectManager.writeDescriptor(mac, service, character, descriptor, value, response);
            break;

        case CODE_NOTIFY:
            BleConnectManager.notify(mac, service, character, response);
            break;

        case CODE_UNNOTIFY:
            BleConnectManager.unnotify(mac, service, character, response);
            break;

        case CODE_READ_RSSI:
            BleConnectManager.readRssi(mac, response);
            break;

        case CODE_SEARCH:
            SearchRequest request = args.getParcelable(EXTRA_REQUEST);
            BluetoothSearchManager.search(request, response);
            break;

        case CODE_STOP_SESARCH:
            BluetoothSearchManager.stopSearch();
            break;

        case CODE_INDICATE:
            BleConnectManager.indicate(mac, service, character, response);
            break;

        case CODE_REQUEST_MTU:
            int mtu = args.getInt(EXTRA_MTU);
            BleConnectManager.requestMtu(mac, mtu, response);
            break;

        case CODE_CLEAR_REQUEST:
            int clearType = args.getInt(EXTRA_TYPE, 0);
            BleConnectManager.clearRequest(mac, clearType);
            break;

        case CODE_REFRESH_CACHE:
            BleConnectManager.refreshCache(mac);
            break;
    }
    return true;
}
```

handleMessage 方法中首先解析了 bundle,然后区分不同的 CODE 处理不同的操作,针对**"连接"**的 connect 方法,接下来追踪到 BleConnectMaster.connect 方法

```java
@Override
public void connect(BleConnectOptions options, BleGeneralResponse response) {
    getConnectDispatcher().connect(options, response);
}
```

以上可以看出通过拿到 dispatcher 这个分发类来处理任务,跳转到 dispatcher 中的 addNewRequest 方法 ,

```java
private void addNewRequest(BleRequest request) {
    checkRuntime();

    if (mBleWorkList.size() < MAX_REQUEST_COUNT) { //最多的请求数是100
        request.setRuntimeChecker(this);
        request.setAddress(mAddress);
        request.setWorker(mWorker);//将worker设置为request,worker才是真正干活的
        mBleWorkList.add(request);
    } else {
        request.onResponse(Code.REQUEST_OVERFLOW);
    }

    scheduleNextRequest(10);
}
```

scheduleNextRequest 中通过 handler 发送了一个延时消息,消息处理的过程中调用了 scheduleNextRequest()方法

```java
private void scheduleNextRequest(long delayInMillis) {
    mHandler.sendEmptyMessageDelayed(MSG_SCHEDULE_NEXT, delayInMillis);
}

@Override
public boolean handleMessage(Message msg) {
    switch (msg.what) {
        case MSG_SCHEDULE_NEXT:
            scheduleNextRequest();
            break;
    }
    return true;
}

private void scheduleNextRequest() {
    if (mCurrentRequest != null) {
        return;
    }

    if (!ListUtils.isEmpty(mBleWorkList)) {
        mCurrentRequest = mBleWorkList.remove(0);
        //以下为重要代码
        mCurrentRequest.process(this);
    }
}
```

其中有一行关键的代码 mCurrentRequest.process(this),接下来我们看下 BleRequest 到底是怎么干活的?

```java
@Override
final public void process(IBleConnectDispatcher dispatcher) {
    checkRuntime();

    mDispatcher = dispatcher;

    BluetoothLog.w(String.format("Process %s, status = %s", getClass().getSimpleName(), getStatusText()));
    //兼容性的的判断
    if (!BluetoothUtils.isBleSupported()) {
        onRequestCompleted(Code.BLE_NOT_SUPPORTED);
    } else if (!BluetoothUtils.isBluetoothEnabled()) {
        onRequestCompleted(Code.BLUETOOTH_DISABLED);
    } else {
        try {
            registerGattResponseListener(this);
            processRequest();
        } catch (Throwable e) {
            BluetoothLog.e(e);
            onRequestCompleted(Code.REQUEST_EXCEPTION);
        }
    }
}
```

这里面有一个关键的方法, processRequest(),这是一个抽象方法,子类需要实现的自己实现,关于"连接"我们可以追踪到 BleConnectRequest,以下的方法可以看到,最终判断现在的连接状态后 进行连接的回调

```java
@Override
public void processRequest() {
    processConnect();
}

private void processConnect() {
    mHandler.removeCallbacksAndMessages(null);
    mServiceDiscoverCount = 0;

    switch (getCurrentStatus()) {
        case Constants.STATUS_DEVICE_CONNECTED://连接成功
            processDiscoverService();//处理服务 -- 读服务
            break;

        case Constants.STATUS_DEVICE_DISCONNECTED://连接失败,打开Gatt
            if (!doOpenNewGatt()) {
                closeGatt();
            } else {
                mHandler.sendEmptyMessageDelayed(MSG_CONNECT_TIMEOUT, mConnectOptions.getConnectTimeout());
            }
            break;

        case Constants.STATUS_DEVICE_SERVICE_READY:
            onConnectSuccess();
            break;
    }
}
```

至此,分析告一段落,现在我们来分析下连接的另一个关键内容 response 回调的处理,以连接为例,在 BleConnectWorker 中有一个连接回调,根据不同的情况回调回去.

以上为初学蓝牙和蓝牙框架的一些感悟,以后有机会务必会完善此博客~

```
作者：努力深耕 Android 的小透明
链接：https://www.jianshu.com/p/6dca236f6ad5
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```