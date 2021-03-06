## JAVA static 关键字

### 参考文章

- [1] [Java中的static关键字解析](https://www.cnblogs.com/dolphin0520/p/3799052.html)
  - 作用范围(变量，方法，代码块，内部类，静态内部类变量和方法)
  - 关键字使用误区（不允许用来修饰局部变量，不用来限制访问权限，static & this）
  - 静态快、构造函数、调用函数执行时间先后顺序以及继承父类的执行顺序


- [2] [再议Java中的static关键字](https://www.cnblogs.com/dolphin0520/p/10651845.html)
  - static 各种应用场景
  - 非静态内部类对象持有外部类对象的引用（编译器会隐式地将外部类对象的引用作为内部类的构造器参数）；而静态内部类对象不会持有外部类对象的引用  
    - 由于非静态内部类的实例创建需要有外部类对象的引用，所以非静态内部类对象的创建必须依托于外部类的实例；而静态内部类的实例创建只需依托外部类；
    - 并且由于非静态内部类对象持有了外部类对象的引用，因此非静态内部类可以访问外部类的非静态成员；而静态内部类只能访问外部类的静态成员；
    - 两者的根本性区别其实也决定了用static去修饰内部类的真正意图：
      - 内部类需要脱离外部类对象来创建实例
      - 避免内部类使用过程中出现内存溢出

　　第一种是目前静态内部类使用比较多的场景，比如JDK集合中的Entry、builder设计模式。


- [3] [JAVA中的内部类（一）静态内部类](https://www.cnblogs.com/heavenplus/p/9451181.html)
