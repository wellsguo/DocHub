# [Android -- Fragment 基本用法、生命周期与细节注意](https://www.jianshu.com/p/1ff18ec1fb6b?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)

## 引言
这篇文章，大概分析下 Fragment 的生命周期、实际应用方法以及使用Fragment时需要注意的地方，算是Fragment的入门级文章，理解透Fragment生命周期和一些细节，就容易理解Fragment如何与外界通信等问题了。至于对其的源码分析等更加深入的内容，本文涉及不多。  

Fragment的写法就不多说了，一般是继承Fragment，然后重写onCreateView方法去与View布局进行绑定。


## 使用前提
FragmentActivity。使用Fragment，**需要 Activity 继承自FragmentActivity**，并且，为了兼容到 Android3.0 以前的版本，需要使用v4兼容包下的FragmentActivity。

## 用法说明

### I 常见的两种加载方式

#### (1) FragmentManager

> 直接获取 FragmentManager 并使用 FragmentManager 管理下的 FragmentTranscation 来进行 Fragment 或者 Fragment 列表的加载、替换、删除等操作，此时的 Fragment 所在的容器一般选择用 FrameLayout。

  - **FragmentManager**  
    Activity中有个FragmentManager，其内部维护fragment队列，以及fragment事务的回退栈。在Fragment被创建、并由FragmentManager管理时，FragmentManager就把它放入自己维护的fragment队列中。
  
  - **FragmentTransaction**  
    知道了FragmentManger可以管理和维护Fragment，那么FragmentManager是直接去绑定Fragment然后把它set进自己的队列中吗？不是的，而是用FragmentTransaction（Fragment事务），FragmentManager调用beginTransaction()方法返回一个新建的事务，用于记录对于Fragment的add、replace等操作，最终将事务commit回FragmentManager，才开始启动执行事务的内容，实现真正的Fragment显示。

#### (2) ViewPager
  
> 使用 ViewPager 等容器去装载 Fragment 列表并通过他们自己的页面切换能力去切换 Fragment。

  - **FragmentPagerAdapter**  
    对于不再需要的 fragment，选择调用 detach 方法，仅销毁视图，并不会销毁 fragment 实例。

  - **FragmentStatePagerAdapter**  
    会销毁不再需要的 fragment，当当前事务提交以后，会彻底的将 fragment 从当前 Activity 的 FragmentManager 中移除，state 标明，销毁时，会将其 onSaveInstanceState(Bundle outState) 中的 bundle 信息保存下来，当用户切换回来，可以通过该 bundle 恢复生成新的 fragment，也就是说，你可以在 onSaveInstanceState(Bundle outState) 方法中保存一些数据，在 onCreate 中进行恢复创建。

  - **建议**  
    使用 FragmentStatePagerAdapter 当然更省内存，但是销毁新建也是需要时间的。一般情况下，如果你是制作主页面，就3、4个Tab，那么可以选择使用 FragmentPagerAdapter，如果你是用于 ViewPager 展示数量特别多的条目时，那么建议使用 FragmentStatePagerAdapter。

   > ViewPager 管理 Fragment 的原理其实也是 FragmentManager 和 FragmentTransaction，看源码就知道.



### II 关键代码

- FragmentManager

  - activity layout布局
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
        …………
        <Button
            ……………………
        />
        …………
    <FrameLayout
        android:id="@+id/frame_root_fragment"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        />
</LinearLayout>
```

  -  Activity的初始化方法
```java
@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_fragment);
    fragmentA = new MyFragmentA();
    getSupportFragmentManager().beginTransaction().add(R.id.frame_root_fragment,fragmentA).commit();
}
```

- ViewPager
  - activity layout布局
```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        xmlns:app="http://schemas.android.com/apk/res-auto"
        android:orientation="vertical" android:layout_width="match_parent"
        android:layout_height="match_parent">
    <android.support.design.widget.TabLayout
        ……
    />
    <android.support.v4.view.ViewPager
        android:id="@+id/vp_main"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
    />
</LinearLayout>
```
  - 初始化方法
```java
///在onCreate()中调用此方法
private void initView() {
    ///使用LinkedHashMap等方式方便我们管理Fragments
    fragmentMap = new LinkedHashMap<>();
    ///控件初始化
    mTabLayout = (TabLayout) findViewById(R.id.tl_main);
    mViewPager = (ViewPager) findViewById(R.id.vp_main);
    …………
    mPagerAdapter = new FragmentPagerAdapter(getSupportFragmentManager()) {
        @Override
        public Fragment getItem(int position) {
            switch (position) {
                case 0:///Fragment一
                default:
                    if(!fragmentMap.containsKey(titles[0]))
                        fragmentMap.put(titles[0],new DogFragment());
                    return fragmentMap.get(titles[0]);
                case 1:///Fragment二
                    if(!fragmentMap.containsKey(titles[1]))
                        fragmentMap.put(titles[1],new CatFragment());
                    return fragmentMap.get(titles[1]);
            }
        }

        …………
    };
    mViewPager.setAdapter(mPagerAdapter);
    mTabLayout.setupWithViewPager(mViewPager);
}
```

### III 图解 Fragment 的生命周期



![Fragment与宿主Activity的声明周期方法调用顺序](https://upload-images.jianshu.io/upload_images/2369895-d5f0fd063b03482a.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/874/format/webp)

![Fragment生命周期](https://upload-images.jianshu.io/upload_images/2369895-ca76ae83a6bc6912.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/968/format/webp)

#### 图解说明：

- 从图解可以看到，Fragment的一些生命周期方法与Activity比较相似，毕竟Fragment表示“碎片、块”的含义，本身实现出来一个主要目的就是帮Activity分担UI代码部分的实现逻辑的。  

- 蓝色背景的生命周期方法：从 onCreateView() 到onDestroyView()，在整个Fragment创建到被销毁的过程中可以被执行**一次或多次**，这里就涉及到管理着Fragment事务（FragmentTransaction）的FragmentManager底层的后台记录栈的东西了。

- 绿色背景的生命周期方法：在整个Fragment的生命周期中，**仅仅执行一次**。

- 对图解的补充：这里用几个例子具体看清Fragment的周期方法的调用次序，更好地理解Fragment的生命周期：  
  - 首先，可以看看 另一篇博文[查漏补缺（二）：易忘难懂](https://www.jianshu.com/p/c0a4fa16b8d6)中的第10点：Fragment 与 它所在的Activity的生命周期方法执行次序 ，它说明了在 ViewPager 适配 Fragment 列表这种方式下 Fragment 方法执行次序。
  - 这里再加上<u>直接在frameLayout上添加、替换Fragment</u>的情况，进一步分析Fragment生命周期：
    - 执行如下代码，来加载Fragment时
      ```java
      fragmentA = new MyFragmentA()
      getSupportFragmentManager().beginTransaction()
                 .add(R.id.frame_root_fragment,fragmentA);///执行代码①
      //getSupportFragmentManager().beginTransaction()
      //.add(R.id.frame_root_fragment,fragmentA).commit();//执行代码②
      ```
    【执行代码①】  
      ![](http://upload-images.jianshu.io/upload_images/2369895-cdbb4fc1f84cda21.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  
    【执行代码②】  
      ![](http://upload-images.jianshu.io/upload_images/2369895-328ad7dcd62a4313.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)   
    - 退出Activity操作时  
    ![](http://upload-images.jianshu.io/upload_images/2369895-1f80187dba162619.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  
    - Fragment中点击按钮执行startActivityForResult()方法时  
    ![](http://upload-images.jianshu.io/upload_images/2369895-63ca7a20cd072a89.gif?imageMogr2/auto-orient/strip)  
    - 执行 **`Fragment.startActivityForResult()`** Log截图：  
    ![](http://upload-images.jianshu.io/upload_images/2369895-4ddaa474719174e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)  
    - 执行 **`getActivity().startActivityForResult()`** Log截图：  
    ![](http://upload-images.jianshu.io/upload_images/2369895-42fc8eb5d94b2464.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

* 由上可得到</u>***总结***</u>：
  * new 一个Fragment，Fragment只是调用了自身的空参数构造方法，并没有其他操作。
  
  * Fragment要执行其onAttach()及其之后的生命周期方法，需要被FragmentTransition记录并真正提交到FragmentManager处，才能实现。
  
  * 如果Fragment要准备显示了（即被事务提交到FragmentManager，具体后面会说到），那么它再继续执行onCreateView()到onResume()的方法，去创建和绑定UI，最后在前台显示。
  
  * 由于ViewPager在Activity.onCreate()中并没有真正初始化界面完成，即在onCreate()阶段中，ViewPager适配器内部并没有真的调用Fragment的构造方法并从FragmentManager中获取FragmentTransaction事务来记录Fragment的操作，等到Activity.onResume()方法被执行（即Activity启动完成并在前台显示了），这时，ViewPager才选取默认要显示的那一页，并对应执行这一页的Fragment的创建+事务添加+提交给Manager的一个过程。
  
  * 在Activity被停止或即将被销毁的过程中，都首先停止或销毁它内部的所有Fragment，而它内部的所有Fragment则各自检查自己是否有置于前台或显示，如果有，那就得destroyView()销毁掉它所绑定的View布局并使自己处于完全不可见状态，再判断地执行onDestroy()。

  * 对于最后一个例子，Fragment执行自身的startActivityForResult()和getActivity().startActivityForResult()是有区别的：如果执行自身的startActivityForResult()，那么在另一个Activity返回时，Fragment就会执行自身的onActivityResult()方法，否则，只会触发Activity的onActivityResult()，除非你在Activity的onActivityResult()方法中添加几行代码，让它把结果也返回给指定Fragment，如：
```java
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
    if (fragmentA!=null)
        fragmentA.onActivityResult(requestCode,resultCode,data);
    
    if (fragmentB!=null)
        fragmentB.onActivityResult(requestCode,resultCode,data);
}
```

## Fragment 开发遇到的问题和解决（Fragment注意点）


### I Fragment 与 后台事务栈管理
前面说了Fragment的几个生命周期方法可能不止执行一次，关键点就在于Fragment是否被事务管理到后台栈中，这里就涉及到与Fragment有关的几个类的相关方法：

- FragmentTransaction.addToBackStack(String)  
  关键：让携带着Fragment记录的事务保存到后台栈中

- FragmentActivity.onBackPressed()  
  点击BACK按键或者其他方式触发Activity的回退方法时，会促发此方法，FragmentActivity的此方法中会多加一个判断，看后台栈中是否存在事务，存在，则一个事务出栈，这个事务对应的Fragment操作记录则被回退清空，也就是这个事务下Fragment的操作，全部撤销，Fragment会从FragmentManager维护的Fragment队列中拿出并被销毁从而执行它的生命周期的余下方法

- FragmentManager.popBackStack()  
  Manager管理的后台栈的一个出栈操作，返回一个FragmentTransaction事务，但是此操作要等到Application返回它是事件loop时才会触发

- FragmentManager.popBackStackImmediate()  
  与popBackStack()方法差不多，只是它是立即执行出栈操作，而不用顾忌Application


下面举个例子，给大家看看Fragment是怎么跑的：

这里使用FragmentTransaction.replace()作为主要Fragment操作

原因：
- add()方法与replace()方法大多数情况下效果是一样的，add是指“添加”，replace是指“替换”，一般使用同一个FrameLayout去加载Fragment时，推荐是用replace()的，省去add的多层Fragment重叠，当然，在需要进行轮播等需要及时看到多个Fragment的时候，add()比较好的。

- remove()、hide()、show()、detach()、attach()等方法，都相应地只是执行对应Fragment的对应生命周期方法而已

所以这里用replace()做演示更好。

主要执行的代码：
```java
/***
 * 方式一：单个Fragment 做下记录到backStack
 *
 * @param baseFragment
 */
public void onAddFragment(Fragment baseFragment) {
    FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
    ft.replace(R.id.frame_root_fragment, baseFragment, "tag");
    ft.addToBackStack("tag");
    ft.commit();
}

/**
 * 方式二：多个Fragment同时addToBackStack
 *
 * @param fragmentList
 */
public void onAddFragments(Fragment[] fragmentList) {
    FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
    int pos = 0;
    for (Fragment item : fragmentList) {
        pos += 1;
        ft.replace(R.id.frame_root_fragment, item, "tag" + pos);
        ft.addToBackStack("tag" + pos);
    }
    ft.commit();
}
```
gif图：  

执行方式一代码（事务一对一Fragment）  

![](https://upload-images.jianshu.io/upload_images/2369895-bf0487741d248852.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/335/format/webp)

Log截图：  
![](https://upload-images.jianshu.io/upload_images/2369895-8ef4138085a66394.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/944/format/webp)


执行方式二代码（事务一对多Fragments）   
![](https://upload-images.jianshu.io/upload_images/2369895-c0ddade6d5a6eb05.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/335/format/webp)

Log截图：  
![](https://upload-images.jianshu.io/upload_images/2369895-7b90cf2ca17c009d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/949/format/webp)


得出结论：  

- 从代码可以看到，FragmentTransaction可以记录一到多个Fragment的相关操作。
- 示例可以知道，FragmentActivity回退事件发生时，会先把所有的FragmentTransaction事务一一弹出后台栈先。【如果一个事务对应一个Fragment，那么这里就实现了一个Fragment之间的跳转过程；而如果一个事务对应多个Fragment，那么，一个事务弹出，它涉及到的后台队列中Fragment集合便会一下子都弹出销毁，而不是一个个Fragment地出队】

### II Fragment 及其宿主 Activity 的复用
在平时开发中，怎么样方便开发、方便维护、尽量解耦，就怎么写代码，这里给一个比较好的Fragment写法例子（参考鸿洋博客中的一个Fragment例子），供参考：
```java
public class ContentFragment extends Fragment  
{  
    private String mArgument;///Activity传递的数据（值）
    public static final String ARGUMENT = "argument";///Activity传递的数据名（键）  
    public static final String RESPONSE = "response";///Activity

    @Override  
    public void onCreate(Bundle savedInstanceState)  
    {  
        super.onCreate(savedInstanceState);  
        Bundle bundle = getArguments();  
        if (bundle != null)  
        {  
            mArgument = bundle.getString(ARGUMENT);  
            Intent intent = new Intent();  
            intent.putExtra(RESPONSE, "good");  
            getActivity().setResult(ListTitleFragment.REQUEST_DETAIL, intent);  
        }  

    }  
    ////在实例化时获取Activity传入的值（这里示例为String类型）
    public static ContentFragment newInstance(String argument)  
    {  
        Bundle bundle = new Bundle();  
        bundle.putString(ARGUMENT, argument);  
        ContentFragment contentFragment = new ContentFragment();  
        contentFragment.setArguments(bundle);  
        return contentFragment;  
    }  

    @Override  
    public View onCreateView(LayoutInflater inflater, ViewGroup container,  
            Bundle savedInstanceState)  
    {  
        Random random = new Random();  
        TextView tv = new TextView(getActivity());  
        ///.........
        return tv;  
    }  
}  
```
其实写法不一，可能有很多更加灵活的写法，但本文不深究，只要大家有“Fragment的复用”这个思想，旨在写出容易复用、与Activity耦合度小、存在与外界通信接口的Fragment，就能够实际减少工作量、理清思路。

下面是一个抽象Activity，用于简单状态Fragment 的Activity自身代码的复用，可参考：
```java
public abstract class SingleFragmentActivity extends FragmentActivity  {  
  protected abstract Fragment createFragment();  
  @Override  
  protected void onCreate(Bundle savedInstanceState) {  
      super.onCreate(savedInstanceState);  
      setContentView(R.layout.activity_single_fragment);  
      FragmentManager fm = getSupportFragmentManager();  
      Fragment fragment =fm.findFragmentById(R.id.id_fragment_container);  
      if(fragment == null )  
      {  
          fragment = createFragment() ;  
          fm.beginTransaction().add(R.id.id_fragment_container,fragment).commit();  
      }  
  }  
}  
```
### III 关于 DialogFragment
Android 3.0 被引入的一类特殊 Fragment，方便我们构建具有和 Fragment 一样生命周期的一类 Dialog 等组件，从而解决普通的 Dialog 等组件难以管理它的生命周期、与 Activity、Fragment 交互的限制。详细可参考 [Android 官方推荐 : DialogFragment 创建对话框](https://link.jianshu.com/?t=http://blog.csdn.net/lmj623565791/article/details/37815413)

#### IV Fragment 与外界的通信
理解了 Fragment 生命周期和它的基本写法，那么，再说说 Fragment 与外界的通信。上面提到的 DialogFragment 就是用于优化通信和管理的，那么，平常我们使用 Fragment，应该如何保证与其他 Fragment 和外部 Activity 进行通信呢？

##### Fragment 与其宿主 Activity 间的通信
* Activity 传给 Fragment  
  Activity 通过 `Fragment.setArguments(Bundle)` 在创建 Fragment 时传递数据给 Fragment，在 Fragment 的 onCreate() 中，Fragment 通过 `getArguments()` 获取 Bundle 数据。
* Activity传给Fragment  
  Activity 通过 `getSupportFragmentManager().findFragmentById()` 或 `getSupportFragmentManager().findFragmentByTag()` 获取 Fragment 并调用 Fragment 自己定义的方法，数据通过参数形式传给 Fragment。
* Fragment 传给 Activity  
  Fragment 通过 `getActivity()` 方式获取宿主 Activity，就可以调用 Activity 的方法【但是这样不严谨，Fragment 能够调用的方法，应该要受到限定，所以，使用如下代码的方式，通过在 Fragment 中定义一个接口，然后让宿主 Activity 实现这些方法】
```java
public static class FragmentA extends ListFragment{
    OnArticleSelectedListener mListener;
    ...
    @Override
    public void onAttach(Activity activity){
        super.onAttach(activity);
        try{
            mListener = (OnArticleSelectedListener)activity;
        }catch(ClassCastException e){
            throw new ClassCastException(activity.toString()+"must implement OnArticleSelectedListener");
        }
    }
}
```

* Activity 传给 Fragment、Fragment 传 Fragment  
  还可以通过广播的方式，让 Fragment 去注册广播，然后，Fragment 调用 `getActivity().sendBroadcast(Intent)` 或者 Activity 调用 `sendBroadcast(Intent)` 来发出广播，让注册了该广播的 Fragment 去接收并过滤广播信息【然而这样做有些小题大做，而且需考虑广播的注册等】 
*<u>关键代码</u>*：  
```java
public class FragmentA extends Fragment{
    MyBroadcast broadcast;
    //.........
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        //........
        IntentFilter filter = new IntentFilter();
        try {
            if (mReceiver != null) {
                getActivity().unregisterReceiver(broadcast);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        broadcast = new MyBroadcast();
        filter.addAction(PageOneFragment.DATA_CHANGED);
        getActivity().registerReceiver(broadcast, filter);

        //........
    }
    
    //..................
    
    class MyBroadcast extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (intent.getAction().equals(PageOneFragment.DATA_CHANGED)) {
            ///。。。。。
            }
        }
    }
}
```

##### Fragment之间的通信
* 在同一个 Activity 下的两个 Fragment 的通信  
  FragmentA 调用其宿主 Activity 的方法，宿主 Activity 再根据F ragmentA 的调用参数去调用 FragmentB 的方法并传递参数给 B 。
* 不同 Activity 下的两个 Fragment 的通信
  * 首先能够保证两者都能够执行到 `onActivityResult()` 方法【文章前面有说到】
  * （A传给B）FragmentA 通过 startActivityForResult()【调用Fragment本身或者getActivity()都可以】的方式，把Intent数据等传到另一个Activity，然后让另一个Activity传值给FragmentB
  * （B返回给A）FragmentB 处理完，通过 getActivity().setResult() 把返回的数据设置好，然后返回 Activity，A 再从它的 onActivityResult 中拿。
* 同一个 Activity 下，DialogFragment 与 Fragment的交互：
  > 原理：FragmentA中new一个DialogFragment对象，并让其`setTargetFragment()`来绑定目的Fragment，等DialogFragment处理完数据，调用刚刚绑定的FragmentA的`onActivityResult()`把数据传回给FragmetnA。
上关键代码:

*<u>Fragment 的代码</u>*
```java
public class ContentFragment extends Fragment  
{  
    //...  
    @Override  
    public View onCreateView(LayoutInflater inflater, ViewGroup container,  
            Bundle savedInstanceState)  
    {  
        //....
        tv.setOnClickListener(new OnClickListener()  
        {  
  
            @Override  
            public void onClick(View v)  
            {  
                EvaluateDialog dialog = new EvaluateDialog();  
                //注意setTargetFragment  
                dialog.setTargetFragment(ContentFragment.this, REQUEST_EVALUATE);  
                dialog.show(getFragmentManager(), EVALUATE_DIALOG);  
            }  
        });  
        return tv;  
    }  
  
    //接收返回回来的数据  
    @Override  
    public void onActivityResult(int requestCode, int resultCode, Intent data)  
    {  
        super.onActivityResult(requestCode, resultCode, data);  
  
        if (requestCode == REQUEST_EVALUATE)  
        {  
            String evaluate = data  
                    .getStringExtra(EvaluateDialog.RESPONSE_EVALUATE);  
            Toast.makeText(getActivity(), evaluate, Toast.LENGTH_SHORT).show();  
            Intent intent = new Intent();  
            intent.putExtra(RESPONSE, evaluate);  
            getActivity().setResult(Activity.REQUEST_OK, intent);  
        }  
    }  
}  
```
*<u>DialogFragment 的代码</u>*

```java
public class EvaluateDialog extends DialogFragment
{
    private String[] mEvaluteVals = new String[] { "GOOD", "BAD", "NORMAL" };
    public static final String RESPONSE_EVALUATE = "response_evaluate";
    
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState)
    {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        builder.setTitle("Evaluate :").setItems(mEvaluteVals,
        new OnClickListener()
        {
            @Override
            public void onClick(DialogInterface dialog, int which)
            {
                setResult(which);
            }
        });
        return builder.create();
    }
    // 设置返回数据
    protected void setResult(int which)
    {
        // 判断是否设置了targetFragment
        if (getTargetFragment() == null)
            return;
        Intent intent = new Intent();
        intent.putExtra(RESPONSE_EVALUATE, mEvaluteVals[which]);
        getTargetFragment().onActivityResult(ContentFragment.REQUEST_EVALUATE,
        Activity.RESULT_OK, intent);
    }
}
```

补充：关于 DialogFragment 调整窗口大小，可以参考这篇[文章](https://link.jianshu.com/?t=http://blog.csdn.net/angcyo/article/details/50613084)



## 推荐阅读

- [Android开发细节--查漏补缺（二）：易忘难懂](https://www.jianshu.com/p/c0a4fa16b8d6)
- [Java面试相关（一）-- Java类加载全过程](https://www.jianshu.com/p/ace2aa692f96)
- http://blog.csdn.net/lmj623565791/article/details/37815413
- http://blog.csdn.net/lmj623565791/article/details/42628537/
- http://www.cnblogs.com/android-joker/p/4414891.html