def getNrFromArgs(args, key, default = None, condition = None):
    if key in args:
        value = int(args[key])
        if not condition or condition(value):
            return value
    return default
