## [handler 中 post 一个 runnable 问题](https://dennies211.iteye.com/blog/1172235)

Runnable 并不一定是新开一个线程，比如下面的调用方法就是运行在UI主线程中的： 

```java
Handler mHandler=new Handler(); 
mHandler.post(new Runnable(){ 
    @Override 
    public void run() { 
        // TODO Auto-generated method stub 
    } 
});
```

> 官方对这个方法的解释如下，注意其中的：**“The runnable will be run on the user interface thread. ”** 

```
boolean android.view.View.post(Runnable action) 
    Causes the Runnable to be added to the message queue. The runnable will be run on the user interface thread. 

Parameters: 
    action The Runnable that will be executed. 
Returns: 
    Returns true if the Runnable was successfully placed in to the message queue. Returns false on failure, usually because the looper processing the message queue is exiting. 
```


## [说说 getMainLooper](https://blog.csdn.net/icodeyou/article/details/49556765)

关于 Handler、Looper、MessageQueue，我想大家都了解的差不多了，简单来说就是一个 Handler 对应一个 Looper，一个 Looper 对应一个 Message。那么再想个问题，一个 Handler 可以对应多个 Looper 吗？ 一个 Looper 可以对应多个 Handler 吗？

之所以会提出上面这个问题，主要是因为在看 Looper 的源码时，发现了其中的 getMainLooper 这个方法，从名字可以看出是获取主线程的 Looper，那么为什么要特别提供这个方法呢？首先看一下这个方法的源码，很简单：

```java
    /*
     * 返回应用主线程中的 Looper
     */
    public static Looper getMainLooper() {
        synchronized (Looper.class) {
            return sMainLooper;
        }
    }
```
其实我们平时最常用的是无构造参数的 Handler，其实 Handler 还有构造参数的构造方法，如下：

```java
    public Handler(Looper looper, Callback callback, boolean async) {
        mLooper = looper;
        mQueue = looper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }
```

在此注意构造函数中第一个参数是 Looper 就可以了，那么也就是说，我们可以传递一个已有的 Looper 来创建 Handler。这里先不写示例代码了，填个坑，以后有时间再写，大概是下面这样：

```java
    Handler handler = new Handler(Looper.getMainLooper()){
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
        }
    };
```

注意上面的 Looper.getMainLooper()，将主线程中的 Looper 扔进去了，也就是说 handleMessage 会运行在主线程中，那么这样有什么用呢？**这样可以在主线程中更新 UI 而不用把 Handler 定义在主线程中**。

当然刚才提到的作用只是对应于主线程中的 sMainLooper 了，其实各种 Looper 都可以往 Handler 的构造方法这里扔，从而使得 handleMessage 运行在你想要的线程中，进而实现线程间通信。

那么想到另一篇文章 *[HandlerThread源码解析](http://icodeyou.com/2015/10/11/2015-10-11-HandlerThread%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/)* 中 HandlerThread#getLooper() 的作用了吗？

文章开头也提到了一个问题，那么答案就应该是：一个 Handler 中只能有一个 Looper，而一个 Looper 则可以对应多个 Handler，只要把 Looper 往 Handler 的构造方法里扔扔扔就好了。

今天再看了看 AsyncTask 的源码，发现其中也用到了 getMainLooper()，来更新 UI，源码如下：

```java
private static class InternalHandler extends Handler {
        public InternalHandler() {
            // 使用主线程的 Looper 扔给 Handler
            super(Looper.getMainLooper());
        }
}
```

## [Handler一定要在主线程实例化吗](https://blog.csdn.net/thanklife/article/details/17006865)

### Handler一定要在主线程实例化吗?

`new Handler()` 和 `new Handler(Looper.getMainLooper())`的区别

如果你不带参数的实例化：

```java
Handler handler = new Handler();
```
那么这个会默认用当前线程的looper  
一般而言，如果你的Handler是要来刷新操作UI的，那么就需要在主线程下跑。

情况:
- 1.**要刷新UI**，handler 要用到主线程的looper。那么  
  - 在主线程   
```java
Handler handler = new Handler();
``` 
  - 在其他线程 
```java
Handler handler = new Handler(Looper.getMainLooper());
```

- 2.**不用刷新ui, 只是处理消息**。 
   - 当前线程是主线程
```java
Handler handler = new Handler();
```

  - 当前线程不是主线程
```java
Looper.prepare(); 
Handler handler = new Handler();
Looper.loop();
```
或者
```java
Handler handler = new Handler(Looper.getMainLooper());
```
若是实例化的时候用 `Looper.getMainLooper()` 就表示放到主UI线程去处理。
如果不是的话，因为只有UI线程默认 `Loop.prepare();Loop.loop();` 过，其他线程需要手动调用这两个，否则会报错。


### message.what,message.arg1,message.arg2,message.obj，他们在之间有什么区别呢？

- what 就是一般用来区别消息的，比如你传进去的时候msg.what = 3;
然后处理的时候判断msg.what == 3是不是成立的，是的话，表示这个消息是干嘛干嘛的（自己能区别开）

- arg1,arg2，其实也就是两个传递数据用的，两个int值，看你自己想要用它干嘛咯。如果你的数据只是简单的int值，那么用这两个，比较方便。  
其实这里你还少说了个，setData(Bundle),上面两个arg是传递简单int的，这个是传递复杂数据的。

- msg.obj呢，这个就是传递数据了，msg中能够携带对象，在handleMessage的时候，可以把这个数据取出来做处理了。不过呢，如果是同一个进程，最好用上面的setData就行了，这个一般是Messenger类来用来跨进程传递可序列化的对象的，这个比起上面的来，更消耗性能一些。

```java

public class HandlerActivity extends AppCompatActivity {
 
    private static final String TAG = "Handler";
 
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_handler2);
 
        Handler mainHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                Log.i(TAG, "mainHandler handle message");
            }
        };
 
 
       Thread thread = new Thread(new Runnable() {
 
            @Override
            public void run() {
                Handler handler = new Handler(Looper.getMainLooper()) {
                    @Override
                    public void handleMessage(Message msg) {
                        Log.i(TAG, "threadHandler handle message");
                        Toast.makeText(HandlerActivity.this, "test", Toast.LENGTH_SHORT).show();
                    }
                };
                Message message = Message.obtain(handler);
                message.sendToTarget();
            }
        });
        thread.start();
    }
```

## 小结
要利用 Handler 实现 UI 更新，可以通过在 UI 线程中创建 Handler 并 覆写 handleMessage 方法。 或者在非 UI 线程中利用 view.post(Runnable) 或 new Handler(Looper.getMainLooper()) 创建 Handler 实例再调用 handler.sendMessage(message).


