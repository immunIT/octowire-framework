# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


from octowire.utils.Logger import Logger
from prompt_toolkit.styles import Style


def set_config(owf_instance, *args):
    """
    Set a config variable to a value.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if len(args) < 3:
        owf_instance.logger.handle("Bad usage", Logger.ERROR)
        owf_instance.logger.handle("Usage: setc SECTION key value", Logger.INFO)
    else:
        if not owf_instance.config.has_section(args[0]):
            owf_instance.logger.handle("Config section '{}' does not exist".format(args[0]), Logger.ERROR)
        else:
            if not owf_instance.config.has_option(args[0], args[1]):
                owf_instance.logger.handle("Value '{}' does not exist in section '{}'"
                                           .format(args[1], args[0]), Logger.ERROR)
            else:
                owf_instance.config[args[0]][args[1]] = args[2]
            if args[0] == "THEME":
                owf_instance.prompt_style = Style.from_dict({
                    # User input (default text), no value = system default.
                    '': owf_instance.config['THEME']['user_input'],

                    # Prompt.
                    'base': owf_instance.config['THEME']['base'],
                    'pound': owf_instance.config['THEME']['pound'],
                    'module': owf_instance.config['THEME']['module'],
                    'category': owf_instance.config['THEME']['category'],
                })
            owf_instance.logger.handle("Please use the 'save' command to set the new configuration permanently",
                                       Logger.USER_INTERACT)
