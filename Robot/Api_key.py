import os
from langchain_openai import ChatOpenAI


class Open_ai:

    def deepseek_ai(self):
        self.deepseek = os.getenv("DEEPSEEK_API_KEY")
        self.model = ChatOpenAI(
            api_key=self.deepseek,
            model="deepseek-v4-flash-vision-exp",
            base_url="https://api.deepseek.com"
        )
        return self.model


    def qwen_ai(self):
        self.qwen = os.getenv("DASHSCOPE_API_KEY")
        self.model = ChatOpenAI(
            api_key=self.qwen,
            model="qwen3.7-flash",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        return self.model


    def bocha_key(self):
        api_key = os.getenv("BOCHA")
        return api_key
