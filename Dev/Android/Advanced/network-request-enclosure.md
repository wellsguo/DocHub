

## RxJava 调用

```java
public <T> void call(Observable<T> o, DisposableObserver<T> s) {
    o.subscribeOn(Schedulers.io())
            .unsubscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .retry(RETRY_COUNT)//请求失败重连次数
            .subscribe(s);
}
```

### 1. 被观察者 Obeserverable&lt;T> 
被观察者即数据生产者，主要完成网络数据的请求和转换等。

### 2. 观察者 DisposableObserver&lt;T>
观察者即数据的消费者，对获取到的数据进行处理，显示在 UI 中，或者保存为文件等。

### 3. 运行线程
```java
...
.subscribeOn(Schedulers.io()) // 被观察者(生产者) 运行在 IO 线程（效率高），也可 new Thread，
.observeOn(AndroidSchedulers.mainThread()) // 观察者(消费者)运行在主线程，主要为了更新 UI
...
```

## 观察者的产生

```java
Api api = retrofitInstance.create(Api.class);
Observerable<T> observerable = api.getXXX(params...);
```
### 1. retrofit 实例化
```java
retrofitInstance = new Retrofit.Builder()
        .client(okHttpClient)
        .baseUrl(API_HOST)
        .addConverterFactory(GsonConverterFactory.create())
        .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
        .build();
```
### 2. Api 定义

```java
    @GET('{user}')
    Observable<XResponse<User>> getUser(@Query("id")String id); // 可用参数注解@Query,@QueryMap, @Path
    
    @FormUrlEncoded
    @POST("{login}")
    Observable<XResponse<User>> login(@Field("name") String name,
                       @FieldMap Map params); // @Body、@Field，@FieldMap、@Part，@PartMap，@Path
    
    @Multipart
    @POST("{upload}")
    Observable<User> upload(@Part ("file") MultipartBody.Part file, @Part(“key”) RequestBody key,
                      @PartMap Map<String,RequestBody> files);
                               
    @Streaming //大文件时要加不然会OOM
    @GET
    Observable<ResponseBody> download(@Url String fileUrl);
    
    @Headers({
        "Accept: application/vnd.yourapi.v1.full+json",
        "User-Agent: Your-App-Name"
    })
    @GET("/tasks/{task_id}")
    Observable<XResponse<Task>> getTask(@Path("task_id") long taskId);
```

注解 | 说明
 --  | -- 
@Get | 用的参数注解就@Query,@QueryMap
@Post | 则会用到 @Body、@Field，@FieldMap，@Part，@PartMap
@Body | 将数据转化成Json,然后post
@Field<br>@FieldMap | post上传表单.<br>需要添加上面的@FormUrlEncoded表示表单提交 ,对应Content-Type:application/x-www-form-urlencoded
@Part<br>@PartMap | post上传文件/数据.其中<br>@Part MultipartBody.Part 类型代表文件;<br>@Part(“key”) RequestBody类型代表参数,需要添加@Multipart表示支持文件上传的表单，Content-Type: multipart/form-data;<br>如果参数较少,使用@Part ("file")就可以解决了,如果参数较多,那就需要使用@PartMap

### 观察者  

```java
public abstract class BaseObserver<T> implements Observer<T> {

    protected String errMsg = "";
    protected Disposable disposable;

    @Override
    public void onSubscribe(Disposable d) {
        disposable = d;
    }

    @Override
    public void onNext(T t) {}

    @Override
    public void onError(Throwable e) {
        LogUtils.d("Subscriber onError", e.getMessage());
        if (!NetworkUtils.isConnected()) {
            errMsg = "网络连接出错,";
        } else if (e instanceof APIException) {
            APIException exception = (APIException) e;
            errMsg = exception.getMessage() + ", ";
        } else if (e instanceof HttpException) {
            errMsg = "网络请求出错,";
        } else if (e instanceof IOException) {
            errMsg = "网络出错,";
        }

        if (disposable != null && !disposable.isDisposed()) {
            disposable.dispose();
        }
    }

    @Override
    public void onComplete() {
        if (disposable != null && !disposable.isDisposed()) {
            disposable.dispose();
        }
    }
}
// --------------------- 
//作者：Stephec 
//来源：CSDN 
//原文：https://blog.csdn.net/c_j33/article/details/78774546 
//版权声明：本文为博主原创文章，转载请附上博文链接！
```


> 封装请求（登录为例）

```
public void login(String phone, String password, BaseObserver<ResponseBean<UidBean>> observer) {
    userService.login(phone,password)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(observer);
}
```

> 方法调用

```
APIUser.getInstance().login(phone, password, new BaseObserver<ResponseBean<UidBean>>() {
     @Override
     public void onNext(ResponseBean<UidBean> responseBean) {
        ToastUtils.showShort("登录成功");
     }
 });
// --------------------- 
// 作者：Stephec 
// 来源：CSDN 
// 原文：https://blog.csdn.net/c_j33/article/details/78774546 
// 版权声明：本文为博主原创文章，转载请附上博文链接！
```