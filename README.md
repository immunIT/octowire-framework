[![Python 3.7+](https://img.shields.io/badge/python-v3.7+-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# octowire-framework [v1.0.0]

## Description

This project is a framework around the [Octowire hardware]().  
It provides multiple modules allowing you to work efficiently and save time on any hardware project.  
This framework is fully compatible with Linux and Windows (Not tested on MacOS).  
To obtain a more beautiful rendering on Windows, use the new [Windows Terminal](https://www.microsoft.com/fr-ch/p/windows-terminal/9n0dx20hk701).

[![asciicast](https://asciinema.org/a/342058.svg)](https://asciinema.org/a/342058)

## Requirements

Installing the framework will require the following: 
 - python (at least 3.7)
 - pip (for python3)
 - python3-requests (`pip install requests`)
 - python3-setuptools (`pip install setuptools`)

## Installation

### One-liner

```
# Windows powershell (as Administrator)
curl.exe -s https://raw.githubusercontent.com/immunIT/octowire-framework/master/install.py | python

# Linux (as root)
curl https://raw.githubusercontent.com/immunIT/octowire-framework/master/install.py | python
```


### Manual method

Clone this repository or get the latest release, then run:

```
python3 setup.py install
```

## Usage

This framework is designed to be simple to use.  
Just run `owfconsole`, list available modules using the `show modules` command and load the one you need with `use <module_categroy>/<module_name>`.  
Then, list available options for the current module: `show options`, setup the needed ones with `set <option_name> <value>` and finally run it with `run`!

## Updating the framework and updating/installing latest modules.

```
(sudo) owfupdate
```

## Using the Docker image

### Build the image

```
docker build -t owf .
```

### Run the instance

```
docker run --rm -it -v /local/folder/:/remote/folder --device=/dev/ttyACM0:/dev/ttyACM0 owf
```

## Configuration explanation

Framework configuration is stored in the `/home/<user>/.owf/owf.cfg` file.  
This configuration can be changed through the framework using commands.

```bash
[OCTOWIRE]
port = /dev/ttyACM0 # Octowire device
baudrate = 7372800 # baudrate value to communicate with the Octowire device
read_timeout = 1 # The serial read timeout value (in seconds) 

[MINITERM]
parity = N # set parity. one of {N, E, O, S, M}
xonxoff = False # enable software flow control
echo = False # enable local echo
filters = default # Text transformation, see Miniterm man
raw = False # Do no apply any encodings/transformations if True
quiet = False # suppress non-error messages
exit_char = 29 # Unicode of special character that is used to exit the application, default ctrl+] (29)
menu_char = 20 # Unicode of special character that is used to control miniterm (menu), default ctrl+t (20)
serial_port_encoding = UTF-8 # set the encoding for the serial port (Latin1, UTF-8, ...)
eol = CR # end of line mode (CR, LF, CRLF)

[THEME] # You can use HTML color codes. For all possible theme values, see prompt_toolkit manual https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html#style-strings
base = #3399ff # Base prompt color ([owf])
pound = #3399ff # Pound prompt color (>)
module = #ff0000 bold # Selected module name color
category = #ffffff # Selected module category color
```

## Contributing

Follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## FAQ

### How to list available modules?

```[owf] > show modules```

### What's a global option?

A global option is an option that will be used for every module loaded.
Setting the option with the `setg` command will set the specified option globally for every module loaded.
Unset a specific global option with the `unsetg` command.
It is also possible to print all previously defined global options using the `show global` command.

### Can you give me a typical example of use?

You identify an SPI flash chip on a hardware device. You want to dump its memory.
Simply run `owfconsole` from a shell and follow these instructions:

1. List available module:

```[owf] > show modules```

2. Select the appropriate module:

```[owf] > use spi/flash_dump```

3. Show available options:

```[owf] spi(flash_dump) > show options```

4. Set necessary options:

```[owf] spi(flash_dump) > set dump_file dump.bin```

5. Run the module:

```[owf] spi(flash_dump) > run```

### How to properly remove the framework along with any installed modules?

### Using owfremove

Run `owfremove` in your terminal to uninstall the framework along with its modules.
User configuration files need to be manually removed; these are present in '~/.owf' directory for any user which has run the framework at least once.

#### Manual method

Run `owfconsole` and execute the `show modules` command to list installed modules.
The module names returned by the framework are in the following format: `category/module_name`.

For each module, run `pip3 uninstall owfmodules.<category>.<module_name>`.

Then, run `pip3 uninstall octowire_framework`.

Finally, delete the `.owf` directory in your home folder.
