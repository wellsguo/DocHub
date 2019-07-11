## RecyclerView (六) 添加头部和尾部

### 一、分析listview源码

#### 1. addHeaderView

**添加头部**

```java
/**
* Add a fixed view to appear at the top of the list. If this method is
* called more than once, the views will appear in the order they were
* added. Views added using this call can take focus if they want.
* <p>
* Note: When first introduced, this method could only be called before
* setting the adapter with {@link #setAdapter(ListAdapter)}. Starting with
* {@link android.os.Build.VERSION_CODES#KITKAT}, this method may be
* called at any time. If the ListView's adapter does not extend
* {@link HeaderViewListAdapter}, it will be wrapped with a supporting
* instance of {@link WrapperListAdapter}.
*
* @param v The view to add.
* @param data Data to associate with this view
* @param isSelectable whether the item is selectable
*/
public void addHeaderView(View v, Object data, boolean isSelectable) {
    if (v.getParent() != null && v.getParent() != this) {
        if (Log.isLoggable(TAG, Log.WARN)) {
            Log.w(TAG, "The specified child already has a parent. "
                        + "You must call removeView() on the child's parent first.");
        }
    }
    final FixedViewInfo info = new FixedViewInfo();
    info.view = v;
    info.data = data;
    info.isSelectable = isSelectable;
    mHeaderViewInfos.add(info);
    mAreAllItemsSelectable &= isSelectable;

    // Wrap the adapter if it wasn't already wrapped.
    if (mAdapter != null) {
        if (!(mAdapter instanceof HeaderViewListAdapter)) {
            wrapHeaderListAdapterInternal();
        }

        // In the case of re-adding a header view, or adding one later on,
        // we need to notify the observer.
        if (mDataSetObserver != null) {
            mDataSetObserver.onChanged();
        }
    }
}
```

```java
protected void wrapHeaderListAdapterInternal() {
    mAdapter = wrapHeaderListAdapterInternal(mHeaderViewInfos, mFooterViewInfos, mAdapter);
}
```

```java
protected HeaderViewListAdapter wrapHeaderListAdapterInternal(
        ArrayList<ListView.FixedViewInfo> headerViewInfos,
        ArrayList<ListView.FixedViewInfo> footerViewInfos,
        ListAdapter adapter) {
    return new HeaderViewListAdapter(headerViewInfos, footerViewInfos, adapter);
}
```

我们来分析以上 listview 中添加头部的 API 源码，主要看红色部分，

- （1）mHeaderViewInfos.add(info)  
意图是在数组 mHeaderViewInfos 里添加头部信息 
  - info 中的 view 就是我们添加的头部布局，
  - info.data 就是为 header 准备数据,
  - info.isSelectable定义头部是否可以选择（一般用于TV上的光标选择）。既然 mHeaderViewInfos 是一个数组，说明 Listview 可以添加多个头部。
  - 总结一下，就是 mHeaderViewInfos 可以添加多个头部 view。
- （2）wrapHeaderListAdapterInternal(...)   
从上述代码中可以看出 该函数最终调用了  
```java
return new HeaderViewListAdapter(headerViewInfos, footerViewInfos, adapter);
```  
  - 也就是说返回了一个全新的 `adapter = HeaderViewListAdapter`, 观察3个构造函数参分别是**头部视图**、**尾部视图**、**普通adapter**.看来这个全新的 adapter 不一般，它可以处理带有头部和尾部视图以及正常条目的 ListView 。
  - 总结一下，就是当 listview 有头部和尾部的时候，会专门为这样的 listview 重新封装一个 HeaderViewListAdapter，这个 HeaderViewListAdapter 会为 listview 显示不同类型的布局，如头部布局、正常条目的布局、尾部布局。

### 2. setAdapter

```java
    /**
     * Sets the data behind this ListView.
     *
     * The adapter passed to this method may be wrapped by a {@link WrapperListAdapter},
     * depending on the ListView features currently in use. For instance, adding
     * headers and/or footers will cause the adapter to be wrapped.
     *
     * @param adapter The ListAdapter which is responsible for maintaining the
     *        data backing this list and for producing a view to represent an
     *        item in that data set.
     *
     * @see #getAdapter()
     */
    @Override
    public void setAdapter(ListAdapter adapter) {
        if (mAdapter != null && mDataSetObserver != null) {
            mAdapter.unregisterDataSetObserver(mDataSetObserver);
        }
 
        resetList();
        mRecycler.clear();
 
        if (mHeaderViewInfos.size() > 0|| mFooterViewInfos.size() > 0) {
            mAdapter = wrapHeaderListAdapterInternal(mHeaderViewInfos, mFooterViewInfos, adapter);
        } else {
            mAdapter = adapter;
        }
 
        mOldSelectedPosition = INVALID_POSITION;
        mOldSelectedRowId = INVALID_ROW_ID;
 
        // AbsListView#setAdapter will update choice mode states.
        super.setAdapter(adapter);
 
        if (mAdapter != null) {
            mAreAllItemsSelectable = mAdapter.areAllItemsEnabled();
            mOldItemCount = mItemCount;
            mItemCount = mAdapter.getCount();
            checkFocus();
 
            mDataSetObserver = new AdapterDataSetObserver();
            mAdapter.registerDataSetObserver(mDataSetObserver);
 
            mRecycler.setViewTypeCount(mAdapter.getViewTypeCount());
 
            int position;
            if (mStackFromBottom) {
                position = lookForSelectablePosition(mItemCount - 1, false);
            } else {
                position = lookForSelectablePosition(0, true);
            }
            setSelectedPositionInt(position);
            setNextSelectedPositionInt(position);
 
            if (mItemCount == 0) {
                // Nothing selected
                checkSelectionChanged();
            }
        } else {
            mAreAllItemsSelectable = true;
            checkFocus();
            // Nothing selected
            checkSelectionChanged();
        }
 
        requestLayout();
    }
```

以上是 Listview 的 setAdapter 函数

```java
if (mHeaderViewInfos.size() > 0|| mFooterViewInfos.size() > 0){//表面当有头部或尾部的时候
   mAdapter = wrapHeaderListAdapterInternal(mHeaderViewInfos, mFooterViewInfos, adapter);
}
```

mAdapter实质被赋值为一个封装过的adapter，与源码片段1一样，封装过的adapter就是HeaderViewListAdapter。

也就是说，我们通常表面上调用的是setAdapter(adapter),实质当我们调用了addHeaderView函数之后，系统会帮我们把正常条目的adapter做了一次全新的封装，封装后的HeaderViewListAdapter有能力去显示头部、尾部，正常条目的。

### 二、模仿（一）中的Listview的源码来扩展RecyclerView（可添加头部与尾部）

#### 1.我们要扩展RecyclerView，那自然先创建一个子类继承RecyclerView

```java
package com.anyikang.volunteer.sos.recyclerview;
 
import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.util.AttributeSet;
import android.view.View;
 
import java.util.ArrayList;
 
public class MyRecyclerView extends RecyclerView{
	private ArrayList<View> mHeaderViewInfos = new ArrayList<View>();
	private ArrayList<View> mFooterViewInfos = new ArrayList<View>();
	private Adapter mAdapter;
 
	public MyRecyclerView(Context context, AttributeSet attrs) {
		super(context, attrs);
	}
	
    public void addHeaderView(View v) {
        mHeaderViewInfos.add(v);
 
        // Wrap the adapter if it wasn't already wrapped.
        if (mAdapter != null) {
            if (!(mAdapter instanceof HeaderViewAdapterForRecycler )) {
                mAdapter = new HeaderViewAdapterForRecycler (mHeaderViewInfos, mFooterViewInfos, mAdapter);
            }
        }
    }
    
    public void addFooterView(View v) {
        mFooterViewInfos.add(v);
 
        // Wrap the adapter if it wasn't already wrapped.
        if (mAdapter != null) {
            if (!(mAdapter instanceof HeaderViewAdapterForRecycler )) {
                mAdapter = new HeaderViewAdapterForRecycler (mHeaderViewInfos, mFooterViewInfos, mAdapter);
            }
        }
    }
	
    @Override
    public void setAdapter(Adapter adapter) {
    	if (mHeaderViewInfos.size() > 0|| mFooterViewInfos.size() > 0) {
            mAdapter = new HeaderViewAdapterForRecycler (mHeaderViewInfos, mFooterViewInfos, adapter);
        } else {
            mAdapter = adapter;
        }
    	super.setAdapter(mAdapter);
    }
 
}
```

是否有种似曾相识的感觉。继承于RecyclerView主要扩展了3个函数：
- addHeaderView增加头部、
- addFooterView增加尾部、
- 重写了setAdapter.
这3个函数都干了同一件事：那就是如果我们添加了头部（尾部），我们的adapter将偷梁换柱成HeaderViewAdapterForRecycler,可显示头、中、尾条目的适配器。现在是时候来分析这个顶梁柱HeaderViewAdapterForRecycler的时候了。

### 三、老套路，先分析Listview中的HeaderViewListAdapter的源码

```java
/*
 * Copyright (C) 2006 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
package android.widget;
 
import android.database.DataSetObserver;
import android.view.View;
import android.view.ViewGroup;
 
import java.util.ArrayList;
 
/**
 * ListAdapter used when a ListView has header views. This ListAdapter
 * wraps another one and also keeps track of the header views and their
 * associated data objects.
 *<p>This is intended as a base class; you will probably not need to
 * use this class directly in your own code.
 */
public class HeaderViewListAdapter implements WrapperListAdapter, Filterable {
 
    private final ListAdapter mAdapter;
 
    // These two ArrayList are assumed to NOT be null.
    // They are indeed created when declared in ListView and then shared.
    ArrayList<ListView.FixedViewInfo> mHeaderViewInfos;
    ArrayList<ListView.FixedViewInfo> mFooterViewInfos;
 
    // Used as a placeholder in case the provided info views are indeed null.
    // Currently only used by some CTS tests, which may be removed.
    static final ArrayList<ListView.FixedViewInfo> EMPTY_INFO_LIST =
        new ArrayList<ListView.FixedViewInfo>();
 
    boolean mAreAllFixedViewsSelectable;
 
    private final boolean mIsFilterable;
 
    public HeaderViewListAdapter(ArrayList<ListView.FixedViewInfo> headerViewInfos,
                                 ArrayList<ListView.FixedViewInfo> footerViewInfos,
                                 ListAdapter adapter) {
        mAdapter = adapter;
        mIsFilterable = adapter instanceof Filterable;
 
        if (headerViewInfos == null) {
            mHeaderViewInfos = EMPTY_INFO_LIST;
        } else {
            mHeaderViewInfos = headerViewInfos;
        }
 
        if (footerViewInfos == null) {
            mFooterViewInfos = EMPTY_INFO_LIST;
        } else {
            mFooterViewInfos = footerViewInfos;
        }
 
        mAreAllFixedViewsSelectable =
                areAllListInfosSelectable(mHeaderViewInfos)
                && areAllListInfosSelectable(mFooterViewInfos);
    }
 
    public int getHeadersCount() {
        return mHeaderViewInfos.size();
    }
 
    public int getFootersCount() {
        return mFooterViewInfos.size();
    }
 
    public boolean isEmpty() {
        return mAdapter == null || mAdapter.isEmpty();
    }
 
    private boolean areAllListInfosSelectable(ArrayList<ListView.FixedViewInfo> infos) {
        if (infos != null) {
            for (ListView.FixedViewInfo info : infos) {
                if (!info.isSelectable) {
                    return false;
                }
            }
        }
        return true;
    }
 
    public boolean removeHeader(View v) {
        for (int i = 0; i < mHeaderViewInfos.size(); i++) {
            ListView.FixedViewInfo info = mHeaderViewInfos.get(i);
            if (info.view == v) {
                mHeaderViewInfos.remove(i);
 
                mAreAllFixedViewsSelectable =
                        areAllListInfosSelectable(mHeaderViewInfos)
                        && areAllListInfosSelectable(mFooterViewInfos);
 
                return true;
            }
        }
 
        return false;
    }
 
    public boolean removeFooter(View v) {
        for (int i = 0; i < mFooterViewInfos.size(); i++) {
            ListView.FixedViewInfo info = mFooterViewInfos.get(i);
            if (info.view == v) {
                mFooterViewInfos.remove(i);
 
                mAreAllFixedViewsSelectable =
                        areAllListInfosSelectable(mHeaderViewInfos)
                        && areAllListInfosSelectable(mFooterViewInfos);
 
                return true;
            }
        }
 
        return false;
    }
 
    public int getCount() {
        if (mAdapter != null) {
            return getFootersCount() + getHeadersCount() + mAdapter.getCount();
        } else {
            return getFootersCount() + getHeadersCount();
        }
    }
 
    public boolean areAllItemsEnabled() {
        if (mAdapter != null) {
            return mAreAllFixedViewsSelectable && mAdapter.areAllItemsEnabled();
        } else {
            return true;
        }
    }
 
    public boolean isEnabled(int position) {
        // Header (negative positions will throw an IndexOutOfBoundsException)
        int numHeaders = getHeadersCount();
        if (position < numHeaders) {
            return mHeaderViewInfos.get(position).isSelectable;
        }
 
        // Adapter
        final int adjPosition = position - numHeaders;
        int adapterCount = 0;
        if (mAdapter != null) {
            adapterCount = mAdapter.getCount();
            if (adjPosition < adapterCount) {
                return mAdapter.isEnabled(adjPosition);
            }
        }
 
        // Footer (off-limits positions will throw an IndexOutOfBoundsException)
        return mFooterViewInfos.get(adjPosition - adapterCount).isSelectable;
    }
 
    public Object getItem(int position) {
        // Header (negative positions will throw an IndexOutOfBoundsException)
        int numHeaders = getHeadersCount();
        if (position < numHeaders) {
            return mHeaderViewInfos.get(position).data;
        }
 
        // Adapter
        final int adjPosition = position - numHeaders;
        int adapterCount = 0;
        if (mAdapter != null) {
            adapterCount = mAdapter.getCount();
            if (adjPosition < adapterCount) {
                return mAdapter.getItem(adjPosition);
            }
        }
 
        // Footer (off-limits positions will throw an IndexOutOfBoundsException)
        return mFooterViewInfos.get(adjPosition - adapterCount).data;
    }
 
    public long getItemId(int position) {
        int numHeaders = getHeadersCount();
        if (mAdapter != null && position >= numHeaders) {
            int adjPosition = position - numHeaders;
            int adapterCount = mAdapter.getCount();
            if (adjPosition < adapterCount) {
                return mAdapter.getItemId(adjPosition);
            }
        }
        return -1;
    }
 
    public boolean hasStableIds() {
        if (mAdapter != null) {
            return mAdapter.hasStableIds();
        }
        return false;
    }
 
    public View getView(int position, View convertView, ViewGroup parent) {
        // Header (negative positions will throw an IndexOutOfBoundsException)
        int numHeaders = getHeadersCount();
        if (position < numHeaders) {
            return mHeaderViewInfos.get(position).view;
        }
 
        // Adapter
        final int adjPosition = position - numHeaders;
        int adapterCount = 0;
        if (mAdapter != null) {
            adapterCount = mAdapter.getCount();
            if (adjPosition < adapterCount) {
                return mAdapter.getView(adjPosition, convertView, parent);
            }
        }
 
        // Footer (off-limits positions will throw an IndexOutOfBoundsException)
        return mFooterViewInfos.get(adjPosition - adapterCount).view;
    }
 
    public int getItemViewType(int position) {
        int numHeaders = getHeadersCount();
        if (mAdapter != null && position >= numHeaders) {
            int adjPosition = position - numHeaders;
            int adapterCount = mAdapter.getCount();
            if (adjPosition < adapterCount) {
                return mAdapter.getItemViewType(adjPosition);
            }
        }
 
        return AdapterView.ITEM_VIEW_TYPE_HEADER_OR_FOOTER;
    }
 
    public int getViewTypeCount() {
        if (mAdapter != null) {
            return mAdapter.getViewTypeCount();
        }
        return 1;
    }
 
    public void registerDataSetObserver(DataSetObserver observer) {
        if (mAdapter != null) {
            mAdapter.registerDataSetObserver(observer);
        }
    }
 
    public void unregisterDataSetObserver(DataSetObserver observer) {
        if (mAdapter != null) {
            mAdapter.unregisterDataSetObserver(observer);
        }
    }
 
    public Filter getFilter() {
        if (mIsFilterable) {
            return ((Filterable) mAdapter).getFilter();
        }
        return null;
    }
    
    public ListAdapter getWrappedAdapter() {
        return mAdapter;
    }
}
```

核心源码分析：

#### 1.HeaderViewListAdapter()

它有3个参数，头、尾、正常条目的mAdapter，这个与我们（一）中分析的一样，也是传递这3个内容。

#### 2.getCount()

这个函数返回真正的条目数：headerCount + footerCount + mAdapter.count

#### 3.getItem(int position)

返回position条目上要显示的数据： 这里有也是3部分，其中第一个if判断该position是否是头部，第二个if判断是否是中间条目，最后是尾部条目，根据不同的情况返回对应的数据

 return mHeaderViewInfos.get(position).data;
 return mAdapter.getItem(adjPosition);//这个是创建普通adapter时，new adapter的时候传递给adapter的数据集合的position索引里的数据、
 return mFooterViewInfos.get(adjPosition - adapterCount).data;//构造函数传递过来的数组

#### ４. getview()

这个函数再熟悉不过了，就是为条目返回要显示的布局VIEW以及可在这个函数里为VIEW中元素赋值，如为条目上的 
Textview 赋值一个字符串文本。在这里也和３中一样返回对应的VIEW（头部VIEW、普通条目VIEW、尾部VIEW）：

return mHeaderViewInfos.get(position).view;

return mAdapter.getView(adjPosition,convertView,parent);

return mFooterViewInfos.get(adjPosition - adapterCount).view;

这里提醒一下，mAdapter就是我们普通条目的MyAdapter，就是我们在不需要添加 头尾部的时候，使用listview显示数据得先创建一个MyAdapter，比如MyAdapter继承BaseAdapter，然后重写getview等方法，我相信你懂我说的。

总结一下，观察以上HeaderViewListAdapter的4个函数我们会发现它们总是离不开mAdapter，也就是说它们总要改造一番：在原mAdapter的基础上都额外涉及到了header和footer，只有这样才能满足listview正常显示头尾部的需求。



### 四、模仿（三）中的HeaderViewListAdapter为RecyclerView自定义适合它的
HeaderViewListAdapter

#### 1.我们要扩展adapter，那自然先创建一个子类HeaderViewAdapterForRecycler继承Adapter,这个HeaderViewAdapterForRecycler就是我们经常提到的全新的adapter.

```java
package com.anyikang.volunteer.sos.recyclerview;
 
import android.support.v7.widget.RecyclerView.Adapter;
import android.support.v7.widget.RecyclerView.ViewHolder;
import android.view.View;
import android.view.ViewGroup;
 
import java.util.ArrayList;
 
public class HeaderViewAdapterForRecycler  extends Adapter {
    private Adapter mAdapter;
 
    ArrayList<View> mHeaderViewInfos;
    ArrayList<View> mFooterViewInfos;
 
    /**
     *
     * @param headerViewInfos  头布局VIEW
     * @param footerViewInfos  尾布局VIWE
     * @param adapter          普通ITEM的适配器adapter
     */
	public HeaderViewAdapterForRecycler (ArrayList<View> headerViewInfos,
			ArrayList<View> footerViewInfos, Adapter adapter) {
		mAdapter = adapter;
 
        if (headerViewInfos == null) {
            mHeaderViewInfos = new ArrayList<View>();
        } else {
            mHeaderViewInfos = headerViewInfos;
        }
 
        if (footerViewInfos == null) {
            mFooterViewInfos = new ArrayList<View>();
        } else {
            mFooterViewInfos = footerViewInfos;
        }
	}
 
    /**
     *
     * @return
     */
	@Override
	public int getItemCount() {
	  if (mAdapter != null) {
          //从此列表的条目数为：头+尾+普通条目适配器的 条数（即列表中间条目数）
            return getFootersCount() + getHeadersCount() + mAdapter.getItemCount();
        } else {
            return getFootersCount() + getHeadersCount();
        }
	}
 
	@Override
	public void onBindViewHolder(ViewHolder holder, int position) {
 
 
		int numHeaders = getHeadersCount();
        if (position < numHeaders) {
            //判断是头布局的话，不用填充数据因为我们已经在 MainActivity里为头VIEW填充了数据
            return ;
        }
 
        final int adjPosition = position - numHeaders;
        int adapterCount = 0;
        if (mAdapter != null) {
            adapterCount = mAdapter.getItemCount();
 
            //中间条目的数据 我们直接调度 普通条目adapter的onBindViewHolder来为条目VIEW填充数据
            if (adjPosition < adapterCount) {
            	mAdapter.onBindViewHolder(holder, adjPosition);
                return ;
            }
        }
 
        //其它情况就是尾布局VIEW,不用填充数据因为我们已经在 MainActivity里为尾VIEW填充了数据
 
	}
 
 
    /**
     * 得到条目类型：INVALID_TYPE表示当前条目是头部
     * @param position
     * @return
     */
	@Override
	public int getItemViewType(int position) {
 
        //
        int numHeaders = getHeadersCount();
        if (position < numHeaders) {//是头部
            return -1;
        }
        //正常条目部分
        // Adapter
        final int adjPosition = position - numHeaders;
        int adapterCount = 0;
        if (mAdapter != null) {
            adapterCount = mAdapter.getItemCount();
            if (adjPosition < adapterCount) {
                return mAdapter.getItemViewType(adjPosition);
            }
        }
        //footer部分
        return 1;
	}
 
    /**
     * 根据getItemViewType获得的viewType来返回对应的布局
     * @param parent
     * @param viewType
     * @return
     */
	@Override
	public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
		//header
		if(viewType == -1){
			return new HeaderViewHolder(mHeaderViewInfos.get(0));
		}else if(viewType == 1){//footer
			return new HeaderViewHolder(mFooterViewInfos.get(0));
		}
        // Footer (off-limits positions will throw an IndexOutOfBoundsException)
        return mAdapter.onCreateViewHolder(parent, viewType);
	}
	
    public int getHeadersCount() {
        return mHeaderViewInfos.size();
    }
 
    public int getFootersCount() {
        return mFooterViewInfos.size();
    }
 
    private static class HeaderViewHolder extends ViewHolder{
    	
		public HeaderViewHolder(View view) {
			super(view);
		}
    }
    
}
```

#### 2. 普通条目的adapter

由于HeaderViewAdapterForRecycler 重新包装了普通条目的adapter,我们在此有必要帖出普通（中间条目）adapter的源码：

```java
package com.anyikang.volunteer.sos.recyclerview;
 
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
 
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

### 五、如何使用我们自定义好的MyRecyclerView与HeaderViewAdapterForRecycler
梳理使用过程：

#### （1）在MainAcitivity的布局文件里声明MyRecyclerView：

```xml
<com.anyikang.volunteer.sos.recyclerview.MyRecyclerView
    android:layout_margin="50dp"
    android:id="@+id/recylerview"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    />
```

#### （2）先定义普通adapter（用于显示中间条目）

代码，见（四）中的 第2节

#### （3）定义HeaderViewAdapterForRecycler（具有处理理头部和尾部能力）

它相当于一个代理类，可以根据是否有头或尾的需求来重新封装了普通adapter
代码，见（四）中的 第1节

#### （4）在MainActivity里使用全新的RecyclerView

###### 核心步骤

```java
//实例化布局中的recylerview控件
recylerview = (MyRecyclerView)findViewById(R.id.recylerview);

recylerview.addHeaderView(head); //添加头部
recylerview.addFooterView(footer);//添加尾部
adapter = new MyRecyclerAdapter(list); //普通条目（中间条目）的adapter	
recylerview.setAdapter(adapter);   // setAdapter里发现有header或footer就会 将我们的adapter“偷梁换柱”
```

### 六、回马枪

重温原理, 直接上图：
