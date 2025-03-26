from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
from ai_api import chat_vloces, chat_deepseek

_log = get_log()

config.set_bot_uin("3935598191")  # 设置 bot qq 号 (必填)
config.set_root("1254795592")  # 设置 bot 超级管理员账号 (建议填写)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("")  # 设置 token (napcat 服务器的 token)

bot = BotClient()


@bot.group_event()
async def on_group_message_test(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        await msg.reply(text="NcatBot 测试成功喵~")

@bot.group_event()
async def on_group_message_joy(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message[:2] == "乔伊":
        await msg.reply(text= chat_deepseek(msg.raw_message, syetem_content="你是来自电影银翼杀手2049的女主角乔伊!") )


# 群友小助手
@bot.group_event()
async def on_group_message_bot(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message[:3] == "Bot":
        await msg.reply(text= chat_deepseek(msg.raw_message, syetem_content="你是一个有用的助手") )

@bot.group_event()
async def on_group_message_anime1(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message[:3] == "阿尼亚":
        await msg.reply(text= chat_deepseek(msg.raw_message, syetem_content="你是阿尼亚·福杰，来自漫画《间谍×过家家》的世界") )


@bot.group_event()
async def on_group_message_anime2(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message[:4] == "丰川祥子":
        await msg.reply(text= chat_deepseek(msg.raw_message, syetem_content="你是丰川祥子，女，二次元少女乐队企划“BanG Dream!”中的角色。祥子是一名对音乐充满热情却经历乐队解散挫折的少女，她坚韧不拔地追求梦想，最终组建乐队Ave Mujica，以严格要求和不懈努力向主流音乐界迈进，同时也面临着家庭变故与个人情感的挑战。") )

@bot.group_event()
async def on_group_message_anime2(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message == "川川生日快乐！":
        await msg.reply(text= chat_deepseek("王润洲今天过生日了,你可以给他最大的祝福吗", syetem_content="川川是群里的宝贝男孩王润洲") )


@bot.group_event()
async def on_group_message_ai_api(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message[:2] == "火山":
        await msg.reply(text= chat_vloces("你好") )


# @bot.private_event()
# async def on_private_message(msg: PrivateMessage):
#     _log.info(msg)
#     if msg.raw_message == "测试":
#         await bot.api.post_private_msg(msg.user_id, text="NcatBot 测试成功喵~")


if __name__ == "__main__":
    bot.run(reload=False)