from importlib import import_module


def get_handle(path):
    arg = path.split(".")
    try:
        module = import_module(arg[0])
        handle = getattr(module, arg[1])
    except:
        handle = None

    return handle
