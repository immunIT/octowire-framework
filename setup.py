# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup


__authors__ = "Jordan Ovrè, Paul Duncan"
__copyright__ = "Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan"
__license__ = "Apache 2.0"
__version__ = "1.1.3"
__contact__ = "Jordan Ovrè / Ghecko <jovre@immunit.ch>, Paul Duncan / Eresse <pduncan@immunit.ch>"

description = 'Octowire Framework Core'
name = 'octowire_framework'

setup(
    name=name,
    version=__version__,
    packages=find_packages(),
    license=__license__,
    description=description,
    author=__authors__,
    zip_safe=True,
    url='https://github.com/immunIT/octowire-framework',
    install_requires=[
        'prompt_toolkit>=3.0.3,<4',
        'pyserial>=3.4,<4',
        'psutil>=5.6.7',
        'octowire-lib>=1.0.1',
        'colorama>=0.4.3;platform_system=="Windows"',
        'requests>=2.23.0'
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable'
    ],
    keywords=['octowire', 'framework', 'hardware', 'security', 'core', 'engine', 'pentest'],
    entry_points={
            'console_scripts': [
                'owfconsole = octowire_framework.owfconsole:main',
                'owfupdate = octowire_framework.owfupdate:main',
                'owfremove = octowire_framework.owfremove:main',
            ]
    }
)
