# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import pkg_resources
from octowire.octowire import Octowire
from octowire.utils.Logger import Logger
from octowire.utils.serial_utils import detect_and_connect


def _get_package_version(package_name):
    """
    Return the version of a given Python package.
    :param package_name: Package name.
    Return: Version string or None
    """
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        Logger().handle(f"Unable to find the package '{package_name}'", Logger.ERROR)
        return None
    #try:
    #    package = import_module(package_name)
    #except ImportError:
    #    Logger().handle(f"Unable to find the package '{package_name}'", Logger.ERROR)
    #else:
    #    for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
    #        try:
    #            if not is_pkg:
    #                imported_module = import_module(module)
    #                for d_module in get_amodule_class(imported_module, module, AModule):
    #                    modules.append(d_module)
    #        except ImportError as err:
    #            self.logger.handle('Unable to import package "{}":  {}...'.format(module, err), Logger.ERROR)
    #self.logger.handle("{} modules loaded, run 'owfupdate' command to install the latest modules"
    #                   .format(len(modules)), Logger.USER_INTERACT)


def version(owf_instance, *args):
    """
    Displays the Framework, Library and Firmware versions
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    versions = []
    # Recovering the actual Octowire Framework and Octowire Library version
    for pkg in ["octowire-framework", "octowire-lib"]:
        pkg_version = _get_package_version(pkg)
        if pkg_version:
            versions.append({"Name": pkg, "Version": pkg_version})
    # Recovering the Octowire firmware version
    Logger().handle("Attempting to find the Octowire to recover the firmware version...", Logger.HEADER)
    s_octowire = detect_and_connect()
    if s_octowire is not None:
        Logger().handle("Recovering the actual firmware version...")
        # Instantiate the Octowire instance
        octowire_instance = Octowire(serial_instance=s_octowire)
        # Recovering the actual firmware version
        fw_version = octowire_instance.get_octowire_version().split()[1]
        versions.append({"Name": "Octowire firmware", "Version": fw_version})
    else:
        versions.append({"Name": "Octowire firmware", "Version": "Octowire not found / not in 'normal' mode"})
    owf_instance.logger.print_tabulate(versions, headers={"Name": "Name", "Version": "Version"})
