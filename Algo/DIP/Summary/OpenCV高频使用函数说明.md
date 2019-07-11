## 二值化
  
> 就是将图像上的像素点的灰度值设置为0或255，也就是将整个图像呈现出明显的只有黑和白的视觉效果，便于接下来的操作。

### 函数声明

```c++
double threshold(InputArray src, OutputArray dst, double thresh, double maxval, int type)
```

- 第一个参数，InputArray类型的src，输入数组，填单通道 , 8或32位浮点类型的Mat即可。

- 第二个参数，OutputArray类型的dst，函数调用后的运算结果存在这里，即这个参数用于存放输出结果，且和第一个参数中的Mat变量有一样的尺寸和类型。

- 第三个参数，double类型的thresh，阈值的具体值。

- 第四个参数，double类型的maxval，当第五个参数阈值类型type取 THRESH_BINARY 或THRESH_BINARY_INV阈值类型时的最大值.

- 第五个参数，int类型的type，阈值类型,。

	其它参数很好理解，我们来看看第五个参数，第五参数有以下几种类型

	 - 0: THRESH_BINARY  当前点值大于阈值时，取Maxval,也就是第四个参数，下面再不说明，否则设置为0

	 - 1: THRESH_BINARY_INV 当前点值大于阈值时，设置为0，否则设置为Maxval

	 - 2: THRESH_TRUNC 当前点值大于阈值时，设置为阈值，否则不改变

	 - 3: THRESH_TOZERO 当前点值大于阈值时，不改变，否则设置为0

	 - 4: THRESH_TOZERO_INV  当前点值大于阈值时，设置为0，否则不改变

## 形态学操作

> 用来消除噪声的影响

### 函数声明

```c++
void morphologyEx(InputArray src, OutputArray dst, 
                  int op, InputArray kernel, 
                  Point anchor=Point(-1,-1), intiterations=1, 
                  int borderType=BORDER_CONSTANT, 
                  const Scalar& borderValue=morphologyDefaultBorderValue());
```

- 第一个参数，InputArray类型的src，输入图像，即源图像，填Mat类的对象即可。图像位深应该为以下五种之一：CV_8U, CV_16U,CV_16S, CV_32F 或CV_64F。

- 第二个参数，OutputArray类型的dst，即目标图像，函数的输出参数，需要和源图片有一样的尺寸和类型。

- 第三个参数，int类型的op，表示形态学运算的类型，可以是如下之一的标识符：

   - MORPH_OPEN – 开运算（Opening operation）
   - MORPH_CLOSE – 闭运算（Closing operation）
   - MORPH_GRADIENT -形态学梯度（Morphological gradient）
   - MORPH_TOPHAT - “顶帽”（“Top hat”）
   - MORPH_BLACKHAT - “黑帽”（“Black hat“）

- 第四个参数，InputArray类型的kernel，形态学运算的内核。若为NULL时，表示的是使用参考点位于中心3x3的核。我们一般使用函数 getStructuringElement配合这个参数的使用。getStructuringElement函数会返回指定形状和尺寸的结构元素（内核矩阵）。

- 第五个参数，Point类型的anchor，锚的位置，其有默认值（-1，-1），表示锚位于中心。

- 第六个参数，int类型的iterations，迭代使用函数的次数，默认值为1。

- 第七个参数，int类型的borderType，用于推断图像外部像素的某种边界模式。注意它有默认值BORDER_ CONSTANT。

- 第八个参数，const Scalar&类型的borderValue，当边界为常数时的边界值，有默认值morphologyDefaultBorderValue()，一般不管。

> java

```java
Mat element2 = Imgproc.getStructuringElement(Imgproc.MORPH_RECT, new Size(5, 5));
Imgproc.erode(gray, gray, element2);
Imgproc.dilate(mGrayMat, mGrayMat, element2);
```

## Android opencv 直线检测

```java
Mat lines = new Mat();
Imgproc.HoughLines(canny, lines, 1, Math.PI / 180.0, 20);
float[] data = new float[2];
for (int i = 0; i < lines.rows(); i++){
    lines.get(i, 0, data);
    float rho =  data[0], theta = data[1];
    double a = Math.cos(theta), b = Math.sin(theta);
    double x0 = a * rho, y0 = b * rho;

    Point pt1 = new Point();
    Point pt2 = new Point();

    pt1.x = Math.round(x0 + 100* (-b));
    pt1.y = Math.round(y0 + 100* (a));
    pt2.x = Math.round(x0 + 100* (-b));
    pt2.y = Math.round(y0 + 100* (a));

    Imgproc.line(cannyCopy, pt1, pt2, new Scalar(255, 255, 0), 1, Imgproc.LINE_AA, 0);
}

```
