// pages/modify/index.js
Page({
    data: {
      loading: false,
    },
  
    submit: function (e) {
      if (this.data.loading) {
        return;
      }
  
      let u = e.detail.value;
      console.log("表单数据:", u); // 调试：打印表单数据
  
      if (!u.nickname) {
        wx.showToast({
          title: "请输入原小组名称",
          icon: "error",
        });
        return;
      }
      if (!u.groupName) {
        wx.showToast({
          title: "请输入新小组名称",
          icon: "error",
        });
        return;
      }
  
      this.setData({
        loading: true,
      });
  
      wx.cloud.callFunction({
        name: "quickstartFunctions", // 如果单独部署，改为 "modifyGroup"
        data: {
          type: "modifyGroup",
          data: { ...u },
        },
      })
        .then((res) => {
          this.setData({
            loading: false,
          });
          console.log("云函数返回:", res); // 调试：打印返回结果
  
          if (res.result.success) {
            wx.showToast({
              title: "修改成功",
              icon: "success",
            });
            wx.navigateBack();
          } else {
            wx.showToast({
              title: res.result.message || "修改失败",
              icon: "error",
            });
          }
        })
        .catch((err) => {
          this.setData({
            loading: false,
          });
          wx.showToast({
            title: err.message || "请求失败",
            icon: "error",
          });
          console.error("云函数调用失败:", err); // 调试：打印详细错误
        });
    },
  });