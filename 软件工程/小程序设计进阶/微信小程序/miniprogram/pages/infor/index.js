Page({

    /**
     * 页面的初始数据
     */
    data: {
      loginOk:false,
      nickName:"",
      avatarUrl:"",
    },
  
    //页面加载的时候，将load页面传过来的值获取过来
    onLoad: function (options) {
      console.log("这里的options",options);
      this.setData({
        nickName:options.nickName,
        avatarUrl:options.avatarUrl
      })
    },
  
    //小程序声明周期的可见性函数里面来控制显示
    onShow(){
      let userInfo = wx.getStorageSync('userInfo')
      console.log("我的缓存信息",userInfo);
      if(userInfo){
        this.setData({
          loginOk:true,
          nickName:userInfo.nickName,   //从缓存中拿数据
          avatarUrl:userInfo.avatarUrl
        })
      }else{
        this.setData({
          loginOk:false
        })
      }
    },
  
    //点击登录
    load(){
      wx.navigateTo({
        url: '/pages/input/index',
      })
    },
  
    //退出登录
    exit(){
      wx.showModal({
        content:"确定退出吗"
      }).then(res=>{
        if(res.confirm){
        console.log("用户点击了确定");
        this.setData({
          loginOk:false
        })
        //清空登录的缓存
        wx.setStorageSync('userInfo', null)
        }else if(res.cancel){
          console.log("用户点击了取消");
        }
      })
    },
  
  })