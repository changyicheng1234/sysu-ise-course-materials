const getOpenId = require('./getOpenId/index');
const createGroup = require('./Group/createGroup');
const getGroup = require('./Group/getGroup');
const modifyGroup = require('./Group/modifyGroup');

// 云函数入口函数
exports.main = async (event, context) => {
  switch (event.type) {
    case 'getOpenId':
      return await getOpenId.main(event, context);
    case 'createGroup':
        return await createGroup(event,context);
    case 'getGroup':
        return await getGroup(event,context);
    case 'joinGroup':
        return await joinGroup(event,context);
    case 'modifyGroup':
        return await modifyGroup(event,context);
  }
};
        
