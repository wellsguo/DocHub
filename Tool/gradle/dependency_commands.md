## gradle


| 2.x             | 3.x                  | 
| ---             | ---                  |  
| Complie         | implementation / api |
| provided        | compile only         |
| apk             | runtime only         |
| Test Compile    | Test implementation  |
| Debug compile   | Dubug implementation |
| Release compile | Release implementation |

### 1. implementation vs. compile  
implementation：只能在内部使用此模块，比如一个 libiary 中使用 implementation 依赖了 gson 库，然后主项目依赖了 libiary，那么，主项目将无法访问 gson 库中的方法。这样的好处是编译速度会加快，推荐使用 implementation 的方式去依赖，如果你需要提供给外部访问，那么就使用api依赖即可.

### 2. api / compile

这是最常用的方式，使用该方式依赖的库将会参与**编译**和**打包**。  
当我们依赖一些第三方的库时，可能会遇到 com.android.support 冲突的问题，就是因为开发者使用的 compile 依赖的 com.android.support 包，而他所依赖的包与我们本地所依赖的 com.android.support 包版本不一样，所以就会报 All com.android.support libraries must use the exact same version specification (mixing versions can lead to runtime crashes 这个错误。

### 3. compileOnly / provided
只在编译时有效，不会参与打包。  
可以在自己的 moudle 中使用该方式依赖一些比如 com.android.support，gson 这类开发者常用的库，避免冲突。

### 4. runtimeOnly / apk
只在生成 apk 的时候参与打包，编译时不会参与，**很少用**。

### 5. testImplementation / testCompile
testCompile 只在单元测试代码的编译以及最终打包测试 apk 时有效。

### 6. debugImplementation/ debugCompile
debugCompile 只在 debug 模式的编译和最终的 debug apk 打包时有效

### 7. releaseImplementation / releaseCompile
Release compile 仅仅针对Release 模式的编译和最终的 Release apk 打包。
