# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


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
            for option_name, option in owf_instance.current_module.options.items():
                if option_name.upper() == args[0].upper():
                    option["Value"] = ""
                    msg = "{} ==> ".format(option_name)
                    owf_instance.logger.handle(msg)
                    break
            else:
                for option_name, option in owf_instance.current_module.advanced_options.items():
                    if option_name.upper() == args[0].upper():
                        option["Value"] = ""
                        msg = "{} ==> ".format(option_name)
                        owf_instance.logger.handle(msg)
                        break
                else:
                    owf_instance.logger.handle("Option does not exist", Logger.ERROR)
