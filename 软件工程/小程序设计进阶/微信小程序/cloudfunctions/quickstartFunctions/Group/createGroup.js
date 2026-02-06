//获得微信服务端开发工具包
const cloud = require('wx-server-sdk');
//初始化一下
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});
//设置一个数据库变量
const db = cloud.database();
//module.export包裹的内容会在调用云函数createGroup.js时候调用，async是异步调用
module.exports = async(event) =>{
  let u = event.data;  //获得小程序前端发送的数据
  //获得用户唯一ID
  let wxContext = cloud.getWXContext();
  let openID = wxContext.OPENID;
  //递增小组id编号
  let res = await db.collection("test-group").count();   //await db.collection()用于查询数据库，count()为统计行数
  let groupID = parseInt(res.total) + 1   //行数+1
  await db.collection("test-group").add({   //将数据添加进数据库中
    data:{
      leaderName: u.nickname,
      leaderNumber: u.number,
      member: 1,
      openID,
      groupID,
      memberNumber:[],  //创建列表
      memberName:[],  
      groupName:u.groupName,
    },
  });
  return {
    success: true,  //给前端返回成功
  };
};