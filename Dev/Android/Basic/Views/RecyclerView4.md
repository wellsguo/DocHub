## RecyclerView (四) 网格分隔线

### 1. 垂直列表与网格布局间隔线原理图对比

#### 1.1. 垂直列表间隔线

![](https://img-blog.csdn.net/20180507215338743)

我们简单回顾一下，Rect 是为列表项之间分配了一个矩形空间，绘制分割线就是在这个空间里绘制的。这个 RECT 的坐标系原点为 item 列表项的左下角。然后分别向右拉伸和向下偏移一个高度而形成一个矩形空间。这个 **RECT** 空间是通过 `ItemDecoration` 列表项装饰类的 `getItemsOffsets` 来分配的。


#### 1.2. 网格布局的间隔线的 Rect 空间

![](https://img-blog.csdn.net/20180508215746326)

如上图所示，网格布局与垂直列表间隔线唯一的区别是，每一个ITEM有2个间隔线，一个是竖直方向；另一个是水平方向。这意味着getItemsOffsets函数对每一个ITEM都同时分配了2个RECT矩形空间供 onDraw函数绘制间隔线。

### 2. 代码

#### 2.1. ItemDecoration的实现


```java
public class DividerGridViewItemDecoration extends ItemDecoration {

    private Drawable mDivider;
    private int[] attrs= new int[]{
        android.R.attr.listDivider
    };

    public DividerGridViewItemDecoration(Context context) {
        TypedArray typedArray = context.obtainStyledAttributes(attrs);
        mDivider = typedArray.getDrawable(0);
        typedArray.recycle();
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, State state) {
        drawVertical(c,parent);
        drawHorizontal(c,parent);
    }

    /**
     * 绘制grid网格列表 水平间隔线
     * @param c
     * @param parent
     */
    private void drawHorizontal(Canvas c, RecyclerView parent) {
        int childCount = parent.getChildCount();

        for (int i = 0; i < childCount; i++) {
            View child = parent.getChildAt(i);

            /**
             * 水平间隔线看做一个矩形
             * (1)上边界为当前item的最底边缘 + item的marginBottom（与周围的空白间隔）即上边界比ITEM的底部Y坐标再往下偏移
             * (2)下边界，显然就是上边界 + 线的高度
             * (3)左边界为当前item的最左边缘 -  item的marginLeft（与周围的空白间隔）,即左边界比ITEM的左边缘X坐标再往左偏移。
             * (4)右边界为当前item的最右边缘 +  item的marginRight（与周围的空白间隔）,即右边界比ITEM的右边缘X坐标再往右偏移
             */
            RecyclerView.LayoutParams params = (LayoutParams) child.getLayoutParams();
            int left = child.getLeft() - params.leftMargin;
            int right = child.getRight()+ params.rightMargin;
            int top = child.getBottom() + params.bottomMargin;
            int bottom = top + mDivider.getIntrinsicHeight();
            mDivider.setBounds(left, top, right, bottom);
            mDivider.draw(c);
        }
    }

    @Override
    @Deprecated
    public void getItemOffsets(Rect outRect, int itemPosition,  RecyclerView parent) {
        /**
         * 以下代码同时定义了itemPosition这个条目上的2个RECT间隔空间：
         * （1）竖直分割线：0,0以网格方块的右边缘最上端为原点，bottom可以任意给值，即使是0也会拉伸RECT空间的高为方块的高，
         *   right则是rect的宽，即将来 间隔线能绘制的 最粗值，在此恰好定义竖直RECT空间的宽度恰好为线的宽度。
         *
         * （2）水平分割线：RECT空间的左、上、右、下和上一篇垂直列表 的 水平分割线一样，0,0是方块的左下角，right可以给任意值，
         *   即使是0也会拉伸RECT空间的宽为方块的宽度，bottom则是rect的高，即将来 水平间隔线能绘制的 最粗值，
         *   在此恰好定义为线的高度。
         *
         * 总之，right 定义了竖直间隔线，bottom定义了水平间隔线
         */
        int right = mDivider.getIntrinsicWidth();
        int bottom = mDivider.getIntrinsicHeight();
        outRect.set(0, 0, right, bottom);
    }

}
```

#### 2.2. 布局文件

```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
     >

    <android.support.v7.widget.RecyclerView
        android:layout_margin="50dp"
        android:id="@+id/recylerview"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        />
</RelativeLayout>
```

#### 3. MainActivity

```java
public class MainActivity extends Activity {

    private RecyclerView recylerview;  //RecyclerView控件实例对象
    private ArrayList<String> list = new ArrayList<>();    //RecyclerView要显示的 列表数据，在此为一组字符串。
    private MyRecyclerAdapter adapter; //同ListView一样，需要一个适配器来 将list数据 装载到 RecyclerView列表控件。
    //private MyStaggedRecyclerAdapter adapter;  //列表显示风格  为瀑布流 界面样式 的 适配器。
    boolean isGrid = true;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        // initData();
    }

    public void initView(){

        for (int i = 0; i < 6; i++) {
            list.add("item"+i);
        }

        //实例化布局中的recylerview控件
        recylerview = (RecyclerView)findViewById(R.id.recylerview);

        //普通列表的适配器
        adapter = new MyRecyclerAdapter(list);

        //显示风格为网格，3列
        recylerview.setLayoutManager(new GridLayoutManager(this, 3));

        //装载显示列表数据
        recylerview.setAdapter(adapter);

        recylerview.addItemDecoration(new DividerGridViewItemDecoration(this));

        recylerview.setItemAnimator(new DefaultItemAnimator());

        adapter.setOnItemClickListener(new OnItemClickListener(){
            @Override
            public void onItemClick(View view, int position) {
                Toast.makeText(MainActivity.this, "点了"+position, Toast.LENGTH_SHORT).show();
            }
        });

        return;
    }
}
```

### 至此运行效果图

![](https://img-blog.csdn.net/20180507230032779)

基本上绘制完成了，只是最右列的间隔线与最后一行的水平间隔线多余了，具体如何取消最后一列与最后一行的间隔线

### 最终效果

![](https://img-blog.csdn.net/20180507230344902)

