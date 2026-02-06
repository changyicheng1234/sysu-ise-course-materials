// pages/index/index.js
Page({
    /**
     * 页面的初始数据
     */
    data: {
      isLoggedIn: false // 添加一个变量来跟踪登录状态，默认为 false (未登录)
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
      // 可以在 onLoad 中也检查一次，但 onShow 更常用，因为它每次页面显示都会触发
      // this.checkLoginStatus();
    },
  
    /**
     * 生命周期函数--监听页面显示
     */
    onShow() {
      // 每次页面显示时都检查登录状态
      this.checkLoginStatus();
    },
  
    /**
     * 检查登录状态的函数
     */
    checkLoginStatus: function() {
      // --- !!! 重要：请将 'userInfo' 替换为你实际存储登录凭证的 Storage Key !!! ---
      // 例如，如果你在登录成功后存储的是 token，就用 wx.getStorageSync('token')
      try {
        const loginCredential = wx.getStorageSync('userInfo'); // 尝试获取登录凭证
        if (loginCredential) {
          // 如果获取到了凭证，说明用户已登录
          this.setData({
            isLoggedIn: true
          });
          console.log('index.js: 用户已登录');
        } else {
          // 如果没获取到凭证，说明用户未登录
          this.setData({
            isLoggedIn: false
          });
          console.log('index.js: 用户未登录');
        }
      } catch (e) {
        // 处理异常情况，例如存储API调用失败
        console.error('index.js: 检查登录状态时发生错误', e);
        this.setData({
          isLoggedIn: false // 出错时默认视为未登录
        });
      }
    },
  
    // --- 注意：---
    // 实际的登录逻辑（调用 wx.login, 请求服务器, wx.setStorageSync 保存登录状态）
    // 应该在你导航到的登录页面 (/pages/input/index.js) 中完成。
    // 同样，登出逻辑（比如在“我的”页面操作）需要调用 wx.removeStorageSync 清除状态。
    // 这个 index.js 文件只负责 *检查* 状态并据此更新界面。
  
    // 以下是原有的生命周期函数和事件处理函数，保持不变
    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady() {},
    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide() {},
    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload() {},
    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh() {},
    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom() {},
    /**
     * 用户点击右上角分享
     */
    onShareAppMessage() {}
  })