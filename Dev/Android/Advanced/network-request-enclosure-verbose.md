# Android 网络层封装





作者：一直奔跑的熊猫  
来源：CSDN   
原文：https://blog.csdn.net/zhongwei123/article/details/80624364   
版权声明：本文为博主原创文章，转载请附上博文链接！  
  
## Android网络层重构设计 Rx+Retrofit+okhttp

公司app应用一直使用okhttp，虽然它确实好用，但是经年日久，使用时的不方便越来越多，比如重复代码过多，内存泄露不好控制，调用时参数过多等等。

还是决定痛下杀手，早点除掉这个顽疾。

So，有了这次网络层重新架构，感觉还算满意，现在列出一下过程：

### 1、接口封装
```java
/** 网络层工具类 */
public class AppConnecter {
    public static int CONNNET_TIMEOUT = 30; // 超时设置
    private static AppConnecter appConnecter; // 单例对象
    private RequestInterface mServer; // Retrofit2网络接口
    private String mInitServerUrl; // 请求域名中的主机名 如https://m.test.com
    private final OkHttpClient client; // 实际的请求主体 OkHttpClient

    // 初始化httpserver
    private AppConnecter() {
        OkHttpClient.Builder builder = new OkHttpClient().newBuilder(); // 创建OkHttpClient
        try {
            builder.sslSocketFactory(createSSLSocketFactory()); // 创建httpsClient
            builder.hostnameVerifier(new TrustAllHostnameVerifier());
        } catch (Exception e) {
        }
        builder.connectTimeout(CONNNET_TIMEOUT, TimeUnit.SECONDS); // 设置网络超时
        builder.readTimeout(CONNNET_TIMEOUT, TimeUnit.SECONDS);
        builder.addInterceptor(new RequestInterceptor()); // OkHttp请求拦截器
        client = builder.build();
        mInitServerUrl = "https://m.test.com";
        mServer = getServer();
    }

    private RequestInterface getServer() {
        Retrofit retrofit = new Retrofit.Builder().baseUrl(mInitServerUrl).client(client)
                .addConverterFactory(ScalarsConverterFactory.create())
                .addCallAdapterFactory(RxJavaCallAdapterFactory.create()).build();
        return retrofit.create(RequestInterface.class); // 自定义的网络接口
    }

    public static AppConnecter getInsatnce() { // 单例 不用多说
        if (appConnecter == null) {
            synchronized (AppConnecter.class) {
                if (appConnecter == null) {
                    appConnecter = new AppConnecter();
                }
            }
        }
        return appConnecter;
    }

    // 用于切换网路请求的线程,observeOn是指定回调线程
    Observable.Transformer schedulersTransformer() {
        return new Observable.Transformer() {
            @Override
            public Observable call(Object observable) {
                return ((Observable) observable).subscribeOn(Schedulers.io()).unsubscribeOn(Schedulers.io())
                        .observeOn(Schedulers.immediate());
            }
        };
    }

    /**
     * 发送Post请求
     */
    public Observable reqPostWithRx(String postUrl, Map postparams, PublishSubject lifecycleSubject) {
        if (postparams == null) {
            postparams = new HashMap<String, String>();
        }
        // 防止内存创建的Observable,当call返回true的时候,终止rx的所有消息发送
        Observable<ActivityLifeCycleEvent> compareLifecycleObservable = lifecycleSubject
                .takeFirst(new Func1<Integer, Boolean>() {
                    @Override
                    public Boolean call(Integer integer) {
                        return integer.equals(ActivityLifeCycleEvent.STOP);
                    }
                });
        // 发送请求
        return mServer.queryRxPostUrl(postUrl, postparams).compose(schedulersTransformer())
                .takeUntil(compareLifecycleObservable);
    }

    /**
     *发送Get请求
     */
    public Observable reqGetWithRx(String url, Map<String, String> params, PublishSubject lifecycleSubject) {
        if (params == null) {
            params = new HashMap<String, String>();
        }
        //防止内存创建的Observable,当call返回true的时候,终止rx的所有消息发送
        Observable<ActivityLifeCycleEvent> compareLifecycleObservable =
                lifecycleSubject.takeFirst(new Func1<Integer, Boolean>() {
                    @Override
                    public Boolean call(Integer integer) {
                        boolean isStop = integer.equals(ActivityLifeCycleEvent.STOP);
                        return isStop;
                    }
                });
        //发送请求
        return mServer.queryRxGetUrl(url, params).compose(schedulersTransformer()).takeUntil(compareLifecycleObservable);
    }
}
```
这个类公布出来的就2个接口 ： 
  - reqGetWithRx  (用于get) 
  - reqPostWithRx   (用于post)

它们返回的对象都是 **Observable** (Rx的关键核心类)，用它可以做一系列的不同操作，什么排序，过滤等等，你想怎么弄它就怎么弄。它就是发送网络请求后，服务端返回的结果。

**compareLifecycleObservable** 这个对象，十分关键，它就是为了防止我们android中经常容易犯错的那个内存泄露而设置的。我们在activity基类中统一新建 **lifecycleSubject**。

> 它在哪使用呢？

就是在我们的本地界面activity finish的时候，
```java
    public void finish() {
        lifecycleSubject.onNext(ActivityLifeCycleEvent.STOP);
        super.finish();

    }
```
这样它就会帮我们把当前页面所有的请求finish掉，怎么样，省心吧！



### 2、RequestInterceptor 

这个 RequestInterceptor，其实是OkHttp自带的拦截器，我们只要继承okhttp3.Interceptor就可以了。
然后覆盖它的intercept方法，在这个方法里，做一些针对URL的操作，比如**编码，签名，加密**等。



### 3、RequestInterface (自定义的网络接口)
```
public interface RequestInterface {
 
    //结合RxJava的Post请求
    @FormUrlEncoded
    @POST("{url}")
    Observable<String> queryRxPostUrl(@Path("url") String url, @FieldMap Map<String, String> params);
 
    //结合RxJava的get请求
    @GET("{url}")
    Observable<String> queryRxGetUrl(@Path("url") String url, @QueryMap Map<String,String> params);
 
}
```
这样调用的时候，我们传的参数，只需要 与功能相关的接口名称与参数了。



### 4、Rx 网络回调订阅者 Subscriber

这个类主要是用于统一处理返回的字符串解析，我们给它加上泛型，就可以统一解析成需要的数据对象。
```java
public abstract class BaseSubscriber<T> extends Subscriber {
 
   public final void onNext(final Object o) {
        String result = (String) o;
	    //此处转换成我们需要的数据对象
        Type type = ((ParameterizedType) this.getClass().getGenericSuperclass()).getActualTypeArguments()[0];
        final T bean = JSON.parseObject(result, type);		//假定返回的数据是json格式
        // ...
        // onSuccess
        // onFailed
        // onError
   }
}       
```
### 5、在 Activity 基类中增加通用方法

```java
//BaseBean：自定义的数据对象基类
//ReqBean：自定义的网络请求参数对象
public <T extends BaseBean> void reqByGet(ReqBean reqBean, BaseSubscriber<T> reqCallBack) {
	AppConnecter.getInsatnce().queryGetWithRx(reqBean.url, reqBean.getLastParams(), lifecycleSubject)
		.subscribe(reqCallBack);
}
```

### 6、测试
做了这么多，终于到了享受的时候了，很简单，一句代码搞定：

```
String url = "/test/test.do";
reqByGet(new ReqBean(url, new String[][]{{"参数1", "参数值"}}), new BaseSubscriber<XxxBean>(){
            @Override
            public void onSuccess(XxxBean sKeyBean) {
                //此处处理相关业务
            }
 
            @Override
            public void onFailed(String code, String msg) {
		        //错误处理
            }
        });
```
大功告成了~~~~！

> 但其实它还是有明显的问题，大家有没有发现呢？

就是返回的 Observable，是依赖第三方框架的，这个东东要是以后替换或者升级时，Rx 改动了它，那就麻烦大了。

所以，最好的办法是自定义一个接口，来包装Observable。  

--------------------- 
作者：woshifano   
来源：CSDN   
原文：https://blog.csdn.net/woshifano/article/details/46984729   
版权声明：本文为博主原创文章，转载请附上博文链接！  
## Android 网络层的封装

因为项目需要封装了其网络层，主要对其原来的模式进行改进，使用的回调的方式来进行网络的访问和返回结果的处理，还有就是在 View 层和网络层之间加了一个中间层，用来分配各种网络请求，这样就可以方便的调度和管理。

我就不拿原项目的代码来演示，自己写了一个 demo，首先是最底层，处理最基本的 Http 协议，里面包含一个 execute 方法，用来 Post 或者 Get 获取数据，这里为了方便我只写了一个 Get，可以根据具体需要进行改成Post 或者其他方法：

### 1. Request 方法封装

```java
import java.util.Map;
 
import org.apache.http.HttpResponse;
import org.apache.http.HttpVersion;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.params.ConnManagerParams;
import org.apache.http.conn.scheme.PlainSocketFactory;
import org.apache.http.conn.scheme.Scheme;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.tsccm.ThreadSafeClientConnManager;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
 
public class RequestService {
 
	private static final String DEFAULT_CHARSET = HTTP.UTF_8;
	private static HttpClient simpleHttpClient = null;
 
	// 连接超时设定
	public final static int CONNECT_TIME_OUT = 10 * 1000;
	// 连接池取连接超时设定
	public final static int WAIT_TIME_OUT = 10 * 1000;
	// 读超时设定
	public final static int READ_TIME_OUT = 40 * 1000;
	// 连接池容量设定
	public final static int MAX_CONNECTION = 10;
 
	private static void init() {
		if (null == simpleHttpClient) {
			HttpParams params = new BasicHttpParams();
			HttpProtocolParams.setVersion(params, HttpVersion.HTTP_1_1);
			HttpProtocolParams.setContentCharset(params, DEFAULT_CHARSET);
			HttpProtocolParams.setUseExpectContinue(params, true);
			ConnManagerParams.setTimeout(params, WAIT_TIME_OUT);
			ConnManagerParams.setMaxTotalConnections(params, MAX_CONNECTION);
			// 通信读超时时间
			HttpConnectionParams.setSoTimeout(params, READ_TIME_OUT);
			// 通信连接超时时间
			HttpConnectionParams.setConnectionTimeout(params, CONNECT_TIME_OUT);
			SchemeRegistry schReg = new SchemeRegistry();
			schReg.register(new Scheme("http", PlainSocketFactory
					.getSocketFactory(), 80));
			// schReg.register(new Scheme("https",
			// SSLSocketFactory.getSocketFactory(), 443));
			ClientConnectionManager connectionManager = new ThreadSafeClientConnManager(params, schReg);
			simpleHttpClient = new DefaultHttpClient(connectionManager, params);
		}
	}
 
	protected static String get(String url, Map params) {
		String json = "";
		try {
			init();
			HttpGet httpGet = new HttpGet(url);
            // todo set params
			HttpResponse httpResponse;
			httpResponse = simpleHttpClient.execute(httpGet);
			if (httpResponse.getStatusLine().getStatusCode() == 200)
				json = EntityUtils.toString(httpResponse.getEntity());
		} catch (Exception e) {
			log.error(TAG, "request (get) error: "+e.getMessagem, e);
		}
		return json;
	}
 
}
```


### 2. 请求对象封装
可以看到这个 execute 方法的参数是 String url 和 Map<String,String> params，这样我们就需要一个POJO来构造这些参数。

```java
package com.example.callbacktest;
 
import java.util.HashMap;
import java.util.Map;
 
public class Request {
	private String url;
	private Map params;
 
	public String getUrl() {
		return url;
	}
 
	public void setUrl(String url) {
		this.url = url;
	}
 
	public Map getParams() {
		return params;
	}
 
	public void setParams(Map params) {
		this.params = params;
	}
 
}
```


### 3. 请求对象工厂类
接下来是一个工厂类，这里用到了简单工厂模式，可以根据不同的参数很方便的创造出POJO的实例。

```java
import java.util.HashMap;
import java.util.Map;
 
public class NetworkFactory {
 
	private static final String baseUrl = "http://contests.acmicpc.info/contests.json";
 
	private static final String login = "/user/login.php";
	private static final String reg = "/user/reg.php";
 
	private static Request createRequest(Map requestParams, String apiUrl) {
		String url = baseUrl + apiUrl;
		Request request = new Request();
		request.setUrl(url);
		request.setParams(requestParams);
		return request;
	}
 
	public static Request createLogin(String name, String pwd) {
		Map requestParams = new HashMap();
		requestParams.put("name", name);
		requestParams.put("pwd", pwd);
		return createRequest(requestParams, login);
	}
 
	public static Request createGo() {
		Map requestParams = new HashMap();
		return createRequest(requestParams, "");
	}
 
}
```
### 4. 中间层
接下来是中间层，所有的网络方法都需要经过这里才能调用底层协议，在这里进行各种网络方法的调度和管理.


```java
import android.os.AsyncTask;
 
public class Network {
	
	/**
	 *  这个方法运行在主线程中，在具体使用时需要自己将其运行在子线程中
	 * @param request
	 * @param callback
	 */
	public static void postOnUI(Request request, Callback callback) {
		String json = RequestService.get(request.getUrl(), request.getMap());
		if (json == "")
			callback.onSuccess(json);
		else
			callback.onError();
	}
	
	/**
	 * 这个方法运行在子线程中，构造好回调函数，使用时只需要简单调用就可以
	 * @param request
	 * @param callback
	 */
	public static void postOnThread(Request request, Callback callback) {
		new RequestAsyncTask(request, callback).get("");
	}
	
	/**
	 * 这个是不带回调的方法，使用时需要根据自己的需要进行判断返回值处理各种逻辑
	 * @param request
	 * @return
	 */
	public static String post(Request request) {
		String json = RequestService.get(request.getUrl(), request.getMap());
		return json;
	}
	
	/**
	 * AsyncTask
	 * @author ukfire
	 *
	 */
	static class RequestAsyncTask extends AsyncTask {
 
		private Request request;
		private Callback callback;
 
		public RequestAsyncTask(Request request, Callback callback) {
			this.request = request;
			this.callback = callback;
		}
 
		@Override
		protected String doInBackground(String... arg0) {
			String json = "";
			json = RequestService.get(request.getUrl(), request.getMap());
			return json;
		}
 
		@Override
		protected void onPostExecute(String result) {
			super.onPostExecute(result);
			if (result == "")
				callback.onError();
			else
				callback.onSuccess(result);
		}
	}
}
```

### 5. 回调接口
自己定义回调接口，一般来说就是进行Success处理和Error处理，还可以进一步抽象.


```java
public interface Callback {
	public void onError();
 
	public void onSuccess(String json);
}
```


### 6. 实现回调接口
最后就是在主函数中进行调用，这里调用的是运行在子线程中的方法，只需要构造好Callback回调函数，简单调用即可.
```java
final Request request = NetworkFactory.createGo();	//构造POJO

btn.setOnClickListener(new OnClickListener() {
    @Override
    public void onClick(View arg0) {
        Network.postOnThread(request, new Callback() {
            @Override
            public void onSuccess(String json) {
                text.setText(json);
            }
            @Override
            public void onError() {
                text.setText("Error");
            }
        });
    }
});
```
这样 View 层和底层中间就多了一个中间层，提供运行在不同线程的各种调用方法，使用时对其回调方法进行实现就可以了，最大的优点就是**方便调度和管理**。


## giffun 网络封装

### 1. Request 封装

```kotlin


/**
 * 网络请求模式的基类，所有的请求封装都应该要继承此类。这里会提供网络模块的配置，以及请求的具体逻辑处理等。
 *
 * @author guolin
 * @since 17/2/12
 */
abstract class Request {

    private lateinit var okHttpClient: OkHttpClient

    private val okHttpBuilder: OkHttpClient.Builder = OkHttpClient.Builder().addNetworkInterceptor(LoggingInterceptor())

    private var callback: Callback? = null

    private var params: Map<String, String>? = null

    var getParamsAlready = false

    var deviceName: String

    var deviceSerial: String

    init {
        connectTimeout(10)
        writeTimeout(10)
        readTimeout(10)
        deviceName = Utility.deviceName
        deviceSerial = Utility.getDeviceSerial()
    }

    private fun build() {
        okHttpClient = okHttpBuilder.build()
    }

    fun connectTimeout(seconds: Int) {
        okHttpBuilder.connectTimeout(seconds.toLong(), TimeUnit.SECONDS)
    }

    fun writeTimeout(seconds: Int) {
        okHttpBuilder.writeTimeout(seconds.toLong(), TimeUnit.SECONDS)
    }

    fun readTimeout(seconds: Int) {
        okHttpBuilder.readTimeout(seconds.toLong(), TimeUnit.SECONDS)
    }

    /**
     * 设置响应回调接口
     * @param callback
     * 回调的实例
     */
    fun setListener(callback: Callback?) {
        this.callback = callback
    }

    /**
     * 组装网络请求后添加到HTTP发送队列，并监听响应回调。
     * @param requestModel
     * 网络请求对应的实体类
     */
    fun <T : com.quxianggif.network.model.Response> inFlight(requestModel: Class<T>) {
        build()
        val requestBuilder = okhttp3.Request.Builder()
        if (method() == GET && getParams() != null) {
            requestBuilder.url(urlWithParam())
        } else {
            requestBuilder.url(url())
        }
        requestBuilder.headers(headers(Headers.Builder()).build())
        when {
            method() == POST -> requestBuilder.post(formBody())
            method() == PUT -> requestBuilder.put(formBody())
            method() == DELETE -> requestBuilder.delete(formBody())
        }
        okHttpClient.newCall(requestBuilder.build()).enqueue(object : okhttp3.Callback {

            @Throws(IOException::class)
            override fun onResponse(call: Call, response: Response) {
                try {
                    if (response.isSuccessful) {
                        val body = response.body()
                        val result = if (body != null) {
                            body.string()
                        } else {
                            ""
                        }
                        logVerbose(LoggingInterceptor.TAG, result)
                        val gson = GsonBuilder().disableHtmlEscaping().create()
                        val responseModel = gson.fromJson(result, requestModel)
                        response.close()
                        notifyResponse(responseModel)
                    } else {
                        notifyFailure(ResponseCodeException(response.code()))
                    }
                } catch (e: Exception) {
                    notifyFailure(e)
                }

            }

            override fun onFailure(call: Call, e: IOException) {
                notifyFailure(e)
            }

        })
    }

    abstract fun url(): String

    abstract fun method(): Int

    abstract fun listen(callback: Callback?)

    /**
     * 构建和服务器身份认证相关的请求参数。
     * @param params
     * 构建参数的param对象
     * @return 如果完成了身份认证参数构建返回true，否则返回false。
     */
    fun buildAuthParams(params: MutableMap<String, String>?): Boolean {
        if (params != null && AuthUtil.isLogin) {
            val userId = AuthUtil.userId.toString()
            val token = AuthUtil.token
            params[NetworkConst.UID] = userId
            params[NetworkConst.DEVICE_SERIAL] = deviceSerial
            params[NetworkConst.TOKEN] = token
            return true
        }
        return false
    }

    /**
     * 根据传入的keys构建用于进行服务器验证的参数，并添加到请求头当中。
     * @param builder
     * 请求头builder
     * @param keys
     * 用于进行服务器验证的键。
     */
    fun buildAuthHeaders(builder: Headers.Builder?, vararg keys: String) {
        if (builder != null && keys.isNotEmpty()) {
            val params = mutableListOf<String>()
            for (i in keys.indices) {
                val key = keys[i]
                getParams()?.let {
                    val p = it[key]
                    if (p != null) {
                        params.add(p)
                    }
                }
            }
            builder.add(NetworkConst.VERIFY, AuthUtil.getServerVerifyCode(*params.toTypedArray()))
        }
    }

    /**
     * Android客户端的所有请求都需要添加User-Agent: GifFun Android这样一个请求头。每个接口的封装子类可以添加自己的请求头。
     * @param builder
     * 请求头builder
     * @return 添加完请求头后的builder。
     */
    open fun headers(builder: Headers.Builder): Headers.Builder {
        builder.add(NetworkConst.HEADER_USER_AGENT, NetworkConst.HEADER_USER_AGENT_VALUE)
        builder.add(NetworkConst.HEADER_APP_VERSION, Utility.appVersion)
        builder.add(NetworkConst.HEADER_APP_SIGN, Utility.appSign)
        return builder
    }

    open fun params(): Map<String, String>? {
        return null
    }

    /**
     * 构建POST、PUT、DELETE请求的参数体。
     *
     * @return 组装参数后的FormBody。
     */
    private fun formBody(): FormBody {
        val builder = FormBody.Builder()
        val params = getParams()
        if (params != null) {
            val keys = params.keys
            if (!keys.isEmpty()) {
                for (key in keys) {
                    val value = params[key]
                    if (value != null) {
                        builder.add(key, value)
                    }
                }
            }
        }
        return builder.build()
    }

    /**
     * 当GET请求携带参数的时候，将参数以key=value的形式拼装到GET请求URL的后面，并且中间以?符号隔开。
     * @return 携带参数的URL请求地址。
     */
    private fun urlWithParam(): String {
        val params = getParams()
        if (params != null) {
            val keys = params.keys
            if (!keys.isEmpty()) {
                val paramsBuilder = StringBuilder()
                var needAnd = false
                for (key in keys) {
                    if (needAnd) {
                        paramsBuilder.append("&")
                    }
                    paramsBuilder.append(key).append("=").append(params[key])
                    needAnd = true
                }
                return url() + "?" + paramsBuilder.toString()
            }
        }
        return url()
    }

    /**
     * 获取本次请求所携带的所有参数。
     *
     * @return 本次请求所携带的所有参数，以Map形式返回。
     */
    private fun getParams(): Map<String, String>? {
        if (!getParamsAlready) {
            params = params()
            getParamsAlready = true
        }
        return params
    }

    /**
     * 当请求响应成功的时候，将服务器响应转换后的实体类进行回调。
     * @param response
     * 服务器响应转换后的实体类
     */
    private fun notifyResponse(response: com.quxianggif.network.model.Response) {
        callback?.let {
            if (it is OriginThreadCallback) {
                it.onResponse(response)
                callback = null
            } else {
                GifFun.getHandler().post {
                    it.onResponse(response)
                    callback = null
                }
            }
        }
    }

    /**
     * 当请求响应失败的时候，将具体的异常进行回调。
     * @param e
     * 请求响应的异常
     */
    private fun notifyFailure(e: Exception) {
        callback?.let {
            if (it is OriginThreadCallback) {
                it.onFailure(e)
                callback = null
            } else {
                GifFun.getHandler().post {
                    it.onFailure(e)
                    callback = null
                }
            }
        }
    }

    companion object {

        const val GET = 0

        const val POST = 1

        const val PUT = 2

        const val DELETE = 3
    }

}
```

#### 1.1 httpClient 初始化 


```kotlin 
    init { // 默认参数设置
        connectTimeout(10)
        writeTimeout(10)
        readTimeout(10)
        deviceName = Utility.deviceName
        deviceSerial = Utility.getDeviceSerial()
    }

    private fun build() { // 初始化
        okHttpClient = okHttpBuilder.build()
    }
```

#### 1.2 请求信息配置

- URL  
```kotlin
abstract fun url(): String
```
   

- mehtod
```kotlin
 abstract fun method(): Int
```
- header
```kotlin
    /**
     * 根据传入的keys构建用于进行服务器验证的参数，并添加到请求头当中。
     * @param builder
     * 请求头builder
     * @param keys
     * 用于进行服务器验证的键。
     */
    fun buildAuthHeaders(builder: Headers.Builder?, vararg keys: String) {
        if (builder != null && keys.isNotEmpty()) {
            val params = mutableListOf<String>()
            for (i in keys.indices) {
                val key = keys[i]
                getParams()?.let {
                    val p = it[key]
                    if (p != null) {
                        params.add(p)
                    }
                }
            }
            builder.add(NetworkConst.VERIFY, AuthUtil.getServerVerifyCode(*params.toTypedArray()))
        }
    }

    /**
     * Android客户端的所有请求都需要添加User-Agent: GifFun Android这样一个请求头。每个接口的封装子类可以添加自己的请求头。
     * @param builder
     * 请求头builder
     * @return 添加完请求头后的builder。
     */
    open fun headers(builder: Headers.Builder): Headers.Builder {
        builder.add(NetworkConst.HEADER_USER_AGENT, NetworkConst.HEADER_USER_AGENT_VALUE)
        builder.add(NetworkConst.HEADER_APP_VERSION, Utility.appVersion)
        builder.add(NetworkConst.HEADER_APP_SIGN, Utility.appSign)
        return builder
    }
```


- params

```kotlin  
    /**
     * 构建和服务器身份认证相关的请求参数。
     * @param params
     * 构建参数的param对象
     * @return 如果完成了身份认证参数构建返回true，否则返回false。
     */
    fun buildAuthParams(params: MutableMap<String, String>?): Boolean {
        if (params != null && AuthUtil.isLogin) {
            val userId = AuthUtil.userId.toString()
            val token = AuthUtil.token
            params[NetworkConst.UID] = userId
            params[NetworkConst.DEVICE_SERIAL] = deviceSerial
            params[NetworkConst.TOKEN] = token
            return true
        }
        return false
    }
    
   
    /**
     * 构建POST、PUT、DELETE请求的参数体。
     *
     * @return 组装参数后的FormBody。
     */
    private fun formBody(): FormBody {
        val builder = FormBody.Builder()
        val params = getParams()
        if (params != null) {
            val keys = params.keys
            if (!keys.isEmpty()) {
                for (key in keys) {
                    val value = params[key]
                    if (value != null) {
                        builder.add(key, value)
                    }
                }
            }
        }
        return builder.build()
    }

    /**
     * 当GET请求携带参数的时候，将参数以key=value的形式拼装到GET请求URL的后面，并且中间以?符号隔开。
     * @return 携带参数的URL请求地址。
     */
    private fun urlWithParam(): String {
        val params = getParams()
        if (params != null) {
            val keys = params.keys
            if (!keys.isEmpty()) {
                val paramsBuilder = StringBuilder()
                var needAnd = false
                for (key in keys) {
                    if (needAnd) {
                        paramsBuilder.append("&")
                    }
                    paramsBuilder.append(key).append("=").append(params[key])
                    needAnd = true
                }
                return url() + "?" + paramsBuilder.toString()
            }
        }
        return url()
    }

    /**
     * 获取本次请求所携带的所有参数。
     *
     * @return 本次请求所携带的所有参数，以Map形式返回。
     */
    private fun getParams(): Map<String, String>? {
        if (!getParamsAlready) {
            params = params()
            getParamsAlready = true
        }
        return params
    }
```    

#### 1.3 发起请求

```kotlin
    /**
     * 组装网络请求后添加到HTTP发送队列，并监听响应回调。
     * @param requestModel
     * 网络请求对应的实体类
     */
    fun <T : com.quxianggif.network.model.Response> inFlight(requestModel: Class<T>) {
        build()
        val requestBuilder = okhttp3.Request.Builder()
        if (method() == GET && getParams() != null) {
            requestBuilder.url(urlWithParam())
        } else {
            requestBuilder.url(url())
        }
        requestBuilder.headers(headers(Headers.Builder()).build())
        when {
            method() == POST -> requestBuilder.post(formBody())
            method() == PUT -> requestBuilder.put(formBody())
            method() == DELETE -> requestBuilder.delete(formBody())
        }
        okHttpClient.newCall(requestBuilder.build()).enqueue(object : okhttp3.Callback {

            @Throws(IOException::class)
            override fun onResponse(call: Call, response: Response) {
                try {
                    if (response.isSuccessful) {
                        val body = response.body()
                        val result = if (body != null) {
                            body.string()
                        } else {
                            ""
                        }
                        logVerbose(LoggingInterceptor.TAG, result)
                        val gson = GsonBuilder().disableHtmlEscaping().create()
                        val responseModel = gson.fromJson(result, requestModel)
                        response.close()
                        notifyResponse(responseModel)
                    } else {
                        notifyFailure(ResponseCodeException(response.code()))
                    }
                } catch (e: Exception) {
                    notifyFailure(e)
                }

            }

            override fun onFailure(call: Call, e: IOException) {
                notifyFailure(e)
            }

        })
    }
```

#### 1.4 回调函数处理
实现返回数据的处理，或更新UI或抛出异常，或下文文件等等...

```kotlin
    abstract fun listen(callback: Callback?)
 
    /**
     * 当请求响应成功的时候，将服务器响应转换后的实体类进行回调。
     * @param response
     * 服务器响应转换后的实体类
     */
    private fun notifyResponse(response: com.quxianggif.network.model.Response) {
        callback?.let {
            if (it is OriginThreadCallback) {
                it.onResponse(response)
                callback = null
            } else {
                GifFun.getHandler().post {
                    it.onResponse(response)
                    callback = null
                }
            }
        }
    }

    /**
     * 当请求响应失败的时候，将具体的异常进行回调。
     * @param e
     * 请求响应的异常
     */
    private fun notifyFailure(e: Exception) {
        callback?.let {
            if (it is OriginThreadCallback) {
                it.onFailure(e)
                callback = null
            } else {
                GifFun.getHandler().post {
                    it.onFailure(e)
                    callback = null
                }
            }
        }
    }

 
```








