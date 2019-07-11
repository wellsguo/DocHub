## 异常

### 异常处理模板  

```java
try {
    ... // 可能出现异常的语句
} catch(Exception e) {
    ... // 异常处理
} finally {
    ...
}
```

#### 关于 finally
1. 不论是否能捕捉到异常，finally 块中代码都会执行；

2. 当 try和 catch 中有 return 时，finally 仍然会执行；

3. finally 是在 return 后面的表达式运算后执行的（此时并没有返回运算后的值，而是先把要返回的值保存起来，不管 finally 中的代码怎么样，返回的值都不会改变，任然是之前保存的值），所以函数返回值是在 finally 执行前确定的；

4. finally 中最好不要包含 return，否则程序会提前退出，返回值不是 try 或 catch 中保存的返回值。

#### 培养好的编程习惯
1. 在写程序时，对可能会出现异常的部分通常要用 `try{...}catch{...}` 去捕捉它并对它进行处理；

2. 用 `try{...}catch{...}` 捕捉了异常之后一定要对在 `catch{...}` 中对其进行处理，那怕是最简单的一句输出语句，或栈输入`e.printStackTrace()`;

3. 如果是捕捉IO输入输出流中的异常，一定要在 `try{...}catch{...}` 后加 `finally{...}` 把输入输出流关闭；

4. 如果在函数体内用 `throw` 抛出了某种异常，最好要在函数名中加 `throws` 抛异常声明，然后交给调用它的上层函数进行处理。

#### 抛出异常  

##### throw

```java
public class throws_function{
	public static void main(String[] args) {  
        String str = "123456";  
        if(str.equals("123456")) {  
             throw new NumberFormatException();  
        } else {  
             System.out.println(str);  
        } 
      	System.out.println("end!!!");  	
	}  
}
```

##### 系统自动抛异常
```java
public class throws_function{
	public static void main(String[] args) {  
        int a = 100, b =0;  
        System.out.println(5/b);  
        System.out.println("end!!!");
    }
}  
```

##### throws
```java
public class throws_function {   
    public static void function1() throws NumberFormatException {  
      System.out.println(Double.parseDouble("abc"));  
	  System.out.println("function1()第二条语句。"); 
	  System.err.println("function1() NumberFormatException error!!!!"); 
    }  
 
	public static void main(String[] args) {  
        function1(); 
        System.out.println("end!!!");  	
    }  
}
```

##### throw vs. throws  
1、throws出现在方法函数头；而throw出现在函数体。

2、throws表示出现异常的一种可能性，并不一定会发生这些异常；throw则是抛出了异常，执行throw则一定抛出了某种异常对象。

3、两者都是消极处理异常的方式（这里的消极并不是说这种方式不好），只是抛出或者可能抛出异常，但是不会由函数去处理异常，真正的处理异常由函数的上层调用处理。

4、throws说明你有那个可能，倾向。throw的话，那就是你把那个倾向变成真实的了。
