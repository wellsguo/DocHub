## [拒绝recycleView嵌套recycleView，处理数据使用稳定的一个recycleView](https://blog.csdn.net/liyuali2012/article/details/78689276)  


之前写订单功能，后台给的数据不尽人意，接口又不能改了。查阅资料，发现一个新颖的思路。

### 需求

可以看到：每个大订单里包含不确定数量的小订单，所以item界面不能单一控制。想过用recycleview嵌套recycleview也实践过，但出问题了，具体是滑动冲突？还是数据计算？忘了。

![](https://img-blog.csdn.net/20171201180948378?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbGl5dWFsaTIwMTI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

### 解决思路

上网查了一些资料，看到一篇[文章](http://www.jianshu.com/p/b25340903671)(**[code](https://github.com/19snow93/OrderListLogic)**),
思路是这样：利用 `recycleview` 的 `viewType` 拆分成不同的 `view`，所以重要的是拆分数据。


可以看到，每个item可以拆分为三个布局：

![](https://img-blog.csdn.net/20171201175718818?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbGl5dWFsaTIwMTI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

想办法把数据解析成自己想要的样子。像下面这样，把拿到的后台数据list，解析成三个对象，然后再放进另一个datalist中。这样规范的datalist塞到recycleview中，完美。哈哈

```java
* List<Object>有三种数据类型：
* 1、GoodsOrderInfo 表示每个小订单的头部信息（订单号、订单状态、店铺名称）
* 2、OrderGoodsItem 表示小订单中的商品
* 3、OrderPayInfo 表示大订单的支付信息（金额、订单状态）

// 把所有数据按照头部、内容和尾部三个部分放入
dataList.add(orderHeadInfo);
dataList.addAll(orderGoodsItems);
dataList.add(orderPayInfo);
```

### 具体操作

重点就是怎么解析成想要的样子的。看下面，之前看原作者的文章时，看了两天，差点绕晕，所以想以自己的理解重新记录一下，非常感谢原作者的思路。

- 首先经过一系列网络请求，拿到订单数据orderListBeanList（已由GsonFormat解析）

```java
orderListBeanList = dataBean.getOrderList();
List<Object>dataList = OrderDataHelper.getDataAfterHandle(orderListBeanList);
```

##### OrderDataHelper.java

```java
public class OrderDataHelper {
    /**
     * List<Object>有三种数据类型：
     * 1、GoodsOrderInfo 表示每个小订单的头部信息（订单号、订单状态、店铺名称）
     * 2、OrderGoodsItem 表示小订单中的商品
     * 3、OrderPayInfo 表示大订单的支付信息（金额、订单状态）
     *
     * @param resultList
     * @return
     */
    public static List<Object> getDataAfterHandle(List<MyOrderListBean.DataBean.OrderListBean> resultList) {


        List<Object> dataList = new ArrayList<Object>();
        //遍历每一张大订单
        for (MyOrderListBean.DataBean.OrderListBean orderListBean : resultList) {
            //订单支付的金额和订单状态
            OrderPayInfo orderPayInfo = new OrderPayInfo();
            orderPayInfo.setTotalPrice(orderListBean.getTotalPrice());
            orderPayInfo.setState(orderListBean.getState());
            orderPayInfo.setOrderId(orderListBean.getId());
            orderPayInfo.setOrderNo(orderListBean.getOrderNo());
            orderPayInfo.setComment(orderListBean.isCommented());

            //创建时间
            OrderHeadInfo orderHeadInfo = new OrderHeadInfo();
            orderHeadInfo.setCreatTime(orderListBean.getCreateTimeStr());
            orderHeadInfo.setState(orderListBean.getState());
            orderHeadInfo.setOrderId(orderListBean.getId());
            orderHeadInfo.setOrderNo(orderListBean.getOrderNo());

            //订单商品
            List<MyOrderListBean.DataBean.OrderListBean.OrderDetailListBean> orderDetailList = orderListBean.getOrderDetailList();

            List<OrderGoodsItem> orderGoodsItems = new ArrayList<>();

            //遍历每个大订单里面的商品
            for (MyOrderListBean.DataBean.OrderListBean.OrderDetailListBean orderDetailListBean : orderDetailList) {
                //获取商品的订单id
                OrderGoodsItem orderGoodsItem = new OrderGoodsItem();
                orderGoodsItem.setGoodsName(orderDetailListBean.getGoodsName());
                orderGoodsItem.setGoodsDescribe(orderDetailListBean.getGoodsDescribe());
                orderGoodsItem.setGurl(orderDetailListBean.getGurl());
                orderGoodsItem.setOrderId(orderDetailListBean.getOrderId()+"");
                orderGoodsItem.setSalePrice(orderDetailListBean.getSalePrice());
                orderGoodsItem.setGoodsCount(orderDetailListBean.getGoodsCount());
                orderGoodsItems.add(orderGoodsItem);
            }
            //把所有数据按照头部、内容和尾部三个部分排序好
            dataList.add(orderHeadInfo);
            dataList.addAll(orderGoodsItems);
            dataList.add(orderPayInfo);
        }
        return dataList;
    }
}
```

- 处理完数据之后，就可以像普通数据一样放到自己的订单adapter中了，具体写法如下：

##### Adapter.java

```java
public class OrderAdapter extends RVBaseAdapter {

    private int ITEM_HEADER = 1, ITEM_CONTENT = 2, ITEM_FOOTER = 3;

    private String clientId;

    private DialogTiShi dialogTiShi;

    public OrderAdapter(BaseActivity activity) {
        super(activity);
    }

    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view;
        if (viewType == TYPE_EMPTY) {
            view = LayoutInflater.from(activity).inflate(R.layout.order_empty, parent, false);
            MyApplication.scaleScreenHelper.loadView((ViewGroup) view, new AppScale());
            return new EmptyViewHolder(view);
        } else if (viewType == ITEM_HEADER) {
            view = LayoutInflater.from(activity).inflate(R.layout.item_order_head, parent, false);
            MyApplication.scaleScreenHelper.loadView((ViewGroup) view, new AppScale());
            return new ViewHolderHeader(view);
        } else if (viewType == ITEM_CONTENT) {
            //view = LayoutInflater.from(activity).inflate(R.layout.item_order_content, parent, false);
            view = LayoutInflater.from(activity).inflate(R.layout.item_order_detail_list, parent, false);
            MyApplication.scaleScreenHelper.loadView((ViewGroup) view, new AppScale());
            return new ItemViewHolder(view);
        } else if (viewType == ITEM_FOOTER) {
            view = LayoutInflater.from(activity).inflate(R.layout.item_order_foot, parent, false);
            MyApplication.scaleScreenHelper.loadView((ViewGroup) view, new AppScale());
            return new ViewHolderFoot(view);
        }
        return null;
    }

    @Override
    public void onBindViewHolder(RecyclerView.ViewHolder holder, int position) {
        holder.itemView.setClickable(true);

        clientId = SpUtil.getSpString(Constant.SpConstants.USER_INFO, Constant.SpConstants.ClientId, "");

        if (holder instanceof ViewHolderHeader) {
            final ViewHolderHeader viewHolderHeader = (ViewHolderHeader) holder;
            OrderHeadInfo orderHeadInfo = (OrderHeadInfo) allList.get(position);
        } else if (holder instanceof ItemViewHolder) {
            final ItemViewHolder itemViewHolder = (ItemViewHolder) holder;
            final OrderGoodsItem orderGoodsItem = (OrderGoodsItem) allList.get(position);
        }
        if (holder instanceof ViewHolderFoot) {
            final ViewHolderFoot viewHolderFoot = (ViewHolderFoot) holder;
            OrderPayInfo orderPayInfo = (OrderPayInfo) allList.get(position);
        }
    }

    @Override
    public int getItemCount() {
        return allList.size() == 0 ? 1 : allList.size();
    }

    @Override
    public int getItemViewType(int position) {
        if (allList.size() == 0) {
            return TYPE_EMPTY;
        } else if (allList.get(position) instanceof OrderHeadInfo) {
            return ITEM_HEADER;
        } else if (allList.get(position) instanceof OrderGoodsItem) {
            return ITEM_CONTENT;
        } else if (allList.get(position) instanceof OrderPayInfo) {
            return ITEM_FOOTER;
        }
        return ITEM_CONTENT;
    }

    static class ItemViewHolder extends RecyclerView.ViewHolder {
        @Bind(R.id.rel_item)
        LinearLayout relItem;
        @Bind(R.id.iv_order_picture)
        ImageView ivOrderPicture;
        @Bind(R.id.tv_title)
        TextView tvTitle;
        @Bind(R.id.tv_content)
        TextView tvContent;
        @Bind(R.id.tv_order_realprice)
        TextView tvOrderRealprice;
        @Bind(R.id.tv_count)
        TextView tvCount;

        ItemViewHolder(View view) {
            super(view);
            ButterKnife.bind(this, view);
        }
    }

    static class ViewHolderHeader extends RecyclerView.ViewHolder {
        @Bind(R.id.tv_order_time)
        TextView tvOrderTime;
        @Bind(R.id.tv_order_state)
        TextView tvOrderState;

        ViewHolderHeader(View view) {
            super(view);
            ButterKnife.bind(this, view);
        }
    }

    static class ViewHolderFoot extends RecyclerView.ViewHolder {
        @Bind(R.id.tv_account)
        TextView tvAccount;
        @Bind(R.id.tv_cancle)
        TextView tvCancle;
        @Bind(R.id.tv_pay)
        TextView tvPay;
        @Bind(R.id.lay_btn)
        LinearLayout layBtn;

        ViewHolderFoot(View view) {
            super(view);
            ButterKnife.bind(this, view);
        }
    }

}
```
