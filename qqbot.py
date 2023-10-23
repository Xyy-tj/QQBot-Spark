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
from spark_gpt.spark_gpt import SparkGPT



def connect_sqlite():
    conn = sqlite3.connect('qqbot.db')
    cursor = conn.cursor()
    return

def gpt():
    speaker = SparkGPT("接下来我会给你发送一个文案，请你帮我润色一下，加上合适的称呼", language="chinese")
    answer = speaker.ask("今生今世有缘和你在一起，每一分，每一秒都是幸福，都是老天恩赐的福祉。")
    return answer

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content=gpt())


# intents = botpy.Intents(public_guild_messages=True) 
# client = MyClient(intents=intents)
# client.run(appid="102069399", token="fku0DRitB6XmEOdBBeJM2ibWdzkGdA0Q")
gpt()