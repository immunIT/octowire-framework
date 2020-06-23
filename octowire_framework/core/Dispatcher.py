# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import os
from octowire_framework.core.commands.back import back
from octowire_framework.core.commands.detect import detect
from octowire_framework.core.commands.help import owf_help
from octowire_framework.core.commands.miniterm import miniterm
from octowire_framework.core.commands.run import run_module
from octowire_framework.core.commands.save_config import save_config
from octowire_framework.core.commands.search import search
from octowire_framework.core.commands.set_config import set_config
from octowire_framework.core.commands.set_globals import set_globals
from octowire_framework.core.commands.set_options import set_options
from octowire_framework.core.commands.show import show
from octowire_framework.core.commands.unset_globals import unset_globals
from octowire_framework.core.commands.unset_options import unset_options
from octowire_framework.core.commands.use import use
from octowire_framework.core.commands.quit import owf_exit


class Dispatcher:
    def __init__(self):
        self.commands = {
            "?": {"descr": "Alias for help menu", "run": owf_help, "arguments": {}},
            "help": {"descr": "Help menu", "run": owf_help, "arguments": {}},
            "show": {"descr": "modules|options|advanced|config|global: Displays modules list,\n"
                              "module (advanced) options, global configuration or global options", "run": show,
                     "arguments": {"options": None, "advanced": None, "modules": None, "config": None, "global": None}},
            "search": {"descr": "Search modules that matches the keywords.", "run": search, "arguments": {}},
            "use": {"descr": "Load a module by name", "run": use, "arguments": {}},
            "run": {"descr": "Run the selected module", "run": run_module, "arguments": {}},
            "back": {"descr": "Move back from the current context", "run": back, "arguments": {}},
            "set": {"descr": "Set a context-specific variable to a value", "run": set_options,
                    "arguments": {}},
            "unset": {"descr": "Unset a context-specific variable", "run": unset_options, "arguments": {}},
            "setg": {"descr": "Set a global variable to a value", "run": set_globals, "arguments": {}},
            "unsetg": {"descr": "Unset a global variable", "run": unset_globals, "arguments": {}},
            "setc": {"descr": "Set a config key to a value", "run": set_config, "arguments": {}},
            "save": {"descr": "Save the current config into owf.cfg file", "run": save_config, "arguments": {}},
            "detect": {"descr": "Try to automatically detect the Octowire port", "run": detect, "arguments": {}},
            "miniterm": {"descr": "Open a miniterm serial console", "run": miniterm, "arguments": {}},
            "exit": {"descr": "Exit the console", "run": owf_exit, "arguments": {}}
        }

    def handle(self, owf_instance, user_input):
        """
        User console command handler.
        :param owf_instance: Octowire framework instance
        :param user_input: User input
        """
        args = user_input.split(" ")
        command = args.pop(0)
        try:
            self.commands[command]["run"](owf_instance, *args)
        except KeyError:
            os.system(user_input)
