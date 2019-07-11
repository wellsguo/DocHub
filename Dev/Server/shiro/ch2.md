## 2 身份认证

身份验证，即在应用中谁能证明他就是他本人。一般提供如他们的身份ID一些标识信息来表明他就是他本人，如提供身份证，用户名/密码来证明。在shiro中，用户需要提供principals （身份）和credentials（证明）给shiro，从而应用能验证用户身份。

name | name_zh | desc.
 -- |--|--
principals|身份|即主体的标识属性，可以是任何东西，如用户名、邮箱等，唯一即可。<br>一个主体可以有多个principals，但只有一个Primary principals，一般是用户名/密码/手机号。
credentials|证明/凭证|即只有主体知道的安全值，如密码/数字证书等。

最常见的principals和credentials组合就是用户名/密码了。

### 2.1 环境依赖

```xml
<dependencies>  
    <dependency>  
        <groupId>junit</groupId>  
        <artifactId>junit</artifactId>  
        <version>4.9</version>  
    </dependency>  
    <dependency>  
        <groupId>commons-logging</groupId>  
        <artifactId>commons-logging</artifactId>  
        <version>1.1.3</version>  
    </dependency>  
    <dependency>  
        <groupId>org.apache.shiro</groupId>  
        <artifactId>shiro-core</artifactId>  
        <version>1.2.2</version>  
    </dependency>  
</dependencies>   
```

### 2.2 登录/登出测试
> 准备一些用户身份/凭据（shiro.ini）

```
[users]  
zhang=123  
wang=123
```
> 测试用例

```java
@Test  
public void testHelloworld() {  
    //1、获取SecurityManager工厂，此处使用Ini配置文件初始化SecurityManager  
    Factory<org.apache.shiro.mgt.SecurityManager> factory =  
            new IniSecurityManagerFactory("classpath:shiro.ini");  
    //2、得到SecurityManager实例 并绑定给SecurityUtils  
    org.apache.shiro.mgt.SecurityManager securityManager = factory.getInstance();  
    SecurityUtils.setSecurityManager(securityManager);  
    //3、得到Subject及创建用户名/密码身份验证Token（即用户身份/凭证）  
    Subject subject = SecurityUtils.getSubject();  
    UsernamePasswordToken token = new UsernamePasswordToken("zhang", "123");  
  
    try {  
        //4、登录，即身份验证  
        subject.login(token);  
    } catch (AuthenticationException e) {  
        //5、身份验证失败  
    }  
  
    Assert.assertEquals(true, subject.isAuthenticated()); //断言用户已经登录  
  
    //6、退出  
    subject.logout();  
}  
```   
身份验证失败请捕获 AuthenticationException 或其子类，常见的如： DisabledAccountException（禁用的帐号）、LockedAccountException（锁定的帐号）、UnknownAccountException（错误的帐号）、ExcessiveAttemptsException（登录失败次数过多）、IncorrectCredentialsException （错误的凭证）、ExpiredCredentialsException（过期的凭证）等，具体请查看其继承关系；对于页面的错误消息展示，最好使用如“用户名/密码错误”而不是“用户名错误”/“密码错误”，防止一些恶意用户非法扫描帐号库；

> 小结

身份验证步骤：
- 收集用户身份/凭证，即如用户名/密码；
- 调用Subject.login进行登录，如果失败抛出相应的AuthenticationException异常，根据异常提示用户错误信息；否则登录成功；
- 最后调用Subject.logout进行退出操作。

如上测试的几个问题：
- 用户名/密码硬编码在ini配置文件，以后需要改成如数据库存储，且密码需要加密存储；
- 用户身份Token可能不仅仅是用户名/密码，也可能还有其他的，如登录时允许用户名/邮箱/手机号同时登录。 

### 2.3 身份认证流程

![](ch2-1.png)

> 流程如下：

- 首先调用Subject.login(token)进行登录，其会自动委托给Security Manager，调用之前必须通过SecurityUtils. setSecurityManager()设置；
- SecurityManager负责真正的身份验证逻辑；它会委托给Authenticator进行身份验证；
- Authenticator才是真正的身份验证者，Shiro API中核心的身份认证入口点，此处可以自定义插入自己的实现；
- Authenticator可能会委托给相应的AuthenticationStrategy进行多Realm身份验证，默认ModularRealmAuthenticator会调用AuthenticationStrategy进行多Realm身份验证；
- Authenticator会把相应的token传入Realm，从Realm获取身份验证信息，如果没有返回/抛出异常表示身份验证失败了。此处可以配置多个Realm，将按照相应的顺序及策略进行访问。

### 2.4 Realm
Shiro从Realm获取安全数据（如用户、角色、权限），换句话说SecurityManager要验证用户身份，那么它需要从Realm获取相应的用户进行比较以确定用户身份是否合法；也需要从Realm得到用户相应的角色/权限进行验证用户是否能进行操作；可以把Realm看成DataSource，即安全数据源。如我们之前的ini配置方式将使用org.apache.shiro.realm.text.IniRealm。

 

org.apache.shiro.realm.Realm接口如下： 

```java
String getName(); //返回一个唯一的Realm名字  
boolean supports(AuthenticationToken token); //判断此Realm是否支持此Token  
AuthenticationInfo getAuthenticationInfo(AuthenticationToken token)  
 throws AuthenticationException;  //根据Token获取认证信息  
``` 

#### 单Realm配置

1、自定义Realm

```java
public class MyRealm1 implements Realm {  
    @Override  
    public String getName() {  
        return "myrealm1";  
    }  
    @Override  
    public boolean supports(AuthenticationToken token) {  
        //仅支持UsernamePasswordToken类型的Token  
        return token instanceof UsernamePasswordToken;   
    }  
    @Override  
    public AuthenticationInfo getAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {  
        String username = (String)token.getPrincipal();  //得到用户名  
        String password = new String((char[])token.getCredentials()); //得到密码  
        if(!"zhang".equals(username)) {  
            throw new UnknownAccountException(); //如果用户名错误  
        }  
        if(!"123".equals(password)) {  
            throw new IncorrectCredentialsException(); //如果密码错误  
        }  
        //如果身份认证验证成功，返回一个AuthenticationInfo实现；  
        return new SimpleAuthenticationInfo(username, password, getName());  
    }  
}   
``` 

2、ini配置文件指定自定义Realm (shiro-realm.ini)  

```
#声明一个realm  
myRealm1=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm1  
#指定securityManager的realms实现  
securityManager.realms=$myRealm1  
```
通过`$name`来引入之前的realm定义


 

#### 多Realm配置

1、ini配置文件（shiro-multi-realm.ini）  
```
#声明一个realm  
myRealm1=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm1  
myRealm2=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm2  
#指定securityManager的realms实现  
securityManager.realms=$myRealm1,$myRealm2 
```
securityManager会按照realms指定的顺序进行身份认证。此处我们使用显示指定顺序的方式指定了Realm的顺序，如果删除`“securityManager.realms=$myRealm1,$myRealm2”`，那么securityManager会按照realm声明的顺序进行使用（即无需设置realms属性，其会自动发现），当我们显示指定realm后，其他没有指定realm将被忽略，如`“securityManager.realms=$myRealm1”`，那么myRealm2不会被自动设置进去。


#### Shiro 默认 Realm
![](ch2-2.png)

org.apache.shiro.realm.text.IniRealm：[users]部分指定用户名/密码及其角色；[roles]部分指定角色即权限信息；

org.apache.shiro.realm.text.PropertiesRealm： user.username=password,role1,role2指定用户名/密码及其角色；role.role1=permission1,permission2指定角色及权限信息；

org.apache.shiro.realm.jdbc.JdbcRealm：通过sql查询相应的信息，如“select password from users where username = ?”获取用户密码，“select password, password_salt from users where username = ?”获取用户密码及盐；“select role_name from user_roles where username = ?”获取用户角色；“select permission from roles_permissions where role_name = ?”获取角色对应的权限信息；也可以调用相应的api进行自定义sql；

##### JDBC Realm使用

1、数据库及依赖
```java
<dependency>  
    <groupId>mysql</groupId>  
    <artifactId>mysql-connector-java</artifactId>  
    <version>5.1.25</version>  
</dependency>  
<dependency>  
    <groupId>com.alibaba</groupId>  
    <artifactId>druid</artifactId>  
    <version>0.2.23</version>  
</dependency>   
```

2、到数据库shiro下建三张表
- users（用户名/密码）
- user_roles（用户/角色）
- roles_permissions（角色/权限）  
具体请参照shiro-example-chapter2/sql/shiro.sql；并添加一个用户记录，用户名/密码为zhang/123；

 

3、ini配置（shiro-jdbc-realm.ini） 

```
jdbcRealm=org.apache.shiro.realm.jdbc.JdbcRealm  
dataSource=com.alibaba.druid.pool.DruidDataSource  
dataSource.driverClassName=com.mysql.jdbc.Driver  
dataSource.url=jdbc:mysql://localhost:3306/shiro  
dataSource.username=root  
#dataSource.password=  
jdbcRealm.dataSource=$dataSource  
securityManager.realms=$jdbcRealm
```

### 2.5 Authenticator及AuthenticationStrategy
Authenticator 的职责是验证用户帐号，是 Shiro API 中身份验证核心的入口点： 

```
public AuthenticationInfo authenticate(AuthenticationToken authenticationToken)  
            throws AuthenticationException; 
```            
 - 如果验证成功，将返回AuthenticationInfo验证信息，此信息中包含了身份及凭证；
 - 如果验证失败将抛出相应的AuthenticationException实现。


SecurityManager接口继承了Authenticator，另外还有一个ModularRealmAuthenticator实现，其委托给多个Realm进行验证，验证规则通过AuthenticationStrategy接口指定，默认提供的实现：
 - FirstSuccessfulStrategy：只要有一个Realm验证成功即可，只返回第一个Realm身份验证成功的认证信息，其他的忽略；
 - AtLeastOneSuccessfulStrategy：只要有一个Realm验证成功即可，和FirstSuccessfulStrategy不同，返回所有Realm身份验证成功的认证信息(**默认**)
 - AllSuccessfulStrategy：所有Realm验证成功才算成功，且返回所有Realm身份验证成功的认证信息，如果有一个失败就失败了。

 

假设我们有三个realm：

myRealm1： 用户名/密码为zhang/123时成功，且返回身份/凭据为zhang/123；   
myRealm2： 用户名/密码为wang/123时成功，且返回身份/凭据为wang/123；   
myRealm3： 用户名/密码为zhang/123时成功，且返回身份/凭据为zhang@163.com/123，和myRealm1不同的是返回时的身份变了；  

 

1、ini配置文件(shiro-authenticator-all-success.ini) 

```
#指定securityManager的authenticator实现  
authenticator=org.apache.shiro.authc.pam.ModularRealmAuthenticator  
securityManager.authenticator=$authenticator  
  
#指定securityManager.authenticator的authenticationStrategy  
allSuccessfulStrategy=org.apache.shiro.authc.pam.AllSuccessfulStrategy  
securityManager.authenticator.authenticationStrategy=$allSuccessfulStrategy  

myRealm1=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm1  
myRealm2=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm2  
myRealm3=com.github.zhangkaitao.shiro.chapter2.realm.MyRealm3  
securityManager.realms=$myRealm1,$myRealm3  
 ```

2、测试代码

2.1、首先通用化登录逻辑 

```
private void login(String configFile) {  
    //1、获取SecurityManager工厂，此处使用Ini配置文件初始化SecurityManager  
    Factory<org.apache.shiro.mgt.SecurityManager> factory =  
            new IniSecurityManagerFactory(configFile);  
  
    //2、得到SecurityManager实例 并绑定给SecurityUtils  
    org.apache.shiro.mgt.SecurityManager securityManager = factory.getInstance();  
    SecurityUtils.setSecurityManager(securityManager);  
  
    //3、得到Subject及创建用户名/密码身份验证Token（即用户身份/凭证）  
    Subject subject = SecurityUtils.getSubject();  
    UsernamePasswordToken token = new UsernamePasswordToken("zhang", "123");  
  
    subject.login(token);  
}  
``` 

2.2、测试AllSuccessfulStrategy成功：    

```
@Test  
public void testAllSuccessfulStrategyWithSuccess() {  
    login("classpath:shiro-authenticator-all-success.ini");  
    Subject subject = SecurityUtils.getSubject();  
  
    //得到一个身份集合，其包含了Realm验证成功的身份信息  
    PrincipalCollection principalCollection = subject.getPrincipals();  
    Assert.assertEquals(2, principalCollection.asList().size());  
} 
```
即PrincipalCollection包含了zhang和zhang@163.com身份信息。

 

2.3、测试AllSuccessfulStrategy失败：

```
@Test(expected = UnknownAccountException.class)  
public void testAllSuccessfulStrategyWithFail() {  
    login("classpath:shiro-authenticator-all-fail.ini");  
    Subject subject = SecurityUtils.getSubject();  
}  
```
shiro-authenticator-all-fail.ini与shiro-authenticator-all-success.ini不同的配置是使用了securityManager.realms=$myRealm1,$myRealm2；即myRealm验证失败。

 

对于AtLeastOneSuccessfulStrategy和FirstSuccessfulStrategy的区别，请参照testAtLeastOneSuccessfulStrategyWithSuccess和testFirstOneSuccessfulStrategyWithSuccess测试方法。唯一不同点一个是返回所有验证成功的Realm的认证信息；另一个是只返回第一个验证成功的Realm的认证信息。

 

自定义AuthenticationStrategy实现，首先看其API：

```
//在所有Realm验证之前调用  
AuthenticationInfo beforeAllAttempts(  
Collection<? extends Realm> realms, AuthenticationToken token)   
throws AuthenticationException;  
//在每个Realm之前调用  
AuthenticationInfo beforeAttempt(  
Realm realm, AuthenticationToken token, AuthenticationInfo aggregate)   
throws AuthenticationException;  
//在每个Realm之后调用  
AuthenticationInfo afterAttempt(  
Realm realm, AuthenticationToken token,   
AuthenticationInfo singleRealmInfo, AuthenticationInfo aggregateInfo, Throwable t)  
throws AuthenticationException;  
//在所有Realm之后调用  
AuthenticationInfo afterAllAttempts(  
AuthenticationToken token, AuthenticationInfo aggregate)   
throws AuthenticationException;   
```
因为每个AuthenticationStrategy实例都是无状态的，所有每次都通过接口将相应的认证信息传入下一次流程；通过如上接口可以进行如合并/返回第一个验证成功的认证信息。

 

自定义实现时一般继承org.apache.shiro.authc.pam.AbstractAuthenticationStrategy即可，具体可以参考代码com.github.zhangkaitao.shiro.chapter2.authenticator.strategy包下OnlyOneAuthenticatorStrategy 和AtLeastTwoAuthenticatorStrategy。

 

到此基本的身份验证就搞定了，对于AuthenticationToken 、AuthenticationInfo和Realm的详细使用后续章节再陆续介绍。

 


 