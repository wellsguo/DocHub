
# activity 与 fragment 之间的传递数据
 

## 1. activity 之间的数据传递


### 1.1 intent

**传递**

```java
Intent i= new Intent(MainActivity.this,TheAty.class);
i.putExtra("date","Hello SWWWWWW");
startActivity(i);
```

**接受数据**

```java
Intent i =getIntent();

tv=(TextView) findViewById(R.id.tv);

//通过“date”关键字进行添加tv.setText(i.getStringExtra("date"));
```

 

### 1.2 intent+bundle

**传递数据**

```java
Intent i= new Intent(MainActivity.this,TheAty.class);
Bundle b=new Bundle();
b.putString("name","SWWWWW");
b.putInt("age",21);
b.putString("depart","KuaiJi");
i.putExtras(b);
startActivity(i);
```


**接受数据**

```java
Intent i =getIntent();
Bundle data=i.getExtras();
tv=(TextView) findViewById(R.id.tv);
tv.setText(String.format("name=%s,age=%d,depart=%s",data.getString("name"),data.getInt("age"),data.getString("depart")));
```



## 2. Activity 传给 Fragment

### 2.1 setArguments()

```java
MyFragment myFragment = new MyFragment();
Bundle bundle = new Bundle();
bundle.putString("DATA",values);//这里的values就是我们要传的值
myFragment.setArguments(bundle);
```

### 2.2 Activity interface

- 宿主 Activity 中的 getTitles() 方法
    ```java
    public String getTitles(){
        return "hello";
    }
    ```

- Fragment 中的 onAttach 方法
    ```java
    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        titles = ((MainActivity) activity).getTitles();
    }
    //通过强转成宿主activity，就可以获取到传递过来的数据
    ```


## 3. Fragment向activity中传值

- (1) 在Fragment中写一个回调接口  

- (2) 在activity中实现这个回调接口

- (3) 在Fragment中onAttach 方法中得到activity中实现好的 实例化接口对象

- (4) 用接口的对象进行传值

### activity

```java  
@SuppressLint("NewApi")   
public class MainActivity extends Activity implements CallBackValue{  
  
    private TextView tv1;  
    @Override  
    protected void onCreate(Bundle savedInstanceState) {  
        super.onCreate(savedInstanceState);  
        setContentView(R.layout.activity_main);  
          
        tv1 = (TextView) findViewById(R.id.tv1);  
          
        FragmentManager manager = getFragmentManager();  
        FragmentTransaction transaction = manager.beginTransaction();  
          
        transaction.add(R.id.contents, new Fragmen1());  
        transaction.commit();  
          
    }  
    //要获取的值  就是这个参数的值  
    @Override  
    public void SendMessageValue(String strValue) {  
        // TODO Auto-generated method stub  
        tv1.setText(strValue);  
    }  
      
}  
```

## Fragment

```java
@SuppressLint("NewApi")   
public class Fragmen1 extends Fragment{  
    private Button btn1;  
    private EditText et1; 
    /** 
     * fragment与activity产生关联是  回调这个方法  
     */  
    CallBackValue callBackValue;  

    @Override  
    public void onAttach(Activity activity) {  
        super.onAttach(activity);  
        //当前fragment从activity重写了回调接口  得到接口的实例化对象  
        callBackValue =(CallBackValue) getActivity();  
    }  
      
      
    @Override  
    public View onCreateView(LayoutInflater inflater, ViewGroup container,  
            Bundle savedInstanceState) {  
        View view = inflater.inflate(R.layout.fragment_layout1, container, false);  
        btn1 = (Button) view.findViewById(R.id.btn1);  
        et1 = (EditText) view.findViewById(R.id.et1);  
        btn1.setOnClickListener(new OnClickListener() {  
            @Override  
            public void onClick(View v) {  
                String strValue = et1.getText().toString().trim();  
                callBackValue.SendMessageValue(strValue);  
            }  
        });  
          
        return view;  
    }  
    //定义一个回调接口  
    public interface CallBackValue{  
        public void SendMessageValue(String strValue);  
    }  
}  
```