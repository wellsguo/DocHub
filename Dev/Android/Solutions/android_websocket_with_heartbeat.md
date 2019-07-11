> 最近公司要做一款内部使用的工具类 app，方便销售部门打电话（其实就是在后台有好多用户数据，之前销售部门同事拨打电话，需要自己从销售后台查看用户手机号等信息，然后自己拿自己手机拨号，然后打出去。现在想实现销售的同事，点击销售后台的按钮，自己的手机直接拨号的功能）。为此，开始着手思考，怎么实现销售后台点击按钮，手机 app 端能收到点击按钮的监听。

首先，后台提供一个接口，在服务器端不断的调用接口以监听后台按钮的点击事件以及收到后台传过来的信息。这样太繁琐，而且不断的调接口，比较耗性能，肯定不合适。然后想到建立一个长连接，在 app 端写一个长连接（用 Socket 或者 WebSocket ），并加入心跳检测，定期的去检测长连接是否连接正常，如果连接中断，执行重新连接。于是乎自己写了个Socket 的长连接，加入了心跳检测。但是等和后台联调的时，后台的同事提议用 WebSocket 长连接，这样也许能方便些。于是自己又不情愿的把 Socket 长连接换成 WebSocket 方式实现的长连接。还好我网络请求用的鸿洋大神的 OkttpUtils，里面提供了一个关于 WebSocket 连接的回调。最终实现了这一功能。好了废话不多说，上代码了。。。。

## 1. 在 AndroidManifest.xml 中注册服务
> 开发时很容易忘记

```xml
<!-- 后台服务-长连接 -->
<service android:name=".service.BackService" />
```
## 2. 写一个类 BackService 继承 Service

```java
public class BackService extends Service{
    @Override
    public void onCreate() {
        super.onCreate();
    }
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
```

### 3. 在 BackService 的 onCreate() 方法中开启线程
```java
   @Override
    public void onCreate() {
        super.onCreate();
        new InitSocketThread().start();
    }
```

```java
class InitSocketThread extends Thread {
    @Override
    public void run() {
        super.run();
        try {
            initSocket();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

```java
/**
 * 心跳检测时间
 */
private static final long HEART_BEAT_RATE = 15 * 1000;//每隔15秒进行一次对长连接的心跳检测
private static final String WEBSOCKET_HOST_AND_PORT = "ws://xxx:9501";//可替换为自己的主机名和端口号
private WebSocket mWebSocket;
// 初始化socket
private void initSocket() throws UnknownHostException, IOException {
    OkHttpClient client = new OkHttpClient.Builder().readTimeout(0, TimeUnit.MILLISECONDS).build();
    Request request = new Request.Builder().url(WEBSOCKET_HOST_AND_PORT).build();
    client.newWebSocket(request, new WebSocketListener() {
        @Override
        public void onOpen(WebSocket webSocket, Response response) {//开启长连接成功的回调
            super.onOpen(webSocket, response);
            mWebSocket = webSocket;
        }

        @Override
        public void onMessage(WebSocket webSocket, String text) {//接收消息的回调
            super.onMessage(webSocket, text);
            //收到服务器端传过来的消息text
        }

        @Override
        public void onMessage(WebSocket webSocket, ByteString bytes) {
            super.onMessage(webSocket, bytes);
        }

        @Override
        public void onClosing(WebSocket webSocket, int code, String reason) {
            super.onClosing(webSocket, code, reason);
        }

        @Override
        public void onClosed(WebSocket webSocket, int code, String reason) {
            super.onClosed(webSocket, code, reason);
        }

        @Override
        public void onFailure(WebSocket webSocket, Throwable t, @Nullable Response response) {//长连接连接失败的回调
            super.onFailure(webSocket, t, response);
        }
    });
    client.dispatcher().executorService().shutdown();
    mHandler.postDelayed(heartBeatRunnable, HEART_BEAT_RATE);//开启心跳检测
}
```
## 4. 开启心跳检测

```java
private long sendTime = 0L;
// 发送心跳包
private Handler mHandler = new Handler();
private Runnable heartBeatRunnable = new Runnable() {
    @Override
    public void run() {
        if (System.currentTimeMillis() - sendTime >= HEART_BEAT_RATE) {
            boolean isSuccess = mWebSocket.send("");
            //发送一个空消息给服务器，通过发送消息的成功失败来判断长连接的连接状态
            if (!isSuccess) {//长连接已断开
                mHandler.removeCallbacks(heartBeatRunnable);
                mWebSocket.cancel();//取消掉以前的长连接
                new InitSocketThread().start();//创建一个新的连接
            } else {//长连接处于连接状态

            }

            sendTime = System.currentTimeMillis();
        }
        mHandler.postDelayed(this, HEART_BEAT_RATE);//每隔一定的时间，对长连接进行一次心跳检测
    }
};
    ```
### 5. 当 BackService 销毁时，关闭长连接

```java
@Override
public void onDestroy() {
    super.onDestroy();
    if (mWebSocket != null) {
        mWebSocket.close(1000, null);
    }
}
```
## 来源
作者：行走在青春路上的小蜜蜂   
来源：CSDN   
原文：https://blog.csdn.net/u010257931/article/details/79694911   
版权声明：本文为博主原创文章，转载请附上博文链接！