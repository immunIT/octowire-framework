# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire.utils.Logger import Logger


def _print_usage(owf_instance):
    """
    Print 'search' command usage.
    :param owf_instance: Octowire framework instance (self).
    :return: Nothing
    """
    owf_instance.logger.handle("Bad usage", Logger.ERROR)
    owf_instance.logger.handle("Usage: search [keywords]", Logger.INFO)


def _check_args(owf_instance, *args):
    """
    Check the length of 'search' command arguments and their validity.
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


def search(owf_instance, *args):
    """
    Method used to find a module that matches the keywords.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    matching_modules = []
    if _check_args(owf_instance, *args):
        for module in owf_instance.modules:
            # Check if keywords are in path or description
            module_string = f"{module['path']} {module['class'](owf_instance.config).meta['description']}"
            if all(x in module_string for x in args[:]):
                matching_modules.append({"Path": module["path"],
                                         "Description": module["class"](owf_instance.config).meta["description"]})
        print("\n====================")
        print("| Matching Modules |")
        print("====================")
        owf_instance.logger.print_tabulate(matching_modules,
                                           headers={"Path": "Path", "Description": "Description"})
