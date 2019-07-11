## Apk Upgrade

### 1. 核心步骤

#### 1.1 detection for upgrade

升级检测主要是匹配服务器与本地版本号是否一致，不一致则需要下载更新。  
其中注意 `versionCode` 和 `versionName` 的区别，versionCode 多用于程序的更新检测和程序员开发使用，而 versionName 更加倾向于普通用户的阅读使用。 
```
private void getCurrentVersion() {
    if (null == mContext)
        return;

    try {
        PackageInfo info = mContext.getPackageManager().getPackageInfo(mContext.getPackageName(), 0);
        localVersionCode = info.versionCode;
    } catch (PackageManager.NameNotFoundException e) {
        e.printStackTrace();
    }
}
``` 
##### 1.1.1 versionName

常见软件版本号的形式是 major.minor.maintenance.build
 - major是主版本号，一般在软件有重大升级时增长
 - minor是次版本号，一般在软件有新功能时增长
 - maintenance是维护版本，一般在软件有主要的问题修复后增长
 - build构建版本（测试版本一般会用到）
   
正式版本：major.minor.maintenance----1.0.0  
测试版本：major.minor.maintenance.build----1.0.0.5  



##### 1.1.2 versionCode

以5位数的 int 来表示 (每次升级版本时,versioncode的值都要比以前的值要大)

正式版本：major.minor.maintenance----1.0.0（versioncode:10000）  
测试版本：major.minor.maintenance.build----1.0.0.5(versioncode:10005)



#### 1.2 download

网络下载可以使用 OKHttp 或 HTTPURLConnection 发送请求。

```java
public class DownloadManager {

    private static final String TAG = "DownloadManager";

    private static DownloadManager DOWNLOAD_MANAGER;

    public static DownloadManager getInstance() {
        if (DOWNLOAD_MANAGER == null) {
            DOWNLOAD_MANAGER = new DownloadManager();
        }
        return DOWNLOAD_MANAGER;
    }

    private DownloadManager() {

    }


    public void download(final String url, final String saveDir, final OnDownloadListener listener) {
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .readTimeout(20, TimeUnit.SECONDS)
                .build();

        final Request request = new Request.Builder()
                .url(url)//请求的url
                .get()
                .build();

        okHttpClient.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Call call, IOException e) {
                // 下载失败
                listener.onDownloadFailed();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                Log.e(TAG, "onResponse: "+ "开始下载" );
                InputStream is = null;
                byte[] buf = new byte[2048];
                int len = 0;
                FileOutputStream fos = null;
                // 储存下载文件的目录
                String savePath = isExistDir(saveDir);
                try {
                    is = response.body().byteStream();
                    long total = response.body().contentLength();
                    File file = new File(savePath, getNameFromUrl(url));
                    fos = new FileOutputStream(file);
                    long sum = 0;
                    while ((len = is.read(buf)) != -1) {
                        fos.write(buf, 0, len);
                        sum += len;
                        int progress = (int) (sum * 1.0f / total * 100);
                        // 下载中
                        listener.onDownloading(progress);
                    }
                    fos.flush();
                    // 下载完成
                    listener.onDownloadSuccess();
                } catch (Exception e) {
                    Log.e(TAG, "onResponse: "+ "存储数据异常" + e.getMessage() );
                    listener.onDownloadFailed();
                } finally {
                    try {
                        if (is != null)
                            is.close();
                    } catch (IOException e) {
                    }
                    try {
                        if (fos != null)
                            fos.close();
                    } catch (IOException e) {
                    }
                }
            }
        });
    }

    private String isExistDir(String saveDir) throws IOException {
        // 下载位置
        File downloadFile = new File(Environment.getExternalStorageDirectory(), saveDir);
        if (!downloadFile.mkdirs()) {
            downloadFile.createNewFile();
        }
        String savePath = downloadFile.getAbsolutePath();
        return savePath;
    }

    private String getNameFromUrl(String url) {
        return url.substring(url.lastIndexOf("/") + 1);
    }

    public interface OnDownloadListener {

        void onDownloadSuccess();

        void onDownloading(int progress);

        void onDownloadFailed();
    }

}
```
注意事项：  
1） 在 DownloadManager 中采用监听 Listener 机制。监听下载成功，失败和下载中三种状态。采用 Listener 将三种状态的实现延迟到了具体的实现中，有很强的抽象能力；  
2） 注意单例的使用，此处非最优实现；  
3） OKHttp get / post 请求的实现；  
4） 在下载过程中，需要访问到 SDCard，注意动态权限的申请。


#### 1.3 install apk

下载完成后，安装APK，需要注意不同的 API 版本会有很大的差别。

```java   
private void installApk(Context context, String app)
{
    File file = new File(app);
    // 兼容 8.0
    boolean installAllowed;
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        installAllowed = context.getPackageManager().canRequestPackageInstalls();
        if (installAllowed) {
            installApk(context, file);
        } else {
            Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                Uri.parse("package:" + context.getPackageName()));
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent);
            installApk(context, file);
            return;
        }
    } else {
        installApk(context, file);
    }
}
```

```java
private void installApk(Context context, File file) {
    if (!file.exists()) {
        return;
    }

    Intent intent = new Intent(Intent.ACTION_VIEW);
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    // 兼容 7.0
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
        Uri apkUri = FileProvider.getUriForFile(context, "com.kys.ct.demostration.fileprovider", file);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        intent.setDataAndType(apkUri, "application/vnd.android.package-archive");
    } else {
        // earlier
        intent.setDataAndType(Uri.fromFile(file),"application/vnd.android.package-archive");
    }

    context.startActivity(intent);
}
```

仅仅上述两个方法是无法实现真正的 APK 安装的，在这之前，还有权限的配置和访问路径的相关设置。

##### 1.3.1 权限配置

在 AndroidManifest.xml 中添加 REQUEST_INSTALL_PACKAGES 权限
```
<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />
```

##### 1.3.2 FileProvider

- a AndroidManifest.xml 配置
```
<application
        ...>
    <provider
        android:name="android.support.v4.content.FileProvider"
        android:authorities="com.kys.ct.demostration.fileprovider"
        android:exported="false"
        android:grantUriPermissions="true">
        <meta-data
            android:name="android.support.FILE_PROVIDER_PATHS"
            android:resource="@xml/file_paths" />
    </provider>
    ...
</application>
```
需要注意的地方有四处：  
1）```authorities="com.kys.ct.demostration.fileprovider``` 必须和 installApk 中的 FileProvider 的 authorities 一致；  
2）exported="false"；  
3）grantUriPermissions="true"；  
4）android:resource="@xml/file_paths" 中的即为 res/xml/file_paths；

- b file_paths.xml
```
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="download" path="" />
</paths>
```
[更多>>](https://www.jianshu.com/p/577816c3ce93)

