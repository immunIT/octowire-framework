# Contribution guidelines

## Before starting

Thanks for your interest in the Octowire framework project!
There are multiple ways to help beyond just writing code:

* Submit bug and feature requests with detailed information about your issue or idea.
* Help fellow users with open issues.
* Submit an update, a brand new module or a module improvement.

# Contributing to the Octowire framework

Here's a short list of do's and don'ts to make sure your valuable contributions actually make it into Octowire framework's master branch.
If you do not care to follow these rules, your contribution will be closed.

## Code contributions

* Follow the [PEP 8 style guide for python code](https://www.python.org/dev/peps/pep-0008/)
* Do one commit for each modification/addition/improvement
* Use explicit commit messages
* License your code as GPLv3 clause
* Always start a new module using the [owfmodules.skeleton](XXXXXX) base repository

## Creating a new module

Create an issue on [offmodules.skeleton](XXXXXXXXXX) with these details:

* Module name (owfmodules.CATEGORY.NAME)
* A short description
* Module category (uart, jtag, spi, misc, ...)

If we accept the module, we will create a repository initiated with the [owfmodules.skeleton](xxxxxx) repository.

### Useful information

**Use the `octowire-lib` library as much as possible for protocol interaction.**

#### Initial steps

1. Fill the README.md file
2. Rename the `category` directory (uart, spi, i2c, ...)
3. Rename the `module_name.py` file
4. Rename the class
5. Modify the setup.py file

#### Start coding (<module_name>.py)

1. Update meta variable (into \_\_init\_\_ method)

```
self.meta.update({
    'name': 'Module short description',
    'version': '1.0.0',
    'description': 'Module long description',
    'author': 'Name and/or email'
})
```

2. Define necessary options (A list of dict)

```
self.options = [
    {"Name": "Option1", "Value": "", "Required": True, "Type": "string/int/bool",
     "Description": "Option1 description", "Default": "default value if available"},
    {"Name": "Option2", "Value": "", "Required": False, "Type": "string/int/bool",
     "Description": "Option2 description", "Default": self.config["OCTOWIRE"]["read_timeout"]},
]
```

3. Implement the `run` method

## Pull Requests

* Write "WIP" on your PR if submitting working yet unfinished code.
* Include only one module per pull request.
* Always start your work on the master branch to ensure you are using the latest and most stable codebase.
* As much as possible, make use of functions from the library (`octowire-lib`) and framework (`octowire-framework`).
* Include verification steps on your PR message (target, environment, ...).
* Include a short summary of what your code/module does on your PR message.

## Bug fixes

* Link any corresponding issues in the format of ```See #1234``` in your PR description.
* Explain in a few words how you fixed it in your PR message.

## Bug reports

* Write a detailed description of your bug and use a descriptive title.
* Give as many details as possible about your environment.
* Include steps to reproduce the issue, stack traces and anything that might help us fix your bug.
* Search for your bug in open issues before opening a new issue.

Thank you for taking a few moments to read these contribution guidelines!