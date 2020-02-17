Android aar Packgets Management Based on Maven



## 前言

在日常的项目开发中，尤其是 Android 组件化/模块化 开发的盛行，常常需要开发一些公共组件，公共模块，和基于公司特殊需求的SDK。而这些资源又被多个项目同时使用，要实现这些公用资源的统一使用和管理，一般有以下三种做法：

1. 整个 module 导入工程。如果 module 中有什么 bug 或新的需求，修改了还要其他项目再重新添加进去，很不方便。

2. 将 module 打包 AAR，在具体的项目引用添加。如果有什么 bug 或新的需求，修改了重新发给其他项目成员重新更新。

3. 使用 Gradle Add Libay 的方式。类似 `implementation 'com.android.support:appcompat-v7:27.1.1'` 的方式来引用我们的 module，如果有变更，修改人直接重新上传 module，使用方修改版本号，重新 bulid 就可以更新 module。==（**强烈推荐**）==




## 实战：打包到本地 Maven 仓库


1. 在 `module` 根目录下面，新建并编辑 `maven-release-aar.gradle` 文件。

```groovy
apply plugin: 'maven'

ext{
    PUBLISH_GROUP_ID = "com.kys"
    PUBLISH_ARTIFACT_ID = "utils"
    PUBLISH_VERSION = "1.0"
}


uploadArchives{
    repositories.mavenDeployer{
        // aar 文件输出的最终目录
        // 如果是存放在本地请注意路径是 file://{absolute_path}
        repository(url:"file:///Users/adamsguo/Desktop/maven/aar")

        pom.project{
            groupId project.PUBLISH_GROUP_ID
            artifactId project.PUBLISH_ARTIFACT_ID
            version PUBLISH_VERSION
        }
    }
}

// 生成 jar 源码包，不想让其他人看到源码可以注释掉
task androidSourceJar(type: Jar){
    classifier = 'source'
    from android.sourceSets.main.java.sourceFiles
}

artifacts{
    archives androidSourceJar
}
```


2. 在 library 的 build.gradle 引入打包配置文件。

```grrovy
apply from:'maven-release-aar.gradle'
```


3. 配置完成后，同步项目，此时在 `gradle 侧边栏`看到 `upload` 选项，运行 `uploadArchives`即可。
   
   执行完后就可以在 `Users/adamsguo/Desktop/maven/aar`(*{maven_local_repository_absolute_path}*) 目录下可以看到生成的 aar 文件。

4. 在新项目中的 `build.gradle` 文件，进行相应的配置，就可以调用 Maven 本地仓库的 aar 包。

```groovy
respositories{
    jcenter()
    
    // 本地 maven 仓库绝对路径
     maven{
       url "file:///Users/adamsguo/Desktop/maven/aar"
     }
}

dependencies{
    // ....
  
    // 注意后面的两个冒号
    implementation 'com.kys:utils:1.0'
}
```


### 注意事项

在上面的仓库配置中使用的是

```groovy
    repository(url:"file:///Users/adamsguo/Desktop/maven/aar")
```

这样打包的 aar 仅存在于本地，只能供本人使用，其他人是无法访问的。因此需要搭建一个 Maven 私服管理平台来完成团队间的共享。


----

https://blog.csdn.net/xiaxiayige/article/details/80636091

## 实战：打包到私服 Maven 仓库


###  第一步：安装Maven私服管理平台 Nexus
1. 下载安装 [nexus](https://www.sonatype.com/download-oss-sonatype)；

2. 在安装的目录 (*{nexus_install_path}\bin*) 下执行 `nexus.exe /run` 运行 nexus；

3. 进入配置目录 (*{nexus_install_path}\etc*) 按需修改 `nexus-default.properties` 配置文件；

4. 访问 http://127.0.0.1:8081 ，然后右上角登录，`账号默认 admin 密码 admin123`。


到此完成了 nexus 的安装，有了管理 maven 仓库的这样一个平台。

### 第二步：配置 Gradle

配置方法与 [实战：打包到本地 Maven 仓库]() 基本相同。仅需要修改 `repository` 配置 

```groovy
repository(url: 'http://127.0.0.1:8081/repository/maven-releases/') {
        authentication(userName: 'admin', password: 'admin123')
    }
```

#### 注意

```groovy
implementation 'com.kys:utils:1.0.0@aar'
```

在使用aar时 `graoupId:artifactId:version` 这里注意需要后面跟上 `@aar`,如果不跟上这个默认是去加载`.jar`的文件，就会出现找不到的情况，怎么样可以不加？

在配置文件中指明 pom 的 `packaging` 类型即可。

```groovy
apply plugin:'maven'

uploadArchives {
    configuration = configurations.archives
    repositories {
        mavenDeployer {
            repository(url: 'http://127.0.0.1:8081/repository/maven-releases/') {
                authentication(userName: 'admin', password: 'admin123')
            }
            pom.project {
                version '1.1.0'
                artifactId 'utils'
                groupId 'com.kys'
                packaging 'aar'
                description 'update version 1.1.0'
            }
        }
    }
}
```
