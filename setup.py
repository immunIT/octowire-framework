# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__authors__ = "Jordan Ovrè, Paul Duncan"
__copyright__ = "Copyright (c) Jordan Ovrè / Paul Duncan"
__license__ = "GPLv3"
__version__ = "0.0.1"
__contact__ = "Jordan Ovrè / Ghecko <ghecko78@gmail.com>, Paul Duncan / Eresse <eresse@dooba.io>"

description = 'Octowire Framework Core'
name = 'octowire_framework'


setup(
    name=name,
    version='0.0.1',
    packages=find_packages(),
    license=__license__,
    description=description,
    author=__authors__,
    url='https://bitbucket.org/dooba_core/octowire-framework/',
    install_requires=[
        'prompt_toolkit>=3.0.2,<4',
        'pyserial>=3.4,<4',
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha'
    ],
    keywords=['octowire', 'framework', 'hardware', 'security', 'core', 'engine', 'pentest'],
    entry_points={
            'console_scripts': [
                'owfconsole = octowire_framework.owfconsole:main',
                'owfupdate = octowire_framework.owfupdate:main',
            ]
    }
)
