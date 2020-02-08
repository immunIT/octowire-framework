# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import serial

from abc import ABC, abstractmethod

from octowire.utils.Logger import Logger
from octowire.utils.serial_utils import detect_and_connect


class AModule(ABC):
    def __init__(self, owf_config):
        self.name = None
        self.logger = Logger()
        self.config = owf_config
        self.owf_serial = None
        self.meta = {
            'name': '',
            'version': '',
            'description': '',
            'author': ''
        }
        self.options = []
        self.advanced_options = [
            {"Name": "octowire", "Value": "", "Required": True, "Type": "string",
             "Description": "Octowire hardware serial port", "Default": self.config["OCTOWIRE"]["port"]},
            {"Name": "baudrate", "Value": "", "Required": True, "Type": "int",
             "Description": "Octowire serial baudrate", "Default": self.config["OCTOWIRE"]["baudrate"]},
            {"Name": "timeout", "Value": "", "Required": True, "Type": "int",
             "Description": "Octowire read timeout", "Default": self.config["OCTOWIRE"]["read_timeout"]},
        ]

    def __name__(self):
        """
        Simply return the module name
        :return: Module name
        :rtype: string
        """
        return self.name

    def connect(self):
        """
        Connect to the Octowire using configured options.
        :return: Nothing
        """
        if self.get_option_value("detect_octowire"):
            self.owf_serial = self._manage_connection()
        else:
            port = self.get_advanced_option_value("octowire")
            baudrate = self.get_advanced_option_value("baudrate")
            timeout = self.get_advanced_option_value("timeout")
            self.owf_serial = self._manage_connection(auto_connect=False, octowire_port=port,
                                                      octowire_baudrate=baudrate, octowire_timeout=timeout)

    def _manage_connection(self, auto_connect=True, octowire_port=None, octowire_baudrate=None, octowire_timeout=1):
        """
        Manage connection to the Octowire hardware and return a serial instance.
        :param auto_connect: Automatically detect and connect to the octowire if set to True.
        :param octowire_port: The Octowire port (required if auto_connect is False).
        :param octowire_baudrate: The Octowire baudrate. Default=7372800 (required if auto_connect is False).
        :param octowire_timeout: The Octowire timeout. Default=1 (required if auto_connect is False).
        :return: Serial instance or None.
        """
        try:
            if auto_connect:
                return detect_and_connect()
            else:
                if not octowire_port:
                    self.logger.handle("If auto_detect is set to False, please specify the Octowire port.",
                                       self.logger.ERROR)
                    return None
                return serial.Serial(port=octowire_port, baudrate=octowire_baudrate, timeout=octowire_timeout)
        except serial.SerialException as err:
            self.logger.handle("Error during serial connection: {}".format(err))
            return None

    def get_advanced_option_value(self, option_name):
        """
        Return the value of a specific advanced option.
        :param option_name: The desired option name.
        :return: Option value.
        """
        for option in self.advanced_options:
            if option["Name"] == option_name:
                return option["Value"]
        else:
            raise UserWarning("Value {} not found in module options".format(option_name))

    def get_option_value(self, option_name):
        """
        Return the value of a specific option.
        :param option_name: The desired option name.
        :return: Option value.
        """
        for option in self.options:
            if option["Name"] == option_name:
                return option["Value"]
        else:
            raise UserWarning("Value {} not found in module options".format(option_name))

    def show_options(self):
        """
        Print available options for the module to the console.
        :return: Nothing
        """
        formatted_options = []
        if len(self.options) > 0:
            self.print_meta()
            for option in self.options:
                if option["Default"] != "" and option["Value"] == "":
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Default"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
                else:
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Value"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
            self.logger.print_tabulate(formatted_options, headers={"Name": "Name", "Description": "Description",
                                                                   "Value": "Value", "Required": "Required"})

    def show_advanced_options(self):
        """
        Print available advanced options for the module to the console.
        :return: Nothing
        """
        formatted_options = []
        if len(self.advanced_options) > 0:
            for option in self.advanced_options:
                if option["Default"] != "" and option["Value"] == "":
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Default"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
                else:
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Value"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
            self.logger.print_tabulate(formatted_options, headers={"Name": "Name", "Description": "Description",
                                                                   "Value": "Value", "Required": "Required"})

    def print_meta(self):
        """
        Print meta information of the module (author, module name, description).
        :return: Nothing
        """
        self.logger.handle('Author: {}'.format(self.meta['author']), Logger.HEADER)
        self.logger.handle('Module name: {}, version {}'.format(self.meta['name'], self.meta['version']), Logger.HEADER)
        self.logger.handle('Description: {}'.format(self.meta['description']), Logger.HEADER)

    @abstractmethod
    def run(self):
        """
        Main function prototype.
        """
        pass

