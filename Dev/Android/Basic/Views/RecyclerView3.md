## RecyclerView (三) 分隔线

RecyclerView 列表项之间默认是没有分隔线的，原先旧的列表控件（Listview）的各列表项之间默认是有分割线的。该如何为 `RecyclerView` 列表添加**自定义分割线**？

![](https://img-blog.csdn.net/20180501191310430)  

为 RecyclerView 自定义分割线需要用到一个类 `ItemDecoration` 列表项装饰类，我们就是通过继承这个类来为 RecyclerView 列表的 ITEM 定义间隔线的。

### ItemDecoration 应用

```java
for (int i = 0; i < 10; i++) {
   list.add("item"+i);
}

//实例化布局中的recylerview控件
recylerview = (RecyclerView)findViewById(R.id.recylerview);
recylerview.addItemDecoration(new MyItemDecoration(this, LinearLayout.VERTICAL));

//普通列表的适配器
adapter = new MyRecyclerAdapter(list);

//列表显示风格为 垂直方向的列表
recylerview.setLayoutManager(new LinearLayoutManager(this));

//装载显示列表数据
recylerview.setAdapter(adapter);
```

以上代码片段声明了一个RecyclerView控件并且设置了一个adapter,列表要显示的数据在list里。我们主要看这一句 `recylerview.addItemDecoration(new MyItemDecoration(this);` 这个就是为 RecyclerView 列表控件的 ITEM 列表项添加了一个自定义装饰，其中 `DividerItemDecoration` 是我们自定义的类继承于系统类ItemDecoration，也就是说我们将通过重新定义 ItemDecoration 类来自绘制列表项的间隔线。好，下来我们就来看看这个 MyItemDecoration 类里都干了什么？

### ItemDecoration 实现

```java
public class MyItemDecoration extends ItemDecoration {
    @Override
    public void onDraw(Canvas c, RecyclerView parent, State state) {
        super.onDraw(c, parent, state);
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, State state) {
    }
}
```
在这里我们重写父类的 onDraw 和 getItemOffsets 方法。这两个方法有何用:  

#### 1.getItemOffsets()  

> 边界线的限定区域 (Rect)
 
```java
int left = 0;
int top = 0;
int right = 0;
int bottom = mDivider.getIntrinsicHeight();

outRect.set(left, top, right, bottom);
```

在此假设列表是垂直列表，那么我们应该画的间隔线是水平的，因此矩形的4个边界分别是：  
- 左边界: x 坐标为 0（相对于 ITEM 左边的水平位移）
- 顶边界: y 坐标为 0（相对于 item 底部的垂直偏移量）
- 右边界: x 坐标仍为 0，这里本应是 ITEM 的宽度，但是 RECT 区域会随着 ITEM 的宽度而拉伸，因此这里的大小无关紧要，不管赋值为什么值，最终还是 ITEM 的宽度。
- 下边界: y 坐标为分割线 mDivider 的高度。（我们恰好能给分割线留够相应的空间即可）。

#### 2.onDraw()

> 在 RECT 中绘制自定义的分割线

```java
//线的 x 起点坐标
int left = parent.getPaddingLeft();
//线的终点 x 坐标
int right = parent.getWidth() - parent.getPaddingRight();
int childCount = parent.getChildCount();
for (int i = 0; i < childCount ; i++) {
    View child = parent.getChildAt(i);
    LayoutParams params = (LayoutParams) child.getLayoutParams();
    //线的 y 方向的起点坐标
    // params.bottomMargin 考虑了下边距
    // ViewCompat.getTranslationY(child) 考虑 Y 方向的阴影
    int top = child.getBottom() + params.bottomMargin + Math.round(ViewCompat.getTranslationY(child));
    //线的 y 方向的终点坐标
    int bottom = top + mDivider.getIntrinsicHeight();
    mDivider.setBounds(left, top , right, bottom);
    mDivider.draw(c);
}
```

### 完整代码

```java
public class MyItemDecorationextends ItemDecoration {

    private Drawable mDivider;
    private int[] attrs= new int[]{
        android.R.attr.listDivider
    };

    public MyItemDecoration(Context context) {
        TypedArray typedArray = context.obtainStyledAttributes(attrs);
        mDivider = typedArray.getDrawable(0);
        typedArray.recycle();
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, State state) {
        // 画水平线
        int left = parent.getPaddingLeft();
        int right = parent.getWidth() - parent.getPaddingRight();
        int childCount = parent.getChildCount();
        for (int i = 0; i < childCount ; i++) {
            View child = parent.getChildAt(i);
            
            LayoutParams params = (LayoutParams) child.getLayoutParams();
            int top = child.getBottom() + params.bottomMargin + Math.round(ViewCompat.getTranslationY(child));
            int bottom = top + mDivider.getIntrinsicHeight();
            mDivider.setBounds(left, top , right, bottom);
            mDivider.draw(c);
        }
        super.onDraw(c, parent, state); 
    } 

    @Override 
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, State state) {
        outRect.set(0, 0, 0, mDivider.getIntrinsicHeight()); 
    }
}
```

