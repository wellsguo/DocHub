# Java 异步实现的几种方式

> 很多时候我们都希望能够最大的利用资源，比如在进行 IO 操作的时候尽可能的避免同步阻塞的等待，因为这会浪费 CPU 的资源。如果在有可读的数据的时候能够通知程序执行读操作甚至由操作系统内核帮助我们完成数据的拷贝，这再好不过了。从`NIO` 到 `CompletableFuture`、`Lambda`、`Fork/Join`，java 一直在努力让程序尽可能变的异步甚至拥有更高的并行度，这一点一些函数式语言做的比较好，因此 java 也或多或少的借鉴了某些特性。下面介绍一种非常常用的实现异步操作的方式。

### 1. JDK 1.8 之前的 Future

考虑有一个耗时的操作，操作完后会返回一个结果（不管是正常结果还是异常），程序如果想拥有比较好的性能不可能由线程去等待操作的完成，而是应该采用 `listener` 模式。JDK 并发包里的 Future 代表了未来的某个结果，当我们向线程池中提交任务的时候会返回该对象，可以通过 Future 获得执行的结果，但是 JDK 1.8 之前的 Future 有点鸡肋，并不能实现真正的异步，需要阻塞的获取结果，或者不断的轮询。

通常我们希望当线程执行完一些耗时的任务后，能够自动的通知我们结果，很遗憾这在原生 JDK 1.8 之前是不支持的，但是我们可以通过第三方的库实现真正的异步回调。

```java
/**
 * jdk1.8之前的Future
 * @author Administrator
 */
public class JavaFuture {
	public static void main(String[] args) throws Throwable, ExecutionException {
		ExecutorService executor = Executors.newFixedThreadPool(1);
    // Future代表了线程执行完以后的结果，可以通过future获得执行的结果
	  // 但是jdk1.8之前的Future有点鸡肋，并不能实现真正的异步，需要阻塞的获取结果，或者不断的轮询
	  // 通常我们希望当线程执行完一些耗时的任务后，能够自动的通知我们结果，很遗憾这在原生jdk1.8之前
	  // 是不支持的，但是我们可以通过第三方的库实现真正的异步回调
		Future<String> f = executor.submit(new Callable<String>() {

			@Override
			public String call() throws Exception {
				System.out.println("task started!");
				longTimeMethod();
				System.out.println("task finished!");
				return "hello";
			}
		});

		//此处get()方法阻塞main线程
		System.out.println(f.get());
		System.out.println("main thread is blocked");
	}
}
```

如果想获得耗时操作的结果，可以通过`get()`方法获取，但是该方法会阻塞当前线程，我们可以在做完剩下的某些工作的时候调用`get()`方法试图去获取结果。

也可以调用非阻塞的方法`isDone`来确定操作是否完成，`isDone`这种方式有点儿类似下面的过程：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190103145647255.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzUyNTExNg==,size_16,color_FFFFFF,t_70)

这种方式对流程的控制很混乱，但是在 jdk1.8 之前只提供了这种笨拙的实现方式，以至于很多高性能的框架都实现了自己的一套异步框架，比如 Netty 和 Guava，下面分别介绍下这三种异步的实现方式（包括 jdk1.8）。首先是 Guava 中的实现方式：

```java
package guava;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

/**
 * Guava中的Future
 *
 * @author Administrator
 *
 */
public class GuavaFuture {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(1);
        // 使用guava提供的MoreExecutors工具类包装原始的线程池
        ListeningExecutorService listeningExecutor = MoreExecutors.listeningDecorator(executor);
        //向线程池中提交一个任务后，将会返回一个可监听的Future，该Future由Guava框架提供
        ListenableFuture<String> lf = listeningExecutor.submit(new Callable<String>() {
            @Override
            public String call() throws Exception {
                System.out.println("task started!");
                //模拟耗时操作
                Thread.sleep(3000);
                System.out.println("task finished!");
                return "hello";
            }
        });
        //添加回调，回调由executor中的线程触发，但也可以指定一个新的线程
        Futures.addCallback(lf, new FutureCallback<String>() {
            //耗时任务执行失败后回调该方法
            @Override
            public void onFailure(Throwable t) {
                System.out.println("failure");
            }

            //耗时任务执行成功后回调该方法
            @Override
            public void onSuccess(String s) {
                System.out.println("success " + s);
            }
        });

        //主线程可以继续做其他的工作
        System.out.println("main thread is running");
    }
}
```

Guava 提供了一套完整的异步框架，核心是可监听的 Future，通过注册监听器或者回调方法实现及时获取操作结果的能力。需要提一点的是，假设添加监听的时候耗时操作已经执行完了，此时回调方法会被立即执行并不会丢失。想探究其实现方式的话可以跟一下源码，底层的原理并不难。

谈到异步编程就不得不提一下 Promise，很多函数式语言比如 js 原生支持 Promise，但是在 java 界也有一些 promise 框架，其中就有大名鼎鼎的 Netty。从 Future、Callback 到 Promise 甚至线程池，Netty 实现了一套完整的异步框架，并且 netty 代码中也大量使用了 Promise，下面是 Netty 中的例子：

```java
package netty_promise;

import io.netty.util.concurrent.DefaultEventExecutorGroup;
import io.netty.util.concurrent.EventExecutorGroup;
import io.netty.util.concurrent.Future;
import io.netty.util.concurrent.FutureListener;

/**
 * netty中的promise
 *
 * @author Administrator
 *
 */
public class PromiseTest {
   @SuppressWarnings({ "unchecked", "rawtypes" })
   public static void main(String[] args) throws Throwable {
        //线程池
        EventExecutorGroup group = new DefaultEventExecutorGroup(1);
        //向线程池中提交任务，并返回Future，该Future是netty自己实现的future
        //位于io.netty.util.concurrent包下，此处运行时的类型为PromiseTask
        Future<?> f = group.submit(new Runnable() {
            @Override
            public void run() {
            System.out.println("任务正在执行");
            //模拟耗时操作，比如IO操作
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("任务执行完毕");
            }
        });
        //增加监听
        f.addListener( new FutureListener() {
            @Override
            public void operationComplete(Future arg0) throws Exception {
                System.out.println("ok!!!");
            }
        });
        System.out.println("main thread is running.");
    }
}
```

### 2. JDK 1.8 开始的 Future

直到 JDK 1.8 才算真正支持了异步操作，JDK 1.8 中提供了`lambda`表达式，使得 JAVA 向函数式语言又靠近了一步。借助 JDK 原生的`CompletableFuture`可以实现异步的操作，同时结合`lambada`表达式大大简化了代码量。代码例子如下：

```java
package netty_promise;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Supplier;

/**
 * 基于jdk1.8实现任务异步处理
 * @author Administrator
 */
public class JavaPromise {
	public static void main(String[] args) throws Throwable, ExecutionException {
		// 两个线程的线程池
		ExecutorService executor = Executors.newFixedThreadPool(2);
		//  jdk1.8之前的实现方式
		CompletableFuture<String> future = CompletableFuture.supplyAsync(new Supplier<String>() {
			@Override
			public String get() {
				System.out.println("task started!");
				try {
					//模拟耗时操作
					longTimeMethod();
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				return "task finished!";
			}
		}, executor);

		// 采用lambada的实现方式
		future.thenAccept(e -> System.out.println(e + " ok"));

		System.out.println("main thread is running");
	}
}
```

实现方式类似下图：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190103150252949.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzUyNTExNg==,size_16,color_FFFFFF,t_70)

### 3. Spring 的异步方法

先把 longTimeMethod 封装到 Spring 的异步方法中，这个异步方法的返回值是 Future 的实例。这个方法一定要写在 Spring 管理的类中，注意注解@Async。

```java
@Service
public class AsynchronousService{
    @Async
    public Future springAsynchronousMethod(){
        Integer result = longTimeMethod();
        return new AsyncResult(result);
    }
}
```

其他类调用这个方法。这里注意，一定要其他的类，如果在同类中调用，是不生效的。

```java
@Autowired
private AsynchronousService asynchronousService;

public void useAsynchronousMethod(){
    Future future = asynchronousService.springAsynchronousMethod();
    future.get(1000, TimeUnit.MILLISECONDS);
}
```

其实 Spring 只不过在原生的 Future 中进行了一次封装，我们最终获得的还是 Future 实例。

### 4. Java 如何将异步调用转为同步

换句话说，就是需要在异步调用过程中，持续阻塞至获得调用结果。

- 使用 wait 和 notify 方法
- 使用条件锁
- Future
- 使用 CountDownLatch
- 使用 CyclicBarrier
  五种方法，具体举例说明戳[原文链接](https://www.jianshu.com/p/f00aa6f66281).

---

很多时候，我们需要调用一个耗时方法，但是我们并不需要等待它执行完，才继续后面的工作，阻塞在这里是一个非常浪费时间的事，那么我们有没有办法解决呢？有！让它异步执行！

**首先我们先来看看不异步执行的方案，下面是伪代码**

```JAVA
//我们需要执行的代码1
longTimeMethod();
//我们需要执行的代码2
```

如上，如果我们执行到 `longTimeMethod` 的时候，必须等待这个方法彻底执行完才能执行 `我们需要执行的代码 2`，但是如果二者的关联性不是那么强，其实是没有必要去等待 `longTimeMethod` 执行完的。

**那么异步执行如何解决以上问题呢?**

- 采用多线程把 longTimeMethod 封装到一个多线程中，让它去执行

```java
Thread t = new Thread(){
  @Override
  public void run() {
    longTimeMethod();
  }
};
```

- 采用 Spring 的异步方法去执行

1. 先把 longTimeMethod 封装到 Spring 的异步方法中，这个方法一定要写在 Spring 管理的类中，注意注解@Async

```java
@Service
public class AsynchronousService{
  @Async
  public void springAsynchronousMethod(){
    longTimeMethod();
  }
}
```

2. 其他类调用这个方法。这里注意，一定要其他的类，如果在同类中调用，是不生效的。具体原因，可以去学习一下 Spring AOP 的原理

```java
@Autowired
private AsynchronousService asynchronousService;

public void useAsynchronousMethod(){
  //我们需要执行的代码1
  asynchronousService.springAsynchronousMethod();
 //我们需要执行的代码2
}
```

**那么问题来了，以上异步调用的方法都是没有返回值的，如果有返回值的方法该怎么获取到返回值呢？**

- 非异步的写法

```java
//我们需要执行的代码1
Integer result = longTimeMethod();
//我们需要执行的代码2
```

- 采用 JDK 原生的 Future 类

```java
//我们需要执行的代码1
Future future = longTimeMethod2();
//我们需要执行的代码2
Integer result = future.get();
```

可以看到，我们调用 longTimeMethod2 返回一个 Future 对象（注意了，这里的 longTimeMethod2 当然不是上面的 longTimeMethod），然后处理“我们需要执行的代码 2”，到了需要返回结果的时候直接调用 future.get()便能获取到返回值。下面我们来看看 longTimeMethod2 如何实现。

```cpp
private Future longTimeMethod2() {
  //创建线程池
  ExecutorService threadPool = Executors.newCachedThreadPool();
  //获取异步Future对象
  Future future = threadPool.submit(new Callable() {
    @Override
    public Integer call() throwsException {
        return longTimeMethod();
    }
  });
  return future;
}
```

可以看到我们用到了线程池，把任务加入线程池中，返回 Future 对象。其实我们调用 longTimeMethod2 方法是开启了其他的线程，其他的线程在调用工作。

对于 Future 来说，除了无参的 get()方法之外，还有一个有参的 get()方法。有参的 get()方法中传入的参数是需要等待的时间，也就是超时设置，不需要一直等待下去。而我们返回的 Future 对象是 FutureTask 的实例。

- 采用 Spring 的异步方法执行

1. 先把 longTimeMethod 封装到 Spring 的异步方法中，这个异步方法的返回值是 Future 的实例。这个方法一定要写在 Spring 管理的类中，注意注解@Async。

```java
@Service
public class AsynchronousService{
  @Async
  public Future springAsynchronousMethod(){
    Integer result = longTimeMethod();
    return new AsyncResult(result);
  }
}
```

1. 其他类调用这个方法。这里注意，一定要其他的类，如果在同类中调用，是不生效的。

```cpp
@Autowired
private AsynchronousService asynchronousService;

public void useAsynchronousMethod(){
    Future future = asynchronousService.springAsynchronousMethod();
    future.get(1000, TimeUnit.MILLISECONDS);
}
```

其实 Spring 只不过在原生的 Future 中进行了一次封装，我们最终获得的还是 Future 实例。

---

##### 源码地址：https://gitee.com/sunnymore/asyncToSync

---

Sunny 先来说一下对异步和同步的理解：

> 同步调用：调用方在调用过程中，持续等待返回结果。
> 异步调用：调用方在调用过程中，不直接等待返回结果，而是执行其他任务，结果返回形式通常为回调函数。

其实，两者的区别还是很明显的，这里也不再细说，我们主要来说一下 Java 如何将异步调用转为同步。换句话说，就是需要在异步调用过程中，持续阻塞至获得调用结果。
不卖关子，先列出五种方法，然后一一举例说明：

> 1. 使用 wait 和 notify 方法
> 2. 使用条件锁
> 3. Future
> 4. 使用 CountDownLatch
> 5. 使用 CyclicBarrier

### 0.构造一个异步调用

首先，写 demo 需要先写基础设施，这里的话主要是需要构造一个异步调用模型。异步调用类:

```csharp
public class AsyncCall {

    private Random random = new Random(System.currentTimeMillis());
    private ExecutorService tp = Executors.newSingleThreadExecutor();

    //demo1,2,4,5调用方法
    public void call(BaseDemo demo){

        new Thread(()->{
            long res = random.nextInt(10);
            try {
                Thread.sleep(res*1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            demo.callback(res);
        }).start();


    }

    //demo3调用方法
    public Future<Long> futureCall(){

        return tp.submit(()-> {
            long res = random.nextInt(10);
            try {
                Thread.sleep(res*1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return res;
        });
    }

    public void shutdown(){
        tp.shutdown();
    }

}
```

我们主要关心 call 方法，这个方法接收了一个 demo 参数，并且开启了一个线程，在线程中执行具体的任务，并利用 demo 的 callback 方法进行回调函数的调用。大家注意到了这里的返回结果就是一个[0,10)的长整型，并且结果是几，就让线程 sleep 多久——这主要是为了更好地观察实验结果，模拟异步调用过程中的处理时间。
至于 futureCall 和 shutdown 方法，以及线程池 tp 都是为了 demo3 利用 Future 来实现做准备的。
demo 的基类:

```csharp
public abstract class BaseDemo {

    protected AsyncCall asyncCall = new AsyncCall();
    public abstract void callback(long response);

    public void call(){
        System.out.println("发起调用");
        asyncCall.call(this);
        System.out.println("调用返回");
    }

}
```

BaseDemo 非常简单，里面包含一个异步调用类的实例，另外有一个 call 方法用于发起异步调用，当然还有一个抽象方法 callback 需要每个 demo 去实现的——主要在回调中进行相应的处理来达到异步调用转同步的目的。

### 1. 使用 wait 和 notify 方法

这个方法其实是利用了锁机制，直接贴代码：

```csharp
public class Demo1 extends BaseDemo{

    private final Object lock = new Object();

    @Override
    public void callback(long response) {
        System.out.println("得到结果");
        System.out.println(response);
        System.out.println("调用结束");

        synchronized (lock) {
            lock.notifyAll();
        }

    }

    public static void main(String[] args) {

        Demo1 demo1 = new Demo1();

        demo1.call();

        synchronized (demo1.lock){
            try {
                demo1.lock.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        System.out.println("主线程内容");

    }
}
```

可以看到在发起调用后，主线程利用 wait 进行阻塞，等待回调中调用 notify 或者 notifyAll 方法来进行唤醒。注意，和大家认知的一样，这里 wait 和 notify 都是需要先获得对象的锁的。在主线程中最后我们打印了一个内容，这也是用来验证实验结果的，如果没有 wait 和 notify，主线程内容会紧随调用内容立刻打印；而像我们上面的代码，主线程内容会一直等待回调函数调用结束才会进行打印。
没有使用同步操作的情况下，打印结果：

```undefined
发起调用
调用返回
主线程内容
得到结果
1
调用结束
```

而使用了同步操作后：

```undefined
发起调用
调用返回
得到结果
9
调用结束
主线程内容
```

### 2. 使用条件锁

和方法一的原理类似：

```csharp
public class Demo2 extends BaseDemo {

    private final Lock lock = new ReentrantLock();
    private final Condition con = lock.newCondition();

    @Override
    public void callback(long response) {

        System.out.println("得到结果");
        System.out.println(response);
        System.out.println("调用结束");
        lock.lock();
        try {
            con.signal();
        }finally {
            lock.unlock();
        }

    }

    public static void main(String[] args) {

        Demo2 demo2 = new Demo2();

        demo2.call();

        demo2.lock.lock();

        try {
            demo2.con.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }finally {
            demo2.lock.unlock();
        }
        System.out.println("主线程内容");
    }
}
```

基本上和方法一没什么区别，只是这里使用了条件锁，两者的锁机制有所不同。

### 3. Future

使用 Future 的方法和之前不太一样，我们调用的异步方法也不一样。

```cpp
public class Demo3{

    private AsyncCall asyncCall = new AsyncCall();

    public Future<Long> call(){

        Future<Long> future = asyncCall.futureCall();

        asyncCall.shutdown();

        return future;

    }

    public static void main(String[] args) {

        Demo3 demo3 = new Demo3();

        System.out.println("发起调用");
        Future<Long> future = demo3.call();
        System.out.println("返回结果");

        while (!future.isDone() && !future.isCancelled());

        try {
            System.out.println(future.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }

        System.out.println("主线程内容");

    }
}
```

我们调用 futureCall 方法，方法中会想线程池 tp 提交一个 Callable，然后返回一个 Future，这个 Future 就是我们 demo3 中 call 中得到的，得到 future 对象之后就可以关闭线程池啦，调用 asyncCall 的 shutdown 方法。关于关闭线程池这里有一点需要注意，我们回过头来看看 asyncCall 的 shutdown 方法：

```cpp
public void shutdown(){
		tp.shutdown();
}
```

发现只是简单调用了线程池的 shutdown 方法，然后我们说注意的点，这里最好不要用 tp 的 shutdownNow 方法，该方法会试图去中断线程中中正在执行的任务；也就是说，如果使用该方法，有可能我们的 future 所对应的任务将被中断，无法得到执行结果。
然后我们关注主线程中的内容，主线程的阻塞由我们自己来实现，通过 future 的 isDone 和 isCancelled 来判断执行状态，一直到执行完成或被取消。随后，我们打印 get 到的结果。

### 4. 使用 CountDownLatch

使用 CountDownLatch 或许是日常编程中最常见的一种了，也感觉是相对优雅的一种：

```java
public class Demo4 extends BaseDemo{

    private final CountDownLatch countDownLatch = new CountDownLatch(1);

    @Override
    public void callback(long response) {
        System.out.println("得到结果");
        System.out.println(response);
        System.out.println("调用结束");

        countDownLatch.countDown();
    }

    public static void main(String[] args) {

        Demo4 demo4 = new Demo4();
        demo4.call()
        try {
            demo4.countDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("主线程内容");

    }
}
```

正如大家平时使用的那样，此处在主线程中利用 CountDownLatch 的 await 方法进行阻塞，在回调中利用 countDown 方法来使得其他线程 await 的部分得以继续运行。
当然，这里和 demo1 和 demo2 中都一样，主线程中阻塞的部分，都可以设置一个超时时间，超时后可以不再阻塞。

### 5. 使用 CyclicBarrier

CyclicBarrier 的情况和 CountDownLatch 有些类似：

```java
public class Demo5 extends BaseDemo{

    private CyclicBarrier cyclicBarrier = new CyclicBarrier(2);


    @Override
    public void callback(long response) {

        System.out.println("得到结果");
        System.out.println(response);
        System.out.println("调用结束");

        try {
            cyclicBarrier.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (BrokenBarrierException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {

        Demo5 demo5 = new Demo5();

        demo5.call();

        try {
            demo5.cyclicBarrier.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (BrokenBarrierException e) {
            e.printStackTrace();
        }

        System.out.println("主线程内容");

    }
}
```

大家注意一下，CyclicBarrier 和 CountDownLatch 仅仅只是类似，两者还是有一定区别的。比如，一个可以理解为做加法，等到加到这个数字后一起运行；一个则是减法，减到 0 继续运行。一个是可以重复计数的；另一个不可以等等等等。
另外，使用 CyclicBarrier 的时候要注意两点。第一点，初始化的时候，参数数字要设为 2，因为异步调用这里是一个线程，而主线程是一个线程，两个线程都 await 的时候才能继续执行，这也是和 CountDownLatch 区别的部分。第二点，也是关于初始化参数的数值的，和这里的 demo 无关，在平时编程的时候，需要比较小心，如果这个数值设置得很大，比线程池中的线程数都大，那么就很容易引起死锁了。

### 总结

综上，就是本次需要说的几种方法了。事实上，所有的方法都是同一个原理，也就是在调用的线程中进行阻塞等待结果，而在回调中函数中进行阻塞状态的解除。
如果你还有其他方法，欢迎与我讨论哦～

