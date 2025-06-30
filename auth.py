# utils/auth.py

from telegram import Update
from database.memory_db import db

def is_authorized(update: Update) -> bool:
    """
    只有被添加为「操作人」的用户才能用机器人。
    私聊、群聊都适用：只要在该 chat_id 下的 operators 列表里，就放行，否则拒绝。
    """
    chat_id = update.effective_chat.id
    username = update.effective_user.username or ""
    # 从数据库里读出这个 chat_id 的操作人列表（初始为空列表）
    operators = db.get(f"operators:{chat_id}") or []

    if username in operators:
        return True

    # 拒绝消息
    update.message.reply_text("❌ 你没有权限，只有操作人可以使用本机器人。")
    return False
