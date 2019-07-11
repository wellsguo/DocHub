
##### Q: toolbar的navigationIcon不垂直居中显示

*`A:`* 如果自定义的minHeight和系统默认的actionBarSize不同的话 `还是会不居中` 我干脆把toolbar的minHeight设置成了 `android:minHeight="?android:attr/actionBarSize"` 就居中了

##### Q: [解决Android 返回桌面在进入软件 会重新打开 进入欢迎界面](https://blog.csdn.net/zhw0596/article/details/82976732 )

*`A:`* 在主界面 oncreate 加
```java
if ((getIntent().getFlags() & Intent.FLAG_ACTIVITY_BROUGHT_TO_FRONT) != 0) {
    finish();
    return;
}
```
