**[QMUI 源码~自定义VIEW]()**



##  VIEW 框架

```java
public class QMUICommonListItemView extends RelativeLayout {
  /// ……
} 

```



```xml
<merge xmlns:android="http://schemas.android.com/apk/res/android"
       android:layout_width="match_parent"
       android:layout_height="wrap_content">

</merge>
```



> 在上述的框架中，自定义的 QMUICommonListItemView 继承了 RelativeLayout。采用了继承 Android 的基础 View 组件方式， XML 中使用了 merge 来完成作为父节点可以有效减小 ViewTree 的嵌套层次。



## 属性注解

```java
@IntDef({ACCESSORY_TYPE_NONE, ACCESSORY_TYPE_CHEVRON, ACCESSORY_TYPE_SWITCH, ACCESSORY_TYPE_CUSTOM})
@Retention(RetentionPolicy.SOURCE)
public @interface QMUICommonListItemAccessoryType {
}
```



### RetentionPolicy LifeCycle

- SOURCE：Annotations are to be discarded by the compiler.
- RUNTIME: Annotations are to be recorded in the class file by the compiler and **retained by the VM at run time, so they may be read reflectively**.
- CLASS: Annotations are to be recorded in the class file by the compiler but **need not be retained by the VM at run time**.

`.java —> .class —> .dex —> .apk`

`CLASS` 的作用时间最多是在 `.class -> apk`，这个过程是由 Android 系统来进行编译和打包的，那么能够操作 `CLASS` 注解的人，也就只有 Android 系统，换句话说，也就是来定制开发编译过程的开发人员来做，譬如 ButterKnife、GreenDao 等。

```java
/**
 * Bind a field to the view for the specified ID. The view will automatically be cast to the field
 * type.
 * <pre><code>
 * {@literal @}BindView(R.id.title) TextView title;
 * </code></pre>
 */
@Retention(CLASS) @Target(FIELD)
public @interface BindView {
  /** View ID to which the field will be bound. */
  @IdRes int value();
}
```



`RetentionPolicy.SOURCE` 仅仅是给应用层开发人员用的（如，规范输入参数的范围等），`RetentionPolicy.CLASS` 需要应用层和底层系统开发人员配合使用。注解 *`@IntDef`* 限定了取值范围，最后将*`@SeparatorStyle`*注解用在参数上就行了，这样在使用调用方法的使用只能使用指定的参数*`{SEPARATOR_STYLE_NORMAL, SEPARATOR_STYLE_NONE}`*，就算用`数值 1 `编译器也会提示报错。除了*`@IntDef`*注解外还用一个 *`@StringDef`* 注解，用于字符串处理。

```java
public static final int SEPARATOR_STYLE_NORMAL = 0;
public static final int SEPARATOR_STYLE_NONE = 1;

@IntDef({SEPARATOR_STYLE_NORMAL, SEPARATOR_STYLE_NONE})
@Retention(RetentionPolicy.SOURCE)
public @interface SeparatorStyle {
}
```









