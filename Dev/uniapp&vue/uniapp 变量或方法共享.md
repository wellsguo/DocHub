# uniapp 登录统一验证解决方案



`通用说明`：对于一个新闻、阅读、论坛、购物等应用，浏览页面并不需要用户进行登录和注册；但是在编辑、评论等页面需要用户先登录。故需要封装一个全局的登录检查函数，在对应的页面进行调用。检查判断是否已登录，已登录则可继续操作；未登录则跳转至登录页先完成登录，然后再回到之前页面。

## 1. 在 main.js 中封装全局登录函数



```jsx
 //封装全局登录检查函数:backpage为登录后返回的页面；backtype为打开页面的类型[1 : redirectTo 2 : switchTab]
 //3种页面跳转方式：NavigationTo(直接打开新页面),RedirectTo(覆盖原页面后打开新页面),SwitchTo(切换顶部导航的方式来切换页面)
Vue.prototype.checkLogin = function(backpage, backtype){
    var SUID  = uni.getStorageSync('SUID');//本地持久化存储
    var SRAND = uni.getStorageSync('SRAND');
    var SNAME = uni.getStorageSync('SNAME');
    var SFACE = uni.getStorageSync('SFACE');
    if(SUID == '' || SRAND == '' || SFACE == ''){
        uni.redirectTo({url:'../login/login?backpage='+backpage+'&backtype='+backtype});
        return false;
    }
    return [SUID, SRAND, SNAME, SFACE];//已经登录返回数组 [用户 id, 用户随机码, 用户昵称, 用户表情]，以供后续使用用户信息
}
//定义全局api接口地址和token
var APITOKEN = 'api2019'
Vue.prototype.apiServer = 'http://localhost/index.php?token=' + APITOKEN + '&c=';
```

`备注`：uni-app基于vue.js，vue对象是uni-app中一个关键的对象。**main.js文件可定义全局函数和变量(如全局api接口地址)**，通过vue对象原型拓展来定义全局函数，对应页面通过this指向来调用main.js文件定义的全局函数。

## 2. 创建 login 页面



```xml
<template>
    <view>
        
    </view>
</template>

<script>
export default {
    data() {
        return {
            
        }
    },
    methods: {
        
    },
    onLoad:function(options){
        console.log(options);
    }
}
</script>

<style>

</style>
```

`备注`：login 页面作为登录过度页面，多端登录都通过此页面完成。

## 3. 在对应页面中调用登录检查函数，如



```xml
// write.vue 
<script>
export default {
    data() {
        return {
            
        };
    },
    onLoad : function() {
        var loginRes = this.checkLogin('../my/my', '2');
        if(!loginRes){return false;}
    }
}
</script>
```



# 全局变量实现的4 种方法





## 一、公用模块

定义一个专用的模块，用来组织和管理这些全局的变量，在需要的页面引入。

**注意：这种方式只支持多个[vue](http://www.javanx.cn/tag/vue/)页面或多个nvue页面之间公用，vue和nvue之间不公用。**

示例如下：
在 [uni-app](http://www.javanx.cn/tag/uni-app/) 项目根目录下创建 `common` 目录，然后在 common 目录下新建 base.js 用于定义公用的方法。

```javascript
const websiteUrl = 'http://www.javanx.cn';  
const now = Date.now || function () {  
  return new Date().getTime();  
};  
const isArray = Array.isArray || function (obj) {  
  return obj instanceof Array;  
};  

export default {  
  websiteUrl,  
  now,  
  isArray  
}
```

接下来在 `pages/index/index.vue` 中引用该模块

```javascript
<script>  
import helper from '/common/base.js';  

export default {  
  data() {  
    return {};  
  },  
  onLoad(){  
    console.log('now:' + helper.now());  
  },  
  methods: {  
  }  
}  
</script>
```

这种方式维护起来比较方便，但是缺点就是每次都需要引入。

## 二、挂载 Vue.prototype


将一些使用频率较高的常量或者方法，直接扩展到 Vue.prototype 上，每个 Vue 对象都会“继承”下来。

**注意这种方式只支持多个vue页面或多个nvue页面之间公用，vue和nvue之间不公用。**

示例如下：
在 `main.js` 中挂载属性/方法

```javascript
Vue.prototype.websiteUrl = 'http://www.javanx.cn';  
Vue.prototype.now = Date.now || function () {  
  return new Date().getTime();  
};  
Vue.prototype.isArray = Array.isArray || function (obj) {  
  return obj instanceof Array;  
}; 
```



然后在 `pages/index/index.vue` 中调用

```javascript
<script>  
export default {  
  data() {  
    return {};  
  },  
  onLoad(){  
    console.log('now:' + this.now());  
  },  
  methods: {  
  }  
}  
</script>  
```

这种方式，只需要在 main.js 中定义好即可在每个页面中直接调用。

**注意：**
1、每个页面中不要在出现重复的属性或方法名。

2、建议在 Vue.prototype 上挂载的属性或方法，可以加一个统一的前缀。比如 $url、[global](http://www.javanx.cn/tag/global/)_url 这样，在阅读代码时也容易与当前页面的内容区分开。

## 三、globalData


小程序中可以在 App 上声明[全局变量](http://www.javanx.cn/tag/全局变量/)，但在 Vue 中没有，uni-app 中在 App.vue 可以定义在 globalData 属性上，也可以使用 API 读写这个值。

**这个方式支持vue和nvue共享数据。是目前nvue和vue共享数据的一种比较好的方式。**

定义：App.vue

```javascript
<script>  
export default {  
  globalData: {  
    text: 'text'  
  },  
  onLaunch: function() {  
    console.log('App Launch')  
  },  
  onShow: function() {  
    console.log('App Show')  
  },  
  onHide: function() {  
    console.log('App Hide')  
  }  
}  
</script>  

<style>  
  /*每个页面公共css */  
</style>
```



js中操作globalData的方式如下：

赋值：

```javascript
getApp().globalData.text = 'test'
```



取值：

```javascript
console.log(getApp().globalData.text)
// test
```



如果需要把globalData的数据绑定到页面上，可在页面的onshow声明周期里进行变量重赋值。HBuilderX 2.0.3起，nvue页面在uni-app编译模式下，也支持onshow。

## 四、Vuex


Vuex 是一个专为 Vue.js 应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。

**注意这种方式只支持多个vue页面或多个nvue页面之间公用，vue和nvue之间不公用。**

这里以登录后同步更新用户信息为例，简单说明下 Vuex 的用法，更多更详细的 Vuex 的内容，建议前往其官网 Vuex 学习下。

举例说明：

在 uni-app 项目根目录下新建 store 目录，在 store 目录下创建 index.js 定义状态值

```javascript
const store = new Vuex.Store({  
  state: {  
    login: false,  
    token: '',  
    avatarUrl: '',  
    userName: ''  
  },  
  mutations: {  
    login(state, provider) {  
      console.log(state)  
      console.log(provider)  
      state.login = true;  
      state.token = provider.token;  
      state.userName = provider.userName;  
      state.avatarUrl = provider.avatarUrl;  
    },  
    logout(state) {  
      state.login = false;  
      state.token = '';  
      state.userName = '';  
      state.avatarUrl = '';  
    }  
  }  
}) 
```



然后，需要在 main.js 挂载 Vuex

```javascript
import store from './store'  
Vue.prototype.$store = store  
```



最后，在 pages/index/index.vue 使用

```javascript
<script>  
import {  
  mapState,  
  mapMutations  
} from 'vuex';  

export default {  
  computed: {  
    ...mapState(['avatarUrl', 'login', 'userName'])  
  },  
  methods: {  
    ...mapMutations(['logout'])  
  }  
}  
</script>  
```



详细示例，请下载附件，在 HBuilderX 中运行。

示例操作步骤：
未登录时，提示去登录。跳转至登录页后，点击“登录”获取用户信息，同步更新状态后，返回到个人中心即可看到信息同步的结果。

**注意：对比前面的方式，该方式更加适合处理全局的并且值会发生变化的情况。**

更多VUEX学习，[请点击](http://www.javanx.cn/?post_type=post&s=vuex)

## 总结

1、.vue 和 .nvue 并不是一个规范，因此一些在 .vue 中适用的方案并不适用于 .nvue。

2、Vue 上挂载属性，不能在 .nvue 中使用。

3、.nvue 不支持 vuex

4、如果希望 .vue 和 .nvue 复用一些方法的话，需要采用公用模块的方案，分别在 .vue 和 .nvue 文件中引入。