# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import copy
import serial
import traceback
from octowire_framework.core.utils.Validator import Validator
from octowire_framework.module.AModule import AModule
from octowire.utils.Logger import Logger
from octowire.octowire import Octowire

def run_module(owf_instance, *args):
    """
    Check all arguments and run the selected module.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    if isinstance(owf_instance.current_module, AModule):
        # Create a backup of both options and advanced_options dict
        # (to keep values readability after the Validator's call)
        b_options = copy.deepcopy(owf_instance.current_module.options)
        b_advanced_options = copy.deepcopy(owf_instance.current_module.advanced_options)
        try:
            opt_checked = Validator().check_args(owf_instance.current_module.options)
            adv_checked = Validator().check_args(owf_instance.current_module.advanced_options)
            if opt_checked and adv_checked:
                try:
                    owf_instance.current_module.run()
                    # Close the serial instance after module completion
                    if isinstance(owf_instance.current_module.owf_serial, serial.Serial):
                        # Check if the serial connection is not closed
                        if owf_instance.current_module.owf_serial.is_open:
                            # Return into text mode before closing serial_instance
                            octowire_base = Octowire(serial_instance=owf_instance.current_module.owf_serial)
                            octowire_base.ensure_text_mode()
                            owf_instance.current_module.owf_serial.close()
                            owf_instance.current_module.owf_serial = None
                except KeyboardInterrupt:
                    pass
        except ValueError as err:
            owf_instance.logger.handle(err, Logger.ERROR)
        except Exception as err:
            owf_instance.logger.handle("{}: {}".format(type(err).__name__, str(err)))
        except:
            owf_instance.logger.handle("Error running module", Logger.ERROR)
            traceback.print_exc()
        finally:
            # Restoring the dictionaries backup for values readability
            owf_instance.current_module.options = copy.deepcopy(b_options)
            owf_instance.current_module.advanced_options = copy.deepcopy(b_advanced_options)
