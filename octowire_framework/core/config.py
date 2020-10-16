# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import configparser
import platform
import sys
from pathlib import Path

from octowire.utils.serial_utils import detect_octowire


def create_default_config(config, owf_dir, owf_config_path):
    """
    Create the default config file if it does not exist.
    :param config: configparser instance.
    :param owf_dir: pathlib object of the home directory for the current user.
    :param owf_config_path: pathlib object of the configuration path located in the current user's home.
    :return: Nothing
    """
    if not owf_dir.is_dir():
        owf_dir.mkdir()
    port = detect_octowire(verbose=False)
    if port:
        config['OCTOWIRE'] = {
            'port': port,
            'baudrate': '7372800',
            'read_timeout': 1
        }
    else:
        config['OCTOWIRE'] = {
            'port': 'COMX' if "Windows" in platform.system() else "/dev/ttyXXXX",
            'baudrate': '7372800',
            'read_timeout': 1
        }
    config['MINITERM'] = {
        'parity': 'N',
        'xonxoff': True,
        'echo': False,
        'filters': 'default',
        'raw': False,
        'quiet': False,
        'exit_char': 0x1b if "Windows" in platform.system() else 0x1d,
        'menu_char': 0x14,
        'menu_char_help': 0x48 if "Windows" in platform.system() else 0x08,
        'serial_port_encoding': sys.getdefaultencoding(),
        'eol': 'CR'
    }
    config['THEME'] = {
        'user_input': '',
        'base': '#3399ff',
        'pound': '#3399ff',
        'module': '#ff0000 bold',
        'category': '#ffffff',
    }
    with owf_config_path.open('w') as cfg_file:
        config.write(cfg_file)


def load_config():
    """
    Load the existing configuration file and return it.
    :return: configparser file content.
    """
    config = configparser.ConfigParser(allow_no_value=True)
    owf_dir = Path.home() / '.owf'
    owf_config_path = owf_dir / 'owf.cfg'
    if not owf_dir.is_dir() or not owf_config_path.is_file():
        create_default_config(config, owf_dir, owf_config_path)
    config.read(str(owf_config_path))
    # New from 1.2.0
    try:
        config['OCTOWIRE']['detect']
    except KeyError:
        # The detect key config does not exist, create it
        config['OCTOWIRE']['detect'] = "1"
        with owf_config_path.open('w') as cfg_file:
            config.write(cfg_file)
    return config
