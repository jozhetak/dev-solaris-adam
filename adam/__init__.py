"""
Packaging Test
==============

This package contains:

- ADAM6224 device class - ADAM6217 is a 8-ch  Isolated Analog Input Modbus TCP Module
- ADAM6224 device class - ADAM6224 is a 4-ch  Isolated Analog Output Modbus TCP Module with additional 4-ch Digital Input
- ADAM6250 device class - ADAM6250 is a 15-ch  Isolated Digital I/O Modbus TCP Module

For more information and documentation of the device visit http://www.advantech.com/products/ethernet-i-o-modules-with-daisy-chain-adam-6200/sub_7447e150-338d-402d-b5a1-c9ce6d98816e
"""


from setuptools import find_packages

__all__ = ['adam', 'adam_6217', 'adam_6250', 'run_server', 'version']
__doc__ = ""
__author__ = "Patryk Fraczek"
__author_email__ = "pat.fraczekC@gmail.com"
