# Uniapp 开发笔记



### page 页面模版

```vue
<template>
    <!-- vue & uni-app code here -->
</template>

<script>
   // js script here
</script>

<style>
  @import '../../../common/uni-nvue.css';
  // css here
</style>
```



### css



#### [align-items (适用于父类容器上)](http://caibaojian.com/demo/flexbox/align-items.html)

设置或检索弹性盒子元素在侧轴（纵轴）方向上的对齐方式。

#### 语法

```
align-items: flex-start | flex-end | center | baseline | stretch
```

- flex-start：弹性盒子元素的侧轴（纵轴）起始位置的边界紧靠住该行的侧轴（纵轴）起始边界。
- flex-end：弹性盒子元素的侧轴（纵轴）结束位置的边界紧靠住该行的侧轴（纵轴）结束边界。
- center：弹性盒子元素在该行的侧轴（纵轴）上居中放置。（如果该行的尺寸小于弹性盒子元素的尺寸，则会向两个方向溢出相同的长度）。
- baseline：如弹性盒子元素的行内轴与侧轴为同一条，则该值与'flex-start'等效。其它情况下，该值将参与基线对齐。
- stretch：如果指定侧轴大小的属性值为'auto'，则其值会使项目的边距盒的尺寸尽可能接近所在行的尺寸，但同时会遵照'min/max-width/height'属性的限制。



