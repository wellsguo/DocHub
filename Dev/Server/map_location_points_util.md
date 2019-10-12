## 腾讯地图&百度地图&高德地图转换

### 定义

GCJ02 坐标系：即火星坐标系，是由中国国家测绘局制订的地理信息系统的坐标系统。由WGS84坐标系经加密后的坐标系。
1. 谷歌中国地图
2. 腾讯地图
3. 高德地图

BD09 坐标系：即百度坐标系，GCJ02坐标系经加密后的坐标系;
1. 百度地图

### GCJ02坐标转换BD09

```php
  /**
   * 中国正常GCJ02坐标---->百度地图BD09坐标 
   * 腾讯地图用的也是GCJ02坐标
   * @param double $lat 纬度
   * @param double $lng 经度
   */
  public function Convert_GCJ02_To_BD09($lat,$lng){
          $x_pi = 3.14159265358979324 * 3000.0 / 180.0;
          $x = $lng;
          $y = $lat;
          $z =sqrt($x * $x + $y * $y) + 0.00002 * sin($y * $x_pi);
          $theta = atan2($y, $x) + 0.000003 * cos($x * $x_pi);
          $lng = $z * cos($theta) + 0.0065;
          $lat = $z * sin($theta) + 0.006;
          return array('lng'=>$lng,'lat'=>$lat);
  }
```

### BD09 坐标转换GCJ02

```php 
  /**
   * 百度地图BD09坐标---->中国正常GCJ02坐标
   * 腾讯地图用的也是GCJ02坐标
   * @param double $lat 纬度
   * @param double $lng 经度
   * @return array();
   */
  public function Convert_BD09_To_GCJ02($lat,$lng){
      $x_pi = 3.14159265358979324 * 3000.0 / 180.0;
      $x = $lng - 0.0065;
      $y = $lat - 0.006;
      $z = sqrt($x * $x + $y * $y) - 0.00002 * sin($y * $x_pi);
      $theta = atan2($y, $x) - 0.000003 * cos($x * $x_pi);
      $lng = $z * cos($theta);
      $lat = $z * sin($theta);
      return array('lng'=>$lng,'lat'=>$lat);
  }
```

## 谷歌、高德和百度地图使用的坐标分析
2017.05.23 14:16:29

众所周知地球是一个不规则椭圆体，GIS中的坐标系定义由基准面和地图投影两组参数确定，而基准面的定义则由特定椭球体及其对应的转换参数确定。 基准面是利用特定椭球体对特定地区地球表面的逼近，因此每个国家或地区均有各自的基准面。基准面是在椭球体基础上建立的，椭球体可以对应多个基准面，而基准面只能对应一个椭球体。 意思就是无论是谷歌地图、搜搜地图还是高德地图、百度地图区别只是针对不同的大地地理坐标系标准制作的经纬度，不存在准不准的问题，大家都是准的只是参照物或者说是标准不一样。

谷歌地图采用的是**WGS84**地理坐标系（中国范围除外），谷歌中国地图和搜搜中国地图采用的是**GCJ02**地理坐标系，百度采用的是**BD09**坐标系，而设备一般包含 ***GPS芯片或者北斗芯片获取的经纬度为WGS84*** 地理坐标系，为什么不统一用WGS84地理坐标系这就是国家地理测绘总局对于出版地图的要求，出版地图必须符合GCJ02坐标系标准了，也就是国家规定不能直接使用WGS84地理坐标系。所以定位大家感觉不准确很多又叫出版地图为火星地图其实只是坐标系不一样而已。

这就是为什么设备采集的经纬度在地图上显示的时候经常有很大的偏差，远远超出民用GPS 10米偏移量的技术规范，于是我们就有了谷歌地图纠偏 腾讯搜搜纠偏 混合地图纠偏 百度谷歌互转存在的价值。

那如何对谷歌地图纠偏、搜搜soso地图纠偏或者对百度地图纠偏呢，如果用算法目前没有太好的算法直接转换，所以大家采用的都是比对的方法吧地球划分成若干个小块找到地图的偏差量记录下来，然后根据任意经纬度找寻最接近的偏差量加上偏差量就可以实现不同地图之间的经纬度转换。现在有0.01度纠偏经纬度信息，可以提供任意格式，可以直接把经纬度偏移量调整回来。

百度地图纠偏信息包含中国海域一共29,699,997条纠偏数据，谷歌地图只包含中国陆地一共12,597,551条纠偏数据，基站数据移动和联通的共340万数据。

移动联通基站数据字段说明： MCC：国家 （460是中国） MNC：0是移动，1是联通 LAC：小区号 CELL：基站号 LNG：纬度 LAT：经度 O_LNG：纠偏后的纬度（用于google地图显示） O_LAT：纠偏后的经度（用于google地图显示）PRECISION：基站半径范围单位米 ADDRESS：详细地址中文描述 REGION：省份 CITY：城市 COUNTRY：国家

经研究发现，百度地图的坐标系为BD09，高德地图坐标为GCJ02，这样就存在不同坐标系的坐标之间转换的问题了，查api吧，然后又发现无论百度地图还是高德地图，api列表里都没有提这个事情。

而因为我是展示的百度地图，有要获取百度地图上的中心点的经纬度然后在作为参数调用高德地图api的需求，而百度地图并未提供bd09坐标系转出的api(也可以理解，因为如果这样的话，相当于没加密啊，自己将加密算法写出来，再给个解密的api不是有毛病么，不能不把国家的规定放眼里嘛，百度也说有深层次的需求要以公司名义给他们发邮件什么的，但是一般来说一个小iOS项目客户不会那么兴师动众，而且据群众反映，邮件的效果也不怎么好)，所以一时做了罢。

但是柳暗花明又一村了，虽然无法将百度地图上的任意点转为gcj02坐标系的点，但是百度地图还是在他们的定位api里提供了方法，使得应用在获取当前位置的时候，可以获取以“gcj02”为坐标系的点：

这样以来，就可以用高德地图获取位置信息了，虽然说只能有当前位置这一个点是取成gcj02坐标的点是比较囧的o(╯□╰)o ，还有，别忘了，取得的当前点要转化成bd09的坐标系之后，再展示在百度地图上，不然是会有偏差的。

另外比较一下百度地图和高德地图(因为害怕谷歌地图在大陆地区的服务受限问题等等，所以没考虑使用谷歌地图，也就没怎么研究)。

百度地图在页面上的展示方面做的还是很好的，包括页面的缩放，信息的标注等等，相比之下高德地图就会在某些安卓版本的某些机器上出现在放缩的时候地图信息展示的不够清晰不够明确的情况，而且在定位时，百度的地位相对准确，因为我们公司的网络服务器不在公司办公所在地，所以高德地图有时候定位就定位到服务器的地址去了，百度从我使用至今还没出现过这样的错误。

但是百度地图在poi搜索这一块，在我看来是相对薄弱的，百度地图的poi搜索在不输入关键字的时候，是不能做模糊搜索的，而且也不能根据类型搜索(比如仅搜索饮食，搜索学校之类的)，而在高德地图里这些就做到了。而且在逆地理编码时，高德地图获取的结果是相对比百度地图更丰富的。

- WGS84坐标系：即地球坐标系，国际上通用的坐标系。

- GCJ02坐标系：即火星坐标系，WGS84坐标系经加密后的坐标系。

- BD09坐标系：即百度坐标系，GCJ02坐标系经加密后的坐标系。

- 搜狗坐标系、图吧坐标系等，估计也是在GCJ02基础上加密而成的。

*注1：百度地图使用百度坐标，支持从地球坐标和火星坐标导入成百度坐标，但无法导出。并且批量坐标转换一次只能转换20个(待验证)。*

*注2：搜狗地图支持直接显示地球坐标，支持地球坐标、火星坐标、百度坐标导入成搜狗坐标，同样，搜狗坐标也无法导出。*

### 地球坐标转为火星坐标

```objective-c
const double ee = 0.00669342162296594323;

+ (CLLocation *)transformToMars:(CLLocation *)location {
  //是否在中国大陆之外
  if ([[self class] outOfChina:location]) {
    return location;
  }

  double dLat = [[self class] transformLatWithX:location.coordinate.longitude - 105.0 y:location.coordinate.latitude - 35.0];

  double dLon = [[self class] transformLonWithX:location.coordinate.longitude - 105.0 y:location.coordinate.latitude - 35.0];

  double radLat = location.coordinate.latitude / 180.0 * M_PI;

  double magic = sin(radLat);

  magic = 1 - ee * magic * magic;

  double sqrtMagic = sqrt(magic);

  dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * M_PI);

  dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * M_PI);

  return [[CLLocation alloc] initWithLatitude:location.coordinate.latitude + dLat longitude:location.coordinate.longitude + dLon];

}
```

```objective-c
+ (BOOL)outOfChina:(CLLocation *)location {

  if (location.coordinate.longitude < 72.004 || location.coordinate.longitude > 137.8347) {
    return YES;
  }

  if (location.coordinate.latitude < 0.8293 || location.coordinate.latitude > 55.8271) {
    return YES;
  }

  return NO;

}
```

```objective-c
+ (double)transformLatWithX:(double)x y:(double)y {
  double ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x));

  ret += (20.0 * sin(6.0 * x * M_PI) + 20.0 * sin(2.0 * x * M_PI)) * 2.0 / 3.0;

  ret += (20.0 * sin(y * M_PI) + 40.0 * sin(y / 3.0 * M_PI)) * 2.0 / 3.0;

  ret += (160.0 * sin(y / 12.0 * M_PI) + 320.0 * sin(y * M_PI / 30.0)) * 2.0 / 3.0;

  return ret;

}
```

```objective-c
+ (double)transformLonWithX:(double)x y:(double)y {

  double ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x));

  ret += (20.0 * sin(6.0 * x * M_PI) + 20.0 * sin(2.0 * x * M_PI)) * 2.0 / 3.0;

  ret += (20.0 * sin(x * M_PI) + 40.0 * sin(x / 3.0 * M_PI)) * 2.0 / 3.0;

  ret += (150.0 * sin(x / 12.0 * M_PI) + 300.0 * sin(x / 30.0 * M_PI)) * 2.0 / 3.0;

  return ret;

}
```


### 火星坐标和地球坐标转换

```objective-c
// World Geodetic System ==> Mars Geodetic System（地球坐标转化为火星坐标）

+ (CLLocationCoordinate2D)WorldGS2MarsGS:(CLLocationCoordinate2D)coordinate {

  // a = 6378245.0, 1/f = 298.3

  // b = a * (1 - f)

  // ee = (a^2 - b^2) / a^2;

  const double a = 6378245.0;

  const double ee = 0.00669342162296594323;

  if (outOfChina(coordinate.latitude, coordinate.longitude))
  {

    return coordinate;

  }

  double wgLat = coordinate.latitude;

  double wgLon = coordinate.longitude;

  double dLat = transformLat(wgLon - 105.0, wgLat - 35.0);

  double dLon = transformLon(wgLon - 105.0, wgLat - 35.0);

  double radLat = wgLat / 180.0 * PI;

  double magic = sin(radLat);

  magic = 1 - ee * magic * magic;

  double sqrtMagic = sqrt(magic);

  dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);

  dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * PI);

  return CLLocationCoordinate2DMake(wgLat + dLat, wgLon + dLon);

}
```

```objective-c
// Mars Geodetic System ==> World Geodetic System（火星坐标转为地球坐标）

+ (CLLocationCoordinate2D)MarsGS2WorldGS:(CLLocationCoordinate2D)coordinate{

  double gLat = coordinate.latitude;

  double gLon = coordinate.longitude;

  CLLocationCoordinate2D marsCoor = [ALDGeocoder WorldGS2MarsGS:coordinate];

  double dLat = marsCoor.latitude - gLat;

  double dLon = marsCoor.longitude - gLon;

  return CLLocationCoordinate2DMake(gLat - dLat, gLon - dLon);

}
```
### GCJ-02(火星坐标系)和BD-09转换

```objective-c
// GCJ-02 坐标转换成 BD-09 坐标

+ (CLLocationCoordinate2D)MarsGS2BaiduGS:(CLLocationCoordinate2D)coordinate{

  double x_pi = PI * 3000.0 / 180.0;

  double x = coordinate.longitude, y = coordinate.latitude;

  double z = sqrt(x * x + y * y) + 0.00002 * sin(y * x_pi);

  double theta = atan2(y, x) + 0.000003 * cos(x * x_pi);

  double bd_lon = z * cos(theta) + 0.0065;

  double bd_lat = z * sin(theta) + 0.006;

  return CLLocationCoordinate2DMake(bd_lat, bd_lon);

}
```

```objective-c
// BD-09 坐标转换成 GCJ-02 坐标

+ (CLLocationCoordinate2D)BaiduGS2MarsGS:(CLLocationCoordinate2D)coordinate{

  double x_pi = PI * 3000.0 / 180.0;

  double x = coordinate.longitude - 0.0065, y = coordinate.latitude - 0.006;

  double z = sqrt(x * x + y * y) - 0.00002 * sin(y * x_pi);

  double theta = atan2(y, x) - 0.000003 * cos(x * x_pi);

  double gg_lon = z * cos(theta);

  double gg_lat = z * sin(theta);

  return CLLocationCoordinate2DMake(gg_lat, gg_lon);

}
```

## 更多

- *[腾讯地图&百度地图&高德地图转换](https://www.jianshu.com/p/4387d0a077bd0) * 
- *[国内各地图API坐标系统比较与转换(做LBS的朋友请转](https://www.jianshu.com/p/0fe30fcd4ae7)*
- *[国内地图坐标系介绍及常见地图（百度、高德、凯立德）之间的坐标系转换 JAVA](https://www.jianshu.com/p/260ae49ef38b)*
- *[Google地图百度地图GPS经纬度偏移转换(JAVA)](https://my.oschina.net/Thinkeryjgfn/blog/402565)*