## [简述 Python 类中的 `__init__`、`__new__`、`__call__` 方法](https://www.cnblogs.com/bingpan/p/8270487.html)

任何事物都有一个从创建，被使用，再到消亡的过程，在程序语言面向对象编程模型中，对象也有相似的命运：**创建、初始化、使用、垃圾回收**，不同的阶段由不同的方法（角色）负责执行。

定义一个类时，大家用得最多的就是 `__init__` 方法，而 `__new__` 和 `__call__` 使用得比较少，这篇文章试图帮助大家把这3个方法的正确使用方式和应用场景分别解释一下。

关于 Python 新式类和老式类在这篇文章不做过多讨论，因为老式类是 Python2 中的概念，现在基本没人再会去用老式类，新式类必须显示地继承 object，而 Python3 中，只有新式类，默认继承了 object，无需显示指定，本文代码都是基于 Python3 来讨论。

### `__init__` 方法
`__init__` 方法负责对象的初始化，系统执行该方法前，其实该对象已经存在了，要不然初始化什么东西呢？先看例子：

```python
 1 # class A(object): python2 必须显示地继承object
 2 class A:
 3     def __init__(self):
 4         print("__init__ ")
 5         super(A, self).__init__()
 6 
 7     def __new__(cls):
 8         print("__new__ ")
 9         return super(A, cls).__new__(cls)
10 
11     def __call__(self):  # 可以定义任意参数
12         print('__call__ ')
13 
14 A()
```

输出

```
1 __new__
2 __init__
```

从输出结果来看， `__new__`方法先被调用，返回一个实例对象，接着 `__init__` 被调用。` __call__` 方法并没有被调用，这个我们放到最后说，先来说说前面两个方法，稍微改写成：

```python
 1 def __init__(self):
 2     print("__init__ ")
 3     print(self)
 4     super(A, self).__init__()
 5 
 6 def __new__(cls):
 7     print("__new__ ")
 8     self = super(A, cls).__new__(cls)
 9     print(self)
10     return self
```

输出：

```
1 __new__ 
2 <__main__.A object at 0x1007a95f8>
3 __init__ 
4 <__main__.A object at 0x1007a95f8>
```

从输出结果来看，`__new__` 方法的返回值就是类的实例对象，这个实例对象会传递给 `__init__` 方法中定义的 `self` 参数，以便实例对象可以被正确地初始化。

如果 `__new__` 方法不返回值（或者说返回 `None`）那么 `__init__` 将不会得到调用，这个也说得通，因为实例对象都没创建出来，调用 init 也没什么意义，此外，Python 还规定，`__init__` 只能返回 `None` 值，否则报错，这个留给大家去试。

`__init__` 方法可以用来做一些初始化工作，比如给实例对象的状态进行初始化：

```python
1 def __init__(self, a, b):
2     self.a = a
3     self.b = b
4     super(A, self).__init__()
```
### `__new__` 方法

一般我们不会去重写该方法，除非你确切知道怎么做，什么时候你会去关心它呢，它作为构造函数用于创建对象，是一个工厂函数，专用于生产实例对象。著名的设计模式之一，单例模式，就可以通过此方法来实现。在自己写框架级的代码时，可能你会用到它，我们也可以从开源代码中找到它的应用场景，例如微型 Web 框架 Bootle 就用到了。

```python
1 class BaseController(object):
2     _singleton = None
3     def __new__(cls, *a, **k):
4         if not cls._singleton:
5             cls._singleton = object.__new__(cls, *a, **k)
6         return cls._singleton
```


这就是通过 `__new__` 方法是实现单例模式的的一种方式，如果实例对象存在了就直接返回该实例即可，如果还没有，那么就先创建一个实例，再返回。当然，实现单例模式的方法不只一种，Python之禅有说：

>There should be one-- and preferably only one --obvious way to do it.  
用一种方法，最好是只有一种方法来做一件事

### `__call__` 方法

关于 `__call__` 方法，不得不先提到一个概念，就是可调用对象（callable），我们平时自定义的函数、内置函数和类都属于可调用对象，但凡是可以把一对括号()应用到某个对象身上都可称之为可调用对象，判断对象是否为可调用对象可以用函数 callable

如果在类中实现了 `__call__` 方法，那么实例对象也将成为一个可调用对象，我们回到最开始的那个例子：

```
1 a = A()
2 print(callable(a))  # True
```
a是实例对象，同时还是可调用对象，那么我就可以像函数一样调用它。试试：

```
a()  # __call__
```

很神奇不是，实例对象也可以像函数一样作为可调用对象来用，那么，这个特点在什么场景用得上呢？这个要结合类的特性来说，类可以记录数据（属性），而函数不行（闭包某种意义上也可行），利用这种特性可以实现基于类的装饰器，在类里面记录状态，比如，下面这个例子用于记录函数被调用的次数：

```python
 1 class Counter:
 2     def __init__(self, func):
 3         self.func = func
 4         self.count = 0
 5 
 6     def __call__(self, *args, **kwargs):
 7         self.count += 1
 8         return self.func(*args, **kwargs)
 9 
10 @Counter
11 def foo():
12     pass
13 
14 for i in range(10):
15     foo()
16 
17 print(foo.count)  # 10
```

在 Bottle 中也有 `call ` 方法的使用案例，另外，[stackoverflow](https://stackoverflow.com/questions/5824881/python-call-special-method-practical-example) 也有一些关于 call 的实践例子，推荐看看，如果你的项目中，需要更加抽象化、框架代码，那么这些高级特性往往能发挥出它作用。

### `__del__` 方法

如果c`__new__()` 和 `__init__()` 函数时类的构造函数(即在类实例化时自动执行函数中定义的内容)，那么  `__del__()` 是类的析构函数，是python垃圾回收机制的实际应用，当类的所有引用都被删除后，该类就会被系统从内存中删除，**注意是所有的引用都被删除哦**，而不是每一次删除；

```python
>>> class D(object):
    def __init__(self):
        print 'this is D.__init__()'
    def __del__(self):
        print 'this is D.__del__()'

        
>>> 
>>> d = D()
this is D.__init__()
>>> 
>>> d2 = d
>>> d3 = d
>>> 
>>> del d
>>> del d2
>>> del d3
this is D.__del__()
>>> 
```

将D()实例化对象赋值给d，后d2,d3都是指向D()的这次实例化对象，删除d和d2的引用都不会触发`__del__()`函数，最后一个d3的引用被删除，就会触发`__del__()`，此时D()的这一次实例化的对象就被清除；

 

### 最后

用一段简单的代码，来总体感受一下三个方法的用法和区别：

```python
>>> 
>>> class A(object):
    def __init__(self, x):
        print 'x in __init__', x
    def __new__(cls, y):
        print 'y in __new__', y
        return super(A, cls).__new__(cls)
    def __call__(self, z):
        print 'z in __call__', z
    def __del__(self):
        print 'this is in A.__del__()'

        
>>> 
>>> A('123')('abc')
y in __new__ 123
x in __init__ 123
z in __call__ abc
this is in A.__del__()
>>>
```

由执行结果可以看出，虽然`__init__()`方法定义在`__new__()`方法之前，但是结果中先展示了`__new__()`方法的执行结果.