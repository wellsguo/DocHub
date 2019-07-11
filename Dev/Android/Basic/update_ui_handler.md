# 问答 Handler

<span id="top">目录</span>

#### Q1 : 什么是 handler ？ 在 Android 开发中扮演什么样的作用？

[**龙西岳@慕课网：**](https://www.imooc.com/article/25134?block_id=tuijian_wz) Handler 主要用于异步消息的处理： 有点类似辅助类，封装了消息投递、消息处理等接口。当发出一个消息之后，首先进入一个消息队列，发送消息的函数即刻返回，而另外一个部分在消息队列中逐一将消息取出，然后对消息进行处理，也就是发送消息和接收消息不是同步的处理。 这种机制通常用来处理相对耗时比较长的操作。

[**我的观点：**]() Handler 用于 Android 的异步 UI 更新，他就是一个游离于 UI 主线程和工作线程之间的一个特使或特工。首先在主线程中创建，然后在子线程中调用发送消息，最后在主线程中又根据返回的信息完成相应的处理。

###### STEP1 : 创建 Handler 

```java
private Handler handler = new Handler(){
    @Override
    public void handleMessage(Message msg) {
        super.handleMessage(msg);
        switch (msg.what) {
            case 1:
                // todo: 获取数据，更新UI
                break;
        }
    }
};
```

###### STEP2 : 子线程发送消息
```java
public class WorkThread extends Thread {
    @Override
    public void run() {
        super.run();
        // todo: 耗时操作
        Message msg =Message.obtain(); 
        msg.obj = data;
        msg.what = 1;
        handler.sendMessage(msg);
    }
}

new WorkThread().start();
```

###### STEP3 : 主线程 MessageQueue 分发并调用相应的 Handler 执行 handler.handlerMessage(msg) 

##### Q2 : 为什么要用handler？

[**龙西岳@慕课网：**](https://www.imooc.com/article/25134?block_id=tuijian_wz) 为什么要用handler？不用这种机制行不行？不行！android在设计的时候，就封装了一套消息的**创建、传递、处理**机制，如果不遵循这种机制，就没有办法更新 UI 信息，就会抛出异常信息。

##### Q3 : Handler 怎么用？

###### Android 相关 API
 - handlerMessage(Message message)
 - handler.postXXX(Runable...)
 - handler.sendMessageXXXX(Message...)
 - handler.removeXXX

#### Q4 : Android 为什么要设计只能通过 handler 机制更新 UI？

[**龙西岳@慕课网：**](https://www.imooc.com/article/25134?block_id=tuijian_wz) 最根本的目的是**解决多线程并发温问题**：
- 如果在一个 activity 当中，有多个线程去更新 UI，并且都没有加锁机制，那么会什么样子的问题？更新界面混乱。
- 如果对更新 UI 的操作都进行加锁处理的话又会产生什么样子的呢？性能下降。

出于对以上问题的考虑，Android 给我们提供了一套更新UI的机制，我们只要遵循这个机制就可以了，根本不用去关心多线程并发的问题，所有的更新UI的操作，都是在主线程的消息队列中去轮训处理的。

#### Q5 : Handler 的原理是什么?

[**龙西岳@慕课网：**](https://www.imooc.com/article/25134?block_id=tuijian_wz) 

##### Looper
1. 内部包含一个消息对列，也就是MessageQueue，所有的handler发送的消息都走向这个消息对列。
2. Loopler.looper方法，就是一个死循环，不断地从MessageQueue取消息，如果有消息就处理消息，没有消息就阻塞

##### MessageQueue
  就是一个消息对列，可以添加消息，并处理消息  

##### handler 
  handler 也很简单，内部会跟 Looper 进行关联，也就是说在 handler 的内部可以找到 Looper，找到 Looper 也就找到了 MessageQueue，在 handler 中发送消息，其实就是向 MessageQueue 队列中发送消息

总结：handler负责发送消息，Looper负责接收handler发送的消息，并直接把消息回传给handler自己。MessageQueue就是一个存储消息的容器

#### Q6 : 使用handler时候遇到的问题?

#### Q7 : 如何实现一个与线程相关的Handler？

#### Q8 : HandlerThread又是什么？

#### Q9 : 如何在主线程给子线程发送消息呢？

#### Q10 : android中更新UI的几种方式？

#### Q11 : 非UI线程真的不能更新UI吗？

#### Q12 : 使用handler时遇到的问题？

[TOP](#top)

## more

https://www.cnblogs.com/cheneasternsun/p/5467115.html  
https://segmentfault.com/a/1190000005926314  
http://ivanfan.site/2016/07/17/Handler_2/  
https://juejin.im/entry/57fc9e937db2a20059628aa6?utm_source=gold-miner&utm_medium=readme&utm_campaign=github  
