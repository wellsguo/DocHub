## websocket + service for android

依赖 autobahn-0.5.0.jar 文件包，通过创建 service 建立长连接，该包封装的有断开超链接的细节操作，简单实用。超链接的存在替代了轮循请求接口，大大的节约了服务器的压力。



### MainActivity

```java
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends BaseActivity implements View.OnClickListener{


    private Button connectBtn;
    private Button disconnectBtn;
    private TextView messageTv;
    private EditText sendMsgEdit;
    private Button sendMsgBtn;
    private Intent websocketServiceIntent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        websocketServiceIntent = new Intent(this, WebSocketService.class);
        startService(websocketServiceIntent);
        findViews();
        initViews();
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.connect_btn:
                WebSocketService.webSocketConnect();
                break;

            case R.id.disconnect_btn:
                WebSocketService.closeWebsocket(false);
                break;

            case R.id.send_msg_btn:
                WebSocketService.sendMsg(sendMsgEdit.getText().toString());
                break;
        }
    }


    private void findViews(){
        connectBtn = (Button)findViewById(R.id.connect_btn);
        disconnectBtn = (Button)findViewById(R.id.disconnect_btn);
        messageTv = (TextView)findViewById(R.id.message_tv);
        sendMsgEdit = (EditText)findViewById(R.id.send_msg_edit);
        sendMsgBtn = (Button)findViewById(R.id.send_msg_btn);
    }

    private void initViews(){
        connectBtn.setOnClickListener(this);
        disconnectBtn.setOnClickListener(this);
        sendMsgBtn.setOnClickListener(this);
    }


    @Override
    protected void getMessage(String msg) {
        messageTv.setText("");
        messageTv.setText(msg);
    }

    @Override
    public void onBackPressed() {
        WebSocketService.closeWebsocket(true);
        stopService(websocketServiceIntent);
        super.onBackPressed();
    }
}
```

- startService(intent)  启动 service
- stopService(intent) 停用 service

### WebSocketService 

> 这个是service,需要在配置清单注册

```java
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Toast;

import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;
import de.tavendo.autobahn.WebSocketOptions;

/**
 * Created by wxs on 16/8/17.
 */
public class WebSocketService extends Service {

    private static final String TAG = WebSocketService.class.getSimpleName();

    public static final String WEBSOCKET_ACTION = "WEBSOCKET_ACTION";

    private BroadcastReceiver connectionReceiver;
    private static boolean isClosed = true;
    private static WebSocketConnection webSocketConnection;
    private static WebSocketOptions options = new WebSocketOptions();
    private static boolean isExitApp = false;
    private static String websocketHost = ""; //websocket服务端的url,ws是协议


    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        if (connectionReceiver == null) {
            connectionReceiver = new BroadcastReceiver() {
                @Override
                public void onReceive(Context context, Intent intent) {
                    ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
                    NetworkInfo networkInfo = connectivityManager.getActiveNetworkInfo();

                    if (networkInfo == null || !networkInfo.isAvailable()) {
                        Toast.makeText(getApplicationContext(), "网络已断开，请重新连接", Toast.LENGTH_SHORT).show();
                    } else {
                        if (webSocketConnection != null) {
                            webSocketConnection.disconnect();
                        }
                        if (isClosed) {
                            webSocketConnect();
                        }
                    }

                }
            };

            IntentFilter intentFilter = new IntentFilter();
            intentFilter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
            registerReceiver(connectionReceiver, intentFilter);
        }
        return super.onStartCommand(intent, flags, startId);

    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public static void closeWebsocket(boolean exitApp) {
        isExitApp = exitApp;
        if (webSocketConnection != null && webSocketConnection.isConnected()) {
            webSocketConnection.disconnect();
            webSocketConnection = null;
        }
    }

    public static void webSocketConnect(){
        webSocketConnection = new WebSocketConnection();
        try {
            webSocketConnection.connect(websocketHost,new WebSocketHandler(){


                //websocket启动时候的回调
                @Override
                public void onOpen() {
                    Log.d(TAG,"open");
                    isClosed = false;
                }


                //websocket接收到消息后的回调
                @Override
                public void onTextMessage(String payload) {
                    Log.d(TAG, "payload = " + payload);
                }

                //websocket关闭时候的回调
                @Override
                public void onClose(int code, String reason) {
                    isClosed = true;
                    Log.d(TAG, "code = " + code + " reason = " + reason);
                    switch (code) {
                        case 1:
                            break;
                        case 2:
                            break;
                        case 3://手动断开连接
//                            if (!isExitApp) {
//                                webSocketConnect();
//                            }
                            break;
                        case 4:
                            break;
                        /**
                         * 由于我在这里已经对网络进行了判断,所以相关操作就不在这里做了
                         */
                        case 5://网络断开连接
//                            closeWebsocket(false);
//                            webSocketConnect();
                            break;
                    }
                }
            } , options);
        } catch (WebSocketException e) {
            e.printStackTrace();
        }
    }

    public static void sendMsg(String s) {
        Log.d(TAG, "sendMsg = " + s);
        if (!TextUtils.isEmpty(s))
            if (webSocketConnection != null) {
                webSocketConnection.sendTextMessage(s);
            }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (connectionReceiver != null) {
            unregisterReceiver(connectionReceiver);
        }
    }
}
```

### BaseActivity
```java
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.text.TextUtils;

/**
 * Created by wxs on 16/8/17.
 *
 * 这个基类里面就是注册了一下service以及注销service
 * 里面有一个抽象方法,每次activity收到消息后都会调用这个抽象方法
 * 只要继承这个类的都能收到消息
 *
 *
 */
public abstract class BaseActivity extends Activity {


    private BroadcastReceiver imReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (WebSocketService.WEBSOCKET_ACTION.equals(action)) {
                Bundle bundle = intent.getExtras();
                if (bundle != null) {
                    String msg = bundle.getString("message");
                    if (!TextUtils.isEmpty(msg))
                        getMessage(msg);
                }

            }
        }
    };


    protected abstract void getMessage(String msg);

    @Override
    protected void onStart() {
        super.onStart();
        IntentFilter filter = new IntentFilter(WebSocketService.WEBSOCKET_ACTION);
        registerReceiver(imReceiver,filter);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(imReceiver);
    }
}
```

### 布局
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/white"
    tools:context="com.example.wxs.androidwebsocketdemo.MainActivity"
    android:orientation="vertical">


    <Button
        android:id="@+id/connect_btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="connect"
        android:textSize="20sp"
        android:layout_marginTop="20dp"/>


    <Button
        android:id="@+id/disconnect_btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="disconnect"
        android:textSize="20sp"
        android:layout_marginTop="20dp"/>


    <TextView
        android:id="@+id/message_tv"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="16sp"
        android:layout_marginTop="20dp"/>

    <EditText
        android:id="@+id/send_msg_edit"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="16sp"
        android:layout_marginTop="20dp"/>

    <Button
        android:id="@+id/send_msg_btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textSize="20sp"
        android:text="send"
        android:layout_marginTop="20dp"/>

</LinearLayout>
```
