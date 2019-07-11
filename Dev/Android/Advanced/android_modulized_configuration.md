## Android 模块化（二）：可插拔模块化配置 

模块化的好处之一——**模块可以独立的开发编译运行**安装到用户的手机上，这样就方便了对某一模块的单独开发调试，单一模块生成的apk体积也小，编译时间也快，开发效率会高很多。

### 1. 项目根模块配置

> gradle.properties

```
# 是否需要单独编译 true表示不需要，false表示需要
isNeedHomeModule=true
#isNeedHomeModule=false
isNeedChatModule=true
#isNeedChatModule=false
isNeedRecomModule=true
#isNeedRecomModule=false
isNeedMeModule=true
#isNeedMeModule=false
```

### 2. 模块中配置

> module_me.gradle

```
if (!isNeedMeModule.toBoolean()) {
    apply plugin: 'com.android.application'
} else {
    apply plugin: 'com.android.library'
}

defaultConfig {
    if (!isNeedMeModule.toBoolean()) {
        applicationId "tsou.cn.module_me"
    }
}
```

### 3. app 主模块配置

> app.gradle

```
if (isNeedHomeModule.toBoolean()) {
    compile project(':module_home')
}
if (isNeedChatModule.toBoolean()) {
    compile project(':module_chat')
}
if (isNeedRecomModule.toBoolean()) {
    compile project(':module_recom')
}
if (isNeedMeModule.toBoolean()) {
    compile project(':module_me')
}
```

### 4 单模块调试运行

> 例如单独运行 **module_home** 模块

#### 4.1 开启 isNeedHomeModule=false

#### 4.2 AndroidManifest 配置启动项

##### 方式一：手动法  

在 AndroidManifest.xml 的 MainActivity 添加  

```xml
<intent-filter>
    <action android:name="android.intent.action.MAIN" />

    <category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```
如果要作为依赖库运行时则手动注释掉即可。但是比较low，对程序员不够友好。

##### 方式二：通过 build 自动配置

###### (1) src/main/AndroidManifest.xml 不变
  
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="tsou.cn.module_home">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
        </activity>
    </application>

</manifest>
```

###### (2) 新建 src/debug/AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="tsou.cn.module_home">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

###### (3) 在子模块的build中配置

```groovy
android {
    ...

    sourceSets {
        main {
            if (!isNeedHomeModule.toBoolean()) {
                manifest.srcFile 'src/debug/AndroidManifest.xml'
            } else {
                manifest.srcFile 'src/main/AndroidManifest.xml'
                java {
                    //全部Module一起编译的时候剔除debug目录
                    exclude '**/debug/**'
                }
            }
        }
    }
}
```
