## svn.bat
```cmd
@echo on 
color 2f 
mode con: cols=80 lines=25 
@REM 
@echo 正在清理SVN文件，请稍候...... 
@rem 循环删除当前目录及子目录下所有的SVN文件 
@rem for /r . %%a in (.) do @if exist "%%a\.svn" @echo "%%a\.svn" 
@for /r . %%a in (.) do @if exist "%%a\.svn" rd /s /q "%%a\.svn" 
@echo 清理完毕！！！ 
@pause
:: --------------------- 
:: 作者：爱人间 
:: 来源：CSDN 
:: 原文：https://blog.csdn.net/menghuannvxia/article/details/47748245 
:: 版权声明：本文为博主原创文章，转载请附上博文链接！
```

## 一、Linux

删除这些目录是很简单的，命令如下  
```
find . -type d -name ".svn"|xargs rm -rf
```  
或者  
```
find . -type d -iname ".svn" -exec rm -rf {} \;
```


## 二、Windows   

### 1、平级目录   
```
xcopy project_dir project_dir_1 /s /i 
```  

### 2、根目录执行    
``` 
for /r . %%a in (.) do @if exist "%%a\.svn" rd /s /q "%%a\.svn" 
```  
其实第二种方法可以用来干很多事的，比如把代码中的 `.svn` 替换为任意其他文件名并在硬盘根目录下执行，就可以从硬盘上删除所有的这个文件啦。 