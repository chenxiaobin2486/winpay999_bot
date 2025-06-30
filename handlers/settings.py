from telegram import Update
from telegram.ext import ContextTypes
from config import CONFIG
from database.memory_db import db
from handlers.permissions import is_operator

# 设置汇率
async def set_exchange_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    try:
        rate = float(context.args[0])
        db.set("exchange_rate", rate)
        await update.message.reply_text(f"操作成功：设置汇率{rate}")
    except:
        await update.message.reply_text("格式错误，应为：设置汇率 7.2")

# 设置费率
async def set_fee_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    try:
        percent = float(context.args[0])
        db.set("fee_rate", percent / 100)  # 存为小数
        await update.message.reply_text(f"操作成功：设置费率{percent}%")
    except:
        await update.message.reply_text("格式错误，应为：设置费率 0.5")

# 设置出款汇率
async def set_out_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    try:
        rate = float(context.args[0])
        db.set("out_rate", rate)
        await update.message.reply_text(f"操作成功：设置出款汇率{rate}")
    except:
        await update.message.reply_text("格式错误，应为：设置出款汇率 7.2")

# 设置出款费率
async def set_out_fee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    try:
        percent = float(context.args[0])
        db.set("out_fee", percent / 100)
        await update.message.reply_text(f"操作成功：设置出款费率{percent}%")
    except:
        await update.message.reply_text("格式错误，应为：设置出款费率 1.0")

# 设置日切时间
async def set_cut_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    try:
        time_str = context.args[0]
        assert ":" in time_str
        db.set("cut_time", time_str)
        await update.message.reply_text(f"操作成功：设置日切时间 {time_str}")
    except:
        await update.message.reply_text("格式错误，应为：日切 08:00")

# 取消日切
async def cancel_cut_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_operator(update): return
    db.set("cut_time", None)
    await update.message.reply_text("操作成功：取消账单日切")
