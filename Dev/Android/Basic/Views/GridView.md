## GridView 用法

### I. GridView 实例

#### 1. Activity
```java
public class MainActivity extends Activity {
    private GridView gridView;
    private List<Map<String, Object>> dataList;
    private SimpleAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        gridView = (GridView) findViewById(R.id.gridview);
        //初始化数据
        initData();

        String[] from={"img","text"}; // 与 Item layout 对应

        int[] to={R.id.img,R.id.text};

        adapter=new SimpleAdapter(this, dataList, R.layout.gridview_item, from, to);

        gridView.setAdapter(adapter);

        gridView.setOnItemClickListener(new OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2,
                    long arg3) {
            AlertDialog.Builder builder= new AlertDialog.Builder(MainActivity.this);
            builder.setTitle("提示")
            .setMessage(dataList.get(arg2).get("text").toString()).create().show();
            }
        });
    }

    void initData() {
        //图标
        int icon[] = { R.drawable.i1, R.drawable.i2, R.drawable.i3,
                R.drawable.i4, R.drawable.i5, R.drawable.i6, R.drawable.i7,
                R.drawable.i8, R.drawable.i9, R.drawable.i10, 
                R.drawable.i11, R.drawable.i12 };
        //图标下的文字
        String name[]={"时钟","信号","宝箱","秒钟","大象","FF","记事本","书签",
        "印象","商店","主题","迅雷"};
        dataList = new ArrayList<Map<String, Object>>();
        for (int i = 0; i <icon.length; i++) {
            Map<String, Object> map=new HashMap<String, Object>();
            map.put("img", icon[i]);
            map.put("text",name[i]);
            dataList.add(map);
        }
    }

}
```

#### 2. Layout

##### 2.1 Container Layout
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#000"
    tools:context="com.example.l7.MainActivity" >
    <GridView
        android:id="@+id/gridview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:columnWidth="80dp"
        android:stretchMode="spacingWidthUniform"
        android:numColumns="3" 
         />
</LinearLayout>
```

##### 2.2 Item Layout
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_gravity="center"
    android:orientation="vertical" >

    <ImageView
        android:id="@+id/img"
        android:layout_width="60dp"
        android:layout_height="60dp"
        android:layout_marginTop="10dp" 
        android:src="@drawable/ic_launcher" />
    <TextView
        android:id="@+id/text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="2dp" 
        android:layout_gravity="center"
        android:textColor="#FFF"
        android:text="文字"
        />

</LinearLayout>
```

#### 样式控制 stretchMode

stretchMode 可选值：   
   - columnWidth 如果列有空闲空间就加宽列   
   - spacingWidth 如果列有空闲空间就加宽各列间距    
   - none 没有任何动作    
   - spacingWidthUniform 平均分配空间   
 
![spacingWidthUniform](https://img-blog.csdn.net/20170427212139809?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvc2luYXRfMjU5MjY0ODE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

### II 分割线

1. 通过前后背景颜色差设置  
    - 设置 GridView 背景色
    - 设置水平和垂直方向上的间隔： `android:horizontalSpacing`  `android:verticalSpacing`
    - 设置 GridView item 背景色 和 选择后的背景色
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <selector xmlns:android="http://schemas.android.com/apk/res/android">
        <item android:state_selected="true" >
            <shape android:shape="rectangle">  
                 <solid android:color="#CCCCCC" />
            </shape>
        </item>
        <item android:state_pressed="true" >
            <shape android:shape="rectangle">  
                 <solid android:color="#CCCCCC" />
            </shape>
        </item>
        <item>
            <shape android:shape="rectangle">  
                <solid android:color="#FFFFFF" /> 
            </shape>
        </item>  
    </selector>
    ```
2. 设置选择器
    - 
    ```xml
    <?xml version="1.0" encoding="utf-8"?>
    <selector xmlns:android="http://schemas.android.com/apk/res/android">
        <item android:state_selected="true" >
            <shape android:shape="rectangle">  
                 <solid android:color="#CCCCCC"/>
                 <stroke android:width="1.0px" android:color="#999999" />
            </shape>
        </item>
        <item android:state_pressed="true" >
            <shape android:shape="rectangle">  
                 <solid android:color="#CCCCCC"/>
                 <stroke android:width="1.0px" android:color="#999999" />
            </shape>
        </item>
        <item>
            <shape android:shape="rectangle">  
                <stroke android:width="1.0px" android:color="#999999" />  
            </shape>
        </item>  
    </selector>
    ```
    - 采用此方法会出现中间的线条别边缘的线条粗。究其原因在于，中间的部分是两个 GridView Item 的线条重合的部分。
    - 虽然操作简单，但存在 bug 故不推荐使用。
3. 重写 GridView
    > https://blog.csdn.net/u011803341/article/details/52789469
    > https://blog.csdn.net/qq_17681243/article/details/49360795

    -  (1) 自定义 LineGridView 继承 GridView 重写 onDraw()
    ```java  
    public class LineGridView extends GridView {
            //定义行数
            private int rownum;  
            
            //实现构造方法
            public LineGridView(Context context) {
                super(context);
                // TODO Auto-generated constructor stub
            }
            
            public LineGridView(Context context, AttributeSet attrs) {
                super(context, attrs);
            }
            
            public LineGridView(Context context, AttributeSet attrs, int defStyle) {
                super(context, attrs, defStyle);
            }
            
            ....
   
            @Override
            protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                int colnum = getNumColumns(); //获取列数
                int total = getChildCount();  //获取Item总数
                 //计算行数
                if (total % colnum == 0) {
                    rownum = total / colnum;
                } else {
                    rownum = (total / colnum) + 1; //当余数不为0时，要把结果加上1
                }
                Paint localPaint; //设置画笔
                localPaint = new Paint();
                localPaint.setStyle(Paint.Style.STROKE); //画笔实心      
                localPaint.setColor(getContext().getResources().getColor(R.color.grid_line));//画笔颜色
                View view0 = getChildAt(0); //第一个view
                View viewColLast = getChildAt(colnum - 1);//第一行最后一个view
                View viewRowLast = getChildAt((rownum - 1) * colnum); //第一列最后一个view
                for (int i = 1, c = 1; i < rownum || c < colnum; i++, c++) {
                    //画横线 
                    canvas.drawLine(view0.getLeft(), view0.getBottom() * i, viewColLast.getRight(), viewColLast.getBottom() * i, localPaint);
                    //画竖线
                    canvas.drawLine(view0.getRight() * c, view0.getTop(), viewRowLast.getRight() * c, viewRowLast.getBottom(), localPaint);
                }
            }
    }        
    ```
    - (2) 自定义 LineGridView 重写 dispatchDraw()
    ```java
    public class LineGridView extends GridView {
        public LineGridView(Context context) {
            super(context);
        }

        public LineGridView(Context context, AttributeSet attrs) {
            super(context, attrs);
        }

        public LineGridView(Context context, AttributeSet attrs, int defStyle) {
            super(context, attrs, defStyle);
        }

        @Override
        public void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
            int expandSpec = MeasureSpec.makeMeasureSpec(Integer.MAX_VALUE >> 2, MeasureSpec.AT_MOST);
            super.onMeasure(widthMeasureSpec, expandSpec);
        }

        @Override
        protected void dispatchDraw(Canvas canvas) {
            super.dispatchDraw(canvas);
            View localView1 = getChildAt(0);
            int column = getWidth() / localView1.getWidth();//列数
            int childCount = getChildCount();
            Paint localPaint;
            localPaint = new Paint();
            localPaint.setStyle(Paint.Style.STROKE);
            localPaint.setColor(getContext().getResources().getColor(R.color.ddcx_color_grey2));//这个就是设置分割线的颜色
            for (int i = 0; i < childCount; i++) {
                View cellView = getChildAt(i);
                if ((i + 1) % column == 0) {//每一行最后一个
                    canvas.drawLine(cellView.getLeft(), cellView.getBottom(), cellView.getRight(), cellView.getBottom(), localPaint);
                } else if ((i + 1) > (childCount - (childCount % column))) {//最后一行的item
                    canvas.drawLine(cellView.getRight(), cellView.getTop(), cellView.getRight(), cellView.getBottom(), localPaint);
                } else {
                    canvas.drawLine(cellView.getRight(), cellView.getTop(), cellView.getRight(), cellView.getBottom(), localPaint);
                    canvas.drawLine(cellView.getLeft(), cellView.getBottom(), cellView.getRight(), cellView.getBottom(), localPaint);
                }
            }
        }
    }
    ```
    -  像使用 GridView 一样使用 LineGridView

    ![效果图1](https://img-blog.csdn.net/20151023143706216?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)
    
    ![效果图2](https://img-blog.csdn.net/20161011164644977)
    
    



