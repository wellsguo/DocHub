## 自定义View 二： 基于 Layout 布局的自定义view

### 1. 布局文件

```xml
<?xml version="1.0" encoding="utf-8"?>

<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="48dp"
    android:gravity="center_vertical"
    android:orientation="horizontal">

    <TextView
        android:id="@+id/required"
        android:layout_width="8dp"
        android:layout_height="wrap_content"
        android:text="*"
        android:textColor="#ff0000" />

    <TextView
        android:id="@+id/label"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="标签"
        android:textSize="16sp" />

    <LinearLayout
        android:id="@+id/content"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:gravity="right"
        android:orientation="horizontal">

        <EditText
            android:id="@+id/text"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:background="@null"
            android:gravity="right"
            android:hint="请输入"
            android:textSize="16sp" />

        <ImageView
            android:id="@+id/tips"
            android:layout_width="12dp"
            android:layout_height="22dp"
            android:gravity="center_vertical"
            android:src="@drawable/ic_arrow_right"
            android:tint="@color/colorAccent" />
    </LinearLayout>
</LinearLayout>
```

### 属性定义

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <attr name="text" format="string"/>
    <attr name="tips" format="reference|color"/>
    <attr name="tips_visible" format="boolean" />
    <declare-styleable name="KInput">
        <attr name="required" format="boolean" />
        <attr name="label" format="string"/>
        <attr name="hint" format="string" />
        <attr name="text" />
        <attr name="text_editable" format="boolean" />
        <attr name="tips"  />
        <attr name="tips_visible" />
    </declare-styleable>

    <declare-styleable name="KTouchIn">
        <attr name="icon" format="reference|color" />
        <attr name="iconBackground" format="reference"/>
        <attr name="iconVisible" format="enum" >
            <enum name="VISIBLE" value="0"/>
            <enum name="INVISIBLE" value="1"/>
            <enum name="GONE" value="2"/>
        </attr>
        <attr name="text"/>
        <attr name="description" format="string" />
        <attr name="tips" />
        <attr name="tips_visible"/>
    </declare-styleable>
</resources>
```

### 布局与属性关联

```java
package com.kys.klib.view;

import android.content.Context;
import android.content.res.TypedArray;
import android.support.annotation.Nullable;
import android.text.TextUtils;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.kys.klib.R;

public class KInput extends LinearLayout {

    private TextView required;
    private TextView label;
    private LinearLayout content;
    private EditText text;
    private ImageView tips;

    private boolean _required;
    private String _label;
    private String _hint;
    private String _text;
    private boolean _textEditable;
    private int _tips;
    private Boolean _tipsVisible;

    public KInput(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);

        bindStyleable(context, attrs);
        bindView(context);
        init();
    }

    private void init() {
        if(!_required){
            required.setVisibility(INVISIBLE);
        }

        label.setText(_label);
        if(TextUtils.isEmpty(_text)){
            text.setText(_text);
        }else{
            text.setHint(_hint);
        }
        if(_tipsVisible){
            tips.setVisibility(GONE);
        }else{
            tips.setImageResource(_tips);
        }

        if(!_textEditable){
            text.setFocusable(false);
            text.setFocusableInTouchMode(false);
        }else{
            text.setFocusable(true);
            text.setFocusableInTouchMode(true);
        }
    }

    // 属性 绑定
    private void bindStyleable(Context context, AttributeSet attrs) {
        TypedArray ta = context.obtainStyledAttributes(attrs, R.styleable.KInput);
        _required = ta.getBoolean(R.styleable.KInput_required, false);
        _label = ta.getString(R.styleable.KInput_label);
        _hint = ta.getString(R.styleable.KInput_hint);
        _text = ta.getString(R.styleable.KInput_text);
        _textEditable = ta.getBoolean(R.styleable.KInput_text_editable,true);
        _tips = ta.getResourceId(R.styleable.KInput_tips, R.drawable.ic_arrow_right);
        _tipsVisible = ta.getBoolean(R.styleable.KInput_tips_visible,false);
    }

    // view 绑定
    private void bindView(Context context) {
        LayoutInflater.from(context).inflate(R.layout.item_kinput, this);
        required = findViewById(R.id.required);
        label = findViewById(R.id.label);
        content = findViewById(R.id.content);
        text = findViewById(R.id.text);
        tips = findViewById(R.id.tips);
    }

    public LinearLayout getContent(){
        return content;
    }

    public String getText(){
        return text.getText().toString();
    }

    public void setText(String str){
        text.setText(str);
    }

}

```

### 应用

略
