# Android 共享元素的基本使用以及一些需要注意的坑

## 1. 如何实现 fragment 到 fragment 共享元素?

在微信朋友圈查看九宫格图片的大图或类似场景，为了提高 UI 的性能和响应时间，可以通过元素共享方式来实现。假设我们RecycleView（fragment中）的某一个 item 中点击图片，跳转到另外一个 View 中。

### 1.1 在 adapter 中为 imageview 设置 transitionName

```java
@Override
public void onBindViewHolder(final MyViewHolder holder, final int position) {
    //省略
    
    ViewCompat.setTransitionName(holder.getImageView(), url);
    //省略
    
}
```

使用 `ViewCompat.setTransitionName` 为每一个 image 绑定他自己的照片url，防止重复（前提是你的照片url不重复）。我们将 adapter 的图片的 fragment 定义为 `界面1`， 显示大图的 fragment 定义为`界面2`。

### 1.2 设置跳转目标页面的 transiotionName

此时我们已经为 `界面1` 的每一个 imageView 都绑定了 transitionName，接下来我们需要为 `界面2` 的照片也设置一个transiotionName。

###### 界面2 的 xml 设置

```xml
<ImageView
        android:id="@+id/detail_image"
        android:layout_width="240dp"
        android:layout_height="240dp"
        android:transitionName="TransitionName"
        tools:ignore="UnusedAttribute"/>
```

trasitionName 可以静态 xml 设置也可以动态设置.

### 1.3 跳转

在两边界面都设置后，就可以进行跳转了。

```java
//界面2的fragment
DetailFragment detailFragment = DetailFragment.newInstance(position);

if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
    detailFragment.setSharedElementEnterTransition(new DetailTransition());
    setExitTransition(new Fade());
    detailFragment.setEnterTransition(new Fade());
    detailFragment.setSharedElementReturnTransition(new DetailTransition());
}

getActivity().getSupportFragmentManager().beginTransaction()
        .addSharedElement(holder.getImageView(), "TransitionName")
        .replace(R.id.main_cl_container, detailFragment)
        .addToBackStack(null)
        .commit();
```

其中需要注意的是 `addSharedElement` 中的 **参数1**是 `界面1` 的 imageview, **参数2**是`界面2`的 imageview 的 transitionName。

效果及源码参见[链接](https://www.jianshu.com/p/e9f63ead8bf5).


## 2. 有哪些坑呢？

### 2.1 不能用 add 只能用 replace

fragment 跳转的时候不能用 `add` 只能用 `replace`。我在这里卡住一段时间最后发现不能用add。

### 2.2 加载网络图片会有问题

因为如果下载图片时间比 transition 共享的动画慢的话，动画会有问题。

#### 怎么解决呢？

##### `A1`: [StackOverflow's solution](https://stackoverflow.com/questions/26977303/how-to-postpone-a-fragments-enter-transition-in-android-lollipop)  


> There's no direct equivalent in Fragment Transitions because Fragments use FragmentTransaction and we can't really postpone something that is supposed to happen in a transaction.
>
>To get the equivalent, you can add a Fragment and hide it in a transaction, then when the Fragment is ready, remove the old Fragment and show the new Fragment in a transaction.

```java
getFragmentManager().beginTransaction()
    .add(R.id.container, fragment2)
    .hide(fragment2)
    .commit();
```

Later, when fragment2 is ready:

```java
getFragmentManager().beginTransaction()
    .addSharedElement(sharedElement, "name")
    .remove(fragment1)
    .show(fragment2)
    .commit();
```

> 但是我没试验成功

##### `A2`: 使用 activity 而不使用 fragment  

我强烈建议使用方法2。使用activty的话要提到两个关键方法 `postponeEnterTransition()` 和 `startPostponedEnterTransition()` 
第一个是暂停共享元素动画，第二个是开始共享元素动画，这两个方法只能在 activity 中使用。

**代码实现**

  - 首先在界面1的adapter中 绑定每一个 imageview 的 transitionName
```java
ViewCompat.setTransitionName(holder.getImageView(), url);
```
界面1可以是 activity 也可以是 fragment 都不影响

  - 然后跳转方式要换成activity的跳转方式
```java
ActivityOptionsCompat activityOptions = ActivityOptionsCompat.makeSceneTransitionAnimation(
                            getActivity(),
                            new Pair<View, String>(view,o.getText()));
Intent intent = new Intent(getActivity(), PhotoActivity.class);
intent.putExtra("url", o.getText());
ActivityCompat.startActivity(getActivity(), intent, activityOptions.toBundle());
```

    其中 `new Pair<View, String>(view,o.getText())` 第一个参数就是要进行共享元素的view（在这里是imageView） 第二个参数就是界面2的view的transitionName。界面1和界面2的view的transitionName要一致，因此我传递了url过去界面2

  - 界面2：
在界面2的activty中 直接套上之前的fragment就行
然后设置界面2的imageview的transitionName，这里我们动态进行设置

    ```java
    getActivity().postponeEnterTransition();//先停止
    ViewCompat.setTransitionName(photoView, url);//然后设置transitionName， photoview为界面2要进行共享元素的view
    ```

- 然后使用 [glide4.0]() 加载网络图片
```java
Glide
    .with(App.getContext())
    .load(url)
    .apply(options)
    .listener(new RequestListener<Drawable>() {
        @Override
        public boolean onLoadFailed(@Nullable GlideException e, Object model, Target<Drawable> target, boolean isFirstResource) {
            scheduleStartPostponedTransition(photoView);
            return true;
        }

        @Override
        public boolean onResourceReady(Drawable resource, Object model, Target<Drawable> target, DataSource dataSource, boolean isFirstResource) {
            photoView.setImageDrawable(resource);
            scheduleStartPostponedTransition(photoView);
            return true;
        }
    })
    .into(photoView);
```

- 重点是 listener 里面的 `scheduleStartPostponedTransition` 方法
```java
if (sharedElement == null) return;
sharedElement.getViewTreeObserver().addOnPreDrawListener(
        new ViewTreeObserver.OnPreDrawListener() {
            @TargetApi(Build.VERSION_CODES.LOLLIPOP)
            @Override
            public boolean onPreDraw() {
                if (sharedElement == null) return false;
                sharedElement.getViewTreeObserver().removeOnPreDrawListener(this);
                getActivity().startPostponedEnterTransition();//开启动画
                return true;
            }
        });
```
通过activity 就能使用这两个方法进行延时了。

还需要注意的是，如果发现动画能运行。但是定位到图片上的时候有偏差，那可能是你设置了centerCrop之类的属性，查看一下 去掉，就行了。

fragment多次调用onCreateView导致动画部分失效
如果还是不行得话 看看有没有可能是fragment多次调用onCreateView，打一下log

解决方法就是判断是否是第一次加载root view

```java
private View rootView;

//oncreateview
if (null != rootView) {//不是第一次
    ViewGroup parent = (ViewGroup) rootView.getParent();
    if (parent != null) {
        parent.removeView(rootView);
    }
    unbinder = ButterKnife.bind(this, rootView);////这一句是因为用了ButterKnife注入 没有用得忽视就行
} else {//第一次
    rootView = inflater.inflate(R.layout.fragment_gallery, container, false);
    unbinder = ButterKnife.bind(this, rootView);//这一句是因为用了ButterKnife注入 没有用得忽视就行

    EventBus.getDefault().register(this);
    initRv();
    initToolbar();
    initData();
    initEvent();
}
return rootView;
```
## more
- *[Android高阶转场动画-ShareElement完全攻略](https://www.jianshu.com/p/fa1c8deeaa57)*
- *[Android动画：转场动画(过度动画) ActivityOptionsCompat](https://blog.csdn.net/ss1168805219/article/details/53445063)*
