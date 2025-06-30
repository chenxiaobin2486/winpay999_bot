# handlers/billing.py

from database.memory_db import db
from handlers.settings import get_today_key
from handlers.wallet_check import is_wallet_address
from handlers.permissions import is_operator

def add_entry(group_id, user_name, text):
    if not is_operator(group_id, user_name):
        return "⛔ 仅限操作人使用本功能"

    today_key = get_today_key(group_id)
    if group_id not in db:
        db[group_id] = {}
    if today_key not in db[group_id]:
        db[group_id][today_key] = {"入款": [], "下发": [], "出款": [], "代付出款": []}

    entry = parse_entry(text)
    if entry:
        db[group_id][today_key][entry["类型"]].append(entry)
        if entry["类型"] == "地址验证":
            return None  # 不输出账单
        return format_bill(group_id)
    return "⚠️ 指令格式错误，请重新输入"

def parse_entry(text):
    text = text.replace(" ", "").replace("：", ":")
    if text.startswith("入款"):
        try:
            amount = float(text[2:])
            return {"类型": "入款", "原始金额": amount}
        except:
            return None
    if text.startswith("下发"):
        try:
            amount = float(text[2:])
            return {"类型": "下发", "原始金额": amount}
        except:
            return None
    if text.startswith("出款"):
        try:
            amount = float(text[2:])
            return {"类型": "出款", "原始金额": amount}
        except:
            return None
    if is_wallet_address(text):
        return {
            "类型": "地址验证",
            "地址": text
        }
    return None

def format_bill(group_id):
    from handlers.settings import get_setting

    today_key = get_today_key(group_id)
    records = db.get(group_id, {}).get(today_key, {"入款": [], "下发": [], "出款": [], "代付出款": []})

    入款费率 = get_setting(group_id, "入款费率", 0)
    入款汇率 = get_setting(group_id, "入款汇率", 7.0)
    出款费率 = get_setting(group_id, "出款费率", 0)
    出款汇率 = get_setting(group_id, "出款汇率", 7.0)

    result = []

    # 入款记录
    result.append(f"📥 入款（{len(records['入款'])}笔）：")
    total_in = 0
    for r in records["入款"]:
        raw = r["原始金额"]
        u = raw * (1 - 入款费率) / 入款汇率
        result.append(f"{raw} * {1 - 入款费率:.3f} / {入款汇率} = {u:.2f}")
        total_in += raw

    result.append(f"总入款：{total_in}")
    result.append(f"入款费率：{入款费率 * 100:.1f}%")
    result.append(f"入款汇率：{入款汇率}")
    final_in = total_in * (1 - 入款费率)
    in_u = final_in / 入款汇率
    result.append(f"应下发金额：{final_in:.2f} / {入款汇率} = {in_u:.2f}u")

    # 下发记录
    result.append(f"\n📤 下发（{len(records['下发'])}笔）：")
    total_out = 0
    for r in records["下发"]:
        raw = r["原始金额"]
        u = raw * (1 + 出款费率) / 出款汇率
        result.append(f"{raw} * {1 + 出款费率:.3f} / {出款汇率} = {u:.2f}")
        total_out += raw

    final_out = total_out * (1 + 出款费率)
    out_u = final_out / 出款汇率
    result.append(f"总下发金额：{total_out}")
    result.append(f"出款费率：{出款费率 * 100:.1f}%")
    result.append(f"出款汇率：{出款汇率}")
    result.append(f"总下发：{final_out:.2f} / {出款汇率} = {out_u:.2f}u")

    # 未下发金额
    diff = in_u - out_u
    result.append(f"未下发金额：{diff:.2f}u")

    # 出款（代付）记录
    if records["出款"]:
        total_proxy = sum([r["原始金额"] for r in records["出款"]])
        result.append(f"\n💸 代付出款：{total_proxy}")

    return "\n".join(result)
