# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from octowire.utils.serial_utils import detect_octowire


def detect(owf_instance, *args):
    """
    Run the 'detect_octowire' function from the octowire library utils.
    If detected, add the port to the configuration file. The 'save' command is
    needed if yo want to add it permanently.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    port = detect_octowire()
    if port:
        owf_instance.config["OCTOWIRE"]["port"] = port
        owf_instance.logger.handle("Octowire port configuration temporarily modified. Please use the 'save' command"
                                   " to set the new configuration permanently", owf_instance.logger.USER_INTERACT)
