# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import pkg_resources
import serial

from abc import ABC, abstractmethod
from importlib import import_module

from octowire.utils.Logger import Logger
from octowire.utils.serial_utils import detect_and_connect
from octowire_framework.core.config import load_config
from octowire_framework.core.utils.get_amodule_class import get_amodule_class


class AModule(ABC):
    def __init__(self, owf_config):
        self.logger = Logger()
        self.config = owf_config
        self.owf_serial = None
        self.meta = {
            'name': '',
            'version': '',
            'description': '',
            'author': ''
        }
        self.options = {}
        self.advanced_options = {}
        self.dependencies = []

    def __name__(self):
        """
        Simply return the module name
        :return: Module name
        :rtype: string
        """
        return self.meta["name"]

    def _check_dependencies(self):
        """
        Verify the module dependencies.
        :return: Bool
        """
        update_msg = "Please run 'owfupdate' in your terminal to install the latest module version"
        for dependency in self.dependencies:
            req = pkg_resources.Requirement.parse(dependency)
            try:
                pkg_resources.get_provider(req)
            except pkg_resources.RequirementParseError as err:
                self.logger.handle(err, self.logger.ERROR)
                return False
            except pkg_resources.DistributionNotFound:
                self.logger.handle("The '{}' distribution was not found and is required "
                                   "by the module".format(dependency), self.logger.ERROR)
                self.logger.handle(update_msg, self.logger.USER_INTERACT)
                return False
            except pkg_resources.VersionConflict:
                dist = pkg_resources.get_distribution(req.name)
                Logger().handle("Version conflict: '{}' is required. Version '{}' is currently "
                                "installed".format(dependency, dist.version), Logger().ERROR)
                self.logger.handle(update_msg, self.logger.USER_INTERACT)
                return False
            # Recursively check sub_module dependencies
            if req.name == "octowire-lib":
                sub_module = import_module("octowire")
            else:
                sub_module = import_module(req.name)
            for d_amodule_class in get_amodule_class(sub_module, req.name, AModule):
                amodule_class = d_amodule_class["class"](load_config())
                if not amodule_class._check_dependencies():
                    return False
        return True

    def connect(self):
        """
        Connect to the Octowire using configured options.
        If owf_serial is a valid serial instance, skip the connexion part (manage by a parent module).
        :return: Nothing
        """
        if not isinstance(self.owf_serial, serial.Serial) or not self.owf_serial.is_open:
            if self.config["OCTOWIRE"].getint("detect"):
                self.owf_serial = self._manage_connection()
            else:
                port = self.config["OCTOWIRE"]["port"]
                baudrate = self.config["OCTOWIRE"].getint("baudrate")
                timeout = self.config["OCTOWIRE"].getint("read_timeout")
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

    def show_options(self, options):
        """
        Print available options for the module to the console.
        :return: Nothing
        """
        formatted_options = []
        if len(options) > 0:
            self.print_meta()
            for option_name, option in options.items():
                if option["Default"] != "" and option["Value"] == "":
                    formatted_options.append(
                        {
                            'Name': option_name,
                            'Value': option["Default"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
                else:
                    formatted_options.append(
                        {
                            'Name': option_name,
                            'Value': option["Value"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
            self.logger.print_tabulate(formatted_options, headers={"Name": "Name", "Value": "Value",
                                                                   "Required": "Required",
                                                                   "Description": "Description"})

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

