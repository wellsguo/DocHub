# UI 篇



### [Android中RecyclerView布局代替GridView实现类似支付宝的界面](https://blog.csdn.net/qq_15970265/article/details/53690913)

**单纯使用GridView**

- 第一种是利用GridView 的 android:horizontalSpacing="1dp"与android:verticalSpacing="1dp" 属性 利用GridView的背景色 与ItemView的背景色 ，之间的间隙作为分割线。

![](http://files.jb51.net/file_images/article/201606/201668164227327.png?201658164237)

![](http://files.jb51.net/file_images/article/201606/201668164253698.png?201658164259)

![](http://files.jb51.net/file_images/article/201606/201668164309842.png?201658164316)

- 第二种方法 就是使用背景选择器 Selector。

​         *实现起来更简单，但是也有一个小瑕疵，因为item 使用了selector, 那么相邻两个item 之间的分割线相当于两条，会加深。*



**RecyclerView**





