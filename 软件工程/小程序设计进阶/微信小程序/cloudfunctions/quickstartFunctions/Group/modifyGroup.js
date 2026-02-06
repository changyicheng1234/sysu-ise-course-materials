// 云函数: modifyGroup.js
const cloud = require('wx-server-sdk');

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV,
});

const db = cloud.database();

module.exports = async (event) => {
  console.log("接收到的数据:", event); // 调试：打印输入数据

  let u = event.data || {};
  if (!u.nickname || !u.groupName) {
    return {
      success: false,
      message: "原小组名称或新小组名称不能为空",
    };
  }

  try {
    const queryResult = await db.collection("test-group").where({
      groupName: u.nickname,
    }).get();

    console.log("查询结果:", queryResult); // 调试：打印查询结果

    if (queryResult.data.length === 0) {
      return {
        success: false,
        message: "未找到匹配的小组",
      };
    }

    await db.collection("test-group").where({
      groupName: u.nickname,
    }).update({
      data: {
        groupName: u.groupName,
      },
    });

    return {
      success: true,
      message: "小组名称修改成功",
    };
  } catch (error) {
    console.error("数据库操作失败:", error); // 调试：打印错误
    return {
      success: false,
      message: `修改失败：${error.message}`,
    };
  }
};