"""
Packaging Test
==============

This is the top-level docstring (of the whole package).
"""

from setuptools import find_packages

__all__ = ['adam','adam_6224_ds', 'version']
__doc__ = ""
__author__ = "Patryk Fraczek"
__author_email__ = "pat.fraczekC@gmail.com"

for package_name in find_packages():
    package_import = __import__(package_name)
    __doc__ += "%s: %s" % (package_name, package_import.__doc__)
    __author__ += package_import.__author__ + ", "
    __author_email__ += package_import.__author_email__ + ", "
