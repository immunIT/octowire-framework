[![Python 3.8](https://img.shields.io/badge/python-v3.7%7Cv3.8-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-important.svg)](LICENSE)

# octowire-framework [v1.0.0]

## Description

This project is a framework around the [Octowire project]().
It provides multiple modules allowing you to work efficiently and save time on any hardware project.
This framework is fully compatible with Linux and Windows (Not tested on MAC OS).

[![asciicast]()]()

## Installation

Clone this repository or get the latest release, then:

```
python3 setup.py install
```

## Usage

This framework work like metasploit. Simply run owfconsole, load any available modules and enjoy!

## Use Docker image

### Build the image

```
docker build -t owf .
```

### Run the instance

```
docker run --rm -it -v /local/folder/:/remote/folder --device=/dev/ttyACM0:/dev/ttyACM0 owf
```

## Configuration explanation

```bash

[OCTOWIRE]
port = /dev/ttyACM0 # Octowire device
baudrate = 7372800 # baudrate value to communicate with the octowire device
read_timeout = 1 # The read timeout value

[MINITERM]
parity = N # set parity (octowire communication, not device). one of {N, E, O, S, M}
xonxoff = False # enable software flow control
echo = False # enable local echo
filters = default # Text transformation, see Miniterm man
raw = False # Do no apply any encodings/transformations if True
quiet = False # suppress non-error messages
exit_char = 29 # Unicode of special character that is used to exit the application, default ctrl+] (29)
menu_char = 20 # Unicode code of special character that is used to control miniterm (menu), default ctrl+t (20)**
serial_port_encoding = UTF-8 # set the encoding for the serial port (Latin1, UTF-8, ...)
eol = CR # end of line mode (CR, LF, CRLF)

[THEME] # You can use HTML color code. For all possible theme value, see promp_toolkit manual https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html#style-strings
base = #3399ff # Base prompt color [owf]
pound = #3399ff # Pound prompt color >
module = #ff0000 bold # Selected module name color (baudrate)
category = #ffffff # Selected module category color uart()

```

## Contributing

Follow the guideline on the [CONTRIBUTING.md](CONTRIBUTING.md) files

## FAQ

### How to list available modules ?

``` [owf] > show modules ```

### What's a global options ?

A global option is an option who will be used for every module loaded.
Setting the options with the `setg` command will set the specified options globally for every module loaded.
Unset a specific global option with `unsetg` command.
It is also possible to print the previously defined global using `show global` command.

### Can you give me a typical example of use?

You identify an SPI flash chip on a hardware device. You want to dump his memory.
Simply run `owfconsole` from a shell and follow these instructions:

1. List available module:

```[owf] > show modules```

2. Select the correct module:

```[owf] > use spi/flash_dump```

3. Show available options

```[owf] spi(flash_dump) > show options```

4. Set necessary options

```[owf] spi(dump_flash) > set dump_file dump.bin```

5. Run the module

```[owf] spi(flash_dump) > run```

### How to properly remove the framework along with installed modules?

#### Manually method

run owfconsole and execute the `show modules` command to list installed modules.
The module name returned by the framework is something like that (protocol/module_name).

For each module, run `pip3 uninstall owfmodules.<protocol>.<module_name>`.

Then, run `pip3 uninstall octowire_framework`.

Finally, delete the `.owf` directory in your home folder.

### owfremove

**Coming soon**