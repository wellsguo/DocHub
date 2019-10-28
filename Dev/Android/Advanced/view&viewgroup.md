Android的UI界面都是由View和ViewGroup及其派生类组合而成的。其中，View是所有UI组件的基类，而ViewGroup是容纳View及其派生类的容器，ViewGroup也是从View派生出来的。一般来说，开发UI界面都不会直接使用View和ViewGroup（自定义控件的时候使用），而是使用其派生类。

下图：UI布局的层次结构。


![](https://img-blog.csdn.net/2018090717301180?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxOTQxMjYzMDEz/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
 

## View和ViewGroup的区别：

可以从两方面来说：

1. 事件分发方面的区别；

2. UI绘制方面的区别；

 

### 事件分发方面的区别：

事件分发机制主要有三个方法：dispatchTouchEvent()、onInterceptTouchEvent()、onTouchEvent()

1. ViewGroup 包含这三个方法，而 View 则只包含其中的两个方法，不包含 `onInterceptTouchEvent()`。

2. 触摸事件由 Action_Down、Action_Move、Action_Up 组成，一次完整的触摸事件，包含一个 Down 和 Up，以及若干个 Move（可以为0）。

3. 在 Action_Down 的情况下，事件会先传递到最顶层的 ViewGroup，调用 ViewGroup 的dispatchTouchEvent()：
   - 如果 ViewGroup 的 onInterceptTouchEvent() 返回 false 不拦截该事件，则会分发给子 View，调用子 View 的 dispatchTouchEvent()，如果子 View 的 dispatchTouchEvent() 返回 true，则调用 View 的 onTouchEvent() 消费事件。
   - 如果 ViewGroup 的 onInterceptTouchEvent() 返回 true 拦截该事件，则调用 ViewGroup 的 onTouchEvent() 消费事件，接下来的 Move 和 Up 事件将由该 ViewGroup 直接进行处理。

4. 当某个子 View 的 dispatchTouchEvent() 返回true时，会中止 Down 事件的分发，同时在 ViewGroup 中记录该子 View。接下来的 Move 和 Up 事件将由该子 View 直接进行处理。

5. 当 ViewGroup 中所有子 View 都不捕获 Down 事件时，将触发 ViewGroup 自身的 onTouch(); 触发的方式是调用 super.dispatchTouchEvent 函数，即父类 View 的 dispatchTouchEvent 方法。在所有子 View 都不处理的情况下，触发 Acitivity 的 onTouchEvent 方法。

6. 由于子 View 是保存在 ViewGroup 中的，多层 ViewGroup 的节点结构时，上层 ViewGroup 保存的会是真实处理事件的 View 所在的 ViewGroup 对象。如 ViewGroup0——ViewGroup1——TextView 的结构中，TextView 返回了 true，它将被保存在 ViewGroup1 中，而 ViewGroup1 也会返回 true，将被保存在 ViewGroup0 中；当 Move 和 Up 事件来时，会先从 ViewGroup0 传递到 ViewGroup1，再由 ViewGroup1 传递到 TextView，最后事件由 TextView 消费掉。

7. 子 View 可以调 getParent().requestDisallowInterceptTouchEvent(),请求父 ViewGroup 不拦截事件。

 

### UI绘制方面的区别：

UI绘制主要有五个方法：onDraw(),onLayout(),onMeasure()，dispatchDraw(),drawChild()

1. ViewGroup包含这五个方法，而View只包含其中的三个方法，不包含dispatchDraw(),drawChild()。

2. 绘制流程：onMeasure（测量）——> onLayout（布局）——> onDraw（绘制）。

3. 绘制按照视图树的顺序执行，视图绘制时会先绘制子控件。如果视图的背景可见，视图会在调用onDraw()之前调用drawBackGround()绘制背景。强制重绘，可以使用invalidate();

4. 如果发生视图的尺寸变化，则该视图会调用requestLayou()，向父控件请求再次布局。如果发生视图的外观变化，则该视图会调用invalidate()，强制重绘。如果requestLayout()或invalidate()有一个被调用，框架会对视图树进行相关的测量、布局和绘制。
    > 注意：视图树是单线程操作，直接调用其它视图的方法必须要在UI线程里。跨线程的操作必须使用Handler。

5. onLayout()：对于View来说，onLayout()只是一个空实现；而对于ViewGroup来说，onLayout()使用了关键字abstract的修饰，要求其子类必须重载该方法，目的就是安排其children在父视图的具体位置。

6. draw过程：drawBackground()绘制背景 ——> onDraw()对View的内容进行绘制 ——> dispatchDraw()对当前View的所有子View进行绘制 ——> onDrawScrollBars()对View的滚动条进行绘制。



 

#### 方法说明：

1. onDraw(Canvas canvas)：  
   UI绘制最重要的方法，用于UI重绘。这个方法是所有View、ViewGroup及其派生类都具有的方法。  
   自定义控件时，可以重载该方法，并在内容基于canvas绘制自定义的图形、图像效果。

2. onLayout(boolean changed, int left, int top, int right, int bottom)：  
   布局发生变化时调用此方法。这个方法是所有View、ViewGroup及其派生类都具有的方法。  
   自定义控件时，可以重载该方法，**在布局发生改变时实现特效等定制处理**。

3. onMeasure(int widthMeasureSpec, int heightMeasureSpec)：  
   用于计算自己及所有子对象的大小。这个方法是所有View、ViewGroup及其派生类都具有的方法。  
   自定义控件时，可以重载该方法，重新计算所有对象的大小。   
   MeasureSpec 包含了测量的模式和测量的大小，通过MeasureSpec.getMode()获取测量模式，通过MeasureSpec.getSize()获取测量大小。  
   - mode共有三种情况： 
     - MeasureSpec.UNSPECIFIED（ View想多大就多大）;
     - MeasureSpec.EXACTLY（默认模式，精确值模式：将layout_width或layout_height属性指定为具体数值或者match_parent）;
     - MeasureSpec.AT_MOST（ 最大值模式：将layout_width或layout_height指定为wrap_content）。

4. dispatchDraw(Canvas canvas)：  
   ViewGroup及其派生类具有的方法，主要用于控制子View的绘制分发。  
   自定义控件时，重载该方法可以改变子View的绘制，进而实现一些复杂的视效。

5. drawChild(Canvas canvas, View child, long drawingTime)：  
   ViewGroup及其派生类具有的方法，用于直接绘制具体的子View。  
   自定义控件时，重载该方法可以直接绘制具体的子View。

————————————————  
版权声明：本文为CSDN博主「一个灵活的胖子」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。  
原文链接：https://blog.csdn.net/qq941263013/article/details/82500145