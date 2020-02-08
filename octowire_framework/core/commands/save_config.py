# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


from pathlib import Path


def save_config(owf_instance, *args):
    """
    Save the current framework config into the owf.cfg file.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    owf_config_path = Path.home() / '.owf' / 'owf.cfg'
    with owf_config_path.open('w') as cfg_file:
        owf_instance.config.write(cfg_file)
