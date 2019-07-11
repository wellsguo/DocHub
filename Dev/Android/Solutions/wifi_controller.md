## 1、需要申请的权限

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.WAKE_LOCK"/>
```

## 2. code

```java
//2、获取WifiManager
WifiManager wifiManager = (WifiManager) this.getSystemService(Context.WIFI_SERVICE); 

//3、开启、关闭wifi
if (wifiManager.isWifiEnabled()) {  
    wifiManager.setWifiEnabled(false);  
} else {  
    wifiManager.setWifiEnabled(true);  
}
```
