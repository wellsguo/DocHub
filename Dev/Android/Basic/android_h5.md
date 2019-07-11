
作者：horseLai  
链接：https://www.jianshu.com/p/7bfa5e288aa3  
来源：简书  
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

作者：吴威龙   
来源：CSDN   
原文：https://blog.csdn.net/leaf_130/article/details/55510921   
版权声明：本文为博主原创文章，转载请附上博文链接！  


## 混合开发概述
微信，微博以及现在市面上大量的软件使用内嵌了H5页面；有些外包公司，为了节约成本，采用Android内嵌H5模式开发，便于在IOS上直接复用页面， 从而提高开发效率。


## 实现的原理
本质是 **Java 和 Javascript 之间调用**.  
H5 页面，只是 Html 的扩展，仅作业面展示，而 Javascript 用来处理页面的逻辑



### WebView的基本设置

```
private void initWebView() {
    webView = new WebView(this);
    WebSettings webSettings = webView.getSettings();
    
    //设置支持javaScript脚步语言
    webSettings.setJavaScriptEnabled(true);

    //支持双击-前提是页面要支持才显示
    //webSettings.setUseWideViewPort(true);

    //支持缩放按钮-前提是页面要支持才显示
    webSettings.setBuiltInZoomControls(true);

    //设置客户端-不跳转到默认浏览器中
    webView.setWebViewClient(new WebViewClient());

    //设置支持js调用java
    webView.addJavascriptInterface(new  AndroidAndJSInterface(),"Android");

    //加载本地资源       
    webView.loadUrl("file:///android_asset/JavaAndJavaScriptCall.html");

    //显示页面
    // setContentView(webView);
}
```

### JAVA 调用 Javascript  
> java调用js原理就是Java代码调用了Js里面的函数。

#### 核心Java
```
//登录功能里，java代码调用了js里面的JavaCallJs函数实现将name传到JS中，这样JS页面可以显示该用户名了。
private void login(String name) {
    webView.loadUrl("javascript:javaCallJs(" + "'" + name + "'" + ")");
    setContentView(webView);
}
```

#### 核心js
```html
<!-- 上面Java核心代码执行将调用下面JS代码 -->
 <script type="text/javascript">
    function javaCallJs(arg){
         document.getElementById("content").innerHTML =
             ("欢迎："+arg );
    }
</script>
```

### JavaScript 调用 JAVA

#### 1.在初始化webview代码中配置Javascript接口
```java
//设置支持js调用java，调用时候将执行第一个参数的接口类
webView.addJavascriptInterface(new AndroidAndJSInterface(),"Android");  
//第二个参数("android")为执行接口类方法的标示，与js相呼应
```

#### 2.在该Activity中实现Javascript接口类
```
/**
 * js可以调用该类的方法
 */
class AndroidAndJSInterface{
    @JavascriptInterface
    public void showToast(){
        Toast.makeText(JavaAndJSActivity.this, "我被js调用了", Toast.LENGTH_SHORT).show();
    }
}
```

#### 3. JavaScript中调用java
```html
<input type="button" value="点击Android被调用" onclick="window.Android.showToast()" />
```

###### 执行流程

点击js页面的button，将执行js的onclick方法（onclick=”window.Android.showToast()”），根据该Android标示与webview配置接口方法的第二个参数相匹配，然后执行js接口实现类的showToast()方法。从而实现js代码调用java代码。








```
// 先假设id参数为content
Stirng elementId = "content";
String jsCode = "javascript:document.getElementById(\" + elementId +\").innerHtml"; 
webView.evaluateJavascript(jsCode, new ValueCallback<String>() {
        @Override
        public void onReceiveValue(String html) {
            // ...
        }
    }); 
```
这种写法是固定的，但是方法参数比较多时就比较蛋疼了，拼凑方法名和多个参数是很烦人的，且容易出错，因而我们可以抽象出以下工具类：
```
/**
 * @Author horseLai
 * CreatedAt 2018/10/22 17:42
 * Desc: JS 代码执行器，包含通过WebView执行JS代码的通用方法。
 * Update:
 */
public final class JsExecutor {

    private static final String TAG = "JsExecutor";
    private JsExecutor() {
    }

    /**
     * JS方法不带参，且无返回值时用此方法
     *
     * @param webView
     * @param jsCode
     */
    public static void executeJsRaw(@NonNull WebView webView, @NonNull String jsCode) {
        executeJsRaw(webView, jsCode, null);
    }

    /**
     * JS方法带参，且有返回值时用此方法
     *
     * @param webView
     * @param jsCode
     * @param callback
     */
    public static void executeJsRaw(@NonNull WebView webView, @NonNull String jsCode, @Nullable ValueCallback<String> callback) {
        if (Build.VERSION.SDK_INT >= 19) {
            webView.evaluateJavascript(jsCode, callback);
        } else { 
            // 注意这里，这种方式没有直接的结果回调，不过可以迂回解决，比如我们可以
            // 执行JS的一个固定的方法，并传入类型参数，然后在JS方法中根据这个类型参
            // 数去匹配方法并执行，执行完成后再调用我们注入的相应回调方法将结果传回
            // 来，这样就可以解决结果回调问题了，如果要适配 Android 4.4 以下的版本则可以这么做。
            webView.loadUrl(jsCode);
        }
    } 

    /**
     * JS方法带参，且有返回值时用此方法
     *
     * @param webView
     * @param methodName
     * @param callback
     * @param params
     */
    public static void executeJs(@NonNull WebView webView, @NonNull CharSequence methodName, @Nullable ValueCallback<String> callback, @NonNull CharSequence... params) {

        StringBuilder sb = new StringBuilder();
        sb.append("javascript:")
                .append(methodName)
                .append("(");
        if (params != null && params.length > 0) {
            for (int i = 0; i < params.length; i++) {
                sb.append("\"")
                        .append(params[i])
                        .append("\"");
                if (i < params.length - 1)
                    sb.append(",");
            }
        }
        sb.append(");");
        Log.i(TAG, "executeJs: " + sb);
        executeJsRaw(webView, sb.toString(), callback);

    }

    /**
     * JS方法带参，且无返回值时用此方法
     *
     * @param webView
     * @param methodName
     * @param params
     */
    public static void executeJs(@NonNull WebView webView, @NonNull CharSequence methodName, @NonNull CharSequence... params) {
        executeJs(webView, methodName, null, params);
    } 
}


```