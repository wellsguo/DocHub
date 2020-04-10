## uni.navigateBack 传参数

```javascript
var pages = getCurrentPages();
var currPage = pages[pages.length - 1]; //当前页面
var prevPage = pages[pages.length - 2]; //上一个页面
//直接调用上一个页面的setData()方法，把数据存到上一个页面中去
prevPage.setData({
  hope_job: "test"
});
```

```javascript
uni.navigateBack();
```

```javascript
onShow:function(e){
    let pages = getCurrentPages();
    let currPage = pages[pages.length-1];
    if (currPage.data.hope_job==""){
        this.getHopeJob();
    }else{
        this.hope_job = currPage.data.hope_job
    }

}
```





## VUE JQUERY AJAX



jsp页面：

```vue

<div id="app">
  {{message }}<br>
  <button v-on:click="showData">测试jquery加载数据</button>
  <table border="1">
    <tr v-for="data in datas">
      <td>{{data.Name}}</td>
      <td>{{data.Url}}</td>
      <td>{{data.Country}}</td>
    </tr>
  </table>
</div>
```



```javascript
//定义Vue组件
var vum=new Vue({
  el: "#app",
  data: {
    message: "",
    datas: "",
 
  },
  methods:{
    showData:function () {
      jQuery.ajax({
        type: 'Get',
        url: "/vue1/json/data.json",
        success: function (data) {
          vum.datas = data.sites;
        }
      })
    }
  }
})
```



