## 下载地址

https://studygolang.com/dl

## 解压拷贝

```sh
tar -xzf go1.8.linux-amd64.tar.gz  -C /usr/local
# verify
/usr/local/go/bin/go version
```

## 设置环境变量

### 单用户

> 添加环境变量

```
sudp gedit ~/.bashrc
```

```
# text 
export GOPATH=/opt/go
export GOROOT=/usr/local/go
export GOARCH=386
export GOOS=linux
export GOBIN=$GOROOT/bin/
export GOTOOLS=$GOROOT/pkg/tool/
export PATH=$PATH:$GOBIN:$GOTOOLS
```

> 重载profile

```
source ~/.bashrc
```

### 多用户[推荐]

```
vim /etc/profile
```

```
export GOPATH=/home/www/golang/gopath 
export GOROOT=/usr/local/go
export GOARCH=386
export GOOS=linux
export GOTOOLS=$GOROOT/pkg/tool
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```

> 重载 profile

source /etc/profile

## 测试

### 测试代码
```go
package main
import "fmt"
func main() {
    fmt.Println("Hello World!")
}
```

### 执行

#### (1) go run 运行

```
go run hello.go 
# Hello World!
```

#### (2) go build 生成可执行文件

```
go build hello.go 
ls
# hello  hello.go
./hello
# Hello World!
```

#### (3) go env

> go env

```
GOARCH="386"
GOBIN=""
GOEXE=""
GOHOSTARCH="amd64"
GOHOSTOS="linux"
GOOS="linux"
GOPATH="/home/www/golang/gopath"
GORACE=""
GOROOT="/usr/local/go"
GOTOOLDIR="/usr/local/go/pkg/tool/linux_amd64"
GCCGO="gccgo"
GO386="sse2"
CC="gcc"
GOGCCFLAGS="-fPIC -m32 -fmessage-length=0 -fdebug-prefix-map=/tmp/go-build103397464=/tmp/go-build -gno-record-gcc-switches"
CXX="g++"
CGO_ENABLED="0"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
```

**GOPATH路径，需动手创建：mkdir -p /home/www/golang/gopath**

##### 变量说明：

> GOROOT

go的安装路径

> GOPATH 

编译后二进制的存放目的地和import包时的搜索路径 (其实也是你的工作目录)

###### GOPATH 目录结构

```
goWorkSpace // (goWorkSpace为GOPATH目录)
  -- bin    // golang编译可执行文件存放路径，可自动生成。
  -- pkg    // golang编译的.a中间文件存放路径，可自动生成。
  -- src    // 源码路径。按照golang默认约定，go run，go install等命令的当前工作路径（即在此路径下执行上述命令）。
```
GOPATH之下主要包含三个目录: bin、pkg、src   
（1）bin 目录主要存放可执行文件;  
（2）pkg 目录存放编译好的库文件, 主要是\*.a文件;  
（3）src 目录下主要存放go的源文件  
（4）GOPATH可以是一个目录列表, go get下载的第三方库, 一般都会下载到列表的第一个目录里面  
（5）需要把GOPATH中的可执行目录也配置到环境变量中, 否则你自行下载的第三方go工具就无法使用了, 操作如下:   
（6）GOBIN go install编译存放路径。不允许设置多个路径。可以为空。为空时则遵循“约定优于配置”原则，可执行文件放在各自GOPATH目录的bin文件夹中（前提是：package main的main函数文件不能直接放到GOPATH的src下面


## 获取远程包
   go语言有一个获取远程包的工具就是`go get`，目前go get支持多数开源社区(例如：github、googlecode、bitbucket、Launchpad)

	go get github.com/astaxie/beedb
	
>go get -u 参数可以自动更新包，而且当go get的时候会自动获取该包依赖的其他第三方包	

通过这个命令可以获取相应的源码，对应的开源平台采用不同的源码控制工具，例如github采用git、googlecode采用hg，所以要想获取这些源码，必须先安装相应的源码控制工具

通过上面获取的代码在我们本地的源码相应的代码结构如下

	$GOPATH
	  src
	   |--github.com
			  |-astaxie
				  |-beedb
	   pkg
		|--相应平台
			 |-github.com
				   |--astaxie
						|beedb.a

go get本质上可以理解为首先第一步是通过源码工具clone代码到src下面，然后执行`go install`

在代码中如何使用远程包，很简单的就是和使用本地包一样，只要在开头import相应的路径就可以

	import "github.com/astaxie/beedb"

## 程序的整体结构
通过上面建立的我本地的 mygo 的目录结构如下所示

	bin/
		mathapp
	pkg/
		平台名/ 如：darwin_amd64、linux_amd64
			 mymath.a
			 github.com/
				  astaxie/
					   beedb.a
	src/
		mathapp
			  main.go
		mymath/
			  sqrt.go
		github.com/
			   astaxie/
					beedb/
						beedb.go
						util.go

从上面的结构我们可以很清晰的看到，bin目录下面存的是编译之后可执行的文件，pkg下面存放的是应用包，src下面保存的是应用源代码



