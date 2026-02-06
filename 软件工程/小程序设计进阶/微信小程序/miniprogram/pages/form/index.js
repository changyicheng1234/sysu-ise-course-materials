// pages/form/index.js
Page({
    /**
     * 页面的初始数据
     */
    data: {
      loading: false,   //防止多次按提交造成重复创建
      nickname: '',     // 用于存储昵称
    },
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad() {
      // 从本地缓存中获取昵称
      const nickname = wx.getStorageSync('nickname');
      if (nickname) {
        this.setData({
          nickname: nickname,
        });
      }
    },
  
    submit: function(e) {   //e中保存有wxml中传递给js的数据，这里保存有form表单
      if (this.data.loading) {
        return;   //如果已经点击提交了就不再重复提交
      }
      let u = e.detail.value;   //创建一个临时变量u，获得form表单
      if (!u.nickname) {   //如果为空，提醒用于
        wx.showToast({   //显示提醒组件
          title: "请输入昵称",
          icon: "error",
        });
        return;
      }
      if (!u.number) {   //如果为空返回，提醒用户
        wx.showToast({
          title: "请输入学号",
          icon: "error",
        });
        return;
      }
      this.setData({     //this.setData用于修改data中的属性
        loading: true,
      });
      wx.cloud.callFunction({     //wx.cloud为云开发环境，callFunction调用云开发函数
        name: "quickstartFunctions",   //云开发文件夹名称
        data: {
          type: "createGroup",       //要调用的函数
          data: {
            //...u是js中的拆分语法，将u（这里是form表达）发送过去
            ...u,
          },
        },
      }).then((res) => {     //执行完成后，res为云开发环境返回的数据
        this.setData({
          loading: false,
        });
        console.log(res);
        //返回上一页
        wx.navigateBack();
      });
    },
  })