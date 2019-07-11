# Android 之不要滥用 SharedPreference

作者：godliness  
链接：https://www.jianshu.com/p/8eb2147c328b/  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。   




> 本文不是与大家一起探讨SharedPreference的基本使用，而是结合源码的角度揭秘对SharedPreference使用不当引发的严重后果以及该如何正确使用。

SharedPreferences是Android平台上一个轻量级的存储辅助类，用来保存应用的一些常用配置，它提供了 `string，set，int，long，float，boolean` 六种数据类型。最终数据是以xml形式进行存储。在应用中通常做一些简单数据的持久化缓存。SharedPreferences 作为一个轻量级存储，所以就限制了它的使用场景，如果对它使用不当将会带来严重的后果。

## 一、从源码的角度出发
### 1、SharedPreferences 的创建过程
> 后面统一简称：Sp

通过 Context 的 getSharedPreferences 方法得到 Sp 对象。
```java
SharedPreferences sp = getSharedPreferences("cache", MODE_PRIVATE)
```

这里实际调用了 ContextImpl 的 getSharedPreferences()。
```java
@Override
    public SharedPreferences getSharedPreferences(String name, int mode) {
        // At least one application in the world actually passes in a null
        // name.  This happened to work because when we generated the file name
        // we would stringify it to "null.xml".  Nice.
        if (mPackageInfo.getApplicationInfo().targetSdkVersion <
                Build.VERSION_CODES.KITKAT) {
            if (name == null) {
                name = "null";
            }
        }

        File file;
        synchronized (ContextImpl.class) {
            if (mSharedPrefsPaths == null) {
                mSharedPrefsPaths = new ArrayMap<>();
            }
            file = mSharedPrefsPaths.get(name);
            if (file == null) {
                file = getSharedPreferencesPath(name);
                mSharedPrefsPaths.put(name, file);
            }
        }
        return getSharedPreferences(file, mode);
    }
```

从源码可以看到：首先在sSharedPrefs中获取Sp对象，那这个sSharedPrefs是个什么东西？

```java
    /**
     * Map from package name, to preference name, to cached preferences.
     */
    @GuardedBy("ContextImpl.class")
    private static ArrayMap<String, ArrayMap<File, SharedPreferencesImpl>> sSharedPrefsCache;

    /**
     * Map from preference name to generated path.
     */
    @GuardedBy("ContextImpl.class")
    private ArrayMap<String, File> mSharedPrefsPaths;
```
sSharedPrefs 实际是个 Map 对象，并且被声明为 static final，这就意味着我们整个应用中只存在一个 sSharedPrefs 对象。如果第一次创建Sp对象此时肯定是获取到的是null，紧接着进入第一个if语句getSharedPrefsFile(name)，参数想必大家都猜的到：就是我们创建Sp时传的的name，其实通过名字也可以看得出根据传递name创建一个File：

```java
    @Override
    public File getSharedPreferencesPath(String name) {
        return makeFilename(getPreferencesDir(), name + ".xml");
    }
```
创建name.xml文件。
```java
    private File makeFilename(File base, String name) {
        if (name.indexOf(File.separatorChar) < 0) {
            return new File(base, name);
        }
        throw new IllegalArgumentException(
                "File " + name + " contains a path separator");
    }
```
跟踪到这里储存文件的创建我们就找到了。

紧接着new SharedPreferencesImpl()，看下SharedPreferencesImpl的构造方法：


实际上SharedPreferences只是个接口，而真正的实现是SharedPreferencesImpl，我们后续的get，put操作实际也是通过SharedPreferencesImpl对象完成的。

构造方法最后一行：startLoadFromDisk()：


从这里可以看出首先将mLoaded变量赋值为false，起到一个状态的变化作用，在后续我们会说到这个mLoaded变量很重要（其实主要多线程等待），然后开启一个线程loadFromDiskLocked()：


代码稍微有点长，但是并不复杂。94行 - 105行都是做一些相关的检查。紧接着向下创建BufferedInputStream对象，将mFile作为参数，mFile还记得吗？它就是根据我们传递的name创建的文件。然后通过XmlUtils.readMapXml()将文件内容写入到map中并返回。在123行将mLoaded设置为true，代表已经将文件里的加载完成，存储在一个map中并且将其赋值给成员变量mMap：


说道这想必大家已经明白：我们在Sp储存的数据会在本地生成一个.xml文件外，还会将该文件的数据缓存在一个map对象中。如果是第一次创建显然BufferedInputStream不会读取到任何数据，此时XmlUtils.readMapXml()解析返回自然为null，然后mMap = new HashMap（）；

然后再回到ContextImpl的getSharedPreferences方法最后：


如果Sp已经存在了，会判断mode否等于Context.MODE_MULTI_PROCESS，然后如果API小于11：


没错Context.MODE_MULTI_PROCESS仅仅是重新加载一遍数据到内存mMap，所以指望SharedPreferences实现跨进程通信可以死心了。

说到这，SharedPreference的创建过程就算是讲完了：getSharedPreferences实际返回SharedPrefenercesImpl对象，首先在sSharedPrefs容器中查找，如果未找到则创建Sp的对象并添加到sSharedPrefs。

### 2、put数据

通过上面的分析getSharedPreferences实际创建的是SharedPreferencesImpl对象。


此时edit自然是调用的SharedPreferencesImpl的方法：



还记得我们之前提到的mLoaded变量吗：当我们第一次创建SharedPreferences时候，会将该变量置为false，然后开启线程将文件中的数据完成读取进map之后再将其置为true，读取文件的内容到map是在工作线程，此时edit方法是在主线程，如果此时工作线程读取时间过久，那edit方法将长时间处于等待状态。一旦超过5秒就会发生ANR危险。

调用SharedPreferencesImpl的edit方法返回的是EditorImpl对象：


我们一些列的put操作，还有clear，remove，apply，commit都是在EditorImpl对象中：


从源码可以得知，我们一些列的put和remove之后是将数据添加进入mModifiled中，mModifiled是一个Map对象，其实从名字也可以看出代表为暂存的。clear仅修改mClear状态。执行操作之后必须要执行commit：


这里需要注意的是：我们每次edit都会创建一个新的EditorImpl对象。接着跟踪commit操作：


commitToMemory()：


接下面：


代码篇幅有些长，我们只关注重点部分：for循环这里，上面我们提到一系列的put和remove操作都添加进入mModified中，也就是mModified保留着我们当前的改变，通过遍历该容器，与mMap数据做一个比较，比如相同key但是value发生了变化此时修改mMap中的数据。然后mMap就是最后一次commit的数据。最后清空mModified容器。

方法的最后返回MemoryCommitResult，其实从名字也可以看出它的作用：标记本次提交的状态是否发生改变并将结果返回。

此时又回到commit方法：


调用enqueueDiskWirte：


首先writeToDiskRunnable对象，在该对象的方法中执行写入文件操作（就是将最后一次提交之后mMap的数据写回到文件）。

接着向下：

由于commit方法的第二个参数Runnable传递null，故此时siFromSyncCommit为true，可以看到执行writeToDiskRunnable.run，直接在当前线程（UI线程）执行写入文件操作。此时return。

我们在修改数据之后除了选择commit提交之外，还可以使用apply进行提交：首先writeToDiskRunnable对象，在该对象的方法中执行写入文件操作（就是将最后一次提交之后mMap的数据写回到文件）。

使用apply进行提交：


此时siFromSyncCommit等于false，此时会执行enqueueDiskWrite方法的：


QueuedWork是一个线程池，而且只有一个核心线程，提交的任务到会加入到一个等待队列中按照顺序执行。

那么commit发生在UI线程而apply发生在工作线程。如果保证不阻塞UI线程我们使用apply来提交修改是否就绝对安全了呢？这里先告诉大家答案：绝对不是！！！！，后面会给大家继续分析。

接下来我们先来看下get操作。

### 3、get数据

我们看get操作做了哪些：


也就是SharedPreferencesImpl的get操作：


其实通过上面的分析我们已经得到答案：通过SharedPreferenceImpl存储的数据都会在内存中保留一份mMap，这里也是直接在mMap中读取数据即可。

这里要着重说下awaitLoadedLocked方法，之前我们也提到过该方法主要是检查mLoaded变量状态：当我们第一次创建Sp对象时，它会开启一个工作线程将指定的文件中内容加载到mMap中，当加载完成改变mLoaed变量状态；否则awaitLoadedLocked方法会一直等待下去。这里涉及到一个优化点我们后续给大家总结。

## 二、apply一定安全吗？

上面我们提到过确认提交数据除了commit还可以apply，apply使写入文件操作发生在工作线程中，这样防止IO操作阻塞UI线程；这样真的就绝对安全吗？答案不是的。

我们要去跟踪另外一部分源码：

首先Android四大组件的创建以及生命周期调用都是进程间通信完成的，到我们自己的进程中完成调度过渡任务的是ActivityThread，ActivityThread是我们应用进程的入口。来看下Actvity的onStop回调过程：

ActivityThread.java：


你没有看错又要等待，等待什么呢？

还记得我们确认提交数据使用apply操作将写入文件操作添加进线程池队列中吗？sPendingWorkFinishers就是SharedPreferencesImpl的enqueueDiskWirte方法的最后一行，当我们使用apply时就会执行如下添加到线程池中任务队列：


QueuedWork.java：


假设我们apply非常多的任务。该线程池队列是串行执行，当我们关闭Activity时：会检查sPendingWorkFinishers队列中任务是否已经全部执行完成，否则一直等到全部执行完成。如果此时等待超过5s


由此得知apply也不是绝对安全的，试想当你apply提交较多的任务并且都是大型key或value时。


## 三、结论

当我们首次创建 SharedPreferences 对象时，会根据文件名将文件下内容一次性加载到 mMap 容器中，每当我们 edit 都会创建一个新的 EditorImpl 对象，当修改或者添加数据时会将数据添加到 mModifiled 容器中，然后 commit 或者 apply 操作比较 mMap 与 mModifiled 数据修正 mMap 中最后一次提交数据然后写入到文件中。而 get 直接从 mMap 中读取。试想如果此时你存储了一些大型 key 或者 value 它们会一直存储在内存中得不到释放。

## 四、正确使用的建议

1. 不要存放大的 key 和 value 在 SharedPreferences 中，否则会一直存储在内存中得不到释放，内存使用过高会频发引发GC，导致界面丢帧甚至ANR。

2. 不相关的配置选项最好不要放在一起，单个文件越大读取速度则越慢。

3. 读取频繁的key和不频繁的key尽量不要放在一起（如果整个文件本身就较小则忽略，为了这点性能添加维护得不偿失）。

4. 不要每次都 edit，因为每次都会创建一个新的 EditorImpl 对象，最好是批量处理统一提交。否则 edit().commi 每次创建一个 EditorImpl 对象并且进行一次 IO 操作，严重影响性能。

5. commit 发生在 UI 线程中，apply 发生在工作线程中，对于数据的提交最好是批量操作统一提交。虽然 apply 发生在工作线程（不会因为IO阻塞UI线程）但是如果添加任务较多也有可能带来其他严重后果（参照 ActivityThread 源码中 handleStopActivity 方法实现）。

6. 尽量不要存放 json 和 html，这种可以直接文件缓存。

7. **不要指望这货能够跨进程通信** Context.PROCESS 。

8. **最好提前初始化** SharedPreferences，避免 SharedPreferences 第一次创建时读取文件线程未结束而出现等待情况。

荐：http://www.cnblogs.com/mingfeng002/p/5970221.html