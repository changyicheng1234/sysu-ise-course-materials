const defaultAvatarUrl = 'https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0'
let nickName = ''
let avatarUrl = defaultAvatarUrl
const res = {
  nickName: '',
  avatarUrl: ''
}
Page({
  data: {
    avatarUrl: avatarUrl
  },
  onChooseNickName(e) {
    nickName = e.detail.value
  },
  onChooseAvatar(e) {
    avatarUrl = e.detail.avatarUrl
    this.setData({
      avatarUrl,
    })
  },
  goto() {
    res.nickName = nickName
    res.avatarUrl = avatarUrl
    wx.setStorageSync('userInfo', res)
    // 在存储 userInfo 的同时，单独存储 nickname
    wx.setStorageSync('nickname', nickName)
    wx.reLaunch({
      //将微信头像和微信名称传递给infor的index页面
      url: '/pages/infor/index?nickName=' + nickName + '&avatarUrl=' + avatarUrl,
    })
    console.log('/pages/infor/index?nickName=' + nickName + '&avatarUrl=' + avatarUrl)
  }
})