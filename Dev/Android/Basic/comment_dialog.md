## \# [Android评论回复弹框](https://blog.csdn.net/qq_32518491/article/details/85000421)

这是一个很多app评论回复的时候  ， 经常用到的弹框。使用Dialog的方式，不会耦合布局，使用简单，可在任何地方使用。可自定义样式。

进入自动弹出输入法，发送后自动关闭输入法，设置最大输入字数，超过字数后，字体会变红 等功能。

![](https://img-blog.csdnimg.cn/20181214142742778.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTE4NDkx,size_16,color_FFFFFF,t_70)
![](https://img-blog.csdnimg.cn/20181214145553851.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNTE4NDkx,size_16,color_FFFFFF,t_70)
 
### \# InputTextMsgDialog

```java
public class InputTextMsgDialog extends AppCompatDialog {
    private Context mContext;
    private InputMethodManager imm;
    private EditText messageTextView;
    private TextView confirmBtn;
    private RelativeLayout rlDlg;
    private int mLastDiff = 0;
    private TextView tvNumber;
    private int maxNumber = 200;
 
    public interface OnTextSendListener {
 
        void onTextSend(String msg);
    }
 
 
    private OnTextSendListener mOnTextSendListener;
 
    public InputTextMsgDialog(@NonNull Context context, int theme) {
        super(context, theme);
        this.mContext = context;
        this.getWindow().setWindowAnimations(R.style.main_menu_animstyle);
        init();
        setLayout();
    }
 
    /**
     * 最大输入字数  默认200
     */
    @SuppressLint("SetTextI18n")
    public void setMaxNumber(int maxNumber) {
        this.maxNumber = maxNumber;
        tvNumber.setText("0/" + maxNumber);
    }
 
    /**
     * 设置输入提示文字
     */
    public void setHint(String text) {
        messageTextView.setHint(text);
    }
 
    /**
     * 设置按钮的文字  默认为：发送
     */
    public void setBtnText(String text) {
        confirmBtn.setText(text);
    }
 
    private void init() {
        setContentView(R.layout.dialog_input_text_msg);
        messageTextView = (EditText) findViewById(R.id.et_input_message);
        tvNumber = (TextView) findViewById(R.id.tv_test);
        final LinearLayout rldlgview = (LinearLayout) findViewById(R.id.rl_inputdlg_view);
        messageTextView.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
 
            }
 
            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
 
            }
 
            @Override
            public void afterTextChanged(Editable editable) {
                tvNumber.setText(editable.length() + "/" + maxNumber);
                if (editable.length() > maxNumber) {
                    // dot_hong 颜色值：#E73111,text_bottom_comment颜色值：#9B9B9B
                    tvNumber.setTextColor(mContext.getResources().getColor(R.color.dot_hong));  
                } else {
                    tvNumber.setTextColor(mContext.getResources().getColor(R.color.text_bottom_comment));
                }
                if (editable.length() == 0) {
                    confirmBtn.setBackgroundResource(R.drawable.btn_send_normal);
                } else {
                    confirmBtn.setBackgroundResource(R.drawable.btn_send_pressed);
                }
            }
        });

        confirmBtn = (TextView) findViewById(R.id.confrim_btn);
        LinearLayout ll_tv = findViewById(R.id.ll_tv);
        imm = (InputMethodManager) mContext.getSystemService(Context.INPUT_METHOD_SERVICE);
 
        ll_tv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String msg = messageTextView.getText().toString().trim();
                if (msg.length() > maxNumber) {
                    Toast.makeText(mContext, "超过最大字数限制", Toast.LENGTH_LONG).show();
                    return;
                }
                if (!TextUtils.isEmpty(msg)) {
                    mOnTextSendListener.onTextSend(msg);
                    imm.showSoftInput(messageTextView, InputMethodManager.SHOW_FORCED);
                    imm.hideSoftInputFromWindow(messageTextView.getWindowToken(), 0);
                    messageTextView.setText("");
                    dismiss();
                } else {
                    Toast.makeText(mContext, "请输入文字", Toast.LENGTH_LONG).show();
                }
                messageTextView.setText(null);
            }
        });
 
        messageTextView.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                switch (actionId) {
                    case KeyEvent.KEYCODE_ENDCALL:
                    case KeyEvent.KEYCODE_ENTER:
                        if (messageTextView.getText().length() > maxNumber) {
                            Toast.makeText(mContext, "超过最大字数限制", Toast.LENGTH_LONG).show();
                            return true;
                        }
                        if (messageTextView.getText().length() > 0) {
                            imm.hideSoftInputFromWindow(messageTextView.getWindowToken(), 0);
                            dismiss();
                        } else {
                            Toast.makeText(mContext, "请输入文字", Toast.LENGTH_LONG).show();
                        }
                        return true;
                    case KeyEvent.KEYCODE_BACK:
                        dismiss();
                        return false;
                    default:
                        return false;
                }
            }
        });
 
        messageTextView.setOnKeyListener(new View.OnKeyListener() {
            @Override
            public boolean onKey(View view, int i, KeyEvent keyEvent) {
                Log.d("My test", "onKey " + keyEvent.getCharacters());
                return false;
            }
        });
 
        rlDlg = findViewById(R.id.rl_outside_view);
        rlDlg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (v.getId() != R.id.rl_inputdlg_view)
                    dismiss();
            }
        });
 
        rldlgview.addOnLayoutChangeListener(new View.OnLayoutChangeListener() {
            @Override
            public void onLayoutChange(View view, int i, int i1, int i2, int i3, int i4, int i5, int i6, int i7) {
                Rect r = new Rect();
                //获取当前界面可视部分
                getWindow().getDecorView().getWindowVisibleDisplayFrame(r);
                //获取屏幕的高度
                int screenHeight = getWindow().getDecorView().getRootView().getHeight();
                //此处就是用来获取键盘的高度的， 在键盘没有弹出的时候 此高度为0 键盘弹出的时候为一个正数
                int heightDifference = screenHeight - r.bottom;
 
                if (heightDifference <= 0 && mLastDiff > 0) {
                    dismiss();
                }
                mLastDiff = heightDifference;
            }
        });
        rldlgview.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                imm.hideSoftInputFromWindow(messageTextView.getWindowToken(), 0);
                dismiss();
            }
        });
 
        setOnKeyListener(new OnKeyListener() {
            @Override
            public boolean onKey(DialogInterface dialogInterface, int keyCode, KeyEvent keyEvent) {
                if (keyCode == KeyEvent.KEYCODE_BACK && keyEvent.getRepeatCount() == 0)
                    dismiss();
                return false;
            }
        });
    }
 
    private void setLayout() {
        getWindow().setGravity(Gravity.BOTTOM);
        WindowManager m = getWindow().getWindowManager();
        Display d = m.getDefaultDisplay();
        WindowManager.LayoutParams p = getWindow().getAttributes();
        p.width = WindowManager.LayoutParams.MATCH_PARENT;
        p.height = WindowManager.LayoutParams.WRAP_CONTENT;
        getWindow().setAttributes(p);
        setCancelable(true);
        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_VISIBLE);
    }
 
 
    public void setmOnTextSendListener(OnTextSendListener onTextSendListener) {
        this.mOnTextSendListener = onTextSendListener;
    }
 
    @Override
    public void dismiss() {
        super.dismiss();
        //dismiss之前重置mLastDiff值避免下次无法打开
        mLastDiff = 0;
    }
 
    @Override
    public void show() {
        super.show();
    }
}
```

下面是布局文件.

### \# dialog_input_text_msg

```xml
<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/rl_outside_view"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="horizontal">
 
    <LinearLayout
        android:id="@+id/rl_inputdlg_view"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:background="@color/white"
        android:orientation="vertical">
 
        <ImageView
            android:id="@+id/iv_smile"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:visibility="gone" />
 
        <EditText
            android:id="@+id/et_input_message"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:background="@drawable/room_chat_bg"
            android:gravity="top"
            android:hint="想说点什么"
            android:imeOptions="flagNoExtractUi"
            android:lineSpacingMultiplier="1.2"
            android:maxLength="2000"
            android:maxLines="6"
            android:minHeight="104dp"
            android:paddingBottom="10dp"
            android:paddingLeft="15dp"
            android:paddingRight="15dp"
            android:paddingTop="10dp"
            android:scrollbars="vertical"
            android:textColor="#FF333333"
            android:textColorHint="@color/text_bottom_comment"
            android:textSize="@dimen/textsize_14"
            tools:ignore="InvalidImeActionId" />
 
        <View
            android:layout_width="match_parent"
            android:layout_height="@dimen/line"
            android:background="@color/line" />
 
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal"
            android:paddingBottom="@dimen/margins_10"
            android:paddingLeft="@dimen/margins_15"
            android:paddingTop="@dimen/margins_10">
 
            <TextView
                android:id="@+id/tv_test"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:layout_gravity="center"
                android:text="0/200"
                android:textColor="@color/text_bottom_comment" />
 
            <LinearLayout
                android:id="@+id/confirm_area"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_gravity="center"
                android:gravity="right"
                android:orientation="horizontal">
 
                <ImageView
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:layout_gravity="center"
                    android:paddingRight="10dp"
                    android:visibility="gone" />
 
 
                <LinearLayout
                    android:id="@+id/ll_tv"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:gravity="right"
                    android:orientation="horizontal"
                    android:paddingRight="@dimen/margins_15">
 
 
                    <TextView
                        android:id="@+id/confrim_btn"
                        android:layout_width="50dp"
                        android:layout_height="28dp"
                        android:background="@drawable/btn_send_normal"
                        android:gravity="center"
                        android:text="发送"
                        android:textColor="@color/white" />
                </LinearLayout>
            </LinearLayout>
        </LinearLayout>
    </LinearLayout>
</RelativeLayout>
```

### \# btn_send_normal

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="4dp"/>
    <solid android:color="#FFD2D2D2"/>
</shape>
```

### \# btn_send_pressed

```xml
<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="4dp"/>
    <solid android:color="#F9780D"/>
</shape>
```

### \#  main_menu_animstyle

```xml
    <style name="main_menu_animstyle">
        <item name="android:windowEnterAnimation">@anim/anim_enter_from_bottom</item>
        <item name="android:windowExitAnimation">@anim/anim_exit_from_bottom</item>
    </style>
```

### \# anim_enter_from_bottom

```xml
<?xml version="1.0" encoding="utf-8"?>
 
<set xmlns:android="http://schemas.android.com/apk/res/android">
    <translate 
        android:fromYDelta="100%"
        android:toYDelta="0"
        android:fillAfter="false"
        android:duration="300"   
        /> 
    <alpha 
        android:fromAlpha="0.0"
        android:toAlpha="1.0"
        android:duration="300"
        android:fillAfter="true"/>
    </set>
```

### \# anim_exit_from_bottom

```xml
<?xml version="1.0" encoding="utf-8"?>
 
<set xmlns:android="http://schemas.android.com/apk/res/android">
   <translate 
        android:fromYDelta="0"
        android:toYDelta="100%"
        android:fillAfter="false"
        android:duration="300"   
        /> 
    <alpha 
        android:fromAlpha="1.0"
        android:toAlpha="0.0"
        android:duration="300"
        android:fillAfter="true"/>
    </set>
```

## 使用方式

在 OnCreate 方法里直接 new 出这个 Dialog 即可，在需要的地方调用 show 方法显示.

```java
 inputTextMsgDialog = new InputTextMsgDialog(mContext, R.style.dialog_center);
 inputTextMsgDialog.setmOnTextSendListener(new InputTextMsgDialog.OnTextSendListener() {
            @Override
            public void onTextSend(String msg) {
                //点击发送按钮后，回调此方法，msg为输入的值
            }
        });
```

下面是dialog_center的代码，如果你需要让这个Dialog点击空白部分的activity时消失，背景变暗等功能，就加上这个style.

### \# style.xml

```xml
  <!-- 中间弹出框 -->
    <style name="dialog_center" parent="Theme.AppCompat.Dialog.Alert">
        <!-- 去黑边 -->
        <item name="android:windowFrame">@null</item>
        <item name="android:screenOrientation">portrait</item>
        <!-- 设置是否可滑动 -->
        <item name="android:windowIsFloating">true</item>
        <!-- 背景 -->
        <!-- 窗口背景 @color/touming的值为：#00000000 ， style中不能直接引用16进制，感谢评论区的老铁提醒-->
 
        <item name="android:windowBackground">@color/touming</item> 
 
        <!-- 是否变暗 -->
        <item name="android:backgroundDimEnabled">true</item>
        <!-- 点击空白部分activity不消失 -->
        <item name="android:windowCloseOnTouchOutside">true</item>
    </style>
```

### \# API

- inputTextMsgDialog.show()   //显示此dialog
- inputTextMsgDialog.dismiss()  //隐藏此dialog
- inputTextMsgDialog.setHint()   //设置输入提示文字
- inputTextMsgDialog.setBtnText()  //设置按钮的文字 默认为：发送
- inputTextMsgDialog.setMaxNumber()  //最大输入字数 默认200

注1：如果需要自定义样式，请自己写一个layout，替换dialog_input_text_msg。

注2：如果需要改变按钮颜色等，修改btn_send_normal和btn_send_pressed里的

```xml
<solid android:color="#FFD2D2D2"/>
```

其中，btn_send_normal为输入框内未输入文字的颜色，btn_send_pressed为输入后的颜色。
