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
        Logger().handle(f"Unable to find package '{package_name}'", Logger.ERROR)
        return None


def version(owf_instance, *args):
    """
    Displays the Framework, Library and Firmware versions
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    versions = []
    # Identify the current Octowire Framework and Library versions
    for pkg in ["octowire-framework", "octowire-lib"]:
        pkg_version = _get_package_version(pkg)
        if pkg_version:
            versions.append({"Name": pkg, "Version": pkg_version})
    # Identify the current Octowire firmware version
    Logger().handle("Attempting to detect the Octowire to identify the firmware version...", Logger.HEADER)
    s_octowire = detect_and_connect()
    if s_octowire is not None:
        Logger().handle("Identifying the current firmware version...")
        # Instantiate the Octowire
        octowire_instance = Octowire(serial_instance=s_octowire)
        # Get the current firmware version
        fw_version = octowire_instance.get_octowire_version().split()[1]
        versions.append({"Name": "Octowire firmware", "Version": fw_version})
    else:
        versions.append({"Name": "Octowire firmware", "Version": "Octowire not detected"})
    owf_instance.logger.print_tabulate(versions, headers={"Name": "Name", "Version": "Version"})
