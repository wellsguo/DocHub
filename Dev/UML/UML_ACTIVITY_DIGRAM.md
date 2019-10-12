# [活动图（Activity Diagrams）](https://cloud.tencent.com/developer/article/1330338)

活动图是UML中一种行为图，它展示了控制流和对象流，并且强调它们的顺序和条件控制流。

## 6.1  组元介绍

***开始(inital)和结束状态(final)***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/a6fzxspyzq.png?imageView2/2/w/1620)

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/60hztwzaaa.png?imageView2/2/w/1620)

***活动(action)：标示动作***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/qnmp259l1b.png?imageView2/2/w/1620)

***控制流(control flow)：链接活动***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/ngxv6d2cfq.png?imageView2/2/w/1620)

***决策(decison):条件判断***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/139zp1tlh1.png?imageView2/2/w/1620)

***合并（merge）:任意一个节点到达该点都继续往下走，不管其他分支***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/u735v00r4d.png?imageView2/2/w/1620)

***游泳道（swimlanes）：模型中存在多个对象时候使用比较适合***

分为水平和垂直

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/mw0sr1jcq2.png?imageView2/2/w/1620)

***分岔汇合（join）：所有分支都到该点时候才继续往下走，类似CountDownLatch.await后在继续往下走***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/lt61faxlrh.png?imageView2/2/w/1620)

***分流（fork）：类似fork多个线程执行放入线程池执行。***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/eveghwjxs3.png?imageView2/2/w/1620)

***接受信号（acceptsignal）***

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/mdygq0xr7b.png?imageView2/2/w/1620)

## 6.2  online shopping例子

下面拿uml官方online shopping网上购物例子介绍

![image.png](https://ask.qcloudimg.com/http-save/yehe-2190306/le5v1rey8p.png?imageView2/2/w/1620)

如图左上角黑色圆为活动开始，首先通过decision的条件判断是进行搜索还是浏览，如果是搜索则通过merge节点后搜索商品，然后通过decision节点判断搜到商品则进入在做决定是浏览商品信息还是加入购物车。加入购物车后可以选择进入B继续
 搜索其他商品，或者查看购物车内容，然后购物完后，进入C进行付款，然后流程结束。

另外可以随时接受信号去查看进入A查看购物车信息，也可以随时收到信号去checkout商品。

## 6.3  Activation of Trial Product例子

下面拿uml官方Activation of Trial Product激活试用产品例子介绍

![Activation of Trial Product](https://ask.qcloudimg.com/http-save/yehe-2190306/npqo4p1ej9.png?imageView2/2/w/1620)

首先这个活动图里面由于模型涉及到了Order Management, Customer Service, Customer三个对象，所以使用了垂直的swimlanes。

首先customer请求激活自己正在使用的试用期产品（估计试用期过了，不能使用了），然后顾客服务对象通过fork开启两个流程，一个流程是让Order Management创建产品订单，一个是让用户产生C2V文件。然后Customer Service在 join 处等待两者完成，这里都完成在拿着产品秘钥和C2v文件去激活产品，通过email等把文件传递给用户，用户拿到文件既可以激活，至此活动结束。
