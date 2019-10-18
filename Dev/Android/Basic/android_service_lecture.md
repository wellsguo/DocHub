

## [前言](https://blog.csdn.net/weixin_39460667/article/details/82770164)

service服务，能够使得应用程序即使在关闭的情况下仍然可以在后台继续执行。后台功能属于四大组件之一，其重要程度不言而喻，那让我们接下来来来好好学习一下。

 


通过本文你可以学到以下内容

- service是什么
- service的两种状态
- Service在清单文件中的声明
- Service启动服务实现方式及其详解
- Service绑定服务的三种实现方式
- 关于启动服务与绑定服务间的转换问题
- 前台服务以及通知发送
- 服务Service与线程Thread的区别
- 管理服务生命周期的要点
- Android 5.0以上的隐式启动问题及其解决方案
- 保证服务不被杀死的实现思路
 

## 一、service 是什么

**Service** 是 Android 中实现程序后台运行的解决方案，他非常适合是去执行那些不需要和用户交互而且还要长期运行的任务。服务的运行不依赖于任何用户界面，即使程序被切换到后台，或者用户打开了另一个应用程序，服务仍然能够保持独立运行。不过需要注意的是，服务并不是运行在一个独立的进程当中，而是依赖于创建服务时所在的应用程序进程。当某个应用程序被杀掉时，所有依赖该进程的服务也会停止运行。service 基本上分为**两种形式**：

 

### 本地服务

该服务依附在主进程上而不是独立的进程，这样在一定程度上节约了资源，另外本地服务因为是在同一进程因此不需要 IPC，也不需要 AIDL。相应 `bindService` 会方便很多，当主进程被Kill 后，服务便会终止。一般使用在音乐播放器播放等不需要常驻的服务。指的是服务和启动服务的 `Activity` 在同一个进程中。

 

### 远程服务

该服务是独立的进程，对应进程名格式为所在包名加上你指定的 `android:process` 字符串。一般定义方式 android:process=":service" 由于是独立的进程，因此在Activity所在进程被Kill的时候，该服务依然在运行，不受其他进程影响，有利于为多个进程提供服务具有较高的灵活性。由于是独立的进程，会占用一定资源，并且使用 AIDL 进行 IPC 比较麻烦。一般用于系统的Service，这种Service是常驻的。指的是服务和启动服务的activity不在同一个进程中。

***注意***: 启动本地服务用的是**显式启动**；远程服务的启动要用到**隐式启动**.



## 二、Service 的两种状态

[四]()、[五]()会进行详讲

### 启动状态

当应用组件（如 Activity）通过调用 `startService()` 启动服务时，服务即处于“启动”状态。一旦启动，服务即可在后台无限期运行，即使启动服务的组件已被销毁也不受影响，除非手动调用才能停止服务， 已启动的服务通常是执行单一操作，而且不会将结果返回给调用方。

### 绑定状态

当应用组件通过调用 `bindService()` 绑定到服务时，服务即处于“绑定”状态。绑定服务提供了一个客户端-服务器接口，*允许组件与服务进行交互、发送请求、获取结果*，甚至是利用进程间通信 (IPC) 跨进程执行这些操作。 仅当与另一个应用组件绑定时，绑定服务才会运行。 多个组件可以同时绑定到该服务，但全部取消绑定后，该服务即会被销毁。

 

## 三、Service 在清单文件中的声明

不管是哪一种的 service ，也都需要在 AndroidManifest.xml中声明  

```xml
 <service android:name=".myservice"
            android:enabled="true"
            android:exported="true"
            android:icon="@drawable/background_blue"
            android:label="string"
            android:process="string"
            android:permission="string">
 </service>
```
 field | description
 -- | -- 
android:exported	|表示是否允许除了当前程序之外的其他程序访问这个服务
android:enabled	|表示是否启用这个服务
android:permission	|是权限声明
android:process	|是否需要在单独的进程中运行,当设置为android:process=”:remote”时，代表Service在单独的进程中运行。注意“：”很重要，它的意思是指要在当前进程名称前面附加上当前的包名，所以“remote”和”:remote”不是同一个意思，前者的进程名称为：remote，而后者的进程名称为：App-packageName:remote。
android:isolatedProcess 	|设置 true 意味着，服务会在一个特殊的进程下运行，这个进程与系统其他进程分开且没有自己的权限。与其通信的唯一途径是通过服务的API(bind and start)。
 

## 四、Service 启动服务 以及 终止服务

首先要创建服务，必须创建 Service 的子类（或使用它的一个现有子类如 IntentService）。在实现中，我们需要重写一些回调方法，以处理服务生命周期的某些关键过程，下面我们通过简单案例来分析需要重写的回调方法有哪些？

```java
package com.example.jie.sign;
 
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.IntDef;
import android.support.annotation.Nullable;
import android.util.Log;
 
 
 
/**
 * Created by jie on 2018/9/15.
 */
 
public class myservice extends Service {
 
    private static final String TAG = "myservice";
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
 
    @Override
    public void onCreate() {
        Log.e(TAG, "onCreate:");
        super.onCreate();
    }
 
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.e(TAG, "onStartCommand:");
        return super.onStartCommand(intent, flags, startId);
    }
 
    @Override
    public void onDestroy() {
        Log.e(TAG, "onDestroy:");
        super.onDestroy();
    }
}
```

activity的点击事件 **启动** 以及 **关闭**

```java
    public void processClick(View v) {
        switch (v.getId()){
            case R.id.bt_demo:
                Intent start = new Intent(this,myservice.class);
                startService(start);
                break;
            case R.id.bt_demo1:
                Intent stop = new Intent(this,myservice.class);
                stopService(stop);
                break;
            default:
                break;
        }
    }
```

###### 下面结果为测试案例

下方操作流程：第一次启动服务- --》第二次调用启动服务---》第三次关闭服务--》第四次打开服务--》第五次打开服务

![](https://img-blog.csdn.net/20180919184915543?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTQ2MDY2Nw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

通过上面的操作案例我们可以得知，在我们第一次启动服务的时候，会执行 service 中的 oncreate 还有 onStartCommand(前提是服务在之前还没有进行启动) 否则只会单独调用 onStartCommand 方法 ，使用 stopservice() 就能够实现中断服务的启动。

###### 下面时启动服务还有中断服务的方式

- 启动
    ```java
    Intent start = new Intent(this,myservice.class);
    startService(start);
    ```

- 停止
    ```java
    Intent stop = new Intent(this,myservice.class);
    stopService(stop);
    ```

从上面的代码myservice继承了Service类，并重写了 `onBind` 方法，该方法是必须重写的，但是由于此时是启动状态的服务，则该方法无须实现，返回null即可，**只有在绑定状态的情况下**才需要实现该方法并返回一个IBinder的实现类（这个后面会详细说），接着重写了 onCreate、onStartCommand、onDestroy 三个主要的生命周期方法，关于这几个方法说明如下:

- [onBind()]()  
  当另一个组件想通过调用 bindService() 与服务绑定（例如执行 RPC）时，系统将调用此方法。在此方法的实现中，必须返回 一个IBinder 接口的实现类，供客户端用来与服务进行通信。无论是启动状态还是绑定状态，此方法必须重写，但在启动状态的情况下直接返回 null。

- [onCreate()]()  
  首次创建服务时，系统将调用此方法来执行一次性设置程序（在调用 onStartCommand() 或onBind() 之前）。如果服务已在运行，则不会调用此方法，该方法只调用一次

- [onStartCommand()]()  
  当另一个组件（如 Activity）通过调用 `startService()` 请求启动服务时，系统将调用此方法。一旦执行此方法，服务即会启动并可在后台无限期运行。 如果自己实现此方法，则需要在服务工作完成后，通过调用 `stopSelf()` 或 `stopService()` 来停止服务。（在绑定状态下，无需实现此方法。）

- [onDestroy()]()  
  当服务不再使用且将被销毁时，系统将调用此方法。服务应该实现此方法来清理所有资源，如线程、注册的侦听器、接收器等，这是服务接收的最后一个调用。

 

## 五、Service 绑定服务

通过第四节我们知道了启动和停止服务的基本方法，不知道你有没有发现，虽然 Service 是在 Activity 里启动的，但在启动了 Service 之后，Activity 与 Service 基本就没有了什么关系。确实如此，我们在活动里调用了 startService 方法之后启动 myservice 这个服务。然后 myservice 的 oncreate 和 onstartCommand 方法就会得到执行。之后服务会一直处于运行状态，但具体的运行的什么逻辑，活动就已经控制不了。那就是代表 ***我们无法通过组件对 Service 进行控制吗? 不不不 ，不是的***。这时候我们就要用到我们 service 中继承的另一个方法 `onbind` 方法。

绑定服务是 Service 的另一种变形，当 Service 处于绑定状态时，其代表着客户端-服务器接口中的服务器。当其他组件（如 Activity）绑定到服务时（有时我们可能需要从 Activity 组建中去调用Service中的方法，此时 Activity 以绑定的方式挂靠到 Service 后，我们就可以轻松地方法到 Service 中的指定方法），组件（如Activity）可以向 Service（也就是服务端）发送请求，或者调用 Service（服务端）的方法，此时被绑定的 Service（服务端）会接收信息并响应，甚至可以通过绑定服务进行执行进程间通信 (即IPC，这个后面再单独分析)。与启动服务不同的是绑定服务的生命周期通常只在为其他应用组件(如Activity)服务时处于活动状态，不会无限期在后台运行，也就是说宿主(如Activity)解除绑定后，绑定服务就会被销毁。

为了实现客户端与服务器的交互，我们一般都会通过下方**三种方式进行处理**。

- [扩展 Binder 类 ]()  
在service类中进行添加一个binder内部类，我们通过前台进行绑定后，当绑定后成功后，客户端收到binder 后，可利用他直接访问 Binder 实现中以及Service 中可用的公共方法。如果我们的服务只是自有应用的后台工作线程，则优先采用这种方法。前提：service服务端与客户端相同的进程中运行。

- [使用 Messenger ]()  
以后知道在补上，这是执行进程间通信 (IPC) 的最简单方法，因为 Messenger 会在单一线程中创建包含所有请求的队列，也就是说Messenger是以串行的方式处理客户端发来的消息，这样我们就不必对服务进行线程安全设计了。（小编未知，以后再进行补充）

- [使用 AIDL]()   
如果我们想让服务同时处理多个请求，则应该使用 AIDL。 在此情况下，服务必须具备多线程处理能力，并采用线程安全式设计。使用AIDL必须创建一个定义编程接口的 .aidl 文件。Android SDK 工具利用该文件生成一个实现接口并处理 IPC 的抽象类，随后可在服务内对其进行扩展。（小编未知，以后再进行补充）

上面介绍完对 service的各种绑定之后 ，我们接下去就是来说一下我们如何进行操作，首先我们先看一下扩展Binder类的实现方法。

### 扩展binder类

我们这里的目的就是为了使 `应用组件` 能够与应用的 `service` 服务进行交互。并且我们的服务仅供于本地服务的使用，不需要跨进程工作，然后我们就可以实现自有的 binder 类。

#### 流程如下

1. 创建 binder 子类，让前端能够通过 binder 类实现对 service 的调用。

2. service 中的 onBind 方法返回 binder 实例

3. 在 前端中的 onServiceConnected 中接收返回的 binder 实例。

###### myservice

```java
package com.example.jie.foreverdemo;
 
import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;
 
 
/**
 * Created by jie on 2018/9/15.
 */
 
public class myservice extends Service {
 
    private static final String TAG = "myservice";
    private LocalBinder mbinder = new LocalBinder();
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        Log.e(TAG, "onBind:" );
        return mbinder;
    }
 
    public class LocalBinder extends Binder{
        public myservice getservices(){
            return myservice.this;
        }
        public void start(){
            Log.e(TAG, "start:" );
        }
        public void end(){
            Log.e(TAG, "end:" );
        }
    }
 
    @Override
    public void onCreate() {
        Log.e(TAG, "onCreate:");
        super.onCreate();
    }
 
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.e(TAG, "onStartCommand:");
        return super.onStartCommand(intent, flags, startId);
    }
 
    @Override
    public void onDestroy() {
        Log.e(TAG, "onDestroy:");
        super.onDestroy();
    }
 
    public  String myway(){
        Log.e(TAG, "myway:hello world");
        return "hello world";
    }
 
    @Override
    public boolean onUnbind(Intent intent) {
        Log.e(TAG, "onUnbind:");
        return super.onUnbind(intent);
    }
}
```

###### 前端

```java
package com.example.jie.foreverdemo;
 
import android.app.Service;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.util.Log;
import android.view.View;
import android.widget.Button;
 
/**
 * Created by jie on 2018/9/19.
 */
 
public class DemoActivity extends BaseActivity {
    private myservice services;
 
    private ServiceConnection conn;
    private Button button1;
    private Button button2;
    private Button button3;
    private Button button4;
 
    private static final String TAG = "DemoActivity";
    @Override
    public int getLayoutId() {
        return R.layout.activity_demo;
    }
 
    @Override
    public void initViews() {
        button1 = findView(R.id.bt_demo);
        button2 = findView(R.id.bt_demo1);
        button3 = findView(R.id.btn_bind);
        button4 = findView(R.id.btn_unbind);
    }
 
    @Override
    public void initListener() {
        button2.setOnClickListener(this);
        button1.setOnClickListener(this);
        button3.setOnClickListener(this);
        button4.setOnClickListener(this);
    }
 
    /**
     * 里面主要是为了实现一个可以从service的回调接口
     */
    @Override
    public void initData() {
        conn = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
                myservice.LocalBinder binder = (myservice.LocalBinder) iBinder;
                binder.start();
                binder.end();
                services = binder.getservices();
                services.myway();
            }
 
            @Override
            public void onServiceDisconnected(ComponentName componentName) {
                services = null;
                Log.e(TAG, "onServiceDisconnected:");
            }
        };
    }
 
    @Override
    public void processClick(View v) {
        switch (v.getId()){
            case R.id.bt_demo:
                Intent start = new Intent(this,myservice.class);
                startService(start);
                break;
            case R.id.bt_demo1:
                Intent stop = new Intent(this,myservice.class);
                stopService(stop);
                break;
            case R.id.btn_bind:
                //绑定服务
                Intent intent = new Intent(this, myservice.class);
                bindService(intent,conn, Service.BIND_AUTO_CREATE);
                break;
            case R.id.btn_unbind:
                //解绑服务
                Intent intent1 = new Intent(this, myservice.class);
                unbindService(conn);
                break;
            default:
                break;
        }
    }
}
```

在上面代码中，我们在前端代码中实现了一个 ServiceConnection 接口，该接口有两个方法， onServiceConnected和onServiceDisconnected。

- onServiceConnected(ComponentName componentName, IBinder iBinder) 
  当我们进行绑定的时候，onbind() 方法会返回 binder 实例对象。进而我们可以对其进行调用。


- onServiceDisconnected(ComponentName componentName)
Android 系统会在与服务的连接意外中断时（例如当服务崩溃或被终止时）调用该方法。注意:当客户端取消绑定时，系统“绝对不会”调用该方法。

    ```java
    conn = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            myservice.LocalBinder binder = (myservice.LocalBinder) iBinder;
            binder.start();
            binder.end();
            services = binder.getservices();
            services.myway();
        }

        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            services = null;
            Log.e(TAG, "onServiceDisconnected:");
        }
    };
    ```

我们对服务的 `绑定` 还有 `解绑` 如下:

- 绑定  
    ```java
    //绑定服务
    Intent intent = new Intent(this, myservice.class);
    bindService(intent,conn, Service.BIND_AUTO_CREATE);
    ```
- 解绑  
    ```java
    //解绑服务
    Intent intent1 = new Intent(this, myservice.class);
    unbindService(conn);
    ```
loge 日志如下

前五行是进行绑定服务的 ，后面的是进行解绑



通过Log可知，当我们第一次点击绑定服务时，LocalService 服务端的 onCreate()、onBind 方法会依次被调用，此时客户端的 ServiceConnection#onServiceConnected() 被调用并返回 LocalBinder 对象，接着调用 LocalBinder#getService 方法返回 myservice 实例对象，此时客户端便持有了myservice 的实例对象，也就可以任意调用 myservice 类中的声明公共方法了。更值得注意的是，我们多次调用 bindService 方法绑定 LocalService 服务端，而 LocalService 得 onBind 方法只调用了一次，那就是在第一次调用 bindService 时才会回调 onBind 方法。

 

### 使用Messenger

前面我们了解通过扩展 Binder 类来进行通信。接下来我们就来介绍一下不同进程之间的通信，我们下面就是采用最简单的方式 Messenger 来进行通信，通过此来了解进程之间的通信，这也是最轻量级的方式。过程如下：

1. 在service中创建handler，然后通过这个 handler 创建 Messenger 对象。

2. 我们在客户端通过绑定 onBinder 函数返回 binder 对象，然后我们在创建出 Messenger 对象
  创建Messenger对象 **两种方式**
    - Messenger（Binder）；
    - Messenger（Handler）；

3. 通过 Messenger 发送信息  `mService.send(msg)`;
  message对象的创建方式：  
    - Message.obtain(null, MessageService.MSG_SAY_HELLO, 0, 0)
      - 第二个参数为 int 类型的变量以作为信息的区分。

下方高能出现 （案例代码）

###### service

```java
package com.example.jie.foreverdemo;
 
import android.app.Service;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.Toast;
 
/**
 * 服务端
 * Created by jie on 2018/9/28.
 */
 
public class MessageService extends Service {
    static final int MSG_SAY_HELLO = 1;
    private static final String TAG = "MessageService";
 
    class Localhandler extends Handler {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case MSG_SAY_HELLO:
                    Log.e(TAG, "handleMessage : accepted!");
                    //信息回馈
                    Messenger client = msg.replyTo;
                    Message replyMsg = Message.obtain(null, MessageService.MSG_SAY_HELLO,0,0);
                    Bundle bundle = new Bundle();
                    bundle.putString("reply", "ok~,I had receiver message from you! ");
                    replyMsg.setData(bundle);
                    try {
                        client.send(replyMsg);
                        Log.e(TAG, "handleMessage:" );
                    } catch (RemoteException e) {
                        e.printStackTrace();
                    }
                    break;
                default:
                    super.handleMessage(msg);
            }
        }
    }
 
    //通过IncomingHandler对象创建一个Messenger对象,该对象是与客户端交互的特殊对象
    final Messenger mMessenger = new Messenger(new Localhandler());
 
    /**
     * 当绑定Service时,该方法被调用,将通过mMessenger返回一个实现
     * IBinder接口的实例对象
     */
    @Override
    public IBinder onBind(Intent intent) {
        Log.e(TAG, "onBind:");
        return mMessenger.getBinder();
    }
}
```

###### 客户端：

```java
package com.example.jie.foreverdemo;
 
import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
 
import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.OnClick;
 
/**
 * 客户端
 * Created by jie on 2018/9/28.
 */
 
public class ActivityMessenger extends Activity implements View.OnClickListener {
 
    @BindView(R.id.bindservice)
    Button bindservice;
    @BindView(R.id.unbindservice)
    Button unbindservice;
    @BindView(R.id.sendmsg)
    Button sendmsg;
    /**
     * 与服务端交互的Messenger
     */
    Messenger mService = null;
    /**
     * Flag indicating whether we have called bind on the service.
     */
    boolean mBound;
    private static final String TAG = "MessageService";
    private ServiceConnection myConnection = new ServiceConnection() {
 
        @Override
        public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
            Log.e(TAG, "onServiceConnected: ");
            mService = new Messenger(iBinder);
            mBound = true;
        }
 
        @Override
        public void onServiceDisconnected(ComponentName componentName) {
            mService = null;
            mBound = false;
        }
    };
    /**
     * 用于接收服务器返回的信息
     */
    private Messenger mRecevierReplyMsg = new Messenger(new ReceiverReplyMsgHandler());
 
    private class ReceiverReplyMsgHandler extends Handler {
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                //接收服务端回复
                case MessageService.MSG_SAY_HELLO:
                    Log.e(TAG, "receiver message from service:" + msg.getData().getString("reply"));
                    break;
                default:
                    super.handleMessage(msg);
            }
        }
    }
 
    public void sayHello(View v) {
        if (!mBound) return;
        // 创建与服务交互的消息实体Message
        Message msg = Message.obtain(null, MessageService.MSG_SAY_HELLO, 0, 0);
        msg.replyTo = mRecevierReplyMsg;
        try {
            //发送消息
            mService.send(msg);
            Log.e(TAG, "sayHello:");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }
 
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_messenger);
        ButterKnife.bind(this);
        initClick();
    }
 
    private void initClick() {
//        @OnClick(R.id.bindservice)
        bindservice.setOnClickListener(this);
        unbindservice.setOnClickListener(this);
        sendmsg.setOnClickListener(this);
    }
 
    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.bindservice:
                Intent intent = new Intent(this, MessageService.class);
                bindService(intent, myConnection, Context.BIND_AUTO_CREATE);
                Toast.makeText(this, "我们都好", Toast.LENGTH_SHORT).show();
                break;
            case R.id.unbindservice:
                if (mBound) {
                    Log.e("zj", "onClick-->unbindService");
                    unbindService(myConnection);
                    mBound = false;
                }
                break;
            case R.id.sendmsg:
                sayHello(view);
                break;
            default:
                break;
        }
    }
 
    @Override
    protected void onDestroy() {
        super.onDestroy();
    }
}
```

对了 还有一点就是我们的目的是为了验证不同进程之间的通信，所以我们这里需要为服务重新设置一个的单独进程。

```xml
<service
    android:name=".MessageService"
    android:enabled="true"
    android:exported="true"
    android:process=":remote"></service>
```

对了，可能会有一部分小伙伴会想提问，那么如果我想重新从服务端发送信息给客户端那么我应该如何操作。

其实道理也还是一样的，我们只需跟上方一样进行相同的操作就能得到我们想要的结果。我们可以只要在我们发送信息给客户端把我们的客户端的 Messenger 对象也发送给 service 就可以了

- 客户端
    ```java
    Message msg = Message.obtain(null, MessageService.MSG_SAY_HELLO, 0, 0);
    msg.replyTo = mRecevierReplyMsg;
    ```
- 服务端
    ```java
    //信息回馈
    Messenger client = msg.replyTo;
    Message replyMsg = Message.obtain(null, MessageService.MSG_SAY_HELLO,0,0);
    Bundle bundle = new Bundle();
    bundle.putString("reply", "ok~,I had receiver message from you! ");
    replyMsg.setData(bundle);
    try {
        client.send(replyMsg);
        Log.e(TAG, "handleMessage:" );
    } catch (RemoteException e) {
        e.printStackTrace();
    }
    ```

我们通过客户端进行绑定服务-》发送信息 通过此我们得到如下的log日志。

###### 主线程日志

```log
09-28 17:51:06.273 20031-20031/com.example.jie.foreverdemo E/MessageService: onServiceConnected: 
09-28 17:51:12.790 20031-20031/com.example.jie.foreverdemo E/MessageService: sayHello:
09-28 17:51:12.808 20031-20031/com.example.jie.foreverdemo E/MessageService: receiver message from service:ok~,I had receiver message from you! 
```
###### remote线程日志

```log
09-28 17:51:06.264 20492-20492/com.example.jie.foreverdemo:remote E/MessageService: onBind:
09-28 17:51:12.793 20492-20492/com.example.jie.foreverdemo:remote E/MessageService: handleMessage : accepted!
09-28 17:51:12.793 20492-20492/com.example.jie.foreverdemo:remote E/MessageService: handleMessage:
```

###### Meeeenger 进程通信图

![](https://img-blog.csdn.net/20161004221152656)

#### 绑定的细节注意点

1. 多个客户端可同时连接到一个服务。不过，只有在第一个客户端绑定时，系统才会调用服务的 onBind() 方法来检索 IBinder。系统随后无需再次调用 onBind()，便可将同一 IBinder 传递至任何其他绑定的客户端。当最后一个客户端取消与服务的绑定时，系统会将服务销毁。

2. 通常情况下我们应该在客户端生命周期（如Activity的生命周期）的引入 (bring-up) 和退出 (tear-down) 时刻设置绑定和取消绑定操作，以便控制绑定状态下的Service，一般有以下两种情况：

    - 如果只需要在 Activity 可见时与服务交互，则应在 onStart() 期间绑定，在 onStop() 期间取消绑定。

    - 如果希望 Activity 在后台停止运行状态下仍可接收响应，则可在 onCreate() 期间绑定，在 onDestroy() 期间取消绑定。需要注意的是，这意味着 Activity 在其整个运行过程中（甚至包括后台运行期间）都需要使用服务，因此如果服务位于其他进程内，那么当提高该进程的权重时，系统很可能会终止该进程。

3. 应用组件（客户端）可通过调用 bindService() 绑定到服务,Android 系统随后调用服务的 onBind() 方法，该方法返回用于与服务交互的 IBinder，而该绑定是异步执行的。

 

## 六、关于启动服务与绑定服务之间的问题 

### 先绑定服务后启动服务

如果当前Service实例先以绑定状态运行，然后再以启动状态运行，那么绑定服务将会转为启动服务运行，这时如果之前绑定的宿主（Activity）被销毁了，也不会影响服务的运行，服务还是会一直运行下去，指定收到调用停止服务或者内存不足时才会销毁该服务。

### 先启动服务后绑定服务

如果当前Service实例先以启动状态运行，然后再以绑定状态运行，当前启动服务并不会转为绑定服务，但是还是会与宿主绑定，只是即使宿主解除绑定后，服务依然按启动服务的生命周期在后台运行，直到有Context调用了stopService()或是服务本身调用了stopSelf()方法抑或内存不足时才会销毁服务。

以上两种情况显示出启动服务的优先级确实比绑定服务高一些。

最后这里有点需要特殊说明一下的，由于服务在其托管进程的主线程中运行（UI线程），它既不创建自己的线程，也不在单独的进程中运行（除非另行指定）。 这意味着，如果服务将执行任何耗时事件或阻止性操作（例如 MP3 播放或联网）时，则应在服务内创建新线程来完成这项工作，简而言之，耗时操作应该另起线程执行。只有通过使用单独的线程，才可以降低发生“应用无响应”(ANR) 错误的风险，这样应用的主线程才能专注于用户与 Activity 之间的交互， 以达到更好的用户体验。

 

## 七、前台服务以及通知发送

服务几乎都是在后台运行的，一直以来他都是默默地做着辛苦的工作。但是服务的系统优先级还是比较低的，当系统出现内存不足的情况时，就有可能会回收正在后台运行的服务。如果你希望可以一直保持运行状态，而不会由于系统内存不足的原因导致被回收，就**可以考虑使用前台服务**。前台服务和普通服务最大的区别就在于，他会一直有一个正在运行的图标在系统的状态栏显示，下拉状态栏后可以看到更加详细的信息，非常类似于通知的效果。当然有时候你也可能不仅仅是为了防止服务被回收掉才用前台服务，有些项目也有可能有着这样的特殊要求。

### 不多说先介绍两个api先

- startForeground(NOTIFICATION_DOWNLOAD_PROGRESS_ID,notification);  
第一个参数为int数值，只要你不要使用两个相同的int就可以 ，第二个参数为弹框对象

- stopForeground(true);  
只有一个boolean参数 ，关闭弹框的出现。其余我直接上案例代码

###### 客户端

```java
package com.example.jie.foreverdemo;
 
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
 
/**
 * Created by jie on 2018/9/28.
 */
 
public class ForegroundActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_foreground);
        Button btnStart= (Button) findViewById(R.id.startForeground);
        Button btnStop= (Button) findViewById(R.id.stopForeground);
        final Intent intent = new Intent(this,ForegroundService.class);
 
 
        btnStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                intent.putExtra("cmd",0);//0,开启前台服务,1,关闭前台服务
                startService(intent);
            }
        });
 
 
        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                intent.putExtra("cmd",1);//0,开启前台服务,1,关闭前台服务
                startService(intent);
            }
        });
    }
 
 
}
```

###### 服务端

```java
package com.example.jie.foreverdemo;
 
import android.app.Notification;
import android.app.Service;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;
 
/**
 * Created by jie on 2018/9/28.
 */
 
public class ForegroundService extends Service {
    /**
     * id不可设置为0,否则不能设置为前台service
     */
    private static final int NOTIFICATION_DOWNLOAD_PROGRESS_ID = 0x0001;
 
    private boolean isRemove=false;//是否需要移除
 
    /**
     * Notification
     */
    public void createNotification(){
        //使用兼容版本
        NotificationCompat.Builder builder=new NotificationCompat.Builder(this);
        //设置状态栏的通知图标
        builder.setSmallIcon(R.mipmap.ic_launcher);
        //设置通知栏横条的图标
        builder.setLargeIcon(BitmapFactory.decodeResource(getResources(),R.mipmap.ic_launcher_round));
        //禁止用户点击删除按钮删除
        builder.setAutoCancel(false);
        //禁止滑动删除
        builder.setOngoing(true);
        //右上角的时间显示
        builder.setShowWhen(true);
        //设置通知栏的标题内容
        builder.setContentTitle("I am Foreground Service!!!");
        //创建通知
        Notification notification = builder.build();
        //设置为前台服务
        startForeground(NOTIFICATION_DOWNLOAD_PROGRESS_ID,notification);
    }
 
 
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        int i=intent.getExtras().getInt("cmd");
        if(i==0){
            if(!isRemove) {
                createNotification();
            }
            isRemove=true;
        }else {
            //移除前台服务
            if (isRemove) {
                stopForeground(true);
            }
            isRemove=false;
        }
 
        return super.onStartCommand(intent, flags, startId);
    }
 
    @Override
    public void onDestroy() {
        //移除前台服务
        if (isRemove) {
            stopForeground(true);
        }
        isRemove=false;
        super.onDestroy();
    }
 
 
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
```
前台服务就是这么的简单，好啦我们开始进行翻页了。

 

## 八、服务于service与线程的区别

### 两者概念的迥异

Thread 是程序执行的最小单元，它是分配CPU的基本单位，android系统中UI线程也是线程的一种，当然Thread还可以用于执行一些耗时异步的操作。

Service 是 Android 的一种机制，服务是运行在主线程上的，它是由系统进程托管。它与其他组件之间的通信类似于client和server，是一种轻量级的IPC通信，这种通信的载体是binder，它是在linux层交换信息的一种IPC，而所谓的Service后台任务只不过是指没有UI的组件罢了。

### 两者的执行任务迥异

在android系统中，线程一般指的是工作线程(即后台线程)，而主线程是一种特殊的工作线程，它负责将事件分派给相应的用户界面小工具，如绘图事件及事件响应，因此为了保证应用 UI 的响应能力主线程上不可执行耗时操作。如果执行的操作不能很快完成，则应确保它们在单独的工作线程执行。

Service 则是android系统中的组件，一般情况下它运行于主线程中，因此在Service中是不可以执行耗时操作的，否则系统会报ANR异常，之所以称Service为后台服务，大部分原因是它本身没有UI，用户无法感知(当然也可以利用某些手段让用户知道)，但如果需要让Service执行耗时任务，可在Service中开启单独线程去执行。

### 两者使用场景

当要执行耗时的网络或者数据库查询以及其他阻塞UI线程或密集使用CPU的任务时，都应该使用工作线程(Thread)，这样才能保证UI线程不被占用而影响用户体验。

在应用程序中，如果需要长时间的在后台运行，而且不需要交互的情况下，使用服务。比如播放音乐，通过Service+Notification方式在后台执行同时在通知栏显示着。

### 两者的真正关系

两者没有半毛钱关系。

***参考链接***  
- https://www.cnblogs.com/carlo/p/4947342.html

- https://blog.csdn.net/jiangwei0910410003/article/details/17008687

- https://blog.csdn.net/wei_chong_chong/article/details/52251193#commentBox

- https://www.cnblogs.com/perfy/p/3820502.html

 

## 九、管理服务的生命周期

![](https://img-blog.csdn.net/20161004164521384)

服务的整个生命周期从调用 onCreate() 开始起，到 onDestroy() 返回时结束。与 Activity 类似，服务也在 onCreate() 中完成初始设置，并在 onDestroy() 中释放所有剩余资源。例如，音乐播放服务可以在 onCreate() 中创建用于播放音乐的线程，然后在 onDestroy() 中停止该线程。

### 销毁的两种情况：

- 启动服务
该服务在其他组件调用 startService() 时创建，然后无限期运行，且必须通过调用 stopSelf() 来自行停止运行。此外，其他组件也可以通过调用 stopService() 来停止服务。服务停止后，系统会将其销毁。

- 绑定服务
该服务在另一个组件（客户端）调用 bindService() 时创建。然后，客户端通过 IBinder 接口与服务进行通信。客户端可以通过调用 unbindService() 关闭连接。多个客户端可以绑定到相同服务，而且当所有绑定全部取消后，系统即会销毁该服务。 （服务不必自行停止运行）

 

## 十、Android 5.0 以上的隐式启动问题

### 显隐存在的意义 
如果在同一个应用中，两者都可以用。在不同应用时，只能用隐式启动

 

### 显示启动

直接上代码一目了然，不解释了。

```JAVA
//显示启动
Intent intent = new Intent(this,ForegroundService.class);
startService(intent);
```

### 隐式启动

需要设置一个 `Action`，我们可以把 Action 的名字设置成 ***Service的全路径名字***，在这种情况下 `android:exported` 默认为 true。如下
```xml
<service  
    android:name="com.dbjtech.acbxt.waiqin.UploadService"  
    android:enabled="true" >  
 
    <intent-filter android:priority="1000" >  
        <action android:name="com.dbjtech.myservice" />  
    </intent-filter>  
 
</service> 
```

```java
final Intent serviceIntent=new Intent(); 
serviceIntent.setAction("com.android.ForegroundService");
serviceIntent.setPackage(getPackageName());//设置应用的包名
startService(serviceIntent);
``` 
好啦 显隐式的介绍也就到此结束了 谢谢，下面就是本节的最后一点

 

## 十一、如何保证服务不会被杀死

- 返回 start_ticky

当 Service 因内存不足而被系统 kill 后，一段时间后内存再次空闲时，系统将会尝试重新创建此Service，一旦创建成功后将回调 onStartCommand 方法，但其中的 Intent 将是null，除非有挂起的Intent，如pendingintent，这个状态下比较适用于不执行命令、但无限期运行并等待作业的媒体播放器或类似服务。

```java
/**
 * 返回 START_STICKY或START_REDELIVER_INTENT
 * @param intent
 * @param flags
 * @param startId
 * @return
 */
@Override
public int onStartCommand(Intent intent, int flags, int startId) {
    // return super.onStartCommand(intent, flags, startId);
    return START_STICKY;
}
``` 

- 提高service的优先权

```xml
<service  
    android:name="com.dbjtech.acbxt.waiqin.UploadService"  
    android:enabled="true" >  
 
    <intent-filter android:priority="1000" >  
        <action android:name="com.dbjtech.myservice" />  
    </intent-filter>  
 
</service> 
```


 

## 最后

大部分模仿并参考下列文章  
https://blog.csdn.net/javazejian/article/details/52709857#t9  
