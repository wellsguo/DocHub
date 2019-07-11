## Activiti   

### 全局变量 & 局部变量

#### 1. 设置全局流程变量

```
/**
 * 设置流程变量数据
 */
@Test
public void setVariableValues(){
    TaskService taskService=processEngine.getTaskService(); // 任务Service
    String taskId="15004"; // TODO
    taskService.setVariable(taskId, "days", 2);
    taskService.setVariable(taskId, "date", new Date());
    taskService.setVariable(taskId, "reason", "发烧");
    Student student=new Student();
    student.setId(1);
    student.setName("张三");
    taskService.setVariable(taskId, "student", student); // 存序列化对象
}
```

```
/**
 * 设置流程变量数据
 */
@Test
public void setVariableValues2(){
    TaskService taskService=processEngine.getTaskService(); // 任务Service
    String taskId="15004";
    Student student=new Student();
    student.setId(1);
    student.setName("张三");

    Map<String, Object> variables=new HashMap<String,Object>();
    variables.put("days", 2);
    variables.put("date", new Date());
    variables.put("reason", "发烧");
    variables.put("student", student);
    taskService.setVariables(taskId, variables);
}
```
#### 2. 获取全局流程变量
```
/**
 * 获取流程变量数据
 */
@Test
public void getVariableValues(){
    TaskService taskService=processEngine.getTaskService(); // 任务Service
    String taskId="20002";
    Integer days=(Integer) taskService.getVariable(taskId, "days");
    Date date=(Date) taskService.getVariable(taskId, "date");
    String reason=(String) taskService.getVariable(taskId, "reason");
    Student student=(Student) taskService.getVariable(taskId, "student"); 
    System.out.println("请假天数："+days);
    System.out.println("请假日期："+date);
    System.out.println("请假原因："+reason);
    System.out.println("请假对象："+student.getId()+","+student.getName());
}
```

```
/**
 * 获取流程变量数据
 */
@Test
public void getVariableValues2(){
    TaskService taskService=processEngine.getTaskService(); // 任务Service
    String taskId="20002";
    Map<String,Object> variables=taskService.getVariables(taskId);
    Integer days=(Integer) variables.get("days");
    Date date=(Date) variables.get("date");
    String reason=(String) variables.get("reason");
    Student student=(Student)variables.get("student"); 
    System.out.println("请假天数："+days);
    System.out.println("请假日期："+date);
    System.out.println("请假原因："+reason);
    System.out.println("请假对象："+student.getId()+","+student.getName());
}
```

#### 3. 设置局部流程变量
```
TaskService taskService=processEngine.getTaskService(); // 任务Service
String taskId="72504";
taskService.setVariableLocal(taskId,"date", new Date());
```        

#### 4. 获取局部流程变量
```
TaskService taskService=processEngine.getTaskService(); // 任务Service
String taskId="80002";  
Date date=(Date) taskService.getVariableLocal(taskId, "date");
```

# Q & A

##### 如何实现任务的委托和代理

##### 在 Spring + Activiti 中 Listener 无法通过 @AutoWired 注入Bean