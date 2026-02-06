const cloud = require("wx-server-sdk");

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV,
});

const db = cloud.database();
module.exports = async (event) => {
  try {
    let res = await db    //获得数据库内容
      .collection("test-group")
      .orderBy("groupID", "asc")  //按照groupID排序
      .get();
    return {
      success: true,
      groupList: res.data,   //返回数据库中的数据给小程序前端
    };
  } catch (error) {
    return {
      success: false,
      errorMessage: error,
    };
  }
};