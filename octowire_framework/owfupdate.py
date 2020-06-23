# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import argparse
import ctypes
import os
import sys
from octowire_framework.core.utils.OWFUpdate import OWFUpdate
from octowire.utils.Logger import Logger


def is_venv():
    return hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--moduleonly', help='Only update/install modules, not the framework',
                        action="store_true")
    args = parser.parse_args()
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    if not is_admin and not is_venv():
        Logger().handle("Please run 'owfupdate' as root or use a virtualenv. Exiting...", Logger.ERROR)
        exit(1)
    print('-----------------------------------------------------------------------')
    print('----------------Fetching and installing available modules--------------')
    print('-----------------------------------------------------------------------')
    if args.moduleonly:
        OWFUpdate().update(update_framework=False)
    else:
        OWFUpdate().update(update_framework=True)


if __name__ == "__main__":
    main()
