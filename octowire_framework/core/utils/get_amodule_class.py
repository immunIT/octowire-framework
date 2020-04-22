import inspect


def get_amodule_class(imported_module, base_module_path, AModule):
    """
    This function return a dictionary that contains all AModule subclass belonging to module.
    :param imported_module: module instance. (from importlib.import_module)
    :param base_module_path: Base module path name (e.g. owfmodules.spi.device_id).
    :param AModule: The AModule class instance.
    :return:
    """
    modules = []
    for x in dir(imported_module):
        obj = getattr(imported_module, x)
        if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
            # Unsure that the class is not a class imported by the module
            if obj.__module__ == base_module_path:
                module_path = base_module_path.replace('owfmodules.', '').replace('.', '/')
                modules.append({"path": module_path, "class": obj})
    return modules
