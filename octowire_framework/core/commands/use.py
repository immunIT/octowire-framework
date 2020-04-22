# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire.utils.Logger import Logger


def _print_usage(owf_instance, *args):
    """
    Print 'use' command usage.
    :param owf_instance: Octowire framework instance (self).
    :return: Nothing
    """
    owf_instance.logger.handle("Bad usage", Logger.ERROR)
    owf_instance.logger.handle("Usage: use <module_name>", Logger.INFO)


def _check_args(owf_instance, *args):
    """
    Check the length of 'use' command arguments and their validity.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs ('use' command arguments).
    :return: bool
    """
    if len(args) < 1:
        _print_usage(owf_instance)
        return False
    if args[0] == "":
        _print_usage(owf_instance)
        return False
    return True


def use(owf_instance, *args):
    """
    Method used to select a specific module.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if _check_args(owf_instance, *args):
        for module in owf_instance.modules:
            if module["path"] == args[0]:
                # Check module dependencies
                new_module = module["class"](owf_instance.config)
                if new_module._check_dependencies():
                    # Save current module in the history before switching
                    if owf_instance.current_module is not None and owf_instance.current_module_name != module["path"]:
                        owf_instance.modules_history.append({"path": owf_instance.current_module_name,
                                                             "class": owf_instance.current_module})
                    owf_instance.current_module = new_module
                    owf_instance.current_module_name = module["path"]
                    # Set module option from global option
                    for global_option_name, global_option_value in owf_instance.global_options.items():
                        for module_option in owf_instance.current_module.options:
                            if global_option_name.upper() == module_option["Name"].upper():
                                module_option["Value"] = global_option_value
                    owf_instance.update_completer_options_list()
                break
        else:
            owf_instance.logger.handle("Module not found", Logger.ERROR)
