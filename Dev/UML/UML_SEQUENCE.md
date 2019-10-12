# [一、时序图](https://cloud.tencent.com/developer/article/1330326)

时序图是一种强调消息时序的交互图，他由**对象（Object）、消息（Message）、生命线（Lifeline）和Combined Fragments**组成，它主要描述系统中**对象和对象之间的交互**，它将这些交互建模成消息交换。

时序图将交互关系展示成了一个平面二维图，其中纵向标示时间轴，时间沿竖线从上向下进行。横向轴标示了交互中各各个对象。对象的的用生命线表示。消息从一个对象的生命线到另一个对象生命线的箭头表示，箭头以时间顺序在图中从上到下排列，从左到右排列。

***对象（Object）和生命线（Lifeline）***

生命线头上那个方正的框里面存放的就是对象，对象有自己的名字，生命线其实就是从上到下的一个虚线。生命线标示一个对象存在的生命周期，两条生命线中间通过消息连接起来，

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/8gwkt8ddo2.png?imageView2/2/w/1620)

***消息（Message）***

消息用于对象间传递信息，对象之间的信息互通就是通过消息，消息按照分类可分为：同步消息（Synchronous Message），异步消息（Asynchronous Message）和返回消息（Return Message） 自关联消息（Self-Message）

- 同步消息：发送消息的对象在发送消息后会挂住，等消息接受对象接受消息返回后才会解除挂住的状态继续自己的工作。
- 异步消息：发送消息的对象在发送消息后会继续自己的工作，而不等消息接受对象接受消息返回。
- 返回消息：标示发送消息后返回的动作
- 自关联消息：一个对象内自调用的情况。

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/1cxdpmj8jv.png?imageView2/2/w/1620)

***Combined Fragments***

 表示有一定条件的消息发送，

- Alternative fragment（denoted “alt”） 标示 if…then…else
- Option fragment (denoted “opt”) 标示Switch
- Parallel fragment (denoted “par”) 标示同时发生
- Loop fragment(denoted “loop”) 标示for
- Break标示退出循环

###### 1. loop

- 当没有指定循环边界默认范围为[0,无穷大]：

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/sv93uihxny.png?imageView2/2/w/1620)

- 如果只指定了一个值，那么默认执行该值次数：

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/2u59uj5wwf.png?imageView2/2/w/1620)

- 指定了循环边界,则最少执行最小值值，最多执行最大值次数：

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/b32w4x2533.png?imageView2/2/w/1620)

- 实现do-while方式，至少执行一次,如果size<0则退出:

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/zzobo5wc1i.png?imageView2/2/w/1620)

###### 2. alt

条件判断，如果n>0则执行agree函数否者执行reject函数

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/potsqotmd2.png?imageView2/2/w/1620)

###### 3. opt

switch，当满足不同条件执行不同方法：

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/xcq5lzv6om.png?imageView2/2/w/1620)

###### 4. break

n=10时候执行save并退出循环

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/15hw9lbuh0.png?imageView2/2/w/1620)

###### 5. par

同时进行，比如多个线程同时执行任务

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/xr54jqb0m3.png?imageView2/2/w/1620)

## 例子

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/tz0cifhtf0.png?imageView2/2/w/1620)
