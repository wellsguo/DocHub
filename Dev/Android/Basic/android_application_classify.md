>《App研发录》对移动应用分为三种: **数据展示类应用**，**手机助手类应用**，**游戏**。  

**数据展示类**: 应用特点是页面多，需要频繁调用后端接口进行数据交互，一般都涉及支付流程，考验弱网络环境下数据的正常获取，减少电量和流量消耗。  
**手机助手类**: 应用则主要着眼于系统API的调用，达到辅助管理系统的目的。  
我们一般做的应用都是数据展示类型应用，然而一般应用上了规模也或多或少会涉及到系统API的调用，暂且不表。


但是，假如现在要做的不是Demo，而是一个商城应用的购物车页面呢？或者是商品详情页面，订单结算页面呢，这些页面都有大量的__<u>控件初始化，数据增删改查，手势操作</u>__，如果这些事情都交给Activity/Fragment来做，那么一个类的代码很快就会破千行。涉及到诸如用户数据之类的应用全局共享数据，又或是检查缓存之类的功能，Activity/Fragment的负担也会十分繁重。

对于这种问题，解决方法就是要分担Activity和Fragment的工作，**一般来说，页面无关的方法，我们都会将其放到工具类里面，比如验证手机号、邮箱之类的正则，对Log的封装，而网络调用一般是通过异步网络库来做的，比如volley，Retrofit，封装为一个个Request，Call，通过将这些代码抽出来，**会小幅改善Activity和Fragment压力过大的情况，(如何使用和封装这些网络框架请参见相关博文，此处不赘述也不写示例了)

我做的第一个应用就是这样的架构，应用比较简单，但是写起来还是比较蹩脚，因为除了网络调用，Activity/Fragment还需要操作当前的Java Entity对象，操作本地数据库，操作本地文件等。**比如获取当前用户信息的缓存，或者获取文章列表，购物车列表之类的数据，有可能涉及到多个页面使用数据，而获取数据也有一定的检查，比如分页加载和下拉刷新的判断，是否使用缓存等。**这些操作本身不应由Activity和Fragment来做，将这些操作放在网络模块或者Java Entities里面明显都不很合理。**Java Entity本身就应该只是一个数据库数据映射的Java对象模型**，赋予其管理缓存数据的职责只会让其变得混乱，功能不明确。比如涉及到分页加载的列表，如新闻列表，如果我在Model包中定义一个NewsList，那么这个NewsList到底是一个数据模型呢，还是一个数据管理者呢？想必以后看代码的时候，可能会困惑一下。**User的数据一般是应用内全局使用的，如果我将其定义成一个单例模式，JSON反序列化之类的操作又会比较蛋疼了。而放在网络模块就更不合理了，为什么我注销用户会需要一个UserCall对象？**

在有了上面的困惑之后，改良的方案已经呼之欲出了：**抽象出一个新的管理者，让它去协调缓存与网络调用。** (在开发中，可能会出现模块间或不同任务功能模块的划分不清，可以通过新起一个 Manager 来协调)    
其实在试图处理分页加载的数据缓存的时候，这个新的数据管理者就已经初步成形了，NewsList这个所谓的Model实际上就是一个数据管理者。只不过它的数据刷新需要依靠Activity/Fragment调用网络回调之后再set给它而已。先抛开细枝末节仔细回想一下，从客户端的UI点击响应向服务端发起请求，到服务端返回数据刷新UI，其实是有一个清晰的数据流的：  
> UI发起请求 &#8594; 检查缓存 &#8594; 调用网络模块 &#8594; 解析返回JSON / 统一处理异常 &#8594; JSON对象映射为Java对象 &#8594; 缓存 &#8594; UI获取数据并展示

通过这个数据流，可以很明显的网络数据请求的一个三级分层：**UI层**，**数据管理层**(缓存处理，请求网络)，**网络调用层**   
继续以分页加载新闻列表这个例子来说：
之前只是声明了一个 NewsList 的 Model，只有存储数据的功能，对于一个 Java Entity 来说，可能 NewsList 是这样的
```
public class NewsList {
	//当前新闻列表
	private List<News> newsList = new ArrayList<News>();
	//当前页码
	private int currentPage = 1;
	//总页码
	private int totalPage = 1;
 
	public NewsList() {
		......
	}
 
	public void addToList(List<News> list, int currentPage) {
		newsList.addAll(list);
		this.currentPage = currentPage;
	}
 
	public void setTotalPage(int totalPage) {
		this.totalPage = totalPage;
	}
 
	public void getTotalPage() {
		return totalPage;
	}
	/*
     * 以下各种 set 和 get 就不占篇幅了，这里也有一个上面所述的问题，即对于一个数据管理者来说，
	 * 要开放 get / set 把私有数据给外部用么？
     * 如果不开放，它是 Entity 么？
     * 这也是职责混乱的一个体现吧...
     */
}
```

现在不妨将其提升为 NewsListManager，也许它看上去就会更加合理了：
```
//首先定义一个获取数据的回调接口
public interface ActionCallbackListener<T> {
	void onSuccess(T data);
 
	void onFailed(Exception e, String message);//这里异常返回可以是处理过的异常id，也可以是原始的Exception对象，按照自己设计即可
}
```

```
//Manager对象的实现
public class NewsListManager extends BaseDataManager {
	//当前新闻列表
	private List<News> mNewsList = new ArrayList<News>();
	//当前页码
	private int currentPage = 1;
	//总页码
	private int totalPage = 1;
 
	public NewsListManager() {
		getCacheFromDatabase();
	}
 
	public List<News> getCachedData() {
		return mNewsList;
	}
 
	public void pageLoadNewsList(boolean isRefresh, final ActionCallbackListener<List<News>> mActionCallbackerListener) {
		if(isRefresh) {
			clearCache();
			mNewsList.clear();
			currentPage = 1;
		}
		NewsListRequest request = new NewsListRequest(); //假定这里是网络调用模块请求新闻列表的Request对象，细节不表
		request.setData(currentPage);
		request.request(new RequestCallback() {
			@Override
			void onSuccess(JSONObject response) {
				totalPage = response.optInt("total_page");
				currentPage = response.optInt("current_page");
				//将网络数据存储到manager....... 
				saveToDataBase()
				if(mActionCallbackerListener != null) {
					mActionCallbackListener.onSuccess(mNewsList);
				}
			}
			@Override
			void onFailed(Exception e, String message) {
				if(mActionCallbackerListener != null) {
					mActionCallbackListener.onFailed(e, message);
				}
			}
		});
	}
 
	private void getCacheFromDatabase() {
		//将缓存数据从数据库中取出
	}
 
	private void saveToDatabase() {
		//缓存新闻数据至数据库
	}
 
	private void clearCache() {
		//清除数据库中的缓存
	}
	//......
}
```

可以看到通过这样的封装，UI层根本不需要管理分页加载的逻辑，只需要调用NewsListManager的pageLoadNewsList()方法，告诉Manager是否需要刷新即可，与UI的处理逻辑(下拉刷新，分页加载)一致，这样就极大的简化了Activity和Fragment的工作。同理，这样的逻辑也可以应用于应用使用的用户数据，通过isRefresh去判断是否需要从服务端重新拉取，因为大部分应用修改用户数据的入口就那么几个，大部分情况下是不需要每次请求用户数据都用request从网络获取的，Manager实现的缓存机制就可以大幅减少不必要的接口调用，但是UI层请求数据的方法并没有任何改变。  

通过Manager的封装，可以将整个应用分为三层：UI，Managers，NetModules。注意所谓分层并不是随便分几个package而已，而是有严格的职责和权限划分的，即每层都各有其职，每一层都向上层提供接口，封闭细节。比如UI层向Manager发起数据请求，并不需要关心Manager使用的是缓存还是网络请求，也不需要关心网络请求如何封装的报文参数。只需要根据Manager提供的接口参数发起请求，即可获得数据。这种架构大概是这个样子的：

由于绝大部分代码都从Activity和Fragment中剥离，现在Activity/Fragment只负责UI控制与数据获取，其它的绝大部分代码都可以做到UI无关，如果在开发中尽力确保这一点，那么在接口设计合理的基础之上，现有的Managers，网络模块以及其它一些工具类完全可以构成一个AppSDK，为手机，平板应用提供支持，项目无关的工具类和通用控件，则可以划归到公共开发资源库模块，大幅减少重复工作量。







