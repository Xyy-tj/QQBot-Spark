# QQBot
<div align="center">

[![Language](https://img.shields.io/badge/language-python-green.svg?style=plastic)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg?style=plastic)](https://github.com/tencent-connect/botpy/blob/master/LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![PyPI](https://img.shields.io/pypi/v/qq-botpy)
[![BK Pipelines Status](https://api.bkdevops.qq.com/process/api/external/pipelines/projects/qq-guild-open/p-713959939bdc4adca0eea2d4420eef4b/badge?X-DEVOPS-PROJECT-ID=qq-guild-open)](https://devops.woa.com/process/api-html/user/builds/projects/qq-guild-open/pipelines/p-713959939bdc4adca0eea2d4420eef4b/latestFinished?X-DEVOPS-PROJECT-ID=qq-guild-open)

_✨ 基于 [机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/) 实现的机器人框架 ✨_

_✨ 为开发者提供一个易使用、开发效率高的开发框架 ✨_
</div>

## 准备工作

### 安装

```bash
pip install qq-botpy
```

更新包的话需要添加 `--upgrade` `兼容版本：python3.8+`

### 使用

需要使用的地方`import botpy`

```python
import botpy
```

## 使用方式

### 快速入门

#### 步骤1

通过继承实现`bot.Client`, 实现自己的机器人Client 

#### 步骤2

实现机器人相关事件的处理方法,如 `on_at_message_create`， 详细的事件监听列表，请参考 [事件监听.md](./docs/事件监听.md)

如下，是定义机器人被@的后自动回复:

```python
import botpy
from botpy.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")
```

``注意:每个事件会下发具体的数据对象，如`message`相关事件是`message.Message`的对象 (部分事件透传了后台数据，暂未实现对象缓存)``

#### 步骤3

设置机器人需要监听的事件通道，并启动`client`

```python
import botpy
from botpy.message import Message

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        await self.api.post_message(channel_id=message.channel_id, content="content")

intents = botpy.Intents(public_guild_messages=True) 
client = MyClient(intents=intents)
client.run(appid="12345", token="xxxx")
```