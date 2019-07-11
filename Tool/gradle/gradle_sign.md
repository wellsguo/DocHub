## build.gradle 之 buildTypes 

### buildTypes {} 封装此项目的所有构建类型配置

```groovy
buildTypes {
       debug {
       }
       release {
           debuggable false
           zipAlignEnabled true
           minifyEnabled true
           proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
       }
   }
```   
下面来说说 `buildTypes` 里面各项的的常见属性：

类型 | 属性 |	描述
 -- | -- | --
boolean| debbuggable|	该构建类型是否生成一个可调式的apk
boolean| minifyEnabled	|是否可以移出无用的java代码，默认为false
Boolean| multiDexEnabled|	是否可以分包
File| multiDexKeepFile|	指定放在main dex内的类，如果设置则它的格式为一个类一行：com/example/MyClass.class
File| multiDexKeepProguard	|指定用在main dex 的类上的混淆文件，跟系统混淆文件联合使用
String| name	|这种构建类型的名称
|proguardFiles|	指定插件使用的混淆文件
SigningConfig |signingConfig|	签名配置文件
boolean| zipAlignEnabled|	是否使用zipAlign优化apk,Android sdk包里面的工具，能够对打包的应用程序进行优化，让整个系统运行的更快
String |versionNameSuffix	|VersionName的后缀
常见方法
DefaultBuildType initWith(BuildType that)
使用方法如下：
```groovy
android.buildTypes {
    customBuildType {
        initWith debug
            // customize...
        }
}   //复制所有debug里面的属性
```
以上只是常用的一些属性方法，如要了解更多可从以下[网址](http://google.github.io/android-gradle-dsl/current/index.html)了解.

### show case

```groovy
buildTypes {
    //正式
    release {
        buildConfigField "boolean", "IS_DEBUG", "false"  // 自定义数据类型
        buildConfigField "String", "buildTime", "\"" + releaseTime() + "\""
        buildConfigField "int", "URL_CONFIG", "" + getUrl(2) + ""
        //混淆
        minifyEnabled true
        //Zipalign优化
        zipAlignEnabled true
        // 移除无用的resource文件
        shrinkResources false
        proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    }
}
``` 
###### AppConfig.java

```java
    private void initARouter(){
        if (BuildConfig.IS_DEBUG) {
            //打印日志
            ARouter.openLog();
            //开启调试模式(如果在InstantRun模式下运行，必须开启调试模式！线上版本需要关闭,否则有安全风险)
            ARouter.openDebug();
        }
        //推荐在Application中初始化
        ARouter.init(Utils.getApp());
    }
``` 

## Gradle 配置签名信息
作者：Amy_LuLu\_\_  
链接：https://www.jianshu.com/p/f52aef25f1a4  
来源：简书   
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。  


### 1.配置签名信息

> 编辑app/build.gradle文件

在android闭包中添加以下内容

```
android {
  ...
  signingConfigs{
      config{ //配置keystore文件的各种信息
          storeFile file('/Users/apple/Desktop/androddemo/haha.jks') //指定keystore文件的位置
          storePassword '123456' //密码
          keyAlias 'key' //别名
          keyPassword '123456' //别名密码
      }
  }
  ...
}
```

### 2.应用配置
即在生成正式版APK的时候去应用这个配置

> 编辑app/build. gradle文件

```
android {
  ...
    buildTypes {
        release {
            minifyEnabled false 
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.config //应用刚才添加的签名配置
            //则生成正式版APK的时候就会自动使用我们刚才配置的签名信息来进行签名了。
        }
    }
  ...
}
```

### 3. 配置 gradle.properties

#### 3.1.在gradle.properties中存放敏感数据
AS项目的根目录下有一个 gradle.properties 文件， 专门用来配置全局键值对数据的。

> gradle.properties中添加以下内容：

```groovy
KEY_PATH=/Users/apple/Desktop/androddemo/haha.jks
KEY_PASS=123456
ALIAS_NAME=key
ALIAS_PASS=123456
```

#### 2.在build.gradle中读取数据
> 编辑app/build.gradle

```groovy
android {
  ...
  signingConfigs{
      config{ //配置keystore文件的各种信息
            storeFile file(KEY_PATH)
            storePassword KEY_PASS
            keyAlias ALIAS_NAME
            keyPassword ALIAS_PASS
      }
  }
  ...
}
```

## AndroidStudio获取开发版和发布版的SHA1值

![](https://upload-images.jianshu.io/upload_images/2851519-d58abc4ec9b25b25.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/415/format/webp)


