## [Windows: C++ Console 端输出颜色控制](https://blog.csdn.net/u012424148/article/details/52792472 )

C++控制台程序运行时输出框默认的文字颜色是白色，所以我常称其输出框为黑白框。但是这个文字样式不是固定不变的，是可以改变颜色的字体的。方法有两种：
1. **设置输出框的框体属性**  
在运行时弹出的输出框标题栏上点击右键设置它的属性，可以调节输出框的大小、背景色、文字颜色等属性。但是这种设置只能在自己的机子上运行显示。在其他人的机子上是没有用的。这里不做重点介绍。

2. **代码实现**  
这里介绍C++中用代码修改输出框显示文字的颜色。具体代码是调用一个函数 `SetConsoleTextAttribute(args...)`。
SetConsoleTextAttribute()函数是一个API设置字体颜色和背景色的函数。参数表中使用两个属性（属性之间用，隔开）。GetStdHandle()和FOREGROUND_或BACKGROUND_。\*值为 INTENSITY 或 RED 或 GREEN 或 BLUE。第一个属性获得句柄（即要设置颜色的地方），第二个属性设置颜色。属性相加是在属性值中间加 `|` 隔开即可。
  - GetStdHandle(STD_OUTPUT_HANDLE)获得句柄。
  - FOREGROUND_INTENSITY 表示设置前景色为高亮显示。
  - FOREGROUND_RED 表示设置前景色为红色，即字体颜色为红色。
  - FOREGROUND_GREEN 表示设置前景色为绿色，即字体颜色为绿色。
  - FOREGROUND_BLUE 表示设置前景色为蓝色，即字体颜色为蓝色。
  - BACKGROUND_INTENSITY 表示设置背景色为高亮显示。
  - BACKGROUND_RED 表示设置背景色为红色。
  - BACKGROUND_GREEN 表示设置背景色为绿色。
  - BACKGROUND_BLUE 表示设置背景色为蓝色。
  - ……
  
###### 说明：在使用时要在预处理中包含window.h头文件

### DEMO

```c++
#include <iostream>
#include "windows.h"
using namespace std;

int main()
{
    cout << "原色testCOLOR（没有设置字体颜色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);//设置三色相加
    cout << "白色testCOLOR（红色绿色蓝色相加）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED);//设置红色
    cout << "红色testCOLOR（设置的颜色为红色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_GREEN);//设置绿色
    cout << "绿色testCOLOR（设置的颜色为绿色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_BLUE);//设置蓝色
    cout << "蓝色testCOLOR（设置的颜色为蓝色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN);//设置红色和绿色相加
    cout << "黄色testCOLOR（红色和绿色相加色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_BLUE);//设置红色和蓝色相加
    cout << "粉色testCOLOR（红色和蓝色相加色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_GREEN | FOREGROUND_BLUE);//设置绿色和蓝色相加
    cout << "青色testCOLOR（绿色和蓝色相加色）" << endl;

    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY); //设置颜色，没有添加颜色，故为原色
    cout << "恢复原色" << endl;

    system("pause");
    return 0;
}
```


## [linux printf color 颜色](https://blog.csdn.net/junjun5156/article/details/52640427)


###### color.h

```C
#define NONE         "\033[m"
#define RED          "\033[0;32;31m"
#define LIGHT_RED    "\033[1;31m"
#define GREEN        "\033[0;32;32m"
#define LIGHT_GREEN  "\033[1;32m"
#define BLUE         "\033[0;32;34m"
#define LIGHT_BLUE   "\033[1;34m"
#define DARY_GRAY    "\033[1;30m"
#define CYAN         "\033[0;36m"
#define LIGHT_CYAN   "\033[1;36;43m"
#define PURPLE       "\033[0;35m"
#define LIGHT_PURPLE "\033[1;35m"
#define BROWN        "\033[0;33m"
#define YELLOW       "\033[1;33m"
#define LIGHT_GRAY   "\033[0;37m"
#define WHITE        "\033[1;37m"
 
/*
比如：
printf("\033[31m ####----->> \033[32m" "hello\n" "\033[m");
颜色分为背景色和字体色，30~39用来设置字体色，40~49设置背景：
背景色                        字体色
40: 黑                          30: 黑
41: 红                          31: 红
42: 绿                          32: 绿
43: 黄                          33: 黄
44: 蓝                          34: 蓝
45: 紫                          35: 紫
46: 深绿                      36: 深绿
47: 白色                      37: 白色
记得在打印完之后，把颜色恢复成NONE，不然再后面的打印都会跟着变色。
另外，还可以加一些ANSI控制码。加颜色只是以下控制码中的一种：
\033[0m   关闭所有属性
\033[1m   设置高亮度
\033[4m   下划线
\033[5m   闪烁
\033[7m   反显
\033[8m   消隐
\033[30m   --   \033[37m   设置前景色
\033[40m   --   \033[47m   设置背景色
\033[nA   光标上移n行
\033[nB   光标下移n行
\033[nC   光标右移n行
\033[nD   光标左移n行
\033[y;xH设置光标位置
\033[2J   清屏
\033[K   清除从光标到行尾的内容
\033[s   保存光标位置
\033[u   恢复光标位置
\033[?25l   隐藏光标
\033[?25h   显示光标
printf( CYAN "current function is %s " GREEN " file line is %d\n" NONE,
    __FUNCTION__, __LINE__ );
fprintf(stderr, RED "current function is %s " BLUE " file line is %d\n" NONE,
    __FUNCTION__, __LINE__ );
    return 0;
*/
```

###### color.c

```C
#include <stdio.h>
#include "color.h"
 
 
int main()
{
    printf("\033[31m ####----->> \033[32m" "hello\n" "\033[m");
    printf( LIGHT_CYAN "current function is %s " GREEN " file line is %d\n" NONE,
        __FUNCTION__, __LINE__ );
    fprintf(stderr, RED "current function is %s " BLUE " file line is %d\n" NONE,
        __FUNCTION__, __LINE__ );
        return 0;
}

```