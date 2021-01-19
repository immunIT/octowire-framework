# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import binascii
import math
import pkg_resources
import re
import requests
import serial
import tarfile
import tempfile
from octowire.utils.Logger import Logger
from octowire.octowire import Octowire
from octowire.utils.Colors import Colors
from octowire.utils.serial_utils import detect_and_connect
from prompt_toolkit import prompt
from serial.tools import list_ports


# Flash Page Size
_PAGE_SIZE = 512


def erase_flash(octowire_ser, fw):
    """
    Erase flash (for given firmware size)
    :param octowire_ser: Octowire serial instance
    :param fw: Buffer containing the firmware image
    :return: Bool
    """

    print(f"{Colors.OKBLUE}Erasing flash before writing to it...{Colors.ENDC}")
    octowire_ser.write(bytes("x%i\n" % len(fw), "ascii"))
    res = octowire_ser.readline().strip().decode()
    if res.startswith("ERROR"):
        Logger().handle("An Error occurred during the erase process. Exiting...", Logger.ERROR)
        return False
    return True


def write_flash(octowire_ser, fw):
    """
    Write a chunk of Flash
    :param octowire_ser: Octowire serial instance
    :param fw: Buffer containing the firmware image
    :return: Bool
    """
    print(f"{Colors.OKBLUE}Writing to flash...{Colors.ENDC}")
    w_data = fw
    addr = 0
    while len(w_data):
        chunk = w_data[:_PAGE_SIZE]
        w_data = w_data[_PAGE_SIZE:]
        octowire_ser.write(bytes("w%s,%s\n" % (hex(addr)[2:], chunk.hex()), "ascii"))
        res = octowire_ser.readline().strip().decode()
        if res.startswith("ERROR"):
            Logger().handle("An Error occurred during the erase process. Exiting...", Logger.ERROR)
            return False
        addr += len(chunk)
    return True


def verify_flash(octowire_ser, fw):
    """
    Verify Flash contents (against a given firmware image)
    :param octowire_ser: Octowire serial instance
    :param fw: Buffer containing the firmware image
    :return: Nothing
    """
    print(f"{Colors.OKBLUE}Verifying flash...{Colors.ENDC}")
    pages = math.ceil(len(fw) / _PAGE_SIZE)
    check_fw = bytearray()
    for i in range(0, pages):
        octowire_ser.write(bytes("r%s,%i\n" % (hex(i * _PAGE_SIZE)[2:], _PAGE_SIZE), "ascii"))
        res = octowire_ser.readline().strip().decode()
        if res.startswith("ERROR"):
            exit(1)
        check_fw += binascii.unhexlify(res)
    if check_fw[:len(fw)] != fw:
        print(f"{Colors.FAIL}Flash verification failed! Exiting...{Colors.ENDC}")
    else:
        print(f"{Colors.OKGREEN}Flash verification OK!{Colors.ENDC}")


def _is_octowire_in_bootloader():
    """
    Iterate over serial devices to find the Octowire, returning the serial port.
    :return: Octowire port if found in normal mode, False otherwise.
    """
    ports_list = list_ports.comports(include_links=True)
    for port in ports_list:
        if port.vid == 0xc0de and port.pid == 0xb007:
            Logger().handle("Octowire found in bootloader mode.", Logger.SUCCESS)
            return port.device
        elif port.vid == 0xc0de and port.pid == 0x0c70:
            Logger().handle("The Octowire can only be flashed when in 'bootloader' mode.", Logger.ERROR)
            Logger().handle("To enter bootloader mode follow the method described below:\n"
                            "   1. With the board already powered on, press and maintain the 'User' button\n"
                            "   2. Press the 'Reset' button while keeping the User button pressed, "
                            "until the activity LED (blue) lights up\n"
                            "   3. Press enter to retry", Logger.USER_INTERACT)
            return None
    Logger().handle("Octowire not found. Please ensure the Octowire is properly plugged into your computer and run the "
                    "command again.", Logger.ERROR)
    return None


def _get_latest_firmware_version():
    """
    Return the latest released version of the Octowire framework.
    :return: String
    """
    firmware_release_url = 'https://api.bitbucket.org/2.0/repositories/octowire/octowire-firmware-releases/' \
                           'refs/tags?sort=-name&pagelen=1'
    resp = requests.get(firmware_release_url)
    if resp.status_code == 200:
        latest_release = resp.json()["values"]
        if latest_release:
            return latest_release[0]["name"]
        else:
            Logger().handle('No release found for the Octowire firmware', Logger.ERROR)
            return None
    elif resp.status_code == 429:
        Logger().handle("API rate limiting reached, please try updating again later.", Logger.ERROR)
        return None
    else:
        Logger().handle('Unable to get the latest firmware released version', Logger.ERROR)
        return None


def _print_bootloader_instruction():
    Logger().handle("The Octowire can only be flashed when in 'bootloader' mode. To enter bootloader mode "
                    "follow the method described below:\n"
                    "   1. With the board already powered on, press and maintain the 'User' button\n"
                    "   2. Press the 'Reset' button while keeping the User button pressed, "
                    "until the activity LED (blue) lights up\n"
                    "   3. Press enter to continue", Logger.USER_INTERACT)


def _download_release(firmware_version):
    """
    Download the latest release of a package (module or framework).
    :param firmware_version: The latest firmware version number.
    :return: Filename or None.
    """
    Logger().handle(f"Downloading 'octowire-firmware' v{firmware_version}...", Logger.INFO)
    resp = requests.get(f"https://bitbucket.org/octowire/octowire-firmware-releases/get/{firmware_version}.tar.gz",
                        stream=True)
    if resp.status_code == 200:
        file = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
        file.write(resp.content)
        file.close()
        return file.name
    else:
        Logger().handle("failed to download the latest firmware release - HTTP response code: {}"
                        .format(resp.status_code), Logger.ERROR)
    return None


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


def _manage_install(octowire_ser, firmware_version):
    filename = _download_release(firmware_version)
    if filename:
        firmware_path = f"{_extract_tarball(filename)}/firmware/octowire-firmware.bin"
        try:
            fw = open(firmware_path, "rb").read()
        except FileNotFoundError:
            print(f"{Colors.FAIL}The file {firmware_path} does not exist. Exiting...{Colors.ENDC}")
            return False
        # Flash process (erase, write and verify firmware image)
        if erase_flash(octowire_ser, fw):
            if write_flash(octowire_ser, fw):
                verify_flash(octowire_ser, fw)
    else:
        return False


def _update_process(firmware_version):
    _print_bootloader_instruction()
    while True:
        try:
            input("Press enter to continue or 'Ctrl-C' to abort:")
            port = _is_octowire_in_bootloader()
            if port:
                # Attempt to open Serial port
                octowire_ser = None
                try:
                    octowire_ser = serial.Serial(port, 115200, timeout=1)
                except serial.SerialException as e:
                    print(f"{Colors.FAIL}Error opening serial port {port}: {e}{Colors.ENDC}")
                    break
                _manage_install(octowire_ser, firmware_version)
                break
            else:
                continue
        except KeyboardInterrupt:
            Logger().handle("\nAborted.", Logger.ERROR)
            break


def fwupdate(owf_instance, *args):
    """
    Download and install the latest Octowire firmware.
    This command automatically detect the octowire.
    :param owf_instance: Octowire framework instance (self).
    :param args: Varargs command options.
    :return: Nothing
    """
    Logger().handle("Attempting to find the Octowire...", Logger.HEADER)
    s_octowire = detect_and_connect()
    if s_octowire is not None:
        Logger().handle("Recovering the actual firmware version...")
        # Instantiate the Octowire instance
        octowire_instance = Octowire(serial_instance=s_octowire)
        # Recovering the actual firmware version
        current_version = pkg_resources.parse_version(octowire_instance.get_octowire_version().split()[1])
        if current_version:
            latest_version = _get_latest_firmware_version()
            if latest_version:
                latest_version = pkg_resources.parse_version(latest_version)
                if latest_version > current_version:
                    Logger().handle(f"A new firmware version is available ({current_version} -> {latest_version})",
                                    Logger.RESULT)
                    res = prompt("Do you want to continue? [Y/n]:")
                    if res.upper() == "Y" or res == "":
                        _update_process(latest_version)
                else:
                    Logger().handle(f"The latest firmware revision is already installed.", Logger.WARNING)
                    res = prompt("Do you want to continue the installation anyway? [y/N]:")
                    if res.upper() == "Y":
                        _update_process(latest_version)
            else:
                Logger().handle("Unable to get the latest firmware version.")
        else:
            Logger().handle("Unable to get the current Octowire version, please press the reset button and retry...",
                            Logger.ERROR)

