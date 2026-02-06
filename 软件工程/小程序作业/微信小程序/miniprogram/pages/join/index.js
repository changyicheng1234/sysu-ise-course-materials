// pages/join/index.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
      groupID:"",
    },
    onLoad:function(e){
      //e中具有从pages/list/index.wxml文件中的
      //<navigator url="/pages/join/index?groupID={{group.groupID}}" class="card">
      //传来的?groupID的数值
      this.setData({
        groupID:e.groupID  
      })
    },
    submit:function(e){   //基本和创建小组区别不大
      if(this.data.groupID){
        let u = e.detail.value;
        if (!u.nickname) {
          wx.showToast({
            title: "请输入昵称",
            icon: "error",
          });
          return;
        }
        if (!u.number) {
          wx.showToast({
            title: "请输入学号",
            icon: "error",
          });
          return;
        }
        wx.cloud
        .callFunction({
          name: "quickstartFunctions",
          data: {
            type: "joinGroup",
            data: {
              ...u,
              groupID: Number(this.data.groupID),
            },
          },
        })
        .then((res) => {
          this.setData({
            loading: false,
          });
          wx.hideLoading();
          //如果添加成功自动页面跳转到小组列表
          if (res.result.success) {
            wx.redirectTo({
              url:
                "/pages/list/index"
            });
          }
        });
      }
    }
  })