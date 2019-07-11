## receiver

```java
package com.tlj.kys.jwcw.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * @author GUOJ
 * @date 6/5/19
 */
public class NetWorkChangReceiver extends BroadcastReceiver {
    /**
     * 获取连接类型
     *
     * @param type
     * @return
     */
    private String getConnectionType(int type) {
        String connType = "";
        if (type == ConnectivityManager.TYPE_MOBILE) {
            connType = "3G网络数据";
        } else if (type == ConnectivityManager.TYPE_WIFI) {
            connType = "WIFI网络";
        }
        return connType;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        if (WifiManager.WIFI_STATE_CHANGED_ACTION.equals(intent.getAction())) {// 监听wifi的打开与关闭，与wifi的连接无关
            int wifiState = intent.getIntExtra(WifiManager.EXTRA_WIFI_STATE, 0);
            Log.e("TAG", "wifiState:" + wifiState);
            switch (wifiState) {
                case WifiManager.WIFI_STATE_DISABLED:
                    break;
                case WifiManager.WIFI_STATE_DISABLING:
                    break;
            }
        }
        // 监听网络连接，包括wifi和移动数据的打开和关闭,以及连接上可用的连接都会接到监听
        if (ConnectivityManager.CONNECTIVITY_ACTION.equals(intent.getAction())) {
            //获取联网状态的NetworkInfo对象
            NetworkInfo info = intent.getParcelableExtra(ConnectivityManager.EXTRA_NETWORK_INFO);
            if (info != null) {
                //如果当前的网络连接成功并且网络连接可用
                if (NetworkInfo.State.CONNECTED == info.getState() && info.isAvailable()) {
                    if (info.getType() == ConnectivityManager.TYPE_WIFI || info.getType() == ConnectivityManager.TYPE_MOBILE) {
                        String msg;
                        if (ping()){
                            msg = String.format("%s%s%s",getConnectionType(info.getType()) ,"<外网>", "连上"+
                                    (info.getType() == ConnectivityManager.TYPE_WIFI ? ",将在2s钟后关闭wifi": ""));
                        }else{
                            msg = String.format("%s%s%s",getConnectionType(info.getType()) ,"", "连上");
                        }
                        Toast.makeText(context, msg, Toast.LENGTH_LONG).show();
                        if (info.getType() == ConnectivityManager.TYPE_WIFI ){
                            WifiManager wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
                            if (wifiManager.isWifiEnabled()) {
                                wifiManager.setWifiEnabled(false);
                            } else {
                                //wifiManager.setWifiEnabled(true);
                            }
                        }
                    }
                } else {
                    Toast.makeText(context, getConnectionType(info.getType()) + "断开", Toast.LENGTH_LONG).show();
                }
            }
        }
    }


    /**
     * 推断Ping 网址是否返回成功
     *
     * @param times
     * @param host
     * @return
     */
    public boolean ping(int times, String host) {
        StringBuffer ret = new StringBuffer();
        try {
            Process p = Runtime.getRuntime().exec("/system/bin/ping -c " + times + " " + host); // 10.83.50.111
            int status = p.waitFor();

            BufferedReader buf = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String str;
            // 读出全部信息并显示
            while ((str = buf.readLine()) != null) {
                str = str + "\r\n";
                ret.append(str);
            }
            Log.i("Net", String.format("ping: %s", ret.toString()));

            return status == 0;
        } catch (Exception ex) {
            Log.e("Net", String.format("ping: %s", ex.getMessage()));
        }
        return false;
    }

    public boolean ping(){
        return ping(4, "14.215.177.38");// baidu
    }
}
```

## Activity

```java
public class BaseAppCompatActivity extends AppCompatActivity {

    private boolean isRegistered = false;
    private NetWorkChangReceiver netWorkChangReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //注册网络状态监听广播
        netWorkChangReceiver = new NetWorkChangReceiver();
        IntentFilter filter = new IntentFilter();
        filter.addAction(WifiManager.WIFI_STATE_CHANGED_ACTION);
        filter.addAction(WifiManager.NETWORK_STATE_CHANGED_ACTION);
        filter.addAction(ConnectivityManager.CONNECTIVITY_ACTION);
        registerReceiver(netWorkChangReceiver, filter);
        isRegistered = true;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        //解绑
        if (isRegistered) {
            unregisterReceiver(netWorkChangReceiver);
        }
    }
}
```

## AndroidManifest.xml

```xml
<uses-permission android:name="android.permission.INTERNET"/>
 
<!-- 网络状态 -->
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
 

<!--监听网络状态-->
<receiver android:name=".receiver.NetWorkChangReceiver" >
    <intent-filter>
        <action android:name="android.net.conn.CONNECTIVITY_CHANGE" />
        <action android:name="android.net.wifi.WIFI_STATE_CHANGED" />
        <action android:name="android.net.wifi.STATE_CHANGE" />
    </intent-filter>
</receiver>
```
