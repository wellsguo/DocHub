## 创建 Java 对象

1. 如何封装一个 Java 对象
2. 如何编写 equals / hashCode 函数
3. 如何让对象不可变，其中尤其注意 trackId 的限定符 final 的用法[[1](https://www.cnblogs.com/dotgua/p/6357951.html)]。

```java
package com.example.android.uamp.model;

import android.support.v4.media.MediaMetadataCompat;
import android.text.TextUtils;

/**
 * Holder class that encapsulates a MediaMetadata and allows the actual metadata to be modified
 * without requiring to rebuild the collections the metadata is in.
 */
public class MutableMediaMetadata {

    public MediaMetadataCompat metadata;
    public final String trackId;

    public MutableMediaMetadata(String trackId, MediaMetadataCompat metadata) {
        this.metadata = metadata;
        this.trackId = trackId;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || o.getClass() != MutableMediaMetadata.class) {
            return false;
        }

        MutableMediaMetadata that = (MutableMediaMetadata) o;

        return TextUtils.equals(trackId, that.trackId);
    }

    @Override
    public int hashCode() {
        return trackId.hashCode();
    }
}
```

## 补充 —— final 用法

### 修改变量  
在编写程序时，我们经常需要说明一个数据是不可变的，我们将其称之为常量。在java中，用final关键字修饰的变量，**只能进行一次赋值操作**，并且在生存期内不可以改变它的值。更重要的是，final会告诉编译器，这个数据是不会修改的，那么编译器就可能会在编译时期就对该数据进行替换甚至执行计算，这样可以对我们的程序起到一点优化。不过在针对基本类型和引用类型时，final关键字的效果存在细微差别。

```java
class Value {
    int v;
    public Value(int v) {
        this.v = v;
    }
}
public class FinalTest {   
    final int f1 = 1;
    final int f2;
    public FinalTest() {
        f2 = 2;
    }
    public static void main(String[] args) {
        final int value1 = 1;
        // value1 = 4;
        final double value2;
        value2 = 2.0;
        final Value value3 = new Value(1);
        value3.v = 4;
    }
}
```

**分析**: 我们先来看一下main方法中的几个final修饰的数据，在给value1赋初始值之后，我们无法再对value1的值进行修改，final关键字起到了常量的作用。从value2我们可以看到，**final修饰的变量可以不在声明时赋值，即可以先声明，后赋值**。value3时一个引用变量，这里我们可以看到final修饰引用变量时，**只是限定了引用变量的引用不可改变**，即不能将value3再次引用另一个Value对象，但是引用的对象的值是可以改变的，从内存模型中我们看的更加清晰：

![](https://images2015.cnblogs.com/blog/1055692/201701/1055692-20170130101552386-541665575.jpg)

### 修饰方法参数  
```java
public class FinalTest {
    /* ... */
    public void finalFunc(final int i, final Value value) {
        // i = 5; 不能改变i的值
        // v = new Value(); 不能改变v的值
        value.v = 5; // 可以改变引用对象的值
    }
}
```

### 修饰方法  

它表示该方法不能被覆盖。这种使用方式主要是从设计的角度考虑，即明确告诉其他可能会继承该类的程序员，**不希望他们去覆盖这个方法**。这种方式我们很容易理解，然而，关于private和final关键字还有一点联系，这就是类中所有的private方法都隐式地指定为是final的，由于无法在类外使用private方法，所以也就无法覆盖它。

### 修饰类  
了解了final关键字的其他用法，我们很容易可以想到使用final关键字修饰类的作用，那就是用**final修饰的类是无法被继承**的。

上面我们讲解了final的四种用法，然而，对于第三种和第四种用法，我们却甚少使用。这不是没有道理的，从final的设计来讲，这两种用法甚至可以说是鸡肋，因为对于开发人员来讲，如果我们写的类被继承的越多，就说明我们写的类越有价值，越成功。即使是从设计的角度来讲，也没有必要将一个类设计为不可继承的。Java标准库就是一个很好的反例，特别是Java 1.0/1.1中Vector类被如此广泛的运用，如果所有的方法均未被指定为final的话，它可能会更加有用。如此有用的类，我们很容易想到去继承和重写他们，然而，由于final的作用，导致我们对Vector类的扩展受到了一些阻碍，导致了Vector并没有完全发挥它应有的全部价值。

