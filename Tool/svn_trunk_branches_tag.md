# [SVN分支/合并原理及最佳实践](http://blog.csdn.net/e3002/article/details/21469437)

使用 `SVN` 几年了，一直对分支和合并敬而远之，一来是因为分支的管理不该我操心，二来即使涉及到分支的管理，也不敢贸然使用合并功能，生怕合并出了问题对团队造成不良影响，最主要的原因是，自己对分支的目的和合并的方法不甚了解，这才是硬伤。

最近由于适配机型的需要，需要经常接触分支和合并两项工作，突然发现这玩意整不明白很难开展工作，遂这两天着重研究了一下，有点收获，怕以后忘了，故趁着余温尚在赶紧写下来，好记性不如烂笔头嘛。下文的实践主要是参考了 TortoiseSVN 的帮助文档和 Subversion 的在线文档，Subversion 的 *[在线文档](http://svnbook.red-bean.com/en/1.5/svn-book.html)*.

话说我公司现在的源代码管理挺乱的。 svn 目录并没有采取标准的 `source/branches`、`source/trunk` 结构，主线和分支放得到处都是，`release`版本也并没有当成 `tag` 处理，而是当成 branch 来管理，经常还要在 release 版本上改来改去...

## 先说说什么是 branch

按照 Subversion 的说法，一个 branch 是某个 development line（通常是主线也即trunk）的一个拷贝，见下图：

![](http://hi.csdn.net/attachment/201107/14/0_1310635624026O.gif)

branch 存在的意义在于，***在不干扰 trunk 的情况下，和 trunk 并行开发***，待开发结束后合并回 trunk 中，在branch 和 trunk 各自开发的过程中，他们都可以不断地提交自己的修改，从而使得每次修改在 repository 中都有记录。

**设想以下场景**

> 如果你的项目需要开发一个新功能，而该功能可能会修改项目中的绝大多数文件，而与此同时，你的另一位同事正在进行 bug fix，如果你的新功能不在 branch 中开发而直接在 trunk 中开发，那么你极有可能影响另一位同事的 bug fix，他/她在bug 修复中可能会遇到各种各样的问题，因为你的频繁提交代码引入了过多的不稳定因素。你可能会说，那我在开发的过程中不提交不就行了，等到我全部开发结束我再提交，是，你可以这么做，那还要版本控制干什么呢？也许等到你最后提交代码的时候（也许一周，也许两周？），你会发现有一大堆 conflict 等着你 resolve ...

 

*那么，正确的做法是什么？*

使用 branch **分支**，从 trunk 创建 branch，然后在你的 branch 上开发，开发完成后再合并到 trunk 中。

关于 branch 先讲到这里，下面说说什么叫做**合并**。很好理解，当 branch 开发完成后（包括必要的测试），将 branch 中的修改同步到 trunk 中，这个过程有可能包括修改文件、增加文件、删除文件等等。


说到这里，貌似本文差不多可以结束了，不就是分支和合并么？只要再简单地说说如何建立分支和如何合并就可以收尾了，可能只需两个命令，也可能只需鼠标点几下然后键盘敲两下即可。其实事情远非这么简单，爱动脑筋的同学可能会问了，将 branch 的改动 merge 到 trunk的时候，和上文说的直接在 trunk 中全部开发完然后提交有何区别？你最后还不是要处理一大堆 conflict？

 

这个问题问得非常好，其实这正是本文的重点：***branch 和 trunk 在并行开发的过程中如何感知对方***，branch 如何才能在开发过程中不会和 trunk 越走越远，导致最后无法合并？试想一下，如果在你开发 branch 的过程中，trunk 中的某个类文件已经被删除了（这可能是另外一个家伙在另一个 branch 上开发了两周后才合并到 trunk 的），而你竟然在这个类文件上做了大量修改，试问你到最后合并回 trunk 的时候该有多蛋疼？解决这一问题的唯一手段是，branch 要不停地和 trunk 保持同步，你要及时地知道 trunk 都做了什么修改，这些修改是否会影响你正在开发的新功能，如果需要，你必须及时调整 branch 的代码，使之能与 trunk “兼容”。

 

### 那么如何让 branch 和 trunk 保持同步？

合并，从 trunk 合并到 branch，你没听错，是从 trunk 合并到 branch。关于 TortoiseSVN 的合并，有几点需要注意：

TortoiseSVN 的合并发生在本地，也即你的 working copy 中，你无需过多担心会对 repository 中的代码造成影响
不管是从 trunk 合并到 branch 还是最终从 branch 合并回 trunk，在每次合并前最好先 update，然后将本地的修改先全部 commit，保护好现场，万一合并不理想随时都可以 revert. 合并完成后看是否能正确编译，然后测试验证，最后将合并后的改动提交到 repository.

## 演示

### 1、创建本地 Repository

略

### 2、Check out

略

### 3、trunk 创建新项目

略

### 4、创建 branch

在 `/trunk/<project>` 目录上右键，依次选择 `TortoiseSVN` > `Branch/tag...`，在弹出窗口的 `To URL` 中填入分支的地址，在这里目标 `revision` 选择 *`HEAD revision`*，如下图所示，添加 log 后点击 `ok` 分支便建立了。

![](http://hi.csdn.net/attachment/201107/14/0_1310654533q26t.gif)

> 这个操作速度非常快，新建的 branch 在 repository 中其实只是一个指向 trunk 某个 revision 的软连接而已，并没有真的复制文件。

### 5、Check out 分支

右键 *`<SVN>`* 目录选择 `TortoiseSVN Update` 即可将刚刚建立的分支下载回本地。

### 6、branch 提交一个新文件

![](http://hi.csdn.net/attachment/201107/14/0_1310655182jGGW.gif)

### 7、trunk 紧接着提交一个修改

![](http://hi.csdn.net/attachment/201107/14/0_131065523464l9.gif)

### 8、branch 再次提交一个修改

![](http://hi.csdn.net/attachment/201107/14/0_1310655316Fc0M.gif)

### 9、将 trunk 中的修改同步到 branch

6-8 演示的是 branch 和 trunk 在独立、并行地开发。为了防止在 ***“错误”*** 的道路上越走越远，现在 branch 意识到是时候和trunk 来一次同步了（将trunk合并到branch）。

首先，在本地 trunk 中先 update 一下，有冲突的解决冲突，保证trunk和repository已经完全同步，然后在 ***`/branches/<project>`*** 上右键，依次选择 `TortoiseSVN` > `Merge..`，在弹出的窗口中选择第一项 `Merge a range of revision`，这个类型的 Merge 已经介绍得很清楚，适用于将某个分支或主线上提交的多个 `revision` 间的变化合并到另外一个分支上。

![](http://hi.csdn.net/attachment/201107/14/0_13106558532uPR.gif)

点击next后，出现如下窗口：

![](http://hi.csdn.net/attachment/201107/14/0_13106562442ZQZ.gif)

由于是要从 trunk 合并到 branch，理所当然这里的 `URL to merge from` 应该填 trunk 的路径，`Revision range to merge` 很好理解，就是你要将 trunk 的哪些 revision 所对应的变化合并到 branch 中，可以是某一连串的 revision ，比如4-7，15-HEAD，也可以是某个单独的 revision 号。由于在 r4 中，trunk 修改了 Person.Java 中的 talk() 方法，所以这里的 revision 只需填 4 即可。点击 next 后出现下图：

![](http://hi.csdn.net/attachment/201107/14/0_1310656626mx9H.gif)

在这里只需保留默认设置即可。在点击Merge按钮前你可以先 `Test merge` 一把，看成功与否，以及 merge 的详细信息。点击Merge按钮后trunk所做的修改将同步到branch中。

### 10、提交合并后的 branch


![](http://hi.csdn.net/attachment/201107/14/0_13106569839g4f.gif)
 

至此，branch已经完全和trunk同步，branch和trunk的代码相处很融洽，没有任何冲突，如果branch已经开发结束，那是时候将branch合并回trunk了，当然，如果branch还要继续开发，那你将不断地重复6-10这几个步骤。

### 11、将 branch 合并回 trunk

在 `/trunk/<project>`上右键（注意是在主线的目录上右键），依次选择 `TortoiseSVN` > `Merge..`，在弹出的窗口中，Merge type 选择第二项 `Reintegrate a branch`，这种类型的合并适合在分支开发结束后将所有的改动合并回主线。

![](http://hi.csdn.net/attachment/201107/14/0_13106573597hYb.gif)

点击next后出现如下窗口：

![](http://hi.csdn.net/attachment/201107/14/0_131065774486Zw.gif)

在这里，"From URL" 选择 `/branches/<project>`，无需选择 revision 号，Reintegrate 会将 branch 上所有修改合并到 trunk。后面的步骤和上文第9步中的一样，不再啰嗦了。如无意外，branch 将成功合并到 trunk，你需要做的只是将合并后的 trunk 赶紧 commit！

### 12、提交合并后的 trunk

so easy...

### 13、删除 branch

如果你认为你新加的功能已经开发完成了，你可以删除你的分支

 

 

到这里，我已经给你演示完了整个过程，我一身的汗也下来了，我想罢工了，不过最后我们还是看看所有的log信息吧，通过log能发现我们干的所有事情：

![](http://hi.csdn.net/attachment/201107/14/0_1310658093DCD2.gif)
 

r1-r7 正是我上文在干的事情，从 Message 中你能发现我对 trunk 和 branch 都干了什么，另外，在Log Messages窗口的左下角勾选了"Include merged revisions"你还能看到额外的Merge information：

![](http://hi.csdn.net/attachment/201107/14/0_1310658311B1x5.gif)

图中灰色的是和 merge 相关的 log，共发生了两 次merge，第一次是在 r6，在 r6 中，branch 合并了 trunk 在 r4 时提交的变化；第二次是在 r7，在 r7 中，trunk 合并了b ranch 从 r2 到 r6 的所有变化。


## 总结

- branch 主要用于新功能的开发
- 合并发生在本地 working copy，只要你不提交就不会影响到 repository
- 合并前一定要先 update、commit，保证不会 out of day，并将本地的修改保存到 repository
- branch 和 trunk 并行开发的过程中，要经常同步，将 trunk 的修改合并到 branch，合并时选择 `Merge a range of - revision`"
- branch 最后合并回 trunk 时，merge type选择 `Reintegrate a branch`




