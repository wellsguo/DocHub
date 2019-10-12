
## 需求

1. 完成数据的请求和返回
2. 显示请求进度
3. 数据缓存
4. 异常处理
5. 重连机制

## 封装伪代码

```java
1. OkHttp 实例化
2. Retrofit 实例化
3. api <- retrofit(apiInterface)
4. Observable<T> <- api.xXX()
5. observable.subscribeOn(Schedulers.io())
              .unsubscribeOn(Schedulers.io())
              .observeOn(AndroidSchedulers.mainThread())  
              .subscribe(  
                    new Subscriber<RetrofitEntity>() {  
                        @Override  
                        public void onCompleted() {  

                        }  

                        @Override  
                        public void onError(Throwable e) {  

                        }  

                        @Override  
                        public void onNext(RetrofitEntity retrofitEntity) {  

                        }sss

                        @Override  
                        public void onStart() {  

                        }
                    }  

            );  
}

```

## 如何创建 retrofit

## 如何抽象 Subscriber
