from ncatbot.core import BotClient, GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log
import jmcomic
import time
import re
import os
import asyncio

_log = get_log()

# 配置 NapCat
config.set_bot_uin("3865588265")  # 设置 bot qq 号 (必填)
config.set_root("1254795592")  # 设置 bot 超级管理员账号 (建议填写)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("")  # 设置 token (napcat 服务器的 token)

# 创建 jmcomic 配置对象
option = jmcomic.create_option_by_file(r'E:\code\python\JMComic-Crawler-Python-master\option.yml')

# PDF 保存路径（从 option.yml 中获取）
PDF_SAVE_DIR = r"D:\PDF"
if not os.path.exists(PDF_SAVE_DIR):
    os.makedirs(PDF_SAVE_DIR)

# 初始化 BotClient
bot = BotClient()

# 查找 PDF 文件的函数
async def find_pdf_file(comic_id):
    # 根据 option.yml 的配置，PDF 文件名为 <comic_id>.pdf
    pdf_filename = f"{comic_id}.pdf"
    pdf_path = os.path.join(PDF_SAVE_DIR, pdf_filename)
    
    # 等待文件生成（最多等待 10 秒）
    max_wait_time = 10
    wait_interval = 1
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        if os.path.exists(pdf_path):
            _log.info(f"找到 PDF 文件: {pdf_path}")
            return pdf_path
        _log.info(f"PDF 文件尚未生成，等待中... ({elapsed_time}/{max_wait_time} 秒)")
        await asyncio.sleep(wait_interval)
        elapsed_time += wait_interval
    
    _log.error(f"PDF 文件未找到: {pdf_path}")
    return None

# 监听群聊消息：提示用户输入漫画编号
@bot.group_event()
async def on_group_message_prompt(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message == "bot我想看本子":
        time.sleep(0.5)
        await msg.reply(text="请输入想看的本子号喵~(100000--999999)")

# 监听群聊消息：处理特定用户和群聊的命令
@bot.group_event()
async def on_group_message_command(msg: GroupMessage):
    group_uin = 464536404  # 指定群聊的账号
    user_uin = 1254795592  # 指定用户的账号
    if msg.group_id == group_uin and msg.user_id == user_uin and msg.raw_message == "waitwaitwait":
        time.sleep(0.5)
        await bot.api.post_group_msg(group_id=group_uin, text="灵感菇里菇里菇里我擦灵感菇灵感菇")

# 监听群聊消息：提取六位数字并下载漫画
@bot.group_event()
async def on_group_message_comic(msg: GroupMessage):
    _log.info(msg)
    
    # 使用正则表达式提取六位数字（100000 到 999999）
    comic_ids = re.findall(r'\b\d{6}\b', msg.raw_message)
    comic_ids = [cid for cid in comic_ids if 100000 <= int(cid) <= 999999]
    
    if not comic_ids:
        return  
    
    # 遍历所有找到的六位数字
    for comic_id in comic_ids:
        _log.info(f"找到漫画编号: {comic_id}")
        
        # 回复：正在下载
        await msg.reply(text=f"正在下载漫画 {comic_id}，请稍等喵~")
        
        try:
            option.download_album(comic_id)
        except Exception as e:
            _log.error(f"下载漫画 {comic_id} 时出错: {e}")
            await msg.reply(text=f"无法下载漫画编号 {comic_id}，请检查编号是否正确喵~")
            continue
        
        # 查找生成的 PDF 文件
        pdf_path = await find_pdf_file(comic_id)
        if not pdf_path:
            await msg.reply(text=f"无法找到漫画 {comic_id} 的 PDF 文件，下载可能失败喵~")
            continue
        
        # 发送 PDF 文件到群聊
        try:
            await bot.api.post_group_file(group_id=msg.group_id, file=pdf_path)
            await bot.api.post_group_msg(group_id=msg.group_id, text=f"已下载漫画 {comic_id}，喵~")
            _log.info(f"PDF 文件 {pdf_path} 已发送")
            
        except AttributeError as e:
            _log.error(f"发送 PDF 文件时出错，bot.api.post_group_file 不存在: {e}")
            try:
                await bot.api.post_group_msg(group_id=msg.group_id, text=f"已下载漫画 {comic_id}，喵~", file=pdf_path)
                _log.info(f"通过 post_group_msg 发送 PDF 文件 {pdf_path}")
            except Exception as e2:
                _log.error(f"使用 post_group_msg 发送 PDF 文件 {pdf_path} 也失败: {e2}")
                await msg.reply(text=f"发送漫画 {comic_id} 时出错: {e2}")
        except Exception as e:
            _log.error(f"发送 PDF 文件 {pdf_path} 时出错: {e}")
            await msg.reply(text=f"发送漫画 {comic_id} 时出错: {e}")
        
        
        await asyncio.sleep(1)


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        time.sleep(2)
        await bot.api.post_private_msg(msg.user_id, text="NcatBot 主人你好喵~")

if __name__ == "__main__":
    bot.run(reload=False)