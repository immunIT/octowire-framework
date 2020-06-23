# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


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
    if _check_args(owf_instance, *args):
        if args[0] == "modules":
            print("\n================")
            print("| Modules list |")
            print("================")
            formatted_modules = []
            # Show available modules in the selected category
            try:
                for module in owf_instance.modules:
                    if args[1] == module["path"].split("/")[0]:
                        formatted_modules.append({"Path": module["path"],
                                                  "Description": module["class"](owf_instance.config).meta["description"]})
                if len(formatted_modules) == 0:
                    owf_instance.logger.handle(f"No module found in the '{args[1]}' category.",
                                               owf_instance.logger.ERROR)
                    return
            # Show all installed modules
            except IndexError:
                for module in owf_instance.modules:
                    formatted_modules.append({"Path": module["path"],
                                              "Description": module["class"](owf_instance.config).meta["description"]})
            owf_instance.logger.print_tabulate(formatted_modules,
                                               headers={"Path": "Path", "Description": "Description"})
        elif args[0] == "config":
            print("\n================")
            print("|    Config    |")
            print("================")
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
