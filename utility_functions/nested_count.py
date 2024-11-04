def nested_count(d):
    n = sum([nested_count(v) if isinstance(v, dict) else 1 for v in d.values()])
    return n
