import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
from handlers.command_parser import handle_command
from utils.auth import is_authorized

# 加载 .env 环境变量
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://winpay999.onrender.com{WEBHOOK_PATH}"  # ← 替换为你 Render 的域名

# 创建 Flask app 与 Telegram 应用
flask_app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# 消息处理器
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    if not is_authorized(update):
        return
    await handle_command(update, context)

# 注册处理器
application.add_handler(MessageHandler(filters.TEXT, message_router))

# Flask 路由：Webhook 接收点
@flask_app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

# Render 主页访问返回提示
@flask_app.route("/", methods=["GET"])
def index():
    return "Telegram bot is running."

# 设置 Webhook（只执行一次）
@flask_app.before_first_request
def setup_webhook():
    application.bot.delete_webhook()
    application.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    flask_app.run(port=5000)
