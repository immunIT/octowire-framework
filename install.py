# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import ctypes
import os
import pkg_resources
import platform
import re
import requests
import subprocess
import sys
import tarfile
import tempfile


from octowire.utils.Logger import Logger


bitbucket_base_url = 'https://api.bitbucket.org/2.0'
bitbucket_download_url = "https://bitbucket.org/octowire/{}/get/{}.tar.gz"
python_path = sys.executable


# Common Colors
class Colors:
    if "Windows" in platform.system() and "WT_SESSION" not in os.environ:
        import colorama
        from colorama import Fore, Style

        colorama.init()
        HEADER = Fore.LIGHTMAGENTA_EX
        OKBLUE = Fore.LIGHTCYAN_EX
        OKGREEN = Fore.LIGHTGREEN_EX
        WARNING = Fore.YELLOW
        FAIL = Fore.LIGHTRED_EX
        ENDC = Fore.RESET
        BOLD = Style.BRIGHT
        MAGENTA = Fore.LIGHTMAGENTA_EX
        UNDERLINE = ""
    else:
        HEADER = '\x1b[95m'
        OKBLUE = '\x1b[94m'
        OKGREEN = '\x1b[92m'
        WARNING = '\x1b[93m'
        FAIL = '\x1b[91m'
        ENDC = '\x1b[0m'
        BOLD = '\x1b[1m'
        MAGENTA = '\x1b[95m'
        UNDERLINE = '\x1b[4m'


def is_venv():
    return hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix


def get_filename_from_cd(cd):
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


def download_release(tarball_url):
    """
    Download the latest release of the Octowire framework.
    :param tarball_url: release tarball url.
    :return: Filename.
    """
    print("Downloading the latest octowire-framework release...")
    resp = requests.get(tarball_url, stream=True)
    if resp.status_code == 200:
        tmpdir = tempfile.gettempdir()
        filename = tmpdir + f"/{get_filename_from_cd(resp.headers.get('content-disposition'))}"
        with open(filename, "wb") as f:
            f.write(resp.content)
        return filename
    else:
        print(f"{Colors.FAIL}[X]{Colors.ENDC} Failed to downlaod the latest framework released. - "
              "HTTP response code: {resp.status_code}")
        exit(-1)


def extract_tarball(filename):
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


def _get_latest_framework_version():
    """
    Return the latest release version of the Octowire framework.
    :return: String
    """
    module_release_url = bitbucket_base_url + '/repositories/octowire/octowire-framework/' \
                                              'refs/tags?sort=-name&pagelen=1'
    resp = requests.get(module_release_url)
    if resp.status_code == 200:
        latest_release = resp.json()["values"]
        if latest_release:
            return latest_release[0]["name"]
        else:
            print(f'{Colors.FAIL}[X]{Colors.ENDC} No release found for the Octowire framework',
                  Logger.ERROR)
            return None
    else:
        print(f"{Colors.FAIL}[X]{Colors.ENDC} Unable to retrieve latest release URL. Check your network connection "
              f"and try again.")
        return None


def install_modules():
    """
    Run the owfupdate command to download and install released modules.
    """
    subprocess.run(['owfupdate', '-m'], stdout=sys.stdout, stderr=sys.stderr)


def manage_install():
    """
    Manage the installation of the octowire-framework.
    """
    # Check if the framework is already installed
    try:
        current_version = pkg_resources.parse_version(
            pkg_resources.get_distribution('octowire-framework').version)
    except pkg_resources.DistributionNotFound:
        current_version = ''
    # Framework already installed
    if current_version != '':
        print("{}[!] The octowire-framework is already installed. Please run 'owfupdate' to update it.{}"
              .format(Colors.WARNING, Colors.ENDC))
        exit(0)
    # Framework not installed on the system
    else:
        release_tarball_url = f"{bitbucket_download_url.format('octowire-framework', _get_latest_framework_version())}"
        tarball_filename = download_release(release_tarball_url)
        print(tarball_filename)
        if tarball_filename:
            print("[*] Extracting the tarball archive...")
            setup_dir = extract_tarball(tarball_filename)
            package_dir = setup_dir.split("/")[-1]
            setup_dir = '/'.join(setup_dir.split("/")[:-1])
            print("[*] Installing the octowire-framework package...")
            pipes = subprocess.Popen([python_path, '-m', 'pip', 'install', '--upgrade', f"./{package_dir}"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=setup_dir)
            stdout, stderr = pipes.communicate()
            if pipes.returncode != 0:
                print("{}[X]{} Error while installing the octowire-framework package: {}\n"
                      .format(Colors.FAIL, Colors.ENDC, stderr.strip()))
                exit(-1)
            else:
                print("{}[V]{} The octowire-framework was successfully installed.\n"
                      .format(Colors.OKGREEN, Colors.ENDC))


if __name__ == '__main__':
    # Check root/admin permission
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin and not is_venv():
        Logger().handle("Please run the installation script as root or use a virtualenv. Exiting...", Logger.ERROR)
        exit(-1)
    # Run the installation of the framework
    manage_install()
    # Run the update process
    install_modules()
