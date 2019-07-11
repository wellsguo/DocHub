> Git如何永久删除文件(包括历史记录)  
> https://www.cnblogs.com/shines77/p/3460274.html  
> Git如何永久删除文件(包括历史记录)

#### 从资料库中清除文件

Git Bash执行如下命令: 
```bash
$ git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path-to-your-remove-file' --prune-empty --tag-name-filter cat -- --all
```

- 其中,** _*path-to-your-remove-file*_** 即是删除文件的相对路径(**相对于git仓库的跟目录**). 
- 注意：这里的文件或文件夹，都不能以 `/` 开头，否则文件或文件夹会被认为是从 git 的安装目录开始。
- 如果要删除的目标不是文件，而是文件夹，那么请在 `git rm --cached` 命令后面添加 -r 命令，表示递归的删除（子）文件夹和文件夹下的文件，类似于 `rm -rf` 命令。

此外，如果要删除的文件很多, 可以写进一个.sh文件批量执行, 如果文件或路径里有中文, 由于MinGW或CygWin对中文路径设置比较麻烦, 你可以使用通配符\*号, 例如: `sound/music\_*.mp3`, 这样就把sound目录下以`music_`开头的mp3文件都删除了.

###### del-music-mp3.sh
```bash
#!/bin/bash

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch projects/Moon.mp3' --prune-empty --tag-name-filter cat -- --all
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch sound/Music_*.mp3' --prune-empty --tag-name-filter cat -- --all
```

- 如果看到类似下面这样的, 说明删除成功了。
```
Rewrite 48dc599c80e20527ed902928085e7861e6b3cbe6 (266/266)
# Ref 'refs/heads/master' was rewritten
```
- 如果显示 xxxxx unchanged  
说明repo里没有找到该文件, 请检查路径和文件名是否正确.

**注意:** 如果想以后不会再上传某个文件（夹）, 请把这个文件或文件夹添加到`.gitignore`文件里, 然后再 push 到 repo. 

#### 推送我们修改后的repo
以强制覆盖的方式推送你的repo, 命令如下:
```bash
$ git push origin master --force --all
```

这个过程其实是重新上传我们的repo, 比较耗时, 虽然跟删掉重新建一个repo有些类似, 但是好处是保留了原有的更新记录, 所以还是有些不同的. 如果你实在不在意这些更新记录, 也可以删掉重建, 两者也差不太多, 也许后者还更直观些.

执行结果类似下面:

```
Counting objects: 4669, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (4352/4352), done.
Writing objects: 100% (4666/4666), 35.16 MiB | 51 KiB/s, done.
Total 4666 (delta 1361), reused 0 (delta 0)
To https://github.com/defunkt/github-gem.git
 + beb839d...81f21f3 master -> master (forced update)
```
为了能从打了 tag 的版本中也删除你所指定的文件或文件夹，您可以使用这样的命令来强制推送您的 Git tags：
```bash
$ git push origin master --force --tags
```

#### 清理和回收空间
虽然上面我们已经删除了文件, 但是我们的repo里面仍然保留了这些objects, 等待垃圾回收(GC), 所以我们要用命令彻底清除它, 并收回空间.

命令如下:

```bash
$ rm -rf .git/refs/original/

$ git reflog expire --expire=now --all

$ git gc --prune=now

Counting objects: 2437, done.
# Delta compression using up to 4 threads.
# Compressing objects: 100% (1378/1378), done.
# Writing objects: 100% (2437/2437), done.
# Total 2437 (delta 1461), reused 1802 (delta 1048)

$ git gc --aggressive --prune=now

Counting objects: 2437, done.
# Delta compression using up to 4 threads.
# Compressing objects: 100% (2426/2426), done.
# Writing objects: 100% (2437/2437), done.
# Total 2437 (delta 1483), reused 0 (delta 0)
```

现在你再看看你的.git目录文件大小是不是变小了.