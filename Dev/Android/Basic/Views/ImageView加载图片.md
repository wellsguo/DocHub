## ImageView 加载图片的 3 种常用方式

比如：我们从相册获取一张照片,通过 `startActivityForResult()` 在 `onActivityResult(Intent data)` 里面给我们返回来照片的路径 

```java
Uri uri = data.getData(); //拿到uri后 就是拿到了照片的路径  然后就进入正题了 拿到这个路径如何设置给我们的imageView呢  
```

### uri

```java
imageView.setImageURI(uri2); // content://media/external/images/media/63   
```

### bitmapt(drawable/resource)

- 首先我们把它转换成 Bitmap
  
```java
Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResulver,uri);
```

- 然后就好办了 有了 bitmap 很多人都知道怎么做了 

```java
imageView.setImageBitmap(bitmap);
```

- 或将 bitmap 转为drawable

```java
Drawable drawable = new BitmapDrawable(bitmap);
imageView.setImageDrawable(drawable); 
```

但是如果我们用 Glide 去加载的话 glide 默认不能直接加载 bitmap

### glide

> 方式1： drawable

```java
Drawable drawable = new BitmapDrawable(bitmap);
imageView.setImageDrawable(drawable); 
// 或者
// Glide.with(context).load(drawable).into(imageView);
```

> 方式2： byte数组

```java
ByteArrayOutputStream baos = new ByteArrayOutputStream();
bitmap.compress(Bitmap.CompressFormat.PNG,100,baos);
byte[ ] bytes = baos.toByteArray;
Glide.with(context).load(bytes ).into(imageView);
```

## 应用场景

注意：**一定不要通过 Intent 传 bitmap **

Intent可传递的**数据大小有限**，具体多少我并未实际测试过，跟ROOM设置的APP最大内存也有关系，网上有人做了[实际代码测试](https://blog.csdn.net/wingichoy/article/details/50679322)



### 本地图片

本地资源只传递R.id，然后通过resource去解析出来；

### SD 图片

如果是SDCard中的文件，只传递Uri；

### 网络图片

如果是网络流，先本地保存图片，然后再传递路径Uri。

## path uri file

```java
public void takePhoto() {
    Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);  
    this.startActivityForResult(intent, 3);  
}
```

### onActivityResult方法中接收

```java
Bundle bundle =data.getExtras();
//获取相机返回的数据，并转换为Bitmap图片格式 
aphoto = (Bitmap)bundle.get("data");
if (data.getData()!=null){
    imageUri =data.getData();
}else {
    imageUri = Uri.parse(MediaStore.Images.Media.insertImage(getActivity().getContentResolver(), aphoto, null,null));
}
```

### Android根据图片path转成Uri，分享图片

```java
Uri uri = Uri.fromFile(new File(filePath));//根据路径转化为uri
Intent imageIntent = new Intent(Intent.ACTION_SEND); //调用系统的ACTION_SEND
imageIntent.setType("image/png");
imageIntent.putExtra(Intent.EXTRA_STREAM, uri);// EXTRA_STREAM对应转化为uri的pathstartActivity(Intent.createChooser(imageIntent, "分享"));
```

### 本地路径转换成URL相对路径

```java
//本地路径转换成URL相对路径
private string urlconvertor(string imagesurl1)
{
    string tmpRootDir = Server.MapPath(System.Web.HttpContext.Current.Request.ApplicationPath.ToString());//获取程序根目录
    string imagesurl2 = imagesurl1.Replace(tmpRootDir, ""); //转换成相对路径
    imagesurl2 = imagesurl2.Replace(@"\", @"/");
    //imagesurl2 = imagesurl2.Replace(@"Aspx_Uc/", @"");
    return imagesurl2;
}
```


