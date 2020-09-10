# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


from prompt_toolkit.completion import NestedCompleter, Completion, CompleteEvent, PathCompleter, Completer
from prompt_toolkit.document import Document
from typing import Iterable, Dict, Optional


class CustomCompleter(NestedCompleter):
    """
    Custom completer to allow completion of file/path for set and setg command.
    Otherwise, NestedCompleter.get_completions() is called.
    """
    def __init__(self, options: Dict[str, Optional[Completer]]):
        super().__init__(options)
        self.path_completer = PathCompleter(expanduser=True)
        self.owf_instance = None

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        # Code for path/file completion
        # Get the length of the command before the cursor
        text = document.text_before_cursor.lstrip()
        try:
            # File completer is always in the third position (set option PATH_COMPLETION_HERE)
            if " " in text and ((len(text.split()) == 2 and document.text_before_cursor[-1] == " ")
                                or (len(text.split()) > 2)):
                # Extract the first term of the command line
                owf_ucmd = text.split()[0]

                # Add a path completer only on set and setg command
                if owf_ucmd in ["set", "setg"]:
                    # Extract the option name supplied by the user to check if it need file autocompletion
                    supplied_opt_name = text.split()[1]

                    # Check if the option required a file
                    for opt_name, opt in self.owf_instance.current_module.options.items():
                        if opt_name == supplied_opt_name and opt["Type"] in ["file_r", "file_w"]:
                            cmd_len = sum(len(x) for x in text.split()[0:2]) + text.count(" ")
                            # Extract only the file parts here (Cut owf cmd and option name)
                            # and ignore text after the cursor
                            sub_doc = Document(document.text[cmd_len:document.cursor_position])
                            yield from (Completion(completion.text, completion.start_position, display=completion.display)
                                        for completion in self.path_completer.get_completions(sub_doc, complete_event))
        # current_module or current_module.options is None
        except AttributeError:
            pass

        # Standard nested completion (No file/path completion needed here)
        for c in super().get_completions(document, complete_event):
            yield c
