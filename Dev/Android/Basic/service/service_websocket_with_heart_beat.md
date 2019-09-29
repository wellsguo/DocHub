// 垃圾小白写了自己看的


## 定义接口

> 处理后台返回的数据

```java
public interface WebsocketMessageHandlder {
    void handleMessage(String message);
}
```

##  service 文件

```java
public class SocketService extends Service {

    // 自己定义接口用来传参
    private static WebsocketMessageHandlder mWebsocketMessageHandlder;
    private SocketBinder socketBinder = new SocketBinder();
    public static WebSocketClient client;
    public static String address = "ws://192.168.0.2:8080/websocket/";
    public static String message;

    private static Handler mHandler = new Handler();
    // 通过 post.Delayed(this, 10 * 1000) 实现了每 10 s 发送一次心跳请求，从而保持 websokect 的链接检测
    private static Runnable heartBeatRunnable = new Runnable() {
        @Override
        public void run() {
            mHandler.postDelayed(this, 10 * 1000);
            sendMsg("@heart");
        }
    };


    @Override
    public void onCreate() {
        super.onCreate();
        try {
            initSocketClient(SharedUtils.getInstance().getToken());
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        L.e("执行了onStartCommand()");
        connect();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        L.e("执行了onDestory()");
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return socketBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        L.e("绑定服务");
        return super.onUnbind(intent);
    }

    @Override
    public void unbindService(ServiceConnection conn) {
        L.e("解绑服务");
        super.unbindService(conn);
    }

    public static class SocketBinder extends Binder {
        public void keep_alive() {
            mHandler.post(heartBeatRunnable);
            L.e("Service关联了Activity,并在Activity执行了Service的方法");
        }

        public String getNewOrder() {
            return message;
        }

        public void getOrder(String orderId) {
            JSONObject object = new JSONObject();
            try {
                object.put("service", "RECEIVEORDER");
                object.put("orderNo", orderId);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            sendMsg(object.toString());
        }

        public void setWebsocketMessageHandlder(WebsocketMessageHandlder handler) {
            mWebsocketMessageHandlder = handler;
        }

    }

    /**
     * 调用 Android 组件里的消息处理方法，完成具体的消息处理
     */ 
    public static void disposeMsg(String msg) {
        if (mWebsocketMessageHandlder != null) {
            mWebsocketMessageHandlder.handleMessage(msg);
        }
    }

    /**
     * 发送消息
     */
    public static void sendMsg(String msg) {

        L.e(msg);
        if (client == null)
            return;
        try {
            client.send(msg);
        } catch (WebsocketNotConnectedException e) {
            e.printStackTrace();
            closeConnect();
            try {
                initSocketClient(SharedUtils.getInstance().getToken());
            } catch (URISyntaxException ee) {
                ee.printStackTrace();
            }
            connect();
        }
    }

    public static void initSocketClient(String token) throws URISyntaxException {
        if (client == null) {
            client = new WebSocketClient(new URI(address + token)) {

                @Override
                public void onOpen(ServerHandshake serverHandshake) {
                    // 连接成功
                    L.e("socket连接成功");
                }

                @Override
                public void onMessage(String s) {
                    // 服务端发送消息 通过接口传给fragment
                    disposeMsg(s);
                }

                @Override
                public void onClose(int i, String s, boolean remote) {
                    // 连接断开，remote判定是客户端断开还是服务端断开
                    L.e("Connection closed by " + (remote ? "remote peer?" : "us") + ", info=" + s);
                }

                @Override
                public void onError(Exception e) {
                    L.e("error:" + e);
                }
            };
        }
    }

    // 连接
    public static void connect() {

        new Thread() {
            @Override
            public void run() {
                if (client != null) {
                    try {
                        client.connect();
                    } catch (IllegalStateException e) {
                        L.e(e.toString());
                    }
                }
                L.e("socket连接");
            }
        }.start();
    }

    // 断开连接
    public static void closeConnect() {
        try {
            client.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            client = null;
        }
    }

}
```

## 服务调用组件

```java

import static android.content.Context.BIND_AUTO_CREATE;

//BaseFragment 自己写的
public class OrderReceiveFragment extends BaseFragment implements WebsocketMessageHandlder {    
    private Order.OrderData.OrderList newOrder;
    private SocketService.SocketBinder socketBinder = new SocketService.SocketBinder();
    private ServiceConnection connection = new ServiceConnection() {
        //重写onServiceConnected()方法和onServiceDisconnected()方法
        // 在Activity与Service建立关联和解除关联的时候调用
        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
        //

        // 在Activity与Service解除关联的时候调用
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            //实例化Service的内部类myBinder
            // 通过向下转型得到了MyBinder的实例
            socketBinder = (SocketService.SocketBinder) service;
            //在Activity调用Service类的方法
            socketBinder.keep_alive();
            socketBinder.setWebsocketMessageHandlder(OrderReceiveFragment.this);
        }
    };
    
    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            switch (msg.what) {
                case 0:
                    //推单
                    data.add(0, newOrder);
                    adapter.notifyDataSetChanged();
                    break;
                case 1:
                    //心跳
                    break;
                case 2:
                    //抢单
                    break;
            }
        }
    };

    //绑定service并启动服务
    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        Intent intent = new Intent(context, SocketService.class);
        getActivity().getApplicationContext().bindService(intent, connection, BIND_AUTO_CREATE);
        getActivity().getApplicationContext().startService(intent);

    }

    // 自己写的接口里的方法
    @Override
    public void handleMessage(String s) {

        try {
            JSONObject jsonObject = new JSONObject(s);
            String data = jsonObject.getString("data");
            Message message = new Message();
            if (data.indexOf("receiveOrder") != -1) { //抢单成功
                message.what = 2;
            }

            if (data.indexOf("heart") != -1) {//心跳
                message.what = 1;
            }

            if (data.indexOf("pushOrder") != -1) {
                Gson gson = new Gson();
                newOrder = gson.fromJson(data, Order.OrderData.OrderList.class);
                message.what = 0;
                message.obj = newOrder;
            }

            handler.sendMessage(message);

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
```