// pages/list/index.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
      groupList:[],
    },
    onLoad:function(e){    //当页面被加载时会调用此函数
      this.loadGroupData();
    },
    onShow: function() {  //当页面显示时会调用此函数
      // 页面显示时执行刷新操作
      this.loadGroupData();
    },
    loadGroupData: function() {
      // 获得列表
      wx.cloud.callFunction({
        name: "quickstartFunctions",
        data: {
          type: "getGroup",
        },
      }).then((res) => {
            this.setData({
              groupList: res.result.groupList,
            });
      });
    },
  })