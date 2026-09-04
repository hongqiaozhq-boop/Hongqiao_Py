from Robot.Agents import Agents
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage


#实例化
agent = Agents()


deepseek_agent = agent.deepseek_agent()
qwen_agent = agent.qwen_agent()


if __name__ == '__main__':

    deepseek_ai_robot = deepseek_agent.invoke(HumanMessage("今天是几月几日"))
    for messages in deepseek_ai_robot["messages"]:
        messages.pretty_print()

    # qwen_ai_robot = qwen_agent.invoke(HumanMessage("你是谁"))
    # for messages in qwen_ai_robot["messages"]:
    #     messages.pretty_print()