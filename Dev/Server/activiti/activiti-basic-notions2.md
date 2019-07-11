# Activiti

- https://blog.csdn.net/qq877507054/article/details/60143099  
- https://blog.csdn.net/yerenyuan_pku/article/details/71307305  
- https://blog.csdn.net/YEN_CSDN/article/details/54633357

一、 [创建引擎对象](#流程定义查询)

模型 &#10132; 工作流定义 &#10132; 工作流实体 &#10132; 任务


## 一、创建引擎对象

```java
// 创建一个流程引擎配置对象
ProcessEngineConfiguration conf = 
ProcessEngineConfiguration.createStandaloneProcessEngineConfiguration();

// 1. 设置jdbc连接参数
conf.setJdbcDriver("com.mysql.jdbc.Driver");  
conf.setJdbcUrl("jdbc:mysql://localhost:3306/activiti_01");
conf.setJdbcUsername("root");
conf.setJdbcPassword("yezi");

// 2. 配置数据源
conf.setDataSource(dataSource);

// 设置自动建表
conf.setDatabaseSchemaUpdate("true");
// 使用配置对象创建一个流程引擎对象，并且在创建过程中可以自动建表
ProcessEngine processEngine = conf.buildProcessEngine();
```
## 二、 流程
### 2.1 流程部署

#### 2.1.1 相关Table

- `ACT_GE_BYTEARRAY`  存储 .bpmn 和 .xml 文件
- `ACT_RE_DEPLOYMENT` 记录部署信息，主要包括 ID 和时间
- `ACT_RE_PROCDEF` 记录定义信息，主要包括 ID ，资源名称和 Key
 - 以上三张表存在关联关系，都包含了 Deployment_ID


```java
// 创建一个部署构建器对象，用于加载流程定义文件(bpmn文件和png文件)
DeploymentBuilder deploymentBuilder = processEngine.getRepositoryService().createDeployment();
// 方式一 资源文件
deploymentBuilder.addClasspathResource("qjlc.bpmn");
deploymentBuilder.addClasspathResource("qjlc.png");

// 方式二 zip压缩文件
ZipInputStream zipInputStream = new ZipInputStream(this.getClass()
                .getClassLoader().getResourceAsStream("process.zip")); // 从类路径下读取process.zip压缩文件，并把它包装成一个输入流
deploymentBuilder.addZipInputStream(zipInputStream );
// 部署，并返回一个部署对象(其实Deployment是一个接口)
Deployment deployment = deploymentBuilder.deploy();
System.out.println(deployment.getId());
```

### 2.2 部署查询

#### 2.2.1 相关TABLE
- ACT_RE_DEPLOYMENT

```java
// 部署查询对象，查询部署表
DeploymentQuery query = processEngine.getRepositoryService().createDeploymentQuery();
List<Deployment> list = query.list();
for (Deployment deployment : list) {
    System.out.println(deployment.getId() + "\t" + deployment.getDeploymentTime());
}
```

### 2.3 部署删除
#### 2.3.1 相关TABLE
- ACT_RE_DEPLOYMENT


```java
String deploymentId = "801"; // 部署id
processEngine.getRepositoryService().deleteDeployment(deploymentId);
```

### 2.4 流程定义查询
#### 相关TABLE
- ACT_RE_PROCDEF


```java
// 流程定义查询对象，用于查询流程定义表（act_re_procdef）
ProcessDefinitionQuery query = processEngine.getRepositoryService().createProcessDefinitionQuery();
// 根据流程定义的key来过滤
query.processDefinitionKey("qjlc");
// 添加排序条件
query.orderByProcessDefinitionVersion().desc();
// 分页查询（伪代码）
query.listPage("从哪开始查", "查几条");
// 以下查询的是所有的流程定义
List<ProcessDefinition> list = query.list();
for (ProcessDefinition pd : list) {
    System.out.println(pd.getId() + "    " + pd.getName() + "    " + pd.getVersion());
}
```

```java
// 1. 部署id进行获取
String deploymentId = "201"; // 部署id
// 获得两个流程定义文件的名称
List<String> names = processEngine
        .getRepositoryService().getDeploymentResourceNames(deploymentId);
for (String name : names) {
    System.out.println(name);
    // 获得两个流程定义文件对应的输入流
    InputStream in = processEngine
            .getRepositoryService().getResourceAsStream(deploymentId, name);
    // 读取输入流写到指定的本地磁盘上
    FileUtils.copyInputStreamToFile(in, new File("F:\\" + name));
    in.close();
}
```

```java
// 2. 流程定义id进行获取
String processDefinitionId = "qjlc:2:104"; // 流程定义id
// 直接获得png图片的名称
// 根据流程定义id查询流程定义对象
ProcessDefinitionQuery query = processEngine.getRepositoryService().createProcessDefinitionQuery();
query.processDefinitionId(processDefinitionId);
ProcessDefinition processDefinition = query.singleResult();
// 根据流程定义对象获得png图片的名称
String pngName = processDefinition.getDiagramResourceName();

// 直接获得png图片对应的输入流
InputStream pngStream = processEngine.getRepositoryService().getProcessDiagram(processDefinitionId);
// 读取输入流写到指定的本地磁盘上
FileUtils.copyInputStreamToFile(pngStream, new File("F:\\" + pngName));
pngStream.close();
```

### 流程实例化
```java
// 方式一 通过流程定义id
String processDefinitionId = "qjlc:2:104"; // 流程定义id
ProcessInstance processInstance = processEngine.getRuntimeService()
        .startProcessInstanceById(processDefinitionId); // 根据请假流程定义来具体地请一次假，即启动流程实例
System.out.println(processInstance.getId());

// 方式二：根据流程定义的key来启动流程实例(建议)——可以自动选择最新版本的流程定义来启动流程实例
String processDefinitionKey = "qjlc"; // 流程定义的key
ProcessInstance processInstance = processEngine.getRuntimeService().startProcessInstanceByKey(processDefinitionKey);
```

### 流程实例查询

```java
// 流程实例查询对象，操作的是流程实例表(act_ru_execution)
ProcessInstanceQuery query = processEngine.getRuntimeService().createProcessInstanceQuery();
List<ProcessInstance> list = query.list();
for (ProcessInstance processInstance : list) {
    System.out.println(processInstance.getId());
}
```

### 流程实例删除
```java
String processInstanceId = "1001"; // 流程实例id
String deleteReason = "不请假了"; // 删除原因，任君写
processEngine.getRuntimeService().deleteProcessInstance(processInstanceId, deleteReason);
```

## 三、 任务
### 3.1任务查询
```java
// 任务查询对象，对应操作的数据库表是任务表(act_ru_task)
TaskQuery query = processEngine.getTaskService().createTaskQuery();
query.taskAssignee("张三");
List<Task> list = query.list();
for (Task task : list) {
    System.out.println(task.getId() + "\t" + task.getName());
}
```
### 3.2任务办理
```java
String taskId = "1104"; // 任务id
processEngine.getTaskService().complete(taskId);
```

## 四、 数据库设计

Activiti后台数据库由23张表组成，所有的表都以ACT_开头。第二部分是表示用途的两个字母标识。用途也和服务的API对应。

ACT\_RE\_\*：’RE’表示repository。这个前缀的表包含了流程定义和流程静态资源 （图片，规则等等）。  
ACT\_RU\_\*：’RU’表示runtime。这些是运行时的表，包含流程实例，任务，变量，异步任务等运行中的数据。Activiti只在流程实例执行过程中保存这些数据， 在流程结束时就会删除这些记录。这样运行时表可以一直很小且速度很快。  
ACT\_ID\_\*：’ID’表示identity。这些表包含身份信息，比如用户，组等等。  
ACT\_HI\_\*：’HI’表示history。这些表包含历史数据，比如历史流程实例，变量，任务等等。  
ACT\_GE\_\*：通用数据，用于不同场景下。  

- 资源库流程规则表  
act_re_deployment：部署信息表  
act_re_model：流程设计模型部署表  
act_re_procdef：流程定义数据表  

- 运行时数据库表
act_ru_execution：运行时流程执行实例表  
act_ru_identitylink：运行时流程人员表，主要存储任务节点与参与者的相关信息  
act_ru_task：运行时任务节点表  
act_ru_variable：运行时流程变量数据表  

- 历史数据库表  
act_hi_actinst：历史节点表  
act_hi_attachment：历史附件表  
act_hi_comment：历史意见表  
act_hi_identitylink：历史流程人员表  
act_hi_detail ：历史详情表，提供历史变量的查询  
act_hi_procinst：历史流程实例表  
act_hi_taskinst：历史任务实例表  
act_hi_varinst：历史变量表  

- 组织机构表  
act_id_group ：用户组信息表  
act_id_info：用户扩展信息表  
act_id_membership：用户与用户组对应信息表  
act_id_user：用户信息表  
`这四张表很常见，基本的组织机构管理，关于用户认证方面建议还是自己开发一套，组件自带的功能太简单，使用中有很多需求难以满足。`

- 通用数据表  
act_ge_bytearray：二进制数据表  
act_ge_property：属性数据表存储整个流程引擎级别的数据，初始化表结构时会默认插入三条记录



## 五、 Summary
- 几个和流程相关的对象   
 - Deployment：部署对象，和部署表(act_re_deployment)对应  
 - ProcessDefinition：流程定义对象，和流程定义表(act_re_procdef)对应  
 - ProcessInstance：流程实例对象，和流程实例表(act_ru_execution)对应  
 - Task：任务对象，和任务表(act_ru_task)对应  


- 几个Service对象   
 - RepositoryService：操作部署、流程定义等静态资源信息  
 - RuntimeService：操作流程实例，启动流程实例、查询流程实例、删除流程实例等动态信息  
 - TaskService：操作任务，查询任务、办理任务等和任务相关的信息  
 - HistoryService：操作历史信息的，查询历史信息  
 - IdentityService：操作用户和组  


- 几个Query对象   
 - DeploymentQuery：对应查询部署表(act_re_deployment)  
 - ProcessDefinitionQuery：对应查询流程定义表(act_re_procdef)  
 - ProcessInstanceQuery：对应查询流程实例表(act_ru_execution)  
 - TaskQuery：对应查询任务表(act_ru_task) 


# ACTIVITI 与 Spring Boot

## ACTITIVI 项目数据初始化
在测试ACTIVI之前可以下载一个activiti-explorer和activiti-rest可war包进行测试，只需要修改其配置文件`db.properties`和添加相应的数据库连接包(也看以不做任何配置使用默认的内存数据H2，但不方便后续的调试和跟踪开发)。

## Activiti 相关子项目
- activiti-rest 提供一些 Restful API
- activiti-spring 方便与 Spring 框架整合
- activiti-diagram-rest 提供 Diagram-Viewer 访问的 Restful API




## FIXED BUG

[**\# Activiti Diagram Viewer Get Diagram Layout Failure Parsererror#**](https://stackoverflow.com/questions/44712298/activiti-diagram-viewer-get-diagram-layout-failure-parsererror)  

Just **comment dataType** line in ActivitiRest.js.There should be three positions. like this:

```javascript
$.ajax({
        url: url,
        //dataType: 'jsonp', //just comment here
        cache: false,
        async: true,
        success: function(data, textStatus) {
            var processDefinition = data;
            if (!processDefinition) {
                console.error("Process definition '" + processDefinitionKey + "' not found");
            } else {
              callback.apply({processDefinitionId: processDefinition.id});
            }
        }
    }).done
```

