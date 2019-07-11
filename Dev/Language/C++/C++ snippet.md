## C、C++ 开发运行平台及编译器判断

C++ 编写跨平台程序的关键，C/C++中的内置宏定义分两部分：
 
操作系统 | 宏
-- | -- 
Windows|   WIN32
Linux|  linux
Solaris|   __sun
 
编译器判定| 宏
-- | -- 
VC|  _MSC_VER
GCC/G++|   \_\_GNUC\_\_
SunCC|   \_\_SUNPRO\_C和\_\_SUNPRO\_CC


```c++
#include <stdio.h>
#include <iostream>
 
using namespace std;
 
int main(int argc,char **argv){
 
    int no_os_flag=1;

    #ifdef linux
       no_os_flag=0;
       cout<<"It is in Linux OS!"<<endl;
    #endif

    #ifdef _UNIX
       no_os_flag=0;
       cout<<"It is in UNIX OS!"<<endl;
    #endif
 
    #ifdef __WINDOWS_
       no_os_flag=0;
       cout<<"It is in Windows OS!"<<endl;
    #endif

    #ifdef _WIN32
       no_os_flag=0;
       cout<<"It is in WIN32 OS!"<<endl;
    #endif

    if(1==no_os_flag){
        cout<<"No OS Defined ,I do not know what the os is!"<<endl;
    }

    return 0;
}
```


### [more](https://github.com/itas109/OSPlatformUtil/blob/master/src/osplatformutil.h)
```C++
#ifndef OSPLATFORMUTIL_H
#define OSPLATFORMUTIL_H

/*
   The operating system, must be one of: (I_OS_x)
     DARWIN   - Any Darwin system (macOS, iOS, watchOS, tvOS)
	 ANDROID  - Android platform
	 WIN32    - Win32 (Windows 2000/XP/Vista/7 and Windows Server 2003/2008)
	 WINRT    - WinRT (Windows Runtime)
	 CYGWIN   - Cygwin
	 LINUX    - Linux
	 FREEBSD  - FreeBSD
	 OPENBSD  - OpenBSD
	 SOLARIS  - Sun Solaris
	 AIX      - AIX
     UNIX     - Any UNIX BSD/SYSV system
*/

#define OS_PLATFORM_UTIL_VERSION 1.0.0.180723

// DARWIN
#if defined(__APPLE__) && (defined(__GNUC__) || defined(__xlC__) || defined(__xlc__))
#  include <TargetConditionals.h>
#  if defined(TARGET_OS_MAC) && TARGET_OS_MAC
#    define I_OS_DARWIN
#    ifdef __LP64__
#      define I_OS_DARWIN64
#    else
#      define I_OS_DARWIN32
#    endif
#  else
#    error "not support this Apple platform"
#  endif

// ANDROID
#elif defined(__ANDROID__) || defined(ANDROID)
#  define I_OS_ANDROID
#  define I_OS_LINUX

// Windows
#elif !defined(SAG_COM) && (!defined(WINAPI_FAMILY) || WINAPI_FAMILY==WINAPI_FAMILY_DESKTOP_APP) && (defined(WIN64) || defined(_WIN64) || defined(__WIN64__))
#  define I_OS_WIN32
#  define I_OS_WIN64
#elif !defined(SAG_COM) && (defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__))
#  if defined(WINAPI_FAMILY)
#    ifndef WINAPI_FAMILY_PC_APP
#      define WINAPI_FAMILY_PC_APP WINAPI_FAMILY_APP
#    endif
#    if defined(WINAPI_FAMILY_PHONE_APP) && WINAPI_FAMILY==WINAPI_FAMILY_PHONE_APP
#      define I_OS_WINRT
#    elif WINAPI_FAMILY==WINAPI_FAMILY_PC_APP
#      define I_OS_WINRT
#    else
#      define I_OS_WIN32
#    endif
#  else
#    define I_OS_WIN32
#  endif

//CYGWIN
#elif defined(__CYGWIN__)
#  define I_OS_CYGWIN

// sun os
#elif defined(__sun) || defined(sun)
#  define I_OS_SOLARIS

// LINUX
#elif defined(__linux__) || defined(__linux)
#  define I_OS_LINUX

// FREEBSD
#elif defined(__FreeBSD__) || defined(__DragonFly__) || defined(__FreeBSD_kernel__)
#  ifndef __FreeBSD_kernel__
#    define I_OS_FREEBSD
#  endif
#  define I_OS_FREEBSD_KERNEL

// OPENBSD
#elif defined(__OpenBSD__)
#  define I_OS_OPENBSD

// IBM AIX
#elif defined(_AIX)
#  define I_OS_AIX
#else
#  error "not support this OS"
#endif

#if defined(I_OS_WIN32) || defined(I_OS_WIN64) || defined(I_OS_WINRT)
#  define I_OS_WIN
#endif

#if defined(I_OS_WIN)
#  undef I_OS_UNIX
#elif !defined(I_OS_UNIX)
#  define I_OS_UNIX
#endif

#ifdef I_OS_DARWIN
#define I_OS_MAC
#endif
#ifdef I_OS_DARWIN32
#define I_OS_MAC32
#endif
#ifdef I_OS_DARWIN64
#define I_OS_MAC64
#endif

#endif // OSPLATFORMUTIL_H
```


## 判断文件是否存在


### WINDOWS

```c++
#include <unistd.h>
#include <fcntl.h>

int main()  
{  
    if((access("test.c",F_OK))!=-1)  
    {  
        printf("文件 test.c 存在. ");  
    }

    return 0
}
```

#### 函数原型说明

```java
int access(const char *pathname, int mode);   
```

**参数：**   
 - *pathname:* 需要测试的文件路径名。   
 - *mode:* 需要测试的操作模式，可能值是一个或多个
           - R_OK(可读?), 
           - W_OK(可写?), 
           - X_OK(可执行?) 
           - F_OK(文件存在?)组合体。 
  
**返回说明： **


成功执行时，返回0。失败返回-1，errno被设为以下的某个值 
 - EINVAL： 模式值无效   
 - EACCES： 文件或路径名中包含的目录不可访问 
 - ELOOP ： 解释路径名过程中存在太多的符号连接 
 - ENAMETOOLONG：路径名太长 
 - ENOENT：  路径名中的目录不存在或是无效的符号连接 
 - ENOTDIR： 路径名中当作目录的组件并非目录 
 - EROFS： 文件系统只读 
 - EFAULT： 路径名指向可访问的空间外 
 - EIO：  输入输出错误 
 - ENOMEM： 不能获取足够的内核内存 
 - ETXTBSY：对程序写入出错 

### LINUX

```c++
#include <io.h>

int main()  
{  
    if((access("test.c",F_OK))!=-1)  
    {  
        printf("文件 test.c 存在. ");  
    }

    return 0
}
```

#### 原型说明

```c++
int _access(const char *pathname, int mode);
```

mode 的值和含义如下所示：
- 00——只检查文件是否存在
- 02——写权限
- 04——读权限
- 06——读写权限

对应的还有_access的宽字符版本，用法相同。