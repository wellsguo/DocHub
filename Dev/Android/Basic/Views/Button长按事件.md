# [Android 编程实现长按 Button 按钮连续响应功能示例](https://www.jb51.net/article/103813.htm)

## 1. 自定义长按连续响应 Button 

```java

/**
 * 长按连续响应的Button
 * Created by admin on 15-6-1.
 */
public class LongClickButton extends Button {
  /**
   * 长按连续响应的监听，长按时将会多次调用该接口中的方法直到长按结束
   */
  private LongClickRepeatListener repeatListener;
  /**
   * 间隔时间（ms）
   */
  private long intervalTime;
  private MyHandler handler;
  public LongClickButton(Context context) {
    super(context);
    init();
  }
  public LongClickButton(Context context, AttributeSet attrs) {
    super(context, attrs);
    init();
  }
  public LongClickButton(Context context, AttributeSet attrs, int defStyleAttr) {
    super(context, attrs, defStyleAttr);
    init();
  }
  /**
   * 初始化监听
   */
  private void init() {
    handler = new MyHandler(this);
    setOnLongClickListener(new OnLongClickListener() {
      @Override
      public boolean onLongClick(View v) {
        new Thread(new LongClickThread()).start();
        return true;
      }
    });
  }
  /**
   * 长按时，该线程将会启动
   */
  private class LongClickThread implements Runnable {
    private int num;
    @Override
    public void run() {
      while (LongClickButton.this.isPressed()) {
        num++;
        if (num % 5 == 0) {
          handler.sendEmptyMessage(1);
        }
        SystemClock.sleep(intervalTime / 5);
      }
    }
  }
  /**
   * 通过handler，使监听的事件响应在主线程中进行
   */
  private static class MyHandler extends Handler {
    private WeakReference<LongClickButton> ref;
    MyHandler(LongClickButton button) {
      ref = new WeakReference<>(button);
    }
    @Override
    public void handleMessage(Message msg) {
      super.handleMessage(msg);
      LongClickButton button = ref.get();
      if (button != null && button.repeatListener != null) {
        button.repeatListener.repeatAction();
      }
    }
  }
  /**
   * 设置长按连续响应的监听和间隔时间，长按时将会多次调用该接口中的方法直到长按结束
   *
   * @param listener   监听
   * @param intervalTime 间隔时间（ms）
   */
  public void setLongClickRepeatListener(LongClickRepeatListener listener, long intervalTime) {
    this.repeatListener = listener;
    this.intervalTime = intervalTime;
  }
  /**
   * 设置长按连续响应的监听（使用默认间隔时间100ms），长按时将会多次调用该接口中的方法直到长按结束
   *
   * @param listener 监听
   */
  public void setLongClickRepeatListener(LongClickRepeatListener listener) {
    setLongClickRepeatListener(listener, 100);
  }
  public interface LongClickRepeatListener {
    void repeatAction();
  }
}
```

## 2. 在 Activity 中调用

```java
LongClickButton buttonSub = (LongClickButton) findViewById(R.id.long_click_button1);
LongClickButton buttonAdd = (LongClickButton) findViewById(R.id.long_click_button2);
final TextView numberTV = (TextView) findViewById(R.id.main_number);
//连续减
buttonSub.setLongClickRepeatListener(new LongClickButton.LongClickRepeatListener() {
  @Override
  public void repeatAction() {
    numberTV.setText(String.valueOf(Integer.parseInt(numberTV.getText().toString()) - 1));
  }
}, 50);
//连续加
buttonAdd.setLongClickRepeatListener(new LongClickButton.LongClickRepeatListener() {
  @Override
  public void repeatAction() {
    numberTV.setText(String.valueOf(Integer.parseInt(numberTV.getText().toString()) + 1));
  }
}, 50);
//减1
buttonSub.setOnClickListener(new View.OnClickListener() {
  @Override
  public void onClick(View v) {
    numberTV.setText(String.valueOf(Integer.parseInt(numberTV.getText().toString()) - 1));
  }
});
//加1
buttonAdd.setOnClickListener(new View.OnClickListener() {
  @Override
  public void onClick(View v) {
    numberTV.setText(String.valueOf(Integer.parseInt(numberTV.getText().toString()) + 1));
  }
});
```

## 3.  长按相当于连续的快速点击

很多时候，长按的事件和普通点击的事件是一样的（也就是说，长按相当于连续的快速点击）。这种情况下，自定义 Button 可以更加简洁：`即在长按时，连续的调用普通的 OnClickListener`。

```java
public class LongClickButton2 extends Button {
  /**
   * 间隔时间（ms）
   */
  private long intervalTime = 50;
  private MyHandler handler;
  public LongClickButton2(Context context) {
    super(context);
    init();
  }
  public LongClickButton2(Context context, AttributeSet attrs) {
    super(context, attrs);
    init();
  }
  public LongClickButton2(Context context, AttributeSet attrs, int defStyleAttr) {
    super(context, attrs, defStyleAttr);
    init();
  }
  /**
   * 初始化监听
   */
  private void init() {
    handler = new MyHandler(this);
    setOnLongClickListener(new OnLongClickListener() {
      @Override
      public boolean onLongClick(View v) {
        new Thread(new LongClickThread()).start();
        return true;
      }
    });
  }
  /**
   * 长按时，该线程将会启动
   */
  private class LongClickThread implements Runnable {
    private int num;
    @Override
    public void run() {
      while (LongClickButton2.this.isPressed()) {
        num++;
        if (num % 5 == 0) {
          handler.sendEmptyMessage(1);
        }
        SystemClock.sleep(intervalTime / 5);
      }
    }
  }
  /**
   * 通过handler，使监听的事件响应在主线程中进行
   */
  private static class MyHandler extends Handler {
    private WeakReference<LongClickButton2> ref;
    MyHandler(LongClickButton2 button) {
      ref = new WeakReference<>(button);
    }
    @Override
    public void handleMessage(Message msg) {
      super.handleMessage(msg);
      LongClickButton2 button = ref.get();
      if (button != null) {
        //直接调用普通点击事件
        button.performClick();
      }
    }
  }
  public void setIntervalTime(long intervalTime) {
    this.intervalTime = intervalTime;
  }
}
```



