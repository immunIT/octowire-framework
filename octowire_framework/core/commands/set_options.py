# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger


def set_options(owf_instance, *args):
    """
    Sets a context-specific variable to a value.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(args) < 2:
        owf_instance.logger.handle("Bad usage", Logger.ERROR)
        owf_instance.logger.handle("Usage: set option_name value", Logger.INFO)
    else:
        if isinstance(owf_instance.current_module, AModule):
            # Standard options
            for option_name, option in owf_instance.current_module.options.items():
                if option_name.upper() == args[0].upper():
                    option["Value"] = args[1]
                    msg = "{} ==> {}".format(option_name, args[1])
                    owf_instance.logger.handle(msg)
                    break
            else:
                # Advanced options
                for option_name, option in owf_instance.current_module.advanced_options.items():
                    if option_name.upper() == args[0].upper():
                        option["Value"] = args[1]
                        msg = "{} ==> {}".format(option_name, args[1])
                        owf_instance.logger.handle(msg)
                        break
                else:
                    owf_instance.logger.handle("Option does not exist", Logger.ERROR)
