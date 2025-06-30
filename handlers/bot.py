from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import command_parser
from config import TELEGRAM_TOKEN


async def start(update, context):
    await update.message.reply_text("✅ 机器人已启动，请发送指令。")


def run_bot():
    # 创建 Application 实例
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 启动命令
    app.add_handler(CommandHandler("start", start))

    # 主指令处理器（处理文本消息）
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_parser.handle_message))

    # 启动轮询
    print("🤖 正在启动 Telegram Bot ...")
    app.run_polling()
