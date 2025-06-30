import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

from handlers.command_parser import handle_message  # 确保路径正确
from utils.auth import is_authorized                # 如果你有权限控制模块

# 加载 .env 环境变量（需要 pip install python-dotenv）
from dotenv import load_dotenv
load_dotenv()

# 从环境变量中读取 TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# 创建机器人应用
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 消息总路由器
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 忽略非文本消息
    if not update.message or not update.message.text:
        return

    # 忽略频道消息
    if update.message.chat.type == "channel":
        return

    # 可选：你也可以加权限检查
    # if not is_authorized(update.effective_user.username):
    #     return

    # 转交给主处理函数
    await handle_message(update, context)

# 添加处理器：只处理文本、非命令消息
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

# 启动机器人
if __name__ == '__main__':
    print("🤖 Bot is running...")
    app.run_polling()
