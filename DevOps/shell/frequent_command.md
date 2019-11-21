### 修改/配置环境变量
---
1. 修改或配置当前用户的环境变量
```bash
vim ~/.bashrc  
export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib  
source ~/.bashrc
```

2. 修改或配置系统的环境变量
```bash 
sudo vim /etc/profile   
export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib  
source /etc/profile
```

3. 临时修改环境变量

>export CLASS_PATH=./JAVA_HOME/lib:\$JAVA_HOME/jre/lib

### find指令
---
find的查询条件可以是文件名，文件类型，文件大小，文件所属用户，最后访问时间，文件访问权限等

```bash
find ./ -iname sbso_1988  
find ./ -name "f[Oo][Oo]" -print
```

### whereis/which/locate/type
---
- which 查找可执行命令
- whereis 搜索程序名，二进制(-b)，man(-m)，source(-s)
- type 区分是否为shell自带指令
- locatte 快速查找locationdb中的文件，非实时，可在查找前执行updatedb

### grep
---
1. grep最简单的用法，匹配一个词：grep word filename

2. 能够从多个文件里匹配：
```bash
grep word filename1 filenam2 filename3
```

3. 能够使用正則表達式匹配：
```bash
grep -E pattern f1 f2 f3...
```

4. 能够使用-o仅仅打印匹配的字符，例如以下所看到的：
```bash
lichao@ubuntu:command\$ echo this is a line. | grep -E -o "[a-z]*\."  
line.
```

5. 打印除匹配行之外的其它行，使用-v
```bash
lichao@ubuntu:command\$ echo -e "1\n2\n3\n4" | grep -v -E "[1-2]"  
3  
4
```

6. 统计匹配字符串的行数。使用-c
```bash
lichao@ubuntu:command\$ echo -e "1111\n2222" | grep -E "[1-2]" -c  
2
```

1. 假设我们统计字符串模式匹配的次数。能够结合-o和-c。例如以下：
>lichao@ubuntu:command\$ echo -e "1111\n2222" | grep -o -E "[1-2]"  | wc -l  
8

8. 假设须要显示行号，能够打开-n，例如以下：
>lichao@ubuntu:command\$ echo -e "1111\n2222\n33333\n44444" | grep -n -E "3"  
3:33333

9. -b选项能够打印出匹配的字符串想对于其所在的行起始位置的偏移量（从0開始）。通常配合-o使用，例如以下：
>lichao@ubuntu:command\$ echo "0123456789" | grep -b -o 4  
4:4

10. 当字符串在多个文件里匹配时。-l选项将仅仅打印文件名称

11. -L与-l相对。仅仅打印不匹配的文件名称
```bash
lichao@ubuntu:command\$ cat test1.txt  
linux  
is  
fun  
lichao@ubuntu:command\$ cat test2.txt  
a      
very        
popular  
os,  
linux  
lichao@ubuntu:command\$ cat test3.txt  
what  
the  
fxxk        
lichao@ubuntu:command\$ grep -l linux test1.txt test2.txt test3.txt  
test1.txt  
test2.txt  
lichao@ubuntu:command\$ grep -L linux test1.txt test2.txt test3.txt  
test3.txt  
```

12. 打开递归搜索功能
```bash
lichao@ubuntu:command\$ grep -n -R linux .   
./test2.txt:5:linux  
./test1.txt:1:linux  
```

13. 忽略大写和小写：-i
```bash
>lichao@ubuntu:command\$ echo "HELLO WORLD" | grep -i "hello"  
HELLO WORLD
```

14. 匹配多个字符串模式

>lichao@ubuntu:command\$ echo "This is a line." | grep -e "This" -e "is" -e "line" -o  
This  
is  
line  

15. 用单独的文件提供匹配样式，每一个匹配的样式作为一行，例如以下例所看到的：
>lichao@ubuntu:command\$ cat pattern.txt  
1\$  
2  
3  
lichao@ubuntu:command\$ cat num.txt   
1  
2  
3  
4  
5  
6  
7  
8  
9  
10  
lichao@ubuntu:command\$ grep -f pattern.txt num.txt   
1  
2  
3  

16. 打印匹配行上下文信息,使用 -A n打印匹配行及其后n行信息。使用-B n打印匹配行及其前n行信息。使用 -C n。打印匹配行及其前后n行信息。假设有多重匹配，将使用--隔离。
示比例如以下：
>lichao@ubuntu:command\$ seq 1 10 | grep 5 -A 3  
5  
6  
7  
8  
lichao@ubuntu:command\$ seq 1 10 | grep 5 -B 3  
2  
3  
4  
5  
lichao@ubuntu:command\$ seq 1 10 | grep 5 -C 3      
2    
3    
4    
5    
6    
7    
8    
lichao@ubuntu:command\$ echo -e "a\nb\nc\nd\na\nb\nc\nd\n" | grep a -A 2  
a  
b  
c  
\-\-  
a  
b  
c  

17. 使用-q进入静默模式，该模式下。grep命令执行目的不过执行一个条件測试。通常在脚本中使用。通过检查其返回值进行下一步操作。示比例如以下：
>lichao@ubuntu:command\$ cat tmp.txt  
hello  
world  
lichao@ubuntu:command\$ cat tmp.csh  
```
\#!/bin/bash
if [ \$# -ne 2 ]; then  
	echo "Usage: \$0 match_pattern file_name"  
	exit  
fi  
match=\$1   
file=\$2  
grep -q $match $file  
if [ \$?  
 -ne 0 ]; then  
	echo "\$match not exist in \$file"   
else
	echo "$match exist in $file"
fi
```
>lichao@ubuntu:command\$ ./tmp.csh hello tmp.txt  
hello exist in tmp.txt

18. -Z选项在输出匹配文件名称时将以/0结尾配合xargs -0能够发挥非常多作用，比如删除匹配某个模式的文件例如以下：
>lichao@ubuntu:command\$ ls -llrt  
total 28      
-rw-rw-r-- 1 lichao lichao  13 Nov  1 20:38 test1.txt  
-rw-rw-r-- 1 lichao lichao  27 Nov  1 20:39 test2.txt  
-rw-rw-r-- 1 lichao lichao  14 Nov  1 20:39 test3.txt  
-rw-rw-r-- 1 lichao lichao  21 Nov  1 20:45 num.txt  
-rw-rw-r-- 1 lichao lichao   7 Nov  1 20:45 pattern.txt  
-rw-rw-r-- 1 lichao lichao  12 Nov  1 21:25 tmp.txt  
-rwxr-xr-x 1 lichao lichao 217 Nov  1 21:27 tmp.csh   
lichao@ubuntu:command\$ cat test1.txt     
linux  
is  
fun  
lichao@ubuntu:command\$ cat test2.txt  
a   
very  
popular   
os,  
linux  
lichao@ubuntu:command\$ grep "linux" * -lZ | xargs -0 rm  
lichao@ubuntu:command\$ ls  
num.txt  pattern.txt  test3.txt  tmp.csh  tmp.txt  
以上命令将包括linux字符串的test1.txt和test2.txt删除。  

19. 排除/包含文件或者文件夹：  
1）--include *{.c,.cpp} 仅仅在文件夹中搜索.c和.cpp文件；  
2）--exclude "README" 排除全部README文件   
3) --include-dir 仅在某些文件夹中搜索   
4) --exclude-dir 排除某些文件夹   
5) --exclude-from FILE 从文件FILE中读取须要排除的文件列表  
```bash
lichao@ubuntu:test\$ ls  
dir1  dir2  exclude.config  test1.txt  test2.doc  test3.word  
lichao@ubuntu:test\$ cat test1.txt   
linux   
is   
fun  
lichao@ubuntu:test\$ cat test2.doc   
wonderful   
os,  
linux  
lichao@ubuntu:test\$ cat test3.word   
wonderful   
os,  
linux  
lichao@ubuntu:test\$ ls dir1/  
test1.txt  test2.doc  test3.word  
lichao@ubuntu:test\$ ls dir2/  
test1.txt  test2.doc  test3.word  
lichao@ubuntu:test\$ cat exclude.config   
\*.txt  
lichao@ubuntu:test\$ grep "linux" -R -n .   
./test2.doc:3:linux  
./test3.word:3:linux  
./test1.txt:1:linux   
./dir2/test2.doc:3:linux  
./dir2/test3.word:3:linux  
./dir2/test1.txt:1:linux     
./dir1/test2.doc:3:linux  
./dir1/test3.word:3:linux  
./dir1/test1.txt:1:linux   
lichao@ubuntu:test\$ grep "linux" -R -n . --include \*.txt --include \*.doc  
./test2.doc:3:linux  
./test1.txt:1:linux   
./dir2/test2.doc:3:linux  
./dir2/test1.txt:1:linux   
./dir1/test2.doc:3:linux  
./dir1/test1.txt:1:linux   
lichao@ubuntu:test\$ grep "linux" -R -n . --exclude \*.txt --eclude \*.doc  
grep: unrecognized option '--eclude'  
Usage: grep [OPTION]... PATTERN [FILE]...  
Try 'grep --help' for more information.  
lichao@ubuntu:test\$ grep "linux" -R -n . --exclude \*.txt --exclude \*.doc    
./test3.word:3:linux    
./dir2/test3.word:3:linux    
./dir1/test3.word:3:linux    
lichao@ubuntu:test\$ grep "linux" -R -n . --exclude-dir dir1  
./test2.doc:3:linux  
./test3.word:3:linux  
./test1.txt:1:linux   
./dir2/test2.doc:3:linux  
./dir2/test3.word:3:linux  
./dir2/test1.txt:1:linux  
lichao@ubuntu:test\$ grep "linux" -R -n . --exclude-dir dir1 --exclude-dir dir2   
./test2.doc:3:linux    
./test3.word:3:linux   
./test1.txt:1:linux   
lichao@ubuntu:test\$ grep "linux" -R -n . --exclude-from exclude.config   
./test2.doc:3:linux  
./test3.word:3:linux  
./dir2/test2.doc:3:linux  
./dir2/test3.word:3:linux  
./dir1/test2.doc:3:linux  
./dir1/test3.word:3:linux  
```
已上即为grep经常使用的选项。
https://www.cnblogs.com/tlnshuju/p/7106790.html

### [Snippet]逐个遍历当前目录下的文件
---
```bash
#!/usr/bin/env bash

# get the absoluth path of current file
cur_dir=$(cd "$(dirname "$0")"; pwd)
files=$(find  $cur_dir -maxdepth 1  -name '*.html')

# fix for loop splits on all whitespace
IFS=$'\n'

for f in ${files}; do  echo ${f}; done

unset IFS
```