> 由于需要使用一个纯单词组成的文件，在网上下载到了一个存放单词的文件，但是里面有中文的解释，那就需要做一下提取了。


## 利用字符集过滤掉中文

```python
#coding:utf-8
 
file_object = open('words.txt')
try:
     lines = file_object.readlines()
finally:
     file_object.close( )
 
for line in lines:
    if line!='\n':
        print line.decode('gb2312','ignore'), 
```

## 利用正则表达式

- 超短文本，ASCII识别

```python
s = "China's Legend Holdings will split its several business arms to go public on stock markets, the group's president Zhu Linan said on Tuesday.该集团总裁朱利安周二表示，中国联想控股将分拆其多个业务部门在股市上市。"
result = "".join(i for i in s if ord(i) < 256)
print(result)
# out:
# China's Legend Holdings will split its several business arms to go public on stock markets, the group's president Zhu Linan said on Tuesday.
```

- unicode 编码识别

```python
import re

s = "China's Legend Holdings will split its several business arms to go public on stock markets, the group's president Zhu Linan said on Tuesday.该集团总裁朱利安周二表示，中国联想控股将分拆其多个业务部门在股市上市。"
uncn = re.compile(r'[\u0061-\u007a,\u0020]')
en = "".join(uncn.findall(s.lower()))
print(en)
# out:
# chinas legend holdings will split its several business arms to go public on stock markets, the groups president zhu linan said on tuesday

s = 'hi新手oh'.decode('utf-8') # 举个栗子是字符串s，为了匹配下文的unicode形式，所以需要解码
p = re.compile(ur'[\u4e00-\u9fa5]') # 这里是精髓，[\u4e00-\u9fa5]是匹配所有中文的正则，因为是unicode形式，所以也要转为ur


print p.split(s) # 使用 re 库的split切割

```


> 1. 中文的编码范围是：`\u4e00-\u9fa5`，相应的 `[^\u4e00-\u9fa5]` 可匹配非中文。  
> 2. 匹配英文时，需要将空格 `[\u0020]` 加入，不然单词之间没空格了。

附：[各国文字Unicode编码范围](http://www.doc88.com/p-801578373970.html)

       