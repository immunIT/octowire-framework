# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import configparser
import platform
import serial
import sys

from octowire.utils.Logger import Logger
from octowire_framework.core.utils.hex_keycodes import hex_keycodes
from serial.tools.miniterm import Miniterm


def key_description(character):
    """
    Return the readable description for a key.
    :param character: An ASCII character.
    :return: Readable description for key.
    """
    if "Windows" in platform.system():
        for key, value in hex_keycodes.items():
            if value == character:
                return key
        else:
            return ""
    else:
        ascii_code = ord(character)
        if ascii_code < 32:
            return 'Ctrl+{:c}'.format(ord('@') + ascii_code)
        else:
            return repr(character)


def miniterm(owf_instance=None, *args):
    """
    Run a serial console session (using miniterm from serial package).
    :param args: Varargs command options.
    :param owf_instance: Octowire framework instance (self).
    :return: Nothing.
    """
    if len(args) < 1:
        config = None
    else:
        config = args[0] if isinstance(args[0], configparser.ConfigParser) else None
    logger = Logger()
    filters = []
    if owf_instance is None and config is None:
        logger.handle("You need to set owf_instance or config", logger.ERROR)
        return False
    if owf_instance is not None:
        config = owf_instance.config
    octowire_cfg = config['OCTOWIRE']
    miniterm_cfg = config['MINITERM']
    filters.append(miniterm_cfg['filters'])

    try:
        serial_instance = serial.serial_for_url(
            octowire_cfg['port'],
            octowire_cfg['baudrate'],
            parity=miniterm_cfg['parity'],
            rtscts=0,
            xonxoff=config.getboolean('MINITERM', 'xonxoff'),
            do_not_open=True)

        if not hasattr(serial_instance, 'cancel_read'):
            # enable timeout for alive flag polling if cancel_read is not available
            serial_instance.timeout = 1

        if isinstance(serial_instance, serial.Serial):
            serial_instance.exclusive = True

        serial_instance.open()
    except serial.SerialException as e:
        logger.handle("could not open port {!r}: {}".format(octowire_cfg['port'], e), logger.ERROR)
        return False

    mt = Miniterm(
        serial_instance,
        echo=config.getboolean('MINITERM', 'echo'),
        eol=miniterm_cfg['eol'].lower(),
        filters=filters)
    mt.exit_character = chr(int(miniterm_cfg['exit_char']))
    mt.menu_character = chr(int(miniterm_cfg['menu_char']))
    mt.raw = miniterm_cfg['raw']
    mt.set_rx_encoding(miniterm_cfg['serial_port_encoding'])
    mt.set_tx_encoding(miniterm_cfg['serial_port_encoding'])

    if not config.getboolean('MINITERM', 'quiet'):
        sys.stderr.write('--- Miniterm on {p.name} {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} ---\n'.format(
            p=mt.serial))

    toolbar = '--- Quit: <{}> | Menu: <{}> | Help: <{}> followed by <{}> ---\n'.format(
        key_description(int(miniterm_cfg['exit_char'])),
        key_description(int(miniterm_cfg['menu_char'])),
        key_description(int(miniterm_cfg['menu_char'])),
        key_description(0x48))
    print(toolbar)

    mt.start()
    try:
        mt.join(True)
    except KeyboardInterrupt:
        pass
    if not config.getboolean('MINITERM', 'quiet'):
        sys.stderr.write('\n--- exit ---\n')
    mt.join()
    mt.close()
