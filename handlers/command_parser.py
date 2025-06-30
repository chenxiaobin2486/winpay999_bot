# handlers/command_parser.py

import re
from handlers.settings import (
    set_rate,
    set_exchange_rate,
    set_cut_time,
    cancel_cut_time,
    get_cut_time,
    delete_bill,
)
from handlers.permissions import (
    add_operator,
    remove_operator,
    list_operators,
)
from handlers.billing import add_entry
from handlers.wallet_check import is_wallet_address
from telegram import Update
from utils.auth import is_authorized

def parse_command(update: Update):
    message = update.effective_message
    text = message.text.strip()
    group_id = str(update.effective_chat.id)
    user_name = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name

    # 空指令
    if text in ("账单", "+0"):
        return add_entry(group_id, user_name, "+0")

    # 设置费率（支持“设置费率12”、“设置入款费率1.2%”、“设置出款费率0.5”）
    if text.startswith("设置费率"):
        try:
            num = float(text.replace("设置费率", "").replace("%", ""))
            return set_rate(group_id, "入款费率", num / 100)
        except:
            return "⚠️ 设置费率失败，格式应为：设置费率12"

    if text.startswith("设置入款费率"):
        try:
            num = float(text.replace("设置入款费率", "").replace("%", ""))
            return set_rate(group_id, "入款费率", num / 100)
        except:
            return "⚠️ 设置失败"

    if text.startswith("设置出款费率"):
        try:
            num = float(text.replace("设置出款费率", "").replace("%", ""))
            return set_rate(group_id, "出款费率", num / 100)
        except:
            return "⚠️ 设置失败"

    # 设置汇率（支持“设置汇率7.2”、“设置入款汇率”、“设置出款汇率”）
    if text.startswith("设置汇率"):
        try:
            num = float(text.replace("设置汇率", ""))
            return set_exchange_rate(group_id, "入款汇率", num)
        except:
            return "⚠️ 设置失败"

    if text.startswith("设置入款汇率"):
        try:
            num = float(text.replace("设置入款汇率", ""))
            return set_exchange_rate(group_id, "入款汇率", num)
        except:
            return "⚠️ 设置失败"

    if text.startswith("设置出款汇率"):
        try:
            num = float(text.replace("设置出款汇率", ""))
            return set_exchange_rate(group_id, "出款汇率", num)
        except:
            return "⚠️ 设置失败"

    # 设置日切时间（如 设置日切08:00）
    if text.startswith("设置日切"):
        time_str = text.replace("设置日切", "")
        return set_cut_time(group_id, time_str)

    # 取消日切
    if text.startswith("取消日切") or text.startswith("取消账单日切"):
        return cancel_cut_time(group_id)

    # 查看当前日切时间
    if text in ("日切", "查看日切"):
        return get_cut_time(group_id)

    # 删除账单
    if text == "删除账单":
        return delete_bill(group_id)

    # 设置操作人
    if text.startswith("设置操作人@"):
        username = text.replace("设置操作人", "")
        return add_operator(group_id, username)

    if text.startswith("删除操作人@"):
        username = text.replace("删除操作人", "")
        return remove_operator(group_id, username)

    if text in ("查看操作人", "操作人"):
        return list_operators(group_id)

    # 钱包地址或金额类自动识别，交由 billing.py 处理
    return add_entry(group_id, user_name, text)
