
### 1.1 引言

**传统光学字符识别** 主要面向高质量的文档图像，此类技术假设输入图像背景干净、字体简单且文字排布整齐，在符合要求的情况下能够达到很高的识别水平。

与文档文字识别不同，**自然场景中的文字识别** 图像背景复杂、分辨率低下、字体多样、分布随意等，传统光学字符识别在此类情况下无法应用。

**图像理解** 仅利用一般的视觉元素（如太阳、大海、山、天空等）及其相互关系，容易缺乏足够的上下文信息约束，难以准确推导出图像所代表的含义，与一般的视觉元素不同，文字包含了丰富的高层语义信息。

### 1.2 相关技术及研究现状

#### 1.2.1 自然场景文字处理流程

主要包括文字检测与文字识别。

- 文字检测的主要功能为：从图像中找到文字区域，并将文字区域从原始图像中分离出来

- 文字识别的主要功能为：从分离出来的图像上，进行文字识别

> **文字识别流程**

- 1）预处理：去噪（滤波算法）、图像增强、缩放，其目的是去除背景或者噪点，突出文字部分，并缩放图片为适于处理的大小

- 2）特征抽取：常用特征：边缘特征、笔画特征、结构特征

- 3）识别：分类器，随机森林 、SVM、NN

![](https://img-blog.csdn.net/20170527110000314?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQveGlhb2ZlaTA4MDE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

#### 1.2.2 自然场景文字识别的困难与挑战

文字背景异常复杂、文字类型丰富、分布随意、字符分割困难、噪音严重

#### 1.2.3 自然场景文字识别的研究现状

基于字符的识别和基于整个单词的识别

##### 1.2.3.1 基于字符的识别

*Strokelets: A Learned Multi-scale Representation for Scene Text Recognition（CVPR 2014）* 通过聚类图像块来学习中层笔画特征，然后使用霍夫（HOG）投票算法检测字符。在笔画特征和HOG特征的基础上，使用随机森林分类器来进行字符分类。

*End-to-end scene text recognition（2011）* 借鉴计算机视觉通用的目标检测方法，提出了一个新的文本识别系统。他们利用字符置信度以及字符之间的空间约束关系，给出最可能的检测和识别结果。但是该算法只能用于水平方向排列的文本的检测识别。

*End-to-End Text Recognition with Hybrid HMM Maxout Models（2013）* 和 * PhotoOCR: Reading Text in Uncontrolled Conditions（2013）* 等人通过无监督的二分类技术或有监督的分类器，将单词图像分割为潜在的字符区域。

*End-to-End Text Recognition with Hybrid HMM Maxout Models（2013）* 使用一种复杂的，包含分割、矫正以及字符识别的CNN网络，结合使用固定词典的隐马尔科夫模型（HMM），生成最终的识别结果。

*PhotoOCR* 系统使用基于HOG特征的神经网络分类器，对分割得到的候选结果进行打分，使用结合N元语言模型（N-gram）的Beam搜索算法，得到候选字符集合。最后，再进一步使用语言模型和形状模型对候选字符组合进行重新排序。

*Deep Features for Text Spotting（2014）* 结合了文本一非文本分类器、字符分类器、二元语言模型分类器，对整张图进行稠密的基于滑动窗口的扫描。最后结合固定词典，对图片中的单词进行分析。
 基于字符的识别技术依赖于使用字符分类器对图像进行逐字符识别，最终将识别得到的字符进行集成，得到图像中的整个单词。

##### 1.2.3.2 基于整个单词的识别

*Scene Text Recognition using Higher Order Language Priors* 以及 *Large-Lexicon Attribute-Consistent Text Recognition in Natural Images* 的工作依旧依赖于显式的字符分类器，但是通过构建一个图结构来推导整个单词。这会遇到和基于字符识别方法类似的困难。

*Whole is Greater than Sum of Parts: Recognizing Scene Text Words（2013）* 使用整张文字图片来识别单词:他们使用基于梯度的特征图与预先制作好的单词图像进行对比，利用动态k近邻来判断当前图片所包含的单词。该方法依赖于一个固定词典以及预先生成的单词图片。

*Label embedding for text recognition（2013）* 使用集成的Fisher向量以及结构化的支持向量机框架来建立图片和整个单词编码的关系。

*Word Spotting and Recognition with Embedded Attributes（2014）* 进一步探索了单词编码的概念，他们为图片和单词字符串创建了一个编码空间。这其实是 *Supervised mid-level features for word image representation（2014）* 方法的扩展:显式利用字符级别的训练数据来学习中间特征。

*Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks（2013）* 等人使用深度CNN对整张图片进行编码，并使用多个位置敏感的字符级分类器来进行文字识别。他们在街景门牌号识别任务中取得了极大的成功。他们还将该模型应用到长达8位的验证码识别任务上，并使用了合成的训练数据对模型进行
训练。该方法在google街景门牌号识别任务中获得了96%以上的识别率。同时还在对goggle验证码识别任务中获得了99%以上的识别率。

*Synthetic Data and Artificial Neural Networks for Natural Scene Text Recognition（2014）* 和 *Reading Text in the Wild with Convolutional Neural Networks（2014）* 对上述模型做了细微变动:取消了预测字符长度的分类器，并引入了结束符表示文字结尾。他们随后证明了，使用合成的训练数据训练出的模型，能够成功应用到现实世界的识别问题中。将单词编码为向量是一种可行的词典单词识别方法，但是在无约束情况下，字符之间可以任意组合。当字符数量足够多时，基于固定长度向量编码的方法性能会显著下降。

**但是依然存在一些不足** :一些研究将深度学习技术用于单个字符的识别步骤中，但整体框架依旧遵循传统处理流程设计，因此在其它步骤中依旧会遇到绪论所述问题。Goodfellow 等人的研究使用纯神经网络直接完成整个识别流程，取得了业界领先的成绩。但是由于他们需要使用固定大小的图像作为输入，并且将输入图像编码为固定长度的特征向量，在图片中字符较多的情况下，模型的识别精度会显著下降。另一方面，由于他们的模型没有对图片进行显式地字符定位和分割，因此无法得知每个字符在原图中所处位置。

#### 1.2.4 现有方法存在的问题

- 1）**大多文字识别方法依赖于人工定义的特征**  
虽然有大量工作研究如何定义一组好的文字特征，但是大部分实际应用的特征都不具有通用性。在极端情况下（如图1.3 a），很多特征几乎无效或甚至无法提取，如笔画特征，形状特征，边缘特征等。另一方面，定义和提取人工特征也是一件极为耗时耗力的工作。

- 2）**脱离上下文的字符识别易造成显著的歧义**  
基于字符的识别方法通常以字符为处理单位，通过分割或者滑动窗口搜索的方法，将单个字符进行分离。然后利用字符分类器来预测字符分类。然而，在复杂情况下，字符的分割非常困难，而强行分割则会破坏字符结构。另外，符的识别需要上下文的参与，如图1.3(b)所示。该图中的单词为defence，若将d、f、 n分离后再进行字符识别，识别成功率会明显下降。


- 3) **简单的单词整体识别有着较大的局限性**  
基于整个单词的识别方法直接从整幅图片中提取特征，然后进行识别。然而， 该类方法面可能临以下三个问题:  
  - a) *难以应对无约束情况下的识别* 。多个字符的组合不一定形成字典中的单词，有很多时候，图像中的文字由随机字符组成(如产品型号、验证码、商标名称)。以单词为单位进行识别的方法无法应对此类情况。  
   - b) *长字符串识别正确率显著下降* 。当字符数量增多时(如20个左右)，图片的情况会变得更为复杂，一些整体识别方法的性能会显著下降。  
   - c) *缺乏字符定位功能* 。很多时候，文字识别不仅仅需要了解图像中包含的 文字内容，还需要了解每个字符在原图中的位置。基于字符的识别方法天然带有字符定位功能。而有些整体识别的方法则缺失了此类性质。如 Goodfellow等人的整体识别方法。
 
- 4) **训练样本制作繁琐**  
不少算法的训练依赖于详细的训练样本标注结果:不仅需要知道每张训练样本中包含的文字，还需要知道每个文字所处的位置。有些算法还需要结合切分好的单字符训练样本、多字符训练样本。有些算法为了进行文字区域非文字区域检测，还需要制作包含文字的正例样本和反例样本。为了获得良好的机器学习效果，大部分的机器学习算法都要求尽量使用丰富、大量、贴近真实世界的样本进行训练。因此，对样本制作要求苛刻的识别算法会加大人工工作量，进而难以通用。

### 2.1 基于深度学习的自然场景文字识别框架

#### 2.2.1问题分析

文字识别是将图像信息转化为计算机可表示和处理的符号序列的一个过程。本质上，文字识别任务可认为是一种特别的翻译过程：将图像信号翻译为“自然语言”。这与语音识别、机器翻译有着相似之处:从数学角度来看，它们都将一组包含大量噪音的输入序列，通过自动学习得到的模型，转化为一组给定标签的输出序列。  

因此，本文结合基于CNN的图像特征提取技术和基于RNN的序列翻译技术，提出了一种新的神经网络结构，用于自然场景文字识别任务，以达到以下两个目标:  
(1) 使用自动学习的、结合上下文的特征取代人工定义的特征;  
(2) 避免字符分割问题，实现端到端的无约束字符定位和识别。  

### 2.2.2 框架介绍

**大量的标注问题都可以使用编码器解码器结构进行建模。** 标注任务根据输入输出通常可以分为四种转换模式:向量到向量、向量到序列、序列到向量以及序列到序列。如对一组特征进行分类可以认为是向量到向量转换、英文到中文的机器翻译则是序列到序列转换、对句子分类则可以建模为序列到向量的转换。

### 3.1 基于CNN和BiRNN的图像编码

在确定CNN结构之后，每个神经元的感受野 也随之确定。在固定感受野中，提取的局部特征可能会造成歧义。  
**CNN提取静态局部特征，BiRNN提取上下文特征（类似Inside-Outside Network）**

![](https://img-blog.csdn.net/20170527152531644)

### 3.2 图像预处理

预处理包括三步：**转化为灰度图**、**图像灰度值归一化**、**图像缩放**  

- 图像灰度值归一化是为了增加对比度，让图像更加清晰  

- 图像缩放是因为后续步骤需要图像保持固定高度，缩放步骤会尽量保持原始图像的宽高比  

### 4.1 基于ARSG的文字解码

文字解码包括字符定位和文字识别两个部分。ARSG通过计算每个注解向量与当前输出的相关性，显式的对神经网络当前的关注点进行建模。  

基于CTC模型以及其变种的模型，如RNN翻译器，是最为接近ARSG的模型。此类模型使用动态规划技术对生成结果进行优化。

![](https://img-blog.csdn.net/20170527163840576)

![](https://img-blog.csdn.net/20170527163755684)


--------------------- 
作者：xiaofei0801    
来源：CSDN   
原文：https://blog.csdn.net/xiaofei0801/article/details/72778223   
版权声明：本文为博主原创文章，转载请附上博文链接！  