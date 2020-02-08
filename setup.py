# -*- coding: utf-8 -*-


import platform
import time
from setuptools import setup, find_packages


__authors__ = "Jordan Ovrè, Paul Duncan"
__copyright__ = "Copyright (c) Jordan Ovrè / Paul Duncan"
__license__ = "GPLv3"
__version__ = "1.0.0"
__contact__ = "Jordan Ovrè / Ghecko <ghecko78@gmail.com>, Paul Duncan / Eresse <eresse@dooba.io>"

description = 'Octowire Framework Core'
name = 'octowire_framework'

# This sleep is necessary when the framework is install from owfupdate.exe on a Windows platform.
if platform.system() == "Windows":
    time.sleep(1)

setup(
    name=name,
    version=__version__,
    packages=find_packages(),
    license=__license__,
    description=description,
    author=__authors__,
    zip_safe=True,
    url='https://bitbucket.org/octowire/octowire-framework/',
    install_requires=[
        'prompt_toolkit>=3.0.3,<4',
        'pyserial>=3.4,<4',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable'
    ],
    keywords=['octowire', 'framework', 'hardware', 'security', 'core', 'engine', 'pentest'],
    entry_points={
            'console_scripts': [
                'owfconsole = octowire_framework.owfconsole:main',
                'owfupdate = octowire_framework.owfupdate:main',
            ]
    }
)
