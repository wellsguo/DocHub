## RecyclerView (二) 列表项操作

除了要以特定的形式展示各个 Item，我们经常还有列表项的单击事件、添加列表项、删除列表项等。

### 1. 列表项的单击事件

不幸的是 RecyclerView 控件没有与 ListView 一样的 onItemClickListener 单击事件监听器，那么就需要我们自定义onItemClickListener。

```java
public class MyRecyclerAdapter extends RecyclerView.Adapter<MyRecyclerAdapter.MyViewHolder> {
    private List<String> list;  //列表数据
    private OnItemClickListener mOnItemClickListener;

    public MyRecyclerAdapter(List<String> list) {
        this.list = list;
    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    @Override
    public void onBindViewHolder(MyViewHolder holder, final int position) {
        holder.tv.setText(list.get(position));

        //实现列表item单击事件，主要使用java interface来实现回调MainActivity中的onItemClick函数
        if(mOnItemClickListener!=null){
            holder.itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    mOnItemClickListener.onItemClick(v, position);
                }
            });
        }
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup viewGroup, int viewType) {
        MyViewHolder holder = new MyViewHolder(View.inflate(viewGroup.getContext(), R.layout.list_item, null));
        return holder;
    }

    public interface OnItemClickListener{
        void onItemClick(View view, int position);
    }

    public void setOnItemClickListener(OnItemClickListener listener){
        this.mOnItemClickListener = listener;
    }

    class MyViewHolder extends RecyclerView.ViewHolder{
        TextView tv;

        public MyViewHolder(View view) {
            super(view);
            tv = (TextView)view.findViewById(R.id.text1);
        }
    }
}
```

我们先回顾一下listview的itemOnclickListener在代码中是如何运用的：

```java
//listview列表项单击事件，放在一个Activity里，例如MainActivity
lvFence.setOnItemClickListener(new AdapterView.OnItemClickListener() {
    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) 
       //在这里添加单击处理代码
        return;
    }
});
```

上述代码通过调用listview的setOnItemClickListener函数为listview设置了一个 单击监听器OnItemClickListener类对象，我们从中能分析到什么？

- （1）Listview 类里有一个成员变量,该成员变量是一个 OnItemClickListener 类的实例对象。同时，有一个 setOnItemClickListener 函数来设置该成员变量的具体实例值。
- （2）从 new AdapterView.OnItemClickListener() 这行代码可以猜测 OnItemClickListener 可能是定义在 ListView 类中的一个抽象接口，需要在 MainActivity 里通过实现（实例化）这个接口以及它包含的抽象函数onItemClick 来处理业务逻辑。当ListView列表项被单击时，ListView会调用OnItemClickListener类型的成员对象（已通过 setOnItemClickListener 赋值）的 onItemClick 函数，由于 onItemClick 函数实质是在 MainActivity 里实现的，因此 onItemClick 的处理代码将在 MainActivity 里执行，这也就是我们通常所说的“回调”，即在 MainActivity 里先实现抽象函数，这时并没有调用，而是在恰当的时机回过头来调用 onItemClick 函数。

综合(1)(2)分析类比，我们为 RecyclerView 控件自定义了列表项监听功能，具体步骤如下：

- **第一步**，在适配器 MyRecyclerAdapter 类里定义抽象接口 `OnItemClickListener`，其中有一个抽象函数 onItemClick。

- **第二步**，在适配器 MyRecyclerAdapter 类声明一个 OnItemClickListener 类型的成员变量与 setOnItemClickListener 函数。

- **第三步**，在 Activity（例如MainActivity）里实现化接口 OnItemClickListener 及 OnItemClick 函数，并调用 setOnItemClickListener 函数为 MyRecyclerAdapter 中的 OnItemClickListener 类型成员变量赋值。

- **第四步**，回调。在 MyRecyclerAsetOnClickListenerdapter 的 onBindViewHolder 函数里为列表项对应的VIEW布局的单击函数
（这个系统里已经有了，就是普通的按钮单击事件处理）里回调onItemClick函数，具体核心代码如下：  
```java
//实现列表item单击事件，主要使用java interface来实现回调MainActivity中的onItemClick函数
if(mOnItemClickListener!=null){
    holder.itemView.setOnClickListener(new View.OnClickListener() {

    @Override
    public void onClick(View v) {
        mOnItemClickListener.onItemClick(v, position);
    }
    });
}
```
到此，为RecyclerView控件补充我们自定义的列表项单击事件分析完毕，具体源码在文章最后。

### 2. RecyclerView 添加、删除列表项与高效更新

当我们更新RecyclerView控件的列表数据时，以往的作法有如下：

- （1）setAdapter ，为控件配置数据适配器，同时刷新全部列表项
- （2）notifyDataSetChanged 刷新全部列表项数据

以上2种作法比较影响效率，RecyclerView 控件为我们提供了更有效率的两个刷新列表项函数：

#### 2.1. notifyItemInserted(int position) 

用于在某一个列表项位置 `position` 上新添加一个列表项的情况下刷新列表。示例代码如下：

```java
list.add(position,"additem"+position);   //在列表数据数组List<String>的position位置上添加一个新数据 
//notifyDataSetChanged();--会影响效率

notifyItemInserted(position);
```
 

其中 `notifyItemInserted(position)` 不会重新刷新整个列表数据，只是在 `position` 位置上新绘制一个列表项，同时原来 `position` 位置上的列表项的索引变为 `position + 1`，即从原 `position` 位置开始的列表项统一后移。

#### 2.2. notifyItemRemoved(int position) 

```java
list.remove(position,"additem"+position);   //在列表数据数组List<String>的position位置上删除一个新数据 
//notifyDataSetChanged();--会影响效率=

notifyItemRemoved(position);
```
其中 `notifyItemInserted(position)` 不会重新刷新整个列表数据，只是在 `position` 位置上删除一个列表项，
同时原来 `position+1` 位置上的列表项的索引变为 `position`，即从原 `position+1` 位置开始的列表项统一前移。

### 3. 完整的代码

##### 布局文件

```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    >
 
    <android.support.v7.widget.RecyclerView
        android:id="@+id/recylerview"
        android:layout_width="match_parent"
        android:layout_height="400dp"
        />
 
    <LinearLayout
        android:layout_marginTop="30dp"
        android:layout_below="@+id/recylerview"
        android:orientation="horizontal"
        android:layout_width="match_parent"
        android:layout_height="match_parent">
 
        <Button
            android:id="@+id/btAdd"
            android:text="添加"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" />
 
        <Button
            android:layout_marginLeft="20dp"
            android:id="@+id/btDelete"
            android:text="删除"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" />
    </LinearLayout>
 
</RelativeLayout>
```

##### MainActivity
   
```java
public class MainActivity extends Activity {

    private RecyclerView recylerview;  //RecyclerView控件实例对象
    private ArrayList<String> list;    //RecyclerView要显示的 列表数据，在此为一组字符串。
    private MyRecyclerAdapter adapter; //同ListView一样，需要一个适配器来 将list数据 装载到 RecyclerView列表控件。
    //private MyStaggedRecyclerAdapter adapter;  //列表显示风格为瀑布流界面样式的适配器。
    boolean isGrid = true;
 
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        initData();
    }
 
    public void initView(){
        //实例化布局中的recylerview控件
        recylerview = (RecyclerView)findViewById(R.id.recylerview);
        Button btAdd = findViewById(R.id.btAdd);
        Button btDelete = findViewById(R.id.btDelete);
        Button btConvert = findViewById(R.id.btConvert);
    
        btAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                adapter.addData(3);
            }
        });
    
        btDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                adapter.removeData(3);
            }
        });
    }
 
    public void initData(){
        //模拟60条数据
        list = new ArrayList<String>();

        for (int i = 0; i < 60; i++) {
            list.add("item"+i);
        }
        //普通列表的适配器
        adapter = new MyRecyclerAdapter(list);
        //列表显示风格为 垂直方向的列表
        //recylerview.setLayoutManager(new LinearLayoutManager(this));
        //列表显示风格为 水平方向的列表
        //recylerview.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, true));
        //列表显示风格为 瀑布流样式
        recylerview.setLayoutManager(new StaggeredGridLayoutManager(3, LinearLayoutManager.VERTICAL));
        //列表显示风格为 网格样式，如9宫格布局
        //recylerview.setLayoutManager(new GridLayoutManager(this, 3));

        //瀑布流适配器，与普通适配器adapter的区别是，每一个列表项的布局大小都可能参差不齐 
        //adapter = new MyStaggedRecyclerAdapter(list); 
        //装载显示列表数据 
        recylerview.setAdapter(adapter); 
        //添加删除列表项时会有动画效果，具体运行源码查看。
        recylerview.setItemAnimator(new DefaultItemAnimator());

        adapter.setOnItemClickListener(new OnItemClickListener() { 
            @Override public void onItemClick(View view, int position) { 
                Toast.makeText(MainActivity.this, "点了"+position, Toast.LENGTH_SHORT).show();
            }
        });
        return; 
    }
}
```

##### Adapter
 
```java
public class MyRecyclerAdapter extends RecyclerView.Adapter<MyRecyclerAdapter.MyViewHolder> {
 
    private List<String> list;  //列表数据
    private OnItemClickListener mOnItemClickListener;
    
    public MyRecyclerAdapter(List<String> list) {
        this.list = list;
    }
    
    class MyViewHolder extends RecyclerView.ViewHolder{
        TextView tv;
        public MyViewHolder(View view) {
            super(view);
            tv = (TextView)view.findViewById(R.id.text1);
        }
    }
    
    @Override
    public int getItemCount() {
        return list.size();
    }
    
    @Override
    public void onBindViewHolder(MyViewHolder holder, final int position) {
        holder.tv.setText(list.get(position));   //将列表数据list数组中的position位置的字符串 填充给 这个列表项上的textview
    
        //实现列表item单击事件，主要使用java interface来实现回调MainActivity中的onItemClick函数
        if(mOnItemClickListener!=null){
            holder.itemView.setOnClickListener(new View.OnClickListener() {
    
                @Override
                public void onClick(View v) {
                mOnItemClickListener.onItemClick(v, position);
                }
            });
        }
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup viewGroup, int arg1) {
        MyViewHolder holder = new MyViewHolder(View.inflate(viewGroup.getContext(), R.layout.list_item, null));
        return holder;
    }
    
    
    public void addData(int position){
        list.add(position,"additem"+position);
        // 提示刷新--会影响效率
        // notifyDataSetChanged();
        notifyItemInserted(position);
    }
    public void removeData(int position){
        list.remove(position);
        notifyItemRemoved(position);
    }
    
    public interface OnItemClickListener{
        void onItemClick(View view, int position);
    }
    
    public void setOnItemClickListener(OnItemClickListener listener){
        this.mOnItemClickListener = listener;
    }
}
```
