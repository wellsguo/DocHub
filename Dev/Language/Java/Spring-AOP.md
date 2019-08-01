# [Spring Boot AOP 自定义注解实现权限控制](https://blog.csdn.net/qq_24689877/article/details/85143929)

附：Spring中aop的[官方文档地址](https://docs.spring.io/spring/docs/5.0.12.BUILD-SNAPSHOT/spring-framework-reference/core.html#aop)

## Aop 的说明

在软件业，AOP为Aspect Oriented Programming的缩写，意为：面向切面编程，通过预编译方式和运行期动态代理实现程序功能的统一维护的一种技术。AOP是OOP的延续，是软件开发中的一个热点，也是Spring框架中的一个重要内容，是函数式编程的一种衍生范型。利用AOP可以对业务逻辑的各个部分进行隔离，从而使得业务逻辑各部分之间的耦合度降低，提高程序的可重用性，同时提高了开发的效率。

## 环境说明

基于spring boot 2.0.4 jdk1.8 实现  
接口测试工具: insomnia

> 事先声明：为了方便流程的演示，本文不涉及token的相关操作  
若请求头带入携带id，则视为已登录。   
角色信息，用head头的形式提交。

## 准备阶段

**第一步，**导入spring boot对spring aop的支持组件

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

此组件是基于spring boot自动配置的spring-boot-starter，可以无需配置文件，与spring boot集成

此外，有的人说直接导入aspectj包的，在这里说明一下，这个包是包含aspectj的，而且spring boot官方推荐使用此依赖来在spring boot中使用aop

**第二步：**构建Controller，提供入口点

```java
@RestController
public class MyController {
	@GetMapping("hello")
	public String hello(Integer id, String name, Integer age) {
		System.out.println("hello方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我不需要用户权限";
	}
	@GetMapping("user")
	public String user(Integer id, String name, Integer age) {
		System.out.println("user方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我需要登陆后才可以访问";
	}
	@GetMapping("admin")
	public String admin(Integer id, String name, Integer age) {
		System.out.println("admin方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我需要管理员身份才可以访问";
	}
}
```

controller中为了提供了三个方法，分别是不需要具有权限、登陆即可访问、需要管理员角色才可以访问。

同时为了模拟实际操作，传入参数并执行方法。

测试访问：



准备阶段完毕。开始构建权限操作。

 

## 权限逻辑操作

**第一步：** 构建注解类

```java
@Target({ ElementType.METHOD, ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface AuthToken {
	/**
	 * 访问所需的身份，默认为空，为登录即可访问，可以多个定义
	 * 
	 * @return
	 * @data 2018年12月19日
	 * @version v1.0.0.0
	 */
	String[] role_name() default "";
}
```

> 此注解定义一个数组属性，role_name，用于标识访问被此注解修饰的方法需要访问的用户具有什么身份。

注：为了方便流程的演示，本文不涉及token的相关操作，权限角色，用head头的形式提交。且若请求头带入携带id，则视为已登录。

**第二步：** 为Controller提供的方法加入此注解。

```java
@RestController
public class MyController {
	/**
	 * 无需校验，不加注解
	 */
	@GetMapping("hello")
	public String hello(Integer id, String name, Integer age) {
		System.out.println("hello方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我不需要用户权限";
	}
 
	/**
	 * 需要登录校验，加上注解，但不传所需角色
	 */
	@GetMapping("user")
	@AuthToken
	public String user(Integer id, String name, Integer age) {
		System.out.println("user方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我需要登陆后才可以访问";
	}
 
	/**
	 * 需要角色校验，加上注解，并且写入两个角色，本文演示两个角色有一个即可访问，当然写一个可以。
	 * 注：若想两个角色同时具有，修改后文的逻辑判断即可。
	 * 若需要更复杂的逻辑操作，推荐使用Spring Security框架。
	 */
	@GetMapping("admin")
	@AuthToken(role_name = { "admin", "Administrator" })
	public String admin(Integer id, String name, Integer age) {
		System.out.println("admin方法执行：id==>" + id + "，name==>" + name + "，age==>" + age);
		return "hi~ 我需要管理员身份才可以访问";
	}
}
```

**第三步：** 写Spring Aop切面，增强方法

先搭出来基本的架子，新建AuthTokenAspect类，引入@Aspect 和 @Component两个注解

- @Aspect标识这个类是一个 spring 切面类

- @Component 将这个类交给spring处理

二者缺一不可

```java
@Aspect
@Component
public class AuthTokenAspect {
	/**
	 * Spring中使用@Pointcut注解来定义方法切入点
	 * @Pointcut 用来定义切点，针对方法  @Aspect 用来定义切面，针对类
	 * 后面的增强均是围绕此切入点来完成的
	 * 此处仅配置被我们刚才定义的注解：AuthToken修饰的方法即可
	 */
	@Pointcut("@annotation(authToken)")
	public void doAuthToken(AuthToken authToken) {
	}
 
	/**
	 * 此处我使用环绕增强，在方法执行之前或者执行之后均会执行。
	 */
	@Around("doAuthToken(authToken)")
	public Object deBefore(ProceedingJoinPoint pjp, AuthToken authToken) throws Throwable {
		System.out.println("---------方法执行之前-------------");
		// 执行原方法，并记录返回值。
		Object proceed = pjp.proceed();
		System.out.println("---------方法执行之后-------------");
		return proceed; 
	}
 
}
```

> 想了解@Pointcut注解中的语法的使用，可以去看看这位博主的博客：https://www.jianshu.com/p/0b78f1156642
>
> 这位博主写了一套Spring Boot Aop的学习教程 目录地址：https://www.jianshu.com/p/9093e6ca3378

十分感谢！

 

先测试一下（此时是没有加权限或者登陆验证的）

针对于上文的Controller 运行user方法来测试



方法按照预期，执行前和执行后都输出了我们的语句。然而，此处方法的返回值是需要我们注意的。



此处的返回值不是由原方法返回的。还记得上面写切面时的那句“ **执行原方法，并记录返回值。**”吗？  
对，上文的方法被我们执行后，将返回值记录了下来。用于保存！注意是保存！  
记录完之后，我们的切点还没有走完呢，它还要继续往下走，输出一条“方法执行之后”的语句，才执行的return语句。  
不信的话，回来看一下代码。



对吧，此时接口测试工具的返回值，是我们事先记录下来的返回值（既然是记录下来的，那么如果我们不记录，或者说不执行方法直接自己定义一个返回值呢？？），正确返回值只能说是我们制造的一种错觉，让人感觉这个方法正常的执行，并按照我们的预期执行了正确的返回值。

 

相信到这里，聪明的童鞋就可以悟出来了，这个方法在切点里就像是一个小姑娘，我们想让她执行她就执行，不想执行就不让她执行（不执行pjp.proceed()方法就行了），想返回什么数据，我们自己定义就好了！（**但是要与原方法的返回值类型相同**，比如我原方法的返回值是String，那么我这里也只能返回String类型的，不能说本来我要的是苹果，你给我一个榴莲就不好了~~）

 

为了验证我们的推断，我们修改代码如下：

```java
@Around("doAuthToken(authToken)")
public Object deBefore(ProceedingJoinPoint pjp, AuthToken authToken) throws Throwable {
    System.out.println("---------方法执行之前-------------");
    // 执行原方法，并记录返回值。
    Object proceed = pjp.proceed();
    System.out.println("---------方法执行之后-------------");
    return "哈哈哈哈，方法执行了也没有你要的返回值！"; 
}
```



方法如我们的预期被执行了。那返回值呢？



到这里为止，我们的大概思路应该就出来了，我们

- 首先拦截带有@AuthToken注解的方法执行，
- 然后去判断@AuthToken注解是否带有所需的角色名（权限），
- 接着去判断 **request** 请求中的请求头是否带有id和我们对应所需的角色:
  - 若判断成功，则方法正常执行，并如预期让这个小姑娘有正确的返回值。
  - 那若判断失败，不好意思，方法不执行，且返回值就是我们自定义错误信息。

 

获得request可以用以下代码：

```java
ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
HttpServletRequest request = attributes.getRequest();
```

上文用到的 ***ProceedingJoinPoint*** 是方法的连接点对象，它是无所不能的，详细信息，同样可以去翻阅本文首提供的Spring官方文档，或者翻阅源码，本文不再赘述。


**第四步：**完善切面类

```java
@Aspect
@Component
public class AuthTokenAspect {

	@Pointcut("@annotation(authToken)")
	public void doAuthToken(AuthToken authToken) {
	}
 
	/**
	 * 此处我使用环绕增强，在方法执行之前或者执行之后均会执行。
	 */
	@Around("doAuthToken(authToken)")
	public Object deBefore(ProceedingJoinPoint pjp, AuthToken authToken) throws Throwable {
		ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
		HttpServletRequest request = attributes.getRequest();
		// 获取访问该方法所需的role_name信息
		String[] role_name = authToken.role_name();
		if (role_name == null || role_name.length == 0) {
			// 只需登录，验证是否具有id即可。
			String id = request.getHeader("id");
			/**
			 * 此处使用短路与，若id==null直接会执行if体，不会继续判断 
			 * 若不等于null，则去验证后面的条件，但是也不会出现因为id为null而出现的空指针异常
			 * 所以这样写也是安全的。
			 */
			if (id != null && !id.equals("")) {
				// 已登录，执行原方法并返回即可。
				return pjp.proceed();
			}
			// 未登录，不执行方法，直接返回错误信息
			return "请登陆后再试！";
		} else {
			// 需要验证身份
			String role = request.getHeader("role");
			for (String str : role_name) {
				/**
				 * 此处str由于是用role_name中取值，则str必定不为空
				 * 而从请求头中获取的role有可能为空，则此处调用str的equals方法
				 * 当然可以直接在获得请求头后进行验证是是否不为空。
				 */
				if (str.equals(role)) {
					// 身份匹配成功
					return pjp.proceed();
				}
			}
			return "权限校验失败，不具有指定的身份";
		}
	}
 
}
```

### 测试

- 统一不传id和role
  - hello方法：
  - user方法：
  - admin方法（因为通常逻辑下，具有身份的前提下肯定是登陆过的。head传入id）：


- 传id和role
  - user方法：
  - admin方法：



 




## 下载地址
https://github.com/zichun0507/SpringBoot_AOP

> 1. AOP 用于完成某一类同意操作，可以是权限控制，日志打印，登录验证，执行效率等等
> 2. AOP 借助于注解方式，注解（Annotation）写法
> 3. AOP ASPECT 框架搭建
> 4. 完善 deBefore 方法
> 5. 注意 deBefore 返回值类型与原方法一致



