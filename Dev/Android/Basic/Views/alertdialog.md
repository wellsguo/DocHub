### AlertDialog



## 基本语法

```
builder=new AlertDialog.Builder(this);
builder.setIcon(R.mipmap.ic_launcher);
builder.setTitle(R.string.simple_dialog);
builder.setMessage(R.string.dialog_message);

//监听下方button点击事件
builder.setPositiveButton(R.string.postive_button, new DialogInterface.OnClickListener() {
    @Override
    public void onClick(DialogInterface dialogInterface, int i) {
        Toast.makeText(getApplicationContext(),R.string.toast_postive,Toast.LENGTH_SHORT).show();
    }
});

builder.setNegativeButton(R.string.negative_button, new DialogInterface.OnClickListener() {
    @Override
    public void onClick(DialogInterface dialogInterface, int i) {
        Toast.makeText(getApplicationContext(), R.string.toast_negative, Toast.LENGTH_SHORT).show();
    }
});

//设置对话框是可取消的
builder.setCancelable(true);
AlertDialog dialog=builder.create();
dialog.show();
```     

![](http://img.blog.csdn.net/20150501172701594)

## 列表 | 单选 | 多选

```java
private void showSimpleListDialog(View view) {
    builder=new AlertDialog.Builder(this);
    builder.setIcon(R.mipmap.ic_launcher);
    builder.setTitle(R.string.simple_list_dialog);

    /**
     * 设置内容区域为简单列表项
     */
    final String[] Items={"Items_one","Items_two","Items_three"};
    builder.setItems(Items, new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialogInterface, int i) {
            Toast.makeText(getApplicationContext(), "You clicked "+Items[i], Toast.LENGTH_SHORT).show();
        }
    });
    
    /**
     * 设置内容区域为单选列表项
     */
    final String[] items={"Items_one","Items_two","Items_three"};
    builder.setSingleChoiceItems(items, 1, new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialogInterface, int i) {
            Toast.makeText(getApplicationContext(), "You clicked "+items[i], Toast.LENGTH_SHORT).show();
        }
    });
    
    /**
     * 设置内容区域为多选列表项
     */
    final String[] items={"Items_one","Items_two","Items_three"};
    builder.setMultiChoiceItems(items, new boolean[]{true, false, true}, new DialogInterface.OnMultiChoiceClickListener() {
        @Override
        public void onClick(DialogInterface dialogInterface, int i, boolean b) {
            Toast.makeText(getApplicationContext(),"You clicked "+items[i]+" "+b,Toast.LENGTH_SHORT).show();
        }
    });

    
    builder.setCancelable(true);
    AlertDialog dialog=builder.create();
    dialog.show();
}
```    

### 自定义 View 
```java
private void showCustomViewDialog(View view){
    builder=new AlertDialog.Builder(this);
    builder.setIcon(R.mipmap.ic_launcher);
    builder.setTitle(R.string.custom_view_dialog);

    /**
     * 设置内容区域为自定义View
     */
    LinearLayout loginDialog= (LinearLayout) getLayoutInflater().inflate(R.layout.custom_view,null);
    builder.setView(loginDialog);

    builder.setCancelable(true);
    AlertDialog dialog=builder.create();
    dialog.show();
}
```

### 自定义 Adapter  
```java
private class ItemBean{
    private int imageId;
    private String message;

    public ItemBean(int imageId, String message) {
        this.imageId = imageId;
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public int getImageId() {
        return imageId;
    }

    public void setImageId(int imageId) {
        this.imageId = imageId;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}


private void showCustomAdapterDialog(View view){

    builder=new AlertDialog.Builder(this);
    builder.setIcon(R.mipmap.ic_launcher);
    builder.setTitle(R.string.custom_adapter_dialog);

    /**
     * 设置内容区域为自定义adapter
     */
    List<ItemBean> items=new ArrayList<>();
    items.add(new ItemBean(R.mipmap.icon,"You can call me xiaoming"));
    items.add(new ItemBean(R.mipmap.ic_launcher, "I'm android xiao"));
    CustomAdapter adapter=new CustomAdapter(items,getApplicationContext());
    builder.setAdapter(adapter, new DialogInterface.OnClickListener() {
        @Override
        public void onClick(DialogInterface dialogInterface, int i) {
            Toast.makeText(getApplicationContext(),"You clicked"+i,Toast.LENGTH_SHORT).show();
        }
    });

    builder.setCancelable(true);
    AlertDialog dialog=builder.create();
    dialog.show();

}
```    

