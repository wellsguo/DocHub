## RRecyclerView（五）飞虎潜行极战之切换

![](https://img-blog.csdn.net/2018051215203218)

RecyclerView控件还有一个非常方便的功能，就是可以动态改变RecyclerView控件的展示风格，即在列表与网格Grid布局之间自由切换，先上效果图《飞虎队剧照》：

### 1. MainActivity

```java
public class MainActivity extends Activity {

    private RecyclerView recylerview;  //RecyclerView控件实例对象
    //RecyclerView要显示的 列表数据，在此为一组字符串。
    private MyRecyclerAdapter adapter; //同ListView一样，需要一个适配器来 将list数据 装载到 RecyclerView列表控件。
    //private MyStaggedRecyclerAdapter adapter;  //列表显示风格  为瀑布流 界面样式 的 适配器。
    boolean isGrid = true;
    Button btConvert;
    DividerGridViewItemDecoration mGridViewItemDecoration;
    MyListItemDecoration myListItemDecoration;
    private RecyclerView.ItemDecoration myItemDecoration;

    private int[] list= new int[]{
            R.drawable.fone,
            R.drawable.ftwo,
            R.drawable.fthree,
            R.drawable.ffour,
            R.drawable.ffive,
            R.drawable.fsix,
            R.drawable.fseven,
            R.drawable.feight,
            R.drawable.fnine,
            R.drawable.ften,
            R.drawable.feleven,
            R.drawable.ftwelve,
            R.drawable.thirteen
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        // initData();
    }

    public void initView(){
        mGridViewItemDecoration = new DividerGridViewItemDecoration(MainActivity.this);
        myListItemDecoration = new MyListItemDecoration(MainActivity.this,LinearLayout.VERTICAL);

        btConvert = findViewById(R.id.btConvert);

        //实例化布局中的recylerview控件
        recylerview = (RecyclerView)findViewById(R.id.recylerview);


        //普通列表的适配器
        adapter = new MyRecyclerAdapter(list);

        //recylerview.setLayoutManager(new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false));//列表显示风格为 水平方向的列表
        //列表显示风格为 垂直方向的列表
        //recylerview.setLayoutManager(new LinearLayoutManager(this));

        //显示风格为网格，2列
        recylerview.setLayoutManager(new GridLayoutManager(this, 2));
        //装载显示列表数据

        myItemDecoration = new DividerGridViewItemDecoration(this);
        //recylerview.addItemDecoration(new MyListItemDecoration(this, LinearLayout.VERTICAL));
        recylerview.addItemDecoration(myItemDecoration);

        recylerview.setItemAnimator(new DefaultItemAnimator());

        adapter.setOnItemClickListener(new MyRecyclerAdapter.OnItemClickListener(){
            @Override
            public void onItemClick(View view, int position) {
                Toast.makeText(MainActivity.this, "点了"+position, Toast.LENGTH_SHORT).show();
            }
        });

        recylerview.setAdapter(adapter);
        
        btConvert.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(myItemDecoration!=null){
                    recylerview.removeItemDecoration(myItemDecoration);
                }
                
                if(!isGrid){
                    recylerview.setLayoutManager(new GridLayoutManager(MainActivity.this, 2));
                    //recylerview.setLayoutManager(new LinearLayoutManager(this,LinearLayoutManager.HORIZONTAL,false));//默认垂直
                    myItemDecoration = new DividerGridViewItemDecoration(MainActivity.this);
                    recylerview.addItemDecoration(myItemDecoration);
                } else {
                    recylerview.setLayoutManager(new LinearLayoutManager(MainActivity.this,LinearLayout.VERTICAL,false));//默认垂直
                    myItemDecoration = new MyListItemDecoration(MainActivity.this, LinearLayoutManager.VERTICAL);
                    recylerview.addItemDecoration(myItemDecoration);
                }
                isGrid = !isGrid;
            }
        });
        return;
    }
}
```

这里值得注意的是以下代码：

```java
if(myItemDecoration!=null){
    recylerview.removeItemDecoration(myItemDecoration); 
}
```

如果事先不移除的话，会出现分割线重复绘制越来越粗.


### 2. adapter

```java
public class MyRecyclerAdapter extends RecyclerView.Adapter<MyRecyclerAdapter.MyViewHolder> {
 
	private int[] list;
	private OnItemClickListener mOnItemClickListener;
 
	public MyRecyclerAdapter(int[] list) {
		this.list = list;
	}
 
	class MyViewHolder extends RecyclerView.ViewHolder{
		ImageView imv;
 
		public MyViewHolder(View view) {
			super(view);
			imv = (ImageView)view.findViewById(R.id.imv);
		}
		
	}
	@Override
	public int getItemCount() {
		return list.length;
	}
 
	@Override
	public void onBindViewHolder(MyViewHolder holder, final int position) {
		holder.imv.setImageResource(list[position]);
 
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
		MyViewHolder holder = new MyViewHolder(View.inflate(viewGroup.getContext(), R.layout.list_item2, null));
		return holder;
	}
 
 
	/*public void addData(int position){
		list.add(position,"additem"+position);
		notifyItemInserted(position);
	}
	public void removeData(int position){
		list.remove(position);
		notifyItemRemoved(position);
	}*/
 
	public interface OnItemClickListener{
		void onItemClick(View view, int position);
	}
 
	public void setOnItemClickListener(OnItemClickListener listener){
		this.mOnItemClickListener = listener;
	}
}
```