

## [控件drawableLeft图片大小控制](https://blog.csdn.net/w23851342/article/details/51744529)

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_login);
    userName = (EditText) findViewById(R.id.userName);
    passWord = (EditText) findViewById(R.id.passWord);
}
```

```java
@Override
protected void onStart() {
    super.onStart();
    //加载
    setDrawLeft(userName, R.drawable.user);
    setDrawLeft(passWord,R.drawable.password);
}
```

```java
//主方法
private void setDrawLeft(EditText editText,int res){
    // Drawable drawable = context.getDrawable(R.drawable.***);  //(API 21以上才能使用此方法)
    Drawable drawable = getResources().getDrawable(res);
    drawable.setBounds(0,0,100,100);
    editText.setCompoundDrawables(drawable,null,null,null);
}
```
> 设置前

<img src="https://img-blog.csdn.net/20160623160704864" width="400px" height="auto"/>

> 设置后

<img src="https://img-blog.csdn.net/20160623161522457" width="400px" height="auto"/>

## [防止EditText自动获取焦点](https://blog.csdn.net/u013425527/article/details/79649600)

**在父布局添加代码**

```xml
android:focusable="true"
android:focusableInTouchMode="true"
```

![](https://img-blog.csdn.net/20180322095142111)
