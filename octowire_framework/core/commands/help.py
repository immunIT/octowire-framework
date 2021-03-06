# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


def owf_help(owf_instance, *args):
    """
    Print framework help on the console.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    print("\nCore Commands")
    print("=============")
    formatted_commands = []
    for cmd_name, cmd_obj in owf_instance.dispatcher.commands.items():
        formatted_commands.append(
            {
                "Command": cmd_name,
                "Description": cmd_obj["descr"]
            }
        )
    owf_instance.logger.print_tabulate(formatted_commands, headers={"name": "Name", "descr": "Description"})
