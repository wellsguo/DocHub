## service

### service 实现及生命周期
```java
public class TemplateService extends Service {
 
    @Override
    public void onCreate() {
        // todo
        super.onCreate();
    }
 
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // todo
        return super.onStartCommand(intent, flags, startId);
    }
 
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        // todo
        return null;
    }
 
    @Override
    public void onDestroy() {
        // todo
        super.onDestroy();
    }
}
```

### mainifest 注册

```xml
    <service 
        android:name="com.example.servicetest.TemplateService" 
    />  

```

### 组件启动/停止 或 绑定/解绑

#### 启动/停止

```java
public class MainActivity extends AppCompatActivity {
 
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // ...
 
        // 连续启动 Service
        Intent intentOne = new Intent(this, TemplateService.class);
        startService(intentOne);
        Intent intentTwo = new Intent(this, TemplateService.class);
        startService(intentTwo);
        Intent intentThree = new Intent(this, TemplateService.class);
        startService(intentThree);
 
        // 停止 Service
        Intent intentFour = new Intent(this, TemplateService.class);
        stopService(intentFour);
 
        // 再次启动 Service
        Intent intentFive = new Intent(this, TemplateService.class);
        startService(intentFive);
 
        // ...
    }
}
```