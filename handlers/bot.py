import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import TELEGRAM_TOKEN
from handlers.command_parser import handle_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 所有文本消息都会传给 handle_message 函数
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 机器人已启动")
    app.run_polling()
