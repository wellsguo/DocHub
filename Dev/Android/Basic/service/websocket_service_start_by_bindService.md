
```java
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends ActionBarActivity {

    public WebSocketConnection  wsC = new WebSocketConnection();

    public Handler handler = new Handler(){
        @Override
        public void handleMessage( Message msg )
        {
            super.handleMessage( msg );
            if ( msg.what == 0 )
            {
            }
        }
    };

    public void toastLog( String s ){
        Toast.makeText( this, s, Toast.LENGTH_SHORT ).show();
    }


    private void wsStart(){
        try {
            wsC.connect( wsUrl, new WebSocketHandler() {
                        @Override
                        public void onOpen()
                        {
                            toastLog( "Status: Connected to " + wsUrl );
                            wsC.sendTextMessage( "Hello, world!" );
                        }

                        @Override
                        public void onTextMessage( String payload )
                        {
                            toastLog( "Got echo: " + payload );
                        }

                        @Override
                        public void onClose( int code, String reason )
                        {
                            toastLog( "Connection lost." );
                        }
                    } );
        } catch ( WebSocketException e ) {
            e.printStackTrace();
        }
    }


    @Override
    protected void onCreate( Bundle savedInstanceState )
    {
        super.onCreate( savedInstanceState );
        setContentView( R.layout.activity_main );

        wsStart();

        Button wsSend = (Button) findViewById( R.id.wsSend );
        wsSend.setOnClickListener( new View.OnClickListener()
                        {
                            @Override
                            public void onClick( View v )
                            {
                                wsC.sendTextMessage( "ooxx" );
                            }
                        } );
    }


    @Override
    protected void onDestroy()
    {
        super.onDestroy();
        if ( wsC.isConnected() )
        {
            wsC.disconnect();
        }
    }


    @Override
    public boolean onCreateOptionsMenu( Menu menu )
    {
        /* Inflate the menu; this adds items to the action bar if it is present. */
        getMenuInflater().inflate( R.menu.main, menu );
        return(true);
    }


    @Override
    public boolean onOptionsItemSelected( MenuItem item )
    {
        /*
        * Handle action bar item clicks here. The action bar will
        * automatically handle clicks on the Home/Up button, so long
        * as you specify a parent activity in AndroidManifest.xml.
        */
        int id = item.getItemId();
        if ( id == R.id.action_settings )
        {
            return(true);
        }
        return(super.onOptionsItemSelected( item ) );
    }
}
```

> 上面的按照使用就好。配置好远程地址，端口号。就基本能够通信了。如果直接放到acvity里面会出现Socket断掉的情况。鉴于此。我把他放到Service里面来跑.

Service 代码如下：

```java
package com.micro_chat.service;

import android.annotation.TargetApi;
import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Binder;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;

import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketConnectionHandler;
import de.tavendo.autobahn.WebSocketException;
import android.app.Service;
import android.widget.Toast;

import com.micro_chat.MainActivity;
import com.micro_chat.R;
import com.micro_chat.api.Apiapp;
import com.micro_chat.base.BaseActivity;
import com.micro_chat.uilit.ACache;

import org.json.JSONException;
import org.json.JSONObject;

/**
* Created by moye on 2016/6/24.
*/
public class SosWebSocketClientService extends Service{
    private final String TAG = “SosWebSocketClientService”;
    private static final String TAGE = “weiliaoService”;
    private static int NOTIFY_ID = 1000;
    private final WebSocketConnection mConnection = new WebSocketConnection();
    private final IBinder mBinder = new SosWebSocketClientBinder();
    NotificationManager mNM;
    

    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    @Override
    public void onCreate() {
        mNM = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        initWebSocket();
        super.onCreate();
        Log.d(TAGE, "Service Create");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }

    /**
    * 销毁
    */
    @Override
    public void onDestroy() {
        if (mConnection.isConnected()) {
            mConnection.disconnect();
        }
        super.onDestroy();
        Log.d(TAGE, "Service Destroy");
    }

    private void initWebSocket(){
        {
            try {
                mConnection.connect(Apiapp.wsuri, new WebSocketConnectionHandler() {
                    @Override
                    public void onOpen() {
                        Log.d(TAGE, "Status: Connected to " + Apiapp.wsuri);
                    }

                    @Override
                    public void onTextMessage(String payload) {
                        //接受服务器消息
                        Log.d(TAGE,"Status: Over msg"+payload);
                        try {
                            JSONObject jsonObject = new JSONObject(payload);
                        } catch (JSONException e) {
                            e.printStackTrace();
                            initWebSocket();
                            Toast.makeText(BaseActivity.activity,"服务器已经重连！",Toast.LENGTH_LONG).show();
                             // restartApplication();
                        }
                    }

                    @Override
                    public void onClose(int code, String reason) {
                        //关闭服务器链接
                        Log.d(TAGE, "Status: Connection lost" + reason);
                        //Toast.makeText(BaseActivity.activity,"Connection lost="+reason,Toast.LENGTH_LONG).show();
                        //restartApplication();
                        initWebSocket();
                        Toast.makeText(BaseActivity.activity,"服务器已经重连！",Toast.LENGTH_LONG).show();
                    }
                });

            } catch (WebSocketException e) {
                Log.d(TAGE, e.toString());
                //restartApplication();
                initWebSocket();
            }
        }
    }

    private void restartApplication() {
        final Intent intent = getPackageManager().getLaunchIntentForPackage(getPackageName());
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }


    public class SosWebSocketClientBinder extends Binder {
        public SosWebSocketClientService getService() {
            return SosWebSocketClientService.this;
        }

        public void sendXxx(String addr){
            if(mConnection.isConnected())
                mConnection.sendTextMessage(addr);
        }
    }

    /***
    * 发送通知
    * @param context
    * @param title
    * @param contentText
    */
    @TargetApi(Build.VERSION_CODES.JELLY_BEAN)
    public static void sendNotification(Context context,String title,String contentText){
        NotificationManager notifyMgr= (NotificationManager)context.getSystemService(Context.NOTIFICATION_SERVICE);
        Intent resultIntent = new Intent(context, MainActivity.class);//MainActivity  GetMesgActivity
        resultIntent.setFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pi = PendingIntent.getActivity(context, 0, resultIntent, PendingIntent.FLAG_UPDATE_CURRENT);
        Notification notification = new Notification.Builder(context)
                .setSmallIcon(R.mipmap.icon)
                .setTicker("点击查看消息")
                .setContentTitle(title)
                .setContentText(contentText)
                .setContentIntent(pi)
                .setDefaults(Notification.DEFAULT_ALL)//DEFAULT_VIBRATE
                .build();
        notification.flags |= Notification.FLAG_AUTO_CANCEL; 

        notifyMgr.notify(NOTIFY_ID, notification);
    }
}
```

在activity 里面启动服务。

```java
Intent intent = new Intent(this, WebSocketClientService.class);
startService(intent);
bindService(intent, conn, Context.BIND_AUTO_CREATE);

private ServiceConnection conn = new ServiceConnection() {
    @Override
    public void onServiceDisconnected(ComponentName name) {

    }

    @Override
    public void onServiceConnected(ComponentName name, IBinder service) {
        // // TODO Auto-generated method stub这里面发送消息通过Service
        WebSocketClientService.WebSocketClientBinder binder = (WebSocketClientService.WebSocketClientBinder)iBinder;
        binder.sendXxx(SentMsg);
    }
};
```

以上基本就实现了通过服务来开启WebSocket了。当然也有服务停止的时候，这时就是展现你的聪明才智的时候了，本人愚昧只能使用定时器来防止服务死掉了。如果有更好的建议欢迎留言给我。
