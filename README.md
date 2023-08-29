<!-- TOC -->
* [pythonKook](#pythonkook)
  * [项目结构](#项目结构)
  * [事件处理机制](#事件处理机制)
  * [施工进度](#施工进度)
    * [API施工进度](#api施工进度)
    * [更好的HTTP请求性能](#更好的http请求性能)
    * [上层的封装](#上层的封装)
* [感谢和免责声明](#感谢和免责声明)
<!-- TOC -->

# pythonKook
自用Kook机器人轮子，希望能够为自己写Kook机器人的时候提供一些便利。

## 使用方法

### 安装

我暂时还没想好该怎么弄，先直接git clone下来然后import吧！

后面考虑用pip之类的方法来搞。

### 使用

#### 最简单的样例

```python
from pyKook.App.Bot import Bot
from pyKook.Config import accountConfig, botConfig

import asyncio

account_conf = accountConfig("Bot", "你的token", "zh-CN")
# 使用 . 来做命令前缀，比如说.r 1d6， .kick xxx等等
bot_conf = botConfig(command=".")
# 你的Bot对象
bot = Bot({"accountConfig": account_conf, "botConfig": bot_conf})

@bot.on_event("isMentioned.atMe") # 有人at我
async def onMentioned(event):
    await bot.sendText(event.getChannel(), "你好！")
    
@bot.on_command("roll")
async def onRoll(event):
    import random
    await bot.sendText(event.getChannel(), "你掷出了一个1d6的骰子，结果是：{}".format(random.randint(1, 6)))

async def main():
    await bot.initialize()
asyncio.run(main())
```

## 项目结构

`pyKook`为项目的根目录。下方包括了`pyKook`的所有子模块。

- `App`模块为群组机器人的核心功能组件，包括具体的消息处理机制和回调函数设置。

- `Config`模块旨在提供封装的、便利的配置文件接口。

- `Api`模块封装了Kook文档中的有关API，便于调用。

- `Utils`为工具模块，提供了网络连接等关键功能。

## 事件处理机制

当程序启动，`App`模块中的`Bot`对象读取相应配置后，通过`gateway`接口获取网关。
随后，一个全局的`Api.eventAPI.websocketMsgHandler`对象被实例化，
其对象池中的一个`websocketHandler`对象建立属于`bot`的ws连接。
随后，通过ws接收到的每一个数据包都会经由`websocketMsgHandler`处理，产生一个“事件”消息发送给`Bot`。

“事件”消息包括了两个部分，分别是事件标识和事件数据。
事件数据是对原始的websockets数据包进行了解析后的数据，其作为一个基本的类提供了部分比较方便的接口用于调用。
事件标识是一个字符串，其标识这个事件的类型，基本分为以下的部分：


|事件标识| 事件类型 |
|---|------|
|`onMentioned`| 被@   |
|`onSystemMessage`| 系统消息 |
|`onNormalMessage`|普通群聊消息更新|
|`onContextUpdate`|带有上下文聊天的消息|

其中`onSystemMessage`包含系统消息、群组消息等各类子事件。

`Bot`对象根据事件标识，调用相应的回调函数对事件进行处理，基本的处理方式包括回应等均为通过`Api`模块调用相应接口。

可以说，本项目基本是**一个*事件驱动*的框架**。


## 施工进度

目前该项目仍在施工的早期阶段。

**目前，我们开发的核心方向是实现基本的机器人功能，即最基础的信息获取、消息回应机制。**

|模块| 进度          |
|---|-------------|
|`App`| 锐意进行中       |
|`Config`| 下一步准备完善本地存储 |
|`Api`| 锐意进行中       |
|`Utils`| 随项目进行       |

### API施工进度

**目前计划实现部分**：

- [x] 事件获取
  - [x] Websocket方式
  - [ ] ~~Webhook方式（懒了，不想写）~~
  - [ ] ~~轮询？（暂时不考虑）~~

- [x] HTTP接口
  - [x] 服务器相关接口列表
    - [x] 获取当前用户加入的服务器列表
    - [x] 获取服务器详情
    - [x] 获取服务器中的用户列表
  - [x] 频道相关接口列表
    - [x] 获取频道列表
    - [x] 获取频道详情
  - [x] 频道消息相关接口
    - [x] 发送频道聊天消息
    - [x] 删除频道聊天消息
  - [x] Gateway相关接口
  - [x] 用户相关接口
    - [x] 获取当前用户信息
    - [x] 获取目标用户信息

- [ ] 事件接口
  - [ ] 频道相关事件
    - [ ] 频道消息更新
  - [ ] 服务器成员相关事件
    - [ ] 新成员加入服务器
  - [x] 消息相关事件
    - [x] 文字消息
    - [x] KMarkdown消息
    - [x] Card消息

### 更好的HTTP请求性能

啊啊啊啊啊啊，多页的multiPageAPI采用了并发的方式请求，但是单独的查询方法我还没想到更好的方法去优化。

### 上层的封装

子模块写的太难看了，App模块里面要封装一下。

# 感谢和免责声明

感谢Kook的文档，感谢websockets、grequest等Python模块的开发者。

感谢博德之门3，真的太好玩了。~~我真的好想玩星空啊！~~

本项目仅仅是我一时兴起的产物，本人对项目的可靠性、稳定性、安全性等等都不做任何保证。如果你使用了本项目，那么你需要自行承担一切可能的后果。
任何对本项目的使用、修改、传播等都无所谓。