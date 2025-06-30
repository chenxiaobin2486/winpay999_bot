import re
from telegram import Update
from telegram.ext import ContextTypes
from database.memory_db import db

# 钱包地址正则（简单示例）
ADDRESS_REGEX = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b|\b[0x]?[a-fA-F0-9]{40,64}\b"

async def check_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    match = re.search(ADDRESS_REGEX, text)
    if not match:
        return

    address = match.group(0)
    sender = update.effective_user.username or update.effective_user.full_name
    group_id = update.effective_chat.id

    key = f"wallet:{group_id}:{address}"
    record = db.get(key) or {
        "count": 0,
        "last_user": None,
    }

    record["count"] += 1
    result = (
        f"验证地址：\n{address}\n"
        f"验证次数：{record['count']}\n"
        f"上次发送人：@{record['last_user'] or '无'}\n"
        f"本次发送人：@{sender}"
    )

    record["last_user"] = sender
    db.set(key, record)

    await update.message.reply_text(result)
