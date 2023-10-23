import botpy
from botpy.message import Message
import openai
import sqlite3
import os
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket

class Ws_Param(object):
        # 初始化
        def __init__(self, gpt_url):
            self.APPID = '004fd304'
            self.APIKey = '835dd4acec99b69c8dac06b9546f50fc'
            self.APISecret = 'NTU5ZTZlMzRkM2IxZGZhOWJkYWQ5Yjlj'
            self.host = urlparse(gpt_url).netloc
            self.path = urlparse(gpt_url).path
            self.gpt_url = gpt_url

        # 生成url
        def create_url(self):
            # 生成RFC1123格式的时间戳
            now = datetime.now()
            date = format_date_time(mktime(now.timetuple()))

            # 拼接字符串
            signature_origin = "host: " + self.host + "\n"
            signature_origin += "date: " + date + "\n"
            signature_origin += "GET " + self.path + " HTTP/1.1"

            # 进行hmac-sha256进行加密
            signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                    digestmod=hashlib.sha256).digest()

            signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

            authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

            # 将请求的鉴权参数组合为字典
            v = {
                "authorization": authorization,
                "date": date,
                "host": self.host
            }
            # 拼接鉴权参数，生成url
            url = self.gpt_url + '?' + urlencode(v)
            # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
            return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, one, two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content, end="")
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, domain, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def connect_sqlite():
    conn = sqlite3.connect('qqbot.db')
    cursor = conn.cursor()
    return

def gpt():
    wsParam = Ws_Param("ws(s)://spark-api.xf-yun.com/v1.1/chat")
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.question = [
        {"role": "system", "content": "假设你是个程序员，你的微信是llike620"},
        {"role": "user", "content": "微信多少"}
    ]
    ws.domain = "general"
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content=gpt())


# intents = botpy.Intents(public_guild_messages=True) 
# client = MyClient(intents=intents)
# client.run(appid="102069399", token="fku0DRitB6XmEOdBBeJM2ibWdzkGdA0Q")
gpt()