<template>
  <view>
    <!-- bindgetphonenumber -->
    <button
      type="primary"
      open-type="getUserInfo"
      @click="getuserinfo"
      withCredentials="true"
    >
      微信登录
    </button>
    <button open-type="getPhoneNumber" @getphonenumber="getPhoneNumber">
      获取电话号码
    </button>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
  onLoad: function () {
    uni.login({
      success: function (res) {
        // 获取code
        // console.log(JSON.stringify(res));
      },
    });
  },

  methods: {
    getPhoneNumber: function (e) {
      console.log(e);
      if (e.detail.errMsg == "getPhoneNumber:fail user deny") {
      } else {
      }

      // console.log(JSON.stringify(e.encryptedData));
      // console.log(JSON.stringify(e.iv));
    },
    getUserInfo: function (loginType, cb) {
      var that = this;
      if (this.globalData.userInfo) {
        typeof cb == "function" && cb(this.globalData.userInfo, true);
      } else {
        //1.调用登录接口
        wx.login({
          success: function () {
            wx.getUserInfo({
              success: function (res) {
                that.globalData.userInfo = res.userInfo;
                typeof cb == "function" && cb(that.globalData.userInfo, true);
              },
              fail: function () {
                //2.第一次登陆不强制授权，直接返回
                if (loginType == 0) {
                  typeof cb == "function" &&
                    cb(that.globalData.userInfo, false);
                } else {
                  //3.授权友好提示
                  wx.showModal({
                    title: "提示",
                    content: "您还未授权登陆，部分功能将不能使用，是否重新授权？",
                    showCancel: true,
                    cancelText: "否",
                    confirmText: "是",
                    success: function (res) {
                      //4.确认授权调用wx.openSetting
                      if (res.confirm) {
                        if (wx.openSetting) {
                          //当前微信的版本 ，是否支持openSetting
                          wx.openSetting({
                            success: (res) => {
                              if (res.authSetting["scope.userInfo"]) {
                                //如果用户重新同意了授权登录
                                wx.getUserInfo({
                                  success: function (res) {
                                    that.globalData.userInfo = res.userInfo;
                                    typeof cb == "function" &&
                                      cb(that.globalData.userInfo, true);
                                  },
                                });
                              } else {
                                //用户还是拒绝
                                typeof cb == "function" &&
                                  cb(that.globalData.userInfo, false);
                              }
                            },
                            fail: function () {
                              //调用失败，授权登录不成功
                              typeof cb == "function" &&
                                cb(that.globalData.userInfo, false);
                            },
                          });
                        } else {
                          typeof cb == "function" &&
                            cb(that.globalData.userInfo, false);
                        }
                      } else {
                        typeof cb == "function" &&
                          cb(that.globalData.userInfo, false);
                      }
                    },
                  });
                }
              },
            });
          },
        });
      }
    },
  },
};
</script>

<style>
</style>
