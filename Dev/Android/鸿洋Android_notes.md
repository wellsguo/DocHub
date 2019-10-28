## [ListView滑动删除 ，仿腾讯QQ](https://blog.csdn.net/lmj623565791/article/details/22961279)

QQListView 继承 ListView 并在其中添加了如：滑动最小距离(touchSlop)，是否响应滑动，手指按下、抬起等事件的坐标位置，当前手指位置，当前view，PopupWindow等。

通过 `dispatchTouchEvent` 监听 MotionEvent.ACTION_DOWN 获取手指按下坐标信息，`View view = getChildAt(mCurrentViewPos - getFirstVisiblePosition());` 获取当前手指按下的 Item。

并监听 MotionEvent.ACTION_MOVE 获取滑动的位置，并计算，从而判断是否应该相应滑动事件。

 `onTouchEvent(MotionEvent ev)` 方法则根据 `dispatchTouchEvent` 方法中设置的响应滑动信息标志，来对自右向左的侧滑进行响应：在 Item 的右侧显示删除 PopupWindow ,并注册 PopupWindow 的点击事件。


## [Android 从网络中获取数据时 产生部分数据乱码的解决](https://blog.csdn.net/lmj623565791/article/details/23562939)

在得到 InputStream 流后，再用 InputStreamReader 封装一下`InputStreamReader isr = new InputStreamReader(is,"UTF-8");`.