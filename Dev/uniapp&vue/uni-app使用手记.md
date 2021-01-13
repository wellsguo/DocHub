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



## UNI-APP 导入外部JS文件

主流模块都支持

### 1. es6 模块 export default 导出

```javascript
import xxx from './common/xxx.js'
```

- canvas.js
```javascript
export default{
    canvasGraph(canvasID,data,summation){
        //...
    }
    
}
```

- canvas.vue
```javascript
import canvas from '/common/canvas.js'

canvas.canvasGraph(...)
```

### 2.  es6 模块 export 导出

```javascript
import {xxx} from './common/xxx.js'
```

- api.js
```javascript
export const saveOrUpdate = (token, params, callback) => { ... }

export const get = (token, params, callback) => { ... }

export const del = (token, params, callback) => { ... }
```

- logic.vue
```javascript
import {saveOrUpdate, get, del} from '/common/api.js'

saveOrUpdate(...)
get(...)
del(...)
```

### 3. commonjs、adm、cmd 模块

```javascript
var xxx = require('./common/xxx.js')
```

- util.js
```javascript
function formatTime(time) {
	if (typeof time !== 'number' || time < 0) {
		return time
	}

	var hour = parseInt(time / 3600)
	time = time % 3600
	var minute = parseInt(time / 60)
	time = time % 60
	var second = time

	return ([hour, minute, second]).map(function (n) {
		n = n.toString()
		return n[1] ? n : '0' + n
	}).join(':')
}

function formatDatetime(fmt, date) { //author: meizz   
	var o = {
		"M+": date.getMonth() + 1, //月份   
		"d+": date.getDate(), //日   
		"h+": date.getHours(), //小时   
		"m+": date.getMinutes(), //分   
		"s+": date.getSeconds(), //秒   
		"q+": Math.floor((date.getMonth() + 3) / 3), //季度   
		"S": date.getMilliseconds() //毫秒   
	};
	if(/(y+)/.test(fmt)){
		fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
	}
	for(var k in o){
		if(new RegExp("(" + k + ")").test(fmt)){
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
		}
	}    
	return fmt;
}

function formatLocation(longitude, latitude) {
	if (typeof longitude === 'string' && typeof latitude === 'string') {
		longitude = parseFloat(longitude)
		latitude = parseFloat(latitude)
	}

	longitude = longitude.toFixed(2)
	latitude = latitude.toFixed(2)

	return {
		longitude: longitude.toString().split('.'),
		latitude: latitude.toString().split('.')
	}
}
var dateUtils = {
	UNITS: {
		'年': 31557600000,
		'月': 2629800000,
		'天': 86400000,
		'小时': 3600000,
		'分钟': 60000,
		'秒': 1000
	},
	humanize: function (milliseconds) {
		var humanize = '';
		for (var key in this.UNITS) {
			if (milliseconds >= this.UNITS[key]) {
				humanize = Math.floor(milliseconds / this.UNITS[key]) + key + '前';
				break;
			}
		}
		return humanize || '刚刚';
	},
	format: function (dateStr) {
		var date = this.parse(dateStr)
		var diff = Date.now() - date.getTime();
		if (diff < this.UNITS['天']) {
			return this.humanize(diff);
		}
		var _format = function (number) {
			return (number < 10 ? ('0' + number) : number);
		};
		return date.getFullYear() + '/' + _format(date.getMonth() + 1) + '/' + _format(date.getDate()) + '-' +
			_format(date.getHours()) + ':' + _format(date.getMinutes());
	},
	parse: function (str) { //将"yyyy-mm-dd HH:MM:ss"格式的字符串，转化为一个Date对象
		var a = str.split(/[^0-9]/);
		return new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
	}
};

module.exports = {
	formatTime: formatTime,
	formatDatetime: formatDatetime,
	formatLocation: formatLocation,
	dateUtils: dateUtils
}

```
- page.vue

```javascript
var util = require('./common/util.js')
var datetime = util.formateDatetime('yyyy-MM-dd hh:mm', new Date())
```