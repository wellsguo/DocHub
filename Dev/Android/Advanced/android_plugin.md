## 一、 定义 & 理解

**插件**：Plug-in 又称 add-in、addon 或 add-on, 也称外挂，它是一种 ***遵循一定规范的应用程序接口*** 编写出来的程序。

我的理解就是：插件是一个程序的辅助或者扩展功能模块，对程序来说插件可有可无，但它能给予程序一定的额外功能。

## 二、背景
Android 插件化的概念始于2012年，出自于免安装的想法。发展到后来，Android 应用程序更多的需要依赖一些第三方库，比如地图 SDK、分享 SDK、支付 SDK 等等，导致安装包变得越来越大，单是依赖这些 sdk，安装包可能就会额外的增加 20-30M 的大小；当需要新增功能时，不得不重新更新整个安装包。所以这时插件化的需求就变得更为更为突出。

插件化主要是解决的是 **减少应用程序大小**、**免安装扩展功能**。一般具一定规模的程序应用插件化才有意义。

## 三、原理

插件本身是一个独立的apk文件，要实现插件动态加载运行，需要了解apk的运行机制。java 虚拟机运行的是class 文件，使用 ClassLoader 加载；而 Android 虚拟机运行的是 dex 文件使用的是 DexClassLoader，而资源是存在 xml 文件中，所以就会涉及到资源文件的加载过程，所以要实现插件的动态加载运行，首先就需要解决**类文件**、**资源**、**库**等的加载。

### 3.1、类加载

Android 运行的是 dex 文件对应的类加载器是 PathClassLoader 和 DexClassLoader，PathClassLoader 和 DexClassLoader 均继承自 BaseDexClassLoader，BaseDexClassLoader 又继承自 ClassLoader。

> 我们来看下 DexClassLoader 基类 BaseDexClassLoader 的构造函数

```java
    /**
     * @param dexPath 目标类所在的apk或jar文件路径，类加载器将从这个apk或jar文件路径查找目标类
     * @param optimizedDirectory 从apk中解压出dex文件，经过odex优化之后，将解压和优化后的dex文件存放到optimizedDirectory 目录，下次直接从这个目录中的dex文件加载目标类。注意从API26开始此参数已经废弃
     * @param librarySearchPath  目标类所使用的c/c++库路径
     * @param parent 父类ClassLoader
     */
    public BaseDexClassLoader(String dexPath, File optimizedDirectory,
            String librarySearchPath, ClassLoader parent) {
        super(parent);
         // 解压、加载dex、资源文件，保存存放dex、资源文件、库文件路径等
        this.pathList = new DexPathList(this, dexPath, librarySearchPath, null);

        if (reporter != null) {
            reportClassLoaderChain();
        }
    }
```

#### 问题1：为什么要传父类的ClassLoader，有什么用？

> PathClassLoader 构造函数

```java
public PathClassLoader(String dexPath, String librarySearchPath, ClassLoader parent) {
    super(dexPath, null, librarySearchPath, parent);
}
```

从PathClassLoader的注释（自己看下PathClassLoader源码的注释）可以知道 PathClassLoader 是用于加载系统和应用内部类的。

#### 问题2：为什么 PathClassLoader 是用于加载系统和应用内部的？有什么依据？
DexClassLoader的构造函数

```java
public DexClassLoader(String dexPath, String optimizedDirectory,
            String librarySearchPath, ClassLoader parent) {
    // 注意 API26 开始optimizedDirectory设置为空，API26之前是new File(optimizedDirectory)
    super(dexPath, null, librarySearchPath, parent);
}
```

从 DexClassLoader 的注释(自己看下DexClassLoader源码的注释）可以知道，DexClassLoader可以加载从指定路径（包括Sd卡）加载 apk、jar、dex 文件，实现动态加载功能，所以插件化类的加载就是通过DexClassLoader 实现。

> 我们来看下类加载的过程：

###### ClassLoader

```java
protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
            // 首先检查类是否已经加载过（可以防止重复加载，提高效率）
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                try {
                    // 未加载过，则优先从父类的ClassLoader加载
                    if (parent != null) {
                        c = parent.loadClass(name, false);
                    } else {
                        // 在从根ClassLoader加载，android中返回空
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }

                if (c == null) {
                    // If still not found, then invoke findClass in order
                    // to find the class.
                   //父类加载失败，则尝试调用自身的findClass方法加载
                    c = findClass(name);
                }
            }
            return c;
    }
```

通过上面类加载的过程可以知道类的加载优先使用父类的 ClassLoader 进行加载，如果父类加载失败，才通过自身去加载，这个过程即使有个术语，叫双亲委派。为什么要这样做呢？主要是为了防止重复加载，提高效率。（这里回答了问题1）

### 3.2、资源加载

Android 中四大组件获取资源一般都是通过 `getResources()` 得到 `Resources` 对象，通过Resources 对象来获取各种资源（文本、字体、颜色等），而 `Resources` 中获取各种资源实际上都是通过`AssetManager` 来实现的。我们来看下 getString 的代码实现过程：

###### Resources.java

```java
public String getString(@StringRes int id) throws NotFoundException {
    return getText(id).toString();
}
public CharSequence getText(@StringRes int id) throws NotFoundException {
    CharSequence res = mResourcesImpl.getAssets().getResourceText(id);
    if (res != null) {
        return res;
    }
    throw new NotFoundException("String resource ID #0x"
            + Integer.toHexString(id));
}
```

通过上面的代码知道 Resources 的实现类是 ResourceImpl 类，getAssets()返回的是 AssetManager，所以也就证实了资源的加载实际是通过 AssetManager 来加载的。

### 3.3、android 四大组件加载

上面讲述了类和资源的加载原理，由于 Android 中的四大组件均有相应的生命周期都是由系统管理，所以如果单纯的只是通过类加载器来加载一个组件，是无法实现生命周期相关的功能。

##### 要怎么实现插件中的组件也具有相应的生命周期呢？

下面我们以 Activity 为实例来讲解。

首先先要知道什么时候、如何加载 Activity 并创建 Activity 实例，并且什么时候创建 Resources 对象、如何将 Resources 与 Activity 建立关系的。我们通过 Activity 的创建过程来一步一步来揭开谜底。

###### ActivityThread.java

```java
//启动Activity
private Activity performLaunchActivity(ActivityClientRecord r, Intent customIntent) {
        //...省略
       // 生成Context的实现类
        ContextImpl appContext = createBaseContextForActivity(r);
        Activity activity = null;
        try {
            java.lang.ClassLoader cl = appContext.getClassLoader();
            activity = mInstrumentation.newActivity(
                    cl, component.getClassName(), r.intent);
            //...省略
        }
        //...省略
        activity.attach(appContext, this, getInstrumentation(), r.token,
                        r.ident, app, r.intent, r.activityInfo, title, r.parent,
                        r.embeddedID, r.lastNonConfigurationInstances, config,
                        r.referrer, r.voiceInteractor, window, r.configCallback);
        //...省略
    }
```

###### Instrumentation.java

```java
public Activity newActivity(ClassLoader cl, String className,
            Intent intent)
            throws InstantiationException, IllegalAccessException,
            ClassNotFoundException {
        return (Activity)cl.loadClass(className).newInstance();
}

// ContextImpl.java类加载器
@Override
public ClassLoader getClassLoader() {
        return mClassLoader != null ? mClassLoader : (mPackageInfo != null ?       mPackageInfo.getClassLoader() : ClassLoader.getSystemClassLoader());
}
```

###### ClassLoader.java

```java
public static ClassLoader getSystemClassLoader() {
        return SystemClassLoader.loader;
}

static private class SystemClassLoader {
        public static ClassLoader loader = ClassLoader.createSystemClassLoader();
} 

private static ClassLoader createSystemClassLoader() {
        String classPath = System.getProperty("java.class.path", ".");
        String librarySearchPath = System.getProperty("java.library.path", "");
        return new PathClassLoader(classPath, librarySearchPath, BootClassLoader.getInstance());
}
```

###### 通过上面的代码我们知道:

- Context的实现类是ContextImpl类
- Activity 实例是在 Instrumentation 中的 newActivity 中通过 ClassLoader 的实现类加载创建的。
- 加载 Activity 使用的 ClassLoader 是 PathClassLoader。(回答了问题2)

#### 问题3：资源对象是什么时候创建的？
#### 问题4：如何与 Activity 建立联系的呢？

我们先看下Activity中getResouces()的代码实现：

###### Activity.java

```java
    @Override
    public Resources getResources() {
        return getResourcesInternal();
    }

    private Resources getResourcesInternal() {
        if (mResources == null) {
            if (mOverrideConfiguration == null) {
                mResources = super.getResources();
            } else {
                final Context resContext = createConfigurationContext(mOverrideConfiguration);
                mResources = resContext.getResources();
            }
        }
        return mResources;
    }
```

通过 `getResouces()` 方法知道，Activity 中 Resources 对象是通过 `Context` 获取的，而上面Activity 的创建过程中 `Context` 是通过 Activity 的 `attach` 方法进行绑定的（回答了问题4）。
既然知道了 Reources 是通过 Context 的获取的，那么我们看下 Context 实现类 ContextImpl 中Resources的创建过程：

###### ActivityThread.java

```java
private ContextImpl createBaseContextForActivity(ActivityClientRecord r) {
  //...省略
  ContextImpl appContext = ContextImpl.createActivityContext(
                this, r.packageInfo, r.activityInfo, r.token, displayId, r.overrideConfig);
  //...省略
}
```

###### ContextImpl.java

```java
static ContextImpl createActivityContext(ActivityThread mainThread,
            LoadedApk packageInfo, ActivityInfo activityInfo, IBinder activityToken, int displayId,
            Configuration overrideConfiguration) {
      //...省略
      //创建ContextImpl实例
      ContextImpl context = new ContextImpl(null, mainThread, packageInfo, activityInfo.splitName,
                activityToken, null, 0, classLoader);
      //...省略
      // 创建ResourcesManager 对象
      final ResourcesManager resourcesManager = ResourcesManager.getInstance();

        // Create the base resources for which all configuration contexts for this Activity
        // will be rebased upon.
        //通过ResourcesManager 对象生成Resources对象并赋值给Context中的Resources
        context.setResources(resourcesManager.createBaseActivityResources(activityToken,
                packageInfo.getResDir(),
                splitDirs,
                packageInfo.getOverlayDirs(),
                packageInfo.getApplicationInfo().sharedLibraryFiles,
                displayId,
                overrideConfiguration,
                compatInfo,
                classLoader));
      //...省略
}
```

###### ResourcesManager.java

```java
public @Nullable Resources createBaseActivityResources(@NonNull IBinder activityToken,
            @Nullable String resDir,
            @Nullable String[] splitResDirs,
            @Nullable String[] overlayDirs,
            @Nullable String[] libDirs,
            int displayId,
            @Nullable Configuration overrideConfig,
            @NonNull CompatibilityInfo compatInfo,
            @Nullable ClassLoader classLoader) {
       //...省略
      //获取或者创建Resources对象
      return getOrCreateResources(activityToken, key, classLoader);
       //...省略
}

private @Nullable Resources getOrCreateResources(@Nullable IBinder activityToken,
            @NonNull ResourcesKey key, @NonNull ClassLoader classLoader) {
      //...省略
      ResourcesImpl resourcesImpl = createResourcesImpl(key);
      //...省略
}

private @Nullable ResourcesImpl createResourcesImpl(@NonNull ResourcesKey key) {
        final DisplayAdjustments daj = new DisplayAdjustments(key.mOverrideConfiguration);
        daj.setCompatibilityInfo(key.mCompatInfo);
        // 创建AssetManager对象
        final AssetManager assets = createAssetManager(key);
        if (assets == null) {
            return null;
        }

        final DisplayMetrics dm = getDisplayMetrics(key.mDisplayId, daj);
        final Configuration config = generateConfig(key, dm);
        //创建Resources实现类对象
        final ResourcesImpl impl = new ResourcesImpl(assets, dm, config, daj);

        if (DEBUG) {
            Slog.d(TAG, "- creating impl=" + impl + " with key: " + key);
        }
        return impl;
}

@VisibleForTesting
protected @Nullable AssetManager createAssetManager(@NonNull final ResourcesKey key) {
        AssetManager assets = new AssetManager();

        // resDir can be null if the 'android' package is creating a new Resources object.
        // This is fine, since each AssetManager automatically loads the 'android' package
        // already.
        if (key.mResDir != null) {
            //添加资源文件目录
            if (assets.addAssetPath(key.mResDir) == 0) {
                Log.e(TAG, "failed to add asset path " + key.mResDir);
                return null;
            }
       //...省略
}
```

通过上面的代码，我们知道 Activity 中的 Resouces 对象是在生成 ContextImpl 时创建的，而且是通过Resources的资源加载是通过AssetManager实现的，而资源文件目录是通过AssetManager的addAssetPath来实现的。（回答了问题3）

结合上面的代码分析，知道了 Activity 是什么时候、在哪里、如何创建的；也知道了 Activity 中资源是怎么创建和建立关系的，那有什么方案可以解决插件中 Activity 的生命周期的问题呢？

###### 目前市面主要有两个方案：通过 `代理` 或通过 `hook`。

#### 问题5：什么是hook?

### 四、代理

#### 问题6：代理的思想是什么或者如何实现插件Activity的生命周期？

**代理的思想：** 是在主工程放一个 ProxyActivity，启动插件的 Activity 时先启动 ProxyActivity，再在ProxyActivity 中创建插件 Activity，并同步生命周期给插件的 Activity（解答了问题6），看下其原理图：

![图1](https://upload-images.jianshu.io/upload_images/2844689-a6c3668fb4fe3fff?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

######  缺点

- 插件中的Activity 必须继承PluginActivity，开发侵入性强。
- 如果想支持 Activity 的 singleTask，singleInstance 等启动模式，需要自己管理 Activity 栈，实现起来很繁琐。
- 插件中需要小心处理Context，容易出错。
- 如果想把之前的模块改造成插件需要很多额外的工作。

### 五、Hook
**Hook** ：使用技术手段在运行时动态的将额外代码依附给现进程，从而实现替换现有处理逻辑或插入额外功能的目的

可以理解为Hook通过代理、反射等机制实现代码的注入，从而实现对原来功能的改写，以达到预想中的效果
（此处回答了问题5）.我们再看下Activity的整体启动流程图：

![图2](https://upload-images.jianshu.io/upload_images/2844689-fe94e447f0e8d630?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

结合Activity创建过程的代码分析和上图的流程中，我们可以通过hook `步骤1` 和 `步骤10` 来实现插件 Activity 的生命周期等相关功能。代理的方式时因为浸入性太强，hook 的方式需要考虑浸入性的问题，其次我们在开发应用的时候，如果 Activity 不再 Manifest中 注册，当正常方式启动 Activity 时就会抛出找不到Activity的错误信息，所以通过 hook 的方式启动插件 Activity 需要解决如下问题：
- a、插件Activity如何绕开Manifest中注册的检测
- b、如何创建Activity实例，并同步生命周期
  
我们通过VirtualApk插件化框架来看其实现方案：

- a、预先在Manifest中注册各种启动模式的Activity占坑，启动时hook第1步，将Intent根据启动模式替换成预先在Manifest占坑的Activity，这样就解决了Manifest中注册的检测
- b、hook第10步，使用插件的ClassLoader反射创建插件Activity，之后Activity的生命周期回调都通知给插件Activity，这样就解决了创建Activity并同步生命周期的问题

#### 5.1、替换系统 Instrumentation
VirtualApk 在初始化时会调用 hookInstrumentationAndHandler()，该方法hook了系统的Instrumentation（该类与Activity启动相关）:

```java
protected void hookInstrumentationAndHandler() {
        try {
            // 获取ActivityThread对象
            ActivityThread activityThread = ActivityThread.currentActivityThread();
            // 获取ActivityThread中的Instrumentation
            Instrumentation baseInstrumentation = activityThread.getInstrumentation();
            // 创建自定义的VAInstrumentation，具有复写父类一些函数且具有代理功能
            final VAInstrumentation instrumentation = createInstrumentation(baseInstrumentation);
            // 反射的机制替换ActivityThread中的Instrumentation
            Reflector.with(activityThread).field("mInstrumentation").set(instrumentation);
            Handler mainHandler = Reflector.with(activityThread).method("getHandler").call();
            Reflector.with(mainHandler).field("mCallback").set(instrumentation);
            this.mInstrumentation = instrumentation;
            Log.d(TAG, "hookInstrumentationAndHandler succeed : " + mInstrumentation);
        } catch (Exception e) {
            Log.w(TAG, e);
        }
    }
```
上面代码，创建自定义的Instrumentation，通过反射替换了ActivityThread中的Instrumentation

#### 5.2、使用自定义统 Instrumentation 启动 Activity

复写 `5.1` 自定义 Instrumentation 的 execStartActivity

```java
@Override
public ActivityResult execStartActivity(Context who, IBinder contextThread, IBinder token, Fragment target, Intent intent, int requestCode, Bundle options) {
        injectIntent(intent);
        return mBase.execStartActivity(who, contextThread, token, target, intent, requestCode, options);
}

protected void injectIntent(Intent intent) {
        // 处理隐身启动，如果匹配到插件Activity,则隐身启动替换为显示启动
        mPluginManager.getComponentsHandler().transformIntentToExplicitAsNeeded(intent);
        // null component is an implicitly intent
        if (intent.getComponent() != null) {
            Log.i(TAG, String.format("execStartActivity[%s : %s]", intent.getComponent().getPackageName(), intent.getComponent().getClassName()));
            // resolve intent with Stub Activity if needed
            //如果是插件Activity,将Intent中的ClassName替换为占坑中的Activity，解决启动时是否
            //在Manifest中注册的校验
            this.mPluginManager.getComponentsHandler().markIntentIfNeeded(intent);
        }
    }

public void markIntentIfNeeded(Intent intent) {
        if (intent.getComponent() == null) {
            return;
        }

        String targetPackageName = intent.getComponent().getPackageName();
        String targetClassName = intent.getComponent().getClassName();
        // search map and return specific launchmode stub activity
        if (!targetPackageName.equals(mContext.getPackageName()) && mPluginManager.getLoadedPlugin(targetPackageName) != null) {
            intent.putExtra(Constants.KEY_IS_PLUGIN, true);
            intent.putExtra(Constants.KEY_TARGET_PACKAGE, targetPackageName);
            intent.putExtra(Constants.KEY_TARGET_ACTIVITY, targetClassName);
            dispatchStubActivity(intent);
        }
    }
```

execStartActivity时，先处理隐身启动，如果匹配到插件Activity则替换为显示启动；接着通过markIntentIfNeeded将待启动的插件Activity替换为预先在Manifest占坑的Activity，并将插件Activity信息保存在Intent中。其中有个dispatchStubActivity函数，会根据Activity的launchMode选择具体启动哪个StubActivity。VirtualAPK为了支持Activity的launchMode在主工程的AndroidManifest中对于每种启动模式的Activity都预埋了多个坑位。

#### 5.3、hook 创建 Activity

上一步欺骗了系统，让系统以为启动的是一个正常的Activity。这一步切换回插件的 Activity，调用VAInstrumentation 的 newActivity:


```java
@Override
public Activity newActivity(ClassLoader cl, String className, Intent intent) throws InstantiationException, IllegalAccessException, ClassNotFoundException {
        try {
            cl.loadClass(className);
            Log.i(TAG, String.format("newActivity[%s]", className));
            
        } catch (ClassNotFoundException e) {
            ComponentName component = PluginUtil.getComponent(intent);
            
            if (component == null) {
                return newActivity(mBase.newActivity(cl, className, intent));
            }
          
            String targetClassName = component.getClassName();
            Log.i(TAG, String.format("newActivity[%s : %s/%s]", className, component.getPackageName(), targetClassName));
            //根据component获取对应的插件
            LoadedPlugin plugin = this.mPluginManager.getLoadedPlugin(component);
            // 插件对象为空时，使用默认的创建方式
            if (plugin == null) {
                // Not found then goto stub activity.
                boolean debuggable = false;
                try {
                    Context context = this.mPluginManager.getHostContext();
                    debuggable = (context.getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0;
                } catch (Throwable ex) {
        
                }
    
                if (debuggable) {
                    throw new ActivityNotFoundException("error intent: " + intent.toURI());
                }
                
                Log.i(TAG, "Not found. starting the stub activity: " + StubActivity.class);
                return newActivity(mBase.newActivity(cl, StubActivity.class.getName(), intent));
            }
            //使用插件的ClassLoader
            Activity activity = mBase.newActivity(plugin.getClassLoader(), targetClassName, intent);
            activity.setIntent(intent);
            
            //设置activity的资源对象
            // for 4.1+
            Reflector.QuietReflector.with(activity).field("mResources").set(plugin.getResources());
            //返回创建的Activity
            return newActivity(activity);
        }

        return newActivity(mBase.newActivity(cl, className, intent));
    }
```

由于Manifest中注册的占坑Activity没有实现类，所以这里会报ClassNotFoundException 异常，在处理异常中取插件Activity的信息，使用插件ClassLoader反射创建插件Activity

#### 5.4、设置 Activity 的资源 Resources 对象

插件 Activity 的构造创建之后，还需要做一些额外的操作方才可以正常运行，比如设置访问资源所使用的Resources对象、Context等：

```java
@TargetApi(Build.VERSION_CODES.LOLLIPOP)
@Override
public void callActivityOnCreate(Activity activity, Bundle icicle, PersistableBundle persistentState) {
        injectActivity(activity);
        mBase.callActivityOnCreate(activity, icicle, persistentState);
}

protected void injectActivity(Activity activity) {
        final Intent intent = activity.getIntent();
        if (PluginUtil.isIntentFromPlugin(intent)) {
            
            Context base = activity.getBaseContext();
            try {
                //根据Intent获取对应的插件对象
                LoadedPlugin plugin = this.mPluginManager.getLoadedPlugin(intent);
                //反射设置Resources对象为插件Resources
                Reflector.with(base).field("mResources").set(plugin.getResources());
                Reflector reflector = Reflector.with(activity);
                // 反射设置Context为插件的Context, 其实就是主工程的Context
                reflector.field("mBase").set(plugin.createPluginContext(activity.getBaseContext()));
                // 反射设置Application为插件的Application,其实就是主工程的Application
                reflector.field("mApplication").set(plugin.getApplication());
                
                //设置横竖屏
                // set screenOrientation
                ActivityInfo activityInfo = plugin.getActivityInfo(PluginUtil.getComponent(intent));
                if (activityInfo.screenOrientation != ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED) {
                    activity.setRequestedOrientation(activityInfo.screenOrientation);
                }
                
                //重新设置Intent
                // for native activity
                ComponentName component = PluginUtil.getComponent(intent);
                Intent wrapperIntent = new Intent(intent);
                wrapperIntent.setClassName(component.getPackageName(), component.getClassName());
                activity.setIntent(wrapperIntent);
                
            } catch (Exception e) {
                Log.w(TAG, e);
            }
        }
    }
```

这段代码主要是将 Activity 中的 Resource，Context 等对象替换成了插件的相应对象，保证插件Activity 在调用涉及到 Context 的方法时能够正确运行。

至此便实现了插件 Activity 的启动，且此插件 Activity 中并不需要什么额外的处理，和常规的 Activity一 样。那问题来了，之后的 onResume，onStop 等生命周期怎么办呢？答案是所有和 Activity 相关的生命周期函数，系统都会调用插件中的 Activity。原因在于 AMS 在处理 Activity 时，通过一个 token 表示具体 Activity 对象，而这个 token 正是和启动 Activity 时创建的对象对应的，而这个 Activity 被我们替换成了插件中的 Activity，所以之后 AMS 的所有调用都会传给插件中的Activity。

### 六、其他组件

四大组件中 Activity 的支持是最复杂的，其他组件的实现原理要简单很多，简要概括如下：

- **Service**：Service 和 Activity的差别在于，Activity 的生命周期是由用户交互决定的，而 Service 的生命周期是我们通过代码主动调用的，且Service实例和 manifest 中注册的是一一对应的。实现 Service 插件化的思路是通过在 manifest 中预埋 StubService，hook 系统 startService 等调用替换启动的 Service，之后在 StubService 中创建插件 Service，并手动管理其生命周期。

- **BroadCastReceiver**：解析插件的 manifest，将静态注册的广播转为动态注册。
  
- **ContentProvider**：类似于 Service 的方式，对插件 ContentProvider 的所有调用都会通过一个在manifest 中占坑的 ContentProvider 分发。

## 七、插件间、插件与主程序间的交互

上面解决了插件化的原理，那么**插件与插件之间、插件与主工程之间如何相互调用、相互访问资源**呢?

相互调用对应的是类的调用，而每个类都需要对应的 ClassLoader 来加载，所以一般就分为两种调用机制：

- 单 ClassLoader 机制：将插件中 DexClassLoader 的 pathList 合入主工程的 pathList 中，这样主工程就可以调用插件的类和方法，插件调用另一个插件则需要借助主工程或者插件框架统一访问接口来实现。单 ClassLoader 的弊端就是如果插件使用不同版本的库就会出现问题。

- 多ClassLoader机制：每个插件对应一个 DexClassLoader，那么主工程调用插件的类和方法就需要借助插件的 ClassLoader，一般需要进行插件化框架进行统一管理。

资源的访问也是有两种方式：

- 合入式：将插件的资源路径合入主工程的 AssetManager 中，因此生成的 Resources 可以同时访问插件和主工程的资源，弊端是由于插件和主工程是独立编译的，所有会存在 ***资源id冲突的情况***（解决资源Id冲突需要通过更改编译过程修改资源 Id，资源 id 是由 8 位 16 进制数表示，表示为 0xPPTTNNNN。**PP段**用来区分包空间，默认只区分了应用资源和系统资源，**TT段**为资源类型，NNNN段在同一个APK中从0000递增。其中系统的pp段的值是0x01,应用pp段的值是0x7f;系统和应用的tt段值都是0x04,剩下的NNNN值在0x0000至0xfffff之间）

- 独立式：资源隔离，不存在冲突情况，但是资源共享比较麻烦，需要借助统一接口进行管理，会存在资源在不同插件重复存在的情况。

## 八、几种成熟的插件框架

![图3](https://upload-images.jianshu.io/upload_images/2844689-c4197508009e4438?imageMogr2/auto-orient/strip%7CimageView2/2/w/720/format/webp)

第一代：**dynamic-load-apk** 最早使用 ProxyActivity 这种静态代理技术，由 ProxyActivity 去控制插件中 PluginActivity 的生命周期。该种方式缺点明显，插件中的 activity 必须继承 PluginActivity，开发时要小心处理 context。而 **DroidPlugin** 通过Hook系统服务的方式启动插件中的 Activity，使得开发插件的过程和开发普通的 app 没有什么区别，但是由于 hook 过多系统服务，异常复杂且不够稳定。

第二代：为了同时达到插件开发的低侵入性（像开发普通app一样开发插件）和框架的稳定性，在实现原理上都是趋近于选择尽量少的 hook，并通过在 manifest 中预埋一些组件实现对四大组件的插件化。另外各个框架根据其设计思想都做了不同程度的扩展，其中 **Small** 更是做成了一个跨平台，组件化的开发框架。

第三代：**VirtualApp** 比较厉害，能够完全模拟 app 的运行环境，能够实现 app 的免安装运行和双开技术。**Atlas** 是阿里今年开源出来的一个结合组件化和热修复技术的一个 app 基础框架，其广泛的应用与阿里系的各个app，其号称是一个容器化框架。

## 九、参考

*[深入理解Android插件化技术](https://zhuanlan.zhihu.com/p/33017826)*

作者：jxiang112  
链接：https://www.jianshu.com/p/7e4958d02094  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。