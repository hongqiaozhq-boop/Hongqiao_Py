from langchain.tools import tool
import requests
from Robot.Api_key import Open_ai





@tool
def bocha_browser(response: str) -> str:
    """
    用于连接博查搜索引擎进行网络搜索查询,可以查询日期,天气,车票,机票,火车票,股市行情,热点新闻,网络热梗
    :param response: 要查询的内容,例如今天的日期或者未来三天的天气
    :return:
    """
    bocha = Open_ai()
    bocha_key = bocha.bocha_key()

    headers = {
        'Authorization': f'Bearer {bocha_key}',
        'Content-Type': 'application/json'
    }
    url = "https://api.bochaai.com/v1/web-search"

    body = {"query": response,
            "summary": True,
            "freshness": "noLimit",
            "count": 10}

    message = requests.post(url=url,headers=headers,json=body)
    return message.json()