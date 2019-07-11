## [一文带你完全理解Python中的metaclass](https://www.jianshu.com/p/224ffcb8e73e)

### 1. Class 也是 Object
在理解metaclass之前，我们需要先理解Python中的class。从某种程度上来说，Python中的class的定位比较特殊。  
对于大部分面向对象语言来说，class是一段定义了如何产生object的代码块。在Python中这一定义也成立：  

```python
>>> class example(object):
...     pass
...
>>> object1 = example()
>>> print(object1)
<__main__.example object at 0x102e26990>
```

但是在Python中，class并不只有这一角色。class实际上也是object。当我们使用class定义一个类的时候，Python会执行相应代码并在内存中创建一个名为example的object。
但该object(class)是具有创建其他object(instance)的能力的。这也是这个object是一个class的原因。由于本质上class任然是一个object，所以我们可以对class做出以下操作：

- 我们可以将其赋给一个变量
- 我们可以对其进行拷贝
- 我们可以赋给其新的变量
- 我们可以将其作为参数赋给其他的函数

举例如下：

```python
# print a class since it's an object
>>> print(example)
<class '__main__.example'>

# assign an attribute to the class
>>> print(hasattr(example, 'new_attribute'))
False
>>> example.new_attribute = 'assign an attribute to the class'
>>> print(hasattr(example, 'new_attribute'))
True
>>> print(example.new_attribute)
assign an attribute to the class

# assign the class to a variable
>>> example_mirror = example
>>> print(example_mirror)
<class '__main__.example'>
>>> print(example_mirror())
<__main__.example object at 0x102e26a90>

# pass class as a parameter
>>> def echo(cls):
...     print(cls)
...
>>> echo(example)
<class '__main__.example'>
```

### 2. 动态创建class
既然class也是object，那么我们就可以像创建普通的object一样动态创建class。  
第一种方法，我们可以在方法中创建class。如下面的例子所示：  

```
>>> def dynamic_class_creater(name):
...     if name == 'name1':
...         class class1(object):
...             pass
...         return class1
...     else:
...         class class2(object):
...             pass
...         return class2
...
>>> first_class = dynamic_class_creater('name1')
>>> print(first_class)
<class '__main__.class1'>
>>> print(first_class())
<__main__.class1 object at 0x10e4149d0>
```

但通过这种方式创建class并没有特别动态。我们任然需要自己定义类的具体内容。考虑到class也是object，那么也一定有某种方法能够像产生instance一样产生类。
当我们使用class关键字创建类的时候，Python会自动创建对应的object。像Python中其他大多数情况一样，我们也可以手动创建这个class object。这一操作可以通过`type()`实现。  

通常情况下我们可以调用type来得到一个object的类型是什么。如下面的例子所示：

```python
>>> print(type(1))
<type 'int'>

>>> print(type('str'))
<type 'str'>

>>> print(type(example()))
<class '__main__.example'>

>>> print(type(example))
<type 'type'>
```

在这里我们看到我们所**创建example类的type是'type'**。这实际上也就是接下来要讨论的内容。既type的完全不同的功能——type可以动态创建class。type()函数可以接收class的描述来作为参数并返回所生成的class object。type同时具有这两个迥异的功能是由于Python兼容性问题导致的。在此我们不做深究。
当使用type创建class时，其用法如下：
```
type(class_name, tuple_of_parent_class, dict_of_attribute_names_and_values)
```
其中第二个参数tuple_of_parent_class用来表示继承关系，可以为空。第三个参数用来描述我们所要创建的类所应该具有的attribute。如下面的例子所示：

```python
>>>class class_example(object):
...     pass
```

上面定义的这个类可以由如下type函数创建：

```python
>>>class_example = type('class_example', (), {}) # create a class on the fly
>>>print(class_example)
<class '__main__.class_example'>
>>> print(class_example()) # get a instance of the class
<__main__.class_example object at 0x10e414b10>
```

在这个例子中，type所接收的第一个参数'class_example'是该类的类名，同时我们使用了class_example作为存储该class object引用的变量。这二者可以不同。但一般我们没有理由采用不同的名字从而使得代码更加复杂。  

我们也可以使用一个字典来定义所创建的class的attribute：

```python
>>> class_example = type('class_example', (), {'attr': 1})
>>> print(class_example)
<class '__main__.class_example'>
>>> print(class_example.attr)
1
>>> print(class_example())
<__main__.class_example object at 0x10e414a90>
>>> print(class_example().attr)
1
```

上面的例子中type返回的class等同于下面这个class：

```python
>>> class class_example(object):
...     attr = 1
```

当然，我们也可以用type返回一个继承class_example的类：

```python
>>> child_example = type('child_example', (class_example,), {})
>>> print(child_example)
<class '__main__.child_example'>
>>> print(child_example.attr)
1
```

上面这个例子中type返回的class等同于如下class：

```python
>>> class child_example(class_example):
...     pass
```

我们甚至可以动态创建包括方法的类。只要我们创建好方法并将其赋给相应的attribute即可：

```python
>>> def echo(self):
...     print(self.attr)
...
>>> child_example = type('child_example', (class_example,), {'echo': echo})
>>> hasattr(class_example, 'echo')
False
>>> hasattr(child_example, 'echo')
True
>>> child_example().echo()
1
```

同样，我们也可以先动态创建一个class，然后再赋给其新的方法：

```python
>>> child_example = type('child_example', (class_example,), {})
>>> def another_method(self):
...     print('another method')
...
>>> child_example.another_method = another_method
>>> hasattr(child_example, 'another_method')
True
>>> child_example().another_method()
another method
```

综上所述，Python中的class其实是一个object，并且我们可以动态创建class。事实上这也是我们在使用class关键字的时候Python所做的事情。Python通过使用metacalss来实现这一过程。

### 3. 究竟什么是metaclass？

**metaclass就是Python中用来创建class object的class**。我们可以将其看做能够产生class的类工厂。我们可以通过如下例子理解这个关系：

```python
class = metaclass()
object = class()
```

从上文中我们知道了`type()`可以被用来动态创建class，这是因为实际上type是一个metaclass。而且type实际上是Python用在在幕后创建所有class的metaclass。
包括int, string, function, class在内，Python中所有的东西都是object，而所有的object都是被相应的class创造的。我们可以通过`__class__`的值得知这一点。

```python
>>> age = 24
>>> age.__class__
<type 'int'>

>>> name = 'bob'
>>> name.__class__
<type 'str'>

>>> def foo(): pass
>>> foo.__class__
<type 'function'>

>>> class Bar(object): pass
>>> bar = Bar()
>>> bar.__class__
<class '__main__.Bar'>
```

那么，这些__class__的__class__又是什么呢？

```python
>>> age.__class__.__class__
<type 'type'>
>>> name.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> bar.__class__.__class__
<type 'type'>
```

可以看出，所有的class都来自于type。type，作为metaclass，创建了以上所有的class object。
**type是Python定义好的metaclass**。当然，我们也可以自定义metaclass。

### 4. 类的__metaclass__ attribute
当定义class的时候，我们可以使用__metaclass__ attribute来指定用来初始化当前class的metaclass。如下面的例子所示：

```python
class Foo(object):
    __metaclass__ = something
    [other statements...]
```

如果我们指定了`__metaclass__`，Python就是使用这个metaclass来生成class Foo。
当Python试图创建class Foo的时候，Python会首先在class的定义中寻找`__metaclass__` attribute。如果存在`__metaclass__`，Python将会使用指定的`__metaclass__`来创建class Foo。如果没有指定的话，Python就会使用默认的type作为metaclas创建Foo。
所以，对于下面这个例子：

```python
class Foo(Bar):
    pass
```

Python首先在Foo中寻找是否存在`__metaclass__` attribute。
- 如果存在的话，Python将使用这个metaclass在内存中创建一个名字为Foo的class object。
- 如果class定义中不存在`__metaclass__`的话，Python将会寻找MODULE级别的`__metaclass__`。如果存在的话就进行与前述相同的操作。但是只有我们定义的class没有继承任何类的情况下，Python才会在MODULE级别寻找`__metaclass__`。或者说，只有当该类是一个旧类的情况下，Python才会在MODULE级别寻找`__metaclass__`。（关于新类和旧类的区别，请看*[这篇文章](https://www.jianshu.com/p/14b8ebf93b73)*）.
- 当Python仍然没有找到`__metaclass__`时，Python将会使用当前类的母类的metaclass来创建当前类。在我们上面这个例子中，Python会使用Foo的母类Bar的metaclass来创建Foo的class object。

同时需要注意的是，在class中定义的`__metaclass__` attribute并不会被子类继承。被子类继承的是母类的metaclass，也就是母类的`.__class__` attribute。比如上面的例子中，`Bar.__class__`将会被Foo继承。也就是说，如果Bar定义了一个`__metaclass__` attribute来使用type()创建Bar的class object（而非使用`type.__new__()`），那么Bar的子类，也就是Foo，并不会继承这一行为。

> 那么问题来了：我们究竟应该在`__metaclass__` attribute中定义什么？

答案是：能够创建class的东西。

那么什么能够创建class呢？type，或者任何type的子类。

### 5. 自定义metaclass
metaclass的主要目的是在class被创建的时候对生成的class进行自动的动态修改。
一般来说，这一点主要应用于API，例如我们想要根据当前的内容创建相匹配的class。
举一个简单的例子如下：我们决定让当前module下所有的class的attribute的名字都是大写。要实现这个功能有很多种方法。使用`__metaclass__`就是其中之一。
设置了`__metaclass__`的话，class的创建就会由指定的metaclass处理，那么我们只需要让这个metaclass将所有attribute的名字改成大写即可。
`__metaclass__`可以是任何Python的callable，不必一定是一个正式的class。
下面我们首先给出一个使用function作为`__metaclass__`的例子。

```python
# the metaclass will automatically get passed the same argument 
# that is passed to `type()`
def upper_attr(class_name, class_parents, class_attr):
    '''Return a class object, with the list of its attribute turned into 
    uppercase.
    '''
    # pick up any attribute that doesn't start with '__' and turn it into uppercase.
    uppercase_attr = {}
    for name, val in class_attr.items():
        if name.startswith('__'):
            uppercase_attr[name] = val
        else:
            uppercase_attr[name.upper()] = val
    
    # let `type` do the class creation
    return type(class_name, class_parents, uppercase_attr)


class Foo(object):
    # this __metaclass__ will affect the creation of this new style class
    __metaclass__ = upper_attr
    bar = 'bar'


print(hasattr(Foo), 'bar')
# False

print(hasattr(Foo), 'BAR')
# True

f = Foo()
print(f.BAR)
# 'bar'
```

接下来我们通过继承type的方式实现一个真正的class形式的metaclass。注意如果尚不清楚`__new__`和`__init__`的作用和区别的，请看*[这篇文章](https://www.jianshu.com/p/14b8ebf93b73)*.

```python
# remember that `type` is actually a just a class like int or str
# so we can inherit from it.

class UpperAttrMetaclass(type):
    '''
    __new__ is the method called before __init__
    It's the function that actually creates the object and returns it.
    __init__ only initialize the object passed as a parameter.
    We rarely use __new__, except when we want to control how the object
    is created.
    For a metaclass, the object created is a class. And since we want to 
    customize it, we need to override __new__.
    We can also do something by overriding __init__ to get customized initialization
    process as well.
    Advanced usage involves override __call__, but we won't talk about this here.
    '''
    def __new__(upperattr_metaclass, class_name, class_parents, class_attr):
        uppercase_attr = {}
        for name, val in class_attr.items():
            if name.startswith('__'):
                uppercase_attr[name] = val
            else:
                uppercase_attr[name.upper()] = val
        return type(class_name, class_parents, uppercase_attr)
```

但这不是很OOP。我们直接调用了type而非调用type.__new__。那么OOP的做法如下。

```python
class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, class_name, class_parents, class_attr):
        uppercase_attr = {}
        for name, val in class_attr.items():
            if name.startswith('__'):
                uppercase_attr[name] = val
            else:
                uppercase_attr[name.upper()] = val
        # basic OOP. Reuse the parent's `__new__()`
        return type.__new__(upperattr_metaclass, class_name, class_parents, uppercase_attr)
```

我们注意到，`__new__`所接收的参数中有一个额外的upperattr_metaclass。这没有什么特别的。如同`__init__`总是接收调用它的object作为第一个参数一样（惯例上用self来命名`__init__`所接收的第一个参数），`__new__`总是接收其被定义在内的class作为第一个参数，就像类方法总是接收其被定义的class作为第一个参数一样（惯例上用cls命名类方法所接收的第一个参数）。

清楚起见，这里给出的例子的变量和方法名都很长。但在实际的应用中，类似于使用self和cls代替第一个参数，我们可以将这些名字替换为更加简洁的形式：
```python
class UpperAttrMetaclass(type):
    def __new__(cls, cls_name, bases, attr_dict):
        uppercase_attr = {}
        for name, val in attr_dict.items():
            if name.startswith('__'):
                uppercase_attr[name] = val
            else:
                uppercase_attr[name.upper()] = val
        return type.__new__(cls, cls_name, bases, uppercase_attr)
```

通过应用super，我们可以使得上面这段代码更加干净简洁，也使得继承更加容易（我们可能有metaclass继承别的一些metaclass，而这些metaclass又继承type）：

```python
class UpperAttrMetaclass(type):
    def __new__(cls, cls_name, bases, attr_dict):
        uppercase_attr = {}
        for name, val in attr_dict.items():
            if name.startswith('__'):
                uppercase_attr[name] = val
            else:
                uppercase_attr[name.upper()] = val
        return super(UpperAttrMetaclass, cls).__new__(cls, cls_name, bases, uppercase_attr)
```

Voilà！上述基本就是关于metaclass的一切了。  
使用metaclass之所以复杂，不是因为其代码实现复杂，而是因为我们一般使用metaclass来做一些逻辑上很复杂的操作，例如自省，修改继承以及改变类的默认attribute如`__dict__`等。  
metaclass的确可以被用来实现一些奇妙的功能，也因此可以用来进行极其复杂的逻辑操作。但是metaclass本身是很简单的：

- 影响class初始化的过程
- 修改class的内容
- 返回修改过的class

### 6. 为什么我们要使用metaclass，而不是使用一些函数来实现类似的功能？
就像前文所说，`__metaclass__`实际上可以是任何callable，那么为什么我们还要使用metaclass而不是直接调用这些函数呢？

使用class作为metaclass有如下几个理由：

使用class作为metaclass能够使得我们代码的动机更加明确。比如当我们读到上面所定义的UpperAttrMetaclass(type)代码时，我们清楚地知道接下来这段代码想要干什么（自定义class object初始化的过程）。  
我们能够使用OOP的思想进行处理。class作为metaclass可以继承其他的metaclass，重载母类的方法，甚至可以使用别的metaclass。  
如果我们使用class作为metaclass，某一使用该metaclass的class的子类将仍是是其metaclass的实例。但这一功能无法通过使用函数作为metaclass实现。  
使用metaclass可以使得代码结构更加优美。实际应用中我们很少使用metaclass来实现上面那样简单的功能。使用metaclass往往是为了实现非常复杂的操作。如果使用class作为metaclass，我们就可以把相应的方法封装到这一个metaclass中，使得代码更加易懂。  
使用class作为metaclass可以在class中容易的定义`__new__`，`__init__`，`__call__`方法。虽然我们在将所有的逻辑都放入`__new__`中，但有的时候根据需要使用其他几个方法会使得逻辑更加清晰。  
额贼！人家名字就叫metaclass。这不是带着个class吗？

### 7. 为什么我们要使用metaclass呢？
那么究竟为什么我们要使用metaclass这样一个难以理解且容易出错的实现方式呢？  
答案是通常情况下我们不需要使用metaclass。  
引用Python大师Tim Peters的话来说，就是：  

>Metaclasses are deeper magic that 99% of users should never worry about. If you wonder whether you need them, you don't (the people who actually need them know with certainty that they need them, and don't need an explanation about why).

metaclass主要的使用情况就是用来创建API。使用metaclass的一个典型的例子是Django ORM。
它是的我们可以使用如下当时定义一个model：

```python
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

同时，如果我们调用这个model:

```python
guy = Person(name='bob', age='35')
print(guy.age)
```

其并不会返回一个IntegerField对象，而是会返回一个int，甚至可以直接从数据库中调用这个值。  
正是因为models.Model定义了`__metaclass__`，并使用了一些操作来将我们使用简单的语句定义的Person转化成了与数据库相应的域相联系的类，这种逻辑才成为可能。  
Django使得很多复杂的逻辑仅暴露一个简单的API接口就可以调用，这正是通过metaclass实现的。metaclass会根据需要重新实现这些复杂操作所需要的真正的代码。  

### 8. 再说两句  
首先我们知道了Python中的class实际上是object，同时class仍具有创建对应的实例的能力。
实际上class本身也是metaclass的实例。

```python
>>> class Foo(object):
...     pass
...
>>> id(Foo)
4299321816
```

Python中的任何东西都是object，这些object不是class的实例就是metaclass的实例。  
当然，type除外。  
type事实上是其自身的metaclass。我们使用Python是无法重复这种实现的。这一逻辑是在Python代码实现的层面定义的。引用一下道德经中的说法，<u>我们可以说Python中type生metaclass，metaclass生class，class生万物</u>。  
另外，metaclass的应用一般颇为复杂，大多数情况下我们可以使用别的方法实现相同的功能。比如我们可以通过一下两种技术修改class：

- monkey patching
- class decorators

99%我们需要改变class的情况下，我们使用上述两种技术可以解决。  
但事实是，99%的情况下我们根本不需要改变class。

## [python当中__metaclass__探讨](http://python.jobbole.com/86566/)

最初博主是希望在 python 当中创建一个单列模式的类，因为 python 当中不像 java 和 php 当中有权限修饰符(private)，所以实现起来要绕一点。

网上找了一下python实现单列模式，类似的大概有这种方法：

```python
class singleton(type):
    """
    实现单列模式的元类
    总之，metaclass的主要任务是：
    拦截类，
    修改类，
    返回类
    """

    def __init__(cls,classname,parrentstuple,attrdict):
        """
        """
        super(SigleInstance,cls).__init__(classname,parrentstuple,attrdict)
        cls._instance = None

    def __call__(self,*args,**kargs):
        """
        """
        if self._instance:
            return self._instance
        else:
            self._instance = super(SigleInstance,self).__call__(*args,**kargs)
            return self._instance
```

这就是单例的元类，我把它小写了，因为type也是小写的。然后呢，在即将要实现单例的class当中这样写：

```python
class Earth(object):
    __metaclass__ = singleton
    def __init__(self,a,b):
        pass
```

这样每次 创建一个 Earth()取得的始终都应该是一个实例。

关于 `__metaclass__` 和 `type` 这个东西可以参考*[深入理解Python中的元类(metaclass)](http://www.jb51.net/article/61138.htm)*。这篇文章解决了我大部分的疑惑，但是我还是没有搞清楚的是：

当 `__metaclass__` 是一个类的时候，metaclass 是怎样去创建一个类的？

在这之前首先说明一下：

### 一、python当中一切都是对象

python当中一切都是对象，而对象都是由类创建，这里为了区分概念，我们不妨换一种说法：实例都是由模板创建的。

### 二、那么什么又是对象的type呢？

type 就是类型的意思。如果您对 java 稍微有一点了解。你会有这样的认识：

```java
/**
* language是一个String类型的变量，值为"python"
* 在java当中，如果 Integer language = "python"就是错误的
*/
String language = "python";
```

由于python是一门动态语言，所以在写代码的时候不必声明变量的类型，也不可能完全确定这个变量是什么类型，除非对自己代码的逻辑以及流程非常清楚，另外python在运行当中变量的类型是可以更改的。但是不能确定变量的类型，不代表就没有类型啊。python当中的变量一样是有类型的。那么怎么来看变量的类型呢？

*答案是使用type*。

```python
language = "python"
print type(language)
# python2.7中输出：<type 'str'>
# ipython 输出 str

number = 2
print type(number)
#输出:<type 'int'>

class A(object):
    pass

a = A()
print type(a)
#输出:<type '__main__.A'>
```

上面段代码分别用type查看到了各个变量的类型。根据（一）【python当中一切都是对象，而对象都是由类创建，这里为了区分概念，我们不妨换一种说法：实例都是由模板创建的】我们可不可以这样说呢：language 是 str 的实例，str 是 language实例的模板。因此`type（a_var）`的输出就是a_var这个实例的模板。所以我们看到 `type(a)` 的输出是，也就是说 a 实例的模板是 A。

class A的模板是什么呢？

```python
print type(A)
#输出:<type 'type'>
```

也就是说，一个类的模板的type，类是type的一个实例，tpye实例化了一个对象，这个对象就是class。所以在python的世界里，一切都是对象，类也是对象。

那么有意思的地方来了，type的模板是什么呢，也就是，type的type是什么呢？

```python
print type(type)
# 输出<type 'type'>
```

是不是很有意思，type的type是type。很绕，换成大白话说：type的模板是type自己。那么是不是就可以这样说呢？TYPE（type，为了区分说明，故意大写）是type的模板，type是TYPE的实例，因此说明type是一个实例；而TYPE是一个模板，也就是一个类！，因为TYPE==type，那么可以得出结论：

> type是一个类（class），type也是自身的实例（instance）

python当中一切都是对象，类也是对象，对于type来说，更为特殊，因为type的模板是type，也就是说，type自己创建了自己，type是自身的实例。

### 三、实例是由类模板创建

实例是由类模板创建（也就是我们平时所写的class），而类是由元类模板创建（就是`__metaclass__`指定的类）。所以【元类和类的关系】就类似于【实例和类的关系】。

根据博主所探讨的结果表明，`__metaclass__`在创建类的过程大概是这样的：当类Earth的实例 earth正要被创建的时候，

查找Earth当中是否有`__metaclass__`,如果没有查找父类是否有`__metaclass__`，如果没有找到，就看包当中是否有`__metaclass__`，如果还是没有，那直接使用type创建该类。如果找到了，就用该`__metaclass__`来创建类。

那么如果找了`__metaclass__`,那么系统首先创建一个`__metaclass__`的实例，而这个由metaclass创建的实例正好的一个 Earth类，注意是Earth类（class），而不是一个Earth的一个实例哦。

那么到这一步究竟发生了些什么呢？我们写几行代码来看一看：

```python
#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 the module's duty
""" 
#---------- code begins below -------

class SimpleMetaClass(type):
    
    def __init__(self,*args,**kwargs):
        print "you have create a class instance by metaclass"
        super(SimpleMetaClass,self).__init__(*args,**kwargs)

class Earth(object):
    
    __metaclass__ = SimpleMetaClass

    def sayHello():
        print "hello world"


if __name__ == "__main__":
    
    print "do something that have nothing with SimpleMetaClass and Earth"
```

最后运行的结果是这样的：

```
you have create a class instance by metaclass                 #①  
do something that have nothing with SimpleMetaClass and Earth #②
```

 
通过这个小例子我们看到：我们并没有使用过 Earth类，也没有使用过SimpleMetaClass这个元类，但实际的结果看来，SimpleMetaClass这个模板确被使用过了，因为打印出了①，后面我们会知道，打印出①是因为python使用SimpleMetaClass模板来创建出了Earth这个类对象（不是Earth的一个实例）。这个过程我们可以用我们平常经常说的一句话来描述：这个步骤相当于实例化了一个metaclass（SimpleMetaClass）对象，而这个对象正好是Earth类。

那么这里肯定会有人问了：我平时写class的时候都是不带__metaclass__的啊？那是因为如果你不写__metaclass__，最终这个类的模板就是type。上面的代码可以看到SimpleMetaClass是继承自type的。

### 四、Earth类已经被metaclass所创建出来了，那么当实例化一个Earth类（也就是创建一个earth对象）的时候又发生了什么呢？

在说明这个问题之前，我们得先聊一聊`__call__`,`__new__`这两个特殊方法。对于一个实现了`__call__`的类，那么它的实例可以当做函数来调用。来看个例子：

```python
class MagicCall(object):

    def __new__(cls,name):
        return super(MagicCall,cls).__new__(cls)

    def __init__(self,name):
        self.name=name

    def __call__(self):
        print "you have invoked __call__ method...."

if __name__ == '__main__':
    magicCall = MagicCall("python")
    magicCall()

#输出的结果为：you have invoked __call__ method....
```

而`__new__`有拦截类实例化的功能，在创建一个对象的过程中，执行`__init__`方法时，解释器已经为对象分配了内存，实例已经存在了，`__init__`方法只是改变这个类当中的某些参数。而在执行`__new__`方法时，这个实例是不存在的，而`__new__`就是要创建这个实例，所以`__new__`必须要有返回值。

现在我们回过头来想一想：为什么创建 一个类的实例是这种写法：

```python
instance = SomeClass()
instance = SomeClass(args1,args2,...)
```

回答这个问题，我们可以用元类来解释。我们知道类是元类的一个对象，而元类的实例都有一个`__call__`方法。拥有`__call__`方法的对象可以把对象当做一个函数调用。所以喽，我们在创建一个类的实例的时候，实际上是调用了类对象的`__call__(MetaClass:__call__)`这个方法。

来看一个比较长的例子：

```python
#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 the module's duty
""" 
#---------- code begins below -------

class SimpleMetaClass(type):
    
    def __new__(cls,*args,**kwargs):
        print "creating class Earth..."
        return  super(SimpleMetaClass,cls).__new__(cls,*args,**kwargs)

    def __init__(self,*args,**kwargs):
        print "you have create a class instance by metaclass"
        super(SimpleMetaClass,self).__init__(*args,**kwargs)

    def __call__(self,*args,**kwargs):
        print "__call__ in metaclass has been invoked...","the args:",args,kwargs
        return super(SimpleMetaClass,self).__call__(*args,**kwargs)

    
class Earth(object):
    
    __metaclass__ = SimpleMetaClass

    def __new__(cls,g,R=65535):
        print "creating instance using __new__"
        cls.g = g
        cls.R = R
        return super(Earth,cls).__new__(cls);

    def __init__(self,g,R=65535):
        print "initializing instance in __init__"
        print "gravity on Earth is:%f" % self.g

    def __call__(self):
        print self.g 

    def sayHello(self):
        print "hello earth,your gravity is:%f" % self.g


if __name__ == "__main__":
    
    earth = Earth(9.8,R=65535)
    earth()
    earth.sayHello()
```    

 
不知道大众喜欢在代码中写注释的方式来讲解，还是直接写文字过程。我就写文字过程吧。

最终上面这段代码执行的结果是：


```
①creating class Earth...
②you have create a class instance by metaclass
③__call__ in metaclass has been invoked... the args: (9.8,) {'R': 65535}
④creating instance using __new__
⑤initializing instance in __init__
⑥gravity on Earth is:9.800000
⑦9.8
⑧hello earth,your gravity is:9.800000
```
 
我们来慢慢分析。

首先python创建SimpleMetaClass类，这个SimpleMetaClass是元类，应该是由type创建的。  
当创建Earth这个类时，找到了它类中有__metaclass__属性，于是，采用SimpleClass来创建这个类
创建Earh类时，解释器会把类名，父类元祖，类的属性三个参数传给SimpleMetaClass
SimpleMetaClass 根据` clazzName,(parent2,parent1,..),{‘attribute’:….,’method’:”}`在自己`__new__`方法中创建出这个Earth实例【打印出①】，然后调用自己的`__init__`方法初始化类的参数【打印出②】。这时，这个Earth类作为metaclass的一个实例就被创建好了。
接下来通过 `earth = Earth(9.8,R=65535)` 创建一个Earth对象实例earth。这一步实际上是调用 Earth这个类对象的`__call__（SimpleMetaClass::__call__）`方法来创建一个Earth的实例。【打印出③，我们还能看到调用`__call__`的参数】。
而创建earth实例的方法`__new__(Earth::__new__),和__init__(Earth:__init__)`,将会在Earth实例中的`__call__（SimpleMetaClass::__call__）`当中先后得以执行【先后打印出④⑤⑥】执行完成Earth实例earth对象被返回。
我想⑦⑧大家应该很容易理解了。

以上就是我对元类的理解，其中如有错误的地方还请大家斧正。


