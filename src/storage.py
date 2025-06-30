from datetime import datetime

entries = []

def add_entry(action: str, amount: float, sender: str):
    entries.append({
        "time": datetime.now().isoformat(),
        "action": action,
        "amount": amount,
        "sender": sender
    })

def record_entry():
    return entries
