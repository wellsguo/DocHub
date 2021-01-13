# uniapp 中混入 mixin

## 局部混入

### mixin.js 文件

```jsx
// 根目录的static下创建js文件夹并创建mixin.js文件
import {api} from "./api.js"  //export 导出的api对象文件
export const mixin={
    data() {
        return {   
            api:api  //接口地址
        }
    },
    methods: {
        //封装post调用接口的方法,
        post:function(url, params) {
            return new Promise((res, rej) => {
                uni.request({
                    url: this.$serverUrl + this.api[url], //$serverUrl 在main.js 设置主要的地址
                    data: params,
                    method: 'POST',
                    header: {
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                        'Authorization': `Bearer ${window.localStorage.getItem('app_token')}`
                    },
                    success: (data) => {
                        //成功执行res
                        res(data)
                    },
                    fail: (err) => {
                        //失败执行rej
                        rej(err)
                    }
                })
            })
        }
    }
}
```

### 局部混入使用

> 在需要使用混入方法的文件中引入

```javascript
//引入混入的文件
import {mixin} from "../../static/js/mixin.js"
export default {
    mixins:[mixin], //混入文件
    data() {
        return {
            pageForm: {
                user_name: '',
                password: ''
            }
        };
    },
    
    methods: {
        login:function(){
            //调用mixin 中的post 方法；具体可了解Promise方法
            this.post('login',this.pageForm).then(res=>{
                console.log(res)
                this.button=false
            }).catch(err=>{
                console.log(err)
            })
        }
    }
};
```

## 全局混入

### 直接在 main.js 文件中使用  Vue.mixin 方法

```javascript
        Vue.mixin({
            data() {
                return {
                    api: api   //引入api文件
                }
            },
            methods: {
                //封装post调用接口的方法,
                post: function(url, params) {
                    return new Promise((res, rej) => {
                        uni.request({
                            url: this.$serverUrl + this.api[url],
                            data: params,
                            method: 'POST',
                            header: {
                                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                                'Authorization': `Bearer ${window.localStorage.getItem('app_token')}`
                            },
                            success: (data) => {
                                //成功执行res
                                res(data)
                            },
                            fail: (err) => {
                                //失败执行rej
                                rej(err)
                            }
                        })
                    })
                },

            }
        })
```

### 或者在 static/js 下创建mixin.js

```jsx
export default {
   install(Vue) {
       Vue.mixin({
           data() {
               return {
                   api: api
               }
           },
           methods: {
               //封装post调用接口的方法,
               post: function(url, params) {
                   return new Promise((res, rej) => {
                       uni.request({
                           url: this.$serverUrl + this.api[url],
                           data: params,
                           method: 'POST',
                           header: {
                               "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                               'Authorization': `Bearer ${window.localStorage.getItem('app_token')}`
                           },
                           success: (data) => {
                               //成功执行res
                               res(data)
                           },
                           fail: (err) => {
                               //失败执行rej
                               rej(err)
                           }
                       })
                   })
               },

           }
       })
   }
}

//在 main.js中引入使用
import mixin from "static/js/mixin.js"
Vue.use(mixin)
```