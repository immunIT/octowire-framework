# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import serial
import traceback
from octowire_framework.core.utils.Validator import Validator
from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger


def run_module(owf_instance, *args):
    """
    Check all arguments and run the selected module.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if isinstance(owf_instance.current_module, AModule):
        try:
            opt_checked = Validator().check_args(owf_instance.current_module.options)
            adv_checked = Validator().check_args(owf_instance.current_module.advanced_options)
            if opt_checked and adv_checked:
                try:
                    owf_instance.current_module.run()
                    # Close the serial instance after module completion
                    if isinstance(owf_instance.current_module.owf_serial, serial.Serial):
                        owf_instance.current_module.owf_serial.close()
                        owf_instance.current_module.owf_serial = None
                except KeyboardInterrupt:
                    pass
        except (ValueError, Exception) as err:
            owf_instance.logger.handle(err, Logger.ERROR)
        except:
            owf_instance.logger.handle("Error running module", Logger.ERROR)
            traceback.print_exc()
