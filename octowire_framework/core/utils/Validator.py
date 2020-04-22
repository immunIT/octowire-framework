# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import os

from octowire.utils.Logger import Logger


class Validator:
    """
    This class checks module options, verifying whether format is valid.
    """
    def __init__(self):
        self.logger = Logger()

    def _args_validator(self, option_name, option):
        """
        Check argument type validity & convert to the specified format.
        :param option: Module option.
        :return: bool
        """
        try:
            if option["Type"] == "int":
                if not isinstance(option["Value"], int):
                    option["Value"] = int(option["Value"], 10)
            elif option["Type"] == "hex":
                if not isinstance(option["Value"], int):
                    option["Value"] = int(option["Value"], 16)
            elif option["Type"] == "bool":
                if not isinstance(option["Value"], bool):
                    if str(option["Value"]).upper() == "FALSE":
                        option["Value"] = False
                    elif str(option["Value"]).upper() == "TRUE":
                        option["Value"] = True
                    else:
                        raise ValueError("option {}: True or False are expected.".format(option["Value"]))
            # File to read
            elif option["Type"] == "file_r":
                if not os.access(option["Value"], os.R_OK):
                    raise Exception("{}: file does not exist or permission denied.".format(option["Value"]))
            # File to write
            elif option["Type"] == "file_w":
                dirname = os.path.dirname(option["Value"])
                dirname = './' if dirname == '' else dirname
                if not os.access(dirname, os.W_OK):
                    raise Exception("{}: permission denied.".format(option["Value"]))
            if option["Value"] == "None":
                option["Value"] = None
        except ValueError:
            self.logger.handle("Value error: {} is not a valid {}".format(option_name, option["Type"]))
            return False
        return True

    def check_args(self, options_dict):
        """
        Check whether all arguments are defined by user, setting them to their default values otherwise (if available).
        :param options_dict: Module options dictionary.
        :return: bool
        """
        if len(options_dict) > 0:
            for option_name, option in options_dict.items():
                if option["Value"] == "":
                    if option["Default"] == "" and option["Required"]:
                        self.logger.handle("OptionValidationError: The following options failed to validate: {}."
                                           .format(option_name), Logger.ERROR)
                        return False
                    else:
                        option["Value"] = option["Default"]
                if not self._args_validator(option_name, option):
                    return False
        return True
