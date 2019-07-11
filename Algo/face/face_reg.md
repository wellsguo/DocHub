### OpenCV人脸识别的原理 

```c++
void GetImageRect(IplImage* orgImage, CvRect rectInImage, IplImage* imgRect,double scale)
{
	//从图像orgImage中提取一块（rectInImage）子图像imgRect
	IplImage *result=imgRect;
	CvRect size;
	size.x=rectInImage.x*scale;
	size.y=rectInImage.y*scale;
	size.width=rectInImage.width*scale;
	size.height=rectInImage.height*scale;
	
	//result=cvCreateImage( size, orgImage->depth, orgImage->nChannels );
	//从图像中提取子图像
	cvSetImageROI(orgImage,size);
	cvCopy(orgImage,result);
	cvResetImageROI(orgImage);
}
```

#### 人脸预处理

现在你已经得到一张人脸，你可以使用那张人脸图片进行人脸识别。然而，假如你尝试这样简单地从一张普通图片直接进行人脸识别的话，你将会至少**损失10%的准确率**！

在一个人脸识别系统中，应用多种预处理技术对将要识别的图片进行标准化处理是极其重要的。多数人脸识别算法对光照条件十分敏感，所以假如在暗室训练，在明亮的房间就可能不会被识别出来等等。这个问题可归于“lumination dependent”，并且还有其它很多例子，比如脸部也应当在图片的一个十分**固定的位置（比如眼睛位置为相同的像素坐标），固定的大小，旋转角度，头发和装饰，表情（笑，怒等），光照方向（向左或向上等）**，这就是在进行人脸识别前，使用好的图片预处理过滤器十分重要的原因。你还应该做一些其它事情，比如去除脸部周围的多余像素（如用椭圆遮罩，只显示其内部的人脸区域而不是头发或图片背景，因为他们的变化多于脸部区域）。

为简单起见，我展示给你的人脸识别系统是使用灰度图像的特征脸方法。所以我将向你说明怎样简单地把彩色图像转化为灰度图像，并且之后简单地使用直方图均衡化（Histogram Equalization）作为一种自动的标准化脸部图像亮度和对比度的方法。为了得到更好的结果，你可以使用彩色人脸识别(color face recognition,ideally with color histogram fitting in HSV or another color space instead of RGB)，或者使用更多的预处理，比如边缘增强(edge enhancement),轮廓检测(contour detection),手势检测(motion detection),等等。

你可以看到一个预处理阶段的例子：

![pre-process](http://www.myexception.cn/img/2012/07/18/144432261.jpg)

这是把一幅RGB格式的图像或灰度图像转变为灰度图像的基本代码。它还把图像调整成了固定的维度，然后应用直方图均衡化来实现固定的亮度和对比度。

#### PCA原理
现在你已经有了一张经过预处理后的脸部图片，你可以使用特征脸(PCA)进行人脸识别。OpenCV自带了执行PCA操作的”cvEigenDecomposite()”函数，然而你需要一个图片数据库(训练集)告诉机器怎样识别当中的人。

所以你应该收集每个人的一组预处理后的脸部图片用于识别。比如，假如你想要从10人的班级当中识别某个人，你可以为每个人存储20张图片，总共就有200张大小相同(如100×100像素)的经预处理的脸部图片。

特征脸的理论在Servo Magazine的两篇文章(Face Recognition with Eigenface)中解释了，但我仍会在这里尝试着向你解释。

我们使用“主元分析”把你的200张训练图片转换成一个代表这些训练图片主要区别的“特征脸”集。首先它将会通过获取每个像素的平均值，生成这些图片的“平均人脸图片”。然后特征脸将会与“平均人脸”比较。第一个特征脸是最主要的脸部区别，第二个特征脸是第二重要的脸部区别，等……直到你有了大约50张代表大多数训练集图片的区别的特征脸。

![eigenface1](http://www.myexception.cn/img/2012/07/18/144432262.jpg)
![eigenface2](http://www.myexception.cn/img/2012/07/18/144432263.jpg)
![eigenface3](http://www.myexception.cn/img/2012/07/18/144432264.jpg)

在上面这些示例图片中你可以看到平均人脸和第一个以及最后一个特征脸。注意到，平均人脸显示的是一个普通人的平滑脸部结构，排在最前的一些特征脸显示了一些主要的脸部特征，而最后的特征脸（比如Eigenface 119）主要是图像噪声。你可以在下面看到前32张特征脸。

![eigenfacex](http://www.myexception.cn/img/2012/07/18/144432265.jpg)

简单地说，特征脸方法(Principal Component Analysis)计算出了训练集中图片的主要区别，并且用这些“区别”的组合来代表每幅训练图片。
比如，一张训练图片可能是如下的组成：
$(averageFace) + (13.5\%\ of\ eigenface0) – (34.3\%\ of\ eigenface1) + (4.7\%\ of\ eigenface2) + … + (0.0\%\ of\ eigenface199)$.

一旦计算出来，就可以认为这张训练图片是这200个比率(ratio)：
$\{13.5, -34.3, 4.7, …, 0.0\}$.

用特征脸图片分别乘以这些比率，并加上平均人脸图片 (average face)，从这200个比率还原这张训练图片是完全可以做到的。但是既然很多排在后面的特征脸是图像噪声或者不会对图片有太大作用，这个比率表可以被降低到只剩下最主要的,比如前30个，不会对图像质量有很大影响。所以现在可以用30个特征脸，平均人脸图片，和一个含有30个比率的表，来代表全部的200张训练图片。

在另一幅图片中识别一个人，可以应用相同的PCA计算，使用相同的200个特征脸来寻找200个代表输入图片的比率。并且仍然可以只保留前30个比率而忽略其余的比率，因为它们是次要的。然后通过搜索这些比率的表，寻找在数据库中已知的20个人，来看谁的前30个比率与输入图片的前30个比率最接近。这就是寻找与输入图片最相似的训练图片的基本方法，总共提供了200张训练图片。

#### 训练图片
创建一个人脸识别数据库，就是训练一个列出图片文件和每个文件代表的人的文本文件，形成一个facedata.xml“文件。
比如，你可以把这些输入一个名为”trainingphoto.txt”的文本文件：
```
joke1.jpg
joke2.jpg
joke3.jpg
joke4.jpg
lily1.jpg
lily2.jpg
lily3.jpg
lily4.jpg
```
它告诉这个程序，第一个人的名字叫“joke，而joke有四张预处理后的脸部图像，第二个人的名字叫”lily”，有她的四张图片。这个程序可以使用”loadFaceImgArray()”函数把这些图片加载到一个图片数组中。

为了从这些加载好的图片中创建一个数据库，你可以使用OpenCV的”cvCalcEigenObjects()”和”cvEigenDecomposite()”函数。

获得特征空间的函数：
```c++
void cvCalcEigenObjects(int nObjects, void* input, 
    void* output, int ioFlags, int ioBufSize, 
    void* userData,CvTermCriteria* calcLimit,
    IplImage* avg, float* eigVals);
```
+ nObjects：目标的数目，即输入训练图片的数目。
+ input：输入训练的图片。
+ output：输出特征脸，总共有nEigens
+ ioFlags、ioBufSize：默认为0
+ userData：指向回调函数(callback function)必须数据结构体的指针。
+ calcLimit：终止迭代计算目标特征的条件。根据calcLimit的参数，计算会在前nEigens主要特征目标被提取后结束（这句话有点绕，应该就是提取了前nEigens个特征值），另一种结束的情况是：目前特征值同最s大特征值的比值降至calcLimit的epsilon值之下。
赋值如下calcLimit = cvTermCriteria( CV_TERMCRIT_ITER, nEigens, 1);
它的类型定义如下：
```c++
typedef struct CvTermCriteria
{
　　int type;　　
      int max_iter;　　　　// 最大迭代次数
　　double epsilon;　　　// 结果精确性
}
```
+ avg：训练样本的平均图像
+ eigVals：以降序排列的特征值的行向量指针。可以为0。

最后将所得数据形成一个facedata.xml“文件保存下来，它可以随时被重新载入来识别经训练过的人。

图像在特征空间的投影：

```c++
void cvEigenDecomposite( IplImage* obj, int nEigObjs, void* eigInput,int ioFlags, void* userData, IplImage* avg, float* coeffs );  
```
+ obj：输入图像，训练或识别图像
+ nEigObjs：特征空间的eigen数量
+ eigInput：特征空间中的特征脸
+ ioFlags、userData：默认为0
+ avg：特征空间中的平均图像
+ coeffs：这是唯一一个输出，即人脸在子空间的投影，特征值

#### 识别的过程

1. 读取用于测试的图片。

2. 平均人脸，特征脸和特征值（比率）使用函数“loadTrainingData()” 从人脸识别数据库文件（the face recognition database fil）“facedata.xml”载入。

3. 使用OpenCV的函数“cvEigenDecomposite()”，每张输入的图片都被投影到PCA子空间，来观察哪些特征脸的比率最适合于代表这张图片。

4. 现在有了特征值（特征脸图片的比率）代表这张输入图片，程序需要查找原始的训练图片，找出拥有最相似比率的图片。这些用数学的方法在“findNearestNeighbor()”函数中执行，采用的是“欧几里得距离（Euclidean Distance）”，但是它只是基本地检查输入图片与每张训练图片的相似性，找到最相似的一张：一张在欧几里得空间上与输入图片距离最近的图片。就像在 Servo Magazine的文章上提到的那样，如果使用马氏距离（ the Mahalanobis space，需要在代码里定义 USE_MAHALANOBIS_DISTANCE），你可以得到更准确的结果。

5. 在输入图片与最相似图片之间的距离用于确定可信度（confidence）,作为是否识别出某人的指导。1.0的可信度意味着完全相同，0.0或者负的可信度意味着非常不相似。但是需要注意，我在代码中用到的可信度公式只是一个非常基本的可信度测量，不是很可靠，但是我觉得多数人会想要看到一个粗略的可信度值。你可能发现它对你的图片给出错误的值，所以你可以禁用它（比如：把可信度设为恒定的1.0）。

一旦指导哪张训练图片和输入图片最相似，并假定可信度值不是太低（应该至少是0.6或更高），那么它就指出了那个人是谁，换句话说，它识别出了那个人！