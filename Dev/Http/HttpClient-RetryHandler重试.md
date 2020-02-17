# HttpClient RetryHandler 重试

> 目前的项目接口都是 http，因此在 java 项目中使用 Apache HttpClient 进行数据传输、访问。

目前程序中涉及到需要 callback 操作，product 需要被动的接收 consume 的处理状态，为了最大程度的能够 callback 成功。因此 consume 在 HTTP 调用出现问题（如：服务不可用、异常、超时）情况下需要进行重试（retry request），在这里我列举出我找到的 `retry` 方案，有些成功有些不成功。

我是用的 `httpclient` 版本是 `4.5.2`。关于 retry 功能我在网上也找了不少的资料，但是都不是我对应的 `httpclient` 版本，大多是过时的。

在 `httpclient` 版本 `4.5.2` 提供了以下几种 `retry` 方案：

## (1) StandardHttpRequestRetryHandler

==这种方案没有测试通过==  

`StandardHttpRequestRetryHandler` 实际上是 `DefaultHttpRequestRetryHandler` 的子类，这是官方提供的一个标准的 `retry` 方案，为了保证幂等性约定 `RESTful` 接口必须是 `GET, HEAD, PUT, DELETE, OPTIONS, and TRACE` 中的一种。

### 定义 HttpClient Pool

```java
public static CloseableHttpClient getHttpClient() {
    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
    cm.setMaxTotal(MAX_TOTAL);
    cm.setDefaultMaxPerRoute(MAX_PERROUTE);

    CloseableHttpClient httpClient = HttpClients
        .custom()
        .setRetryHandler(new StandardHttpRequestRetryHandler())
        .setConnectionManager(cm)
        .build();

    return httpClient;
}
```

### 测试

```java
@Test
public void test6(){
    HttpPost httpPost = new HttpPost("http://127.0.0.1:8080/testjobs1");
    try {
        rsp = httpClient.execute(httpPost);
        log.info(">> {}",rsp.getStatusLine().getStatusCode());
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }finally{
        HttpUtil.close(rsp);
    }
}
```

> 运行测试，当 url 错误、后台报错、后台超时等情况的时候不能进行 retry，因此放弃了此方案。

## (2) DefaultHttpRequestRetryHandler

==这种方案没有测试通过==

和上面的 `StandardHttpRequestRetryHandler` 类似，它提供了一种默认的 `retry` 方案，并没有像 `StandardHttpRequestRetryHandler` 一样约定接口必须是冥等的。



### 定义 HttpClient Pool



```java
public static CloseableHttpClient getHttpClient() {
    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
    cm.setMaxTotal(MAX_TOTAL);
    cm.setDefaultMaxPerRoute(MAX_PERROUTE);
    CloseableHttpClient httpClient = HttpClients
            .custom()
            .setRetryHandler(new DefaultHttpRequestRetryHandler())
            .setConnectionManager(cm)
            .build();

    return httpClient;
}
```

### 测试

```JAVA
@Test
public void test6(){

    HttpPost httpPost=new HttpPost("http://127.0.0.1:8080/testjobs1");

    try {
        rsp=httpClient.execute(httpPost);
        log.info(">> {}",rsp.getStatusLine().getStatusCode());
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }finally{
        HttpUtil.close(rsp);
    }
}
```

依然没有达到希望的效果。

## (3) HttpRequestRetryHandler

==可以实现，但是不够完美==

在[官方文档](http://hc.apache.org/httpcomponents-client-ga/tutorial/html/fundamentals.html#d5e316)有这么一段

```java
HttpRequestRetryHandler myRetryHandler = new HttpRequestRetryHandler() {

    public boolean retryRequest(
            IOException exception,
            int executionCount,
            HttpContext context) {
        if (executionCount >= 5) {
            // Do not retry if over max retry count
            return false;
        }

        if (exception instanceof InterruptedIOException) {
            // Timeout
            return false;
        }

        if (exception instanceof UnknownHostException) {
            // Unknown host
            return false;
        }

        if (exception instanceof ConnectTimeoutException) {
            // Connection refused
            return false;
        }

        if (exception instanceof SSLException) {
            // SSL handshake exception
            return false;
        }

        HttpClientContext clientContext = HttpClientContext.adapt(context);
        HttpRequest request = clientContext.getRequest();
        boolean idempotent = !(request instanceof HttpEntityEnclosingRequest);

        if (idempotent) {
            // Retry if the request is considered idempotent
            return true;

        }
        return false;
    }
};



CloseableHttpClient httpclient = HttpClients.custom()
        .setRetryHandler(myRetryHandler)
        .build();
```

自定义 retry 实现，这比较灵活，可以根据异常自定义 retry 机制以及重试次数，并且可以拿到返回信息

###  定义 HttpClient Pool

```java
public static CloseableHttpClient getHttpClient() {

    HttpRequestRetryHandler retryHandler = new HttpRequestRetryHandler() {

        public boolean retryRequest(
                IOException exception,
                int executionCount,
                HttpContext context) {

            if (executionCount >= 5) {
                // Do not retry if over max retry count
                return false;
            }

            if (exception instanceof InterruptedIOException)
                // Timeout
                return false;
            }

            if (exception instanceof UnknownHostException) {
                // Unknown host
                return false;
            }

            if (exception instanceof ConnectTimeoutException) {
                // Connection refused
                return false;
            }

            if (exception instanceof SSLException) {
                // SSL handshake exception
                return false;
            }

            HttpClientContext clientContext = HttpClientContext.adapt(context);
            HttpRequest request = clientContext.getRequest();
            boolean idempotent = !(request instanceof HttpEntityEnclosingRequest);

            if (idempotent) {
                // Retry if the request is considered idempotent
                return true;
            }
            return false;
        }
    };

    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();

    cm.setMaxTotal(MAX_TOTAL);
    cm.setDefaultMaxPerRoute(MAX_PERROUTE);

    CloseableHttpClient httpClient = HttpClients
            .custom()
            .setRetryHandler(retryHandler)
            .setConnectionManager(cm)
            .build();

    return httpClient;
}
```
### 测试

```java
@Test
public void test6(){

    HttpPost httpPost=new HttpPost("http://127.0.0.1:8080/testjobs1");
    try {
        rsp=httpClient.execute(httpPost);
        log.info(">> {}",rsp.getStatusLine().getStatusCode());
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }finally{
        HttpUtil.close(rsp);
    }
}
```

这种方案，可以实现 retry，并且可以根据我的需求进行 retry，如：retry count，**但是就不能控制 retry 时间的间隔**，也只好放弃了，继续寻找找到了下面这个`ServiceUnavailableRetryStrategy`。

## (4) ServiceUnavailableRetryStrategy

==可以实现，满足需求==



具有`HttpRequestRetryHandler`的所有优点，并且可以`自定义 retry 时间的间隔`，



### 定义 HttpClient Pool



```java
public static CloseableHttpClient getHttpClient() {

    ServiceUnavailableRetryStrategy serviceUnavailableRetryStrategy = 
      new ServiceUnavailableRetryStrategy() {

        /**
         * retry逻辑
         */
        @Override
        public boolean retryRequest(HttpResponse response, int executionCount, 
                                    HttpContext context) {
            if (executionCount <= 3)
                return true;
            else
                return false;
        }

        /**
         * retry间隔时间
         */
        @Override
        public long getRetryInterval() {
            return 2000;
        }
    };



    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
    cm.setMaxTotal(MAX_TOTAL);
    cm.setDefaultMaxPerRoute(MAX_PERROUTE);
    CloseableHttpClient httpClient = HttpClients.custom().setRetryHandler(
      new DefaultHttpRequestRetryHandler())
            .setConnectionManager(cm).build();

    return httpClient;
}
```



### 测试

```java
@Test
public void test6(){
    HttpPost httpPost=new HttpPost("http://127.0.0.1:8080/testjobs1");

    try {
        rsp=httpClient.execute(httpPost);
        log.info(">> {}",rsp.getStatusLine().getStatusCode());
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }finally{
        HttpUtil.close(rsp);
    }
}
```
