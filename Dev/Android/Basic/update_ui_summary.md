## Android 异步更新 UI



Android中有下列几种异步更新ui的解决办法：

- Activity.runOnUiThread(Runnable)
- View.post(Runnable)
- View.postDelayed(Runnable, long)
- Handler <font color=#D2691E>`推荐`</font>
- AsyncTask <font color=#D2691E>`推荐`</font>
- Summary

### 1. Activity.runOnUiThread
通常，在 Activity，我们可以使用 Activity 的 runOnUiThread 方法来更新 UI 。
```java
public void onClick(View v) { 
  new Thread(new Runnable() { 
    public void run() { 
      Bitmap bitmap = loadImageFromNetwork("http://example.com/image.png");
      runOnUiThread(new Runnable() {
        @Override
        public void run() {
          mImageView.setImageBitmap(bitmap); 
        }
      });       
    } 
  }).start(); 
}
```

### 2. View.post(Runable)

View 类及其子类提供了一个 post(Runable) 方法允许我们将我们要做的操作放到这个匿名 Runable 对象的 run 方法中，在这个方法里面我们可以直接更新 UI。
```java
public void onClick(View v) { 
  new Thread(new Runnable() { 
    public void run() { 
      Bitmap bitmap = loadImageFromNetwork("http://example.com/image.png");
      imageView.post(new Runnable() {
       @Override
       public void run() {
         mImageView.setImageBitmap(bitmap); 
       }
      });       
    } 
  }).start(); 
}
```

### 3. View.postDelayed(Runnable, long)
和 View.post(Runable) 方法一样，只是延迟第二个参数指定的时间后执行，而 View.post(Runable) 是立即执行。
```java
public void onClick(View v) { 
  new Thread(new Runnable() { 
    public void run() { 
      Bitmap bitmap = loadImageFromNetwork("http://example.com/image.png"); 
      imageView.postDelayed(new Runnable() {
       @Override
       public void run() {
         mImageView.setImageBitmap(bitmap); 
       }
      },2000);     
    } 
  }).start(); 
}
```

### 4. Handler <font color=#D2691E>`推荐`</font>
前面的几种方法当操作过多时，代码会显得臃肿，代码及业务都难于管理控制。所以，当遇到这类代码较多的时候推荐使用 Handler 方式。

```java
new Thread(new Runnable() { 
  public void run() { 
    Bitmap bitmap = loadImageFromNetwork("http://example.com/image.png"); 
    Message message = mHandler.obtainMessage();
    message.what = 1;
    message.obj = bitmap;
    mHandler.sendMessage(message);    
  } 
}).start();
```

```java
  Handler mHandler = new Handler(){
  @Override
  public void handleMessage(Message msg) {
    switch (msg.what){
      case 1:
        Bitmap bitmap = (Bitmap) msg.obj;
        imageView.setImageBitmap(bitmap);
        break;
      case 2:
        // ...
        break;
      default:
        break;
    }
  }
};
```
### 5. AsyncTask <font color=#D2691E>`推荐`</font>

Android 为我们提供了异步任务 AsyncTask，也可以使用 AsyncTask 轻松地实现异步加载数据及更新 UI。
```java
AsyncTask<String,Void,Bitmap> asyncTask = new AsyncTask<String, Void, Bitmap>() {
 
  /**
   * 即将要执行耗时任务时回调，这里可以做一些初始化操作
   */
  @Override
  protected void onPreExecute() {
    super.onPreExecute();
  }
 
  /**
   * 在后台执行耗时操作，其返回值将作为 onPostExecute 方法的参数
   * @param params
   * @return
   */
  @Override
  protected Bitmap doInBackground(String... params) {
    Bitmap bitmap = loadImageFromNetwork(params[0]);
    return bitmap;
  }
 
  /**
   * 当这个异步任务执行完成后，也就是doInBackground（）方法完成后，
   * 其方法的返回结果就是这里的参数
   * @param bitmap
   */
  @Override
  protected void onPostExecute(Bitmap bitmap) {
    imageView.setImageBitmap(bitmap);
  }
};
asyncTask.execute("http://example.com/image.png");
```

需要知道的是 `doInBackground` 方法工作在工作线程中，所以，我们在这个方法里面执行耗时操作。同时，由于其返回结果会传递到 `onPostExecute` 方法中，而 `onPostExecute` 方法工作在 UI 线程，这样我们就在这个方法里面更新 UI，达到了异步更新 UI 的目的。

### 6. Summary
事实上，对于 Android 的异步加载数据及更新ui，我们不仅可以选择 AsyncTask 异步任务，还可以选择许多开源的网络框架，如 xUtils，Volley，Okhttp，…，这些优秀的网络框架让我们异步更新ui变得非常简单，而且，效率和性能也非常高。

