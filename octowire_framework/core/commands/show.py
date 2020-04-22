# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger


def _print_usage(owf_instance, *args):
    """
    Print 'show' command usage.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    owf_instance.logger.handle("Bad usage", Logger.ERROR)
    owf_instance.logger.handle("Usage: show modules|options|advanced|config|global", Logger.INFO)


def _check_args(owf_instance, *args):
    """
    Check the length of 'show' command arguments and their validity.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs (show command argument).
    :return: bool
    """
    if len(args) < 1:
        _print_usage(owf_instance)
        return False
    if args[0] not in ["modules", "options", "advanced", "config", "global"]:
        _print_usage(owf_instance)
        return False
    return True


def show(owf_instance, *args):
    """
    Displays list of modules, including options/advanced options or global configuration depending on arguments.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    # TODO: print by category separately
    if _check_args(owf_instance, *args):
        if args[0] == "modules":
            print("\n================")
            print("| Modules list |")
            print("================\n")
            formatted_modules = []
            for module in owf_instance.modules:
                formatted_modules.append({"Path": module["path"],
                                          "Description": module["class"](owf_instance.config).meta["description"]})
            owf_instance.logger.print_tabulate(formatted_modules,
                                               headers={"Path": "Path", "Description": "Description"})
        elif args[0] == "config":
            print("\n================")
            print("|    Config    |")
            print("================\n")
            for section in owf_instance.config:
                print("\n[{}]".format(section))
                for key in owf_instance.config[section]:
                    print("{} = {}".format(key, owf_instance.config[section][key]))
        elif args[0] == "global":
            print("\n==================")
            print("| Global options |")
            print("==================\n")
            for key, value in owf_instance.global_options.items():
                print(f"{key} ==> {value}")
        elif args[0] == "options":
            if isinstance(owf_instance.current_module, AModule):
                owf_instance.current_module.show_options(owf_instance.current_module.options)
        elif args[0] == "advanced":
            if isinstance(owf_instance.current_module, AModule):
                owf_instance.current_module.show_options(owf_instance.current_module.advanced_options)
        else:
            _print_usage(owf_instance)
