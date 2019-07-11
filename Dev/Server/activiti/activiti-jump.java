package com.zdc.test;

import java.util.List;

import org.activiti.engine.HistoryService;
import org.activiti.engine.ProcessEngine;
import org.activiti.engine.ProcessEngines;
import org.activiti.engine.RepositoryService;
import org.activiti.engine.RuntimeService;
import org.activiti.engine.TaskService;
import org.activiti.engine.history.HistoricTaskInstance;
import org.activiti.engine.impl.RepositoryServiceImpl;
import org.activiti.engine.impl.RuntimeServiceImpl;
import org.activiti.engine.impl.interceptor.Command;
import org.activiti.engine.impl.interceptor.CommandContext;
import org.activiti.engine.impl.persistence.entity.ExecutionEntity;
import org.activiti.engine.impl.persistence.entity.ProcessDefinitionEntity;
import org.activiti.engine.impl.pvm.PvmTransition;
import org.activiti.engine.impl.pvm.ReadOnlyProcessDefinition;
import org.activiti.engine.impl.pvm.process.ActivityImpl;
import org.activiti.engine.impl.pvm.process.ProcessDefinitionImpl;
import org.activiti.engine.impl.pvm.process.TransitionImpl;
import org.activiti.engine.repository.DeploymentBuilder;
import org.activiti.engine.runtime.Execution;
import org.activiti.engine.runtime.ProcessInstance;
import org.activiti.engine.task.Task;
import org.junit.Test;

public class TestBuildTables {

	ProcessEngine processEngine = ProcessEngines.getDefaultProcessEngine();

	/**
	 * 部署流程
	 */
	public void DeploymentProcess() {
		DeploymentBuilder builder = processEngine.getRepositoryService().createDeployment();
		builder.addClasspathResource("ziyouliu.bpmn");
		builder.addClasspathResource("ziyouliu.png");
		builder.deploy();
		System.out.println("创建成功");
	}

	/**
	 * 启动流程
	 */

	public void StartProcess() {
		ProcessInstance processInstance = processEngine.getRuntimeService().startProcessInstanceById("ziyouliu:1:4");
		String id = processInstance.getId();
		System.out.println("启动流程成功，流程的Id是：" + id);
	}

	/**
	 * 查询所有的活动节点
	 */
	public void queryAllActivities() {

		RepositoryService repositoryService = processEngine.getRepositoryService();
		ReadOnlyProcessDefinition deployedProcessDefinition = (ProcessDefinitionEntity) ((RepositoryServiceImpl) repositoryService)
				.getDeployedProcessDefinition("ziyouliu:1:4");
		List<ActivityImpl> activities = (List<ActivityImpl>) deployedProcessDefinition.getActivities();
		for (ActivityImpl activityImpl : activities) {
			System.out.println(activityImpl.getId() + "活动节点的名称:" + activityImpl.getProperty("name"));

		}
	}

	/**
	 * 根据ActivityId 查询出来想要活动Activity
	 * 
	 * @param id
	 * @return
	 */
	public ActivityImpl queryTargetActivity(String id) {

		RepositoryService repositoryService = processEngine.getRepositoryService();
		ReadOnlyProcessDefinition deployedProcessDefinition = (ProcessDefinitionEntity) ((RepositoryServiceImpl) repositoryService)
				.getDeployedProcessDefinition("ziyouliu:1:4");
		List<ActivityImpl> activities = (List<ActivityImpl>) deployedProcessDefinition.getActivities();
		for (ActivityImpl activityImpl : activities) {
			if (activityImpl.getId().equals(id)) {
				return activityImpl;
			}
		}
		return null;
	}

	/**
	 * 查询当前的活动节点
	 */
	public ActivityImpl qureyCurrentTask(String processDefinitionId) {
		RuntimeService runtimeService = processEngine.getRuntimeService();
		// String processDefinitionId="ziyouliu:1:4";
		Execution execution = runtimeService.createExecutionQuery().processDefinitionId(processDefinitionId)
				.singleResult();
		String activityId = execution.getActivityId();
		ActivityImpl currentActivity = queryTargetActivity(activityId);
		System.out.println(currentActivity.getId() + "" + currentActivity.getProperty("name"));
		return currentActivity;
	}

	/**
	 * 第一种自由跳转的方式: 这种方式是通过 重写命令 ，推荐这种方式进行实现(这种方式的跳转，最后可以通过taskDeleteReason 来进行查询 )
	 */
	public void jumpEndActivity() {
		// 当前节点
		ActivityImpl currentActivityImpl = qureyCurrentTask("ziyouliu:1:4");
		// 目标节点
		ActivityImpl targetActivity = queryTargetActivity("shenchajigou");
		// 当前正在执行的流程实例Id
		final String executionId = "7501";

		((RuntimeServiceImpl) processEngine.getRuntimeService()).getCommandExecutor().execute(new Command<Object>() {
			public Object execute(CommandContext commandContext) {
				ExecutionEntity execution = commandContext.getExecutionEntityManager().findExecutionById(executionId);
				execution.destroyScope("jump"); //
				ProcessDefinitionImpl processDefinition = execution.getProcessDefinition();
				ActivityImpl findActivity = processDefinition.findActivity("endevent1");
				execution.executeActivity(findActivity);
				return execution;
			}

		});
		System.out.println("完成");
	}

	/**
	 * 查询跳转 通过 taskDeleteReason 可以设置为废除 等 taskDeleteReason 对应数据库表中act_hi_taskinst 的
	 * delete_reason_ 字段;
	 * 
	 */
	public void queryAbolishActivity() {
		HistoryService historyService = processEngine.getHistoryService();
		List<HistoricTaskInstance> list = historyService.createHistoricTaskInstanceQuery()
				.processDefinitionId("ziyouliu:1:4").taskDeleteReason("jump").list();
		for (HistoricTaskInstance historicTaskInstance : list) {
			System.out
					.println("流程的名字是:" + historicTaskInstance.getName() + "分配人：" + historicTaskInstance.getAssignee());
		}
	}

	/**
	 * 第二种自由跳转的方式 这种是通过改变 流程的路线来进行跳转
	 */
	@Test
	public void JumpEndActivity() {
		TaskService taskService = processEngine.getTaskService();
		Task task = taskService.createTaskQuery().processDefinitionId("ziyouliu:1:4").taskAssignee("zuzhang")
				.singleResult();
		ActivityImpl currentActivity = qureyCurrentTask("ziyouliu:1:4");
		ActivityImpl targetActivity = queryTargetActivity("endevent1");
		// 通过活动可以获得流程 将要出去的路线，只要更改出去的目的Activity ，就可以实现自由的跳转

		List<PvmTransition> outgoingTransitions = currentActivity.getOutgoingTransitions();
		for (PvmTransition pvmTransition : outgoingTransitions) {
			TransitionImpl transitionImpl = (TransitionImpl) pvmTransition;
			transitionImpl.setDestination(targetActivity);
		}
		taskService.complete(task.getId());

	}

}
