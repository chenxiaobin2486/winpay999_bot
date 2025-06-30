import re
from src.storage import add_entry

admins = {"Ajun56785678", "WinPay06_thomason"}

def is_admin(username: str) -> bool:
    return username in admins

def parse_command(text: str, sender: str) -> str:
    match = re.match(r"(入款|下發|出款)(\d+(?:\.\d+)?)", text)
    if match:
        action, amount = match.groups()
        amount = float(amount)
        add_entry(action, amount, sender)
        return f"✅ 已記錄：{action} {amount}"
    return "⚠️ 指令格式錯誤（如：入款1000）"
