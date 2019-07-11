### 使用 HTTP Client
> Android 6.0不再支持 Apache HTTP client， 建议使用 HttpURLConnection 代替。如果还想要继续使用 Apache HTTP client 的，请在build.gradle中添加下面的代码

```
android {
    useLibrary 'org.apache.http.legacy'
}
```

### 打包 .so 
> 在 Eclipse 中, 将 .so 文件放入 libs 目录里，可以被打包到 apk 中。但是在 Android Studio 中，如果将 .so 文件放在 libs 目录里，是不会被打包到 apk 中的，只有 jniLibs 目录里的 .so 文件会被打包到 apk 中，当然这个目录指定的文件夹可以更改，但是默认就是 \src\main\jniLibs .

> Android Studio 开发的推荐做法是，把 .so 文件放在 libs 目录下，但需要去重新指定 jniLibs 目录对应的文件夹

```
sourceSets {
    main {
        jniLibs.srcDirs = ['libs']
    }
}
```


## build.gradle



> Android Studio 这么强大的工具，就算我们不懂 gradle, groovy， 也照样能借助 AS 对 Android 项目进行编译、调试、运行、打包等操作。其根本就在 Android Studio 自己生成了build.gradle 文件。Android Stdutio 中的 Android 项目有两类 build.gradle 文件，一是项目级 build.gradle， 二是模块级 build.gradle。

### 1. 项目级 build.gradle
```
// Top-level build file where you can add configuration options common to all sub-projects/modules.
apply from: "config.gradle"

buildscript {
    
    repositories {  // repositories闭包
        google()
        jcenter() // 代码托管库：设置之后可以在项目中轻松引用jcenter上的开源项目
    }
    dependencies {  // dependencies闭包
        classpath 'com.android.tools.build:gradle:3.0.0' //// 声明gradle插件，插件版本号为3.0.0
        // gradle是一个强大的项目构建工具，不仅可以构建Android，还可以构建java，C++等
        // 此处引用android的插件
        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}
 
allprojects {
    repositories {
        google()
        jcenter() // 代码托管库：设置之后可以在项目中轻松引用jcenter上的开源项目
    }
}
 
task clean(type: Delete) {
    delete rootProject.buildDir
}
```

### 2. 模块级 build.gradle
```
//Model都有各自的build.gradle，这里声明该Model作为主项目，常见的还有另一个取值：
//apply plugin: 'com.android.library' 声明该Model作为库使用，当然还有其他取值，后面博客会介绍
apply plugin: 'com.android.application'

//这里是在as里引入一个retrolambda插件，具体我也不大懂，可以看看这篇博客： 
//http://blog.csdn.net/zhupumao/article/details/51934317?locationNum=12
apply plugin: 'me.tatarka.retrolambda'

//这里是groovy的代码了，定义了一个获取时间的方法，groovy是兼容java，它可以直接使用jdk里的方法
def releaseTime() {
    return new Date().format("yyyy-MM-dd", TimeZone.getTimeZone("UTC"))
}

//file()是Project.java里的一个方法，这里定义一个File类型的对象，Project后面博客会介绍到
def keyStore = file('meizhi.keystore')

android {

    //这个大家应该很熟悉了，有疑问的应该是后面的代码，这里表示获取一些全局变量
    //这些变量的值在根目录下的build.gradle中定义，具体可以看看这篇博客：
    //http://blog.csdn.net/fwt336/article/details/54613419
    compileSdkVersion rootProject.ext.android.compileSdkVersion
    buildToolsVersion rootProject.ext.android.buildToolsVersion

    //同理，这里都是通过获取全局设置的变量值来进行相关配置，这样做的好处在于当
    //你的项目里有多个model时，可以方便修改这些公共的配置，只需要修改一个地方就可以同步了
    defaultConfig {
        applicationId rootProject.ext.android.applicationId
        minSdkVersion rootProject.ext.android.minSdkVersion
        targetSdkVersion rootProject.ext.android.targetSdkVersion
        versionCode rootProject.ext.android.versionCode
        versionName rootProject.ext.android.versionName
    }

    //这里应该是设置打包后的apk里的META-INF移除指定的文件吧
    packagingOptions {
        exclude 'META-INF/DEPENDENCIES.txt'
        //省略部分exclude 代码...
    }

    //关闭指定的lint检查
    lintOptions {
        disable 'MissingTranslation', 'ExtraTranslation'
    }

    //lint检查到错误时不中断编译，好像是说lint检查是为优化代码，发现的错误其实并不会导致程序异常
    //所以有的时候及时发现Lint检查错误还是可以直接运行查看效果
    lintOptions {
        abortOnError false
    }

    //签名的相关配置
    signingConfigs {
        //这个标签名可以随意命名，这里的作用大概类似于定义一个对象，该对象里设置好了签名需要的各种配置
        //可以定义不止一种配置的签名对象，例如常见的还有 debug{...}, release{...}，然后在buildTypes{}里
        //通过 signingConfigs.app1 进行调用
        app1 {
            //签名的相关配置，网上资料很多，STOREPASS, KEYALIAS, KEYPASS 这些常量是定义在
            //gradle.properties 文件里，如果没有该文件手动创建即可，这样可以保证安全
            //只有定义在 gradle.properties 里的常量才可以直接通过常量名引用
            storeFile file('meizhi.keystore')
            storePassword project.hasProperty('STOREPASS') ? STOREPASS : ''
            keyAlias project.hasProperty('KEYALIAS') ? KEYALIAS : ''
            keyPassword project.hasProperty('KEYPASS') ? KEYPASS : ''
        }
    }

    //编译，打包的项目配置
    buildTypes {

        debug {
            //在 BuildConfig 里自定义一个 boolean 类型的常量
            //更多资料可以查看：http://stormzhang.com/android/2015/01/25/gradle-build-field/ 
            buildConfigField "boolean", "LOG_DEBUG", "true"
            
            debuggable true
            applicationIdSuffix ".debug"
        }

        release {
            buildConfigField "boolean", "LOG_DEBUG", "false"

            debuggable false
            
            //开启混淆
            minifyEnabled true
            //删除无用的资源
            shrinkResources true
            //混淆文件
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            if (keyStore.exists()) {
                println "Meizhi: using drakeet's key"
                //根据在signingConfigs.app1里的签名配置进行签名
                signingConfig signingConfigs.app1
            } else {
                println "Meizhi: using default key"
            }

            //这段代码应该会在大神的项目里挺常见的，我在很多项目里都看见过了
            //这也是groovy的代码，这里的代码作用是重命名最后打包出来的apk
            //根据 def fileName 设置的格式来命名，${}表示的是某个变量的引用
            //例如根据设置的格式最后apk命名可能是： Meizhi_v1.0.0_2017-03-28_fir.apk
            //至于 applicationVariants 这些变量含义后面博客会介绍
            applicationVariants.all { variant ->
                variant.outputs.each { output ->
                    def outputFile = output.outputFile
                    if (outputFile != null && outputFile.name.endsWith('.apk')) {
                        def fileName = "Meizhi_v${defaultConfig.versionName}_${releaseTime()}_${variant.productFlavors[0].name}.apk"
                        output.outputFile = new File(outputFile.parent, fileName)
                    }
                }
            }
        }

        //这里的作用跟 singingConfigs 差不多，只是为不同的 flavor 设置一些属性
        //常见的设置比如设置不同的渠道编号，设置不同的 api 服务器等等
        productFlavors {
            fir {
                //这个的作用是将 AndroidManifest.xml 里的占位符 ￥{UMENG_CHANNEL_VALUE} 的值替换成fir
                manifestPlaceholders = [UMENG_CHANNEL_VALUE: "fir"]
            }
            GooglePlay {
                manifestPlaceholders = [UMENG_CHANNEL_VALUE: "GooglePlay"]
            }
            Umeng {
                manifestPlaceholders = [UMENG_CHANNEL_VALUE: "Umeng"]
            }
        }
    }

    //设置JDK的版本通过compileOptions
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    //lint的相关配置吧
    lintOptions {
        disable "InvalidPackage"
        lintConfig file("lint.xml")
    }
}

//这里就不用说了
dependencies {
    compile fileTree(dir: 'libs', include: ['*.jar'])
    compile project(":libraries:headsupcompat")
    compile project(":libraries:smooth-app-bar-layout")
    //as默认会去下载传递依赖，下面是指定不需要去下载传递依赖
    compile ('com.squareup.retrofit2:retrofit:2.1.0') {
        exclude module: 'okhttp'
    }
    retrolambdaConfig 'net.orfjackal.retrolambda:retrolambda:2.3.0'
    //省略部分compile代码...
}
```


