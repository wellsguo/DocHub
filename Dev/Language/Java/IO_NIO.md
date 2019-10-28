# [文件IO与网络IO（NIO）]()

学习Java IO的时候，被文件io与网络io搞得迷迷糊糊，查询网上的一些资料，这里总结一下。

IO，其实意味着：数据不停地搬入搬出缓冲区而已（使用了缓冲区）。比如，用户程序发起读操作，导致“ syscall read ”系统调用，就会把数据搬入到 一个buffer中；用户发起写操作，导致 “syscall write ”系统调用，将会把一个 buffer 中的数据 搬出去(发送到网络中 or 写入到磁盘文件)。DMA(Direct Memory Access，直接内存存取，不需要CPU参与) 是所有现代电脑的重要特色，它允许不同速度的硬件装置来沟通，而不需要依赖于 CPU 的大量中断负载。

## IO 过程流程

1) 程序员写代码创建一个缓冲区（这个缓冲区是用户缓冲区）：哈哈。然后在一个while循环里面调用read()方法读数据(触发"syscall read"系统调用)
```java
byte[] b = new byte[4096];

while((read = inputStream.read(b))>=0) {
    total = total + read;
    // other code....
}
```
2) 当执行到read()方法时，其实底层是发生了很多操作的：  

① 内核给磁盘控制器发命令说：我要读磁盘上的某某块磁盘块上的数据。--kernel issuing a command to the disk controller hardware to fetch the data from disk.  

② 在DMA的控制下，把磁盘上的数据读入到内核缓冲区。--The disk controller writes the data directly into a kernel memory buffer by DMA.  

③ 内核把数据从内核缓冲区复制到用户缓冲区。--kernel copies the data from the temporary buffer in kernel space.  

> 这里的用户缓冲区应该就是我们写的代码中 new 的 byte[] 数组。

操心系统的核心是内核，独立于普通的应用程序，可以访问受保护的内存空间，也有访问底层硬件设备的所有权限。为了保证用户进程不能直接操作内核，保证内核的安全，操心系统将虚拟空间划分为两部分，一部分为内核空间，一部分为用户空间。针对linux操作系统而言，将最高的1G字节（从虚拟地址0xC0000000到0xFFFFFFFF），供内核使用，称为内核空间，而将较低的3G字节（从虚拟地址0x00000000到0xBFFFFFFF），供各个进程使用，称为用户空间。每个进程可以通过系统调用进入内核，因此，Linux内核由系统内的所有进程共享。

对于操作系统而言，JVM只是一个用户进程，处于用户态空间中。而处于用户态空间的进程是不能直接操作底层的硬件的。而 IO 操作就需要操作底层的硬件，比如磁盘。因此，IO 操作必须得借助内核的帮助才能完成(中断，trap)，即：会有用户态到内核态的切换。

我们写代码 new byte[] 数组时，一般是都是“随意” 创建一个“任意大小”的数组。比如，new byte[128]、new byte[1024]、new byte[4096]....，即用户缓冲区，但是，对于磁盘块的读取而言，每次访问磁盘读数据时，并不是读任意大小的数据的，而是，每次读一个磁盘块或者若干个磁盘块(这是因为访问磁盘操作代价是很大的，而且我们也相信局部性原理) 因此，就需要有一个“中间缓冲区”--即内核缓冲区。先把数据从磁盘读到内核缓冲区中，然后再把数据从内核缓冲区搬到用户缓冲区。这也是为什么我们总感觉到第一次read操作很慢，而后续的read操作却很快的原因吧。因为，对于后续的read操作而言，它所需要读的数据很可能已经在内核缓冲区了，此时只需将内核缓冲区中的数据拷贝到用户缓冲区即可，并未涉及到底层的读取磁盘操作，当然就快了。

![](https://img-blog.csdnimg.cn/2018122416430814.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTQ0Njk4MA==,size_16,color_FFFFFF,t_70)

## NIO 内存映射 

![](https://img-blog.csdnimg.cn/20181224164822170.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTQ0Njk4MA==,size_16,color_FFFFFF,t_70)

内核空间的 buffer 与 用户空间的 buffer 都映射到同一块物理内存区域。当用户进程访问“内存映射文件”（即用户缓存）地址时，自动产生缺页错误，然后由底层的OS负责将磁盘上的数据送到物理内存区域，用户访问用户空间的 buffer时，直接转到物理内存区域，这就是直接内存映射IO，也即JAVA NIO中提到的内存映射文件，或者说 直接内存....总之，它们表达的意思都差不多。

## NIO zerocopy 技术

IO操作需要数据频繁地在内核缓冲区和用户缓冲区之间拷贝，而zerocopy技术可以减少这种拷贝的次数，同时也降低了上下文切换(用户态与内核态之间的切换)的次数。

### 传统 IO 数据拷贝

比如，大多数WEB应用程序执行的一项操作就是：接受用户请求 &#8594; 从本地磁盘读数据 &#8594; 内核缓冲区 &#8594; 用户缓冲区 &#8594; 用户程序 &#8594; 用户缓冲区 &#8594; 内核缓冲区 &#8594; NIC缓冲区（网卡缓冲区） &#8594; 操作系统发送，数据每次在内核缓冲区与用户缓冲区之间的拷贝会消耗CPU以及内存的带宽。而zerocopy有效减少了这种拷贝次数。

![](https://img-blog.csdnimg.cn/201812241655020.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTQ0Njk4MA==,size_16,color_FFFFFF,t_70)

这里经历了四次数据copy和四次上下文切换（用户态与内核态之间的切换）：

- 第一次上下文切换发生在 read()方法执行，表示服务器要去磁盘上读文件了，这会导致一个 sys_read()的系统调用。此时由用户态切换到内核态，完成的动作是：DMA把磁盘上的数据读入到内核缓冲区中（这也是第一次拷贝）。

- 第二次上下文切换发生在read()方法的返回(这也说明read()是一个阻塞调用)，表示数据已经成功从磁盘上读到内核缓冲区了。此时，由内核态返回到用户态，完成的动作是：将内核缓冲区中的数据拷贝到用户缓冲区（这是第二次拷贝）。

- 第三次上下文切换发生在 send()方法执行，表示服务器准备把数据发送出去了。此时，由用户态切换到内核态，完成的动作是：将用户缓冲区中的数据拷贝到内核缓冲区(这是第三次拷贝)

- 第四次上下文切换发生在 send()方法的返回【这里的send()方法可以异步返回，所谓异步返回就是：线程执行了send()之后立即从send()返回，剩下的数据拷贝及发送就交给底层操作系统实现了】。此时，由内核态返回到用户态，完成的动作是：将内核缓冲区中的数据送到 protocol engine.（这是第四次拷贝）

当需要传输的数据远远大于内核缓冲区的大小时，内核缓冲区就会成为瓶颈。这也是为什么 zerocopy 技术合适大文件传输的原因。内核缓冲区为啥成为了瓶颈？

### zerocopy 数据拷贝

![](https://img-blog.csdnimg.cn/20181224165855142.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zOTQ0Njk4MA==,size_16,color_FFFFFF,t_70)

当 `transferTo()` 方法被调用时，由用户态切换到内核态。完成的动作是：DMA 将数据从磁盘读入 Read buffer中(第一次数据拷贝)。然后，还是在内核空间中，将数据从 Read buffer 拷贝到 Socket buffer(第二次数据拷贝)，最终再将数据从 Socket buffer 拷贝到 NIC buffer(第三次数据拷贝)。然后，再从内核态返回到用户态。上面整个过程就只涉及到了：三次数据拷贝和二次上下文切换。感觉也才减少了一次数据拷贝嘛。但这里已经不涉及用户空间的缓冲区了。三次数据拷贝中，也只有一次拷贝需要到CPU的干预。（第2次拷贝），而前面的传统数据拷贝需要四次且有三次拷贝需要CPU的干预。

如果底层的网络硬件以及操作系统支持，还可以进一步减少数据拷贝次数 以及 CPU干预次数。

![](https://img-blog.csdnimg.cn/2018122417035441)

从上图看出：这里一共只有 `两次拷贝` 和 `两次上下文切换`。而且这两次拷贝都是 DMA copy，并不需要CPU干预(严谨一点的话就是不完全需要吧.)。

整个过程如下：用户程序执行 transferTo()方法，导致一次系统调用，从用户态切换到内核态。完成的动作是：DMA将数据从磁盘中拷贝到Read buffer，用一个描述符（Descriptor）标记此次待传输数据的地址以及长度，DMA直接把数据从Read buffer 传输到 NIC buffer。数据拷贝过程都不用CPU干预了。
