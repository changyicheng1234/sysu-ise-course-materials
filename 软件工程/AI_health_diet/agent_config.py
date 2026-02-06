import Agently
import nest_asyncio

# 解决异步执行问题
nest_asyncio.apply()

def init_agent_factory():
    """初始化并配置 Agently 代理工厂"""
    agent_factory = (
        Agently.AgentFactory()
        .set_settings("current_model", "ERNIE")
        .set_settings("model.ERNIE.auth", {"aistudio": "b44dc285697fcdbee35dc37c1cee12fe06fb8d83"})
        .set_settings("model.ERNIE.options", {"model": "ernie-speed"})
    )
    return agent_factory