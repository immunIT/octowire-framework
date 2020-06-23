# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


def back(owf_instance, *args):
    """
    Move back from the current context.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(owf_instance.modules_history) > 0:
        previous_module = owf_instance.modules_history.pop()
        owf_instance.current_module_name = previous_module["path"]
        owf_instance.current_module = previous_module["class"]
    else:
        if owf_instance.current_module is not None:
            owf_instance.current_module = None
            owf_instance.current_module_name = None
    owf_instance.update_set_global_completer()
    owf_instance.update_completer_options_list()
