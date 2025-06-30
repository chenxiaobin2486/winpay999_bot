from telegram import Update
from telegram.ext import ContextTypes
from database.memory_db import db
from utils.auth import is_authorized

def is_operator(update: Update) -> bool:
    username = update.effective_user.username
    chat_id = update.effective_chat.id
    operators = db.get(f"operators:{chat_id}") or []

    if username in operators:
        return True
    else:
        update.message.reply_text("无权限，操作人限定")
        return False

async def add_operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return

    try:
        username = context.args[0].lstrip("@")
        chat_id = update.effective_chat.id
        operators = db.get(f"operators:{chat_id}") or []
        if username not in operators:
            operators.append(username)
        db.set(f"operators:{chat_id}", operators)
        await update.message.reply_text(f"操作成功：设置操作人@{username}")
    except:
        await update.message.reply_text("格式错误，应为：设置操作人 @用户名")

async def remove_operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return

    try:
        username = context.args[0].lstrip("@")
        chat_id = update.effective_chat.id
        operators = db.get(f"operators:{chat_id}") or []
        if username in operators:
            operators.remove(username)
        db.set(f"operators:{chat_id}", operators)
        await update.message.reply_text(f"操作成功：删除操作人@{username}")
    except:
        await update.message.reply_text("格式错误，应为：删除操作人 @用户名")

async def list_operators(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    operators = db.get(f"operators:{chat_id}") or []
    if not operators:
        await update.message.reply_text("当前未设置操作人")
    else:
        op_list = "\n".join(f"@{op}" for op in operators)
        await update.message.reply_text(f"当前操作人列表：\n{op_list}")
