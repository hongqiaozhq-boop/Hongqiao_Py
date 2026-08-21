import gradio as gr
from openai import OpenAI
import os
import html


connect = None

def deepseek_content():
    global connect
    if connect is None:
        connect = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")
    return connect


def chat_ai(message,history):
    chat_ai_connect = deepseek_content()

    message_list = [ {"role": "system","content": "你是一名非常可爱的ai助理,你的名字叫做达尼娅,请你使用可爱的语气回答客户的问题"}]

    for item in history[-12:]:
        message_list.append(item)

    message_list.append({"role": "user", "content": message})

    chat = chat_ai_connect.chat.completions.create(# type: ignore
        model = "deepseek-chat",
        messages = message_list,
        stream=True
    )
    partial_message = ""
    for chunk in chat:
        if chunk.choices[0].delta.content is not None:
            partial_message += chunk.choices[0].delta.content
            escaped = html.escape(partial_message)
            yield escaped



#ChatInterface
# 创建界面
demo = gr.ChatInterface(
    fn=chat_ai,
    title="🤖 和达尼娅聊天",
    description="我是可爱的达尼娅，有什么想和我聊的吗？"
)


demo.queue()

# 开启不阻塞，打印url
app, local_url, share_url = demo.launch(share=True, prevent_thread_lock=True)
print("\n🔗 本地访问地址：", local_url)
if share_url:
    print("🌐 公网分享地址：", share_url)
else:
    print("❌ 公网隧道创建失败，仅本机可访问！")

input("\n程序运行中，按回车键关闭程序\n")



