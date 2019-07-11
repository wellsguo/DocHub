## RecyclerView (-) 基本用法

### 1. 基本步骤

- （1）gradle 引入依赖包
- （2）Activity layout 布局中使用
- （3）编写 Item 布局
- （4）编写 Item 和数据绑定的适配器
- （5）在 Activity 中使用

#### 1.1. gradle 引入依赖包

```Groovy
dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation 'com.android.support:recyclerview-v7:28.0.0'
}
```

#### 1.2. Activity layout 布局

```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
     >
 
    <android.support.v7.widget.RecyclerView
        android:id="@+id/recylerview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        />
 
</RelativeLayout>
```

### 1.2. Item layout

```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
     >
 
    <TextView
        android:id="@+id/content"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        />
 
</RelativeLayout>
```

#### 1.4. Adapter

```java
public class MyRecyclerAdapter extends RecyclerView.Adapter<MyRecyclerAdapter.MyViewHolder> {
 
    //列表数据
    private List<String> list;  
 
    public MyRecyclerAdapter(List<String> list) {
        this.list = list;
    }

    /**
     * 要显示的列表项数
     * @return 列表项总数
     */
    @Override
    public int getItemCount() {
        return list.size();
    }
 
    /**
     * 用数据填充列表项上的 textview文本
     * @param holder：  当前列表项 布局的 控件实例
     * @param position: 列表项的索引
     */
    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        holder.tv.setText(list.get(position));   //将列表数据list数组中的position位置的字符串 填充给 这个列表项上的textview
    }
 
 
    /**
     * 为列表项实例化布局，将在onBindViewHolder里为布局控件赋值
     * @param viewGroup
     * @param arg1
     * @return
     */
    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        MyViewHolder holder = new MyViewHolder(View.inflate(viewGroup.getContext(), R.layout.list_item, null));
        return holder;
    }

    /**
     *
     * 实例化 列表项布局中的控件，在此为一个简单的textview
     */
    class MyViewHolder extends RecyclerView.ViewHolder{
        TextView tv;

        public MyViewHolder(View view) {
            super(view);
            tv = (TextView)view.findViewById(R.id.text1);
        }
    }
}
```

#### 1.5. Activity

```java
public class MainActivity extends Activity {
 
    private RecyclerView recylerview;  //RecyclerView控件实例对象
    private ArrayList<String> list;    //RecyclerView要显示的 列表数据，在此为一组字符串。
    private MyRecyclerAdapter adapter; //同ListView一样，需要一个适配器来 将list数据 装载到 RecyclerView列表控件。
    //private MyStaggedRecyclerAdapter adapter;  //列表显示风格  为瀑布流 界面样式 的 适配器。

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //模拟60条数据
        list = new ArrayList<String>();

        for (int i = 0; i < 60; i++) {
            list.add("item"+i);
        }
        //实例化布局中的recylerview控件
        recylerview = (RecyclerView)findViewById(R.id.recylerview);
        //普通列表的适配器
        adapter = new MyRecyclerAdapter(list);
        //列表显示风格为 垂直方向的列表
        //recylerview.setLayoutManager(new LinearLayoutManager(this));
        //列表显示风格为 水平方向的列表
        // recylerview.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, true));
        //列表显示风格为 瀑布流样式
        //recylerview.setLayoutManager(new StaggeredGridLayoutManager(3, LinearLayoutManager.VERTICAL));
        //列表显示风格为 网格样式，如9宫格布局
        recylerview.setLayoutManager(new GridLayoutManager(this, 3));
        //adapter = new MyStaggedRecyclerAdapter(list); 瀑布流适配器，与普通适配器adapter的区别是，每一个列表项的布局大小都可能参差不齐。
        //装载显示列表数据
        recylerview.setAdapter(adapter);
    }
}
```
### 2. 解释说明

ReyclerView 是 ListView 的升级版，相当于是 View 的 for 循环容器。与 ListView 的不同在于 RecyclerView 可以支持水平布局，垂直布局，网格布局，瀑布布局，在性能上也有很大的提升。

