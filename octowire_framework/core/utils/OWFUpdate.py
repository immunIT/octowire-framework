# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import inspect
import os
import pathlib
import pkg_resources
import pkgutil
import platform
import re
import requests
import subprocess
import sys
import tarfile
import tempfile

from importlib import import_module

from octowire.utils.Logger import Logger
from octowire_framework.module.AModule import AModule


class OWFUpdate:
    def __init__(self):
        self.bitbucket_base_url = 'https://api.bitbucket.org/2.0'
        self.bitbucket_download_url = "https://bitbucket.org/octowire/{}/get/{}.tar.gz"
        self.logger = Logger()
        self.not_updated = []
        self.to_update = []
        self.to_install = []

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
            self.logger.handle('No modules currently installed', Logger.ERROR)
            return installed_modules
        for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
            try:
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                        installed_modules[module] = pkg_resources.get_distribution(module).version
            except ImportError:
                self.logger.handle('Error while dynamically importing package "{}"... Unable to update it'
                                   .format(module), Logger.ERROR)
                self.not_updated.append(module)
        return installed_modules

    def _get_available_modules(self):
        """
        Return a dict of modules that have a release on the octowire-framework project.
        :return: A dict of available modules {'module_name': 'version', ...}.
        """
        self.logger.handle("Obtaining the list of package releases... This may take a while...", self.logger.USER_INTERACT)
        modules = {}
        resp = requests.get('{}{}'.format(self.bitbucket_base_url, '/repositories/octowire/?q=project.key="MOD"'))
        while True:
            if resp.status_code == 200:
                for pkg in resp.json()["values"]:
                    pkg_tag_url = pkg["links"]["tags"]["href"]
                    resp_tags = requests.get(pkg_tag_url + "?sort=-name&pagelen=1")
                    if resp_tags.status_code == 200:
                        latest_release = resp_tags.json()["values"]
                        if latest_release:
                            modules[pkg["name"]] = latest_release[0]["name"]
                if "next" in resp.json():
                    resp = requests.get('{}'.format(resp.json()["next"]))
                else:
                    break
            else:
                self.logger.handle("failed to load module list - HTTP response code: {}".format(resp.status_code),
                                   self.logger.ERROR)
                break
        if not modules:
            self.logger.handle('No releases/modules found', Logger.ERROR)
        return modules

    def _get_latest_framework_version(self):
        """
        Return the latest release version of the Octowire framework.
        :return: String
        """
        module_release_url = self.bitbucket_base_url + '/repositories/octowire/octowire-framework/' \
                                                       'refs/tags?sort=-name&pagelen=1'
        resp = requests.get(module_release_url)
        if resp.status_code == 200:
            latest_release = resp.json()["values"]
            if latest_release:
                return latest_release[0]["name"]
            else:
                self.logger.handle('No release found for the Octowire framework', Logger.ERROR)
                return None
        else:
            self.logger.handle('Unable to get the latest framework release version', Logger.ERROR)
            return None

    @staticmethod
    def _get_filename_from_cd(cd):
        """
        Get filename from content-disposition.
        :param cd: Content-Disposition HTTP header.
        :return: filename from Content-Disposition or None.
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def _download_release(self, package_name, package_version):
        """
        Download the latest release of a package (module or framework).
        :param package_version: The package version.
        :param package_name: The name of the package to downloade (module or framework).
        :return: Filename or None.
        """
        self.logger.handle("Downloading {} v{}...".format(package_name, package_version))
        resp = requests.get(self.bitbucket_download_url.format(package_name, package_version), stream=True)
        if resp.status_code == 200:
            file = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
            file.write(resp.content)
            file.close()
            return file.name
        return None

    @staticmethod
    def _extract_tarball(filename):
        """
        Extract the specified tarball.
        :param filename: The tarball file path.
        :return: Directory path of the extracted archive.
        """
        tar = tarfile.open(filename)
        path = re.sub(r'\.tar.gz$', '', filename)
        setup_dir = '{}/{}'.format(path, tar.getmembers()[0].name)
        tar.extractall(path)
        tar.close()
        return setup_dir

    def _manage_install(self, package_name, package_version):
        """
        Manage the installation of the specified package (module or framework).
        :param package_name: The name of the package to install (module or framework).
        :param package_version: The package version to install (module or framework).
        :return: Bool: True if successfully installed, False otherwise.
        """
        filename = self._download_release(package_name, package_version)
        python_path = sys.executable
        if filename:
            setup_dir = self._extract_tarball(filename)
            try:
                if package_name != "octowire-framework":
                    pipes = subprocess.Popen([python_path, 'setup.py', 'install'], cwd=setup_dir,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = pipes.communicate()
                    if pipes.returncode != 0:
                        self.logger.handle("Error while installing {} package: {}".format(package_name, stderr.strip()),
                                           Logger.ERROR)
                        return False
                    else:
                        self.logger.handle("'{}' successfully installed".format(package_name), Logger.SUCCESS)
                        return True
                else:
                    # This method is necessary to update the framework. Indeed, this allows releasing the owfupdate
                    # executable in order to replace it.
                    current_dir = pathlib.Path().absolute()
                    log_file = current_dir / "framework_install.log"
                    if os.path.isfile(setup_dir + "/update_framework.py"):
                        if platform.system() == "Windows":
                            subprocess.Popen([python_path, 'update_framework.py', '-p', str(os.getpid()), '-f',
                                              str(log_file)], cwd=setup_dir, creationflags=subprocess.DETACHED_PROCESS)
                        else:
                            subprocess.Popen([python_path, 'update_framework.py', '-p', str(os.getpid()), '-f',
                                              str(log_file)], cwd=setup_dir)
                        self.logger.handle("The framework update was launched in background... check the following "
                                           "file to see if it was successfully updated: {}".format(str(log_file)),
                                           self.logger.WARNING)
                        return True
                    else:
                        self.logger.handle("The 'update_framework.py' file is missing from the installer package... "
                                           "Unable to update the octowire-framework package...", self.logger.ERROR)
                        return False
            except subprocess.CalledProcessError as err:
                self.logger.handle("The setup command failed for the '{}' module".format(package_name), Logger.ERROR)
                print(err.stderr)
                return False
        else:
            self.logger.handle("Failed to download the latest release for '{}'"
                               .format(package_name), Logger.ERROR)
            return False

    def _update_framework(self):
        """
        This function updates the Octowire framework.
        :return: Nothing
        """
        latest_release_version = self._get_latest_framework_version()
        if latest_release_version:
            latest_release_version = pkg_resources.parse_version(latest_release_version)
            try:
                current_version = pkg_resources.parse_version(
                    pkg_resources.get_distribution('octowire-framework').version)
            except pkg_resources.DistributionNotFound:
                current_version = ''
            if latest_release_version > current_version:
                self.logger.handle('A new framework release is available, running update...', Logger.INFO)
                if not self._manage_install('octowire-framework', latest_release_version.base_version):
                    self.not_updated.append('octowire-framework')
            else:
                self.logger.handle('Octowire framework is up-to-date', Logger.SUCCESS)
        else:
            self.not_updated.append('octowire-framework')

    def update(self, update_framework=None):
        """
        This script checks all released Octowire modules and compares them with currently installed modules.
        If an update is available, this script installs it. Moreover, if a module is available and not installed,
        it will be installed.
        :param update_framework: If True, check whether a framework update is available.
        :return: Nothing
        """
        available_modules = self._get_available_modules()
        installed_modules = self._get_installed_modules()
        for name, version in available_modules.items():
            installed_module_version = installed_modules.get(name, None)
            if installed_module_version is not None:
                if pkg_resources.parse_version(installed_module_version) < pkg_resources.parse_version(version):
                    self.to_update.append({"name": name, "version": version})
            else:
                self.to_install.append({"name": name, "version": version})
        if not self.to_update and not self.to_install:
            self.logger.handle("Everything is up-to-date", Logger.SUCCESS)
        for module in self.to_update:
            self.logger.handle("Updating module '{}' to version {}".format(module["name"], module["version"]),
                               Logger.INFO)
            if not self._manage_install(module["name"], module["version"]):
                self.not_updated.append(module["name"])
        for module in self.to_install:
            self.logger.handle("Installing module '{}' version {}".format(module["name"], module["version"]),
                               Logger.INFO)
            if not self._manage_install(module["name"], module["version"]):
                self.not_updated.append(module["name"])
        if len(self.not_updated) > 0:
            self.logger.handle("Unable to update/install the following package(s):", Logger.ERROR)
            for module in self.not_updated:
                print(" - {}".format(module))
        if update_framework:
            self._update_framework()
