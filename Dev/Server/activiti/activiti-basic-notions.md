## Aciviti 重要概念理解

在创建好工作流模型 ( MODEL )后，需要对将静态的 XML 资源文件进行管理的执行，形成动态的流程管理过程。首先除了创建模型，创建模型的方式大致有三种，基于 Eclipse 或 IntelliJ IDEA 的插件、基于Activiti-Modeler 或基于 Activiti 模型的程序式创建。

### 1. 部署  

创建出来的模型文件或以 bar、zip、bpmn[20]、xml 等形式文件存在，或直接存储在 Activiti 的数据库表（ ACT_RE_MODEL ）中。这两种方式都是纯静态的资源文件。离工作流这个动态的管理执行过程还有一步之遥——**部署**。  

#### 1.1 API  
```
processEngine.getRepositoryService() // 获取 repositoryService
    .createDeployment() // 创建 deployment 
    .name(“入门程序”) // 设置部署 name
    .addClasspathResource(“hello/helloworld.bpmn”) // 添加资源，还有其他方式
    .deploy(); // 真正部署
```
#### 1.2 说明
部署整个过程共涉及到三张表：ACT_RE_DEPLOYMENT、ACT_RE_PROCDEF、ACT_GE_BYTEARRAY.

- ACT_RE_DEPLOYMENT  
存放流程定义的显示名和部署时间，每部署一次增加一条记录。即，当前部署的记录者，记录部署的名称和时间。
- ACT_RE_PROCDEF  
存放流程定义的属性信息，部署每个新的流程定义都会在这张表中增加一条记录。即，记录部署的结果信息，包含 ProcessDefinition 的 ID、 NAME、KEY、REOURCE 等。
**注意**：当流程定义的key相同的情况下，使用的是版本升级。
- ACT_GE_BYTEARRAY  
存储流程定义资源信息。每部署一次就会增加两条记录，一条是关于 bpmn 规则文件，一条是图片的（如果部署时只指定了 bpmn 一个文件，activiti 会在部署时解析 bpmn 文件内容自动生成流程图）。一般来说，这两个文件不会太大，因此都是以二进制形式存储在数据库中。 

### 2. 启动实例

#### 2.1 API
```
runtimeService.startProcessByKey("processKey");
```
#### 2.2 说明
ProcessInstance 运行过程所操作数据库的是 ACT_RU_EXECUTION 表。在 ProcessInstance 运行过程中，如果遇到的节点为用户任务节点就会在 ACT_RU_EXECUTION 表中新添一条记录，同时也会在 ACT_RU_TASK 添加一条记录。 ACT_RU_EXECUTION 表，对于当前正在运行的执行对象表，ACT_ID. 

### 3. 执行任务

#### 3.1 API  
```
taskService.completeTask(taskId);
```
#### 3.2 说明 
- 当执行完任务，再以当前员工去任务查询的时，会发现这个时候已经没有数据了，因为正在执行的任务中没有数据；  
- 对于执行完的任务，activiti 将从 ACT_RU_TASK 表中删除该任务，下一个任务会被插入进来。 
- 以”部门经理”的身份进行查询，可以查到结果。因为流程执行到部门经理审批这个节点了。 
- 再执行办理任务代码，执行完以后以”部门经理”身份进行查询，没有结果。 
- 重复上述步骤直到流程执行完毕。






