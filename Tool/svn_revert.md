# [SVN 撤回（回滚）提交的代码](https://blog.csdn.net/weixin_36429334/article/details/53765851)

1. 打开 svn show log 日志，查看自己提交的代码文件
![](https://img-blog.csdn.net/20161220171618933?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd2VpeGluXzM2NDI5MzM0/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

2. revert change from this version 从这个版本恢复更改
![](https://img-blog.csdn.net/20161220171618933?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd2VpeGluXzM2NDI5MzM0/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
> 这个操作会恢复本文件未提交前的版本（代码）

3. 修改好后从新再提交  
![](https://img-blog.csdn.net/20161220171925169?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd2VpeGluXzM2NDI5MzM0/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
