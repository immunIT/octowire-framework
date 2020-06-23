# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>

script = """
# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) Jordan Ovrè / Paul Duncan
# License: GPLv3
# Paul Duncan / Eresse <eresse@dooba.io>
# Jordan Ovrè / Ghecko <ghecko78@gmail.com

import argparse
import psutil
import subprocess
import sys
import time
import traceback

from octowire.utils.Colors import Colors


def framework_uninstall(pid, logfile):
    \"\"\"
    Uninstall the framework.
    Loop until the calling process is completed or timeout is reached.
    Once callling process is terminated, start the removal of the Octowire framework.
    :param pid:
    :param logfile:
    :return:
    \"\"\"
    python_path = sys.executable
    with open(logfile, "w") as f:
        f.write("Start waiting for the completion of the calling process (owfremove).\\n")
        timeout = time.time() + 60
        while time.time() < timeout:
            if not psutil.pid_exists(pid):
                pipes = subprocess.Popen([python_path, '-m', 'pip', 'uninstall', '-y', 'octowire-framework'],
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = pipes.communicate()
                if pipes.returncode != 0:
                    f.write("ERROR: Error while removing the octowire-framework. Please try to uninstall it manually "
                            "'(sudo) pip3 uninstall octowire-framework' or run again the 'owfremove' script.")
                    f.write("ERROR details: {}".format(stderr.strip()))
                else:
                    f.write("SUCCESS: The 'octowire-framework' package was successfully removed.")
                break
        else:
            f.write("ERROR: Timeout reached while waiting for the completion of the calling process (owfremove)."
                    " Please run the 'owfremove' command again to try to remove the octowire-framework package, or "
                    "try to uninstall it manually '(sudo) pip3 uninstall octowire-framework'\\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{}This script is not intended to be run manually. It is "
                                                 "called by the 'owfremove' command. Run it at your own risk.{}"
                                     .format(Colors.BOLD, Colors.ENDC))
    parser.add_argument("-p", "--pid", help="The pid of the parent process.", type=int, required=True)
    parser.add_argument("-f", "--logfile", help="The path of the file to log the removal process status", required=True)
    args = parser.parse_args()
    framework_uninstall(args.pid, args.logfile)

"""
