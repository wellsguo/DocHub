## Lambda
> 建议：超过3行的逻辑就不要使用Lambda表达式。  
> 虽然看着很先进，其实Lambda表达式的本质只是一个"语法糖",由编译器推断并帮你转换包装为常规的代码,因此你可以使用更少的代码来实现同样的功能。本人建议不要乱用,因为这就和某些很高级的黑客写的代码一样,简洁,难懂,难以调试,维护人员想骂娘.当然由于各种编译器的推理和代码的其他判断处理可能会使得程序的性能降低[[Java8 Lambda表达式和流操作如何让你的代码变慢5倍](http://www.codeceo.com/article/java8-lambda-slow-5-times.html)].

### Lambda表达式的语法
```java
(parameters) -> expression  
或  
(parameters) ->{ statements; }
```

```java
// 1. 不需要参数,返回值为 5
() -> 5
 
// 2. 接收一个参数(数字类型),返回其2倍的值
x -> 2 * x
 
// 3. 接受2个参数(数字),并返回他们的差值
(x, y) -> x – y
 
// 4. 接收2个int型整数,返回他们的和
(int x, int y) -> x + y
 
// 5. 接受一个 string 对象,并在控制台打印,不返回任何值(看起来像是返回void)
(String s) -> System.out.print(s)
```

### Lambda —— forEach
```java
String[] atp = {"Rafael Nadal", "Novak Djokovic", "Stanislas Wawrinka", 
                "David Ferrer", "Roger Federer", "Andy Murray", 
                "Tomas Berdych", "Juan Martin Del Potro"};
List<String> players =  Arrays.asList(atp);
 
// 以前的循环方式
for (String player : players) {
     System.out.print(player + "; ");
}
 
// 使用 lambda 表达式以及函数操作(functional operation)
players.forEach((player) -> System.out.print(player + "; "));
 
// 在 Java 8 中使用双冒号操作符(double colon operator)
players.forEach(System.out::println);
```

### Lambda —— 匿名类
> 匿名类可以使用lambda表达式来代替

#### 使用匿名内部类
```java
btn.setOnAction(new EventHandler<ActionEvent>() {
          @Override
          public void handle(ActionEvent event) {
              System.out.println("Hello World!"); 
          }
    });

// 或者使用 lambda expression
btn.setOnAction(event -> System.out.println("Hello World!"));
````
    
#### Runnable接口      
```java
// 1.1使用匿名内部类
new Thread(new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello world !");
    }
}).start();

// 1.2使用 lambda expression
new Thread(() -> System.out.println("Hello world !")).start();

// 2.1使用匿名内部类
Runnable race1 = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello world !");
    }
};

// 2.2使用 lambda expression
Runnable race2 = () -> System.out.println("Hello world !");

// 直接调用 run 方法(没开新线程哦!)
race1.run();
race2.run();
```

### Lambdas——集合类排序  
> 在Java中,**Comparator** 类被用来排序集合。   

```java
String[] players = {"Rafael Nadal", "Novak Djokovic", 
    "Stanislas Wawrinka", "David Ferrer",
    "Roger Federer", "Andy Murray",
    "Tomas Berdych", "Juan Martin Del Potro",
    "Richard Gasquet", "John Isner"};
```
######  a. 使用匿名内部类根据 name 排序 players
```java
Arrays.sort(players, new Comparator<String>() {
    @Override
    public int compare(String s1, String s2) {
        return (s1.compareTo(s2));
    }
});
```

###### b. 使用 lambda expression 排序 players
```java
Comparator<String> sortByName = (String s1, String s2) -> (s1.compareTo(s2));
Arrays.sort(players, sortByName);
```

###### c. 使用 lambda expression 排序 players
```java
Arrays.sort(players, (String s1, String s2) -> (s1.compareTo(s2)));
```

### Lambdas——stream
**stream** 是对集合的包装,通常和 lambda 一起使用。 使用lambdas可以支持许多操作,如 <u>map, filter, limit, sorted, count, min, max, sum, collect</u> 等等。 同样,stream 使用懒运算,他们并不会真正地读取所有数据,遇到像getFirst() 这样的方法就会结束链式语法。 在接下来的例子中,我们将探索 lambdas 和 streams 能做什么。 

###### Person 只是一个简单的POJO类:

```java
public class Person {
 
    private String firstName, lastName, job, gender;
    private int salary, age;

    public Person(String firstName, String lastName, String job,
                    String gender, int age, int salary)       {
              this.firstName = firstName;
              this.lastName = lastName;
              this.gender = gender;
              this.age = age;
              this.job = job;
              this.salary = salary;
    }
    // Getter and Setter 
    // ...
}
```
###### 创建两个 list,用来存放 Person 对象
```java
List<Person> javaProgrammers = new ArrayList<Person>() {
  {
    add(new Person("Elsdon", "Jaycob", "Java programmer", "male", 43, 2000));
    add(new Person("Tamsen", "Brittany", "Java programmer", "female", 23, 1500));
    add(new Person("Floyd", "Donny", "Java programmer", "male", 33, 1800));
    add(new Person("Sindy", "Jonie", "Java programmer", "female", 32, 1600));
    add(new Person("Vere", "Hervey", "Java programmer", "male", 22, 1200));
    add(new Person("Maude", "Jaimie", "Java programmer", "female", 27, 1900));
    add(new Person("Shawn", "Randall", "Java programmer", "male", 30, 2300));
    add(new Person("Jayden", "Corrina", "Java programmer", "female", 35, 1700));
    add(new Person("Palmer", "Dene", "Java programmer", "male", 33, 2000));
    add(new Person("Addison", "Pam", "Java programmer", "female", 34, 1300));
  }
};

List<Person> phpProgrammers = new ArrayList<Person>() {
  {
    add(new Person("Jarrod", "Pace", "PHP programmer", "male", 34, 1550));
    add(new Person("Clarette", "Cicely", "PHP programmer", "female", 23, 1200));
    add(new Person("Victor", "Channing", "PHP programmer", "male", 32, 1600));
    add(new Person("Tori", "Sheryl", "PHP programmer", "female", 21, 1000));
    add(new Person("Osborne", "Shad", "PHP programmer", "male", 32, 1100));
    add(new Person("Rosalind", "Layla", "PHP programmer", "female", 25, 1300));
    add(new Person("Fraser", "Hewie", "PHP programmer", "male", 36, 1100));
    add(new Person("Quinn", "Tamara", "PHP programmer", "female", 21, 1000));
    add(new Person("Alvin", "Lance", "PHP programmer", "male", 38, 1600));
    add(new Person("Evonne", "Shari", "PHP programmer", "female", 40, 1800));
  }
};
```

```java
System.out.println("所有程序员的姓名:");
javaProgrammers.forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));
phpProgrammers.forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));

System.out.println("给程序员加薪 5% :");
Consumer<Person> giveRaise = e -> e.setSalary(e.getSalary() / 100 * 5 + e.getSalary());
javaProgrammers.forEach(giveRaise);
phpProgrammers.forEach(giveRaise);
  ```
  
  #### filter——过滤器
  
  ```java
// 过滤器filter() 
System.out.println("下面是月薪超过 $1,400 的PHP程序员:")
phpProgrammers.stream()
      .filter((p) -> (p.getSalary() > 1400))
      .forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));

// 定义 filters
Predicate<Person> ageFilter = (p) -> (p.getAge() > 25);
Predicate<Person> salaryFilter = (p) -> (p.getSalary() > 1400);
Predicate<Person> genderFilter = (p) -> ("female".equals(p.getGender()));

System.out.println("下面是年龄大于 24岁且月薪在$1,400以上的女PHP程序员:");
phpProgrammers.stream()
          .filter(ageFilter)
          .filter(salaryFilter)
          .filter(genderFilter)
          .forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));

// 重用filters
System.out.println("年龄大于 24岁的女性 Java programmers:");
javaProgrammers.stream()
          .filter(ageFilter)
          .filter(genderFilter)
          .forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));      
```
#### limit——限制结果集的个数
```java
System.out.println("最前面的3个 Java programmers:");
javaProgrammers.stream()
          .limit(3)
          .forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));
 
 
System.out.println("最前面的3个女性 Java programmers:");
javaProgrammers.stream()
          .filter(genderFilter)
          .limit(3)
          .forEach((p) -> System.out.printf("%s %s; ", p.getFirstName(), p.getLastName()));
```

#### sorted——排序
```java
System.out.println("根据 name 排序,并显示前5个 Java programmers:");
List<Person> sortedJavaProgrammers = javaProgrammers
          .stream()
          .sorted((p, p2) -> (p.getFirstName().compareTo(p2.getFirstName())))
          .limit(5)
          .collect(toList());

sortedJavaProgrammers.forEach((p) -> System.out.printf("%s %s; %n", p.getFirstName(), p.getLastName()));

System.out.println("根据 salary 排序 Java programmers:");
sortedJavaProgrammers = javaProgrammers
          .stream()
          .sorted( (p, p2) -> (p.getSalary() - p2.getSalary()) )
          .collect( toList() );

sortedJavaProgrammers.forEach((p) -> System.out.printf("%s %s; %n", p.getFirstName(), p.getLastName()));
```

#### min/max——最值
```java
System.out.println("工资最低的 Java programmer:");
Person pers = javaProgrammers
          .stream()
          .min((p1, p2) -> (p1.getSalary() - p2.getSalary()))
          .get()

System.out.printf("Name: %s %s; Salary: $%,d.", pers.getFirstName(), pers.getLastName(), pers.getSalary())

System.out.println("工资最高的 Java programmer:");
Person person = javaProgrammers
          .stream()
          .max((p, p2) -> (p.getSalary() - p2.getSalary()))
          .get()

System.out.printf("Name: %s %s; Salary: $%,d.", person.getFirstName(), person.getLastName(), person.getSalary())
```

#### collect——将结果集放到一个 String / Set / TreeSet / List 中
```java
System.out.println("将 PHP programmers 的 first name 拼接成字符串:");
String phpDevelopers = phpProgrammers
          .stream()
          .map(Person::getFirstName)
          .collect(joining(" ; ")); // 在进一步的操作中可以作为标记(token)   

System.out.println("将 Java programmers 的 first name 存放到 Set:");
Set<String> javaDevFirstName = javaProgrammers
          .stream()
          .map(Person::getFirstName)
          .collect(toSet());

System.out.println("将 Java programmers 的 first name 存放到 TreeSet:");
TreeSet<String> javaDevLastName = javaProgrammers
          .stream()
          .map(Person::getLastName)
          .collect(toCollection(TreeSet::new));
```
#### parallelStream——并行
```java
System.out.println("计算付给 Java programmers 的所有money:");
int totalSalary = javaProgrammers
          .parallelStream()
          .mapToInt(p -> p.getSalary())
          .sum();
```
#### summaryStatistics——获得 stream 中元素的各种汇总数据
```java
//计算 count, min, max, sum, and average for numbers
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
IntSummaryStatistics stats = numbers
          .stream()
          .mapToInt((x) -> x)
          .summaryStatistics();
 
System.out.println("List中最大的数字 : " + stats.getMax());
System.out.println("List中最小的数字 : " + stats.getMin());
System.out.println("所有数字的总和   : " + stats.getSum());
System.out.println("所有数字的平均值 : " + stats.getAverage()); 
```

    



