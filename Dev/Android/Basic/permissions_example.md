## Dynamic permissions

```java

public class LoginSignInActivity extends AppCompatActivity {
    private static final String[] ALL_PERMISSIONS = {
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE};
                
    private static final int APP_PERMISSION_REQUEST_CODE = 0x00000001;  
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
      ...
      
      // step one, check the permissions whether be granted, if granted do something
      if (checkPermissionAllGranted(ALL_PERMISSIONS)) {
           doSomething();
           return;
       }

       // step two, request permissions, if all the permisstion be granted, ignored
       ActivityCompat.requestPermissions(this, ALL_PERMISSIONS, APP_PERMISSION_REQUEST_CODE);
      ...
    }
    
    
    private boolean checkPermissionAllGranted(String[] permissions) {
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(mContext, permission) != PackageManager.PERMISSION_GRANTED) {
                return false;
            }
        }
        return true;
    }

    // step three, handle the result for requesting
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == APP_PERMISSION_REQUEST_CODE) {
            boolean isAllGranted = true;

            for (int grant : grantResults) {
                if (grant != PackageManager.PERMISSION_GRANTED) {
                    isAllGranted = false;
                    break;
                }
            }

            if (isAllGranted) {
                doSomething();
            } else {
                openAppDetails();
            }
        }
    }

    private void doSomething() {
        ...
    }

    private void openAppDetails() {
        AlertDialog.Builder builder = new AlertDialog.Builder(mContext);
        builder.setMessage("应用程序更新需要访问 “外部存储器”，请到 “应用信息 -> 权限” 中授予！");
        builder.setPositiveButton("去手动授权", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Intent intent = new Intent();
                intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
                intent.addCategory(Intent.CATEGORY_DEFAULT);
                intent.setData(Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                intent.addFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
                intent.addFlags(Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS);
                startActivity(intent);
            }
        });
        builder.setNegativeButton("取消", null);
        builder.show();
    }
}               
```

API 
#### 权限检查
```
ContextCompat.checkSelfPermission(thisActivity, Manifest.permission.WRITE_CALENDAR);
// @return PackageManager.PERMISSION_GRANTED or PackageManager.PERMISSION_DENIED。
```

#### 权限请求
```
ActivityCompat.requestPermissions(thisActivity, new String[]{Manifest.permission.READ_CONTACTS}, REQUEST_CODE);
```

#### 请求相应
```
@Override
public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
 
}
```




[more>>](https://github.com/Andy-13/ZbPermission)
