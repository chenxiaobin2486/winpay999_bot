import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from handlers import handle_message
from utils import is_authorized

# 从环境变量中读取 TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_DEFAULT_TOKEN_HERE")

# 创建机器人应用
app = ApplicationBuilder().token(BOT_TOKEN).build()

# 消息处理器
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 忽略非文本消息
    if not update.message or not update.message.text:
        return

    # 忽略频道消息
    if update.message.chat.type == "channel":
        return

    # 分发处理
    await handle_message(update, context)

# 添加处理器：所有文本消息
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_router))
app.add_handler(MessageHandler(filters.COMMAND, message_router))  # 兼容 /指令

# 启动机器人
if __name__ == '__main__':
    print("Bot is running...")
    app.run_polling()
