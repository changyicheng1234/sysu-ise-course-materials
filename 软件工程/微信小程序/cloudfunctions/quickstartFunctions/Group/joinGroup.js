//获得微信服务端开发工具包
const cloud = require('wx-server-sdk');
//初始化一下
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});
//设置一个数据库变量
const db = cloud.database();
const _ = db.command;  //或者数据库操作符，通过command可以进行数据库比较、删改等操作
//Node.js语法，包装好的函数体会在接收到前端数据后执行
module.exports = async(event) =>{

  let u = event.data;  //获得前端发过来的数据
  //获得用户唯一ID，由微信提供
  let wxContext = cloud.getWXContext();   
  let openID = wxContext.OPENID;  

  //对数据库进行操作
  await db
    .collection("test-group")  //找到名为test-group的表单
    .where({    //表单里符合要求的记录
      groupID: u.groupID,
    })
    .update({    //更新该记录
      data: {   
        member: _.inc(1), //人数+1
        memberNumber: _.addToSet(u.number),  //把新加入的同学学号添加进数组中 
        memberName: _.addToSet(u.nickname),  //把新加入的同学昵称添加进数组中 
      },
    });
  return {
    success: true,
  };

};