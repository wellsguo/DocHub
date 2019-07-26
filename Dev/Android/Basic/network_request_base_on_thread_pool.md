## [Android下基于线程池的网络访问基础框架](https://www.cnblogs.com/dreamGong/p/6404587.html)


### 引言

现在的Android开发很多都使用Volley、OkHttp、Retrofit等框架，这些框架固然有优秀的地方(以后会写代码学习分享)，但是我们今天介绍一种基于Java线程池的网络访问框架。

### 实现思路及实现

APP界面上面的数据都是通过网络请求获取的，我们能不能将网络请求依次入队，然后配合着Java线程池，让线程依次处理我们的请求，最后返回结果给我们。下面我们先来看一下线程池工具类的实现：

```java
 1 public class ThreadPoolUtils {
 2 
 3     private ThreadPoolUtils() {}
 4     //核心线程数
 5     private static int CORE_POOL_SIZE = 8;
 6     //最大线程数
 7     private static int MAX_POOL_SIZE = 64;
 8     //线程池中超过corePoolSize数目的空闲线程最大存活时间；可以allowCoreThreadTimeOut(true)使得核心线程有效时间
 9     private static int KEEP_ALIVE_TIME = 5;
10     //任务队列
11     private static BlockingQueue<Runnable> workQueue = new ArrayBlockingQueue<>(64);
12 
13     private static ThreadPoolExecutor threadpool;
14 
15     static {
16         threadpool = new ThreadPoolExecutor(CORE_POOL_SIZE, MAX_POOL_SIZE, KEEP_ALIVE_TIME, TimeUnit.SECONDS, workQueue);
17     }
18 
19     public static void execute(Runnable runnable) {
20         threadpool.execute(runnable);
21     }
22 }
```
我们来看一下ThreadPoolExecutor的构造函数及相关参数：

参数名	| 作用
-- | --
corePoolSize	|核心线程池大小
maximumPoolSize	|最大线程池大小
keepAliveTime	|线程池中超过corePoolSize数目的空闲线程最大存活时间；可以allowCoreThreadTimeOut(true)使得核心线程有效时间
TimeUnit	|keepAliveTime时间单位
workQueue	|阻塞任务队列
threadFactory	|新建线程工厂
RejectedExecutionHandler	|当提交任务数超过maxmumPoolSize+workQueue之和时，任务会交给RejectedExecutionHandler来处理

##### 重点讲解

其中比较容易让人误解的是：`corePoolSize`，`maximumPoolSize`，`workQueue`之间关系。 

1. 当线程池小于corePoolSize时，新提交任务将创建一个新线程执行任务，即使此时线程池中存在空闲线程。 
2. 当线程池达到corePoolSize时，新提交任务将被放入workQueue中，等待线程池中任务调度执行 
3. 当workQueue已满，且maximumPoolSize>corePoolSize时，新提交任务会创建新线程执行任务 
4. 当提交任务数超过maximumPoolSize时，新提交任务由RejectedExecutionHandler处理 
5. 当线程池中超过corePoolSize线程，空闲时间达到keepAliveTime时，关闭空闲线程 
6. 当设置allowCoreThreadTimeOut(true)时，线程池中corePoolSize线程空闲时间达到keepAliveTime也将关闭

### 网络访问的封装

通过上面的分析，我们知道 `ThreadPoolExecutor` 里面可以执行 `Runable` 对象，那么我们将网络访问逻辑封装成 `Runable` 对象，然后扔进线程池进行执行。我们来看一下封装的逻辑：

```java
 1 /**
 2  * post线程
 3  */
 4 public class HttpPostThread implements Runnable {
 5 
 6     private Handler hand;
 7     private String strURL;
 8     private String method;
 9     private List<String> params;
10     private Handler netHand;
11 
12     public HttpPostThread(Handler hand, String strURL, String method, List<String> params) {
13         this.hand = hand;
14         //实际的传值
15         this.strURL = strURL;
16         this.method = method;
17         this.params = params;
18     }
19 
20     public HttpPostThread(Handler hand, Handler netHand, String strURL, String method, List<String> params) {
21         this.hand = hand;
22         //实际的传值
23         this.strURL = strURL;
24         this.method = method;
25         this.params = params;
26         this.netHand = netHand;
27     }
28 
29     @Override
30     public void run() {
31         Message msg = hand.obtainMessage();
32         try {
33             String result;
34             if(!strURL.startsWith("https")) {
35                 RpcHttp rpcHttp = new RpcHttp();
36                 result = rpcHttp.post(strURL, method, params);
37             }
38             else {
39                 RpcHttps rpcHttps = new RpcHttps();
40                 result = rpcHttps.post(strURL, method, params);
41             }
42             /**
43              * 根据访问http来设置标识位
44              * 然后发送msg到handlerMessage进行处理(此处配合Handler进行使用)
45              */
46             if (result.equals("noNet")) {
47                 if (netHand != null) {
48                     netHand.sendEmptyMessage(600);
49                 }
50             } else {
51                 msg.what = 200;
52                 msg.obj = result;
53             }
54         } catch(Exception e){
55             e.printStackTrace();
56         }
57         finally {
58             hand.sendMessage(msg);
59         }
60     }
61 }

```

我们看到，我们封装的这个类的构造函数只需要使用者提供回调的Handler、Http访问的Url、访问的方法及参数。这样就可以将其放入线程中进行处理，然后我们只需要在客户端使用写好回调的Handler即可。我们看34-40行，这时候我们看到会使用封装的Http类去进行网络访问，我们来看一下：

```java
 1  /**
 2      * post请求
 3      *
 4      * @param strURL 请求的地址
 5      * @param method 请求方法
 6      * @param params 请求元素
 7      * @return
 8      */
 9     public String post(String strURL, String method, List<String> params) {
10         Log.e("开始请求","获取请求");
11         String RequestParams = "";
12         long timestamp = System.currentTimeMillis();
13         RequestParams += "{\"method\":\"" + method + "\"";
14         if (params != null && params.size() > 0) {
15             RequestParams += ",\"params\":{";
16             for (String item : params) {
17                 String first = item.substring(0, item.indexOf(":"));
18                 String second = item.substring(item.indexOf(":") + 1);
19                 RequestParams += "\"" + first + "\":\"" + second + "\",";
20             }
21 
22             RequestParams = RequestParams.substring(0, (RequestParams.length() - 1));
23             RequestParams += "}";
24         } else {
25             RequestParams += ",\"params\":{}";
26         }
27         RequestParams += ",\"id\":\"" + timestamp + "\"";
28         RequestParams += "}";
29         return this.post(strURL, RequestParams);
30     }
31 
32     private String post(String strURL, String params) {
33         try {
34             URL url = new URL(strURL);// 创建连接
35             HttpURLConnection connection = (HttpURLConnection) url.openConnection();
36 
37             connection.setDoOutput(true);
38             connection.setDoInput(true);
39             connection.setUseCaches(false);
40             connection.setInstanceFollowRedirects(true);
41             connection.setRequestMethod("POST"); // 设置请求方式
42             connection.setRequestProperty("Accept", "application/json"); // 设置接收数据的格式
43             connection.setRequestProperty("Content-Type", "application/json"); // 设置发送数据的格式
44             connection.setConnectTimeout(10000);//设置超时
45             connection.setReadTimeout(10000);//设置超时
46             Log.e("开始连接","开始连接");
47             connection.connect();
48 
49             OutputStreamWriter out = new OutputStreamWriter(connection.getOutputStream(), "UTF-8"); // utf-8编码
50             out.append(params);
51             out.flush();
52             out.close();
53 
54             String result = convertStreamToString(connection.getInputStream());
55             Log.e("responseContent",result);
56             return result;
57         } catch (Exception e) {
58             Log.e("responseException",String.valueOf(e.getStackTrace()));
59             Log.e("responseException",String.valueOf(e.getLocalizedMessage()));
60             Log.e("responseException",String.valueOf(e.getMessage()));
61             e.printStackTrace();
62         }
63         return "noNet"; // 自定义错误信息
64     }
```

我们看到，我们将Http访问进行了简单的封装。在客户端使用的时候我们就只需要简单的几行代码即可：

```java
1 List<String> params = new ArrayList<>();
2 params.add("access_token:" + getAccessToken());
3 //开始用户更新信息
4 ThreadPoolUtils.execute(new HttpPostThread(userhand, APIAdress.UserClass, APIAdress.GetUserInfoMethod, params));
```

我们看到，我们创建了一个Runable实例，然后传递了回调的Handler、Url、Method及参数。