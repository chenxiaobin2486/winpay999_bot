from telegram import Update
from telegram.ext import ContextTypes
from utils import (
  is_authorized, parse_amount, get_today_key,
  save_record, format_bill, reset_today_data,
  delete_today_data, record_address_usage,
  get_cutoff_time, set_cutoff_time,
  remove_last_record, calculate_settlement,
  set_fee_rate, set_exchange_rate,
  set_out_fee_rate, set_out_exchange_rate,
  set_operator, remove_operator,
  list_operators, get_operator_username,
  get_last_address_info, get_outback_settlement,
  record_outback
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message = update.message
  if not message:
    return

  text = message.text.strip()
  user = update.effective_user
  chat_id = message.chat.id
  username = user.username or f"id_{user.id}"
  is_group = message.chat.type in ['group', 'supergroup']

  # 非操作人不允许操作
  if is_group and not is_authorized(chat_id, username, only_check=True):
    return

  # 地址验证
  if len(text) >= 20 and all(c.isalnum() for c in text):
    count, last_user = record_address_usage(chat_id, text, username)
    await message.reply_text(
      f"验证地址：\n{text}\n"
      f"验证次数：{count}\n"
      f"上次发送人：@{last_user or '无'}\n"
      f"本次发送人：@{username}"
    )
    return

  # 开始/结束记账
  if text == "开始记账":
    get_today_key(chat_id, create=True)
    await message.reply_text("已开始记账")
    return
  if text == "结束记账":
    reset_today_data(chat_id)
    await message.reply_text("已结束并清空账目")
    return

  # 撤销操作
  if text in ["撤销", "撤销出款", "撤销下发"]:
    result = remove_last_record(chat_id, text)
    await message.reply_text(result)
    return

  # 删除账单
  if text == "删除账单":
    delete_today_data(chat_id)
    await message.reply_text("今日账单已删除")
    return

  # 查看账单
  if text in ["账单", "+0"]:
    bill = format_bill(chat_id)
    await message.reply_text(bill)
    return

  # 设置汇率与费率
  if text.startswith("设置汇率"):
    result = set_exchange_rate(chat_id, text)
    await message.reply_text(result)
    return
  if text.startswith("设置费率"):
    result = set_fee_rate(chat_id, text)
    await message.reply_text(result)
    return
  if text.startswith("设置出款汇率"):
    result = set_out_exchange_rate(chat_id, text)
    await message.reply_text(result)
    return
  if text.startswith("设置出款费率"):
    result = set_out_fee_rate(chat_id, text)
    await message.reply_text(result)
    return

  # 日切相关
  if text.startswith("账单日切"):
    result = set_cutoff_time(chat_id, text)
    await message.reply_text(result)
    return
  if text == "取消账单日切":
    result = set_cutoff_time(chat_id, "取消")
    await message.reply_text(result)
    return
  if text == "查看日切":
    result = get_cutoff_time(chat_id)
    await message.reply_text(result)
    return

  # 操作人管理
  if text.startswith("设置操作人@"):
    result = set_operator(chat_id, text)
    await message.reply_text(result)
    return
  if text.startswith("删除操作人@"):
    result = remove_operator(chat_id, text)
    await message.reply_text(result)
    return
  if text == "查看操作人":
    result = list_operators(chat_id)
    await message.reply_text(result)
    return

  # 出款应收
  if text == "应收出款":
    result = get_outback_settlement(chat_id)
    await message.reply_text(result)
    return

  # 已回出款
  if text.startswith("已回+"):
    result = record_outback(chat_id, text)
    await message.reply_text(result)
    return

  # 入款、下发、出款金额记录
  if text.startswith("入款") or text.startswith("+") or parse_amount(text):
    result = save_record(chat_id, text, username)
    await message.reply_text(result)
    if text.startswith("下发"):
      bill = format_bill(chat_id)
      await message.reply_text(bill)
    return
