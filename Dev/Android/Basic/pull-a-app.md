
作者：陈小二来巡山   
来源：CSDN   
原文：https://blog.csdn.net/zang_chen/article/details/76677846   
版权声明：本文为博主原创文章，转载请附上博文链接！  

## 一、需求场景：
A应用拉起B应用的非主页面的某个页面，并且传值（一般是鉴权token值、type值以及其他参数值，本文仅仅以传递type值为例），B应用根据传递过来的不同的值启动不同的页面。


前期说明（主要针对B应用）：

1. Android开发一般页面分为启动页（SplashActivity）、引导页（GuideActivity）、活动闪屏页（ScreenActivity）、主页（MainActivity）、登录页（LoginActivity）以及其他页面。

2. Android开发主页（MainActivity）的启动模式一般设置为：android:launchMode=“singleTask”，只有设置了这种启动模式才能更好的避免重复的启动主页面以及退出页面顺序异常的问题。

3. 我们需要一个Activity的管理工具类，启动时添加Activity，销毁时移除Activity，并且可以提供几个方法方便我们调用：是否包含主页（MainActivity）的方法、获取栈顶Activity的方法等等。

## 二、实现过程
拉起第三方客户端有三种方式：**包名、ACTION、URL（博主推荐）**。

如果简简单单拉起一个B应用的某个页面那么可以通过ACTION和URL的方法，但是如果这样做总让人感觉哪里是不合理的。试想一下，你从A应用拉起一个B应用的非主页面的某个页面，点击返回，一下子返回到A应用了，感觉好突然有木有。如果拉起第三方客户端仅仅只是为了一个页面，还不如我们自己写个原生的页面算了，或者搞成SDK，这样岂不是可以节省好多资源撒。

>因此，真正的实现过程应该是

A应用拉起B应用的启动页（SplashActivity）并传值（token值和type值以及其他参数值），在启动页获取到值并且存储到SharedPreferences中，最好再存储一个Boolean值，代表这是从第三方应用拉起来的。然后有两种情况，通过Activity的管理工具类判断栈中是否含有B应用的主页面（即B应用是否已经运行在后台）

  - **不含有**：代表后台并没有运行B应用。那么我们正常启动主页面，在主页（MainActivity）从SharedPreferences中获取到这个Boolean值与A应用传递过来的值，由主页根据A应用传递过来的值打开相应的页面。这样用户点击返回顺序为：B应用相应页面&rarr;B应用主页面&rarr;A应用；

  - **含有**：代表B应用已经运行在后台，并且现在可能停留在某个页面。因此，我们不应该在启动页继续走启动主页面的逻辑了，如果继续启动主页面（由于设置了主页的启动模式为android:launchMode=“singleTask”），那么B应用栈中主页面以上页面都会出栈，用户将看不到刚刚浏览过的页面，这样太不友好了。因此此时的解决方案是我们要在启动页发个静态广播，在广播接收者中获取到SharedPreferences中的Boolean值与A应用传递过来的值，并且通过Activity的管理工具类获取到栈顶的Activity，然后在栈顶Activity的基础上启动相应的页面，（当然，这里也可以不发送广播，直接在启动页通过Activity的管理工具类获取到栈顶的Activity，然后在栈顶Activity的基础上启动相应的页面，这样效果是一样的）这样用户点击返回的顺序为：B应用相应页面&rarr;B应用用户拉起客户端之前浏览的页面&rarr;B应用主页面&rarr;A应用。

 这样既能跳转到B应用中我们应该跳转的页面，还可以使用B应用其他的功能，也就是说可以正常使用B应用，并且返回的顺序也是合理的，这样才算真正的拉起第三方应用。
 
**注意：**我所描述的栈顶Activity在实际应用中其实并不是真正的栈顶Activity，因为目前栈顶Activity应该是启动页（SplashActivity），并不是用户在拉起客户端之前浏览的页面，我们的目的就是获取到用户在拉起客户端之前浏览的页面，所以Activity的管理工具类应该提供一个获取栈顶下方的第一个Activity方法，因为这个Activity才是用户在拉起客户端之前浏览的页面。切记！！！—其实经过本人亲测，由启动页（SplashActivity）而非用户在拉起客户端之前浏览的页面，打开相应页面时，效果看起来其实是相同的，只是感觉在逻辑上有点别扭，所以本人还是强烈建议最好还是获取到真正的用户在拉起客户端之前浏览的页面，在此页面基础上打开相应页面，这样逻辑上才是最合理的。

## 三、实现方法

### 3.1 前提  
根据包名判断手机设备是否已经安装了B应用：如果未安装-走下载安装逻辑；如果已安装-拉起。

> 根据包名判断手机设备是否已经安装了B应用方法如下

```java
public static boolean isApkInstalled(Context context, String packageName) {
    if (TextUtils.isEmpty(packageName)) {
        return false;
    }
    try {
        ApplicationInfo info = context.getPackageManager().getApplicationInfo(packageName, PackageManager.GET_UNINSTALLED_PACKAGES);
        return true;
    } catch (NameNotFoundException e) {
        e.printStackTrace();
        return false;
    }
}
```

### 3.2 拉起方法
#### 3.2.1 包名
B应用不需要任何配置即可被拉起：

  - 第一种：包名  
  ```java
  Intent intent = getPackageManager().getLaunchIntentForPackage("com.pull.csd");
    if (intent != null) {
        intent.putExtra("type", "110");
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
    }
  ```
  - 第二种：包名+启动页所在项目位置（清单文件Activity配置中android:name所声明的全路径）
  ```java
  ComponentName componentName = new ComponentName("com.pull.csd", "com.pull.csd.SplashActivity");
    Intent intent = new Intent();
    intent.setComponent(componentName);
    intent.putExtra("type", "110");
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    startActivity(intent);
  ```

#### 3.2.2 ACTION
> B应用清单文件需要配置

在启动页（SplashActivity）清单文件增加如下配置

```xml
<!--ACTION启动配置-->
<intent-filter>
    <action android:name="CSD" />
    <category android:name="android.intent.category.DEFAULT" />
</intent-filter>
``` 
**注意：**    
不要在原有的intent-filter中增加代码，而是在原有intent-filter下方再增加一个intent-filter。 

> A 应用两种编码方式

  - 第一种：ACTION字符串
```java
Intent intent = new Intent();
    intent.setAction("CSD");
    intent.putExtra("type", "110");
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    startActivity(intent);
```
  - 第二种：ACTION字符串+包名+启动页所在项目位置（清单文件Activity配置中android:name所声明的全路径）
```java
ComponentName componentName = new ComponentName("com.pull.csd", "com.pull.csd.SplashActivity");
    Intent intent = new Intent();
    intent.setAction("CSD");
    intent.setComponent(componentName);
    intent.putExtra("type", "110");
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    startActivity(intent);
```

**注意：**  
A应用代码中的ACTION字符串必须与B应用清单文件配置的ACTION字符串完全匹配才会成功拉起。

#### 3.2.3 URL
这种方式同样适用于HTML中的a标签链接拉起B应用。
> B应用清单文件需要配置

在启动页（SplashActivity）清单文件增加如下配置
```xml
<!--URL启动启动配置-->
<intent-filter>
    <data
        android:host="pull.csd.demo"
        android:path="/cyn"
        android:scheme="csd" />
    <action android:name="android.intent.action.VIEW" />

    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
</intent-filter>
```            
**注意：**  
1. 不要在原有的intent-filter中增加代码，而是在原有intent-filter下方再增加一个intent-filter。  
2. 这里scheme为必填，host、path为选填。选填内容可以不填，但是一旦填上了就必须全部完全匹配才会成功拉起。

> A 应用编码方式

```java
Intent intent = new Intent();
intent.setData(Uri.parse("csd://pull.csd.demo/cyn?type=110"));
intent.putExtra("", "");//这里Intent当然也可传递参数,但是一般情况下都会放到上面的URL中进行传递
intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
startActivity(intent);
```
B应用启动页拉起后可以获取到Uri，你可以选择先存储到SharedPreferences中，在主页或者广播接收者中取出来，然后再对URI进行解析；或者在启动页立刻将Uri解析成bean对象，放到全局的Application中，在主页或者广播接收者中直接使用。

> B 应用的启动页（SplashActivity）中解析示例

```java
Intent intent = getIntent();
Uri uri = intent.getData();
if (uri != null) {
    String scheme = uri.getScheme();//csd
    String uriHost = uri.getHost();//pull.csd.demo
    String uriPath = uri.getPath();///cyn
    String type = uri.getQueryParameter("type");//110
}
```
如果存储到SharedPreferences中那么一定是把Uri转换成String类型了，下面是你可能会用到的把String转成Uri类型的方法。
```java
Uri uri = Uri.parse(url);
```
**切记：**  
A应用拉起B应用的编码千万不要忘记添加： `intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);`
如果不添加你会发现有时候返回顺序是混乱的。

> 举个例子

如果你在浏览B应用的M页面（从B应用主页面进入的），点击HOME键退出，你打开了A应用，从A应用拉起了B应用的N页面。
此时我们需要的合理友好的的返回顺序应该是：B应用的N页面-B应用的M页面-B应用主页-A应用-桌面，但是你会发现你返回的顺序是：B应用的N页面-A应用-B应用的M页面-B应用主页-桌面。
关于启动模式的相关问题大家可以自行百度，相关文章一搜一大把。

另外，博主强烈推荐拉起第三方APP的需求尽量采用URL拉起方式，原因有两个：
  1. 不必暴露第三方应用的包名与类名；
  2. 博主发现一个特别巨大的问题，而这个问题只有URL启动方式可以避免。通过包名或者ACTION拉起时假如B应用已经运行在后台，然后你再次在A应用中将其拉起，此时你会发现的确拉起了B应用，但是页面还是刚刚点击HOME键退出前的页面，所有页面的所有生命周期都没有触发，也因此并不会走你准备好的跳转到相应页面的逻辑，而URL却是正常的会走相应页面的生命周期。
  
问题场景假设：A应用登陆成功后将鉴权token传递给B应用，然后点击Home键退出B应用再打开A应用，在A应用切换用户以后再次拉起B应用，此时你会发现B应用的所有数据信息还是上一个用户的数据信息，懵逼不？？？

综上所述，博主强烈推荐拉起第三方的APP的需求尽量采用URL拉起方式。

## CODE
 - [拉起APP](https://github.com/zang-chen/lqkhd.git)
 - [被拉起APP](https://github.com/zang-chen/pull.git)

## 写在最后
有些细节还是需要大家去自行处理的，例如：引导页与活动闪屏页的开启逻辑对我们拉起客户端的逻辑如果有影响该如何处理、登录页面如果对我们拉起客户端的逻辑有影响改如何处理（特别是登陆后该如何正确跳转页面刷新数据）等等。
