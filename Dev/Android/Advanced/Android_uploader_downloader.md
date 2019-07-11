
- [Android RxJava之网络处理](https://blog.csdn.net/u014610664/column/info/13297)
- [GitHub](https://github.com/wzgiceman/RxjavaRetrofitDemo-master)


## 上传篇
 
### 1. 定义 service 接口

注意：** Multipart** 是指定大文件上传过程中的标示，一般上传图片的过程中我们需要附带信息，所以我们需要用到 `@part` 指定传递的数值，`MultipartBody.Part` 是指定传递的文件；


```java
/*上传文件*/
@Multipart
@POST("AppYuFaKu/uploadHeadImg")
Observable<BaseResultEntity<UploadResulte>> uploadImage(@Part("uid") RequestBody uid, 
    @Part("auth_key") RequestBody  auth_key,
    @Part MultipartBody.Part file);
```

### 2. 加入进度条

retrofit 是基于 okhttp 的处理，所以我们可以自定义 RequestBody，复写 `writeTo(BufferedSink sink)` 方法，得到传递的进度数据

```java
public class ProgressRequestBody extends RequestBody {
    //实际的待包装请求体
    private final RequestBody requestBody;
    //进度回调接口
    private final UploadProgressListener progressListener;
    //包装完成的BufferedSink
    private BufferedSink bufferedSink;

    public ProgressRequestBody(RequestBody requestBody, UploadProgressListener progressListener) {
        this.requestBody = requestBody;
        this.progressListener = progressListener;
    }

    /**
     * 重写调用实际的响应体的contentType
     * @return MediaType
     */
    @Override
    public MediaType contentType() {
        return requestBody.contentType();
    }

    /**
     * 重写调用实际的响应体的contentLength
     * @return contentLength
     * @throws IOException 异常
     */
    @Override
    public long contentLength() throws IOException {
        return requestBody.contentLength();
    }

    /**
     * 重写进行写入
     * @param sink BufferedSink
     * @throws IOException 异常
     */
    @Override
    public void writeTo(BufferedSink sink) throws IOException {
        if (null == bufferedSink) {
            bufferedSink = Okio.buffer(sink(sink));
        }
        requestBody.writeTo(bufferedSink);
        //必须调用flush，否则最后一部分数据可能不会被写入
        bufferedSink.flush();
    }

    /**
     * 写入，回调进度接口
     * @param sink Sink
     * @return Sink
     */
    private Sink sink(Sink sink) {
        return new ForwardingSink(sink) {
            //当前写入字节数
            long writtenBytesCount = 0L;
            //总字节长度，避免多次调用contentLength()方法
            long totalBytesCount = 0L;

            @Override
            public void write(Buffer source, long byteCount) throws IOException {
                super.write(source, byteCount);
                
                //增加当前写入的字节数
                writtenBytesCount += byteCount;
                
                //获得contentLength的值，后续不再调用
                if (totalBytesCount == 0) {
                    totalBytesCount = contentLength();
                }

                Observable.just(writtenBytesCount).observeOn(AndroidSchedulers.mainThread()).subscribe(new Action1<Long>() {
                    @Override
                    public void call(Long aLong) {
                        progressListener.onProgress(writtenBytesCount, totalBytesCount);
                    }
                });
            }
        };
    }
}
```

### 3. 自定义接口，回调 progress 进度

```java
public interface UploadProgressListener {
    /**
     * 上传进度
     * @param currentBytesCount
     * @param totalBytesCount
     */
    void onProgress(long currentBytesCount, long totalBytesCount);
}
```

### 4. 创建 RequestBody 对象，加入进度

```java
File file=new File("/storage/emulated/0/Download/11.jpg");
RequestBody requestBody = RequestBody.create(MediaType.parse("image/jpeg"), file);
MultipartBody.Part part = MultipartBody.Part.createFormData("file_name", file.getName(), new ProgressRequestBody(requestBody,
        new UploadProgressListener() {
            @Override
            public void onProgress(long currentBytesCount, long totalBytesCount) {
                tvMsg.setText("提示:上传中");
                progressBar.setMax((int) totalBytesCount);
                progressBar.setProgress((int) currentBytesCount);
            }
}));
```

### 5. 传递附带信息

和封装二中post请求的方式一样，我们需要继承baseentity，复写里面的方法，然后设置需要传递的参数，因为是测试接口，所以我的参数直接写死在entity里面,part文件动态指定

```java
/**
 * 上传请求api
 * Created by WZG on 2016/10/20.
 */
public class UplaodApi extends BaseEntity {
    /*需要上传的文件*/
    private MultipartBody.Part part;


    public UplaodApi(HttpOnNextListener listener, RxAppCompatActivity rxAppCompatActivity) {
        super(listener, rxAppCompatActivity);
        setShowProgress(true);
    }

    public MultipartBody.Part getPart() {
        return part;
    }

    public void setPart(MultipartBody.Part part) {
        this.part = part;
    }

    @Override
    public Observable getObservable(HttpService methods) {
        RequestBody uid= RequestBody.create(MediaType.parse("text/plain"), "4811420");
        RequestBody key = RequestBody.create(MediaType.parse("text/plain"), "21f8d9bcc50c6ac1ae1020ce12f5f5a7");
        return methods.uploadImage(uid,key,getPart());
    }
}
```

### 6. post 请求处理

请求和封装二中的请求一样，通过传递一个指定的 HttpOnNextListener 对象来回调来监听结果信息，一一对应

```java
private void uploadeDo(){
    File file=new File("/storage/emulated/0/Download/11.jpg");
    RequestBody requestBody=RequestBody.create(MediaType.parse("image/jpeg"),file);
    MultipartBody.Part part= MultipartBody.Part.createFormData("file_name", file.getName(), new ProgressRequestBody(requestBody,
            new UploadProgressListener() {
                @Override
                public void onProgress(long currentBytesCount, long totalBytesCount) {
                    tvMsg.setText("提示:上传中");
                    progressBar.setMax((int) totalBytesCount);
                    progressBar.setProgress((int) currentBytesCount);
                }
    }));
    UplaodApi uplaodApi = new UplaodApi(httpOnNextListener,this);
    uplaodApi.setPart(part);
    HttpManager manager = HttpManager.getInstance();
    manager.doHttpDeal(uplaodApi);
}


/**
 * 上传回调
 */
HttpOnNextListener httpOnNextListener = new HttpOnNextListener<UploadResulte>() {
    @Override
    public void onNext(UploadResulte o) {
        tvMsg.setText("成功");
        Glide.with(MainActivity.this).load(o.getHeadImgUrl()).skipMemoryCache(true).into(img);
    }

    @Override
    public void onError(Throwable e) {
        super.onError(e);
        tvMsg.setText("失败："+e.toString());
    }

};
```

### 6. post 请求处理

请求和封装二中的请求一样，通过传递一个指定的HttpOnNextListener 对象来回调来监听结果信息，一一对应

```java
private void uploadeDo(){
    File file=new File("/storage/emulated/0/Download/11.jpg");
    RequestBody requestBody=RequestBody.create(MediaType.parse("image/jpeg"),file);
    MultipartBody.Part part= MultipartBody.Part.createFormData("file_name", file.getName(), new ProgressRequestBody(requestBody,
            new UploadProgressListener() {
        @Override
        public void onProgress(long currentBytesCount, long totalBytesCount) {
            tvMsg.setText("提示:上传中");
            progressBar.setMax((int) totalBytesCount);
            progressBar.setProgress((int) currentBytesCount);
        }
    }));
    UplaodApi uplaodApi = new UplaodApi(httpOnNextListener,this);
    uplaodApi.setPart(part);
    HttpManager manager = HttpManager.getInstance();
    manager.doHttpDeal(uplaodApi);
}


/**
 * 上传回调
 */
HttpOnNextListener httpOnNextListener=new HttpOnNextListener<UploadResulte>() {
    @Override
    public void onNext(UploadResulte o) {
        tvMsg.setText("成功");
        Glide.with(MainActivity.this).load(o.getHeadImgUrl()).skipMemoryCache(true).into(img);
    }

    @Override
    public void onError(Throwable e) {
        super.onError(e);
        tvMsg.setText("失败："+e.toString());
    }

};
```

## 下载篇


断点续传下载一直是移动开发中必不可少的一项重要的技术，同样的Rxjava和Retrofit的结合让这个技术解决起来更加的灵活，我们完全可以封装一个适合自的下载框架，简单而且安全！



### 1. 创建 service 接口

注意：Streaming 是判断是否写入内存的标示，如果小文件可以考虑不写，一般情况必须写；下载地址需要通过 `@url` 动态指定（不适固定的），`@head` 标签是指定下载的起始位置（断点续传的位置）

```java
/*断点续传下载接口*/
@Streaming/*大文件需要加入这个判断，防止下载过程中写入到内存中*/
@GET
Observable<ResponseBody> download(@Header("RANGE") String start, @Url String url);
```

### 2. 复写 ResponseBody

和之前的上传封装一样，下载更加的需要进度，所以我们同样覆盖 ResponseBody 类，写入进度监听回调

```java
/**
 * 自定义进度的body
 * @author wzg
 */
public class DownloadResponseBody extends ResponseBody {
    private ResponseBody responseBody;
    private DownloadProgressListener progressListener;
    private BufferedSource bufferedSource;

    public DownloadResponseBody(ResponseBody responseBody, DownloadProgressListener progressListener) {
        this.responseBody = responseBody;
        this.progressListener = progressListener;
    }

    @Override
    public BufferedSource source() {
        if (bufferedSource == null) {
            bufferedSource = Okio.buffer(source(responseBody.source()));
        }
        return bufferedSource;
    }

    private Source source(Source source) {
        return new ForwardingSource(source) {
            long totalBytesRead = 0L;

            @Override
            public long read(Buffer sink, long byteCount) throws IOException {
                long bytesRead = super.read(sink, byteCount);
                // read() returns the number of bytes read, or -1 if this source is exhausted.
                totalBytesRead += bytesRead != -1 ? bytesRead : 0;
                if (null != progressListener) {
                    progressListener.update(totalBytesRead, responseBody.contentLength(), bytesRead == -1);
                }
                return bytesRead;
            }
        };
    }
}
```

### 3. 自定义进度回调接口

```java
/**
 * 成功回调处理
 * Created by WZG on 2016/10/20.
 */
public interface DownloadProgressListener {
    /**
     * 下载进度
     * @param read
     * @param count
     * @param done
     */
    void update(long read, long count, boolean done);
}
```

### 4. 复写Interceptor

复写Interceptor，可以将我们的监听回调通过okhttp的client方法addInterceptor自动加载我们的监听回调和ResponseBody

```java
/**
 * 成功回调处理
 * Created by WZG on 2016/10/20.
 */
public class DownloadInterceptor implements Interceptor {

    private DownloadProgressListener listener;

    public DownloadInterceptor(DownloadProgressListener listener) {
        this.listener = listener;
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
        Response originalResponse = chain.proceed(chain.request());

        return originalResponse.newBuilder()
                .body(new DownloadResponseBody(originalResponse.body(), listener))
                .build();
    }
}
```

### 5. 封装请求 downinfo 数据

这个类中的数据可自由扩展，用户自己选择需要保持到数据库中的数据，可以自由选择需要数据库第三方框架，demo 采用 greenDao 框架存储数据

```java
public class DownInfo {
    /*存储位置*/
    private String savePath;
    /*下载url*/
    private String url;
    /*基础url*/
    private String baseUrl;
    /*文件总长度*/
    private long countLength;
    /*下载长度*/
    private long readLength;
    /*下载唯一的HttpService*/
    private HttpService service;
    /*回调监听*/
    private HttpProgressOnNextListener listener;
    /*超时设置*/
    private  int DEFAULT_TIMEOUT = 6;
    /*下载状态*/
    private DownState state;
}
```

### 6. DownState 状态封装

```java
public enum  DownState {
    START,
    DOWN,
    PAUSE,
    STOP,
    ERROR,
    FINISH,
}
```

### 7. 请求 HttpProgressOnNextListener 回调封装类

注意：这里和 DownloadProgressListener 不同，这里是下载这个过程中的监听回调，DownloadProgressListener 只是进度的监听 
通过抽象类，可以自由选择需要覆盖的类，不需要完全覆盖！更加灵活

```java
/**
 * 下载过程中的回调处理
 * Created by WZG on 2016/10/20.
 */
public abstract class HttpProgressOnNextListener<T> {
    /**
     * 成功后回调方法
     * @param t
     */
    public abstract void onNext(T t);

    /**
     * 开始下载
     */
    public abstract void onStart();

    /**
     * 完成下载
     */
    public abstract void onComplete();


    /**
     * 下载进度
     * @param readLength
     * @param countLength
     */
    public abstract void updateProgress(long readLength, long countLength);

    /**
     * 失败或者错误方法
     * 主动调用，更加灵活
     * @param e
     */
     public  void onError(Throwable e){

     }

    /**
     * 暂停下载
     */
    public void onPuase(){

    }

    /**
     * 停止下载销毁
     */
    public void onStop(){

    }
}
```

### 8. 封装回调 Subscriber
准备的工作做完，需要将回调和传入回调的信息统一封装到sub中，统一判断；和封装二的原理一样，我们通过自定义Subscriber来提前处理返回的数据，让用户字需要关系成功和失败以及向关心的数据，避免重复多余的代码出现在处理类中

sub需要继承DownloadProgressListener，和自带的回调一起组成我们需要的回调结果

传入DownInfo数据，通过回调设置DownInfo的不同状态，保存状态

通过RxAndroid将进度回调指定到主线程中（如果不需要进度最好去掉该处理避免主线程处理负担）

update进度回调在断点续传使用时，需要手动判断断点后加载的长度，因为指定断点下载长度下载后总长度=（物理长度-起始下载长度）

```java
/**
 * 用于在Http请求开始时，自动显示一个ProgressDialog
 * 在Http请求结束是，关闭ProgressDialog
 * 调用者自己对请求数据进行处理
 * Created by WZG on 2016/7/16.
 */
public class ProgressDownSubscriber<T> extends Subscriber<T> implements DownloadProgressListener {
    //弱引用结果回调
    private WeakReference<HttpProgressOnNextListener> mSubscriberOnNextListener;
    /*下载数据*/
    private DownInfo downInfo;


    public ProgressDownSubscriber(DownInfo downInfo) {
        this.mSubscriberOnNextListener = new WeakReference<>(downInfo.getListener());
        this.downInfo=downInfo;
    }

    /**
     * 订阅开始时调用
     * 显示ProgressDialog
     */
    @Override
    public void onStart() {
        if(mSubscriberOnNextListener.get()!=null){
            mSubscriberOnNextListener.get().onStart();
        }
        downInfo.setState(DownState.START);
    }

    /**
     * 完成，隐藏ProgressDialog
     */
    @Override
    public void onCompleted() {
        if(mSubscriberOnNextListener.get()!=null){
            mSubscriberOnNextListener.get().onComplete();
        }
        downInfo.setState(DownState.FINISH);
    }

    /**
     * 对错误进行统一处理
     * 隐藏ProgressDialog
     *
     * @param e
     */
    @Override
    public void onError(Throwable e) {
        /*停止下载*/
        HttpDownManager.getInstance().stopDown(downInfo);
        if(mSubscriberOnNextListener.get()!=null){
            mSubscriberOnNextListener.get().onError(e);
        }
        downInfo.setState(DownState.ERROR);
    }

    /**
     * 将onNext方法中的返回结果交给Activity或Fragment自己处理
     *
     * @param t 创建Subscriber时的泛型类型
     */
    @Override
    public void onNext(T t) {
        if (mSubscriberOnNextListener.get() != null) {
            mSubscriberOnNextListener.get().onNext(t);
        }
    }

    @Override
    public void update(long read, long count, boolean done) {
        if(downInfo.getCountLength()>count){
            read=downInfo.getCountLength()-count+read;
        }else{
            downInfo.setCountLength(count);
        }
        downInfo.setReadLength(read);
        if (mSubscriberOnNextListener.get() != null) {
            /*接受进度消息，造成UI阻塞，如果不需要显示进度可去掉实现逻辑，减少压力*/
            rx.Observable.just(read).observeOn(AndroidSchedulers.mainThread())
                    .subscribe(new Action1<Long>() {
                @Override
                public void call(Long aLong) {
                      /*如果暂停或者停止状态延迟，不需要继续发送回调，影响显示*/
                    if(downInfo.getState()==DownState.PAUSE||downInfo.getState()==DownState.STOP)return;
                    downInfo.setState(DownState.DOWN);
                    mSubscriberOnNextListener.get().updateProgress(aLong,downInfo.getCountLength());
                }
            });
        }
    }

}
```

### 9. 下载管理类封装 HttpDownManager

```java
/**
 * 获取单例
 * @return
 */
public static HttpDownManager getInstance() {
    if (INSTANCE == null) {
        synchronized (HttpDownManager.class) {
            if (INSTANCE == null) {
                INSTANCE = new HttpDownManager();
            }
        }
    }
    return INSTANCE;
}
```

因为单例所以需要记录正在下载的数据和回到sub

```java
/*回调sub队列*/
private HashMap<String, ProgressDownSubscriber> subMap;
/*单例对象*/
private volatile static HttpDownManager INSTANCE;

private HttpDownManager(){
    downInfos = new HashSet<>();
    subMap = new HashMap<>();
}
```

开始下载需要记录下载的service避免每次都重复创建，然后请求service接口，得到ResponseBody数据后将数据流写入到本地文件中（6.0系统后需要提前申请权限）

```java
/**
 * 开始下载
 */
public void startDown(DownInfo info){
    /*正在下载不处理*/
    if(info==null||subMap.get(info.getUrl())!=null){
        return;
    }
    /*添加回调处理类*/
    ProgressDownSubscriber subscriber=new ProgressDownSubscriber(info);
    /*记录回调sub*/
    subMap.put(info.getUrl(),subscriber);
    /*获取service，多次请求公用一个sercie*/
    HttpService httpService;
    if(downInfos.contains(info)){
        httpService=info.getService();
    }else{
        DownloadInterceptor interceptor = new DownloadInterceptor(subscriber);
        OkHttpClient.Builder builder = new OkHttpClient.Builder();
        //手动创建一个OkHttpClient并设置超时时间
        builder.connectTimeout(info.getConnectionTime(), TimeUnit.SECONDS);
        builder.addInterceptor(interceptor);

        Retrofit retrofit = new Retrofit.Builder()
                .client(builder.build())
                .addConverterFactory(GsonConverterFactory.create())
                .addCallAdapterFactory(RxJavaCallAdapterFactory.create())
                .baseUrl(info.getBaseUrl())
                .build();
        httpService= retrofit.create(HttpService.class);
        info.setService(httpService);
    }
    /*得到rx对象-上一次下載的位置開始下載*/
    httpService.download("bytes=" + info.getReadLength() + "-",info.getUrl())
            /*指定线程*/
            .subscribeOn(Schedulers.io())
            .unsubscribeOn(Schedulers.io())
            /*失败后的retry配置*/
            .retryWhen(new RetryWhenNetworkException())
            /*读取下载写入文件*/
            .map(new Func1<ResponseBody, DownInfo>() {
                @Override
                public DownInfo call(ResponseBody responseBody) {
                    try {
                        writeCache(responseBody,new File(info.getSavePath()),info);
                    } catch (IOException e) {
                        /*失败抛出异常*/
                        throw new HttpTimeException(e.getMessage());
                    }
                    return info;
                }
            })
            /*回调线程*/
            .observeOn(AndroidSchedulers.mainThread())
            /*数据回调*/
            .subscribe(subscriber);

}
```

- 写入文件 

注意：一开始调用进度回调是第一次写入在进度回调之前，所以需要判断一次 DownInfo 是否获取到下载总长度，没有这选择当前 ResponseBody 读取长度为总长度

```java
/**
 * 写入文件
 * @param file
 * @param info
 * @throws IOException
 */
public void writeCache(ResponseBody responseBody,File file,DownInfo info) throws IOException{
    if (!file.getParentFile().exists())
        file.getParentFile().mkdirs();
    long allLength;
    if (info.getCountLength()==0){
        allLength=responseBody.contentLength();
    }else{
        allLength=info.getCountLength();
    }
    FileChannel channelOut = null;
    RandomAccessFile randomAccessFile = null;
    randomAccessFile = new RandomAccessFile(file, "rwd");
    channelOut = randomAccessFile.getChannel();
    MappedByteBuffer mappedBuffer = channelOut.map(FileChannel.MapMode.READ_WRITE,
            info.getReadLength(),allLength-info.getReadLength());
    byte[] buffer = new byte[1024*8];
    int len;
    int record = 0;
    while ((len = responseBody.byteStream().read(buffer)) != -1) {
        mappedBuffer.put(buffer, 0, len);
        record += len;
    }
    responseBody.byteStream().close();
    if (channelOut != null) {
        channelOut.close();
    }
    if (randomAccessFile != null) {
        randomAccessFile.close();
    }
}
```

- 停止下载 

调用 subscriber.unsubscribe()解除监听，然后remove记录的下载数据和sub回调，并且设置下载状态（同步数据库自己添加）

```java
/**
 * 停止下载
 */
public void stopDown(DownInfo info){
    if(info==null)return;
    info.setState(DownState.STOP);
    info.getListener().onStop();
    if(subMap.containsKey(info.getUrl())) {
        ProgressDownSubscriber subscriber=subMap.get(info.getUrl());
        subscriber.unsubscribe();
        subMap.remove(info.getUrl());
    }
    /*同步数据库*/
}
```

- 暂停下载 

```java
/**
 * 暂停下载
 * @param info
 */
public void pause(DownInfo info){
    if(info==null)return;
    info.setState(DownState.PAUSE);
    info.getListener().onPuase();
    if(subMap.containsKey(info.getUrl())){
        ProgressDownSubscriber subscriber=subMap.get(info.getUrl());
        subscriber.unsubscribe();
        subMap.remove(info.getUrl());
    }
    /*这里需要讲info信息写入到数据中，可自由扩展，用自己项目的数据库*/
}
```

- 暂停全部和停止全部下载任务
 
```java
/**
 * 停止全部下载
 */
public void stopAllDown(){
    for (DownInfo downInfo : downInfos) {
        stopDown(downInfo);
    }
    subMap.clear();
    downInfos.clear();
}

/**
 * 暂停全部下载
 */
public void pauseAll(){
    for (DownInfo downInfo : downInfos) {
        pause(downInfo);
    }
    subMap.clear();
    downInfos.clear();
}
```
