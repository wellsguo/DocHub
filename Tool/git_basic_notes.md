## clean git

```
find . -name ".git" | xargs rm -Rf
```

## git command

### 1. Git 版本库的诞生

#### 1.1 本地版本库  
```
$ mkdir "repo/dir"  

$ cd "repo/dir"  

$ git init

```

#### 1.2 添加文件到版本库  
> *** Please tell me who you are.  
>
>Run  
>
>  git config --global user.email "you@example.com"  
>  git config --global user.name "Your Name"  
>  
>to set your account's default identity.  
>Omit --global to set the identity only in this repository.
>


```
$ git add . // just add

$ git commit -m "commit messasge"

```

#### 1.3 Github 远程版本库
按向导操作

#### 1.4 本地和远程版本库关联
``` 
$ git remote add origin git@github.com:michaelliao/learngit.git

$ git push -u origin master // the first time to push
```

### 2. 提交 & 更新

#### 2.1 提交
```
$ git add .

$ git commit –m "commit messasge" // submit

$ git push origin master // remote sync
```

#### 2.2 更新
> https://blog.csdn.net/qq_36113598/article/details/78906882  
> http://www.ruanyifeng.com/blog/2014/06/git_remote.html

![work mechanism](http://kmknkk.oss-cn-beijing.aliyuncs.com/image/git.jpg)

##### + 分支
```
$ git branch //查看本地所有分支  

$ git branch -r //查看远程所有分支

$ git branch -a //查看本地和远程的所有分支

$ git branch <branchname> //新建分支

$ git branch -d <branchname> //删除本地分支

$ git branch -d -r <branchname> //删除远程分支，删除后还需推送到服务器

$ git push origin:<branchname>  //删除后推送至服务器

$ git branch -m <oldbranch> <newbranch> //重命名本地分支
/*
* 重命名远程分支：
*   1、删除远程待修改分支
*   2、push本地新分支到远程服务器
*/
```
> - git fetch 是将远程主机的最新内容拉到本地，用户在检查了以后决定是否合并到工作本机分支中。  
> - git pull 则是将远程主机的最新内容拉下来后直接合并，即：**`git pull = git fetch + git merge`**，这样可能会产生冲突，需要手动解决。


#### + fetch
```
$ git fetch <远程主机名> //这个命令将某个远程主机的更新全部取回本地

$ git fetch <远程主机名> <分支名> // 取回特定分支的更新，注意之间有空格

$ git fetch origin master // 最常见的取回origin 主机的master 分支
```
>  取回更新后，会返回一个FETCH_HEAD ，指的是某个branch在服务器上的最新状态，
 可在本地通过命令查看刚取回的更新信息

```
$ git log -p FETCH_HEAD
```

#### + pull
> git pull 的过程可以理解为：

```
$ git fetch origin master //从远程主机的master分支拉取最新内容

$ git merge FETCH_HEAD    //将拉取下来的最新内容合并到当前所在的分支中
```
>即将远程主机的某个分支的更新取回，并与本地指定的分支合并，完整格式可表示为：

```
$ git pull <远程主机名> <远程分支名>:<本地分支名>
```
> 如果远程分支是与当前分支合并，则冒号后面的部分可以省略：

```
$ git pull origin next
```

