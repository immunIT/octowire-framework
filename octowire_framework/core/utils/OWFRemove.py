# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import inspect
import os
import pathlib
import pkg_resources
import pkgutil
import platform
import subprocess
import sys
import tempfile

from importlib import import_module

from octowire.utils.Logger import Logger
from octowire_framework.core.utils.removal_script import script
from octowire_framework.module.AModule import AModule


class OWFRemove:
    def __init__(self):
        self.logger = Logger()
        self.not_removed = []

    def _get_installed_modules(self):
        """
        Return a dict of currently installed module(s).
        :return: A dict of currently installed module(s) {'module_name': 'version', ...}.
        """
        module_name = "owfmodules"
        installed_modules = {}
        try:
            package = import_module(module_name)
        except ImportError:
            return installed_modules
        for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
            try:
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                        installed_modules[module] = pkg_resources.get_distribution(module).version
            except ImportError:
                self.logger.handle('Error while dynamically importing package "{}"... Unable to removed it'
                                   .format(module), Logger.ERROR)
                self.not_removed.append(module)
        return installed_modules

    @staticmethod
    def _create_uninstall_script():
        """
        Create the uninstall script that will be executed in a subprocess.
        :return: Bool
        """
        file = tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False)
        file.write(script)
        file.close()
        return file.name

    def _manage_uninstall(self, package_name):
        """
        Removing the specified package (module or framework).
        :param package_name: The name of the package to install (module or framework).
        :return: Bool: True if successfully removed, False otherwise.
        """
        python_path = sys.executable
        current_dir = pathlib.Path().absolute()
        if package_name != "octowire-framework":
            pipes = subprocess.Popen([python_path, '-m', 'pip', 'uninstall', '-y', package_name],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = pipes.communicate()
            if pipes.returncode != 0:
                self.logger.handle("Error while removing the '{}' package: {}".format(package_name, stderr.strip()),
                                   Logger.ERROR)
                return False
            else:
                self.logger.handle("'{}' successfully removed".format(package_name), Logger.SUCCESS)
                return True
        else:
            # This method is necessary to remove the framework. Indeed, this allows releasing the owfremove
            # executable in order to removed it.
            script_name = self._create_uninstall_script()
            log_file = current_dir / "framework_remove.log"
            if platform.system() == "Windows":
                subprocess.Popen([python_path, script_name, '-p', str(os.getpid()), '-f', str(log_file)],
                                 creationflags=subprocess.DETACHED_PROCESS)
            else:
                subprocess.Popen([python_path, script_name, '-p', str(os.getpid()), '-f', str(log_file)])
            self.logger.handle("The remove of the framework was launched in background... check the following "
                               "file to see if it was successfully removed: {}".format(str(log_file)),
                               self.logger.WARNING)
            return True

    def remove(self, remove_framework=None):
        """
        This script checks all installed Octowire modules and remove it.
        :param remove_framework: If True, remove the octowire Framework.
        :return: Nothing
        """
        installed_modules = self._get_installed_modules()
        if not installed_modules:
            self.logger.handle("No module seems installed", Logger.WARNING)
        for module_name, _ in installed_modules.items():
            self.logger.handle(f"Removing module '{module_name}'..", Logger.INFO)
            if not self._manage_uninstall(module_name):
                self.not_removed.append(module_name)

        if len(self.not_removed) > 0:
            self.logger.handle("Unable to remove the following package(s):", Logger.ERROR)
            for module in self.not_removed:
                print(" - {}".format(module))
            self.logger.handle("Please try to uninstall it manually with the following command: "
                               "'pip3 uninstall owfmodules.<category>.<module_name>'", Logger.ERROR)
        if remove_framework:
            self._manage_uninstall("octowire-framework")
            self.logger.handle("User configuration files need to be manually removed; these are present in '~/.owf' "
                               "directory for any user which has run the framework at least once.",
                               self.logger.USER_INTERACT)
