# database/memory_db.py

# 全局内存存储
_db_store = {}

def get(key: str):
    """
    获取指定 key 的值，默认不存在就返回 None。
    """
    return _db_store.get(key)

def set(key: str, value):
    """
    设置指定 key 的值，会覆盖原来的数据。
    """
    _db_store[key] = value

def delete(key: str):
    """
    删除指定 key（可选）。
    """
    if key in _db_store:
        del _db_store[key]
