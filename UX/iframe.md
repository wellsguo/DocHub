原文链接：http://caibaojian.com/iframe-adjust-content-height.html

[JS](http://caibaojian.com/javascript/)自适应高度，其实就是设置[iframe](http://caibaojian.com/t/iframe)的高度，使其等于内嵌网页的高度，从而看不出来滚动条和嵌套痕迹。对于用户体验和网站美观起着重要作用。

如果内容是固定的，那么我们可以通过[CSS](http://caibaojian.com/css3/)来给它直接定义一个高度，同样可以实现上面的需求。当内容是未知或者是变化的时候。这个时候又有几种情况了。

### [iframe](http://caibaojian.com/t/iframe)内容未知，高度可预测

这个时候，我们可以给它添加一个默认的CSS的min-height值，然后同时使用[JavaScript](http://caibaojian.com/t/javascript)改变高度。常用的兼容代码有：

```
// document.domain = "caibaojian.com";
function setIframeHeight(iframe) {
if (iframe) {
var iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
if (iframeWin.document.body) {
iframe.height = iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight;
}
}
};

window.onload = function () {
setIframeHeight(document.getElementById('external-frame'));
};
```

**演示地址**

[演示一](http://caibaojian.com/demo/2014/2/iframe.html)（如果在同个顶级域名下，不同子域名之间互通信息，设置document.domain="caibaojian.com"[·](http://caibaojian.com/iframe-adjust-content-height.html)

只要修改以上的[iframe](http://caibaojian.com/t/iframe)的ID即可了。或者你可以直接在iframe里面写代码，我们一般为了不污染[HTML](http://caibaojian.com/t/html)代码，建议使用上面的代码。

```
<iframe src="backtop.html" frameborder="0" scrolling="no" id="external-frame" onload="setIframeHeight(this)"></iframe>
```

[演示二](http://caibaojian.com/demo/2014/2/iframe2.html)

### 多个iframe的情况下

```
<script language="javascript">
//输入你希望根据页面高度自动调整高度的iframe的名称的列表
//用逗号把每个iframe的ID分隔. 例如: ["myframe1", "myframe2"]，可以只有一个窗体，则不用逗号。
//定义iframe的ID
var iframeids=["test"];
//如果用户的浏览器不支持iframe是否将iframe隐藏 yes 表示隐藏，no表示不隐藏
var iframehide="yes";
function dyniframesize()
{
var dyniframe=new Array()
for (i=0; i<iframeids.length; i++)
{
if (document.getElementById)
{
//自动调整iframe高度
dyniframe[dyniframe.length] = document.getElementById(iframeids[i]);
if (dyniframe[i] && !window.opera)
{
dyniframe[i].style.display="block";
if (dyniframe[i].contentDocument && dyniframe[i].contentDocument.body.offsetHeight) //如果用户的浏览器是NetScape
dyniframe[i].height = dyniframe[i].contentDocument.body.offsetHeight;
else if (dyniframe[i].Document && dyniframe[i].Document.body.scrollHeight) //如果用户的浏览器是IE
dyniframe[i].height = dyniframe[i].Document.body.scrollHeight;
}
}
//根据设定的参数来处理不支持iframe的浏览器的显示问题
if ((document.all || document.getElementById) && iframehide=="no")
{
var tempobj=document.all? document.all[iframeids[i]] : document.getElementById(iframeids[i]);
tempobj.style.display="block";
}
}
}
if (window.addEventListener)
window.addEventListener("load", dyniframesize, false);
else if (window.attachEvent)
window.attachEvent("onload", dyniframesize);
else
window.onload=dyniframesize;
</script>
```

[演示三](http://caibaojian.com/demo/2014/2/iframe3.html)

### 针对知道的iframe的ID调用

```
function iframeAutoFit(iframeObj){
setTimeout(function(){if(!iframeObj) return;iframeObj.height=(iframeObj.Document?iframeObj.Document.body.scrollHeight:iframeObj.contentDocument.body.offsetHeight);},200)
}
```

[演示四](http://caibaojian.com/demo/2014/2/iframe4.html)

### 内容宽度变化的iframe高度自适应

```
<iframe src="backtop.html" frameborder="0" scrolling="no" id="test" onload="this.height=100"></iframe>
<script type="text/javascript">
function reinitIframe(){
var iframe = document.getElementById("test");
try{
var bHeight = iframe.contentWindow.document.body.scrollHeight;
var dHeight = iframe.contentWindow.document.documentElement.scrollHeight;
var height = Math.max(bHeight, dHeight);
iframe.height = height;
console.log(height);
}catch (ex){}
}
window.setInterval("reinitIframe()", 200);
</script>
```

[演示五](http://caibaojian.com/demo/2014/2/iframe5.html)

打开调试运行窗口可以看到运行。

### 跨域下的iframe自适应高度

跨域的时候，由于js的同源策略，父页面内的js不能获取到iframe页面的高度。需要一个页面来做代理。
 方法如下：假设www.a.com下的一个页面a.html要包含www.b.com下的一个页面c.html。
 我们使用www.a.com下的另一个页面agent.html来做代理，通过它获取iframe页面的高度，并设定iframe元素的高度。

a.html中包含iframe:

```
<iframe src="http://www.b.com/c.html" id="Iframe" frameborder="0" scrolling="no" style="border:0px;"></iframe>
```

在c.html中加入如下代码：

```
<iframe id="c_iframe"  height="0" width="0"  src="http://www.a.com/agent.html" style="display:none" ></iframe>
<script type="text/javascript">
(function autoHeight(){
var b_width = Math.max(document.body.scrollWidth,document.body.clientWidth);
var b_height = Math.max(document.body.scrollHeight,document.body.clientHeight);
var c_iframe = document.getElementById("c_iframe");
c_iframe.src = c_iframe.src + "#" + b_width + "|" + b_height;  // 这里通过hash传递b.htm的宽高
})();
</script>
```

最后，agent.html中放入一段js:

```
//code from http://caibaojian.com/iframe-adjust-content-height.html
<script type="text/javascript">
var b_iframe = window.parent.parent.document.getElementById("Iframe");
var hash_url = window.location.hash;
if(hash_url.indexOf("#")>=0){
var hash_width = hash_url.split("#")[1].split("|")[0]+"px";
var hash_height = hash_url.split("#")[1].split("|")[1]+"px";
b_iframe.style.width = hash_width;
b_iframe.style.height = hash_height;
}
</script>
```

agent.html从URL中获得宽度值和高度值，并设置iframe的高度和宽度（因为agent.html在www.a.com下，所以操作a.html时不受[JavaScript](http://caibaojian.com/t/javascript)的同源限制）

[演示六](http://caibaojian.com/demo/2014/2/iframe6.html)

相关文章：

[postMessage+window.name实现跨域iframe高度自适应兼容版](http://caibaojian.com/postmessage-windowname.html)

[postMessage+window.name实现iframe跨域通信jquery兼容版](http://caibaojian.com/jquery-postmessage-window-name.html)

##### 文章目录

- [iframe内容未知，高度可预测](#t1)
- [多个iframe的情况下](#t2)
- [针对知道的iframe的ID调用](#t3)
- [内容宽度变化的iframe高度自适应](#t4)
- [跨域下的iframe自适应高度](#t5)

####  [iframe](http://caibaojian.com/t/iframe),[JavaScript](http://caibaojian.com/t/javascript) 推荐文章

- #### [跨浏览器使用javascript/jQuery获取iframe的内容](http://caibaojian.com/283.html)

  iframe是内联框架，允许你单独的HTML文件加载到一个现有的文件。您还可以加载文件的动态“src”属性。假设有一个需要iframe内容和过程使用JavaScript。下面的例子可以帮助你做，这已经是一个跨浏览器Firefox和IE浏览器 ...

- #### [js对iframe内外（父子）页面进行操作](http://caibaojian.com/js-get-iframe.html)

  怎么对iframe进行操作，1.在iframe里面控制iframe外面的js代码。2.在父框架对子iframe进行操作。


来源：[前端开发博客](http://caibaojian.com/iframe-adjust-content-height.html)