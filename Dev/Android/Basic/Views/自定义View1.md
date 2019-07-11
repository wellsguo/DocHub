## [自定义View 一： attr 详解](https://blog.csdn.net/qq_30552993/article/details/55258076)

### 1 res/values/attrs.xml

```xml
<?xml version="1.0" encoding="utf-8"?>  
<resources>  
    <declare-styleable name="View名称">  
        <attr name="textColor" format="color"/>  
        <attr name="textSize" format="dimension"/> 
    </declare-styleable>
</resources>
```

注意: format有以下几种类型及读取


序号 |	format取值|	format说明	|format读取
-- | --| -- | --
1	|reference	|资源ID	|attrs.getResourceId(R.styleable.***View名称_attr名称***,  默认值);
2	|color	|颜色值	|attrs.getColor(R.styleable.***View名称_attr名称***, 默认值);
3	|boolean	|布尔值	|attrs.getBoolean(R.styleable.***View名称_attr名称***, 默认值);
4	|dimension|	尺寸值	|attrs.getDimension(R.styleable.***View名称_attr名称***, 默认值);
5	|float	|浮点值	|attrs.getFloat(R.styleable.***View名称_attr名称***, 默认值);
6	|integer	|整型值	|attrs.getInteger(R.styleable.***View名称_attr名称***, 默认值);
7	|string	|字符串	|attrs.getString(R.styleable.***View名称_attr名称***);
8	|fraction	|百分比（%）	|attrs.getString(R.styleable.***View名称_attr名称***);
9	|enum	|枚举值	|attrs.getInt(R.styleable.***View名称_attr名称***, 默认值);
10	|flag	|位或运算	|attrs.getInt(R.styleable.***View名称_attr名称****, 默认值);

### 2 Found item Attr/xxx more than one time

（1）在 attr 中不同 View 引用相同属性名字（**textColor**）

```xml
<?xml version="1.0" encoding="utf-8"?>  
<resources>  
    <declare-styleable name="View名称">  
        <attr name="textColor" format="color"/>  
        <attr name="textSize" format="dimension"/> 
    </declare-styleable>
    <declare-styleable name="View2名称">  
        <attr name="textColor" format="color"/>  
        <attr name="hint" format="reference" />
    </declare-styleable>
</resources>
```

（2）错误提示

```
Error:Execution failed for task ':包路径:mergeReleaseResources'.
> 本地包路径\src\main\res\values\attrs.xml: Error: Found item Attr/textColor more than one time
```

（3）解决方式

```xml
<?xml version="1.0" encoding="utf-8"?>  
<resources>  
    <attr name="textColor" format="color"/> 
    <declare-styleable name="View名称">  
        <attr name="textColor"/>  
        <attr name="textSize" format="dimension"/> 
    </declare-styleable>
    <declare-styleable name="View2名称">  
        <attr name="textColor"/>  
        <attr name="hint" format="reference" />
    </declare-styleable>
</resources>
```

### 3 enum / flag

（1）下面就列举 flag (enum也类似)

```xml
<declare-styleable name = "View名称">
    <attr name="inputType">
        <flag name = "text" value = "0" />
        <flag name = "number" value = "1" />
        <flag name = "textPassword" value = "2" />
        <flag name = "numberPassword" value = "3" />
        <flag name = "numberDecimal" value = "4" />
    </attr>
</declare-styleable>
```

（2）这里是我在自定义一个EditText的时候，为了设置输入内容的类型

> 调用方法

```java
setInputType(attrs.getInt(R.styleable.View名称_inputType, 0));
```

```java
public void setInputType(int type) {
    switch (type) {
        case 0:
            mEditText.setInputType(InputType.TYPE_CLASS_TEXT);
            break;
        case 1:
            mEditText.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_NORMAL);
            break;
        case 2:
            mEditText.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
            break;
        case 3:
            mEditText.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD);
            break;
        case 4:
            mEditText.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL);
            break;
    }
}
```

### 4 属性的定义与使用

（1）属性定义

```xml
<declare-styleable name = "名称">
    <attr name = "itemTextColor" format = "color" />
</declare-styleable>
```

（2）属性使用

```xml
<TextView
    android:layout_width = "42dip"
    android:layout_height = "42dip"
    android:itemTextColor = "#00FF00"/>
```
