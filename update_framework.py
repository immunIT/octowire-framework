# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com

import argparse
import time
import psutil
import subprocess
from octowire.utils.Colors import Colors
from octowire.utils.Logger import Logger


def main(pid, logfile):
    """
    The main function. Loop until the calling process is completed or timeout is reached.
    :param pid: The pid of the parent process.
    :param logfile: The file path where installation logs will be written.
    :return: Nothing
    """
    with open(logfile, "w") as f:
        f.write("Start waiting for the completion of the calling process (owfupdate).\n")
        timeout = time.time() + 60
        while time.time() < timeout:
            if not psutil.pid_exists(pid):
                pipes = subprocess.Popen(['python', 'setup.py', 'install'], stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
                stdout, stderr = pipes.communicate()
                if pipes.returncode != 0:
                    f.write("{}[X]{}Error while updating the octowire-framework package: {}\n"
                            .format(Colors.FAIL, Colors.ENDC, stderr.strip()))
                else:
                    f.write("{}[V]{}The octowire-framework was successfully updated.\n".format(Colors.OKGREEN,
                                                                                               Colors.ENDC))
                break
        else:
            f.write("{}[X]{}Timeout reached while waiting for the completion of the calling process (owfupdate)."
                    " Please run the 'owfupdate' command again to try to update the octowire-framework package.\n"
                    .format(Colors.FAIL, Colors.ENDC))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="{}This script is not intended to be run manually. It is "
                                                 "called by the 'owfupdate' command. Run it at your own risk.{}".format(
                                                  Colors.BOLD, Colors.ENDC))
    parser.add_argument("-p", "--pid", help="The pid of the parent process.", type=int, required=True)
    parser.add_argument("-f", "--logfile", help="The path of the file to log the update process status", required=True)
    args = parser.parse_args()
    main(args.pid, args.logfile)
