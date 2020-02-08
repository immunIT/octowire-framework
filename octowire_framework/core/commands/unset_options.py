# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger


def unset_options(owf_instance, *args):
    """
    Unset a context-specific variable.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(args) < 1:
        owf_instance.logger.handle("Bad usage", Logger.ERROR)
        owf_instance.logger.handle("Usage: unset option_name", Logger.INFO)
    else:
        if isinstance(owf_instance.current_module, AModule):
            for option in owf_instance.current_module.options:
                if option["Name"].upper() == args[0].upper():
                    option["Value"] = ""
                    msg = "{} ==> ".format(option["Name"])
                    owf_instance.logger.handle(msg)
                    break
            else:
                for option in owf_instance.current_module.advanced_options:
                    if option["Name"].upper() == args[0].upper():
                        option["Value"] = ""
                        msg = "{} ==> ".format(option["Name"])
                        owf_instance.logger.handle(msg)
                        break
                else:
                    owf_instance.logger.handle("Option does not exist", Logger.ERROR)
