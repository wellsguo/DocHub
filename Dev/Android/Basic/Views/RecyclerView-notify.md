## Recycle 数据刷新

### 小结
- 刷新全部可见的item，notifyDataSetChanged()
- 刷新指定item，notifyItemChanged(int)
- 从指定位置开始刷新指定个item，notifyItemRangeChanged(int,int)
- 插入/移动一个并自动刷新，notifyItemInserted(int)、notifyItemMoved(int)、notifyItemRemoved(int)
- 局部刷新，notifyItemChanged(int, Object)


### Activity

```java
public class Notify_Activity extends Activity implements MyOnItemClickLitener {
    private RecyclerView mRecyclerView;
    private Notify_Adapter mAdapter;
    private ArrayList<PicUrls.BasicPicBean> beans;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ((SwipeRefreshLayout) findViewById(R.id.swipeLayout)).setEnabled(false);
        mRecyclerView = (RecyclerView) findViewById(R.id.rv);
        initList();
        initView();
    }

    protected void initView() {
        mAdapter = new Notify_Adapter(this, beans);
        mAdapter.setOnItemClickLitener(this);
        mRecyclerView.setAdapter(mAdapter);//设置adapter
        mRecyclerView.setLayoutManager(new GridLayoutManager(this, 3));//设置布局管理器
        mRecyclerView.setItemAnimator(new DefaultItemAnimator());//设置Item增加、移除动画
        mRecyclerView.addItemDecoration(new GridItemDecoration.Builder().spanCount(3)
                .spaceSize(1).mDivider(new ColorDrawable(0x88ff0000)).build());
    }
    private void initList() {
        beans = PicUrls.getPicList(PicUrls.BIG_BEANS_2);
        beans.get(0).name = "刷新当前，notifyItemChanged(int)";
        beans.get(1).name = "全部刷新，notifyDataSetChanged()";
        beans.get(2).name = "从此位置开始刷新2个，notifyItemRangeChanged";
        beans.get(3).name = "插入一个并自动刷新，notifyItemInserted";
        beans.get(4).name = "只更改数据源，这样当然不会刷新UI";
        beans.get(5).name = "插入一个并刷新当前，notifyItemChanged";
        beans.get(6).name = "局部刷新，tv";
        beans.get(7).name = "局部刷新，et";
        beans.get(8).name = "局部刷新，iv";
    }
    @Override
    public void onItemClick(View view, int position) {
        Toast.makeText(this, position + " 被点击了", Toast.LENGTH_SHORT).show();
        reInit(position);
    }

    @Override
    public void onItemLongClick(View view, int position) {
        Toast.makeText(this, position + "被长按了", Toast.LENGTH_SHORT).show();
    }
    private void reInit(int position) {
        switch (position) {
            default:
                mAdapter.notifyItemChanged(position);//刷新指定一个。一定会闪
                break;
            case 1:
                mAdapter.notifyDataSetChanged();//全部刷新。基本不会闪，刚开始个别可能会闪
                break;
            case 2:
                mAdapter.notifyItemRangeChanged(position, 2);//从指定位置开始刷新指定个。一定会闪
                break;
            case 3:
                beans.add(position, new PicUrls.BasicPicBean("http://img.mmjpg.com/2015/74/1.jpg", "新插入的图片1", 1));
                mAdapter.notifyItemInserted(position);//插入一个并刷新，正常
                break;
            case 4://只更改数据源，这样当然不会刷新UI
                beans.add(position, new PicUrls.BasicPicBean("http://img.mmjpg.com/2015/74/2.jpg", "新插入的图片2", 2));
                break;
            case 5://
                beans.add(position, new PicUrls.BasicPicBean("http://img.mmjpg.com/2015/74/3.jpg", "新插入的图片3", 3));
                mAdapter.notifyItemChanged(position);//这样只会导致当前item刷新，而不会刷新其他item，当然是不行的
                break;
            case 6:
                beans.set(position, beans.get(new Random().nextInt(beans.size())));
                mAdapter.notifyItemChanged(position, Notify_Adapter.NOTIFY_TV);//局部刷新
                break;
            case 7:
                beans.set(position, beans.get(new Random().nextInt(beans.size())));
                mAdapter.notifyItemChanged(position, Notify_Adapter.NOTIFY_ET);//局部刷新
                break;
            case 8:
                beans.set(position, beans.get(new Random().nextInt(beans.size())));
                mAdapter.notifyItemChanged(position, Notify_Adapter.NOTIFY_IV);//局部刷新
                break;
        }
    }
}
```

### Adapter + ViewHolder

```java
public class Notify_Adapter extends RecyclerView.Adapter<Notify_Adapter.MyViewHolder> {
    private Context context;
    private List<PicUrls.BasicPicBean> mDatas;
    private MyOnItemClickLitener mOnItemClickLitener;
    public static final int NOTIFY_TV = 10086;
    public static final int NOTIFY_ET = 10087;
    public static final int NOTIFY_IV = 10088;
    public Notify_Adapter(Context context, List<PicUrls.BasicPicBean> mDatas) {
        this.context = context;
        this.mDatas = mDatas;
    }
    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        return new MyViewHolder(LayoutInflater.from(context).inflate(R.layout.item_notify, parent, false));
    }
    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        //不使用
    }
    @Override
    public void onBindViewHolder(final MyViewHolder holder, int position, List payloads) {
        //payloads是从notifyItemChanged(int, Object)中，或从notifyItemRangeChanged(int, int, Object)中传进来的Object集合
        //如果payloads不为空并且viewHolder已经绑定了旧数据了，那么adapter会使用payloads参数进行布局刷新
        //如果payloads为空，adapter就会重新绑定数据，也就是刷新整个item
        PicUrls.BasicPicBean bean = mDatas.get(holder.getAdapterPosition());
        long time = System.currentTimeMillis() + bean.url.hashCode();
        String data = new SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(new Date(time));
        if (payloads.isEmpty()) {//为空，即不是调用notifyItemChanged(position,payloads)后执行的，也即在初始化时执行的
            holder.tv.setText(data);
            holder.et.setText(bean.name);
            Glide.with(context).load(bean.url)
                    .dontAnimate()
                    //.diskCacheStrategy(DiskCacheStrategy.NONE).skipMemoryCache(true)
                    .into(holder.iv);
        } else if (payloads.size() > 0 && payloads.get(0) instanceof Integer) {
            //不为空，即调用notifyItemChanged(position,payloads)后执行的，可以在这里获取payloads中的数据进行局部刷新
            int type = (int) payloads.get(0);// 刷新哪个部分 标志位
            switch (type) {
                case NOTIFY_TV:
                    holder.tv.setText(data);//只刷新tv
                    break;
                case NOTIFY_ET:
                    holder.et.setText(bean.name);//只刷新et
                    break;
                case NOTIFY_IV:
                    Glide.with(context).load(bean.url).dontAnimate().into(holder.iv);//只刷新iv
                    break;
            }
        }
        // 如果设置了回调，则设置点击事件
        holder.itemView.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mOnItemClickLitener != null) mOnItemClickLitener.onItemClick(holder.itemView, holder.getAdapterPosition());
            }
        });
        holder.itemView.setOnLongClickListener(new OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                if (mOnItemClickLitener != null) mOnItemClickLitener.onItemLongClick(holder.itemView, holder.getAdapterPosition());
                return false;
            }
        });
    }
    @Override
    public int getItemCount() {
        return mDatas.size();
    }
    /**
     * 添加并更新数据，同时具有动画效果
     */
    public void addDataAt(int position, PicUrls.BasicPicBean data) {
        mDatas.add(position, data);
        notifyItemInserted(position);//更新数据集，注意如果用adapter.notifyDataSetChanged()将没有动画效果
    }
    /**
     * 移除并更新数据，同时具有动画效果
     */
    public void removeDataAt(int position) {
        mDatas.remove(position);
        notifyItemRemoved(position);
    }
    public void setOnItemClickLitener(MyOnItemClickLitener mOnItemClickLitener) {
        this.mOnItemClickLitener = mOnItemClickLitener;
    }

    
    class MyViewHolder extends RecyclerView.ViewHolder {
        TextView tv;
        ImageView iv;
        EditText et;
        public MyViewHolder(View view) {
            super(view);
            tv = (TextView) view.findViewById(R.id.tv_name);
            iv = (ImageView) view.findViewById(R.id.iv_head);
            et = (EditText) view.findViewById(R.id.et_input);
        }
    }
}
```

### Layout

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
              android:layout_width="match_parent"
              android:layout_height="wrap_content"
              android:gravity="center_horizontal"
              android:orientation="vertical">
    <TextView
        android:id="@+id/tv_name"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="0.00"
        android:textColor="#00f"
        android:textSize="13sp"/>
    <ImageView
        android:id="@+id/iv_head"
        android:layout_width="match_parent"
        android:layout_height="200dp"
        android:scaleType="centerCrop"
        android:src="@mipmap/ic_launcher"/>
    <EditText
        android:id="@+id/et_input"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:hint="包青天"
        android:inputType="numberDecimal"
        android:labelFor="@id/et_input"
        android:maxLines="1"
        android:minWidth="50dp"
        android:textColor="#f00"
        android:textSize="10sp"/>
</LinearLayout>
```

### 获取图片集合

```java
public class PicUrls {
    private static final String HOST0 = "http://img1.mm131.com/pic/";//网站【http://www.mm131.com/】
    private static final String HOST1 = "http://img.mmjpg.com/";//网站【http://www.mmjpg.com/】
    private static final String HOST2 = "http://pic.meituba.com/uploads/allimg/";//网站【http://www.meituba.com/】
    public static final UrlBean BIG_BEANS_0 = new UrlBean.Builder()//http://pic.meituba.com/uploads/allimg/2015/10/23/220.jpg
            .host(HOST2).urlHeader("2015/10/23/").picIndexFrom(220).picCount(100).picDes("100张动漫卡通壁纸").build();
    public static final UrlBean BIG_BEANS_1 = new UrlBean.Builder()//http://pic.meituba.com/uploads/allimg/2017/03/27/121_5600.jpg
            .host(HOST2).urlHeader("2017/03/27/121_").picIndexFrom(5600).picCount(100).picDes("100张搞笑内涵图片").build();
    public static final UrlBean BIG_BEANS_2 = new UrlBean.Builder()//http://pic.meituba.com/uploads/allimg/2015/10/23/360.jpg
            .host(HOST2).urlHeader("2015/10/23/").picIndexFrom(360).picCount(750).picDes("750张性感美女图").build();
    public static final UrlBean BIG_BEANS_3 = new UrlBean.Builder()//http://pic.meituba.com/uploads/allimg/2016/03/25/43_20335.jpg
            .host(HOST2).urlHeader("2016/03/25/43_").picIndexFrom(20335).picCount(1400).picDes("1400张动漫卡通壁纸").build();
    private static final UrlBean[] simpleBeans = {
            //http://img1.mm131.com/pic/996/1.jpg
            new UrlBean.Builder().host(HOST0).urlHeader("996/").picCount(10).picDes("北影校花余雨高清写真图片").build(),
            new UrlBean.Builder().host(HOST0).urlHeader("2958/").picCount(10).picDes("童颜嫩妹桃子黑丝大尺度诱惑").build(),
            new UrlBean.Builder().host(HOST0).urlHeader("2939/").picCount(10).picDes("清纯少女刘奕宁酥胸覆白色内衣").build(),
            new UrlBean.Builder().host(HOST0).urlHeader("2343/").picCount(10).picDes("萌妹销魂写真身材惹火让人欲罢不能").build(),
            new UrlBean.Builder().host(HOST0).urlHeader("2935/").picCount(10).picDes("性感女神杨晨晨透视睡衣大胆秀乳").build(),
            //http://img.mmjpg.com/2015/444/1.jpg
            new UrlBean.Builder().host(HOST1).urlHeader("2015/444/").picCount(10).picDes("模范学院美少女柳侑绮制服大片").build(),
            new UrlBean.Builder().host(HOST1).urlHeader("2015/74/").picCount(10).picDes("极品女神可儿私拍秀完美身材").build(),
            new UrlBean.Builder().host(HOST1).urlHeader("2017/990/").picCount(10).picDes("香艳妹子雪白的美胸绝对让你大饱眼福").build(),
            new UrlBean.Builder().host(HOST1).urlHeader("2017/962/").picCount(10).picDes("真诱人啊!女神雪白的美胸看着很有感觉").build(),
            new UrlBean.Builder().host(HOST1).urlHeader("2017/936/").picCount(10).picDes("身材娇美纯天然美女小叶子美胸艺术照").build(),
            //http://pic.meituba.com/uploads/allimg/2015/10/23/247.jpg
            new UrlBean.Builder().host(HOST2).urlHeader("2015/10/23/").picIndexFrom(247).picCount(10).picDes("呆萌可爱的哆啦A梦动漫").build(),
            new UrlBean.Builder().host(HOST2).urlHeader("2016/03/25/43_").picIndexFrom(20574).picCount(10).picDes("海贼王红发香克斯").build(),
            // ...
```