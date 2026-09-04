from langchain.agents import create_agent
from Robot.Api_key import Open_ai
from Robot.Tools import bocha_browser


class Agents:
    def __init__(self):
        open_ai = Open_ai()
        self.deepseek_ai = open_ai.deepseek_ai()
        self.qwen_ai = open_ai.qwen_ai()

    def deepseek_agent(self):
        deepseeks = create_agent(
            self.deepseek_ai,
            system_prompt="你的名字叫做达尼娅,你是一名非常可爱的ai助手!",
            tools=[bocha_browser]
        )
        return deepseeks

    def qwen_agent(self):
        qwens = create_agent(
            self.qwen_ai,
            system_prompt="你的名字叫做达尼娅,你是一名非常可爱的ai助手!"
        )
        return qwens