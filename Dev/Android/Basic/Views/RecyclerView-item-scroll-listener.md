## [RecyclerView 横向滑动监听，判断是否滑动到了最后一个 Item](https://www.jianshu.com/p/5eb2de368ea0  )


项目中的需求，RecyclerView 横向滑动列表，要有加载更多的功能，给 RecyclerView 设置一个滑动监听，在 onScrolled 方法中判断一下滑动方向，然后在 onScrollStateChanged 方法中判断一下是否滑动到了最后一个 item 即可，代码中已经写了详细的注释：


```java
public abstract class EndlessRecyclerOnScrollListener extends RecyclerView.OnScrollListener {

    // 用来标记是否正在向左滑动
    private boolean isSlidingToLeft = false;

    @Override
    public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
        super.onScrollStateChanged(recyclerView, newState);
        LinearLayoutManager manager = (LinearLayoutManager) recyclerView.getLayoutManager();
        // 当不滑动时
        if (newState == RecyclerView.SCROLL_STATE_IDLE) {
            // 获取最后一个完全显示的itemPosition
            int lastItemPosition = manager.findLastCompletelyVisibleItemPosition();
            int itemCount = manager.getItemCount();

            // 判断是否滑动到了最后一个item，并且是向左滑动
            if (lastItemPosition == (itemCount - 1) && isSlidingToLeft) {
                // 加载更多
                onLoadMore();
            }
        }
    }

    @Override
    public void onScrolled(RecyclerView recyclerView, int dx, int dy) {
        super.onScrolled(recyclerView, dx, dy);
        // dx值大于0表示正在向左滑动，小于或等于0表示向右滑动或停止
        isSlidingToLeft = dx > 0;
    }

    /**
     * 加载更多回调
     */
    public abstract void onLoadMore();
}
```
看下如何使用：

```java
// 设置加载更多监听
recyclerView.addOnScrollListener(new EndlessRecyclerOnScrollListener() {
    @Override
    public void onLoadMore() {
        // 加载更多
    }
});
```
  



## [Recycleview 中让指定 item 在屏幕可视区域内](https://blog.csdn.net/weixin_33785972/article/details/87530931)

类似与歌词滚动 当用户拖动recycle后，在下一句时让当前句重新回到视野

```java
int currItem = 0;
int lastVisibleItem = 0;
boolean isScroll = false;

recycleView.addOnScrollListener(new RecyclerView.OnScrollListener() {
    @Override
    public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
        super.onScrollStateChanged(recyclerView, newState);
        LinearLayoutManager manager = (LinearLayoutManager) recyclerView.getLayoutManager();
        // 当不滚动时
        if (newState == RecyclerView.SCROLL_STATE_IDLE) {
            //获取最后一个完全显示的 ItemPosition
            lastVisibleItem = manager.findLastCompletelyVisibleItemPosition();
            isScroll = true;
        }
    }

    if(isScroll && Math.abs(lastVisibleItem - currItem)>4){
        recycleView.smoothScrollToPosition(currItem);
        isScroll = false;
    } else {
        if(currItem+2 < adapter.getItemCount()){
            recycleView.smoothScrollToPosition(currItem + 2);
        } else {
            recycleView.smoothScrollToPosition(currItem + 1);
        }
    }
}
```

## [Recycleview 获取第一个和最后一个可见 item 的位置](https://blog.csdn.net/suyimin2010/article/details/84501155)  

只有LinearLayoutManager才有查找第一个和最后一个可见view位置的方法

```java
FoodsNameRecycle.setOnScrollListener(new RecyclerView.OnScrollListener() {
    @Override
    public void onScrolled(RecyclerView recyclerView, int dx, int dy) {
        super.onScrolled(recyclerView, dx, dy);
    }
 
    @Override
    public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
        super.onScrollStateChanged(recyclerView, newState);
        RecyclerView.LayoutManager layoutManager = recyclerView.getLayoutManager();
        //判断是当前layoutManager是否为LinearLayoutManager
        // 只有LinearLayoutManager才有查找第一个和最后一个可见view位置的方法
        if (layoutManager instanceof LinearLayoutManager) {
            LinearLayoutManager linearManager = (LinearLayoutManager) layoutManager;
            //获取最后一个可见view的位置
            int lastItemPosition = linearManager.findLastVisibleItemPosition();
            //获取第一个可见view的位置
            int firstItemPosition = linearManager.findFirstVisibleItemPosition();
            if (foodsArrayList.get(firstItemPosition) instanceof Foods) {
                int foodTypePosion = ((Foods) foodsArrayList.get(firstItemPosition)).getFood_stc_posion();  
                FoodsTypeListview.getChildAt(foodTypePosion)
                    .setBackgroundResource(R.drawable.choose_item_selected);
            }
            System.out.println(lastItemPosition + "   " + firstItemPosition);
        }
    }
});
```

## [RecyclerView:设置指定位置的两种方法](https://blog.csdn.net/fangziyi199110/article/details/73469317)

方法一，直接使用当前的manager

```java
/* RecyclerView 移动到当前位置，
 *
 * @param manager  设置RecyclerView对应的manager
 * @param n  要跳转的位置
 */
public static void MoveToPosition(LinearLayoutManager manager, int n) {
    manager.scrollToPositionWithOffset(n, 0);
    manager.setStackFromEnd(true);
}
```

方法二、根据当前RecyclerView的条目数量，这个相对复杂一些，但是可以有效地避免指针越界呦..

```java
/**
 * RecyclerView 移动到当前位置，
 *
 * @param manager   设置RecyclerView对应的manager
 * @param mRecyclerView  当前的RecyclerView
 * @param n  要跳转的位置
 */
public static void MoveToPosition(LinearLayoutManager manager, RecyclerView mRecyclerView, int n) {
    int firstItem = manager.findFirstVisibleItemPosition();
    int lastItem = manager.findLastVisibleItemPosition();
    if (n <= firstItem) {
        mRecyclerView.scrollToPosition(n);
    } else if (n <= lastItem) {
        int top = mRecyclerView.getChildAt(n - firstItem).getTop();
        mRecyclerView.scrollBy(0, top);
    } else {
        mRecyclerView.scrollToPosition(n);
    }
}
```