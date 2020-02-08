# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger


def set_globals(owf_instance, *args):
    """
    Set a global variable to a value.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(args) < 2:
        owf_instance.logger.handle("Bad usage", Logger.ERROR)
        owf_instance.logger.handle("Usage: setg option_name value", Logger.INFO)
    else:
        owf_instance.global_options.update({args[0].upper(): args[1]})
        msg = "{} ==> {}".format(args[0].upper(), args[1])
        owf_instance.logger.handle(msg)
        if isinstance(owf_instance.current_module, AModule):
            for option in owf_instance.current_module.options:
                if option["Name"].upper() == args[0].upper():
                    option["Value"] = args[1]
        owf_instance.update_completer_global_options_list()
