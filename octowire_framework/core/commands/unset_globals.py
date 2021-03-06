# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


from octowire.utils.Logger import Logger


def unset_globals(owf_instance, *args):
    """
    Unset a global variable.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(args) < 1:
        owf_instance.logger.handle("Bad usage", Logger.ERROR)
        owf_instance.logger.handle("Usage: unsetg option_name", Logger.INFO)
    else:
        try:
            owf_instance.global_options.pop(args[0].upper())
            msg = "'{}' successfully unset".format(args[0].upper())
            owf_instance.logger.handle(msg)
            owf_instance.update_unset_global_completer()
        except KeyError:
            owf_instance.logger.handle("'{}' is not declared as a global variable".format(args[0]), Logger.ERROR)

