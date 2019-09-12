[原文链接](https://blog.csdn.net/ldhj1993/article/details/72666867)

之前又一次面试，面试官问我线程池的大小，定义里面的线程数量多少最合适。我当时的回答是和CPU 核数有关，大概是 n+1 的关系。当时看面试官反应，可能没答对。回来后，立即查询线程池的相关资料。

一般说来，大家认为线程池的大小经验值应该这样设置：（其中 $N$ 为CPU的核数） 

- 如果是 `CPU密集型` 应用，则线程池大小设置为 $N+1$ 

- 如果是 `IO密集型` 应用，则线程池大小设置为 $2N+1$

那么我们的 Android 应用是属于哪一种应用呢？看下他们的定义。

### I/O 密集型 

I/O bound 指的是系统的 `CPU效能` 相对 `硬盘/内存效能` 要好很多，此时，系统运作，大部分的状况是 CPU 在等 I/O (硬盘/内存) 的读/写，此时 CPU Loading 不高。 

### CPU-bound 

CPU bound 指的是系统的 `硬盘/内存效能`  相对 `CPU效能` 要好很多，此时，系统运作，大部分的状况是 CPU Loading 100%，CPU 要读/写 I/O (硬盘/内存)，I/O在很短的时间就可以完成，而 CPU 还有许多运算要处理，CPU Loading 很高。

我们的 Android 应用的话应该是属于IO密集型应用，所以数量一般设置为 $2N+1$。下面的例子是我截取的一段线程池创建的代码：

```java
//参数初始化
private static final int CPU_COUNT = Runtime.getRuntime().availableProcessors();
//核心线程数量大小
private static final int corePoolSize = Math.max(2, Math.min(CPU_COUNT - 1, 4));
//线程池最大容纳线程数
private static final int maximumPoolSize = CPU_COUNT * 2 + 1;
//线程空闲后的存活时长
private static final int keepAliveTime = 30;

//任务过多后，存储任务的一个阻塞队列
BlockingQueue<Runnable>  workQueue = new SynchronousQueue<>();

//线程的创建工厂
ThreadFactory threadFactory = new ThreadFactory() {
    private final AtomicInteger mCount = new AtomicInteger(1);

    public Thread newThread(Runnable r) {
        return new Thread(r, "AdvacnedAsyncTask #" + mCount.getAndIncrement());
    }
};

//线程池任务满载后采取的任务拒绝策略
RejectedExecutionHandler rejectHandler = new ThreadPoolExecutor.DiscardOldestPolicy();

//线程池对象，创建线程
ThreadPoolExecutor mExecute = new ThreadPoolExecutor(
        corePoolSize,
        maximumPoolSize,
        keepAliveTime,
        TimeUnit.SECONDS,
        workQueue,
        threadFactory,
        rejectHandler
);
```
