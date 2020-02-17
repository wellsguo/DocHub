[CSS里常见的块级元素和行内元素](https://www.cnblogs.com/kenshinobiy/p/8551798.html)

根据 `CSS` 规范的规定，每个网页元素都有一个 `display` 属性，用于确定该元素的类型，且每个元素都有默认的display属性值，比如, `div` 默认 `display` 属性值为 `block`，称为`块级元素`；而 `span` 默认 `display` 属性值为 `inline`，称为`行内元素`。

`div` 这样的块级元素，就会自动占据一定矩形空间，可以通过设置高度、宽度、内外边距等属性，来调整的这个矩形的样子；与之相反，像`span` `a` 这样的行内元素，则没有自己的独立空间，它是依附于其他块级元素存在的。因此，对行内元素设置高度、宽度、内外边距等属性，都是无效的。

## Block Element

> 特征

1. 每个块级元素都是独自占一行，其后的元素也只能另起一行，==不能两个元素共用一行==。

2. 元素的高度、宽度、行高和顶底边距都是可以设置的。

3. 元素的宽度如果不设置的话，默认为父元素的宽度。

4. 块级元素对应属性 `display：block`；



> 全部元素列表

* h1 ~ h6  & hr & div & table &  form & fieldset(form控制组)
* p  & pre  & ul & ol & dl 
* address - 地址
* blockquote - 块引用
* center - 举中对齐块
* dir - 目录列表
* isindex - input prompt
* menu - 菜单列表
* noframes - frames可选内容，（对于不支持frame的浏览器显示此区块内容
* noscript - ）可选脚本内容（对于不支持script的浏览器显示此内容）


## Inline Element

> 特征



1. 可以和其他元素处于一行，==不用必须另起一行==。

2. 元素的高度、宽度及顶部和底部边距不可设置。

3. ==元素的宽度就是它包含的文字、图片的宽度，不可改变==。

4. 行内元素对应属性 `display：inline`；



> 元素列表

* a - 锚点
* abbr - 缩写
* acronym - 首字
* b - 粗体(不推荐)
* bdo - bidi override
* big - 大字体
* br - 换行
* cite - 引用
* code - 计算机代码(在引用源码的时候需要)
* dfn - 定义字段
* em - 强调
* font - 字体设定(不推荐)
* i - 斜体
* img - 图片
* input - 输入框
* kbd - 定义键盘文本
* label - 表格标签
* q - 短引用
* s - 中划线(不推荐)
* samp - 定义范例计算机代码
* select - 项目选择
* small - 小字体文本
* span - 常用内联容器，定义文本内区块
* strike - 中划线
* strong - 粗体强调
* sub - 下标
* sup - 上标
* textarea - 多行文本输入框
* tt - 电传文本
* u - 下划线
* var - 定义变量

## 可变元素
可变元素为根据上下文语境决定该元素为块元素或者内联元素。

* applet - java applet
* ==button - 按钮==
* del - 删除文本
* iframe - inline frame
* ins - 插入的文本
* ==map - 图片区块(map)==
* object - object对象
* script - 客户端脚本



## 块级元素与行级元素互转

> 如果想将块级元素与行级元素相互转换，该怎么办呢？

用 `display:inline`将块级元素设为行级元素。同样，也可以用`display:block`将行级元素设为块级元素。

> 如果想设置高度、宽度、行高以及顶和底边距，又想元素处于一行，该怎么办呢？

用`display:inline-block`将元素设置为`行级块元素`。

