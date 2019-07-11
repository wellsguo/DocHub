# Android 权限系统

### Android 7.0 开发中需要注意的问题：
 - 大问题没有，主要的一个，也是最重要的一个，Android7.0 以上 不能使用 Uri.fromFile 方法来取得文件 URI。而是使用 FileProvider (v4提供)。具体使用方法可以百度。 
 - 所有影响到的，基本上有，下载应用进行安装的隐式意图，发出拍照的隐式意图，裁剪图片选择图片等的意图。

### Android 8.0 开发中需要注意的问题： 
  - Android_ID 每个应用取到的会不一样。  
  - 创建快捷方式，不再使用广播，而是直接使用 ShortcutManager 的 requestPinShortcut() 方法。
  - 还有，android8.0 原生支持图标的角标。


## Google 官方授权流程

动态授权的过程可以大概分为以下三个步骤：
### 1.检查权限
> ContextCompat.checkSelfPermission();

如果您的应用中需要危险权限，则每次执行需要这一权限的操作时，都必须检查是否具有该权限，用户始终可以自由的调用次权限，因此，即使应用昨天使用了相应，他不能假设自己今天仍然具有该权限。
```java
// Assume thisActivity is the current activity
int permissionCheck = ContextCompat.checkSelfPermission(thisActivity,
        Manifest.permission.WRITE_CALENDAR);
```        
        
### 2.申请权限
> ContextCompat.requestPermissions();

如果应用需要Manifest清单中的危险权限，那么他必须要求用户授予该权限。并且在某些情况下，我们需要让用户了解应用为什么需要某些权限。最简单的例子是，当我们需要相机拍照的时候需要相机权限，这是很正常的需求，但是当我们需要保存照片信息的时候，需要用户的地理位置信息，这个权限对于用户来说就显得很不理解。针对这种现状，Google也为我们提供了很实用的Api ，ContextCompat.shouldShowRequestPermissionRationab-如果应用之前请求过次权限但用户拒绝了，则该方法返回true。如果用户不仅拒绝上次的请求权限，而且勾选了“不再提示”，则该方法返回false。

```java
// Here, thisActivity is the current activity
if (ContextCompat.checkSelfPermission(thisActivity,
                Manifest.permission.READ_CONTACTS)
        != PackageManager.PERMISSION_GRANTED) {
 
    // Should we show an explanation?
    if (ActivityCompat.shouldShowRequestPermissionRationale(thisActivity,
            Manifest.permission.READ_CONTACTS)) {
 
        // Show an expanation to the user *asynchronously* -- don't block
        // this thread waiting for the user's response! After the user
        // sees the explanation, try again to request the permission.
 
    } else {
 
        // No explanation needed, we can request the permission.
 
        ActivityCompat.requestPermissions(thisActivity,
                new String[]{Manifest.permission.READ_CONTACTS},
                MY_PERMISSIONS_REQUEST_READ_CONTACTS);
 
        // MY_PERMISSIONS_REQUEST_READ_CONTACTS is an
        // app-defined int constant. The callback method gets the
        // result of the request.
    }
}
```
### 3.处理申请结果
> onRequestPermissionResult();

当应用请求权限时候，系统将向用户显示一个对话框。当用户相应的时候，系统将调用onRequstPermissionsResult() 方法。向其传递用户的相应。我们需要在我们自己Activity中复写该方法。并且对用户操作的反馈做处理。

```java
@Override
public void onRequestPermissionsResult(int requestCode,
        String permissions[], int[] grantResults) {
    switch (requestCode) {
        case MY_PERMISSIONS_REQUEST_READ_CONTACTS: {
            // If request is cancelled, the result arrays are empty.
            if (grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
 
                // permission was granted, yay! Do the
                // contacts-related task you need to do.
 
            } else {
 
                // permission denied, boo! Disable the
                // functionality that depends on this permission.
            }
            return;
        }
 
        // other 'case' lines to check for other
        // permissions this app might request
    }
}
```

## 实际上的动态授权方案

如果你了解了上面这些内容就以为了解了动态权限申请。那只能说明你太天真。需要说明的是，以上这些内容全部都是来自Google的官方Demo。国内真正的Android开发环境，你心里没有点数吗？国内Rom客制化太多了，Google 原生API被改的很严重，这对于我们要去完美适配，真的是一种噩梦。举几个简单的例子，你就知道当前的现状有多么的惨不忍睹。

> 以小米为例

###### 小米系统在Android原生的动态权限申请的基础下，还有自己的用户授权模块。
（感觉很正常？）。什么意思？先看小米的授权模块UI：

![](https://img-blog.csdn.net/20180519181619490)
![](https://img-blog.csdn.net/20180519181645525)

可以看到小米的授权模块中，对权限操作可以分为```允许，询问，拒绝```。当我们第一次打开应用的时候，默认是询问状态，在该状态下，我们调用 requestPermission() 方法会弹出系统询问框.在弹出系统授权框后，只要你操作了（拒绝或者允许）,你永远也不要想着在以后能看到授权框了，除非你过来设置这边更改为“询问”模式。不然无论你再调用几次 requestPermissions()，都是直接走回调 OnRequestPermissionResult()。总结为一句话，小米客制的授权模块是凌驾于 Google 的授权模块之上的，具体表现为以下几个方面：

  - (1) 所谓的动态授权，Google的原意为应用每次需要涉及到敏感权限，都是需要动态申请的。（原话：即使应用昨天使用了相应，他不能假设自己今天仍然具有该权限）。但是在小米系统中，只要通过一次授权之后，每次检查权限都是返回第一次授权的结果，换句话说，只要昨天你第一次同意了使用相机，那之后每一次我都是有权限使用相机的。如果有一天你不在想赋予应用相机权限，那么你必须要到相应的设置界面去操作。什么叫做动态。小米的做法是“一劳永逸”.

  - (2) Google 动态授权还表现在如果用户上次拒绝授权，或者说用户上次关闭了授权提示，我们是可以通过官方提供的 api shouldShowRequestPermissionRationab()，来判断上次用户的操作的，并且根据结果在增加相应的提示，或者引导用户下一步的操作。这其实是丰富了我们与用户的交互过程，极大提升了用户的体验。但是这些在小米的系统里面全没了，shouldShowRequestPermissionRationab()这个方法在小米系统中没有用的，永远返回的是false。

  - (3) 在处理授权回调中，对于授权的结果无非是PackageManager.PERMISSION_GRANTED,PackageManager.PERMISSION_DENIED,但是在小米的一些机型中，OnRequestPermissionsResult()回调中返回的结果并不是这两者。

  - (4) 在小米的系统中，有些权限显得很混乱。比如说存储卡读写权限。没有动态去申请，直接检查权限，居然是已经授权了。但是有时真正的去读写内部存储卡的时候又会跑出异常，让人很捉摸不透。

    当然小米的系统缺陷远远不止这些。针对这些情况，总结了自己的一套权限申请方案。具体逻辑如下。

![](https://img-blog.csdn.net/2018051919244678)

 > 跟着思路走

 ### 1. 定义权限回调
```java
    // 这是权限回调接口；
    public interface OnPermissionCallback {
        // 授权；
        void onGranted();
 
        // 拒绝；
        void onDenied();
    }
```    
### 2. 请求权限
这个是供外界调用的方法。参数为需要申请的权限，和权限回调。如果申请的权限已经被用户授权，则直接走授权回调，否则去申请权限。
```
/**
 * 要求授权；
 */
public void requestPermissions(@NonNull String[] permissions, @NonNull OnPermissionCallback callback) {
    if (permissions.length < 1) {
        return;
    }
    mPermissions = permissions;
    mPermissionCallback = callback;
    if (checkPermissions(permissions)) {
        // 有权限
        if (mPermissionCallback != null) {
            mPermissionCallback.onGranted();
        }
    } else {
        // 无权限；
        ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
    }
}
```    
### 3.申请权限后
程序会走OnRequestPermissionsResult()的回调。在回调中继续我们的逻辑；
```java
@Override
public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                       @NonNull int[] grantResults) {
    if (requestCode == PERMISSION_REQUEST_CODE) {
        if (checkPermissionResult(grantResults)) {
            // 全部授权
            if (mPermissionCallback != null) {
                mPermissionCallback.onGranted();
            }
        } else {
            if (shouldShowRequestPermissionsRationale(permissions)) {
                // 用户选择了拒绝；
                ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
            } else {
                // 用户选择了不再提示；
                showPermissionRationale(null, null);
            }
            // 没有全部授权；
            if (mPermissionCallback != null) {
                mPermissionCallback.onDenied();
            }
        }

    } else {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
}
 ```   
在onRequestPermissionResult方法中，如果申请的所有权限都已经授权，则走授权回调。没有的话，再通过shouldRequestPermissionRationale()方法继续分析用户的针对我们的上次授权的操作。需要说明的一点是shouldRequestPermissonsRationale()这个方法的返回值，如果用户针对我们的上次请求权限拒绝的话，会返回true，如果用户针对我们的上次请求权限不仅做了拒绝的操作，而且还点击了“不再提醒”（就是以后不会再跳出授权框）的选择框，则该方法返回false。针对这个情况，如果用户只是单纯的拒绝授权，我们在这里进行第二次的请求权限。如果用户选择“不再提醒”,我们就弹出一个自定的Dialog，引导用户去设置界面授权。

这里的Dialog，我直接用了SweetDialog的普通样式。
```java
// 跳出 提示界面；
private void showPermissionRationale(@Nullable String title, @NonNull String content) {
    SweetAlertDialog dialog = new SweetAlertDialog(this, SweetAlertDialog.NORMAL_TYPE);
    dialog.setCancelable(false);
    dialog.setTitleText(TextUtils.isEmpty(title) ? getString(R.string.permission_title) : title)
            .setContentText(TextUtils.isEmpty(content) ? getString(R.string
                    .permission_content) : content)
            .setConfirmButton(R.string.dialog_ok, new SweetAlertDialog.OnSweetClickListener() {
                @Override
                public void onClick(SweetAlertDialog sweetAlertDialog) {
                    sweetAlertDialog.dismissWithAnimation();
                    gotoSetting();
                }
            })
            .setCancelButton(R.string.permission_cancle, new SweetAlertDialog
                    .OnSweetClickListener() {
                @Override
                public void onClick(SweetAlertDialog sweetAlertDialog) {
                    sweetAlertDialog.dismissWithAnimation();
                    if(mPermissionCallback!=null){
                        mPermissionCallback.onDenied();
                    }
                }
            })
            .show();

}
```
    



在Dialog中如果用户选择取消的话，则表示这次授权失败了，直接走失败的回调。如果用户选择"ok”的话，则引导用户到设置详情界面去手动授权。

```java
// 跳转到设置界面；
private void gotoSetting() {
    Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
    intent.setData(Uri.fromParts("package", getPackageName(), null));
    startActivityForResult(intent, PERMISSION_REQUEST_CODE);
}
```    

需要注意的是这里引导用户到设置界面的方式是通过startActivityForResult()的方式。用户在从设置界面回到应用的时候，会走onActivityResult()方法，在这里我们需要再一次的对权限做判断。
```java
@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    if (requestCode == PERMISSION_REQUEST_CODE) {
        if (mPermissions != null && checkPermissions(mPermissions)) {
            if (mPermissionCallback != null) {
                mPermissionCallback.onGranted();
            } else {
                mPermissionCallback.onDenied();
            }
        }
    } else {
        super.onActivityResult(requestCode, resultCode, data);
    }

}
```    
以上的这些都是在我的Activity的基类中完成的。我的所有activity继承这个基类。在需要动态权限的地方只需要一句代码就可以完成动态权限的申请了。
```java
requestPermissions(new String[]{Manifest.permission.CAMERA}, new OnPermissionCallback() {
    @Override
    public void onGranted() {
        Log.d("Permission","onGranted");
    }

    @Override
    public void onDenied() {
        Log.d("Permission","onDenied");
    }
});
```        
一句代码搞定。大功告成。后面的事情就是看看在各个版本的手机上适配问题了。这些问题太头疼了。当然如果觉得用自己的方法去适配动态权限有困难的话，也可以用第三方的开源框架。github上还是有挺多的。

--------------------- 
作者：会写代码的哈士奇    
来源：CSDN   
原文：https://blog.csdn.net/yuguqinglei/article/details/80375702   
版权声明：本文为博主原创文章，转载请附上博文链接！  