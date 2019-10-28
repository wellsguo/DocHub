
## 为什么要插件化开发和动态加载呢？我认为原因有三点：

- 可以实现解耦

- 可以解除单个dex函数不能超过65535的限制
- 可以给apk瘦身，比如说360安全卫士，整个安装包才13.7M，对于一个用户量上亿的app这个大小已经很小了，它里面很多功能都是以插件的形式存在的

## 主要解决三个问题

- 1. 如何加载插件apk的资源文件？

- 2. 如何调用插件apk的方法？

- 3. 如何加载插件中的activity，并且有生命周期？

## 第一个问题：如何加载插件apk的资源文件？

对于第一个问题我们假设有这么一个需求：我们有个app想做类似qq换肤的功能，但是这个皮肤文件很大，如果跟宿主app一起打包的话可能会导致apk包很大，希望通过插件的方式，在用户需要换肤的时候去下载各种皮肤插件，来完成换肤的需求。

首先要了解一个类：

### DexClassLoader 
DexClassLoader是一个类加载器，可以用来从.jar和.apk文件中加载class。可以用来加载执行没用和应用程序一起安装的那部分代码。

构造函数：
```java
DexClassLoader(
String dexPath, //被解压的apk路径，不能为空。
String optimizedDirectory, //解压后的.dex文件的存储路径，不能为空。这个路径强烈建议使用应用程序的私有路径，不要放到sdcard上，否则代码容易被注入攻击。
String libraryPath, //os库的存放路径，可以为空，若有os库，必须填写。
ClassLoader parent//父亲加载器，一般为ClassLoader.getSystemClassLoader()。
)
```

### AssetManager
中的内部的方法addAssetPath，
将插件apk路径传入,从而添加进assetManager中，
然后通过new Resource把assetManager传入构造方法中，
可以得到未安装apk对应的Resource对象。

```java
    /**
     * Add an additional set of assets to the asset manager.  This can be
     * either a directory or ZIP file.  Not for use by applications.  Returns
     * the cookie of the added asset, or 0 on failure.
     * {@hide}
     */
    public final int addAssetPath(String path) {
        int res = addAssetPathNative(path);
        return res;
    }
```

接下来解决这个问题的思路是，先把插件apk下载到本地sd卡上，然后获取这个apk的信息，最后用DexClassLoader动态加载

#### 第一步，下载插件apk：

```java
    /**
     * 下载插件apk
     * */
    private void downLoadPlugApk() {
        DownloadUtils.get().downloadFile(APK_URL, new File(PLUG_APP_PATH, APK_NAME), new DownLoadListener() {
            @Override
            public void onFail(File file) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(UnInstallActivity.this,"下载失败",Toast.LENGTH_LONG).show();
                    }
                });

            }

            @Override
            public void onSucess(File file) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btn_download_plug_apk.setText("下载插件apk");
                        Toast.makeText(UnInstallActivity.this,"下载成功",Toast.LENGTH_LONG).show();
                    }
                });

            }

            @Override
            public void onProgress(long bytesRead, long contentLength, boolean done) {
                LogUtils.d("contentLength:"+contentLength+" | bytesRead:"+bytesRead+" | done:"+done);
                final float persent = (float) bytesRead / contentLength*100;
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        btn_download_plug_apk.setText((int)persent+"%");
                    }
                });
            }
        });

    }
```

这个插件apk里面有一张图片test.png放在mipmap-xxhdpi目录下，我是先把plugapp.apk文件放在一个服务器上，通过代码下载到sd卡的根目录下面

#### 第二步，获取plugapk的信息 通过PackageManager的getPackageArchiveInfo方法获得

```java
    /**
     * 获取未安装apk的信息
     * @param context
     * @param apkPath apk文件的path
     * @return
     */
    private String[] getUninstallApkInfo(Context context, String apkPath) {
        String[] info = new String[2];
        PackageManager pm = context.getPackageManager();
        PackageInfo pkgInfo = pm.getPackageArchiveInfo(apkPath, PackageManager.GET_ACTIVITIES);
        if (pkgInfo != null) {
            ApplicationInfo appInfo = pkgInfo.applicationInfo;
            String versionName = pkgInfo.versionName;//版本号
            Drawable icon = pm.getApplicationIcon(appInfo);//图标
            String appName = pm.getApplicationLabel(appInfo).toString();//app名称
            String pkgName = appInfo.packageName;//包名
            info[0] = appName;
            info[1] = pkgName;
        }
        return info;
    }
```

#### 第三步，获取Resource对象

```java
    /**
     * @param apkPath
     * @return 得到对应插件的Resource对象
     * 通过得到AssetManager中的内部的方法addAssetPath，
     * 将未安装的apk路径传入从而添加进assetManager中，
     * 然后通过new Resource把assetManager传入构造方法中，进而得到未安装apk对应的Resource对象。
     */
    private Resources getPluginResources(String apkPath) {
        try {
            AssetManager assetManager = AssetManager.class.newInstance();
            Method addAssetPath = assetManager.getClass().getMethod("addAssetPath", String.class);//反射调用方法addAssetPath(String path)
            //第二个参数是apk的路径：Environment.getExternalStorageDirectory().getPath()+File.separator+"plugin"+File.separator+"apkplugin.apk"
            //将未安装的Apk文件的添加进AssetManager中，第二个参数为apk文件的路径带apk名
            addAssetPath.invoke(assetManager, apkPath);
            Resources superRes = this.getResources();
            Resources mResources = new Resources(assetManager, superRes.getDisplayMetrics(), superRes.getConfiguration());
            return mResources;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
```

#### 第四步，通过DexClassLoader获得resid

```java
    /**
     * 加载apk获得内部资源
     * @param apkPath apk路径
     * @throws Exception
     */
    private int getRecourceIdFromPlugApk(String apkPath,String apkPackageName) throws Exception {
        File optimizedDirectoryFile = getDir("dex", Context.MODE_PRIVATE);//在应用安装目录下创建一个名为app_dex文件夹目录,如果已经存在则不创建
        Log.v("zxy", optimizedDirectoryFile.getPath().toString());// /data/data/com.example.dynamicloadapk/app_dex
        //参数：1、包含dex的apk文件或jar文件的路径，2、apk、jar解压缩生成dex存储的目录，3、本地library库目录，一般为null，4、父ClassLoader
        DexClassLoader dexClassLoader = new DexClassLoader(apkPath, optimizedDirectoryFile.getPath(), null, ClassLoader.getSystemClassLoader());
        Class<?> clazz = dexClassLoader.loadClass(apkPackageName + ".R$mipmap");//通过使用apk自己的类加载器，反射出R类中相应的内部类进而获取我们需要的资源id
        Field field = clazz.getDeclaredField("test");//得到名为test的这张图片字段
        int resId = field.getInt(R.id.class);//得到图片id
        return resId;
    }
```

#### 第五步，实现换肤效果

```java
    /**
     * 加载资源
     * */
    private void loadPlugResource() {

        String[] apkInfo = getUninstallApkInfo(this, PLUG_APP_PATH + "/" + APK_NAME);
        String appName = apkInfo[0];
        String pkgName = apkInfo[1];
        Resources resource = getPluginResources(APK_PATH);
        try {
            int resid = getRecourceIdFromPlugApk(APK_PATH, pkgName);
            activity_un_install.setBackgroundDrawable(resource.getDrawable(resid));
        } catch (Exception e) {
            e.printStackTrace();

        }

    }
```

## 第二个问题：如何调用插件apk的方法？
根据第一个问题就可以得到答案， 通过DexClassLoader加载类，然后通过反射机制执行类里面的方法

```java
    /**
     * @param apkPath apk路径
     * @throws Exception
     */
    private String runPlugApkMethod(String apkPath,String apkPackageName) throws Exception {
        File optimizedDirectoryFile = getDir("dex", Context.MODE_PRIVATE);//在应用安装目录下创建一个名为app_dex文件夹目录,如果已经存在则不创建
        Log.v("zxy", optimizedDirectoryFile.getPath().toString());// /data/data/com.example.dynamicloadapk/app_dex
        //参数：1、包含dex的apk文件或jar文件的路径，2、apk、jar解压缩生成dex存储的目录，3、本地library库目录，一般为null，4、父ClassLoader
        DexClassLoader dexClassLoader = new DexClassLoader(apkPath, optimizedDirectoryFile.getPath(), null, ClassLoader.getSystemClassLoader());
//        //通过使用apk自己的类加载器，反射出R类中相应的内部类进而获取我们需要的资源id
//        Class<?> clazz = dexClassLoader.loadClass(apkPackageName + ".R$mipmap");
//        Field field = clazz.getDeclaredField("test");//得到名为test的这张图片字段
//        int resId = field.getInt(R.id.class);//得到图片id

        // 使用DexClassLoader加载类
        Class libProvierClazz = dexClassLoader.loadClass(apkPackageName+".TestDynamic");
        //通过反射运行sayHello方法
        Object obj=libProvierClazz.newInstance();
        Method method=libProvierClazz.getMethod("sayHello");
        return (String)method.invoke(obj);

    }
```

## 第三个问题：如何加载插件中的activity，并且有生命周期？

这个问题是最关键的问题，我们知道通过DexClassLoader可以加载插件app里的任何类包括Activity，也可以执行其中的方法，但是Android中的四大组件都有一个特点就是他们有自己的启动流程和生命周期，我们使用DexClassLoader加载进来的Activity是不会涉及到任何启动流程和生命周期的概念，说白了，他就是一个普普通通的类。所以启动肯定会出错。

这里就要看一下activity的启动流程了，步骤太多就不写了，可以网上搜一下资料或者看《Android源码情景分析》这本书介绍的很详细，一个简单的启动要涉及到30多个步骤。

加载Activity的时候，有一个很重要的类：`LoadedApk.Java` 他内部有一个mClassLoader变量是负责加载一个Apk程序d的，所以可以从这里入手，我们首先要获取这个对象，这个对象在ActivityThread中有实例，
`ActivityThread` 类中有一个自己的static对象，然后还有一个ArrayMap存放Apk包名和LoadedApk映射关系的数据结构，那么我们分析清楚了，下面就来通过反射来获取mClassLoader对象。

```java
 private void loadApkClassLoader(DexClassLoader dLoader){
        try{
            String filesDir = this.getCacheDir().getAbsolutePath();
            String libPath = filesDir+File.separator+APK_NAME;

            // 配置动态加载环境
            Object currentActivityThread = RefInvoke.invokeStaticMethod("android.app.ActivityThread", "currentActivityThread", new Class[] {}, new Object[] {});//获取主线程对象 http://blog.csdn.net/myarrow/article/details/14223493
            //当前apk的包名
            String packageName = this.getPackageName();
            ArrayMap mPackages = (ArrayMap) RefInvoke.getFieldOjbect( "android.app.ActivityThread", currentActivityThread, "mPackages");
            WeakReference wr = (WeakReference) mPackages.get(packageName);
            RefInvoke.setFieldOjbect("android.app.LoadedApk", "mClassLoader", wr.get(), dLoader);

        }catch(Exception e){
            e.printStackTrace();
        }


    }
```
所以我们是通过将LoadedApk中的mClassLoader替换成我们的DexClassLoader来实现加载plugappActivity的

```java
   /**
     * 运行插件apk
     * */
    private void runPlug() {
        String filesDir = this.getCacheDir().getAbsolutePath();
        String libPath = filesDir+File.separator+APK_NAME;
        loadResources(libPath);
        DexClassLoader loader = new DexClassLoader(libPath, filesDir, filesDir, ClassLoader.getSystemClassLoader());
//        DexClassLoader loader = new DexClassLoader(libPath, filesDir,null, getClassLoader());
        Class<?> clazz = null;
        try {
            clazz = loader.loadClass("com.demo.plug.MainActivity");

            Class rClazz = loader.loadClass("com.demo.plug.R$layout");
            Field field = rClazz.getField("activity_main");
            Integer ojb = (Integer)field.get(null);

            View view = LayoutInflater.from(this).inflate(ojb, null);

            Method method = clazz.getMethod("setLayoutView", View.class);
            method.invoke(null, view);
            Log.i("demo", "field:"+ojb);

            loadApkClassLoader(loader);

            Intent intent = new Intent(RunPlugActivity.this, clazz);
            startActivity(intent);

        } catch (Throwable e) {
            Log.i("inject","error:"+Log.getStackTraceString(e));
            e.printStackTrace();
        }

    }
```

说白了就是偷梁换柱，欺骗系统来达到启动插件的目的。360的插件框架就是使用这种技术称之为hook技术，然后通过预先占坑的方式来预注册Activity。携程的这套插件化开发框架则是使用代理的模式来实现启动插件Activity的，所有activity都需要继承自proxy avtivity（proxy avtivity负责管理所有activity的生命周期），它的优点是不需要预先占坑了（不需要预先在宿主的清单文件里注册actvity）缺点是不支持Service和BroadCastReceiver，因为activity的生命周期启动还是比较复杂的，所以个人觉得携程的这套插件化框架实现起来是比较有难度的。

最后，除了上面这种方式还有两种： 

- 通过合并 PathClassLoader 和 DexClassLoader中的dexElements 数组，
- 动态代理加载Activity

这里只是做了一个最简单的探讨，如果想要做一套插件化开发框架可能要对android的framework层有一个更深入的理解，但是大概原理和思路我觉得是差不多的。