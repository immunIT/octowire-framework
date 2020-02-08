# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com


import argparse
import shutil

from octowire_framework.core.Framework import Framework
from octowire.utils.Logger import Logger


def welcome(terminal_width):
    """
    Print the framework header.
    :return: Nothing
    """
    logo = """\x1b[38;5;92m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣿⣿⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣴⠾⢶⡄⠀⠀⠀⣿⡍⠻⢿⣿⣿⣿⣿⡿⠟⢋⣿⠀⠀⠀⢠⡶⠷⣦⠀⠀
⣰⡞⠻⠶⠾⠃⠀⠀⠀⠙⢿⣤⣤⣾⣿⣿⣷⣤⣤⡾⠋⠀⠀⠀⠘⠷⠶⠟⢳⣆
⢿⣷⣄⢀⣀⣠⣤⣶⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢶⣶⣤⣄⣀⡀⣠⣾⡿
⠈⠛⠿⠿⠿⠿⠿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠿⠿⠿⠿⠿⠟⠁
⣰⡿⢷⡄⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⢠⡾⢿⣦
⢙⡷⠾⠃⠀⣰⡿⣾⣿⣷⣿⣿⡟⢡⣴⣦⡌⢻⣿⣿⡿⣿⣷⢻⣆⠀⠘⠷⢾⡋
⢸⣿⣀⣀⣴⣿⢷⣿⣿⣸⣿⣿⡇⠸⣧⣼⠏⢸⣿⣿⡇⣿⣿⡟⣿⣦⣀⣀⣾⡇
⠀⠙⠛⠿⠟⠛⢸⣿⣿⡇⣿⣿⣇⠀⠀⠀⠀⣸⣿⣿⢹⣿⣿⡇⠙⠻⠿⠟⠋⠀
⠀⠀⢀⣀⡀⠀⠈⣿⣿⣿⠘⣿⣿⣆⠀⠀⣰⣿⣿⠃⣿⣿⣿⡇⠀⢀⣀⡀⠀⠀
⠀⠀⣿⣉⣿⠀⢸⣿⣿⡇⠀⠘⣿⣿⡆⢰⣿⣿⠃⠀⢸⣿⣿⡇⠀⣿⣉⣿⠆⠀
⠀⢰⣏⠛⠉⠀⣼⣿⡿⠀⠀⠀⠘⣿⡇⢸⣿⠇⠀⠀⠀⢻⣿⣧⠀⠈⠛⣹⡆⠀
⠀⠀⠻⢿⣶⣿⡿⠋⠀⠀⠀⠀⣤⣿⠃⠘⢿⣠⡀⠀⠀⠀⠙⢿⣿⣶⡿⠟⠁⠀
⠀⠀⠀⠀⠀⠀⢀⣴⢶⣤⣴⡿⠛⠁⠀⠀⠈⠛⢿⣦⣤⡶⣶⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⢷⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣧⡾⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣴⡶⣶⡄⠀⢠⣴⡶⡶⠀⣿⣷⣶⠀⢠⣴⢶⣦⡄⢰⣶⠀⢰⣦⠀⣴⡖⢰⣶⠀⢠⣶⠶⡆⢀⣴⠶⣶⡄
⣿⡇⠀⢸⣿⠀⣿⡇⠀⠀⠀⣿⡇⠀⠀⣿⡇⠀⢸⣿⠀⢿⡇⣿⢿⣤⣿⠁⢸⣿⠀⢸⣿⠀⠀⣾⡿⠶⠾⠿
⠙⢿⣶⡾⠏⠀⠹⢷⣶⣶⠀⠻⣷⣶⡄⠹⢷⣶⡾⠏⠀⠘⣿⠇⠘⣿⠇⠀⢸⣿⠀⢸⣿⠀⠀⠘⢿⣶⣶⡆
        \x1b[0m"""
    print('\n'.join(line.center(terminal_width) for line in logo.splitlines()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--file', help='A file containing framework commands (one per line)')
    args = parser.parse_args()
    t_width, _ = shutil.get_terminal_size()
    welcome(terminal_width=t_width)
    if t_width < 95:
        Logger().handle("Please consider using a terminal width >= 95 for a better experience.", Logger.WARNING)
    instance = Framework()
    instance.run(args.file)


if __name__ == "__main__":
    main()
