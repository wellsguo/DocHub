
## [Android TextView 设置行间距字间距](https://www.jianshu.com/p/b9838aedf405)

### 行间距

Android TextView 设置行间距的相对来说比较简单，可以通过设置TextView的android:lineSpacingExtra或android:lineSpacingMultiplier来达到你希望看到的结果。

 func. | demo
  -- | --
设置行间距 | android:lineSpacingExtra="2dp"
设置行间距的倍数 | android:lineSpacingMultiplier="1.2"

<img src="https://img-blog.csdn.net/20180315142524231?watermark/2/text/Ly9ibG9nLmNzZG4ubmV0L3NoYW5zaGFuXzExMTc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="300px" height="auto"/>


### 字间距
Android TextView 设置字间距同样并不难，然而网上很多小伙伴搜索到的方法并不靠谱，要么设置了没有效果要么就是太复杂。  
例如通过设置 TextView 的 **android:textScaleX** 属性，这并不能真正的达到设置字间距的目的，查看源码解释如下：

> Sets the extent by which text should be stretched horizontally.

因此这个属性是设置文本水平方向字体的缩放的，并不是真正意义上的设置字间距。

<img src="https://img-blog.csdn.net/20180315143834644" width="300px" height="auto"/>

###### 而真正有效并且简单的方式如下:

通过设置 **android:letterSpacing**([21+]()) 这个属性就可以非常方便的设置水平方向文本的字间距。

- XML 
```xml
android:letterSpacing="0.05"
```
- java
```java
textView.setLetterSpacing(0.05);
```

<img src="https://img-blog.csdn.net/20180315145504692?watermark/2/text/Ly9ibG9nLmNzZG4ubmV0L3NoYW5zaGFuXzExMTc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" width="300px" height="auto"/>


## [TextView显示html样式的文字](https://www.cnblogs.com/xqxacm/p/5092557.html)


TextView显示一段文字，格式为：

**<font color='red'>白雪公主</font>**（姓名，字数不确定）向您发来了 **<font color='blue'>2</font>**（消息个数，不确定）条消息

> 这段文字中名字和数字的长度是不确定的，还要求名字和数字各自有各自的颜色。

一开始我想的是用 [SpannableString 与 SpannableStringBuilder](http://www.cnblogs.com/xqxacm/p/4962209.html) 来实现，因为它可以实现一段文字显示不同的颜色。
但是貌似它只能固定哪些位置的文字显示什么样式，于是乎放弃。
然后就想到了用 ```Html.fromHtml(String str)``` 来实现。


比如：

```java
Html.fromHtml(<font color='red'>白雪公主</font>" )
```
```java
names.add("奥特曼");
names.add("白雪公主与七个小矮人");
names.add("沃德天·沃纳陌帅·帅德·布耀布耀德 ");

counts.add(1);
counts.add(123);
counts.add(9090909);

for (int i = 0; i < 3; i++) {
    message.add("<font color='red' size='20'>"+names.get(i)+"</font>"+"向您发来"+
                "<font color='blue' size='30'>"+counts.get(i)+"</font>"+"条信息");
}

textView.setText(Html.fromHtml(message.get(0)));
textView2.setText(Html.fromHtml(message.get(1)));
textView3.setText(Html.fromHtml(message.get(2)));
```
<img src="https://images2015.cnblogs.com/blog/493196/201512/493196-20151231191658557-1463138141.jpg" width="400px" height="auto"/>

## [SpannableString & SpannableStringBuilder 实现 RichText](https://blog.csdn.net/harvic880925/article/details/38984705)

![](https://img-blog.csdn.net/20140901205141739)


### [前言](https://blog.csdn.net/fengkuanghun/article/details/7904284 )

在开发应用过程中经常会遇到显示一些不同的字体风格的信息犹如默认的 LockScreen 上面的时间和充电信息。对于类似的情况，可能第一反应就是用不同的多个T extView 来实现，对于每个 TextView 设置不同的字体风格以满足需求。这里推荐的做法是使用 `android.text.\*` 和 `android.text.style.*;`。

主要的基本工具类有:
* android.text.Spanned; 
* android.text.SpannableString; 
* android.text.SpannableStringBuilder;

使用这些类来代替常规 `String`。`SpannableString` 和 `SpannableStringBuilder` 可以用来设置不同的 `Span`(样式)，这些 `Span` 便是用于实现 RichText，比如粗体，斜体，前景色，背景色，字体大小，字体风格等等，`android.text.style.*` 中定义了很多的 `Span` 类型可供使用。

### **SpannableString** vs. **SpannableStringBuilder**

* SpannableString
```java
SpannableString word = new SpannableString("The quick fox jumps over the lazy dog");
```

* SpannableStringBuilder
```java
SpannableStringBuilder multiWord = new SpannableStringBuilder();
multiWord.append("The Quick Fox");
multiWord.append("jumps over");
multiWord.append("the lazy dog");
```

### 使用方法
```java
/**
 * Set the style span to Spannable, such as SpannableString or SpannableStringBuilder
 * @param what --- the style span, such as StyleSpan
 * @param start --- the starting index of characters to which the style span to apply
 * @param end --- the ending index of characters to which the style span to apply
 * @param flags --- the flag specified to control
 */
setSpan(Object what, int start, int end, int flags);
```

###### 常见的 Span
Span | Desc.
-- | --
AbsoluteSizeSpan(int size) | 设置字体大小，参数是绝对数值
RelativeSizeSpan(float proportion) | 设置字体大小，参数是相对于默认字体大小的倍数
ScaleXSpan(float proportion) | 缩放字体，参数是相对于默认字体大小的倍数
BackgroundColorSpan(int color) |背景着色
ForegroundColorSpan(int color) |前景着色
TypefaceSpan(String family) |字体，参数是字体的名字比如“sans", "sans-serif"等
StyleSpan(Typeface style) | 字体风格，比如粗体，斜体等。
StrikethroughSpan | 删除线
UnderlineSpan | 下划线
ImageSpan | 图片置换

### DEMO

```java
SpannableString spanString = new SpannableString("欢迎光临Harvic的博客");  
Drawable d = getResources().getDrawable(R.drawable.ic_launcher);  
d.setBounds(0, 0, d.getIntrinsicWidth(), d.getIntrinsicHeight());  
ImageSpan span = new ImageSpan(d, ImageSpan.ALIGN_BASELINE);  
spanString.setSpan(span, 2, 4, Spannable.SPAN_EXCLUSIVE_EXCLUSIVE);  
editText.setText(spanString); 
```

## SpinnaleString vs Html.fromHtml()

 SpannableString 的样式设置必须给定起止位置，而 html 方式则没有这方面的限制，编码更加灵活。