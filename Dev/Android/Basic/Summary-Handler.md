## Handler使用例1

这个例子是最简单的介绍 handler 使用的, 是将 handler 绑定到它所建立的线程中.

本次实验完成的功能是:

- 单击Start按钮，程序会开始启动线程，并且线程程序完成后延时1s会继续启动该线程，每次线程的run函数中完成对界面输出 `UpdateThread...` 文字，不停的运行下去;
- 当单击End按钮时，该线程就会停止，如果继续单击Start，则文字又开始输出了。


### MainActivity.java

```java
public class MainActivity extends Activity {
    private TextView text_view = null;
    private Button start = null;
    private Button end = null;

    //使用handler时首先要创建一个handler
    Handler handler = new Handler();

    //要用handler来处理多线程可以使用runnable接口，这里先定义该接口
    //线程中运行该接口的run函数
    Runnable update_thread = new Runnable(){
        public void run(){
            //线程每次执行时输出"UpdateThread..."文字,且自动换行
            //textview的append功能和Qt中的append类似，不会覆盖前面
            //的内容，只是Qt中的append默认是自动换行模式
            text_view.append("\nUpdateThread...");
            //延时1s后又将线程加入到线程队列中
            handler.postDelayed(update_thread, 1000);
        }
    };

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        text_view = (TextView)findViewById(R.id.text_view);
        start = (Button)findViewById(R.id.start);
        start.setOnClickListener(new StartClickListener());
        end = (Button)findViewById(R.id.end);
        end.setOnClickListener(new EndClickListener());

    }

    private class StartClickListener implements OnClickListener{
        public void onClick(View v) {
            //将线程接口立刻送到线程队列中
            handler.post(update_thread);
        }                
    }

    private class EndClickListener implements OnClickListener{
        public void onClick(View v) {
            //将接口从线程队列中移除
            handler.removeCallbacks(update_thread);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
```



 
## Handler 使用例2
这个例子比刚才那个例子稍微复杂些。因为这个例子中用到了handler的消息队列机制，即通过handler中一个线程向消息队列中用sendMessage方法发送消息，发送的消息当然可以用来传递参数。在handler中用handleMessage来处理消息，处理方法是获得消息队列中的消息参数，用这些参数来完成另外一些功能。
本实验实现的是当开始按钮按下时，会启动一个线程，并绑定到handler中，该线程发送带有参数的message到handler的消息队列中，消息队列的另一端获取该消息，并且用该消息的参数来更新进度条。





单击Start按钮后，更新的进度条结果如下



### MainActivity.java

```java
public class MainActivity extends Activity {
    private ProgressBar progress_bar = null;
    private Button start = null;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        progress_bar = (ProgressBar)findViewById(R.id.progress_bar);
        start = (Button)findViewById(R.id.start);

        start.setOnClickListener(new StartOnClickListenr());
    }

    private class StartOnClickListenr implements OnClickListener
    {
        public void onClick(View v) {
            //让进度条显示出来
            progress_bar.setVisibility(View.VISIBLE);
            //将线程加入到handler的线程队列中
            update_progress_bar.post(update_thread);

        }
    }
    //创建一个handler，内部完成处理消息方法
    Handler update_progress_bar = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            // TODO Auto-generated method stub
            //super.handleMessage(msg);
            //显示进度条
            progress_bar.setProgress(msg.arg1);
            //重新把进程加入到进程队列中
            update_progress_bar.post(update_thread);
        }       
    };//不加这个分号则不能自动添加代码

    Runnable update_thread = new Runnable(){
        int i = 0;
        public void run() {
            // TODO Auto-generated method stub
            i += 10;
            //首先获得一个消息结构
            Message msg = update_progress_bar.obtainMessage();
            //给消息结构的arg1参数赋值
            msg.arg1 = i;
            //延时1s，java中的try+catch用来排错处理
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                // TODO: handle exception
                e.printStackTrace();
            }
            //把消息发送到消息队列中
            update_progress_bar.sendMessage(msg);
            if(i == 100)
                //把线程从线程队列中移除
                update_progress_bar.removeCallbacks(update_thread);
        }       
    };

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
```






## Handler使用例3

上面2个例子表面上看handler使用了post方法启动了runnbale，其实启动的线程和activity主线程是同一个线程，因为它只是运行了线程的run方法，而不是start方法。Mars老师实验3的目的是为了验证仅使用handler的post方法是否处于同一个线程。

该实验在主activtiy的onCreate函数中打印了2条关于本线程的信息，然后创建一个handler并为它绑定一个线程，在线程的run方法中也打印了线程的信息，观察2者的信息是否一样。

结果如下：  
说明这2个线程确实是同一线程，并且可以看出主界面中的文字大概过了10s才显示出来，因为语句setContentView(R.layout.activity_main);放在了handler的post启动语句后面，而handler绑定的线程中又延时了10s，所以同时也证明了只有是同一个线程才会出现这种情况。


MainActivity.java:

```java
package com.example.handler3;

public class MainActivity extends Activity {
    //新建一个handler
    private Handler handler = new Handler();
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //将runnable加载到handler的线程队列中去
      //  handler.post(r);        
        Thread t = new Thread(r);
        t.start();
        setContentView(R.layout.activity_main);
        //打印activtiy线程信息
        System.out.println("activity_id---->"+Thread.currentThread().getId());
        System.out.println("activity_name---->"+Thread.currentThread().getName());
    }

    Runnable r = new Runnable(){
        public void run() {
            // TODO Auto-generated method stub
            //打印新建线程信息
            System.out.println("handler_id---->"+Thread.currentThread().getId());
            System.out.println("handler_name---->"+Thread.currentThread().getName());
            //延时10s，为了观察主界面中内容出现的时间
            try {
                Thread.sleep(10000);
            } catch (InterruptedException e) {
                // TODO: handle exception
                e.printStackTrace();
            }
        }

    };


}
```
如果把语句：
handler.post(r);
换成：
Thread t = new Thread(r);
t.start();
其它的不变，则程序运行时主界面内容立刻就显示出来了，且系统输出如下：
这2者都说明这样绑定的线程与它所在的activity线程就不是同一个线程了。





## Handler使用例4
这个例子将学会怎样不使用runnable来启动一个线程，而是**用 HandlerThread 的 looper 来构造一个handler**，然后该handler自己获得消息，并传递数据，然后又自己处理消息，当然这是在另一个线程中完成的。
消息结构中传递简单的整型可以采用它的参数arg1和arg2，或者传递一些小的其它数据，可以用它的object，该object可以是任意的对象。当需要传送比较大的数据是，可以使用消息的setData方法，该方法需要传递一个Bundle的参数。Bundle中存放的是键值对的map，只是它的键值类型和数据类型比较固定而已。

程序主要代码和注释如下：
MainActivity.java:

```java
package com.example.handler4;

public class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        System.out.println("activity_ID---->"+Thread.currentThread().getId());
        //新建一个HanderThread对象，该对象实现了用Looper来处理消息队列的功能
        HandlerThread handler_thread = new HandlerThread("handler_thread");
        handler_thread.start();
        //MyHandler类是自己继承的一个类，这里采用hand_thread的Looper来初始化它
        MyHandler my_handler = new MyHandler(handler_thread.getLooper());
        //获得一个消息msg
        Message msg = my_handler.obtainMessage();

        //采用Bundle保存数据，Bundle中存放的是键值对的map，只是它的键值类型和数据类型比较固定而已
        Bundle b = new Bundle();
        b.putString("whether", "晴天");
        b.putInt("temperature", 34);
        msg.setData(b);
      //将msg发送到自己的handler中，这里指的是my_handler,调用该handler的HandleMessage方法来处理该mug
        msg.sendToTarget();
    }
    
    class MyHandler extends Handler{
        //空的构造函数
        public MyHandler(){}
        
        //以Looper类型参数传递的函数，Looper为消息泵，不断循环的从消息队列中得到消息并处理，因此
        //每个消息队列都有一个Looper，因为Looper是已经封装好了的消息队列和消息循环的类
        public MyHandler(Looper looper){
            super(looper);
        }
        @Override
        public void handleMessage(Message msg) {
            System.out.println("Handler_ID---->"+Thread.currentThread().getId());
            System.out.println("Handler_Name---->"+Thread.currentThread().getId());
            //将消息中的bundle数据取出来
            Bundle b = msg.getData();
            String whether = b.getString("whether");
            int temperature = b.getInt("temperature");
            System.out.println("whether= "+whether+" ,temperature= "+temperature);
        }

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
```

## 总结
Android中的handler可以用来完成异步的消息出来，即发送消息和接收消息相互独立，可以同时运行。
- 在例1和例2中，实际上handler中使用的线程是与它所在的activity处于同一个主线程，因为handler中调用的runnable接口是直接运行该接口的run函数的，而不是start函数。
- 例3专门比较了这2中情况。
- 例4学会使用**怎样在新线程中处理消息的方法**。

## Android：异步处理之Handler+Thread的应用（一）



- 不要在UI主线程中进行耗时操作
- 不要在子线程中更新UI界面
- 利用Thread+Handler进行异步处理
- handler.post/view.post 简化操作  
每次都重写handlerMessage()比较麻烦，完全可以用更加简略的方法来解决我们的需求，就是用handler中的post方法。

  ```java
new Thread(){
　　@Override
　　public void run() {
　　　　//在子线程中进行下载操作
　　　　try {
　　　　　　Thread.sleep(1000);
　　　　} catch (InterruptedException e) {
　　　　　　e.printStackTrace();
　　　　}
　　　　handler.post(new Runnable() {
　　　　　　@Override
　　　　　　public void run() {
　　　　　　　　text.setText("下载完成");
　　　　　　}
　　　　});//发送消失到handler，通知主线程下载完成
　　}
}.start();
```

  这样处理的话我们就可以不用重写handlerMessage()方法了，**适合子线程与主线程进行较为单一的交流**。但在这里我们要强调的一点的是，**post里面的Runnable还是在UI主线程中运行的**，而不会另外开启线程运行，千万不要在 Runnable 的 run()里面进行耗时任务，不然到时又ANR了可别找我哦。。

  如果你有时候连handler都不想搞，还可以这样写代码滴。

  我们只需要把handler换成View组件进行post，更新任务自然会加载到UI主线程中进行处理。

  ```java
text.post(new Runnable() {
　　@Override
　　public void run() {
　　　　text.setText("下载完成");
　　}
});//发送消失到handler，通知主线程下载完成
```

## [安全 Handler](https://blog.csdn.net/cau_eric/article/details/88059075 )

```java
class MyHandler extends Handler {
    private WeakReference<MyLayoutActivity> mActivityRef;

    public MyHandler(MyLayoutActivity activity) {
        mActivityRef = new WeakReference<>(activity);
    }

    @Override
    public void handleMessage(Message msg) {
        MyLayoutActivity activity = mActivityRef.get();
        switch (msg.what) {
            case GETLAYOUTINFO:
                parseJsonWithJsonObject(activity.mResponse, 1);
                break;

        }
    }
}
```
这样,就可以避免内存泄露啦,记下来,方便查找!

```java
private final MyHandler mHandler = new MyHandler(this);
```

