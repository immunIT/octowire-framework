# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import ctypes
import os
import sys
from octowire_framework.core.utils.OWFUpdate import OWFUpdate
from octowire.utils.Logger import Logger


def is_venv():
    return hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix


def main():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin and not is_venv():
        Logger().handle("Please run 'owfupdate' as root or use a virtualenv. Exiting...", Logger.ERROR)
        exit(1)
    print('-----------------------------------------------------------------------')
    print('----------------Fetching and installing available modules---------------')
    print('-----------------------------------------------------------------------')
    OWFUpdate().update(update_framework=True)


if __name__ == "__main__":
    main()
