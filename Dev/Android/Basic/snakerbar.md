Dialog 和 Toast，我们在日常的开发中一定非常熟悉，常常被用来作为Android应用内提示性信息的两种展示方式。然而 Google 在 Design 包中又提供了一种新的选择，那就是 **Snackbar**。今天主要介绍 Snackbar 新控件的使用，以及三种提示信息展示方式的比较。

## 什么是Snackbar
**Snackbar** 是 Android 5.0 新特性—— Material Design 中的一个控件，用来代替 Toast ，Snackbar 与 Toast 的主要区别是：**Snackbar可以滑动退出，也可以处理用户交互（点击）事件**。

## Snackbar的特性
1. Snackbar会在超时或者用户在屏幕其他地方触摸之后自动消失；
2. 可以在屏幕上滑动关闭；
3. 出现时不会阻碍用户在屏幕上的输入
4. 屏幕上同时最多只能显示一个Snackbar
5. 如果在屏幕上有一个Snackbar的情况下再显示一个Snackbar，则先将当前显示的Snackbar隐藏后再显示新的Snackbar
6. 可以在Snackbar中添加一个按钮，处理用户点击事件
7. Snackbar一般需要CoordinatorLayout来作为父容器，CoordinatorLayout保证Snackbar可以右滑退出

## Snackbar的使用

通过上文的介绍，我们对Snackbar的含义和功能有了基本了解，接下来通过代码来详细介绍Snackbar的使用。
使用MD控件，首先要在gradle文件中导入依赖，本文中使用的依赖包如下：

```groovy
compile 'com.android.support:design:25.3.0'
```

弹出Snackbar，弹出 Snackbar 的方式和 Toast 方式相似，通过调用 Snackbar 类中的静态方法 `make()` 设置相关信息，`show()` 方法弹窗S nackbar

```java
Snackbar.make(view, message, duration)
        .setAction(action message, click listener)
        .show();
```

### 1. make() 实现简单弹出
- 第一个参数是一个 view，snackbar 会找到一个父 view，以寄存所赋的 snackbar 值。Snackbar 会沿着 view 的树状路径，找到第一个合适的布局或窗口视图，作为父 view。一般是一个CoordinatorLayout对象。
- 第二个参数是Snackbar中想要显示的内容，一般只能显示2行；
- 第三个参数是Snackbar想要显示的时间长短，有三个值：LENGTH_INDEFINITE 永远显示、LENGTH_LONG显示较长时间、LENGTH_SHORT 显示较短时间；

Snackbar也要像Toast一样，调用show()方法才能显示。

#### 案例分析

首先，我们创建一个 Activity，在布局文件中添加 **CoordinatorLayout** 控件，并创建一个 FloatingActionButton，用于测试 FloatingActionButton 结合 Snackbar 的展示效果。布局文件如下：

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context="com.ease.wawaandroid.testdemo.SnackbarActivity">

    <android.support.design.widget.CoordinatorLayout
        android:id="@+id/snackbar_container"
        android:layout_width="match_parent"
        android:layout_height="match_parent">

        <android.support.design.widget.FloatingActionButton
            android:id="@+id/snackbar_fab"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="right|bottom"
            android:layout_marginBottom="10dp"
            android:layout_marginRight="10dp"
            app:borderWidth="0dp"
            app:fabSize="normal" />

    </android.support.design.widget.CoordinatorLayout>

</android.support.constraint.ConstraintLayout>
```

在Activity中对控件进行初始化，并监听FloatingActionButton的点击事件，实现点击FloatingActionButton，弹出Snackbar，Activity的代码如下：

```java
public class SnackbarActivity extends AppCompatActivity implements View.OnClickListener {
    private CoordinatorLayout coordinatorLayout;
    private FloatingActionButton fab;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_snackbar);

        initView();
    }

    private void initView() {
        coordinatorLayout = (CoordinatorLayout) findViewById(R.id.snackbar_container);
        fab = (FloatingActionButton) findViewById(R.id.snackbar_fab);

        fab.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.snackbar_fab:
                Snackbar.make(coordinatorLayout, "这是一个snackbar", Snackbar.LENGTH_SHORT).show();
                break;
        }
    }
}
```

执行上述代码，显示效果为：

![](https://img-blog.csdn.net/20180718120740909?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xoeTM0OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

*注意：mark()方法的第一个参数一定要是coordinatorLayout，否则，弹出的Snackbar将覆盖FloatingActionButton控件。*

到这里就基本实现了Snackbar的简单弹出，但是，目前的效果和我们之前的Toast没什么大的区别，同时发现案例中，我们并没有调用Snackbar的setAction()方法。接下来，我们将开始介绍Snackbar的另一个重要方法setAction()。

### 2.setAction()添加按钮
除了显示之外，Snackbar中还可以有一个按钮，我们称之为Action，它显示在Snackbar的右边，可以通过Snackbar对象的setAction()方法设置，修改上文中FloatingActionButton控件点击事件的处理逻辑：

```java
case R.id.snackbar_fab:
                Snackbar.make(coordinatorLayout, "这是一个snackbar", Snackbar.LENGTH_SHORT)
                        .setAction("action", new View.OnClickListener() {
                            @Override
                            public void onClick(View v) {
                                Snackbar.make(coordinatorLayout, "Action 被点击", Snackbar.LENGTH_SHORT).show();
                            }
                        })
                        .show();
                break;
```

添加setAction()方法，该方法有两个参数，第一个参数是按钮的名称，第二个参数是按钮点击事件的监听方法。显示效果如下：

![](https://img-blog.csdn.net/20180718122701574?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xoeTM0OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

### 3.显示隐藏监听
在Snackbar弹出和消失时，都会触发一个回调事件，我们可以通过Snackbar对象的addCallback()方法（setCallback()方法已经过时）捕获它们：

```java
Snackbar.make(coordinatorLayout, "这是一个snackbar", Snackbar.LENGTH_SHORT)
        .setAction("action", new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Snackbar.make(coordinatorLayout, "Action 被点击", Snackbar.LENGTH_SHORT).show();
            }
        })
        .addCallback(new Snackbar.Callback(){
            @Override
            public void onDismissed(Snackbar transientBottomBar, int event) {
                super.onDismissed(transientBottomBar, event);
                Toast.makeText(SnackbarActivity.this, "Snackbar隐藏", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onShown(Snackbar sb) {
                super.onShown(sb);
                Toast.makeText(SnackbarActivity.this, "Snackbar显示", Toast.LENGTH_SHORT).show();
            }
        })
        .show();
```

Snackbar.Callback中有两个抽象方法，onDismissed()方法是当Snackbar消失的时候触发的事件；onShown()方法是当Snackbar显示的时候触发的事件。显示效果如下所示：

![](https://img-blog.csdn.net/20180718125703619?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xoeTM0OQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

### 4.相关属性设置
Snackbar支持动态的设置一些属性，如Action的文本颜色、显示的文本内容、显示的持续时间等，可通过下面方法进行设置：

```java
Snackbar snackbar = Snackbar.make(coordinatorLayout, "Action 被点击", Snackbar.LENGTH_SHORT);
        snackbar.setText("动态文本");//动态设置文本显示内容
        snackbar.setActionTextColor(Color.RED);//动态设置Action文本的颜色
        snackbar.setDuration(5000);//动态设置显示时间

        View snackbarView = snackbar.getView();//获取Snackbar显示的View对象
        //获取显示文本View,并设置其显示颜色
        ((TextView) snackbarView.findViewById(android.support.design.R.id.snackbar_text)).setTextColor(Color.BLUE);
        //获取Action文本View，并设置其显示颜色
        ((TextView) snackbarView.findViewById(android.support.design.R.id.snackbar_action)).setTextColor(Color.BLUE);
        //设置Snackbar的背景色
        snackbarView.setBackgroundColor(Color.GREEN);

        //设置Snackbar显示的位置
        ViewGroup.LayoutParams params = snackbarView.getLayoutParams();
        CoordinatorLayout.LayoutParams layoutParams = new CoordinatorLayout.LayoutParams(params.width, params.height);
        layoutParams.gravity = Gravity.CENTER_VERTICAL;//垂直居中
        snackbarView.setLayoutParams(layoutParams);
```
至此，Snackbar的相关使用就介绍完了。

## Snackbar 与 Dialog 和 Toast 的比较
通过上文的介绍，我们知道了Snackbar和Dialog、Toast一样都是用来作为android内提示信息的，三者之间的应用场景也有所不同。

### Dialog
此刻该对话框中的内容获取了焦点，想要操作对话框以外的功能，必须先对该对话框进行响应。
**应用场景：** 对于删除确认、版本更新等重要性提示信息，需要用户做出选择的情况下，使用Dialog。

### Toast
提示框的显示并不影响我们对其他地方的操作，Toast 无法手动控制隐藏，需要设置Toast的显示时长，一旦显示时间结束，Toast会自动消失。如果多次点击并显示Toast，就会出现Toast重复创建并显示，给用户造成一种Toast长时间不隐藏的幻觉。
**应用场景：** 对于无网络提示、删除成功、发布操作完成等这类不重要的提示性信息，使用Toast；

### Snackbar
Snackbar和Toast比较相似，但是用途更加广泛，并且它是可以和用户进行交互的。Snackbar使用一个动画效果从屏幕的底部弹出来，过一段时间后也会自动消失。
**应用场景：** 删除操作时，弹出Snackbar用于确认删除操作；消息发送失败时，弹出Snackbar，用于重新发送操作；当然重要的是与MD组件相结合，用户体验效果更佳。

[原文链接](https://blog.csdn.net/lhy349/article/details/81096093)
