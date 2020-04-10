



### 微信原生代码
使用 button 组件，并将 open-type 指定为 getUserInfo 类型，获取用户基本信息。

```html
<button form-type="submit" open-type="getUserInfo" bindgetuserinfo="getUserInfo"> </button>
```

- **bindgetuserinfo**: 用户点击该按钮时，会返回获取到的用户信息，回调的detail数据与wx.getUserInfo返回的一致，open-type="getUserInfo"时有效
- **open-type**: getUserInfo获取用户信息，可以从bindgetuserinfo回调中获取到用户信息

然而uniapp中 使用微信的open-type=“getUserInfo” 不能获取到userinfo
在methods 写入方法

```js
getuserinfo: function(){// wx登录
  wx.login({  
    success (res) {    
      if (res.code) {      //发起网络请求  
        var code = res.code  // 获取微信用户信息
        wx.getUserInfo({  
          success: function(res) {
            var userInfo = res.userInfovar 
            var nickName = userInfo.nickNamevar 
            var avatarUrl = userInfo.avatarUrlvar 
            var gender = userInfo.gender //性别 0：未知、1：男、2：女var 
            var province = userInfo.provincevar 
            var city = userInfo.city
            var country = userInfo.country  
          },  
          fail:res={      
            // 获取失败的去引导用户授权    
          }})    
      } else {
        //...    
      }  
	}
 })
},
```

在调用中 会提示说 `does not have a method “bindgetuserinfo” to handle event “getuserinfo”.`

```html
<button class='testbutton' open-type="getUserInfo" @getuserinfo="getuserinfo" withCredentials="true">
  
</button>
```

> 将`bindgetuserinfo`改成`@getuserinfo="getuserinfo" `，再添加 `withCredentials="true"`，就可以调用了







方法一
**使用button组件（open-type属性）**
<button open-type="getUserInfo"@click="loginMP"></button>

```javascript
		uni.getUserInfo({
				provider:"weixin",
				success(userInfo) {
					loginMP().then(res=>{
						 uni.setStorageSync('token', res.result.token)
						uni.getUserInfo({
							provider:"weixin",
							success(res) {
								console.log(res);
							},
							fail(err) {
								console.log(err);
							}
						})
						uni.showToast({
							title: '登录成功'
						});
					}).catch(err=>{
						uni.showModal({
							title: "提示",
							content: '稍后重试'+err.message,
							showCancel: false,
						});
					})
				}
```


方法二
**使用openSetting引导用户打开相应的权限，相关的API还有getSetting **

```javascript
uni.authorize({
  scope:"scope.scope.userInfo",
  success(res) {
    console.log(res);
  },
  fail() {
    uni.openSetting({
      success(authSetting) {
        console.log(authSetting);
      }
    })
  }
})
```
